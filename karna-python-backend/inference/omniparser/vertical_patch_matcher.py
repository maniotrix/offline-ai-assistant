import os
import numpy as np
from PIL import Image
from typing import Optional, List, Set
from inference.omniparser.patch_matcher import PatchMatcher, PatchMatchResult, KNOWN_SOURCE_TYPES
from inference.omniparser.omni_helper import OmniParserResultModel


class VerticalPatchMatcher(PatchMatcher):
    """
    A specialized PatchMatcher for UI screens that searches for matches 
    by scanning vertically from the bottom of the screen to the top.
    Useful for matching UI elements where a bottom-to-top search order is preferred.
    # TODO: Need to revist the vertical pan , current algo scan whole image, and then decides the best match.
    #       However, if a match is found >= similarity_threshold, search is stopped.
    #       so if multiple matches are found, the topmost match will be returned, if all are below similarity_threshold.
    """
    
    def __init__(
        self, 
        model_name: str = 'resnet50', 
        layer_name: str = 'avgpool',
        similarity_threshold: float = 0.75,
        identical_threshold: Optional[float] = None,
        source_types: Optional[List[str]] = None,
        device: Optional[str] = None
    ):
        """
        Initialize the VerticalPatchMatcher.
        
        Args:
            model_name: Name of the ResNet model to use
            layer_name: Name of the layer to extract features from
            similarity_threshold: Threshold for determining a regular match (0-1)
            identical_threshold: Threshold for determining an identical match (0-1)
                                If None, defaults to 0.85 for resnet50/avgpool or 0.80 for others
            source_types: List of source types to match against
            device: Device to run inference on ('cuda', 'cpu')
        """
        super().__init__(model_name=model_name, layer_name=layer_name, 
                         similarity_threshold=similarity_threshold,
                         source_types=source_types, device=device)
        
        # Set the identical threshold based on model if not provided
        if identical_threshold is None:
            if self.model_name == 'resnet50' and self.layer_name == 'avgpool':
                self.identical_threshold = 0.85
            else:
                self.identical_threshold = 0.80
        else:
            self.identical_threshold = identical_threshold
    
    def find_matching_element(
        self,
        patch: Image.Image,
        omniparser_result: OmniParserResultModel,
        source_types: Optional[List[str]] = None,
        custom_threshold: Optional[float] = None
    ) -> PatchMatchResult:
        """
        Find an element in the OmniParserResultModel that matches the given patch,
        scanning vertically from the bottom of the UI screen to the top.
        
        Args:
            patch: The patch image to match
            omniparser_result: The OmniParserResultModel containing elements to match against
            source_types: Optional list of source types to filter by
            custom_threshold: Optional custom similarity threshold to use for this search
            
        Returns:
            PatchMatchResult: The result of the matching process
        """
        # Use provided source_types or fall back to instance source_types
        active_source_types = set(source_types) if source_types is not None else self.source_types
        
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
        
        # Filter by source type and sort by vertical position (bottom to top)
        # We use the bottom edge (y2) of each bounding box for sorting
        sorted_elements = sorted(
            [pc for pc in omniparser_result.parsed_content_results if pc.source in active_source_types],
            key=lambda pc: pc.bbox[3],  # y2 (bottom edge) is at index 3 in bbox [x1, y1, x2, y2]
            reverse=True  # Descending order (bottom to top)
        )
        
        # Compare against each parsed element in bottom-to-top order
        for parsed_content in sorted_elements:
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
        
        # Use custom threshold if provided, otherwise use instance threshold
        threshold = custom_threshold if custom_threshold is not None else self.similarity_threshold
        
        # Determine if a match was found based on threshold
        match_found = best_similarity >= threshold
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
        omniparser_result: OmniParserResultModel,
        source_types: Optional[List[str]] = None
    ) -> PatchMatchResult:
        """
        Find an identical element in the OmniParserResultModel,
        scanning from bottom to top with a higher similarity threshold.
        
        Args:
            patch: The patch image to match
            omniparser_result: The OmniParserResultModel containing elements to match against
            source_types: Optional list of source types to filter by
            
        Returns:
            PatchMatchResult: The result of the matching process
        """
        # Use the identical_threshold with find_matching_element
        return self.find_matching_element(
            patch=patch,
            omniparser_result=omniparser_result,
            source_types=source_types,
            custom_threshold=self.identical_threshold
        ) 