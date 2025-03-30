import os
import numpy as np
from PIL import Image
from typing import Optional, Dict, Tuple, List, Union
from image_comparison import ResNetImageEmbedder
from dataclasses import dataclass
from omni_helper import OmniParserResultModel, ParsedContentResult

@dataclass
class PatchMatchResult:
    """
    Results of matching an image patch to OmniParserResultModel elements.
    """
    match_found: bool
    matched_element_id: Optional[int] = None
    similarity_score: Optional[float] = None
    classification: Optional[str] = None
    parsed_content_result: Optional[ParsedContentResult] = None
    omniparser_result_model: Optional[OmniParserResultModel] = None

class PatchMatcher(ResNetImageEmbedder):
    """
    A class for matching image patches to elements in OmniParserResultModel objects.
    Inherits from ResNetImageEmbedder to use its image embedding and similarity functions.
    """
    def __init__(
        self, 
        model_name: str = 'resnet50', 
        layer_name: str = 'avgpool',
        similarity_threshold: float = 0.85,
        device: Optional[str] = None
    ):
        """
        Initialize the PatchMatcher.
        
        Args:
            model_name: Name of the ResNet model to use ('resnet18', 'resnet34', 'resnet50')
            layer_name: Name of the layer to extract features from
            similarity_threshold: Threshold for determining a match (0-1)
            device: Device to run inference on ('cuda', 'cpu'). If None, will use CUDA if available.
        """
        super().__init__(model_name=model_name, layer_name=layer_name, device=device)
        self.similarity_threshold = similarity_threshold
    
    def extract_image_from_bbox(
        self, 
        full_image: Image.Image, 
        bbox: List[float]
    ) -> Image.Image:
        """
        Extract a sub-image from the full image using bounding box coordinates.
        
        Args:
            full_image: The full PIL image
            bbox: Bounding box coordinates [x1, y1, x2, y2] in absolute pixels
            
        Returns:
            PIL.Image: The extracted sub-image
        """
        # Ensure bbox values are integers for PIL
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        
        # Crop the image
        sub_image = full_image.crop((x1, y1, x2, y2))
        return sub_image
    
    def find_matching_element(
        self,
        patch: Image.Image,
        omniparser_result: OmniParserResultModel
    ) -> PatchMatchResult:
        """
        Find an element in the OmniParserResultModel that matches the given patch.
        
        Args:
            patch: The patch image to match
            omniparser_result: The OmniParserResultModel containing elements to match against
            
        Returns:
            PatchMatchResult: The result of the matching process
        """
        # Get the full image
        original_image_path = omniparser_result.omniparser_result.original_image_path
        if not os.path.exists(original_image_path):
            raise FileNotFoundError(f"Original image not found: {original_image_path}")
        
        full_image = Image.open(original_image_path)
        
        # Compute the embedding for the patch
        patch_embedding = self.get_embedding(patch)
        
        best_similarity = 0.0
        best_match_id = None
        best_parsed_content = None
        
        # Compare against each parsed element
        for parsed_content in omniparser_result.parsed_content_results:
            # Extract the element image using the bounding box
            bbox = parsed_content.bbox
            try:
                element_image = self.extract_image_from_bbox(full_image, bbox)
                
                # Compute similarity
                element_embedding = self.get_embedding(element_image)
                similarity = np.dot(patch_embedding, element_embedding)
                
                # Update best match if current similarity is higher
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_id = parsed_content.id
                    best_parsed_content = parsed_content
            except Exception as e:
                print(f"Error processing element {parsed_content.id}: {e}")
        
        # Determine if a match was found based on threshold
        match_found = best_similarity >= self.similarity_threshold
        classification = self.classify_similarity(best_similarity) if match_found else None
        
        # Return the result
        return PatchMatchResult(
            match_found=match_found,
            matched_element_id=best_match_id if match_found else None,
            similarity_score=best_similarity if match_found else None,
            classification=classification,
            parsed_content_result=best_parsed_content if match_found else None,
            omniparser_result_model=omniparser_result if match_found else None
        )

    def find_identical_element(
        self,
        patch: Image.Image,
        omniparser_result: OmniParserResultModel
    ) -> PatchMatchResult:
        """
        Find an identical element in the OmniParserResultModel.
        This is a convenience method that sets a high threshold for "identical" matches.
        
        Args:
            patch: The patch image to match
            omniparser_result: The OmniParserResultModel containing elements to match against
            
        Returns:
            PatchMatchResult: The result of the matching process
        """
        # Temporarily save the current threshold
        current_threshold = self.similarity_threshold
        
        # Set a high threshold for identical matches
        # Use 0.85 for ResNet-50 with avgpool, 0.80 for others (as recommended in docs)
        if self.model_name == 'resnet50' and self.layer_name == 'avgpool':
            self.similarity_threshold = 0.85
        else:
            self.similarity_threshold = 0.80
        
        # Find the matching element
        result = self.find_matching_element(patch, omniparser_result)
        
        # Restore the original threshold
        self.similarity_threshold = current_threshold
        
        return result
    
    def match_patch_across_multiple_results(
        self,
        patch: Image.Image,
        omniparser_results: List[OmniParserResultModel]
    ) -> List[PatchMatchResult]:
        """
        Find matches for a patch across multiple OmniParserResultModel objects.
        
        Args:
            patch: The patch image to match
            omniparser_results: List of OmniParserResultModel objects to search through
            
        Returns:
            List[PatchMatchResult]: List of match results, one for each input result model
        """
        match_results = []
        
        for result_model in omniparser_results:
            match_result = self.find_matching_element(patch, result_model)
            if match_result.match_found:
                match_results.append(match_result)
        
        return match_results 