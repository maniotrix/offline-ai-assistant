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
    constraint_ratio: float
    stability_score: float
    patch_path: str
    embedding_path: str

class MainAreaReferenceData(BaseModel):
    """Data model for main area reference patches to be serialized/deserialized."""
    bbox: List[float]
    frame_index: int
    patch_path: str
    embedding_path: str

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
                    "constraint_ratio": position_data["ratio"],
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
            
            # Generate embedding
            try:
                embedding = self.embedder.get_embedding(patch)
                
                # Create reference
                reference = {
                    "bbox": main_area,
                    "patch": patch,
                    "embedding": embedding,
                    "frame_index": idx
                }
                
                main_area_references.append(reference)
            except Exception as e:
                logger.warning(f"Failed to generate embedding for frame {idx}: {e}")
        
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
        embeddings_dir = os.path.join(save_dir, "embeddings")
        
        os.makedirs(anchors_dir, exist_ok=True)
        os.makedirs(main_areas_dir, exist_ok=True)
        os.makedirs(embeddings_dir, exist_ok=True)
        
        # Save anchor points
        serializable_anchors = []
        for i, anchor in enumerate(anchor_points):
            # Save patch image
            patch_filename = f"anchor_{i}_{anchor['constraint_direction']}.png"
            patch_path = os.path.join(anchors_dir, patch_filename)
            anchor["patch"].save(patch_path)
            
            # Save embedding
            embedding_filename = f"anchor_{i}_{anchor['constraint_direction']}.npy"
            embedding_path = os.path.join(embeddings_dir, embedding_filename)
            if anchor["embedding"] is not None:
                np.save(embedding_path, anchor["embedding"])
            
            # Create serializable anchor data
            anchor_data = AnchorPointData(
                element_id=anchor["element_id"],
                element_type=anchor["element_type"],
                bbox=anchor["bbox"],
                source=anchor["source"],
                constraint_direction=anchor["constraint_direction"],
                constraint_ratio=anchor["constraint_ratio"],
                stability_score=anchor["stability_score"],
                patch_path=os.path.join("anchors", patch_filename),
                embedding_path=os.path.join("embeddings", embedding_filename)
            )
            
            serializable_anchors.append(anchor_data)
        
        # Save main area references
        serializable_references = []
        for i, reference in enumerate(main_area_references):
            # Save patch image
            patch_filename = f"main_area_{i}_frame_{reference['frame_index']}.png"
            patch_path = os.path.join(main_areas_dir, patch_filename)
            reference["patch"].save(patch_path)
            
            # Save embedding
            embedding_filename = f"main_area_{i}_frame_{reference['frame_index']}.npy"
            embedding_path = os.path.join(embeddings_dir, embedding_filename)
            np.save(embedding_path, reference["embedding"])
            
            # Create serializable reference data
            reference_data = MainAreaReferenceData(
                bbox=reference["bbox"],
                frame_index=reference["frame_index"],
                patch_path=os.path.join("main_areas", patch_filename),
                embedding_path=os.path.join("embeddings", embedding_filename)
            )
            
            serializable_references.append(reference_data)
        
        logger.info(f"Saved {len(serializable_anchors)} anchor points and {len(serializable_references)} main area references")
        return serializable_anchors, serializable_references
    
    def train(
        self,
        result_model: OmniParserResultModel,
        frames: List[OmniParserResultModel],
        main_area: List[float],
        save_dir: str = None
    ) -> Dict[str, Any]:
        """
        Train the detector using extracted patches from frames and save the model.
        
        Args:
            result_model: OmniParser result for the current frame
            frames: List of OmniParser results for all training frames
            main_area: Bounding box of the main content area [x1, y1, x2, y2]
            save_dir: Directory to save model data (if None, no saving is done)
            
        Returns:
            Dictionary with training results
        """
        logger.info("Training anchor-based main area detector")
        
        # Get the first frame's image path for reference
        image_path = result_model.omniparser_result.original_image_path
        image = Image.open(image_path).convert("RGB")
        
        # Get image dimensions
        image_width = result_model.omniparser_result.original_image_width
        image_height = result_model.omniparser_result.original_image_height
        
        logger.info(f"Training with image dimensions: {image_width}x{image_height}")
        
        # 1. Extract patches
        self._extract_all_patches(image, result_model)
        
        # 2. Find stable elements
        stable_elements = self._find_stable_elements(frames)
        
        # 3. Identify anchor points
        anchor_points = self._identify_anchor_points(
            image, stable_elements, result_model, main_area
        )
        
        # 4. Save model files if save_dir is provided
        if save_dir:
            # Create directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)
            
            # Initialize the model data
            model_data = DetectionModelData(
                main_area=main_area,
                screen_dimensions=[image_width, image_height],
                anchor_points=[],
                main_area_references=[]
            )
            
            # Save anchor point patches and add to model data
            for i, anchor in enumerate(anchor_points):
                patch = anchor["patch"]
                embedding = anchor["embedding"]
                
                # Save patch image
                patch_filename = f"anchor_{i}_patch.png"
                patch_path = os.path.join(save_dir, patch_filename)
                patch.save(patch_path)
                
                # Save embedding
                embedding_filename = f"anchor_{i}_embedding.npy"
                embedding_path = os.path.join(save_dir, embedding_filename)
                np.save(embedding_path, embedding)
                
                # Add to model data
                anchor_data = AnchorPointData(
                    element_id=str(anchor["element_id"]),
                    element_type=anchor["element_type"],
                    bbox=anchor["bbox"],
                    source=anchor["source"],
                    constraint_direction=anchor["constraint_direction"],
                    constraint_ratio=anchor["constraint_ratio"],
                    stability_score=float(anchor["stability_score"]),
                    patch_path=patch_filename,
                    embedding_path=embedding_filename
                )
                model_data.anchor_points.append(anchor_data)
            
            # Save main area reference patches
            # Use the original image as a reference
            main_area_patch = image.crop((main_area[0], main_area[1], main_area[2], main_area[3]))
            main_area_embedding = self.embedder.get_embedding(main_area_patch)
            
            # Save main area patch and embedding
            patch_filename = "main_area_0_patch.png"
            patch_path = os.path.join(save_dir, patch_filename)
            main_area_patch.save(patch_path)
            
            embedding_filename = "main_area_0_embedding.npy"
            embedding_path = os.path.join(save_dir, embedding_filename)
            np.save(embedding_path, main_area_embedding)
            
            # Add to model data
            main_area_data = MainAreaReferenceData(
                bbox=main_area,
                frame_index=0,
                patch_path=patch_filename,
                embedding_path=embedding_filename
            )
            model_data.main_area_references.append(main_area_data)
            
            # Save model metadata
            model_path = os.path.join(save_dir, "model.json")
            with open(model_path, "w") as f:
                f.write(model_data.json(indent=2))
            
            logger.info(f"Saved model data to {save_dir}")
        
        return {
            "success": True,
            "anchor_points": anchor_points,
            "main_area": main_area
        }
