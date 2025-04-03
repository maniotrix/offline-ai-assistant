import os
import numpy as np
from PIL import Image
from typing import List, Dict, Tuple, Optional, Set, Any
import logging
from dataclasses import dataclass
import itertools

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import necessary components
from .image_comparison import ResNetImageEmbedder
from .omni_helper import OmniParserResultModel, OmniParserResultModelList, ParsedContentResult
from .image_diff_creator import ImageDiffCreator, ImageDiffResults, DiffResult


@dataclass
class ChangeFrequencyRegion:
    """Represents a region with change frequency data."""
    bbox: List[float]  # [x1, y1, x2, y2]
    change_frequency: float  # How often this region changes (0-1)
    change_types: Dict[str, int]  # Count of each change type ("added", "removed", "text-changed", "visual-changed")
    saliency: float  # Importance of this region
    
    @property
    def is_dynamic(self) -> bool:
        """Determine if region is dynamic based on change frequency."""
        return self.change_frequency >= 0.3  # If changes in at least 30% of frame pairs
    
    @property
    def area(self) -> float:
        """Calculate area of this region."""
        width = self.bbox[2] - self.bbox[0]
        height = self.bbox[3] - self.bbox[1]
        return width * height
    
    @property
    def center(self) -> Tuple[float, float]:
        """Calculate center point of this region."""
        return ((self.bbox[0] + self.bbox[2]) / 2, 
                (self.bbox[1] + self.bbox[3]) / 2)
    
    @property
    def dominant_change_type(self) -> str:
        """Return the most frequent change type for this region."""
        if not self.change_types:
            return "unknown"
        return max(self.change_types.items(), key=lambda x: x[1])[0]


