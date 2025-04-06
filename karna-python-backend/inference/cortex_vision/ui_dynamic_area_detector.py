import logging
from typing import List, Dict, Optional, Tuple, Any
import numpy as np

from .dynamic_area_detector import DynamicAreaDetector, ChangeFrequencyRegion
from .omni_helper import OmniParserResultModelList

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class UIOptimizedDynamicAreaDetector(DynamicAreaDetector):
    """
    Enhanced Dynamic Area Detector optimized for UI layouts.
    
    Extends the base DynamicAreaDetector with specialized detection methods
    for vertical UI layouts where content is typically scrolled vertically.
    """
    
    def __init__(
        self,
        x_overlap_threshold: float = 0.3,  # Minimum x-axis overlap required (as percentage)
        min_vertical_region_height: float = 0.1,  # Minimum height for vertical regions
        **kwargs
    ):
        """
        Initialize the UI-optimized dynamic area detector.
        
        Args:
            x_overlap_threshold: Minimum horizontal overlap required to merge regions vertically
            min_vertical_region_height: Minimum height for vertical regions as fraction of screen
            **kwargs: Arguments passed to parent DynamicAreaDetector
        """
        super().__init__(**kwargs)
        self.x_overlap_threshold = x_overlap_threshold
        self.min_vertical_region_height = min_vertical_region_height
        
        logger.info(f"UIOptimizedDynamicAreaDetector initialized with x_overlap_threshold={x_overlap_threshold}, "
                    f"min_vertical_region_height={min_vertical_region_height}")
    
    def _calculate_x_overlap(self, bbox1: List[float], bbox2: List[float]) -> float:
        """
        Calculate overlap percentage along the x-axis between two bounding boxes.
        
        Args:
            bbox1: First bounding box [x1, y1, x2, y2]
            bbox2: Second bounding box [x1, y1, x2, y2]
            
        Returns:
            Overlap percentage (0-1) along x-axis
        """
        # No overlap case
        if bbox1[2] <= bbox2[0] or bbox2[2] <= bbox1[0]:
            return 0.0
        
        # Calculate intersection
        x_intersection = min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0])
        
        # Calculate width of each box
        width1 = bbox1[2] - bbox1[0]
        width2 = bbox2[2] - bbox2[0]
        
        # Calculate overlap percentage relative to the smaller width
        smaller_width = min(width1, width2)
        if smaller_width <= 0:
            return 0.0
        
        return x_intersection / smaller_width
    
    def _find_largest_area_region(self, dynamic_regions: List[ChangeFrequencyRegion]) -> Optional[ChangeFrequencyRegion]:
        """
        Find the region with the largest area from the list of dynamic regions.
        
        Args:
            dynamic_regions: List of dynamic regions
            
        Returns:
            The ChangeFrequencyRegion with the largest area, or None if list is empty
        """
        if not dynamic_regions:
            return None
        
        return max(dynamic_regions, key=lambda r: r.area)
    
    def _create_vertical_union_regions(
        self, 
        dynamic_regions: List[ChangeFrequencyRegion]
    ) -> List[ChangeFrequencyRegion]:
        """
        Create vertical union regions by merging regions with significant x-axis overlap.
        
        Args:
            dynamic_regions: List of dynamic regions
            
        Returns:
            List of merged vertical ChangeFrequencyRegion objects
        """
        if not dynamic_regions:
            return []
        
        # Find the largest area region first to ensure it's included
        largest_region = self._find_largest_area_region(dynamic_regions)
        if not largest_region:
            return []
            
        # Sort regions by x-position (left to right)
        sorted_regions = sorted(dynamic_regions, key=lambda r: r.bbox[0])
        
        # Start with the largest region as a seed for the first group
        x_groups = [[largest_region]]
        sorted_regions = [r for r in sorted_regions if r != largest_region]
        
        # First, build a group around the largest region
        for region in sorted_regions[:]:
            # Check if region overlaps with largest region
            overlap = self._calculate_x_overlap(largest_region.bbox, region.bbox)
            if overlap >= self.x_overlap_threshold:
                x_groups[0].append(region)
                sorted_regions.remove(region)
        
        # Then process remaining regions into other groups
        for region in sorted_regions:
            # Try to add to existing group
            added = False
            
            for group in x_groups:
                # Check if region has sufficient x-overlap with any region in group
                for group_region in group:
                    overlap = self._calculate_x_overlap(region.bbox, group_region.bbox)
                    if overlap >= self.x_overlap_threshold:
                        group.append(region)
                        added = True
                        break
                
                if added:
                    break
            
            # If not added to any group, create new group
            if not added:
                x_groups.append([region])
        
        # For each x-group, create a vertical union
        vertical_unions = []
        
        for group in x_groups:
            if len(group) < 2:
                # Single region, only include if it's the largest region
                if group[0] == largest_region:
                    vertical_unions.append(largest_region)
                continue
            
            # Use the union of x-coordinates (min of lefts, max of rights)
            # instead of intersection (max of lefts, min of rights)
            x1 = min(r.bbox[0] for r in group)
            x2 = max(r.bbox[2] for r in group)
            
            # Find full y-range
            y1 = min(r.bbox[1] for r in group)
            y2 = max(r.bbox[3] for r in group)
            
            # Calculate aggregate properties
            avg_change_frequency = sum(r.change_frequency for r in group) / len(group)
            avg_saliency = sum(r.saliency for r in group) / len(group)
            
            # Combine change types
            combined_types = {}
            for r in group:
                for change_type, count in r.change_types.items():
                    combined_types[change_type] = combined_types.get(change_type, 0) + count
            
            # Create vertical union region
            vertical_union = ChangeFrequencyRegion(
                bbox=[x1, y1, x2, y2],
                change_frequency=avg_change_frequency,
                change_types=combined_types,
                saliency=avg_saliency
            )
            
            # Only add if height is significant
            height = y2 - y1
            if height >= self.min_vertical_region_height:
                vertical_unions.append(vertical_union)
        
        return vertical_unions
    
    def _select_main_areas(
        self, 
        dynamic_regions: List[ChangeFrequencyRegion]
    ) -> Dict[str, Any]:
        """
        Override parent method to add vertical union-based selections.
        
        Args:
            dynamic_regions: List of dynamic regions
            
        Returns:
            Dictionary mapping criteria names to selected bboxes
        """
        # Get standard selections from parent method
        result = super()._select_main_areas(dynamic_regions)
        
        # Add vertical union based selections
        result["vertical_union"] = None
        result["main_content_area"] = None
        
        # Create vertical unions
        vertical_unions = self._create_vertical_union_regions(dynamic_regions)
        
        if vertical_unions:
            # Find largest vertical union by area
            largest_union = max(vertical_unions, key=lambda r: r.area, default=None)
            if largest_union:
                result["vertical_union"] = largest_union.bbox
            
            # Find main content area - prioritize larger, more central vertical regions
            screen_center = (0.5, 0.5)
            
            # Ensure main_content_area contains largest_area if possible
            largest_area_bbox = result.get("largest_area")
            
            if largest_area_bbox:
                # Find unions that contain the largest area
                containing_unions = []
                for union in vertical_unions:
                    largest_contained = (
                        union.bbox[0] <= largest_area_bbox[0] and
                        union.bbox[1] <= largest_area_bbox[1] and
                        union.bbox[2] >= largest_area_bbox[2] and
                        union.bbox[3] >= largest_area_bbox[3]
                    )
                    
                    largest_mostly_contained = (
                        self._calculate_overlap_area(union.bbox, largest_area_bbox) >= 0.7 * 
                        ((largest_area_bbox[2] - largest_area_bbox[0]) * 
                         (largest_area_bbox[3] - largest_area_bbox[1]))
                    )
                    
                    if largest_contained or largest_mostly_contained:
                        containing_unions.append(union)
                
                if containing_unions:
                    # From unions containing largest area, select most suitable
                    content_areas = sorted(
                        containing_unions,
                        key=lambda r: (
                            r.area * 
                            (1 - self._get_distance(r.center, screen_center)) * 
                            r.saliency * 
                            ((r.bbox[3] - r.bbox[1]) / 1.0)  # Height ratio (taller is better)
                        ),
                        reverse=True
                    )
                    
                    if content_areas:
                        result["main_content_area"] = content_areas[0].bbox
                else:
                    # If no union contains the largest area, create one that does
                    largest_region = None
                    for region in dynamic_regions:
                        if region.bbox == largest_area_bbox:
                            largest_region = region
                            break
                    
                    if largest_region:
                        # Find regions that overlap with largest area
                        overlapping_regions = [largest_region]
                        for region in dynamic_regions:
                            if region != largest_region and self._intersect_bboxes(region.bbox, largest_area_bbox):
                                overlapping_regions.append(region)
                        
                        # Create a custom vertical union to ensure it contains largest area
                        custom_union = self._create_custom_vertical_union(overlapping_regions, largest_region)
                        result["main_content_area"] = custom_union.bbox
            
            # If still not set, use general scoring
            if result["main_content_area"] is None and vertical_unions:
                content_areas = sorted(
                    vertical_unions,
                    key=lambda r: (
                        r.area * 
                        (1 - self._get_distance(r.center, screen_center)) * 
                        r.saliency * 
                        ((r.bbox[3] - r.bbox[1]) / 1.0)  # Height ratio (taller is better)
                    ),
                    reverse=True
                )
                
                if content_areas:
                    result["main_content_area"] = content_areas[0].bbox
        
        return result
    
    def _calculate_overlap_area(self, bbox1: List[float], bbox2: List[float]) -> float:
        """
        Calculate the overlap area between two bounding boxes.
        
        Args:
            bbox1: First bounding box [x1, y1, x2, y2]
            bbox2: Second bounding box [x1, y1, x2, y2]
            
        Returns:
            Area of overlap
        """
        # Calculate intersection
        x_intersection = max(0, min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0]))
        y_intersection = max(0, min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1]))
        
        return x_intersection * y_intersection
    
    def _create_custom_vertical_union(
        self, 
        regions: List[ChangeFrequencyRegion],
        largest_region: ChangeFrequencyRegion
    ) -> ChangeFrequencyRegion:
        """
        Create a custom vertical union ensuring it contains the largest region.
        
        Args:
            regions: List of regions to consider
            largest_region: The largest area region that must be included
            
        Returns:
            A custom ChangeFrequencyRegion representing the vertical union
        """
        # Start with the bbox of the largest region
        x1, y1, x2, y2 = largest_region.bbox
        
        # Expand y-range based on other regions with similar x-range
        for region in regions:
            # If region has significant x-overlap with largest region
            overlap = self._calculate_x_overlap(largest_region.bbox, region.bbox)
            if overlap >= self.x_overlap_threshold:
                # Expand the vertical range
                y1 = min(y1, region.bbox[1])
                y2 = max(y2, region.bbox[3])
        
        # Calculate aggregate properties
        avg_change_frequency = sum(r.change_frequency for r in regions) / len(regions)
        avg_saliency = sum(r.saliency for r in regions) / len(regions)
        
        # Combine change types
        combined_types = {}
        for r in regions:
            for change_type, count in r.change_types.items():
                combined_types[change_type] = combined_types.get(change_type, 0) + count
        
        # Create custom vertical union region
        return ChangeFrequencyRegion(
            bbox=[x1, y1, x2, y2],
            change_frequency=avg_change_frequency,
            change_types=combined_types,
            saliency=avg_saliency
        )
    
    def detect_main_areas(
        self, 
        results_list: OmniParserResultModelList
    ) -> Dict[str, Any]:
        """
        Detect dynamic content areas with UI optimization for vertical layouts.
        
        Args:
            results_list: OmniParserResultModelList with results for multiple frames
            
        Returns:
            Dictionary mapping criteria names to selected dynamic area bboxes,
            including vertical union-based areas and all regions
        """
        logger.info(f"Starting UI-optimized dynamic area detection for {len(results_list.omniparser_result_models)} frames")
        
        # Use parent method for basic detection
        result = super().detect_main_areas(results_list)
        
        logger.info("UI-optimized dynamic area detection completed")
        return result 