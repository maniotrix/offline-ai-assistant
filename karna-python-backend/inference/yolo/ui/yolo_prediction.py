from ultralytics import YOLO # type: ignore
from inference.yolo.yolo_utils import export_bounding_boxes
from inference import BaseInference, BoundingBoxResult
import os
from PIL import Image
from typing import Union, List, Any
import numpy as np
import uuid
import tempfile

class YOLO_UI_Prediction(BaseInference):
    """
    YOLO prediction class.
    """
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "model/yolo11x_web_ui_1024_50_epoch_best.pt"))
    def __init__(self):
        """
        Initialize the YOLO prediction class.
        """
        super().__init__()
        self.model = YOLO(self.model_path)
        self.logger.info(f"YOLO model loaded from {self.model_path}")

    def predict(self, image: Union[str, Image.Image]):
        """
        Predict the bounding boxes of the image.
        Args:
            image: Either a path to an image (str) or a PIL Image object.
        Returns:
            results (Any): The results of the prediction.
        """
        results = self.model(image)
        self.logger.info(f"YOLO single image prediction results: {results}")
        return results

    def predict_batch(self, images: List[Union[str, Image.Image]]):
        """
        Predict the bounding boxes of the images.
        Args:
            images: List of either image paths (str) or PIL Image objects.
        Returns:
            results (list[Any]): The results of the prediction.
        """
        results = []
        for image in images:
            results.append(self.predict(image))
        self.logger.info(f"YOLO batch prediction results: {results}")
        return results
    
    def predict_and_export_bboxes(self, image: Union[str, Image.Image]):
        """
        Predict the bounding boxes of the image and export the results.
        Args:
            image: Either a path to an image (str) or a PIL Image object.
        Returns:
            BoundingBoxResult: Object containing image information and bounding boxes with fields:
                    image_path: Path to the image (or a generated ID for PIL images)
                    original_width: Original width of the image
                    original_height: Original height of the image
                    bounding_boxes: List of BoundingBox objects
        """
        results = self.predict(image)
        
        # Handle PIL Image objects
        if isinstance(image, Image.Image):
            # Create a temporary file to save the image for processing
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                image.save(temp_path)
                
            bbox_result = export_bounding_boxes(self.model, image_path=temp_path, results=results)
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            # Update the image_path to indicate it was from a PIL Image
            bbox_result.image_path = f"pil_image_{uuid.uuid4()}"
            
            return bbox_result
        else:
            # Handle string paths as before
            return export_bounding_boxes(self.model, image_path=image, results=results)
    
    def predict_and_export_bboxes_batch(self, images: List[Union[str, Image.Image]]):
        """
        Predict the bounding boxes of the images and export the results.
        Args:
            images: List of either image paths (str) or PIL Image objects.
        Returns:
            list[BoundingBoxResult]: List of objects containing image information and bounding boxes.
            Each BoundingBoxResult has fields:
                image_path: Path to the image (or a generated ID for PIL images)
                original_width: Original width of the image
                original_height: Original height of the image
                bounding_boxes: List of BoundingBox objects
        """
        self.logger.info(f"YOLO batch prediction started for {len(images)} images")
        results = []
        for image in images:
            results.append(self.predict_and_export_bboxes(image))
        self.logger.info(f"YOLO batch prediction results: {results}")
        return results
    
    def predict_pil_image(self, pil_image: Image.Image):
        """
        Predict the bounding boxes of a PIL image.
        Args:
            pil_image (Image.Image): The PIL Image object.
        Returns:
            results (Any): The results of the prediction.
        """
        return self.predict(pil_image)
    
    def predict_and_export_bboxes_pil(self, pil_image: Image.Image):
        """
        Predict the bounding boxes of a PIL image and export the results.
        Args:
            pil_image (Image.Image): The PIL Image object.
        Returns:
            BoundingBoxResult: Object containing image information and bounding boxes.
        """
        return self.predict_and_export_bboxes(pil_image)


# if __name__ == "__main__":
#     # 
#     import json
#     yolo_prediction = YOLO_UI_Prediction()
#     screenshot_events_json_path = "data/youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
    
#     with open(screenshot_events_json_path, "r") as f:
#         screenshot_events = json.load(f)
#     print(screenshot_events)
    
#     screenshot_paths = [event["screenshot_path"] for event in screenshot_events]
    
#     results = yolo_prediction.predict_and_export_bboxes_batch(screenshot_paths)
#     print(len(results))
#     print(results)