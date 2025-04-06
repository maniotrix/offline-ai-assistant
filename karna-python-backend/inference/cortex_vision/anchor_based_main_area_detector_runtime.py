import numpy as np
from PIL import Image
import logging
from typing import List, Dict, Tuple, Optional, Any, Union, Set
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
        anchor_match_threshold: float = 0.8,
        sliding_window_steps: int = 5,
        sliding_window_sizes: List[float] = None
    ):
        """
        Initialize the runtime detector.
        
        Args:
            model_name: ResNet model to use for embeddings
            main_area_match_threshold: Threshold for main area patch matching
            anchor_match_threshold: Threshold for anchor point matching
            sliding_window_steps: Number of steps for the sliding window in each dimension
            sliding_window_sizes: List of window sizes as fractions of image size (e.g., [0.5, 0.6, 0.7])
        """
        self.embedder = ResNetImageEmbedder(model_name=model_name)
        self.main_area_match_threshold = main_area_match_threshold
        self.anchor_match_threshold = anchor_match_threshold
        self.sliding_window_steps = sliding_window_steps
        self.sliding_window_sizes = sliding_window_sizes or [0.4, 0.5, 0.6, 0.7, 0.8]
        
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
        Load anchor points and generate their visual embeddings at runtime.
        
        Args:
            model_dir: Directory containing the model files
            anchor_points: List of anchor point data
            
        Returns:
            List of anchor points with loaded patches and generated embeddings
        """
        loaded_anchors = []
        
        for anchor in anchor_points:
            # Load the patch image
            patch_path = os.path.join(model_dir, anchor.patch_path)
            if not os.path.exists(patch_path):
                logger.warning(f"Anchor patch not found: {patch_path}")
                continue
            
            patch = Image.open(patch_path).convert("RGB")
            
            # Generate embedding at runtime
            try:
                embedding = self.embedder.get_embedding(patch)
                
                # Create loaded anchor with patch and embedding
                loaded_anchor = {
                    "element_id": str(anchor.element_id),
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
            except Exception as e:
                logger.error(f"Failed to generate embedding for anchor: {e}")
                continue
        
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
    
    def _generate_candidate_regions(
        self, 
        image: Image.Image, 
        result_model: OmniParserResultModel
    ) -> List[Tuple[List[float], Image.Image]]:
        """
        Generate candidate regions using a sliding window approach and UI element hints.
        
        Args:
            image: Current image
            result_model: OmniParser result with parsed content
            
        Returns:
            List of tuples with (bbox, image_patch)
        """
        regions = []
        
        # Image dimensions
        width, height = image.size
        
        # 1. Generate windows based on sliding window approach
        for scale in self.sliding_window_sizes:
            window_width = int(width * scale)
            window_height = int(height * scale)
            
            step_x = max(1, int(window_width / self.sliding_window_steps))
            step_y = max(1, int(window_height / self.sliding_window_steps))
            
            for y in range(0, height - window_height + 1, step_y):
                for x in range(0, width - window_width + 1, step_x):
                    bbox = [x, y, x + window_width, y + window_height]
                    patch = self._extract_patch(image, bbox)
                    regions.append((bbox, patch))
        
        # 2. Add regions based on UI element clusters (if available)
        if result_model and result_model.parsed_content_results:
            element_clusters = self._find_element_clusters(result_model.parsed_content_results)
            
            for cluster_bbox in element_clusters:
                # Ensure minimum size
                cluster_width = cluster_bbox[2] - cluster_bbox[0]
                cluster_height = cluster_bbox[3] - cluster_bbox[1]
                
                if cluster_width < 100 or cluster_height < 100:
                    continue
                
                # Add some padding
                padding_x = width * 0.02
                padding_y = height * 0.02
                
                padded_bbox = [
                    max(0, cluster_bbox[0] - padding_x),
                    max(0, cluster_bbox[1] - padding_y),
                    min(width, cluster_bbox[2] + padding_x),
                    min(height, cluster_bbox[3] + padding_y)
                ]
                
                patch = self._extract_patch(image, padded_bbox)
                regions.append((padded_bbox, patch))
        
        logger.info(f"Generated {len(regions)} candidate regions")
        return regions
    
    def _find_element_clusters(self, elements: List[ParsedContentResult]) -> List[List[float]]:
        """
        Find clusters of UI elements that might represent content areas.
        
        Args:
            elements: List of parsed content results
            
        Returns:
            List of bounding boxes [x1, y1, x2, y2] for detected clusters
        """
        if not elements:
            return []
        
        clusters = []
        
        # Simple approach: find large groups of elements that are close together
        # This could be enhanced with a proper clustering algorithm
        
        # 1. Sort elements by size (area)
        sorted_elements = sorted(
            elements, 
            key=lambda e: (e.bbox[2] - e.bbox[0]) * (e.bbox[3] - e.bbox[1]),
            reverse=True
        )
        
        # 2. Start with larger elements and grow clusters
        processed_elements = set()
        
        for i, element in enumerate(sorted_elements):
            if i in processed_elements:
                continue
                
            # Start a new cluster with this element
            cluster_elements = [i]
            processed_elements.add(i)
            
            # Find nearby elements
            for j, other in enumerate(sorted_elements):
                if j in processed_elements:
                    continue
                    
                # Check if close to any element in the current cluster
                for cluster_idx in cluster_elements:
                    cluster_element = sorted_elements[cluster_idx]
                    
                    # Check proximity
                    if self._elements_are_close(cluster_element, other):
                        cluster_elements.append(j)
                        processed_elements.add(j)
                        break
            
            # If cluster has enough elements, calculate its bounding box
            if len(cluster_elements) >= 3:  # Minimum size for a content cluster
                min_x = min(sorted_elements[idx].bbox[0] for idx in cluster_elements)
                min_y = min(sorted_elements[idx].bbox[1] for idx in cluster_elements)
                max_x = max(sorted_elements[idx].bbox[2] for idx in cluster_elements)
                max_y = max(sorted_elements[idx].bbox[3] for idx in cluster_elements)
                
                clusters.append([min_x, min_y, max_x, max_y])
        
        return clusters
    
    def _elements_are_close(self, elem1: ParsedContentResult, elem2: ParsedContentResult) -> bool:
        """Check if two elements are close to each other."""
        # Calculate centers
        center1_x = (elem1.bbox[0] + elem1.bbox[2]) / 2
        center1_y = (elem1.bbox[1] + elem1.bbox[3]) / 2
        center2_x = (elem2.bbox[0] + elem2.bbox[2]) / 2
        center2_y = (elem2.bbox[1] + elem2.bbox[3]) / 2
        
        # Calculate distance
        distance = ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5
        
        # Check overlap
        overlap_x = (elem1.bbox[0] <= elem2.bbox[2] and elem2.bbox[0] <= elem1.bbox[2])
        overlap_y = (elem1.bbox[1] <= elem2.bbox[3] and elem2.bbox[1] <= elem1.bbox[3])
        
        # Consider close if overlapping or distance is small relative to element size
        elem1_size = max(elem1.bbox[2] - elem1.bbox[0], elem1.bbox[3] - elem1.bbox[1])
        elem2_size = max(elem2.bbox[2] - elem2.bbox[0], elem2.bbox[3] - elem2.bbox[1])
        avg_size = (elem1_size + elem2_size) / 2
        
        return (overlap_x and overlap_y) or distance < avg_size * 2
    
    def _match_main_area_with_sliding_window(
        self,
        image: Image.Image,
        result_model: OmniParserResultModel,
        main_areas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Match main area references using a sliding window approach.
        
        Args:
            image: Current image
            result_model: OmniParser result with parsed content
            main_areas: List of main area references
            
        Returns:
            Dictionary with match results
        """
        logger.info("Matching main area using sliding window approach")
        
        best_match = {
            "match_found": False,
            "confidence": 0.0,
            "bbox": None,
            "reference": None,
            "region_bbox": None
        }
        
        # Generate candidate regions
        candidate_regions = self._generate_candidate_regions(image, result_model)
        
        # For each reference patch
        for reference in main_areas:
            reference_embedding = reference["embedding"]
            
            # For each candidate region
            for region_bbox, region_patch in candidate_regions:
                # Generate embedding for this region
                try:
                    region_embedding = self.embedder.get_embedding(region_patch)
                    
                    # Compare with reference embedding
                    similarity = np.dot(region_embedding, reference_embedding)
                    
                    if similarity > best_match["confidence"] and similarity >= self.main_area_match_threshold:
                        # Save this as the best match
                        best_match["match_found"] = True
                        best_match["confidence"] = similarity
                        best_match["bbox"] = region_bbox
                        best_match["reference"] = reference
                        best_match["region_bbox"] = region_bbox
                except Exception as e:
                    logger.warning(f"Error calculating embedding for region: {e}")
        
        # If a match was found, refine it using UI elements if possible
        if best_match["match_found"] and result_model and result_model.parsed_content_results:
            refined_bbox = self._refine_main_area_with_elements(
                best_match["bbox"], 
                result_model.parsed_content_results
            )
            
            if refined_bbox:
                best_match["bbox"] = refined_bbox
                best_match["refined"] = True
        
        return best_match
    
    def _refine_main_area_with_elements(
        self, 
        initial_bbox: List[float], 
        elements: List[ParsedContentResult]
    ) -> List[float]:
        """
        Refine a main area bounding box using UI elements.
        
        Args:
            initial_bbox: Initial bounding box [x1, y1, x2, y2]
            elements: List of parsed content results
            
        Returns:
            Refined bounding box
        """
        # Find elements that overlap significantly with the initial bbox
        contained_elements = []
        partial_elements = []
        
        for element in elements:
            overlap = self._calculate_overlap(element.bbox, initial_bbox)
            
            if overlap > 0.8:  # Element mostly inside
                contained_elements.append(element)
            elif overlap > 0.3:  # Element partially inside
                partial_elements.append(element)
        
        # If no contained elements, return the initial bbox
        if not contained_elements:
            return initial_bbox
        
        # Calculate bounds from contained elements
        min_x = min(e.bbox[0] for e in contained_elements)
        min_y = min(e.bbox[1] for e in contained_elements)
        max_x = max(e.bbox[2] for e in contained_elements)
        max_y = max(e.bbox[3] for e in contained_elements)
        
        # Add some padding
        padding_x = (initial_bbox[2] - initial_bbox[0]) * 0.05
        padding_y = (initial_bbox[3] - initial_bbox[1]) * 0.05
        
        refined_bbox = [
            max(initial_bbox[0], min_x - padding_x),
            max(initial_bbox[1], min_y - padding_y),
            min(initial_bbox[2], max_x + padding_x),
            min(initial_bbox[3], max_y + padding_y)
        ]
        
        return refined_bbox
    
    def _calculate_overlap(self, bbox1: List[float], bbox2: List[float]) -> float:
        """
        Calculate the overlap ratio between two bounding boxes.
        
        Args:
            bbox1: First bounding box [x1, y1, x2, y2]
            bbox2: Second bounding box [x1, y1, x2, y2]
            
        Returns:
            Overlap ratio (0-1)
        """
        # Calculate intersection
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])
        
        if x2 <= x1 or y2 <= y1:
            return 0.0  # No overlap
        
        intersection = (x2 - x1) * (y2 - y1)
        
        # Calculate area of bbox1
        area1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        
        # Return ratio of intersection to bbox1 area
        return intersection / area1 if area1 > 0 else 0.0
    
    def _match_and_reconstruct_from_anchors(
        self,
        image: Image.Image,
        result_model: OmniParserResultModel,
        anchors: List[Dict[str, Any]],
        original_main_area: List[float],
        original_dimensions: List[float]
    ) -> Dict[str, Any]:
        """
        Match anchor points and reconstruct the main area using directional constraints.
        
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
            
            # Refine using UI elements if possible
            if result_model and result_model.parsed_content_results:
                refined_bbox = self._refine_main_area_with_elements(
                    reconstructed_bbox,
                    result_model.parsed_content_results
                )
                
                if refined_bbox:
                    reconstructed_bbox = refined_bbox
            
            # Calculate confidence based on number of matched anchors and their scores
            anchor_count_factor = min(len(matched_anchors) / 4, 1.0)  # 4+ anchors = full confidence
            avg_score = sum(match_data["score"] for match_data in matched_anchors) / len(matched_anchors)
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
        
        # Step 1: Try sliding window matching with main area references
        main_area_result = self._match_main_area_with_sliding_window(image, result_model, loaded_main_areas)
        
        if main_area_result["match_found"] and main_area_result["confidence"] >= 0.8:
            logger.info("Main area matched with sliding window with high confidence")
            return {
                "success": True,
                "main_area": main_area_result["bbox"],
                "method": "sliding_window_match",
                "confidence": main_area_result["confidence"],
                "refined": main_area_result.get("refined", False)
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
                        "method": "sliding_window_match",
                        "confidence": main_area_result["confidence"]
                    }
            
            return {
                "success": True,
                "main_area": anchor_result["bbox"],
                "method": "anchor_reconstruction",
                "confidence": anchor_result["confidence"],
                "anchors_matched": anchor_result["anchors_matched"]
            }
        
        # If sliding window match found but with low confidence, use it as fallback
        if main_area_result["match_found"]:
            logger.info("Using sliding window match as fallback (low confidence)")
            return {
                "success": True,
                "main_area": main_area_result["bbox"],
                "method": "sliding_window_fallback",
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