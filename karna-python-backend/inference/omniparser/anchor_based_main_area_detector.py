import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple, Optional, Any, Union
import os
import json
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path

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

# Pydantic data models for serialization
class AnchorPointData(BaseModel):
    """Data model for anchor points to be serialized/deserialized."""
    element_id: str
    element_type: str
    bbox: List[float]
    source: str
    constraint_direction: str
    horizontal_relation: str
    vertical_relation: str
    stability_score: float
    patch_path: str

class MainAreaReferenceData(BaseModel):
    """Data model for main area reference patches to be serialized/deserialized."""
    bbox: List[float]
    frame_index: int
    patch_path: str

class DetectionModelData(BaseModel):
    """Data model for the complete detection model to be serialized/deserialized."""
    model_version: str = "1.0.0"
    model_created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    main_area: List[float]
    screen_dimensions: List[float]
    anchor_points: List[AnchorPointData] = []
    main_area_references: List[MainAreaReferenceData] = []

class AnchorBasedMainAreaDetector:
    """
    Detector that uses stable anchors and main area patches to identify
    the main content area in UI screenshots.
    
    This class focuses on the training phase - creating and saving models.
    For runtime detection, use AnchorBasedMainAreaDetectorRuntime.
    """
    
    def __init__(
        self,
        model_name: str = 'resnet50',
        dynamic_detector: Optional[UIOptimizedDynamicAreaDetector] = None,
        min_stability_score: float = 0.7,
        anchor_match_threshold: float = 0.8,
        max_anchor_points: int = 10,
        max_main_area_references: int = 4
    ):
        """
        Initialize the detector for training.
        
        Args:
            model_name: ResNet model to use for embeddings
            dynamic_detector: Optional detector for finding dynamic areas
            min_stability_score: Minimum stability score for anchor points
            anchor_match_threshold: Threshold for anchor point matching
            max_anchor_points: Maximum number of anchor points to store
            max_main_area_references: Maximum number of main area references to store
        """
        self.dynamic_detector = dynamic_detector or UIOptimizedDynamicAreaDetector()
        self.embedder = ResNetImageEmbedder(model_name=model_name)
        self.patch_matcher = PatchMatcher(model_name=model_name)
        self.diff_creator = ImageDiffCreator(model_name=model_name)
        
        self.min_stability_score = min_stability_score
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
        Simplified to use only directional constraints without proportional ratios.
        
        Args:
            element_position: Element bounding box [x1, y1, x2, y2]
            main_area: Main area bounding box [x1, y1, x2, y2]
            
        Returns:
            Dictionary with constraint direction information
        """
        # Calculate element center
        elem_center_x = (element_position[0] + element_position[2]) / 2
        elem_center_y = (element_position[1] + element_position[3]) / 2
        
        # Main area dimensions and center
        main_left, main_top, main_right, main_bottom = main_area
        main_center_x = (main_left + main_right) / 2
        main_center_y = (main_top + main_bottom) / 2
        
        # Calculate distances to each edge of main area
        dist_to_left = abs(elem_center_x - main_left)
        dist_to_right = abs(elem_center_x - main_right)
        dist_to_top = abs(elem_center_y - main_top)
        dist_to_bottom = abs(elem_center_y - main_bottom)
        
        # Determine closest edge
        min_dist = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)
        
        # Calculate directional relationship (simpler approach)
        horizontal_relation = "left" if elem_center_x < main_center_x else "right"
        vertical_relation = "top" if elem_center_y < main_center_y else "bottom"
        
        # Determine primary constraint direction based on closest edge
        if min_dist == dist_to_left:
            direction = "left"
        elif min_dist == dist_to_right:
            direction = "right"
        elif min_dist == dist_to_top:
            direction = "top"
        else:  # Bottom
            direction = "bottom"
        
        # Determine if element is at a border
        border_threshold = 0.1  # Within 10% of edge
        main_width = main_right - main_left
        main_height = main_bottom - main_top
        is_at_border = min_dist / max(main_width, main_height) < border_threshold
        
        return {
            "direction": direction,
            "horizontal_relation": horizontal_relation,
            "vertical_relation": vertical_relation,
            "is_at_border": is_at_border,
            "distance": min_dist
        }
    
    def _extract_all_patches(
        self,
        image: Image.Image,
        result_model: OmniParserResultModel
    ) -> Dict[str, Dict[str, Any]]:
        """
        Extract patches for all UI elements in the current frame.
        
        Args:
            image: Image of the current frame
            result_model: OmniParser result for the current frame
            
        Returns:
            Dictionary mapping element IDs to element data with patches
        """
        logger.info("Extracting patches for all UI elements")
        
        element_data = {}
        
        for element in result_model.parsed_content_results:
            try:
                # Extract patch
                patch = self._extract_patch(image, element.bbox)
                
                # Generate embedding
                embedding = self.embedder.get_embedding(patch)
                
                # Store element data
                element_data[element.id] = {
                    "element": element,
                    "patch": patch,
                    "embedding": embedding,
                    "bbox": element.bbox
                }
            except Exception as e:
                logger.warning(f"Failed to extract patch for element {element.id}: {e}")
        
        logger.info(f"Extracted patches for {len(element_data)} elements")
        return element_data
    
    def _identify_anchor_points(
        self,
        image: Image.Image,
        stable_elements: Dict[str, Dict[str, Any]],
        result_model: OmniParserResultModel,
        main_area: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Identify anchor points from stable elements.
        
        Args:
            image: Image of the current frame
            stable_elements: Dictionary of stable elements
            result_model: OmniParser result for the current frame
            main_area: Main area bounding box
            
        Returns:
            List of anchor point dictionaries
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
                anchor_point = {
                    "element_id": element.id,
                    "element_type": element.type,
                    "bbox": avg_position,
                    "source": element.source,
                    "patch": data["patch"],
                    "embedding": data["embedding"],
                    "constraint_direction": position_data["direction"],
                    "horizontal_relation": position_data["horizontal_relation"],
                    "vertical_relation": position_data["vertical_relation"],
                    "stability_score": data["stability_score"]
                }
                
                anchor_points.append(anchor_point)
        
        # Sort by stability score and take up to max_anchor_points
        anchor_points.sort(key=lambda x: x["stability_score"], reverse=True)
        anchor_points = anchor_points[:self.max_anchor_points]
        
        # Ensure diversity of constraint directions
        directions = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        for anchor in anchor_points:
            directions[anchor["constraint_direction"]] += 1
        
        logger.info(f"Selected {len(anchor_points)} anchor points with direction distribution: {directions}")
        return anchor_points
    
    def _extract_main_area_references(
        self,
        results_list: OmniParserResultModelList,
        main_area: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Extract visual references of the main area from multiple frames.
        Only extracts patches, without generating embeddings.
        
        Args:
            results_list: List of OmniParser results
            main_area: Main area bounding box
            
        Returns:
            List of main area reference dictionaries
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
            
            # Create reference (without embedding)
            reference = {
                "bbox": main_area,
                "patch": patch,
                "frame_index": idx
            }
            
            main_area_references.append(reference)
        
        logger.info(f"Created {len(main_area_references)} main area references")
        return main_area_references
    
    def _save_model_files(
        self,
        save_dir: str,
        anchor_points: List[Dict[str, Any]],
        main_area_references: List[Dict[str, Any]]
    ) -> Tuple[List[AnchorPointData], List[MainAreaReferenceData]]:
        """
        Save model files to disk and return serializable data.
        
        Args:
            save_dir: Directory to save model files
            anchor_points: List of anchor point dictionaries
            main_area_references: List of main area reference dictionaries
            
        Returns:
            Tuple of serializable anchor points and main area references
        """
        logger.info(f"Saving model files to {save_dir}")
        
        # Create directories
        os.makedirs(save_dir, exist_ok=True)
        anchors_dir = os.path.join(save_dir, "anchors")
        main_areas_dir = os.path.join(save_dir, "main_areas")
        
        os.makedirs(anchors_dir, exist_ok=True)
        os.makedirs(main_areas_dir, exist_ok=True)
        
        # Save anchor points
        serializable_anchors = []
        for i, anchor in enumerate(anchor_points):
            # Save patch image
            patch_filename = f"anchor_{i}_{anchor['constraint_direction']}.png"
            patch_path = os.path.join(anchors_dir, patch_filename)
            anchor["patch"].save(patch_path)
            
            # Create serializable anchor data
            anchor_data = AnchorPointData(
                element_id=anchor["element_id"],
                element_type=anchor["element_type"],
                bbox=anchor["bbox"],
                source=anchor["source"],
                constraint_direction=anchor["constraint_direction"],
                horizontal_relation=anchor["horizontal_relation"],
                vertical_relation=anchor["vertical_relation"],
                stability_score=anchor["stability_score"],
                patch_path=os.path.join("anchors", patch_filename)
            )
            
            serializable_anchors.append(anchor_data)
        
        # Save main area references
        serializable_references = []
        for i, reference in enumerate(main_area_references):
            # Save patch image
            patch_filename = f"main_area_{i}_frame_{reference['frame_index']}.png"
            patch_path = os.path.join(main_areas_dir, patch_filename)
            reference["patch"].save(patch_path)
            
            # Create serializable reference data
            reference_data = MainAreaReferenceData(
                bbox=reference["bbox"],
                frame_index=reference["frame_index"],
                patch_path=os.path.join("main_areas", patch_filename)
            )
            
            serializable_references.append(reference_data)
        
        logger.info(f"Saved {len(serializable_anchors)} anchor points and {len(serializable_references)} main area references")
        return serializable_anchors, serializable_references
    
    def train_with_frames(
        self,
        frames: List[OmniParserResultModel],
        save_dir: str = None
    ) -> Dict[str, Any]:
        """
        Train the detector using a list of frames and save the model.
        The main area is automatically detected using the dynamic detector.
        
        Args:
            frames: List of OmniParser results for all training frames
            save_dir: Directory to save model data (if None, no saving is done)
            
        Returns:
            Dictionary with training results
        """
        if not frames:
            logger.error("No frames provided for training")
            return {"success": False, "error": "No frames provided for training"}
        
        logger.info("Training anchor-based main area detector using frames")
        
        # Get the first frame as the reference frame
        result_model = frames[0]
        image_path = result_model.omniparser_result.original_image_path
        image = Image.open(image_path).convert("RGB")
        
        # Get image dimensions
        image_width = result_model.omniparser_result.original_image_width
        image_height = result_model.omniparser_result.original_image_height
        
        logger.info(f"Training with image dimensions: {image_width}x{image_height}")
        
        # Use the dynamic detector to find the main area automatically
        logger.info("Using dynamic detector to find main content area")
        
        # Create results list for the dynamic detector
        results_list = OmniParserResultModelList(
            omniparser_result_models=frames,
            project_uuid="",  # Placeholder value
            command_uuid=""   # Placeholder value
        )
        
        # Detect main areas
        detection_result = self.dynamic_detector.detect_main_areas(results_list)
        
        # Get the main content area - prefer main_content_area, then vertical_union, then largest_area
        main_area = None
        area_source = None
        
        if detection_result.get("main_content_area"):
            main_area = detection_result["main_content_area"]
            area_source = "main_content_area"
        elif detection_result.get("vertical_union"):
            main_area = detection_result["vertical_union"]
            area_source = "vertical_union"
        elif detection_result.get("largest_area"):
            main_area = detection_result["largest_area"]
            area_source = "largest_area"
        
        if main_area is None:
            logger.error("Dynamic detector failed to find main area")
            return {"success": False, "error": "Dynamic detector failed to find main area"}
        
        logger.info(f"Detected main area from {area_source}: {main_area}")
        
        # 1. Extract patches from the reference frame
        self._extract_all_patches(image, result_model)
        
        # 2. Find stable elements across all frames
        stable_elements = self._find_stable_elements(frames)
        
        # 3. Identify anchor points
        anchor_points = self._identify_anchor_points(
            image, stable_elements, result_model, main_area
        )
        
        # 4. Extract main area references from all frames
        main_area_references = self._extract_main_area_references(
            results_list, main_area
        )
        
        # 5. Save model files if save_dir is provided
        if save_dir:
            # Create directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)
            
            # Use _save_model_files to save anchor points and main area references
            serializable_anchors, serializable_references = self._save_model_files(
                save_dir, anchor_points, main_area_references
            )
            
            # Initialize the model data
            model_data = DetectionModelData(
                main_area=main_area,
                screen_dimensions=[image_width, image_height],
                anchor_points=serializable_anchors,
                main_area_references=serializable_references
            )
            
            # Save model metadata
            model_path = os.path.join(save_dir, "model.json")
            with open(model_path, "w") as f:
                f.write(model_data.json(indent=2))
            
            logger.info(f"Saved model data to {save_dir}")
        
        return {
            "success": True,
            "anchor_points": anchor_points,
            "main_area": main_area,
            "area_source": area_source
        }

    def train(
        self,
        result_model: OmniParserResultModel,
        frames: List[OmniParserResultModel],
        save_dir: str = None
    ) -> Dict[str, Any]:
        """
        Train the detector using extracted patches from frames and save the model.
        The main area is automatically detected using the dynamic detector.
        
        This method is kept for backward compatibility. For new code, use train_with_frames.
        
        Args:
            result_model: OmniParser result for the current frame (ignored, using first frame from frames)
            frames: List of OmniParser results for all training frames
            save_dir: Directory to save model data (if None, no saving is done)
            
        Returns:
            Dictionary with training results
        """
        # Just delegate to train_with_frames
        logger.info("Using train_with_frames method (result_model parameter is now ignored)")
        return self.train_with_frames(frames, save_dir)
