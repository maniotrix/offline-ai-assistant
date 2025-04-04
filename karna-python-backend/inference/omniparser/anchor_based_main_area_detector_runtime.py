import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple, Optional, Any, Union
import os
import json
from pydantic import BaseModel, Field
from pathlib import Path

# Import from existing components
from .image_comparison import ResNetImageEmbedder
from .omni_helper import OmniParserResultModel, ParsedContentResult

# Import shared data models
from .anchor_based_main_area_detector import AnchorPointData, MainAreaReferenceData, DetectionModelData

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class AnchorBasedMainAreaDetectorRuntime:
    """
    Runtime detector that loads a trained model to detect main content areas
    in new screenshots without needing the original training data.
    """
    
    def __init__(
        self,
        model_name: str = 'resnet50',
        main_area_match_threshold: float = 0.7,
        anchor_match_threshold: float = 0.8
    ):
        """
        Initialize the runtime detector.
        
        Args:
            model_name: ResNet model to use for embeddings
            main_area_match_threshold: Threshold for main area patch matching
            anchor_match_threshold: Threshold for anchor point matching
        """
        self.embedder = ResNetImageEmbedder(model_name=model_name)
        self.main_area_match_threshold = main_area_match_threshold
        self.anchor_match_threshold = anchor_match_threshold
        
        logger.info(f"AnchorBasedMainAreaDetectorRuntime initialized with model {model_name}")
    
    def _extract_patch(self, image: Image.Image, bbox: List[float]) -> Image.Image:
        """Extract a patch from an image using a bounding box."""
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        return image.crop((x1, y1, x2, y2))
    
    def load_model(self, model_dir: str) -> DetectionModelData:
        """
        Load a detection model from the specified directory.
        
        Args:
            model_dir: Directory containing the model files
            
        Returns:
            Loaded detection model
        """
        logger.info(f"Loading model from {model_dir}")
        
        # Load model metadata
        model_path = os.path.join(model_dir, "model.json")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, "r") as f:
            model_json = f.read()
        
        # Parse model data
        model_data = DetectionModelData.parse_raw(model_json)
        
        logger.info(f"Loaded model (version {model_data.model_version}) created at {model_data.model_created_at}")
        return model_data
    
    def load_anchors_with_embeddings(
        self, 
        model_dir: str, 
        anchor_points: List[AnchorPointData]
    ) -> List[Dict[str, Any]]:
        """
        Load anchor points with their visual embeddings.
        
        Args:
            model_dir: Directory containing the model files
            anchor_points: List of anchor point data
            
        Returns:
            List of anchor points with loaded patches and embeddings
        """
        loaded_anchors = []
        
        for anchor in anchor_points:
            # Load the patch image
            patch_path = os.path.join(model_dir, anchor.patch_path)
            if not os.path.exists(patch_path):
                logger.warning(f"Anchor patch not found: {patch_path}")
                continue
            
            patch = Image.open(patch_path).convert("RGB")
            
            # Load the embedding if it exists
            embedding_path = os.path.join(model_dir, anchor.embedding_path)
            if os.path.exists(embedding_path):
                embedding = np.load(embedding_path)
            else:
                # Generate embedding if file not found
                logger.warning(f"Embedding file not found: {embedding_path}")
                try:
                    embedding = self.embedder.get_embedding(patch)
                except Exception as e:
                    logger.error(f"Failed to generate embedding: {e}")
                    continue
            
            # Create loaded anchor with patch and embedding
            loaded_anchor = {
                "element_id": anchor.element_id,
                "element_type": anchor.element_type,
                "bbox": anchor.bbox,
                "source": anchor.source,
                "constraint_direction": anchor.constraint_direction,
                "horizontal_relation": anchor.horizontal_relation,
                "vertical_relation": anchor.vertical_relation,
                "stability_score": anchor.stability_score,
                "patch": patch,
                "embedding": embedding
            }
            
            loaded_anchors.append(loaded_anchor)
        
        logger.info(f"Loaded {len(loaded_anchors)} anchor points with embeddings")
        return loaded_anchors
    
    def load_main_areas_with_embeddings(
        self, 
        model_dir: str, 
        main_area_references: List[MainAreaReferenceData]
    ) -> List[Dict[str, Any]]:
        """
        Load main area references and generate their visual embeddings at runtime.
        
        Args:
            model_dir: Directory containing the model files
            main_area_references: List of main area reference data
            
        Returns:
            List of main area references with loaded patches and generated embeddings
        """
        loaded_references = []
        
        for reference in main_area_references:
            # Load the patch image
            patch_path = os.path.join(model_dir, reference.patch_path)
            if not os.path.exists(patch_path):
                logger.warning(f"Main area patch not found: {patch_path}")
                continue
            
            patch = Image.open(patch_path).convert("RGB")
            
            # Generate embedding at runtime
            try:
                embedding = self.embedder.get_embedding(patch)
                
                # Create loaded reference with patch and embedding
                loaded_reference = {
                    "bbox": reference.bbox,
                    "frame_index": reference.frame_index,
                    "patch": patch,
                    "embedding": embedding
                }
                
                loaded_references.append(loaded_reference)
            except Exception as e:
                logger.error(f"Failed to generate embedding: {e}")
                continue
        
        logger.info(f"Loaded {len(loaded_references)} main area references with embeddings")
        return loaded_references
    
    def _match_main_area_directly(
        self,
        image: Image.Image,
        main_areas: List[Dict[str, Any]]
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
                similarity = np.dot(image_embedding, reference["embedding"])
                
                if similarity > best_match["confidence"]:
                    best_match["match_found"] = True
                    best_match["confidence"] = similarity
                    best_match["bbox"] = reference["bbox"]
                    best_match["reference"] = reference
            except Exception as e:
                logger.warning(f"Error during direct main area matching: {e}")
        
        return best_match
    
    def _match_and_reconstruct_from_anchors(
        self,
        image: Image.Image,
        result_model: OmniParserResultModel,
        anchors: List[Dict[str, Any]],
        original_main_area: List[float],
        original_dimensions: List[float]
    ) -> Dict[str, Any]:
        """
        Match anchor points and reconstruct the main area using simplified directional constraints.
        
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
                if element.source != anchor["source"]:
                    continue
                
                # Extract element patch
                try:
                    element_patch = self._extract_patch(image, element.bbox)
                    element_embedding = self.embedder.get_embedding(element_patch)
                    
                    # Compare embeddings
                    similarity = np.dot(element_embedding, anchor["embedding"])
                    
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
        
        # Step 2: Reconstruct main area from matched anchors using directional constraints
        if len(matched_anchors) >= 2:
            # Initialize constraints for each edge of the screen
            constraints = {
                "left": None,
                "right": None,
                "top": None,
                "bottom": None
            }
            
            # Get current image dimensions
            image_width = result_model.omniparser_result.original_image_width
            image_height = result_model.omniparser_result.original_image_height
            
            # Apply directional constraints from each matched anchor
            for match_data in matched_anchors:
                anchor = match_data["anchor"]
                element = match_data["match"]
                
                # Get the element center and boundaries
                element_x1, element_y1, element_x2, element_y2 = element.bbox
                element_center_x = (element_x1 + element_x2) / 2
                element_center_y = (element_y1 + element_y2) / 2
                
                # Get the horizontal and vertical relations
                h_relation = anchor["horizontal_relation"]
                v_relation = anchor["vertical_relation"]
                
                # Calculate constraint values (with some padding)
                padding_x = image_width * 0.05  # 5% padding
                padding_y = image_height * 0.05  # 5% padding
                
                # Apply horizontal constraints regardless of primary direction
                if h_relation == "left":
                    # Anchor is left of main area - main area should be to the right of this element
                    if constraints["left"] is None or element_x2 + padding_x > constraints["left"]:
                        constraints["left"] = element_x2 + padding_x
                elif h_relation == "right":
                    # Anchor is right of main area - main area should be to the left of this element
                    if constraints["right"] is None or element_x1 - padding_x < constraints["right"]:
                        constraints["right"] = element_x1 - padding_x
                
                # Apply vertical constraints regardless of primary direction
                if v_relation == "top":
                    # Anchor is above main area - main area should be below this element
                    if constraints["top"] is None or element_y2 + padding_y > constraints["top"]:
                        constraints["top"] = element_y2 + padding_y
                elif v_relation == "bottom":
                    # Anchor is below main area - main area should be above this element
                    if constraints["bottom"] is None or element_y1 - padding_y < constraints["bottom"]:
                        constraints["bottom"] = element_y1 - padding_y
            
            # Calculate the reconstructed bbox using available constraints
            reconstructed_bbox = None
            
            # Default values based on original proportions if constraints are missing
            orig_width, orig_height = original_dimensions
            orig_main_width = original_main_area[2] - original_main_area[0]
            orig_main_height = original_main_area[3] - original_main_area[1]
            
            # Scale factors
            scale_x = image_width / orig_width
            scale_y = image_height / orig_height
            
            # Default main area size (scaled from original)
            default_width = orig_main_width * scale_x
            default_height = orig_main_height * scale_y
            
            # Apply horizontal constraints
            if constraints["left"] is not None and constraints["right"] is not None:
                # We have both left and right constraints
                x1 = constraints["left"]
                x2 = constraints["right"]
            elif constraints["left"] is not None:
                # Only left constraint
                x1 = constraints["left"]
                x2 = min(x1 + default_width, image_width)
            elif constraints["right"] is not None:
                # Only right constraint
                x2 = constraints["right"]
                x1 = max(x2 - default_width, 0)
            else:
                # No horizontal constraints, center it
                x1 = (image_width - default_width) / 2
                x2 = x1 + default_width
            
            # Apply vertical constraints
            if constraints["top"] is not None and constraints["bottom"] is not None:
                # We have both top and bottom constraints
                y1 = constraints["top"]
                y2 = constraints["bottom"]
            elif constraints["top"] is not None:
                # Only top constraint
                y1 = constraints["top"]
                y2 = min(y1 + default_height, image_height)
            elif constraints["bottom"] is not None:
                # Only bottom constraint
                y2 = constraints["bottom"]
                y1 = max(y2 - default_height, 0)
            else:
                # No vertical constraints, center it
                y1 = (image_height - default_height) / 2
                y2 = y1 + default_height
            
            # Clamp to image boundaries
            x1 = max(0, min(x1, image_width))
            y1 = max(0, min(y1, image_height))
            x2 = max(0, min(x2, image_width))
            y2 = max(0, min(y2, image_height))
            
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
    
    def detect(
        self,
        result_model: OmniParserResultModel,
        model_dir: str
    ) -> Dict[str, Any]:
        """
        Detect the main content area in a new frame using a saved model.
        
        Args:
            result_model: OmniParser result for the new frame
            model_dir: Directory containing the trained model
            
        Returns:
            Dictionary with detection results
        """
        logger.info(f"Detecting main content area using model from {model_dir}")
        
        # Load image
        image_path = result_model.omniparser_result.original_image_path
        image = Image.open(image_path).convert("RGB")
        
        # Get image dimensions
        image_width = result_model.omniparser_result.original_image_width
        image_height = result_model.omniparser_result.original_image_height
        
        # Load model data
        model_data = self.load_model(model_dir)
        
        # Load anchors and main areas with their embeddings
        loaded_anchors = self.load_anchors_with_embeddings(model_dir, model_data.anchor_points)
        loaded_main_areas = self.load_main_areas_with_embeddings(model_dir, model_data.main_area_references)
        
        # Step 1: Try direct main area matching
        main_area_result = self._match_main_area_directly(image, loaded_main_areas)
        
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
            image, result_model, loaded_anchors, model_data.main_area,
            model_data.screen_dimensions
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
        orig_main_area = model_data.main_area
        orig_width, orig_height = model_data.screen_dimensions
        
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

# def main():
#     """
#     Example usage of the AnchorBasedMainAreaDetectorRuntime.
    
#     This demonstrates how to:
#     1. Initialize the runtime detector
#     2. Load a model
#     3. Detect main content area in a new frame
#     """
#     import argparse
    
#     # Setup argument parser
#     parser = argparse.ArgumentParser(description="Detect main content area using a trained model")
#     parser.add_argument("--model-dir", type=str, required=True, help="Directory containing the trained model")
#     parser.add_argument("--image-path", type=str, required=True, help="Path to the input image")
#     parser.add_argument("--output-path", type=str, help="Path to save the output image with detected area")
#     args = parser.parse_args()
    
#     # Create result model (normally this would come from OmniParser)
#     # This is just a mock for demonstration purposes
#     result_model = OmniParserResultModel(
#         omniparser_result=None,  # Would normally be populated
#         parsed_content_results=[]  # Would normally be populated
#     )
#     result_model.omniparser_result.original_image_path = args.image_path
    
#     # Load the image to get dimensions
#     image = Image.open(args.image_path)
#     result_model.omniparser_result.original_image_width = image.width
#     result_model.omniparser_result.original_image_height = image.height
    
#     # Initialize the detector
#     detector = AnchorBasedMainAreaDetectorRuntime()
    
#     # Detect main area
#     detection_result = detector.detect(result_model, args.model_dir)
    
#     # Print results
#     print(f"Detection result: {detection_result}")
    
#     # Save output image if requested
#     if args.output_path and detection_result["success"]:
#         # Draw rectangle on image
#         from PIL import ImageDraw
#         draw = ImageDraw.Draw(image)
#         bbox = detection_result["main_area"]
#         draw.rectangle(
#             [(bbox[0], bbox[1]), (bbox[2], bbox[3])],
#             outline="red",
#             width=3
#         )
        
#         # Add detection info
#         draw.text(
#             (10, 10),
#             f"Method: {detection_result['method']}, Confidence: {detection_result['confidence']:.2f}",
#             fill="red"
#         )
        
#         # Save image
#         image.save(args.output_path)
#         print(f"Output image saved to {args.output_path}")

# if __name__ == "__main__":
#     main() 