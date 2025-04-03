import os
import numpy as np
import cv2
from PIL import Image
import Levenshtein
from dataclasses import dataclass
from typing import List, Optional, Literal, Dict, Union, Tuple, Set
import logging

from image_comparison import ResNetImageEmbedder
from omni_helper import OmniParserResultModel, ParsedContentResult

logger = logging.getLogger(__name__)

@dataclass
class DiffResult:
    """Result of a single element difference between two images"""
    type: Literal["added", "removed", "text-changed", "visual-changed"]
    bbox: List[float]  # Format [x1, y1, x2, y2]
    element_type: str  # Type from OmniParser (e.g., "button", "text")
    source: str  # Source from OmniParser (e.g., "box_ocr_content_ocr")
    saliency: float
    element_id: int
    old_content: Optional[str] = None  # For text changes
    new_content: Optional[str] = None  # For text changes
    similarity_score: Optional[float] = None  # For visual changes
    visual_diff_ratio: Optional[float] = None  # For visual changes
    classification: Optional[str] = None  # For visual changes (identical, similar, related, different)
    
@dataclass
class ImageDiffResults:
    """Complete results of comparing two images"""
    added: List[DiffResult]
    removed: List[DiffResult]
    text_changed: List[DiffResult]
    visual_changed: List[DiffResult]
    
    @property
    def all_changes(self) -> List[DiffResult]:
        """Return all changes sorted by saliency"""
        all_diffs = self.added + self.removed + self.text_changed + self.visual_changed
        return sorted(all_diffs, key=lambda x: x.saliency, reverse=True)
    
    @property
    def has_changes(self) -> bool:
        """Check if there are any changes"""
        return len(self.all_changes) > 0
    
    def to_dict(self) -> Dict:
        """Convert results to dictionary for serialization"""
        return {
            "added": [diff.__dict__ for diff in self.added],
            "removed": [diff.__dict__ for diff in self.removed],
            "text_changed": [diff.__dict__ for diff in self.text_changed],
            "visual_changed": [diff.__dict__ for diff in self.visual_changed]
        }


