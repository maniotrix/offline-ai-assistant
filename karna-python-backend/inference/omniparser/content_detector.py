import logging
from typing import List, Dict, Any, Optional
from PIL import Image

from .ui_dynamic_area_detector import UIOptimizedDynamicAreaDetector
from .main_area_segmenter import MainAreaSegmenter
from .omni_helper import OmniParserResultModelList, OmniParserResultModel

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ContentDetector:
    """
    Integrated content detection system that combines dynamic area detection
    with content-based segmentation for more accurate content identification.
    """
    
    def __init__(
        self,
        dynamic_detector: Optional[UIOptimizedDynamicAreaDetector] = None,
        segmenter: Optional[MainAreaSegmenter] = None
    ):
        """
        Initialize the content detector.
        
        Args:
            dynamic_detector: Optional UIOptimizedDynamicAreaDetector instance
            segmenter: Optional MainAreaSegmenter instance
        """
        self.dynamic_detector = dynamic_detector or UIOptimizedDynamicAreaDetector()
        self.segmenter = segmenter or MainAreaSegmenter()
        
        logger.info("ContentDetector initialized")
    
    def detect(
        self,
        results_list: OmniParserResultModelList,
        current_frame: Optional[OmniParserResultModel] = None
    ) -> Dict[str, Any]:
        """
        Detect main content areas in a sequence of frames.
        
        Args:
            results_list: List of OmniParser results for multiple frames
            current_frame: Optional current frame to analyze (if None, use last frame)
            
        Returns:
            Dictionary with detection results including main areas and content clusters
        """
        logger.info("Starting content detection")
        
        # Step 1: Use dynamic detector to find main content areas
        dynamic_results = self.dynamic_detector.detect_main_areas(results_list)
        
        # Use current frame or last frame for segmentation
        if current_frame is None and results_list.omniparser_result_models:
            current_frame = results_list.omniparser_result_models[-1]
        
        if not current_frame:
            logger.warning("No current frame available for segmentation")
            return dynamic_results
        
        # Get image from current frame
        image_path = current_frame.omniparser_result.original_image_path
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            return dynamic_results
        
        # Step 2: Apply content-based segmentation to main content area
        main_area_bbox = dynamic_results.get("main_content_area")
        
        if main_area_bbox is None:
            # Try alternative areas if main_content_area not found
            main_area_bbox = dynamic_results.get("vertical_union") or dynamic_results.get("largest_area")
        
        if main_area_bbox is None:
            logger.warning("No main area detected for segmentation")
            return dynamic_results
        
        # Perform segmentation
        try:
            segmentation_results = self.segmenter.segment(
                image, current_frame, main_area_bbox
            )
            
            # Combine results
            result = {
                "dynamic_areas": dynamic_results,
                "content_segmentation": segmentation_results,
                "main_content_bbox": segmentation_results.get("primary_content") or main_area_bbox
            }
            
            logger.info("Content detection completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during content segmentation: {e}")
            # Return dynamic results as fallback
            return {"dynamic_areas": dynamic_results, "main_content_bbox": main_area_bbox}
    
    def visualize(
        self,
        detection_result: Dict[str, Any],
        image_path: str,
        output_path: str
    ) -> None:
        """
        Visualize detection results.
        
        Args:
            detection_result: Result from detect()
            image_path: Path to the original image
            output_path: Path to save visualization
        """
        try:
            image = Image.open(image_path).convert("RGB")
            
            # Get main area bbox
            main_area_bbox = detection_result.get("dynamic_areas", {}).get("main_content_area")
            if main_area_bbox is None:
                main_area_bbox = detection_result.get("dynamic_areas", {}).get("vertical_union")
                if main_area_bbox is None:
                    main_area_bbox = detection_result.get("dynamic_areas", {}).get("largest_area")
            
            if "content_segmentation" in detection_result and main_area_bbox is not None:
                # Use segmenter visualization
                vis_img = self.segmenter.visualize(
                    image,
                    detection_result["content_segmentation"],
                    main_area_bbox,
                    output_path
                )
            else:
                # Basic visualization
                from PIL import ImageDraw
                vis_img = image.copy()
                draw = ImageDraw.Draw(vis_img)
                
                # Draw available areas
                areas = detection_result.get("dynamic_areas", {})
                for area_name, bbox in areas.items():
                    if bbox:
                        color = "red"
                        if area_name == "main_content_area":
                            color = "green"
                        elif area_name == "vertical_union":
                            color = "blue"
                        
                        draw.rectangle(
                            [(bbox[0], bbox[1]), (bbox[2], bbox[3])],
                            outline=color,
                            width=2
                        )
                        draw.text(
                            (bbox[0] + 5, bbox[1] + 5),
                            area_name,
                            fill=color
                        )
                
                # Save visualization
                vis_img.save(output_path)
                
            logger.info(f"Visualization saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}") 