from ultralytics import YOLO # type: ignore
from inference.yolo.ui.yolo_utils import export_bounding_boxes
from inference import BaseInference
import os
class YOLOPrediction(BaseInference):
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

    def predict(self, image_path: str):
        """
        Predict the bounding boxes of the image.
        Args:
            image_path (str): The path to the image.
        Returns:
            results (Any): The results of the prediction.
        """
        results = self.model(image_path)
        self.logger.info(f"YOLO single image prediction results: {results}")
        return results

    def predict_batch(self, image_paths: list[str]):
        """
        Predict the bounding boxes of the images.
        Args:
            image_paths (list[str]): The paths to the images.
        Returns:
            results (list[Any]): The results of the prediction.
        """
        results = []
        for image_path in image_paths:
            results.append(self.predict(image_path))
        self.logger.info(f"YOLO batch prediction results: {results}")
        return results
    
    def predict_and_export_bboxes(self, image_path: str):
        """
        Predict the bounding boxes of the image and export the results.
        Args:
            image_path (str): The path to the image.
        Returns:
            results (Any): The results of the prediction.
            sample_output (dict): {
                    "imagePath": image_path,
                    "originalWidth": original_width,
                    "originalHeight": original_height,
                    "boundingBoxes": bounding_boxes
            }   
        """
        results = self.predict(image_path)
        self.logger.info(f"YOLO single image prediction results: {results}")
        return export_bounding_boxes(self.model, image_path=image_path, results=results)
    
    def predict_and_export_bboxes_batch(self, image_paths: list[str]):
        """
        Predict the bounding boxes of the images and export the results.
        Args:
            image_paths (list[str]): The paths to the images.
        Returns:
            results (list[Any]): The results of the prediction.
            sample_output (list[dict]): The sample output of the prediction.
            [{
                "imagePath": image_path,
                "originalWidth": original_width,
                "originalHeight": original_height,
                "boundingBoxes": bounding_boxes
            }]
        """
        self.logger.info(f"YOLO batch prediction started for {len(image_paths)} images")
        results = []
        for image_path in image_paths:
            results.append(self.predict_and_export_bboxes(image_path))
        self.logger.info(f"YOLO batch prediction results: {results}")
        return results


# if __name__ == "__main__":
#     # 
#     import json
#     yolo_prediction = YOLOPrediction()
#     screenshot_events_json_path = "data/youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
    
#     with open(screenshot_events_json_path, "r") as f:
#         screenshot_events = json.load(f)
#     print(screenshot_events)
    
#     screenshot_paths = [event["screenshot_path"] for event in screenshot_events]
    
#     results = yolo_prediction.predict_and_export_bboxes_batch(screenshot_paths)
#     print(len(results))
#     print(results)