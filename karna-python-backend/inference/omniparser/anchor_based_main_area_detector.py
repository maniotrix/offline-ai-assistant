import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple, Optional, Any, Union
import os

# Import from existing components
from .ui_dynamic_area_detector import UIOptimizedDynamicAreaDetector
from .image_comparison import ResNetImageEmbedder
from .patch_matcher import PatchMatcher
from .image_diff_creator import ImageDiffCreator
from .omni_helper import OmniParserResultModelList, OmniParserResultModel, ParsedContentResult

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class AnchorPoint:
    """Represents a stable anchor point with its spatial relationship to the main area."""
    
    def __init__(
        self,
        element_id: int,
        element_type: str,
        bbox: List[float],
        source: str,
        patch: Image.Image,
        embedding: np.ndarray,
        constraint_direction: str,  # 'top', 'bottom', 'left', 'right'
        constraint_ratio: float,    # Position relative to main area
        stability_score: float      # Higher means more stable across frames
    ):
        self.element_id = element_id
        self.element_type = element_type
        self.bbox = bbox
        self.source = source
        self.patch = patch
        self.embedding = embedding
        self.constraint_direction = constraint_direction
        self.constraint_ratio = constraint_ratio
        self.stability_score = stability_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "element_id": self.element_id,
            "element_type": self.element_type,
            "bbox": self.bbox,
            "source": self.source,
            "constraint_direction": self.constraint_direction,
            "constraint_ratio": self.constraint_ratio,
            "stability_score": self.stability_score
        }


class MainAreaReference:
    """Stores a visual representation of the main content area."""
    
    def __init__(
        self,
        bbox: List[float],
        patch: Image.Image,
        embedding: np.ndarray,
        frame_index: int
    ):
        self.bbox = bbox
        self.patch = patch
        self.embedding = embedding
        self.frame_index = frame_index
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "bbox": self.bbox,
            "frame_index": self.frame_index
        }


