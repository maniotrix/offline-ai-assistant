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


@dataclass
class TrackedElement:
    """Represents an element tracked across frames."""
    element_id: int  # Original ID from ParsedContentResult
    frame_indexes: List[int]  # List of frame indexes where this element appears
    bbox_list: List[List[float]]  # Bounding boxes for each occurrence [frame_index -> bbox]
    content_list: List[Optional[str]]  # Content for each occurrence
    embedding_list: List[np.ndarray]  # Visual embeddings for each occurrence
    source_type: str  # Element source type
    
    @property
    def persistence_score(self) -> float:
        """Fraction of frames where this element appears."""
        return len(self.frame_indexes) / (max(self.frame_indexes) + 1 if self.frame_indexes else 1)
    
    @property
    def is_static(self) -> bool:
        """Determine if element is static based on content stability."""
        # If fewer than 2 occurrences, not enough data
        if len(self.frame_indexes) < 2:
            return False
            
        # For text elements, check text content stability
        if self.source_type in ['box_ocr_content_ocr', 'box_yolo_content_ocr'] and any(self.content_list):
            # Filter out None values
            contents = [c for c in self.content_list if c]
            if not contents:
                # No valid content to compare
                return self._check_visual_stability()
                
            # Check if all contents are the same
            return len(set(contents)) == 1
        else:
            # For visual-only elements, check embedding similarity
            return self._check_visual_stability()
    
    def _check_visual_stability(self) -> bool:
        """Check if visual appearance is stable across occurrences."""
        if len(self.embedding_list) < 2:
            return False
            
        # Calculate pairwise similarities between all embeddings
        similarities = []
        for i in range(len(self.embedding_list)):
            for j in range(i+1, len(self.embedding_list)):
                similarity = np.dot(self.embedding_list[i], self.embedding_list[j])
                similarities.append(similarity)
                
        # If average similarity is high, consider static
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        return avg_similarity > 0.85  # High threshold for stability
    
    @property
    def is_dynamic(self) -> bool:
        """Element is dynamic if it's not static."""
        return not self.is_static
    
    @property
    def average_bbox(self) -> List[float]:
        """Calculate average bounding box across occurrences."""
        if not self.bbox_list:
            return [0, 0, 0, 0]
            
        # Calculate average coordinates
        x1 = sum(bbox[0] for bbox in self.bbox_list) / len(self.bbox_list)
        y1 = sum(bbox[1] for bbox in self.bbox_list) / len(self.bbox_list)
        x2 = sum(bbox[2] for bbox in self.bbox_list) / len(self.bbox_list)
        y2 = sum(bbox[3] for bbox in self.bbox_list) / len(self.bbox_list)
        
        return [x1, y1, x2, y2]