class DynamicAreaDetector:
    """
    Detects dynamic content areas in a sequence of screenshots by tracking
    changes between consecutive frames using ImageDiffCreator.
    """
    def __init__(
        self,
        image_diff_creator: Optional[ImageDiffCreator] = None,
        min_change_frequency: float = 0.3,  # Minimum change frequency to consider dynamic
        min_area_size: float = 0.01,        # Minimum area size (as fraction of screen)
        grouping_distance: float = 0.1,     # Distance threshold for grouping regions
        min_saliency: float = 0.1,          # Minimum saliency threshold for regions
    ):
        """
        Initialize the dynamic area detector.
        
        Args:
            image_diff_creator: ImageDiffCreator instance (created if None)
            min_change_frequency: Minimum frequency of changes to consider area dynamic
            min_area_size: Minimum area size as fraction of screen
            grouping_distance: Distance threshold for grouping nearby regions
            min_saliency: Minimum saliency threshold for regions
        """
        # Create ImageDiffCreator if not provided
        self.diff_creator = image_diff_creator or ImageDiffCreator()
        
        self.min_change_frequency = min_change_frequency
        self.min_area_size = min_area_size
        self.grouping_distance = grouping_distance
        self.min_saliency = min_saliency
        
        logger.info(f"DynamicAreaDetector initialized with min_change_frequency>={min_change_frequency}, "
                    f"min_area_size>={min_area_size}, grouping_distance<={grouping_distance}")
    
    def _compare_consecutive_frames(
        self, 
        results_list: OmniParserResultModelList
    ) -> List[ImageDiffResults]:
        """
        Compare each consecutive pair of frames using ImageDiffCreator.
        
        Args:
            results_list: List of OmniParserResultModel objects
            
        Returns:
            List of ImageDiffResults for each frame pair
        """
        diff_results = []
        
        # Need at least 2 frames for comparison
        if len(results_list.omniparser_result_models) < 2:
            logger.warning("Need at least 2 frames for comparison")
            return diff_results
        
        # Compare each consecutive pair
        for i in range(len(results_list.omniparser_result_models) - 1):
            result1 = results_list.omniparser_result_models[i]
            result2 = results_list.omniparser_result_models[i + 1]
            
            logger.info(f"Comparing frames {i} and {i+1}")
            
            try:
                # Compare the two frames
                diff_result = self.diff_creator.compare_results(result1, result2)
                diff_results.append(diff_result)
                
                logger.info(f"Found {len(diff_result.all_changes)} changes between frames {i} and {i+1}")
            except Exception as e:
                logger.error(f"Error comparing frames {i} and {i+1}: {e}")
                # Add empty result to maintain indices
                diff_results.append(ImageDiffResults([], [], [], []))
        
        return diff_results
    
    def _generate_change_heatmap(
        self, 
        diff_results: List[ImageDiffResults], 
        frame_width: int, 
        frame_height: int
    ) -> np.ndarray:
        """
        Generate a heatmap of changes across all frame pairs.
        
        Args:
            diff_results: List of ImageDiffResults from comparing frames
            frame_width: Width of the frames
            frame_height: Height of the frames
            
        Returns:
            2D numpy array where each cell represents change frequency
        """
        # Create empty heatmap (resolution: 100x100)
        heatmap_size = 100
        heatmap = np.zeros((heatmap_size, heatmap_size), dtype=float)
        
        # For each frame diff result
        for diff_result in diff_results:
            # Temporary mask for this frame pair
            frame_mask = np.zeros((heatmap_size, heatmap_size), dtype=bool)
            
            # Process all changes
            for change in diff_result.all_changes:
                # Skip if saliency is too low
                if change.saliency < self.min_saliency:
                    continue
                
                # Normalize bbox to heatmap size
                x1 = int(change.bbox[0] * heatmap_size)
                y1 = int(change.bbox[1] * heatmap_size)
                x2 = int(change.bbox[2] * heatmap_size)
                y2 = int(change.bbox[3] * heatmap_size)
                
                # Ensure valid coordinates
                x1 = max(0, min(x1, heatmap_size - 1))
                y1 = max(0, min(y1, heatmap_size - 1))
                x2 = max(0, min(x2, heatmap_size))
                y2 = max(0, min(y2, heatmap_size))
                
                # Mark changed area on frame mask
                if x2 > x1 and y2 > y1:
                    frame_mask[y1:y2, x1:x2] = True
            
            # Add frame mask to overall heatmap (if any changes)
            if np.any(frame_mask):
                heatmap += frame_mask.astype(float)
        
        # Normalize heatmap to change frequency (0-1)
        if diff_results:
            heatmap /= len(diff_results)
        
        return heatmap
    
    def _extract_change_regions(
        self, 
        heatmap: np.ndarray,
        diff_results: List[ImageDiffResults]
    ) -> List[ChangeFrequencyRegion]:
        """
        Extract regions with significant change frequency from heatmap.
        
        Args:
            heatmap: Change frequency heatmap
            diff_results: List of ImageDiffResults from comparing frames
            
        Returns:
            List of ChangeFrequencyRegion objects
        """
        # Extract areas with change frequency above threshold
        change_regions = []
        
        # Collect all change bboxes with their types
        all_changes = []
        for diff_result in diff_results:
            for change in diff_result.all_changes:
                if change.saliency >= self.min_saliency:
                    all_changes.append(change)
        
        # Group changes by intersecting bounding boxes
        while all_changes:
            base_change = all_changes.pop(0)
            group = [base_change]
            
            # Find all changes that intersect with base_change
            i = 0
            while i < len(all_changes):
                if self._intersect_bboxes(base_change.bbox, all_changes[i].bbox):
                    group.append(all_changes.pop(i))
                else:
                    i += 1
            
            # Calculate merged bbox for this group
            merged_bbox = self._merge_bboxes([c.bbox for c in group])
            
            # Calculate change frequency for this region
            # (how many frame pairs contain changes in this region)
            frame_pairs_with_changes = set()
            change_types = {"added": 0, "removed": 0, "text-changed": 0, "visual-changed": 0}
            
            for diff_idx, diff_result in enumerate(diff_results):
                for change in diff_result.all_changes:
                    if self._intersect_bboxes(merged_bbox, change.bbox):
                        frame_pairs_with_changes.add(diff_idx)
                        change_types[change.type] += 1
            
            change_frequency = len(frame_pairs_with_changes) / len(diff_results) if diff_results else 0
            
            # Calculate average saliency
            avg_saliency = sum(c.saliency for c in group) / len(group)
            
            # Create region
            region = ChangeFrequencyRegion(
                bbox=merged_bbox,
                change_frequency=change_frequency,
                change_types=change_types,
                saliency=avg_saliency
            )
            
            # Only add if area is large enough and frequency is high enough
            area = (merged_bbox[2] - merged_bbox[0]) * (merged_bbox[3] - merged_bbox[1])
            if area >= self.min_area_size and change_frequency >= self.min_change_frequency:
                change_regions.append(region)
        
        return change_regions
    
    def _group_change_regions(self, regions: List[ChangeFrequencyRegion]) -> List[ChangeFrequencyRegion]:
        """
        Group nearby change regions into larger coherent regions.
        
        Args:
            regions: List of ChangeFrequencyRegion objects
            
        Returns:
            List of merged ChangeFrequencyRegion objects
        """
        if not regions:
            return []
        
        # Start with each region in its own group
        groups = [[region] for region in regions]
        
        # Merge groups if regions are close enough
        merged = True
        while merged:
            merged = False
            for i in range(len(groups)):
                if i >= len(groups):  # Safety check
                    break
                    
                for j in range(i + 1, len(groups)):
                    if j >= len(groups):  # Safety check
                        break
                        
                    # Check if any regions in the groups are close enough
                    if self._should_merge_region_groups(groups[i], groups[j]):
                        # Merge groups
                        groups[i].extend(groups[j])
                        groups.pop(j)
                        merged = True
                        break
        
        # Convert groups back to regions (merge properties)
        merged_regions = []
        for group in groups:
            if not group:
                continue
                
            # Merge bboxes
            merged_bbox = self._merge_bboxes([r.bbox for r in group])
            
            # Average change frequency and saliency
            avg_change_freq = sum(r.change_frequency for r in group) / len(group)
            avg_saliency = sum(r.saliency for r in group) / len(group)
            
            # Combine change types
            combined_types = {}
            for r in group:
                for change_type, count in r.change_types.items():
                    combined_types[change_type] = combined_types.get(change_type, 0) + count
            
            # Create merged region
            merged_regions.append(ChangeFrequencyRegion(
                bbox=merged_bbox,
                change_frequency=avg_change_freq,
                change_types=combined_types,
                saliency=avg_saliency
            ))
        
        return merged_regions
    
    def _should_merge_region_groups(
        self, 
        group1: List[ChangeFrequencyRegion], 
        group2: List[ChangeFrequencyRegion]
    ) -> bool:
        """
        Determine if two region groups should be merged based on proximity.
        
        Args:
            group1: First group of regions
            group2: Second group of regions
            
        Returns:
            True if groups should be merged, False otherwise
        """
        for r1 in group1:
            for r2 in group2:
                # Check if regions are close or intersecting
                if self._intersect_bboxes(r1.bbox, r2.bbox):
                    return True
                    
                # Check center distance
                distance = self._get_distance(r1.center, r2.center)
                if distance <= self.grouping_distance:
                    return True
        
        return False
    
    def _get_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def _intersect_bboxes(self, bbox1: List[float], bbox2: List[float]) -> bool:
        """Check if two bounding boxes intersect."""
        # Check if one bbox is to the left of the other
        if bbox1[2] <= bbox2[0] or bbox2[2] <= bbox1[0]:
            return False
        
        # Check if one bbox is above the other
        if bbox1[3] <= bbox2[1] or bbox2[3] <= bbox1[1]:
            return False
        
        return True
    
    def _merge_bboxes(self, bboxes: List[List[float]]) -> List[float]:
        """Merge multiple bounding boxes into one encompassing all."""
        if not bboxes:
            return [0, 0, 0, 0]
            
        x1 = min(bbox[0] for bbox in bboxes)
        y1 = min(bbox[1] for bbox in bboxes)
        x2 = max(bbox[2] for bbox in bboxes)
        y2 = max(bbox[3] for bbox in bboxes)
        
        return [x1, y1, x2, y2]
    
    def _select_main_areas(
        self, 
        dynamic_regions: List[ChangeFrequencyRegion]
    ) -> Dict[str, Optional[List[float]]]:
        """
        Select main dynamic areas based on different criteria.
        
        Args:
            dynamic_regions: List of dynamic regions
            
        Returns:
            Dictionary mapping criteria names to selected bboxes
        """
        result: Dict[str, Optional[List[float]]] = {
            "largest_area": None,
            "center_weighted": None,
            "highest_frequency": None,
        }
        
        if not dynamic_regions:
            return result
        
        # Sort regions by different criteria
        
        # 1. Largest area
        largest_region = max(dynamic_regions, key=lambda r: r.area, default=None)
        if largest_region:
            result["largest_area"] = largest_region.bbox
        
        # 2. Center-weighted (favor areas in the middle of the screen)
        screen_center = (0.5, 0.5)
        
        # Score = area * (1 - distance_to_center) * saliency
        center_weighted_regions = sorted(
            dynamic_regions,
            key=lambda r: (
                r.area * 
                (1 - self._get_distance(r.center, screen_center)) * 
                r.saliency
            ),
            reverse=True
        )
        
        if center_weighted_regions:
            result["center_weighted"] = center_weighted_regions[0].bbox
        
        # 3. Highest change frequency
        most_dynamic_region = max(dynamic_regions, key=lambda r: r.change_frequency, default=None)
        if most_dynamic_region:
            result["highest_frequency"] = most_dynamic_region.bbox
        
        return result
    
    def detect_main_areas(
        self, 
        results_list: OmniParserResultModelList
    ) -> Dict[str, Optional[List[float]]]:
        """
        Main method to detect dynamic content areas from a sequence of screenshots.
        
        Args:
            results_list: OmniParserResultModelList with results for multiple frames
            
        Returns:
            Dictionary mapping criteria names to selected dynamic area bboxes
        """
        logger.info(f"Starting dynamic area detection for {len(results_list.omniparser_result_models)} frames")
        
        default_result: Dict[str, Optional[List[float]]] = {
            "largest_area": None,
            "center_weighted": None,
            "highest_frequency": None,
        }
        
        # Ensure we have at least 2 frames
        if len(results_list.omniparser_result_models) < 2:
            logger.warning("Need at least 2 frames for dynamic area detection")
            return default_result
        
        try:
            # Step 1: Compare consecutive frame pairs using ImageDiffCreator
            diff_results = self._compare_consecutive_frames(results_list)
            
            if not diff_results:
                logger.warning("No valid frame comparisons")
                return default_result
            
            # Get frame dimensions from first result
            frame_width = results_list.omniparser_result_models[0].omniparser_result.original_image_width
            frame_height = results_list.omniparser_result_models[0].omniparser_result.original_image_height
            
            # Step 2: Generate change frequency heatmap
            heatmap = self._generate_change_heatmap(diff_results, frame_width, frame_height)
            
            # Step 3: Extract regions with significant change frequency
            change_regions = self._extract_change_regions(heatmap, diff_results)
            
            # Step 4: Group nearby regions
            grouped_regions = self._group_change_regions(change_regions)
            
            # Step 5: Filter for dynamic regions only
            dynamic_regions = [r for r in grouped_regions if r.is_dynamic]
            
            logger.info(f"Identified {len(dynamic_regions)} dynamic regions from {len(diff_results)} frame pairs")
            
            # Step 6: Select main areas based on different criteria
            result = self._select_main_areas(dynamic_regions)
            
            logger.info("Dynamic area detection completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during dynamic area detection: {e}", exc_info=True)
            return default_result