class AnchorBasedMainAreaDetector:
    """
    Detector that uses stable anchors and main area patches to identify
    the main content area in UI screenshots.
    """
    
    def __init__(
        self,
        model_name: str = 'resnet50',
        dynamic_detector: Optional[UIOptimizedDynamicAreaDetector] = None,
        min_stability_score: float = 0.7,
        main_area_match_threshold: float = 0.7,
        anchor_match_threshold: float = 0.8,
        max_anchor_points: int = 10,
        max_main_area_references: int = 4
    ):
        """
        Initialize the detector.
        
        Args:
            model_name: ResNet model to use for embeddings
            dynamic_detector: Optional detector for finding dynamic areas
            min_stability_score: Minimum stability score for anchor points
            main_area_match_threshold: Threshold for main area patch matching
            anchor_match_threshold: Threshold for anchor point matching
            max_anchor_points: Maximum number of anchor points to store
            max_main_area_references: Maximum number of main area references to store
        """
        self.dynamic_detector = dynamic_detector or UIOptimizedDynamicAreaDetector()
        self.embedder = ResNetImageEmbedder(model_name=model_name)
        self.patch_matcher = PatchMatcher(model_name=model_name)
        self.diff_creator = ImageDiffCreator(model_name=model_name)
        
        self.min_stability_score = min_stability_score
        self.main_area_match_threshold = main_area_match_threshold
        self.anchor_match_threshold = anchor_match_threshold
        self.max_anchor_points = max_anchor_points
        self.max_main_area_references = max_main_area_references
        
        logger.info(f"AnchorBasedMainAreaDetector initialized with model {model_name}")
    
    def _extract_patch(self, image: Image.Image, bbox: List[float]) -> Image.Image:
        """Extract a patch from an image using a bounding box."""
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        return image.crop((x1, y1, x2, y2))
    
    def _find_stable_elements(self, results_list: OmniParserResultModelList) -> Dict[int, Dict[str, Any]]:
        """
        Identify elements that remain stable across frames.
        
        Args:
            results_list: List of OmniParser results for multiple frames
            
        Returns:
            Dictionary mapping element IDs to stability information
        """
        logger.info("Finding stable elements across frames")
        
        # Track element presence and position across frames
        element_tracker: Dict[str, Dict[str, Any]] = {}
        frame_count = len(results_list.omniparser_result_models)
        
        # For each frame
        for frame_idx, result_model in enumerate(results_list.omniparser_result_models):
            # Load the image
            image_path = result_model.omniparser_result.original_image_path
            image = Image.open(image_path).convert("RGB")
            image_width = result_model.omniparser_result.original_image_width
            image_height = result_model.omniparser_result.original_image_height
            
            # For each element in the frame
            for element in result_model.parsed_content_results:
                # Skip YOLO elements with unreliable content
                if element.source == 'box_yolo_content_yolo':
                    element_key = f"{element.type}_{element.bbox[0]}_{element.bbox[1]}"
                else:
                    # Use content for non-YOLO elements
                    element_key = f"{element.type}_{element.content}"
                
                # If we've seen this element before
                if element_key in element_tracker:
                    # Update its presence count and position history
                    tracker_entry = element_tracker[element_key]
                    tracker_entry["count"] += 1
                    tracker_entry["positions"].append(element.bbox)
                    
                    # Extract and store patch if it's the first time or better quality
                    if "patch" not in tracker_entry or frame_idx == frame_count - 1:
                        patch = self._extract_patch(image, element.bbox)
                        if "patch" not in tracker_entry:
                            tracker_entry["patch"] = patch
                            tracker_entry["element"] = element
                            # Generate embedding
                            try:
                                tracker_entry["embedding"] = self.embedder.get_embedding(patch)
                            except Exception as e:
                                logger.warning(f"Failed to generate embedding: {e}")
                                tracker_entry["embedding"] = None
                        else:
                            # Replace with last frame's version for better quality
                            tracker_entry["patch"] = patch
                            tracker_entry["element"] = element
                            # Update embedding
                            try:
                                tracker_entry["embedding"] = self.embedder.get_embedding(patch)
                            except Exception as e:
                                logger.warning(f"Failed to generate embedding: {e}")
                
                # If this is a new element
                else:
                    patch = self._extract_patch(image, element.bbox)
                    try:
                        embedding = self.embedder.get_embedding(patch)
                    except Exception as e:
                        logger.warning(f"Failed to generate embedding: {e}")
                        embedding = None
                    
                    element_tracker[element_key] = {
                        "count": 1,
                        "positions": [element.bbox],
                        "patch": patch,
                        "embedding": embedding,
                        "element": element,
                        "type": element.type,
                        "source": element.source
                    }
        
        # Calculate stability scores and filter elements
        stable_elements = {}
        for element_key, data in element_tracker.items():
            # Only consider elements that appear in most frames
            stability_threshold = frame_count * 0.75
            if data["count"] >= stability_threshold:
                # Calculate position stability
                positions = np.array(data["positions"])
                position_variance = np.mean(np.var(positions, axis=0))
                position_stability = 1.0 / (1.0 + position_variance)
                
                # Combined stability score (more frames = higher score)
                stability_score = (data["count"] / frame_count) * position_stability
                
                if stability_score >= self.min_stability_score:
                    element = data["element"]
                    stable_elements[element.id] = {
                        "element": element,
                        "stability_score": stability_score,
                        "average_position": np.mean(positions, axis=0).tolist(),
                        "patch": data["patch"],
                        "embedding": data["embedding"]
                    }
        
        logger.info(f"Found {len(stable_elements)} stable elements")
        return stable_elements
    
    def _calculate_element_position_relative_to_main_area(
        self,
        element_position: List[float],
        main_area: List[float]
    ) -> Dict[str, Any]:
        """
        Calculate an element's position relative to the main area.
        
        Args:
            element_position: Element bounding box [x1, y1, x2, y2]
            main_area: Main area bounding box [x1, y1, x2, y2]
            
        Returns:
            Dictionary with constraint direction and ratio information
        """
        # Calculate element center
        elem_center_x = (element_position[0] + element_position[2]) / 2
        elem_center_y = (element_position[1] + element_position[3]) / 2
        
        # Main area dimensions
        main_left, main_top, main_right, main_bottom = main_area
        main_width = main_right - main_left
        main_height = main_bottom - main_top
        
        # Calculate distances to each edge of main area
        dist_to_left = abs(elem_center_x - main_left)
        dist_to_right = abs(elem_center_x - main_right)
        dist_to_top = abs(elem_center_y - main_top)
        dist_to_bottom = abs(elem_center_y - main_bottom)
        
        # Determine closest edge
        min_dist = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)
        
        # Determine constraint direction
        if min_dist == dist_to_left:
            direction = "left"
            ratio = (elem_center_x - main_left) / main_width
        elif min_dist == dist_to_right:
            direction = "right"
            ratio = (main_right - elem_center_x) / main_width
        elif min_dist == dist_to_top:
            direction = "top"
            ratio = (elem_center_y - main_top) / main_height
        else:  # Bottom
            direction = "bottom"
            ratio = (main_bottom - elem_center_y) / main_height
        
        # Determine if element is at a border
        border_threshold = 0.1  # Within 10% of edge
        is_at_border = min_dist / max(main_width, main_height) < border_threshold
        
        return {
            "direction": direction,
            "ratio": ratio,
            "is_at_border": is_at_border,
            "distance": min_dist
        }
    
    def _identify_anchor_points(
        self,
        stable_elements: Dict[int, Dict[str, Any]],
        main_area: List[float]
    ) -> List[AnchorPoint]:
        """
        Identify anchor points from stable elements.
        
        Args:
            stable_elements: Dictionary of stable elements
            main_area: Main area bounding box
            
        Returns:
            List of AnchorPoint objects
        """
        logger.info("Identifying anchor points")
        
        anchor_points = []
        
        for element_id, data in stable_elements.items():
            element = data["element"]
            avg_position = data["average_position"]
            
            # Calculate position relative to main area
            position_data = self._calculate_element_position_relative_to_main_area(
                avg_position, main_area
            )
            
            # Only consider elements near borders
            if position_data["is_at_border"]:
                # Create anchor point
                anchor_point = AnchorPoint(
                    element_id=element.id,
                    element_type=element.type,
                    bbox=avg_position,
                    source=element.source,
                    patch=data["patch"],
                    embedding=data["embedding"],
                    constraint_direction=position_data["direction"],
                    constraint_ratio=position_data["ratio"],
                    stability_score=data["stability_score"]
                )
                
                anchor_points.append(anchor_point)
        
        # Sort by stability score and take up to max_anchor_points
        anchor_points.sort(key=lambda x: x.stability_score, reverse=True)
        anchor_points = anchor_points[:self.max_anchor_points]
        
        # Ensure diversity of constraint directions
        directions = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        for anchor in anchor_points:
            directions[anchor.constraint_direction] += 1
        
        logger.info(f"Selected {len(anchor_points)} anchor points with direction distribution: {directions}")
        return anchor_points
    
    def _extract_main_area_references(
        self,
        results_list: OmniParserResultModelList,
        main_area: List[float]
    ) -> List[MainAreaReference]:
        """
        Extract visual references of the main area from multiple frames.
        
        Args:
            results_list: List of OmniParser results
            main_area: Main area bounding box
            
        Returns:
            List of MainAreaReference objects
        """
        logger.info("Extracting main area references")
        
        main_area_references = []
        frame_count = len(results_list.omniparser_result_models)
        
        # Select a subset of frames to use as references
        # Use evenly spaced indices, including first and last frame
        if frame_count <= self.max_main_area_references:
            frame_indices = list(range(frame_count))
        else:
            step = frame_count / self.max_main_area_references
            frame_indices = [min(int(i * step), frame_count - 1) for i in range(self.max_main_area_references)]
        
        # Ensure first and last frames are included
        if 0 not in frame_indices:
            frame_indices[0] = 0
        if frame_count - 1 not in frame_indices:
            frame_indices[-1] = frame_count - 1
        
        # Extract references from selected frames
        for idx in frame_indices:
            result_model = results_list.omniparser_result_models[idx]
            image_path = result_model.omniparser_result.original_image_path
            image = Image.open(image_path).convert("RGB")
            
            # Extract main area patch
            patch = self._extract_patch(image, main_area)
            
            # Generate embedding
            try:
                embedding = self.embedder.get_embedding(patch)
                
                # Create reference
                reference = MainAreaReference(
                    bbox=main_area,
                    patch=patch,
                    embedding=embedding,
                    frame_index=idx
                )
                
                main_area_references.append(reference)
            except Exception as e:
                logger.warning(f"Failed to generate embedding for frame {idx}: {e}")
        
        logger.info(f"Created {len(main_area_references)} main area references")
        return main_area_references
    
    def train(
        self,
        results_list: OmniParserResultModelList,
        save_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Train the detector on a sequence of frames.
        
        Args:
            results_list: List of OmniParser results
            save_dir: Optional directory to save visual references
            
        Returns:
            Detection model with main area references and anchor points
        """
        logger.info("Training anchor-based main area detector")
        
        # Get screen dimensions from first frame
        first_result = results_list.omniparser_result_models[0]
        screen_width = first_result.omniparser_result.original_image_width
        screen_height = first_result.omniparser_result.original_image_height
        
        # Step 1: Detect dynamic areas using existing detector
        dynamic_areas = self.dynamic_detector.detect_main_areas(results_list)
        
        # Use main_content_area if available, otherwise use largest_area
        main_area = dynamic_areas.get("main_content_area") or dynamic_areas.get("largest_area")
        
        if not main_area:
            logger.warning("No main content area detected")
            return {"success": False, "error": "No main content area detected"}
        
        # Step 2: Find stable elements
        stable_elements = self._find_stable_elements(results_list)
        
        # Step 3: Identify anchor points
        anchor_points = self._identify_anchor_points(stable_elements, main_area)
        
        # Step 4: Extract main area references
        main_area_references = self._extract_main_area_references(results_list, main_area)
        
        # Step 5: Save visual references if requested
        if save_dir:
            self._save_visual_references(anchor_points, main_area_references, save_dir)
        
        # Create detection model
        detection_model = {
            "success": True,
            "main_area": main_area,
            "screen_dimensions": [screen_width, screen_height],
            "anchor_points": [anchor.to_dict() for anchor in anchor_points],
            "main_area_references": [ref.to_dict() for ref in main_area_references],
            # Save patches and embeddings separately as they can't be serialized
            "visual_data": {
                "anchors": anchor_points,
                "main_areas": main_area_references
            }
        }
        
        logger.info("Detector training completed successfully")
        return detection_model
    
    def _save_visual_references(
        self,
        anchor_points: List[AnchorPoint],
        main_area_references: List[MainAreaReference],
        save_dir: str
    ) -> None:
        """
        Save visual references to disk.
        
        Args:
            anchor_points: List of anchor points
            main_area_references: List of main area references
            save_dir: Directory to save visual references
        """
        logger.info(f"Saving visual references to {save_dir}")
        
        # Create directories if they don't exist
        anchors_dir = os.path.join(save_dir, "anchors")
        main_areas_dir = os.path.join(save_dir, "main_areas")
        
        os.makedirs(anchors_dir, exist_ok=True)
        os.makedirs(main_areas_dir, exist_ok=True)
        
        # Save anchor points
        for i, anchor in enumerate(anchor_points):
            anchor_path = os.path.join(anchors_dir, f"anchor_{i}_{anchor.constraint_direction}.png")
            anchor.patch.save(anchor_path)
        
        # Save main area references
        for i, reference in enumerate(main_area_references):
            main_area_path = os.path.join(main_areas_dir, f"main_area_{i}_frame_{reference.frame_index}.png")
            reference.patch.save(main_area_path)
        
        logger.info(f"Saved {len(anchor_points)} anchor points and {len(main_area_references)} main area references")
    
    def detect(
        self,
        result_model: OmniParserResultModel,
        detection_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect the main content area in a new frame using the trained model.
        
        Args:
            result_model: OmniParser result for the new frame
            detection_model: Model created by train()
            
        Returns:
            Dictionary with detection results
        """
        logger.info("Detecting main content area using anchor-based approach")
        
        # Load image
        image_path = result_model.omniparser_result.original_image_path
        image = Image.open(image_path).convert("RGB")
        
        # Get image dimensions
        image_width = result_model.omniparser_result.original_image_width
        image_height = result_model.omniparser_result.original_image_height
        
        # Extract visual data
        anchors = detection_model["visual_data"]["anchors"]
        main_areas = detection_model["visual_data"]["main_areas"]
        
        # Step 1: Try direct main area matching
        main_area_result = self._match_main_area_directly(image, main_areas)
        
        if main_area_result["match_found"] and main_area_result["confidence"] >= 0.8:
            logger.info("Main area matched directly with high confidence")
            return {
                "success": True,
                "main_area": main_area_result["bbox"],
                "method": "direct_match",
                "confidence": main_area_result["confidence"]
            }
        
        # Step 2: Try anchor-based reconstruction
        anchor_result = self._match_and_reconstruct_from_anchors(
            image, result_model, anchors, detection_model["main_area"],
            detection_model["screen_dimensions"]
        )
        
        if anchor_result["match_found"]:
            logger.info("Main area reconstructed from anchors")
            
            # If we have both results, use the one with higher confidence
            if main_area_result["match_found"]:
                if main_area_result["confidence"] > anchor_result["confidence"]:
                    return {
                        "success": True,
                        "main_area": main_area_result["bbox"],
                        "method": "direct_match",
                        "confidence": main_area_result["confidence"]
                    }
            
            return {
                "success": True,
                "main_area": anchor_result["bbox"],
                "method": "anchor_reconstruction",
                "confidence": anchor_result["confidence"],
                "anchors_matched": anchor_result["anchors_matched"]
            }
        
        # If direct match found but with low confidence, use it as fallback
        if main_area_result["match_found"]:
            logger.info("Using direct match as fallback (low confidence)")
            return {
                "success": True,
                "main_area": main_area_result["bbox"],
                "method": "direct_match_fallback",
                "confidence": main_area_result["confidence"]
            }
        
        # If all else fails, use the original main area with scaling
        logger.info("No matches found, using scaled original main area as fallback")
        
        # Scale original main area to new image dimensions
        orig_main_area = detection_model["main_area"]
        orig_width, orig_height = detection_model["screen_dimensions"]
        
        scale_x = image_width / orig_width
        scale_y = image_height / orig_height
        
        scaled_main_area = [
            orig_main_area[0] * scale_x,
            orig_main_area[1] * scale_y,
            orig_main_area[2] * scale_x,
            orig_main_area[3] * scale_y
        ]
        
        return {
            "success": True,
            "main_area": scaled_main_area,
            "method": "scaled_fallback",
            "confidence": 0.3
        }
    
    def _match_main_area_directly(
        self,
        image: Image.Image,
        main_areas: List[MainAreaReference]
    ) -> Dict[str, Any]:
        """
        Attempt to match the main area directly using stored references.
        
        Args:
            image: Current image
            main_areas: List of main area references
            
        Returns:
            Dictionary with match results
        """
        logger.info("Attempting direct main area matching")
        
        best_match = {
            "match_found": False,
            "confidence": 0.0,
            "bbox": None,
            "reference": None
        }
        
        for reference in main_areas:
            try:
                # Generate embedding for the whole image
                image_embedding = self.embedder.get_embedding(image)
                
                # Compare with reference embedding
                similarity = np.dot(image_embedding, reference.embedding)
                
                if similarity > best_match["confidence"]:
                    best_match["match_found"] = True
                    best_match["confidence"] = similarity
                    best_match["bbox"] = reference.bbox
                    best_match["reference"] = reference
            except Exception as e:
                logger.warning(f"Error during direct main area matching: {e}")
        
        return best_match
    
    def _match_and_reconstruct_from_anchors(
        self,
        image: Image.Image,
        result_model: OmniParserResultModel,
        anchors: List[AnchorPoint],
        original_main_area: List[float],
        original_dimensions: List[float]
    ) -> Dict[str, Any]:
        """
        Match anchor points and reconstruct the main area.
        
        Args:
            image: Current image
            result_model: OmniParser result
            anchors: List of anchor points
            original_main_area: Original main area bbox
            original_dimensions: Original screen dimensions [width, height]
            
        Returns:
            Dictionary with reconstruction results
        """
        logger.info("Attempting to match and reconstruct from anchors")
        
        matched_anchors = []
        
        # Step 1: Find matches for each anchor
        for anchor in anchors:
            best_match = None
            best_score = 0.0
            
            for element in result_model.parsed_content_results:
                # Skip if source types don't match
                if element.source != anchor.source:
                    continue
                
                # Extract element patch
                try:
                    element_patch = self._extract_patch(image, element.bbox)
                    element_embedding = self.embedder.get_embedding(element_patch)
                    
                    # Compare embeddings
                    similarity = np.dot(element_embedding, anchor.embedding)
                    
                    if similarity > best_score and similarity >= self.anchor_match_threshold:
                        best_match = element
                        best_score = similarity
                except Exception as e:
                    logger.warning(f"Error matching anchor: {e}")
            
            if best_match:
                matched_anchors.append({
                    "anchor": anchor,
                    "match": best_match,
                    "score": best_score
                })
        
        logger.info(f"Matched {len(matched_anchors)} anchors")
        
        # Step 2: Reconstruct main area from matched anchors
        if len(matched_anchors) >= 2:
            # Group anchors by constraint direction
            direction_groups = {"top": [], "bottom": [], "left": [], "right": []}
            
            for match_data in matched_anchors:
                anchor = match_data["anchor"]
                element = match_data["match"]
                direction_groups[anchor.constraint_direction].append({
                    "anchor": anchor,
                    "element": element,
                    "score": match_data["score"]
                })
            
            # Calculate constraints for each direction
            constraints = {}
            for direction, group in direction_groups.items():
                if group:
                    # Sort by score and use the best match
                    group.sort(key=lambda x: x["score"], reverse=True)
                    best = group[0]
                    
                    anchor_pos = best["anchor"].bbox
                    element_pos = best["element"].bbox
                    
                    # Convert bbox to center points
                    anchor_center = [(anchor_pos[0] + anchor_pos[2]) / 2,
                                    (anchor_pos[1] + anchor_pos[3]) / 2]
                    element_center = [(element_pos[0] + element_pos[2]) / 2,
                                     (element_pos[1] + element_pos[3]) / 2]
                    
                    # Calculate constraint position based on direction and ratio
                    if direction == "top":
                        constraints["top"] = element_center[1] + (
                            (original_main_area[1] - anchor_center[1]) *
                            (element_pos[3] - element_pos[1]) / (anchor_pos[3] - anchor_pos[1])
                        )
                    elif direction == "bottom":
                        constraints["bottom"] = element_center[1] + (
                            (original_main_area[3] - anchor_center[1]) *
                            (element_pos[3] - element_pos[1]) / (anchor_pos[3] - anchor_pos[1])
                        )
                    elif direction == "left":
                        constraints["left"] = element_center[0] + (
                            (original_main_area[0] - anchor_center[0]) *
                            (element_pos[2] - element_pos[0]) / (anchor_pos[2] - anchor_pos[0])
                        )
                    elif direction == "right":
                        constraints["right"] = element_center[0] + (
                            (original_main_area[2] - anchor_center[0]) *
                            (element_pos[2] - element_pos[0]) / (anchor_pos[2] - anchor_pos[0])
                        )
            
            # If we have opposite constraints, use them directly
            reconstructed_bbox = None
            
            if "left" in constraints and "right" in constraints:
                x1 = constraints["left"]
                x2 = constraints["right"]
            elif "left" in constraints:
                # Use left constraint with original aspect ratio
                x1 = constraints["left"]
                aspect_ratio = (original_main_area[2] - original_main_area[0]) / (original_main_area[3] - original_main_area[1])
                if "top" in constraints and "bottom" in constraints:
                    height = constraints["bottom"] - constraints["top"]
                    x2 = x1 + height * aspect_ratio
                else:
                    # Scale based on image size
                    orig_width, orig_height = original_dimensions
                    scale = image.width / orig_width
                    x2 = x1 + (original_main_area[2] - original_main_area[0]) * scale
            elif "right" in constraints:
                # Use right constraint with original aspect ratio
                x2 = constraints["right"]
                aspect_ratio = (original_main_area[2] - original_main_area[0]) / (original_main_area[3] - original_main_area[1])
                if "top" in constraints and "bottom" in constraints:
                    height = constraints["bottom"] - constraints["top"]
                    x1 = x2 - height * aspect_ratio
                else:
                    # Scale based on image size
                    orig_width, orig_height = original_dimensions
                    scale = image.width / orig_width
                    x1 = x2 - (original_main_area[2] - original_main_area[0]) * scale
            else:
                # Default to original x values scaled to new image
                orig_width, orig_height = original_dimensions
                scale_x = image.width / orig_width
                x1 = original_main_area[0] * scale_x
                x2 = original_main_area[2] * scale_x
            
            if "top" in constraints and "bottom" in constraints:
                y1 = constraints["top"]
                y2 = constraints["bottom"]
            elif "top" in constraints:
                # Use top constraint with original aspect ratio
                y1 = constraints["top"]
                aspect_ratio = (original_main_area[3] - original_main_area[1]) / (original_main_area[2] - original_main_area[0])
                if "left" in constraints and "right" in constraints:
                    width = constraints["right"] - constraints["left"]
                    y2 = y1 + width * aspect_ratio
                else:
                    # Scale based on image size
                    orig_width, orig_height = original_dimensions
                    scale = image.height / orig_height
                    y2 = y1 + (original_main_area[3] - original_main_area[1]) * scale
            elif "bottom" in constraints:
                # Use bottom constraint with original aspect ratio
                y2 = constraints["bottom"]
                aspect_ratio = (original_main_area[3] - original_main_area[1]) / (original_main_area[2] - original_main_area[0])
                if "left" in constraints and "right" in constraints:
                    width = constraints["right"] - constraints["left"]
                    y1 = y2 - width * aspect_ratio
                else:
                    # Scale based on image size
                    orig_width, orig_height = original_dimensions
                    scale = image.height / orig_height
                    y1 = y2 - (original_main_area[3] - original_main_area[1]) * scale
            else:
                # Default to original y values scaled to new image
                orig_width, orig_height = original_dimensions
                scale_y = image.height / orig_height
                y1 = original_main_area[1] * scale_y
                y2 = original_main_area[3] * scale_y
            
            # Clamp coordinates to image boundaries
            x1 = max(0, min(x1, image.width))
            y1 = max(0, min(y1, image.height))
            x2 = max(0, min(x2, image.width))
            y2 = max(0, min(y2, image.height))
            
            reconstructed_bbox = [x1, y1, x2, y2]
            
            # Calculate confidence based on number of matched anchors and their scores
            anchor_count_factor = min(len(matched_anchors) / 4, 1.0)  # 4+ anchors = full confidence
            avg_score = sum(m["score"] for m in matched_anchors) / len(matched_anchors)
            confidence = 0.7 * anchor_count_factor + 0.3 * avg_score
            
            return {
                "match_found": True,
                "bbox": reconstructed_bbox,
                "confidence": confidence,
                "anchors_matched": len(matched_anchors),
                "constraints": constraints
            }
        
        return {
            "match_found": False,
            "bbox": None,
            "confidence": 0,
            "anchors_matched": len(matched_anchors)
        }