class DynamicAreaDetector:
    """
    Detects dynamic content areas in a sequence of screenshots by tracking
    elements and analyzing their changes across frames.
    """
    def __init__(
        self,
        embedder: ResNetImageEmbedder,
        similarity_threshold: float = 0.8,  # Threshold for visual similarity
        proximity_threshold: float = 0.1,   # Distance threshold for element matching
        min_persistence: float = 0.5,       # Minimum persistence for reliable elements
        min_area_size: float = 0.01,        # Minimum area size (as fraction of screen)
        grouping_distance: float = 0.1      # Distance threshold for grouping elements
    ):
        """
        Initialize the dynamic area detector.
        
        Args:
            embedder: ResNet embedder for visual similarity
            similarity_threshold: Threshold for visual similarity (0-1)
            proximity_threshold: Max distance for element center matching
            min_persistence: Minimum fraction of frames an element must appear in
            min_area_size: Minimum area size as fraction of screen
            grouping_distance: Distance threshold for grouping nearby elements
        """
        self.embedder = embedder
        self.similarity_threshold = similarity_threshold
        self.proximity_threshold = proximity_threshold
        self.min_persistence = min_persistence
        self.min_area_size = min_area_size
        self.grouping_distance = grouping_distance
        
        logger.info(f"DynamicAreaDetector initialized with similarity>={similarity_threshold}, "
                    f"proximity<={proximity_threshold}, min_persistence>={min_persistence}")
    
    def _extract_elements(self, results_list: OmniParserResultModelList) -> List[List[Tuple[int, ParsedContentResult, np.ndarray]]]:
        """
        Extract elements from each frame with their embeddings.
        
        Returns:
            List of lists, where each inner list contains tuples of 
            (element_id, parsed_content, embedding) for a single frame
        """
        all_frame_elements = []
        
        for frame_idx, result_model in enumerate(results_list.omniparser_result_models):
            frame_elements = []
            screenshot_path = result_model.omniparser_result.original_image_path
            
            logger.info(f"Extracting elements from frame {frame_idx}: {os.path.basename(screenshot_path)}")
            
            # Skip if file doesn't exist
            if not os.path.exists(screenshot_path):
                logger.error(f"Screenshot not found: {screenshot_path}")
                all_frame_elements.append([])
                continue
                
            try:
                # Load the image
                img = Image.open(screenshot_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                img_width, img_height = img.size
                
                # Process each element
                for pcr in result_model.parsed_content_results:
                    try:
                        bbox = pcr.bbox
                        
                        # Ensure bbox is valid
                        if len(bbox) != 4 or not all(isinstance(x, (int, float)) for x in bbox):
                            continue
                        
                        # Convert to absolute coordinates if needed
                        if max(bbox) <= 1.0:
                            # Normalized coordinates [0-1]
                            x1_abs = int(bbox[0] * img_width)
                            y1_abs = int(bbox[1] * img_height)
                            x2_abs = int(bbox[2] * img_width)
                            y2_abs = int(bbox[3] * img_height)
                        else:
                            # Already absolute
                            x1_abs, y1_abs, x2_abs, y2_abs = map(int, bbox)
                        
                        # Ensure valid dimensions
                        if x1_abs >= x2_abs or y1_abs >= y2_abs:
                            # Try to fix tiny areas
                            x2_abs = max(x1_abs + 1, x2_abs)
                            y2_abs = max(y1_abs + 1, y2_abs)
                            
                            # If still invalid, skip
                            if x1_abs >= x2_abs or y1_abs >= y2_abs:
                                continue
                        
                        # Extract image patch
                        patch = img.crop((x1_abs, y1_abs, x2_abs, y2_abs))
                        
                        # Skip very small patches
                        if patch.width < 5 or patch.height < 5:
                            continue
                            
                        # Get embedding
                        embedding = self.embedder.get_embedding(patch)
                        
                        # Store element
                        frame_elements.append((pcr.id, pcr, embedding))
                        
                    except Exception as e:
                        logger.error(f"Error processing element {pcr.id}: {e}")
            
            except Exception as e:
                logger.error(f"Error processing frame {frame_idx}: {e}")
                
            logger.info(f"Extracted {len(frame_elements)} elements from frame {frame_idx}")
            all_frame_elements.append(frame_elements)
            
        return all_frame_elements
    
    def _get_element_center(self, bbox: List[float]) -> Tuple[float, float]:
        """Calculate the center point of a bounding box."""
        return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
    
    def _get_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def _track_elements(self, frame_elements: List[List[Tuple[int, ParsedContentResult, np.ndarray]]]) -> List[TrackedElement]:
        """
        Track elements across frames based on visual similarity and position.
        
        Args:
            frame_elements: List of lists, each containing elements for one frame
            
        Returns:
            List of TrackedElement objects
        """
        tracked_elements = []
        
        # Skip if we have fewer than 2 frames
        if len(frame_elements) < 2:
            logger.warning("Need at least 2 frames for tracking")
            return tracked_elements
            
        # Initialize tracking with first frame
        for element_id, pcr, embedding in frame_elements[0]:
            tracked_elements.append(TrackedElement(
                element_id=element_id,
                frame_indexes=[0],
                bbox_list=[pcr.bbox],
                content_list=[pcr.content],
                embedding_list=[embedding],
                source_type=pcr.source
            ))
        
        # Process subsequent frames
        for frame_idx in range(1, len(frame_elements)):
            current_frame = frame_elements[frame_idx]
            matched_elements = set()
            
            # For each tracked element, try to find a match in current frame
            for tracked_elem in tracked_elements:
                if not tracked_elem.embedding_list:
                    continue
                    
                # Get the most recent occurrence of this element
                last_embedding = tracked_elem.embedding_list[-1]
                last_bbox = tracked_elem.bbox_list[-1]
                last_center = self._get_element_center(last_bbox)
                
                best_match = None
                best_similarity = -1
                
                for element_id, pcr, embedding in current_frame:
                    # Skip if already matched
                    if element_id in matched_elements:
                        continue
                    
                    # Check visual similarity
                    similarity = np.dot(last_embedding, embedding)
                    
                    if similarity >= self.similarity_threshold:
                        # Check position proximity
                        current_center = self._get_element_center(pcr.bbox)
                        distance = self._get_distance(last_center, current_center)
                        
                        if distance <= self.proximity_threshold:
                            # If better match than previous
                            if similarity > best_similarity:
                                best_similarity = similarity
                                best_match = (element_id, pcr, embedding)
                
                # If we found a match, extend the tracked element
                if best_match:
                    element_id, pcr, embedding = best_match
                    tracked_elem.frame_indexes.append(frame_idx)
                    tracked_elem.bbox_list.append(pcr.bbox)
                    tracked_elem.content_list.append(pcr.content)
                    tracked_elem.embedding_list.append(embedding)
                    matched_elements.add(element_id)
            
            # Create new tracked elements for unmatched elements in current frame
            for element_id, pcr, embedding in current_frame:
                if element_id not in matched_elements:
                    tracked_elements.append(TrackedElement(
                        element_id=element_id,
                        frame_indexes=[frame_idx],
                        bbox_list=[pcr.bbox],
                        content_list=[pcr.content],
                        embedding_list=[embedding],
                        source_type=pcr.source
                    ))
        
        logger.info(f"Tracked {len(tracked_elements)} elements across {len(frame_elements)} frames")
        return tracked_elements
    
    def _filter_reliable_elements(self, elements: List[TrackedElement], total_frames: int) -> Tuple[List[TrackedElement], List[TrackedElement]]:
        """
        Filter elements to get those that are reliable (appear in enough frames)
        and classify them as static or dynamic.
        
        Returns:
            Tuple of (static_elements, dynamic_elements)
        """
        if total_frames < 2:
            return [], []
            
        # Filter for reliable elements
        reliable_elements = [elem for elem in elements 
                            if len(elem.frame_indexes) >= max(2, int(total_frames * self.min_persistence))]
                            
        # Separate static and dynamic elements
        static_elements = [elem for elem in reliable_elements if elem.is_static]
        dynamic_elements = [elem for elem in reliable_elements if elem.is_dynamic]
        
        logger.info(f"Classified {len(static_elements)} static and {len(dynamic_elements)} dynamic elements "
                   f"out of {len(reliable_elements)} reliable elements")
        
        return static_elements, dynamic_elements
    
    def _group_dynamic_elements(self, dynamic_elements: List[TrackedElement]) -> List[List[TrackedElement]]:
        """
        Group dynamic elements that are close to each other spatially.
        
        Returns:
            List of element groups (each group is a list of elements)
        """
        if not dynamic_elements:
            return []
            
        # Start with each element in its own group
        groups = [[elem] for elem in dynamic_elements]
        
        # Iteratively merge groups until no more merges are possible
        merged = True
        while merged and len(groups) > 1:
            merged = False
            
            for i in range(len(groups)):
                if i >= len(groups):  # Safety check in case groups shrink
                    break
                    
                group1 = groups[i]
                
                for j in range(i+1, len(groups)):
                    if j >= len(groups):  # Safety check
                        break
                        
                    group2 = groups[j]
                    
                    # Check if groups should be merged
                    if self._should_merge_groups(group1, group2):
                        # Merge group2 into group1
                        groups[i] = group1 + group2
                        # Remove group2
                        groups.pop(j)
                        merged = True
                        break
        
        logger.info(f"Grouped {len(dynamic_elements)} dynamic elements into {len(groups)} groups")
        return groups
    
    def _should_merge_groups(self, group1: List[TrackedElement], group2: List[TrackedElement]) -> bool:
        """
        Determine if two element groups should be merged based on proximity.
        
        Returns:
            True if groups should be merged, False otherwise
        """
        # Get all pairwise distances between elements in both groups
        for elem1 in group1:
            center1 = self._get_element_center(elem1.average_bbox)
            
            for elem2 in group2:
                center2 = self._get_element_center(elem2.average_bbox)
                
                # If any pair is close enough, merge the groups
                if self._get_distance(center1, center2) <= self.grouping_distance:
                    return True
        
        return False
    
    def _calculate_group_bbox(self, group: List[TrackedElement]) -> List[float]:
        """
        Calculate the bounding box that encompasses all elements in a group.
        
        Returns:
            [x1, y1, x2, y2] bounding box
        """
        if not group:
            return [0, 0, 0, 0]
            
        # Collect all bboxes from all elements
        all_bboxes = []
        for elem in group:
            all_bboxes.append(elem.average_bbox)
            
        # Find min/max coordinates
        x1 = min(bbox[0] for bbox in all_bboxes)
        y1 = min(bbox[1] for bbox in all_bboxes)
        x2 = max(bbox[2] for bbox in all_bboxes)
        y2 = max(bbox[3] for bbox in all_bboxes)
        
        # Ensure coordinates are within [0,1]
        x1 = max(0.0, min(1.0, x1))
        y1 = max(0.0, min(1.0, y1))
        x2 = max(0.0, min(1.0, x2))
        y2 = max(0.0, min(1.0, y2))
        
        # Ensure x2 > x1 and y2 > y1
        x2 = max(x1 + 0.01, x2)
        y2 = max(y1 + 0.01, y2)
        
        return [x1, y1, x2, y2]
    
    def _select_main_areas(self, group_bboxes: List[List[float]]) -> Dict[str, Optional[List[float]]]:
        """
        Select main areas based on different criteria.
        
        Returns:
            Dictionary mapping criteria names to selected bboxes
        """
        result = {
            "largest_area": None,
            "center_weighted": None
        }
        
        if not group_bboxes:
            return result
            
        # Only one bbox? It's the main area for all criteria
        if len(group_bboxes) == 1:
            for key in result:
                result[key] = group_bboxes[0]
            return result
            
        # Multiple bboxes - apply different selection criteria
        
        # 1. Largest area
        largest_area = 0
        largest_bbox = None
        
        for bbox in group_bboxes:
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area > largest_area:
                largest_area = area
                largest_bbox = bbox
                
        result["largest_area"] = largest_bbox
        
        # 2. Center-weighted (favor areas in the middle of the screen)
        best_score = -1
        best_bbox = None
        
        screen_center = (0.5, 0.5)
        
        for bbox in group_bboxes:
            # Calculate center of bbox
            center = self._get_element_center(bbox)
            
            # Calculate area
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            
            # Distance from screen center (normalized to [0,1])
            distance = self._get_distance(center, screen_center)
            
            # Score = area * (1 - normalized_distance)
            # This favors larger areas that are closer to center
            score = area * (1 - distance)
            
            if score > best_score:
                best_score = score
                best_bbox = bbox
                
        result["center_weighted"] = best_bbox
        
        return result
    
    def detect_main_areas(self, results_list: OmniParserResultModelList) -> Dict[str, Optional[List[float]]]:
        """
        Main method to detect dynamic content areas from a sequence of screenshots.
        
        Args:
            results_list: OmniParserResultModelList with results for multiple frames
            
        Returns:
            Dictionary mapping criteria names to selected dynamic area bboxes
        """
        logger.info(f"Starting dynamic area detection for {len(results_list.omniparser_result_models)} frames")
        
        default_result = {
            "largest_area": None,
            "center_weighted": None
        }
        
        # Ensure we have at least 2 frames
        if len(results_list.omniparser_result_models) < 2:
            logger.warning("Need at least 2 frames for dynamic area detection")
            return default_result
            
        try:
            # Step 1: Extract elements from each frame
            frame_elements = self._extract_elements(results_list)
            
            # Step 2: Track elements across frames
            tracked_elements = self._track_elements(frame_elements)
            
            # Step 3: Filter and classify elements
            static_elements, dynamic_elements = self._filter_reliable_elements(
                tracked_elements, len(results_list.omniparser_result_models))
                
            # If no dynamic elements, return default result
            if not dynamic_elements:
                logger.warning("No dynamic elements found")
                return default_result
                
            # Step 4: Group dynamic elements spatially
            element_groups = self._group_dynamic_elements(dynamic_elements)
            
            # Step 5: Calculate bounding box for each group
            group_bboxes = []
            
            for group in element_groups:
                bbox = self._calculate_group_bbox(group)
                
                # Skip too small areas
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                if area >= self.min_area_size:
                    group_bboxes.append(bbox)
            
            # Step 6: Select main areas based on different criteria
            result = self._select_main_areas(group_bboxes)
            
            logger.info("Dynamic area detection completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during dynamic area detection: {e}", exc_info=True)
            return default_result