class ImageDiffCreator:
    """
    A class for detecting meaningful differences between UI screenshots.
    Uses a hybrid approach combining bounding box IoU, deep learning embeddings, 
    and pixel-level difference detection.
    """
    
    # Known source types from OmniParser
    KNOWN_SOURCE_TYPES = ['box_ocr_content_ocr', 'box_yolo_content_yolo', 'box_yolo_content_ocr']
    
    def __init__(
        self, 
        model_name: str = 'resnet50',
        source_types: Optional[List[str]] = None,
        saliency_threshold: float = 0.1,
        text_similarity_threshold: float = 0.8,
        visual_change_threshold: float = 0.1,
        pixel_diff_threshold: int = 25,
        device: Optional[str] = None
    ):
        """
        Initialize the ImageDiffCreator.
        
        Args:
            model_name: Name of the ResNet model to use ('resnet18', 'resnet34', 'resnet50')
            source_types: List of source types to include (default: all known types)
            saliency_threshold: Minimum saliency score for changes to be included (0-1)
            text_similarity_threshold: Threshold for text similarity (0-1, higher means more similar)
            visual_change_threshold: Threshold for visual difference ratio (0-1)
            pixel_diff_threshold: Threshold for pixel intensity differences (0-255)
            device: Device to run inference on ('cuda', 'cpu'). If None, will use CUDA if available.
        """
        # Set source types to filter by
        self.source_types = set(source_types) if source_types else set(self.KNOWN_SOURCE_TYPES)
        
        # Validate source types
        unknown_sources = self.source_types - set(self.KNOWN_SOURCE_TYPES)
        if unknown_sources:
            logger.warning(f"Unknown source types specified: {unknown_sources}")
            logger.warning(f"Valid source types are: {self.KNOWN_SOURCE_TYPES}")
        
        # Store other parameters
        self.saliency_threshold = saliency_threshold
        self.text_similarity_threshold = text_similarity_threshold
        self.visual_change_threshold = visual_change_threshold
        self.pixel_diff_threshold = pixel_diff_threshold
        
        # Initialize ResNet embedder for visual similarity
        self.embedder = ResNetImageEmbedder(model_name=model_name, device=device)
    
    def compute_iou(self, bbox1: List[float], bbox2: List[float]) -> float:
        """
        Compute Intersection over Union for two bounding boxes.
        
        Args:
            bbox1: First bounding box [x1, y1, x2, y2]
            bbox2: Second bounding box [x1, y1, x2, y2]
            
        Returns:
            float: IoU score (0-1)
        """
        # Convert bboxes to [x1, y1, x2, y2] if not already
        x1_1, y1_1, x2_1, y2_1 = bbox1
        x1_2, y1_2, x2_2, y2_2 = bbox2
        
        # Compute intersection area
        intersect_x1 = max(x1_1, x1_2)
        intersect_y1 = max(y1_1, y1_2)
        intersect_x2 = min(x2_1, x2_2)
        intersect_y2 = min(y2_1, y2_2)
        
        if intersect_x2 <= intersect_x1 or intersect_y2 <= intersect_y1:
            return 0.0  # No intersection
        
        intersection_area = (intersect_x2 - intersect_x1) * (intersect_y2 - intersect_y1)
        
        # Compute union area
        bbox1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        bbox2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = bbox1_area + bbox2_area - intersection_area
        
        # Compute IoU
        iou = intersection_area / union_area if union_area > 0 else 0.0
        
        return iou
    
    def get_adaptive_iou_threshold(self, element_type: str, source: str) -> float:
        """
        Return appropriate IoU threshold based on element type and source.
        
        Args:
            element_type: Element type from OmniParser
            source: Source type from OmniParser
            
        Returns:
            float: Adaptive IoU threshold
        """
        # Lower threshold for text elements (OCR)
        if source == 'box_ocr_content_ocr':
            return 0.3
        
        # Higher threshold for icon/image elements (YOLO)
        if source == 'box_yolo_content_yolo':
            return 0.5
        
        # Medium threshold for mixed elements (YOLO+OCR)
        return 0.4
    
    def compute_saliency(self, bbox: List[float], image_width: int, image_height: int) -> float:
        """
        Compute the saliency of an element based on its size and position.
        
        Args:
            bbox: Bounding box [x1, y1, x2, y2]
            image_width: Width of the image
            image_height: Height of the image
            
        Returns:
            float: Saliency score (higher is more important)
        """
        # Calculate area
        x1, y1, x2, y2 = bbox
        area = (x2 - x1) * (y2 - y1)
        normalized_area = area / (image_width * image_height)
        
        # Calculate center bias
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        image_center_x = image_width / 2
        image_center_y = image_height / 2
        
        # Normalized distance from center (0-1, where 0 is at center)
        center_dist = np.sqrt(((center_x - image_center_x) / image_width) ** 2 + 
                              ((center_y - image_center_y) / image_height) ** 2)
        center_bias = 1 - min(center_dist, 1.0)  # Closer to center = higher value
        
        # Combine area and center bias for final saliency
        # Weight area more than center position (0.7 vs 0.3)
        saliency = (0.7 * normalized_area) + (0.3 * center_bias)
        
        return saliency
    
    def extract_element_image(self, 
                             result_model: OmniParserResultModel, 
                             element: ParsedContentResult) -> Image.Image:
        """
        Extract image of an element from an OmniParserResultModel.
        
        Args:
            result_model: OmniParserResultModel containing the element
            element: ParsedContentResult of the element to extract
            
        Returns:
            PIL.Image: Extracted image of the element
        """
        # Get original image path
        image_path = result_model.omniparser_result.original_image_path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Original image not found: {image_path}")
        
        # Load image
        full_image = Image.open(image_path).convert("RGB")
        
        # Extract element using bbox
        bbox = [int(coord) for coord in element.bbox]
        x1, y1, x2, y2 = bbox
        
        # Extract the sub-image
        element_image = full_image.crop((x1, y1, x2, y2))
        
        return element_image
    
    def match_elements(self, 
                      result1: OmniParserResultModel, 
                      result2: OmniParserResultModel) -> Dict[int, int]:
        """
        Match elements from result1 to result2 using adaptive IoU and visual similarity.
        
        Args:
            result1: First OmniParserResultModel
            result2: Second OmniParserResultModel
            
        Returns:
            Dict[int, int]: Mapping of element IDs from result1 to result2
        """
        matches = {}  # Maps element IDs from result1 to result2
        
        # Filter elements by source types
        elements1 = [e for e in result1.parsed_content_results if e.source in self.source_types]
        elements2 = [e for e in result2.parsed_content_results if e.source in self.source_types]
        
        # Track already matched elements in result2
        matched_element2_ids = set()
        
        # For each element in result1, find best match in result2
        for element1 in elements1:
            best_match_id = None
            best_match_score = 0.0
            best_iou = 0.0
            
            # Get adaptive threshold based on element type
            adaptive_threshold = self.get_adaptive_iou_threshold(element1.type, element1.source)
            
            for element2 in elements2:
                # Skip if already matched
                if element2.id in matched_element2_ids:
                    continue
                
                # Skip if sources don't match
                if element1.source != element2.source:
                    continue
                
                # Compute IoU between bounding boxes
                iou = self.compute_iou(element1.bbox, element2.bbox)
                
                # If IoU is above adaptive threshold, consider it a potential match
                if iou >= adaptive_threshold:
                    # For box_yolo_content_yolo sources, don't rely on content strings
                    # as omniparser captioning might not be reliable for these elements
                    if element1.source == 'box_yolo_content_yolo':
                        # Always do visual comparison for YOLO elements
                        try:
                            # Extract element images
                            img1 = self.extract_element_image(result1, element1)
                            img2 = self.extract_element_image(result2, element2)
                            
                            # Compute similarity
                            sim_result = self.embedder.get_similarity_with_classification(img1, img2)
                            score = float(sim_result['score'])  # Ensure score is float
                            
                            # Update best match if better
                            if score > best_match_score and score > 0.5:  # Minimum similarity threshold
                                best_match_id = element2.id
                                best_match_score = score
                                best_iou = iou
                        except Exception as e:
                            logger.warning(f"Error comparing YOLO elements: {e}")
                    else:
                        # For other element types, content comparison is reliable
                        if element1.content == element2.content:
                            # Perfect text match
                            if iou > best_iou:
                                best_match_id = element2.id
                                best_match_score = 1.0
                                best_iou = iou
                        else:
                            # Check visual similarity for complex matches
                            try:
                                # Extract element images
                                img1 = self.extract_element_image(result1, element1)
                                img2 = self.extract_element_image(result2, element2)
                                
                                # Compute similarity
                                sim_result = self.embedder.get_similarity_with_classification(img1, img2)
                                score = float(sim_result['score'])  # Ensure score is float
                                
                                # Update best match if better
                                if score > best_match_score and score > 0.5:  # Minimum similarity threshold
                                    best_match_id = element2.id
                                    best_match_score = score
                                    best_iou = iou
                            except Exception as e:
                                logger.warning(f"Error comparing elements: {e}")
            
            # If a match was found, add it
            if best_match_id is not None:
                matches[element1.id] = best_match_id
                matched_element2_ids.add(best_match_id)
        
        return matches
    
    def create_visual_diff_mask(self, img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Create a visual difference mask using OpenCV.
        
        Args:
            img1: First image as numpy array
            img2: Second image as numpy array
            
        Returns:
            numpy.ndarray: Binary mask of differences
        """
        # Check if images have same dimensions
        if img1.shape != img2.shape:
            # Resize to the same dimensions if different
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        
        # Apply slight Gaussian blur to reduce noise
        gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
        gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Apply threshold
        _, thresh = cv2.threshold(diff, self.pixel_diff_threshold, 255, cv2.THRESH_BINARY)
        
        # Dilate to connect nearby differences
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        return dilated
    
    def is_visually_different(self, 
                             diff_mask: np.ndarray, 
                             bbox: List[float]) -> Tuple[bool, float]:
        """
        Check if a region of the diff mask indicates visual difference.
        
        Args:
            diff_mask: Binary mask of differences
            bbox: Bounding box [x1, y1, x2, y2]
            
        Returns:
            Tuple[bool, float]: (is_different, difference_ratio)
        """
        # Convert bbox to integers
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        
        # Ensure coordinates are within mask bounds
        height, width = diff_mask.shape
        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))
        
        # Extract the region
        region = diff_mask[y1:y2, x1:x2]
        
        # Calculate ratio of different pixels
        if region.size == 0:
            return False, 0.0
        
        diff_ratio = np.count_nonzero(region) / region.size
        
        # Consider different if ratio exceeds threshold
        is_different = diff_ratio > self.visual_change_threshold
        
        return is_different, diff_ratio
    
    def get_text_similarity(self, text1: str, text2: str) -> float:
        """
        Compute text similarity using Levenshtein distance.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity score (0-1, higher is more similar)
        """
        if not text1 and not text2:
            return 1.0  # Both empty
        if not text1 or not text2:
            return 0.0  # One empty
        
        # Normalize texts
        text1 = text1.strip().lower()
        text2 = text2.strip().lower()
        
        if text1 == text2:
            return 1.0  # Exact match
        
        # Compute Levenshtein distance
        distance = Levenshtein.distance(text1, text2)
        max_len = max(len(text1), len(text2))
        
        # Convert to similarity (1 - normalized_distance)
        similarity = 1 - (distance / max_len)
        
        return similarity
    
    def compare_results(self, 
                       result1: OmniParserResultModel, 
                       result2: OmniParserResultModel) -> ImageDiffResults:
        """
        Compare two OmniParserResultModel objects and return the differences.
        
        Args:
            result1: First OmniParserResultModel (original)
            result2: Second OmniParserResultModel (new)
            
        Returns:
            ImageDiffResults: Structured results of the comparison
        """
        # Initialize result containers
        added_elements = []
        removed_elements = []
        text_changed_elements = []
        visual_changed_elements = []
        
        # Get image dimensions for saliency calculation
        img1_width = result1.omniparser_result.original_image_width
        img1_height = result1.omniparser_result.original_image_height
        img2_width = result2.omniparser_result.original_image_width
        img2_height = result2.omniparser_result.original_image_height
        
        # Match elements from result1 to result2
        matches = self.match_elements(result1, result2)
        
        # Get all element IDs
        result1_element_ids = {e.id for e in result1.parsed_content_results if e.source in self.source_types}
        result2_element_ids = {e.id for e in result2.parsed_content_results if e.source in self.source_types}
        matched_result1_ids = set(matches.keys())
        matched_result2_ids = set(matches.values())
        
        # Extract all elements from both results for quick lookup
        elements1 = {e.id: e for e in result1.parsed_content_results}
        elements2 = {e.id: e for e in result2.parsed_content_results}
        
        # Create visual diff mask for detecting pixel-level changes
        try:
            # Load images
            img1_path = result1.omniparser_result.original_image_path
            img2_path = result2.omniparser_result.original_image_path
            img1 = np.array(Image.open(img1_path).convert("RGB"))
            img2 = np.array(Image.open(img2_path).convert("RGB"))
            
            # Create diff mask
            diff_mask = self.create_visual_diff_mask(img1, img2)
        except Exception as e:
            logger.error(f"Error creating diff mask: {e}")
            diff_mask = None
        
        # Find removed elements (in result1 but not in result2)
        removed_ids = result1_element_ids - matched_result1_ids
        for element_id in removed_ids:
            element = elements1[element_id]
            # Skip if not in source types filter
            if element.source not in self.source_types:
                continue
                
            # Compute saliency
            saliency = self.compute_saliency(element.bbox, img1_width, img1_height)
            
            # Skip if below saliency threshold
            if saliency < self.saliency_threshold:
                continue
            
            # Add to removed elements
            removed_elements.append(DiffResult(
                type="removed",
                bbox=element.bbox,
                element_type=element.type,
                source=element.source,
                saliency=saliency,
                element_id=element.id,
                old_content=element.content
            ))
        
        # Find added elements (in result2 but not in result1)
        added_ids = result2_element_ids - matched_result2_ids
        for element_id in added_ids:
            element = elements2[element_id]
            # Skip if not in source types filter
            if element.source not in self.source_types:
                continue
                
            # Compute saliency
            saliency = self.compute_saliency(element.bbox, img2_width, img2_height)
            
            # Skip if below saliency threshold
            if saliency < self.saliency_threshold:
                continue
            
            # Add to added elements
            added_elements.append(DiffResult(
                type="added",
                bbox=element.bbox,
                element_type=element.type,
                source=element.source,
                saliency=saliency,
                element_id=element.id,
                new_content=element.content
            ))
        
        # Find changed elements (content or visual changes)
        for element1_id, element2_id in matches.items():
            element1 = elements1[element1_id]
            element2 = elements2[element2_id]
            
            # Skip if not in source types filter
            if element1.source not in self.source_types:
                continue
            
            # Compute saliency (use average of both)
            saliency1 = self.compute_saliency(element1.bbox, img1_width, img1_height)
            saliency2 = self.compute_saliency(element2.bbox, img2_width, img2_height)
            saliency = (saliency1 + saliency2) / 2
            
            # Skip if below saliency threshold
            if saliency < self.saliency_threshold:
                continue
            
            # For YOLO elements, only check for visual changes, not text changes
            if element1.source == 'box_yolo_content_yolo':
                # For YOLO elements, always do visual comparison regardless of pixel diff
                try:
                    img1_elem = self.extract_element_image(result1, element1)
                    img2_elem = self.extract_element_image(result2, element2)
                    
                    # Compute visual similarity
                    sim_result = self.embedder.get_similarity_with_classification(img1_elem, img2_elem)
                    score = sim_result['score']
                    classification = sim_result['classification']
                    
                    # For YOLO elements, add as visual change if not identical
                    if classification != "identical":
                        # Compute diff ratio if we have diff mask
                        diff_ratio = 0.0
                        if diff_mask is not None:
                            _, diff_ratio = self.is_visually_different(diff_mask, element2.bbox)
                        
                        visual_changed_elements.append(DiffResult(
                            type="visual-changed",
                            bbox=element2.bbox,  # Use bbox from the new image
                            element_type=element2.type,
                            source=element2.source,
                            saliency=saliency,
                            element_id=element2.id,
                            similarity_score=score,
                            visual_diff_ratio=diff_ratio,
                            classification=classification
                        ))
                except Exception as e:
                    logger.warning(f"Error comparing YOLO elements for visual changes: {e}")
            # For non-YOLO elements, check for text changes first
            elif element1.content != element2.content:
                text_similarity = self.get_text_similarity(element1.content, element2.content)
                
                # Consider it a text change if similarity is below threshold
                if text_similarity < self.text_similarity_threshold:
                    text_changed_elements.append(DiffResult(
                        type="text-changed",
                        bbox=element2.bbox,  # Use bbox from the new image
                        element_type=element2.type,
                        source=element2.source,
                        saliency=saliency,
                        element_id=element2.id,
                        old_content=element1.content,
                        new_content=element2.content,
                        similarity_score=text_similarity
                    ))
                    continue  # Skip visual check for text changes
            
            # Check for visual changes if we have a diff mask (for non-YOLO elements or YOLO that weren't caught above)
            if diff_mask is not None and element1.source != 'box_yolo_content_yolo':
                is_diff, diff_ratio = self.is_visually_different(diff_mask, element2.bbox)
                
                if is_diff:
                    # Extract images for similarity check
                    try:
                        img1 = self.extract_element_image(result1, element1)
                        img2 = self.extract_element_image(result2, element2)
                        
                        # Compute visual similarity
                        sim_result = self.embedder.get_similarity_with_classification(img1, img2)
                        score = sim_result['score']
                        classification = sim_result['classification']
                        
                        # Only add if not "identical" or diff_ratio is significant
                        if classification != "identical" or diff_ratio > self.visual_change_threshold:
                            visual_changed_elements.append(DiffResult(
                                type="visual-changed",
                                bbox=element2.bbox,  # Use bbox from the new image
                                element_type=element2.type,
                                source=element2.source,
                                saliency=saliency,
                                element_id=element2.id,
                                similarity_score=score,
                                visual_diff_ratio=diff_ratio,
                                classification=classification
                            ))
                    except Exception as e:
                        logger.warning(f"Error comparing visual elements: {e}")
        
        # Create and return the final results
        return ImageDiffResults(
            added=added_elements,
            removed=removed_elements,
            text_changed=text_changed_elements,
            visual_changed=visual_changed_elements
        )
    
    def compare_images(self, 
                      image_path1: str, 
                      image_path2: str, 
                      result1: OmniParserResultModel, 
                      result2: OmniParserResultModel) -> ImageDiffResults:
        """
        Compare two images and their OmniParserResultModel objects.
        This is a convenience method if the image paths in the OmniParserResultModel
        don't point to the correct locations.
        
        Args:
            image_path1: Path to first image
            image_path2: Path to second image
            result1: First OmniParserResultModel
            result2: Second OmniParserResultModel
            
        Returns:
            ImageDiffResults: Structured results of the comparison
        """
        # Create copies of the models
        result1 = OmniParserResultModel(
            event_id=result1.event_id,
            project_uuid=result1.project_uuid,
            command_uuid=result1.command_uuid,
            timestamp=result1.timestamp,
            description=result1.description,
            omniparser_result=result1.omniparser_result,
            parsed_content_results=result1.parsed_content_results
        )
        
        result2 = OmniParserResultModel(
            event_id=result2.event_id,
            project_uuid=result2.project_uuid,
            command_uuid=result2.command_uuid,
            timestamp=result2.timestamp,
            description=result2.description,
            omniparser_result=result2.omniparser_result,
            parsed_content_results=result2.parsed_content_results
        )
        
        # Update image paths
        result1.omniparser_result.original_image_path = image_path1
        result2.omniparser_result.original_image_path = image_path2
        
        # Call the main comparison method
        return self.compare_results(result1, result2)
