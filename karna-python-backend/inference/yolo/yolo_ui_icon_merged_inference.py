import logging
from typing import Dict, List
import json
import os
from datetime import datetime

import cv2
import numpy as np
from PIL import Image

# Replace relative imports with absolute imports
from inference import BoundingBoxResult, VisionDetectResultModel
from inference.yolo.ui.yolo_prediction import YOLO_UI_Prediction
from inference.yolo.icon.yolo_prediction import YOLO_ICON_Prediction
from services.screen_capture_service import ScreenshotEvent
from utils.image_utils import crop_to_render_area

class Merged_UI_IconBBoxes:
    """
    Class for merging UI and icon bounding boxes.
    """
    # Class-level logger
    logger = logging.getLogger("Merged_UI_IconBBoxes")
    
    @staticmethod
    def merge_icon_ui_bboxes(icon_bboxes: BoundingBoxResult, ui_bboxes: BoundingBoxResult) -> BoundingBoxResult:
        """
        Merge icon and UI bounding boxes.
        
        Parameters:
            icon_bboxes (BoundingBoxResult): Icon bounding boxes.
            ui_bboxes (BoundingBoxResult): UI bounding boxes.

        Returns:
            BoundingBoxResult: Merged bounding boxes.
        """
        # check if icon_bboxes and ui_bboxes have the same imagePath
        if icon_bboxes.image_path != ui_bboxes.image_path:
            raise ValueError("icon_bboxes and ui_bboxes have different image paths")
        
        # check if icon_bboxes and ui_bboxes have the same originalWidth and originalHeight
        if icon_bboxes.original_width != ui_bboxes.original_width or icon_bboxes.original_height != ui_bboxes.original_height:
            raise ValueError("icon_bboxes and ui_bboxes have different originalWidth or originalHeight")
        
        # merge the bounding boxes
        merged_bboxes = icon_bboxes.bounding_boxes + ui_bboxes.bounding_boxes
        
        return BoundingBoxResult(
            image_path=icon_bboxes.image_path,
            original_width=icon_bboxes.original_width,
            original_height=icon_bboxes.original_height,
            bounding_boxes=merged_bboxes
        )
    
    @staticmethod
    def path_to_pil_image(image_path: str, should_crop: bool = True) -> Image.Image:
        """
        Convert an image path to a PIL Image.
        
        Parameters:
            image_path (str): Path to the image.
            should_crop (bool): Whether to crop the image to the website render area. Default is True.
            
        Returns:
            Image.Image: PIL Image object.
            
        Raises:
            FileNotFoundError: If the image file does not exist.
            ValueError: If the image cannot be opened.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Use the crop_to_render_area function to get the image
            return crop_to_render_area(image_path, should_crop=should_crop)
        except Exception as e:
            raise ValueError(f"Failed to open image: {str(e)}")
    
    @classmethod
    def paths_to_pil_images(cls, image_paths: List[str], should_crop: bool = True) -> List[Image.Image]:
        """
        Convert a list of image paths to PIL Images.
        
        Parameters:
            image_paths (List[str]): List of image paths.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
            
        Returns:
            List[Image.Image]: List of PIL Image objects.
        """
        cls.logger.info(f"Converting {len(image_paths)} image paths to PIL Images")
        pil_images = []
        
        for image_path in image_paths:
            try:
                pil_image = cls.path_to_pil_image(image_path, should_crop=should_crop)
                pil_images.append(pil_image)
            except (FileNotFoundError, ValueError) as e:
                cls.logger.warning(f"Skipping image {image_path}: {str(e)}")
        
        cls.logger.info(f"Successfully converted {len(pil_images)} images to PIL format")
        return pil_images
    
    @classmethod
    def get_ui_bboxes(cls, screenshot_paths: List[str], should_crop: bool = True) -> List[BoundingBoxResult]:
        """
        Get UI bounding boxes from screenshot paths.
        
        Parameters:
            screenshot_paths (List[str]): List of screenshot paths.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
            
        Returns:
            List[BoundingBoxResult]: List of UI bounding box results.
        """
        cls.logger.info("Initializing YOLO UI prediction model")
        ui_model = YOLO_UI_Prediction()
        
        # If cropping is enabled, first crop the images and then predict
        if should_crop:
            cls.logger.info("Cropping images to website render area before UI prediction")
            pil_images = cls.paths_to_pil_images(screenshot_paths, should_crop=True)
            return cls.get_ui_bboxes_pil(pil_images, screenshot_paths)
        
        cls.logger.info("Starting UI bounding box prediction without cropping")
        ui_bboxes_results = ui_model.predict_and_export_bboxes_batch(screenshot_paths)
        cls.logger.info(f"Completed UI bounding box prediction, found {len(ui_bboxes_results)} results")
        
        return ui_bboxes_results
    
    @classmethod
    def get_ui_bboxes_pil(cls, pil_images: List[Image.Image], original_paths: List[str]) -> List[BoundingBoxResult]:
        """
        Get UI bounding boxes from PIL images.
        
        Parameters:
            pil_images (List[Image.Image]): List of PIL images.
            original_paths (List[str]): List of original image paths for reference.
            
        Returns:
            List[BoundingBoxResult]: List of UI bounding box results.
        """
        cls.logger.info("Initializing YOLO UI prediction model for PIL images")
        ui_model = YOLO_UI_Prediction()
        
        cls.logger.info("Starting UI bounding box prediction with PIL images")
        ui_bboxes_results = []
        
        for pil_image, original_path in zip(pil_images, original_paths):
            result = ui_model.predict_and_export_bboxes_pil(pil_image)
            # Update the image path to the original path
            result.image_path = original_path
            ui_bboxes_results.append(result)
        
        cls.logger.info(f"Completed UI bounding box prediction with PIL images, found {len(ui_bboxes_results)} results")
        
        return ui_bboxes_results
    
    @classmethod
    def get_icon_bboxes(cls, screenshot_paths: List[str], should_crop: bool = True) -> List[BoundingBoxResult]:
        """
        Get icon bounding boxes from screenshot paths.
        
        Parameters:
            screenshot_paths (List[str]): List of screenshot paths.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
            
        Returns:
            List[BoundingBoxResult]: List of icon bounding box results.
        """
        cls.logger.info("Initializing YOLO Icon prediction model")
        icon_model = YOLO_ICON_Prediction()
        
        # If cropping is enabled, first crop the images and then predict
        if should_crop:
            cls.logger.info("Cropping images to website render area before Icon prediction")
            pil_images = cls.paths_to_pil_images(screenshot_paths, should_crop=True)
            return cls.get_icon_bboxes_pil(pil_images, screenshot_paths)
        
        cls.logger.info("Starting Icon bounding box prediction without cropping")
        icon_bboxes_results = icon_model.predict_and_export_bboxes_batch(screenshot_paths)
        cls.logger.info(f"Completed Icon bounding box prediction, found {len(icon_bboxes_results)} results")
        
        return icon_bboxes_results
    
    @classmethod
    def get_icon_bboxes_pil(cls, pil_images: List[Image.Image], original_paths: List[str]) -> List[BoundingBoxResult]:
        """
        Get icon bounding boxes from PIL images.
        
        Parameters:
            pil_images (List[Image.Image]): List of PIL images.
            original_paths (List[str]): List of original image paths for reference.
            
        Returns:
            List[BoundingBoxResult]: List of icon bounding box results.
        """
        cls.logger.info("Initializing YOLO Icon prediction model for PIL images")
        icon_model = YOLO_ICON_Prediction()
        
        cls.logger.info("Starting Icon bounding box prediction with PIL images")
        icon_bboxes_results = []
        
        for pil_image, original_path in zip(pil_images, original_paths):
            result = icon_model.predict_and_export_bboxes_pil(pil_image)
            # Update the image path to the original path
            result.image_path = original_path
            icon_bboxes_results.append(result)
        
        cls.logger.info(f"Completed Icon bounding box prediction with PIL images, found {len(icon_bboxes_results)} results")
        
        return icon_bboxes_results
    
    @classmethod
    def get_merged_ui_icon_bboxes_for_paths(cls, screenshot_paths: List[str], should_crop: bool = True) -> Dict[str, BoundingBoxResult]:
        """
        Get merged UI and icon bounding boxes from screenshot paths.
        """
        cls.logger.info(f"Processing {len(screenshot_paths)} screenshot paths")
        # get the ui_bboxes and icon_bboxes from the screenshot paths
        cls.logger.info(f"Found {len(screenshot_paths)} screenshot paths")
        
        # Get UI and icon bounding boxes
        ui_bboxes_results = cls.get_ui_bboxes(screenshot_paths, should_crop=should_crop)
        icon_bboxes_results = cls.get_icon_bboxes(screenshot_paths, should_crop=should_crop)
        
        # Merge the UI and icon bounding boxes
        cls.logger.info("Merging UI and Icon bounding boxes")
        merged_results = {}
        for ui_result, icon_result in zip(ui_bboxes_results, icon_bboxes_results):
            merged_results[ui_result.image_path] = cls.merge_icon_ui_bboxes(icon_result, ui_result)
        
        cls.logger.info(f"Completed merging, returning {len(merged_results)} merged bounding box results")
        # show the merged results as dict in compact format as truncating the bounding boxes
        cls.logger.info(f"Merged results: {merged_results}")
        
        return merged_results
        
        
    @classmethod
    def get_merged_ui_icon_bboxes(cls, screenshot_events: List[ScreenshotEvent], should_crop: bool = True) -> Dict[str, BoundingBoxResult]:
        """
        Get merged UI and icon bounding boxes from screenshot events.
        
        Parameters:
            screenshot_events (List[ScreenshotEvent]): List of screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.

        Returns:
            Dict[str, BoundingBoxResult]: Dictionary mapping event IDs to their merged UI and icon bounding boxes.
        """
        cls.logger.info(f"Processing {len(screenshot_events)} screenshot events")
        
        # get the ui_bboxes and icon_bboxes from the screenshot paths
        screenshot_paths = [event.screenshot_path for event in screenshot_events]
        event_ids = [event.event_id for event in screenshot_events]
        cls.logger.info(f"Found {len(screenshot_paths)} screenshot paths")
        
        # Get UI and icon bounding boxes
        ui_bboxes_results = cls.get_ui_bboxes(screenshot_paths, should_crop=should_crop)
        icon_bboxes_results = cls.get_icon_bboxes(screenshot_paths, should_crop=should_crop)
        
        # Merge the UI and icon bounding boxes
        cls.logger.info("Merging UI and Icon bounding boxes")
        merged_results = {}
        for event_id, ui_result, icon_result in zip(event_ids, ui_bboxes_results, icon_bboxes_results):
            merged_results[event_id] = cls.merge_icon_ui_bboxes(icon_result, ui_result)
        
        cls.logger.info(f"Completed merging, returning {len(merged_results)} merged bounding box results")
        # show the merged results as dict in compact format as truncating the bounding boxes
        cls.logger.info(f"Merged results: {merged_results}")
        
        return merged_results
    
    @classmethod
    def get_merged_ui_icon_bboxes_pil(cls, screenshot_events: List[ScreenshotEvent], should_crop: bool = True) -> Dict[str, BoundingBoxResult]:
        """
        Get merged UI and icon bounding boxes from screenshot events using PIL images.
        
        Parameters:
            screenshot_events (List[ScreenshotEvent]): List of screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.

        Returns:
            Dict[str, BoundingBoxResult]: Dictionary mapping event IDs to their merged UI and icon bounding boxes.
        """
        cls.logger.info(f"Processing {len(screenshot_events)} screenshot events with PIL images")
        
        # Get the screenshot paths and event IDs
        screenshot_paths = [event.screenshot_path for event in screenshot_events]
        event_ids = [event.event_id for event in screenshot_events]
        cls.logger.info(f"Found {len(screenshot_paths)} screenshot paths")
        
        # Convert paths to PIL images
        pil_images = cls.paths_to_pil_images(screenshot_paths, should_crop=should_crop)
        
        # Get UI and icon bounding boxes using PIL images
        ui_bboxes_results = cls.get_ui_bboxes_pil(pil_images, screenshot_paths)
        
        # We need to create new PIL images because the previous ones might be modified by the UI prediction
        pil_images = cls.paths_to_pil_images(screenshot_paths, should_crop=should_crop)
        icon_bboxes_results = cls.get_icon_bboxes_pil(pil_images, screenshot_paths)
        
        # Merge the UI and icon bounding boxes
        cls.logger.info("Merging UI and Icon bounding boxes from PIL images")
        merged_results = {}
        for event_id, ui_result, icon_result in zip(event_ids, ui_bboxes_results, icon_bboxes_results):
            merged_results[event_id] = cls.merge_icon_ui_bboxes(icon_result, ui_result)
        
        cls.logger.info(f"Completed merging with PIL images, returning {len(merged_results)} merged bounding box results")
        
        return merged_results
        
    @classmethod
    def get_merged_ui_icon_bboxes_from_json(cls, json_file_path: str, should_crop: bool = True) -> Dict[str, BoundingBoxResult]:
        """
        Load screenshot events from a JSON file and get merged UI and icon bounding boxes.
        
        Parameters:
            json_file_path (str): Path to the JSON file containing screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
            
        Returns:
            Dict[str, BoundingBoxResult]: Dictionary mapping event IDs to their merged UI and icon bounding boxes.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            ValueError: If the JSON file is invalid or does not contain screenshot events.
        """
        cls.logger.info(f"Loading screenshot events from JSON file: {json_file_path}")
        
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file: {str(e)}")
        
        if not events_data or not isinstance(events_data, list):
            raise ValueError("JSON file does not contain a list of screenshot events")
        
        # Convert JSON data to ScreenshotEvent objects
        screenshot_events = []
        for event_dict in events_data:
            # Convert ISO format string back to datetime
            if 'timestamp' in event_dict:
                event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
            
            # Create ScreenshotEvent object
            try:
                event = ScreenshotEvent(**event_dict)
                screenshot_events.append(event)
            except (TypeError, ValueError) as e:
                cls.logger.warning(f"Skipping invalid event: {str(e)}")
        
        cls.logger.info(f"Loaded {len(screenshot_events)} screenshot events from JSON file")
        
        # Get merged bounding boxes using the existing method
        return cls.get_merged_ui_icon_bboxes(screenshot_events, should_crop=should_crop)
    
    @classmethod
    def get_merged_ui_icon_bboxes_from_json_pil(cls, json_file_path: str, should_crop: bool = True) -> Dict[str, BoundingBoxResult]:
        """
        Load screenshot events from a JSON file and get merged UI and icon bounding boxes using PIL images.
        
        Parameters:
            json_file_path (str): Path to the JSON file containing screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
            
        Returns:
            Dict[str, BoundingBoxResult]: Dictionary mapping event IDs to their merged UI and icon bounding boxes.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            ValueError: If the JSON file is invalid or does not contain screenshot events.
        """
        cls.logger.info(f"Loading screenshot events from JSON file for PIL processing: {json_file_path}")
        
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file: {str(e)}")
        
        if not events_data or not isinstance(events_data, list):
            raise ValueError("JSON file does not contain a list of screenshot events")
        
        # Convert JSON data to ScreenshotEvent objects
        screenshot_events = []
        for event_dict in events_data:
            # Convert ISO format string back to datetime
            if 'timestamp' in event_dict:
                event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
            
            # Create ScreenshotEvent object
            try:
                event = ScreenshotEvent(**event_dict)
                screenshot_events.append(event)
            except (TypeError, ValueError) as e:
                cls.logger.warning(f"Skipping invalid event: {str(e)}")
        
        cls.logger.info(f"Loaded {len(screenshot_events)} screenshot events from JSON file for PIL processing")
        
        # Get merged bounding boxes using the PIL method
        return cls.get_merged_ui_icon_bboxes_pil(screenshot_events, should_crop=should_crop)
    
    @classmethod
    def visualise_merged_ui_icon_bboxes(cls, screenshot_events: List[ScreenshotEvent], should_crop: bool = True):
        """
        Visualise merged UI and icon bounding boxes.
        
        Parameters:
            screenshot_events (List[ScreenshotEvent]): List of screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
        """
        merged_results = cls.get_merged_ui_icon_bboxes(screenshot_events, should_crop=should_crop)
        for event_id, merged_result in merged_results.items():
            cls.logger.info(f"Visualising merged bounding boxes for event ID: {event_id}")
            cls.visualise_merged_bboxes(merged_result, merged_result.image_path, should_crop=should_crop)
    
    @classmethod
    def visualise_merged_ui_icon_bboxes_pil(cls, screenshot_events: List[ScreenshotEvent], should_crop: bool = True):
        """
        Visualise merged UI and icon bounding boxes using PIL images.
        
        Parameters:
            screenshot_events (List[ScreenshotEvent]): List of screenshot events.
            should_crop (bool): Whether to crop the images to the website render area. Default is True.
        """
        merged_results = cls.get_merged_ui_icon_bboxes_pil(screenshot_events, should_crop=should_crop)
        for event_id, merged_result in merged_results.items():
            cls.logger.info(f"Visualising merged bounding boxes from PIL images for event ID: {event_id}")
            cls.visualise_merged_bboxes(merged_result, merged_result.image_path, should_crop=should_crop)
            
    @classmethod
    def visualise_merged_bboxes_for_paths(cls, image_paths: List[str]   , should_crop: bool = True):
        """
        Visualise merged bounding boxes for a list of screenshot paths.
        """
        merged_results = cls.get_merged_ui_icon_bboxes_for_paths(image_paths, should_crop=should_crop)
        for image_path, merged_result in merged_results.items():
            cls.visualise_merged_bboxes(merged_result, image_path, should_crop=should_crop)

    @classmethod
    def visualise_merged_bboxes(cls, merged_result: BoundingBoxResult, image_path: str, should_crop: bool = True):
        """
        Visualise merged bounding boxes with different colors for different classes.
        
        Parameters:
            merged_result (BoundingBoxResult): Merged bounding box result.
            image_path (str): Path to the image.
            should_crop (bool): Whether to crop the image to the website render area. Default is True.
        """
        cls.logger.info(f"Visualising merged bounding boxes for image: {image_path}")
        
        # Use OpenCV to visualize the merged bounding boxes on the image
        if should_crop:
            # If cropping is enabled, first load the image as PIL and crop it
            pil_image = cls.path_to_pil_image(image_path, should_crop=True)
            # Convert PIL image to OpenCV format
            image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        else:
            # If cropping is disabled, load the image directly with OpenCV
            image = cv2.imread(image_path)
        
        # Create a color mapping for different classes
        # Extract unique class names from the bounding boxes
        unique_classes = set(bbox.class_name for bbox in merged_result.bounding_boxes)
        
        # Generate a color map for each unique class
        color_map = {}
        for i, class_name in enumerate(unique_classes):
            # Generate distinct colors using HSV color space and convert to BGR
            hue = int(255 * i / max(1, len(unique_classes)))
            color = cv2.cvtColor(np.array([[[hue, 255, 255]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
            # Convert to tuple of integers for OpenCV
            color_map[class_name] = (int(color[0]), int(color[1]), int(color[2]))
        
        # Draw bounding boxes with class-specific colors
        for bbox in merged_result.bounding_boxes:
            # Get color for this class (default to red if not found)
            color = color_map.get(bbox.class_name, (0, 0, 255))
            
            # Draw rectangle with class-specific color
            image = cv2.rectangle(image, (bbox.x, bbox.y), (bbox.x + bbox.width, bbox.y + bbox.height), color, 2)
            
            # Add bbox class name and confidence score with the same color
            cv2.putText(image, f"{bbox.class_name} {bbox.confidence:.2f}", 
                       (bbox.x, bbox.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Add a legend to show class-color mapping
        legend_y = 30
        for class_name, color in color_map.items():
            cv2.putText(image, class_name, (10, legend_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            legend_y += 20
            
        cv2.imshow("Merged Bounding Boxes", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @classmethod
    def get_inference_result_models_pil(cls, screenshot_events: List[ScreenshotEvent], should_crop: bool = True) -> List[VisionDetectResultModel]:
        """
        Get inference result models from screenshot events.
        """
        # get the pil images
        screenshot_paths = [event.screenshot_path for event in screenshot_events]
        pil_images = cls.paths_to_pil_images(screenshot_paths, should_crop=should_crop)
        merged_results = cls.get_merged_ui_icon_bboxes_pil(screenshot_events, should_crop=should_crop)
        vision_detect_result_models = []
        
        # Create VisionDetectResultModel for each screenshot event
        for event, pil_image in zip(screenshot_events, pil_images):
            event_id = event.event_id
            
            # Skip if no merged results for this event
            if event_id not in merged_results:
                cls.logger.warning(f"No merged results found for event {event_id}, skipping")
                continue
                
            merged_result = merged_results[event_id]
            
            # Get original image dimensions from the original image file
            try:
                with Image.open(event.screenshot_path) as original_img:
                    original_width, original_height = original_img.size
            except (FileNotFoundError, IOError) as e:
                cls.logger.warning(f"Could not open original image {event.screenshot_path}: {str(e)}")
                # Fallback to using the cropped image dimensions
                original_width, original_height = pil_image.size
            
            # Create VisionDetectResultModel
            vision_detect_result_model = VisionDetectResultModel(
                event_id=event_id,
                project_uuid=event.project_uuid,
                command_uuid=event.command_uuid,
                timestamp=event.timestamp,
                description=event.description,
                original_image_path=event.screenshot_path,
                original_width=original_width,
                original_height=original_height,
                is_cropped=should_crop,
                cropped_image=pil_image,
                cropped_width=pil_image.width,
                cropped_height=pil_image.height,
                merged_ui_icon_bboxes=merged_result.bounding_boxes
            )
            
            vision_detect_result_models.append(vision_detect_result_model)
            
        cls.logger.info(f"Created {len(vision_detect_result_models)} VisionDetectResultModel objects")
        return vision_detect_result_models