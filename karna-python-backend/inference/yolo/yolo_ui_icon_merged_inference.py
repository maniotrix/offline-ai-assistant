import logging
from typing import Dict, List
import json
import os
from datetime import datetime

# Replace relative imports with absolute imports
from inference import BoundingBoxResult
from inference.yolo.ui.yolo_prediction import YOLO_UI_Prediction
from inference.yolo.icon.yolo_prediction import YOLO_ICON_Prediction
from services.screen_capture_service import ScreenshotEvent


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
    
    @classmethod
    def get_ui_bboxes(cls, screenshot_paths: List[str]) -> List[BoundingBoxResult]:
        """
        Get UI bounding boxes from screenshot paths.
        
        Parameters:
            screenshot_paths (List[str]): List of screenshot paths.
            
        Returns:
            List[BoundingBoxResult]: List of UI bounding box results.
        """
        cls.logger.info("Initializing YOLO UI prediction model")
        ui_model = YOLO_UI_Prediction()
        
        cls.logger.info("Starting UI bounding box prediction")
        ui_bboxes_results = ui_model.predict_and_export_bboxes_batch(screenshot_paths)
        cls.logger.info(f"Completed UI bounding box prediction, found {len(ui_bboxes_results)} results")
        
        return ui_bboxes_results
    
    @classmethod
    def get_icon_bboxes(cls, screenshot_paths: List[str]) -> List[BoundingBoxResult]:
        """
        Get icon bounding boxes from screenshot paths.
        
        Parameters:
            screenshot_paths (List[str]): List of screenshot paths.
            
        Returns:
            List[BoundingBoxResult]: List of icon bounding box results.
        """
        cls.logger.info("Initializing YOLO Icon prediction model")
        icon_model = YOLO_ICON_Prediction()
        
        cls.logger.info("Starting Icon bounding box prediction")
        icon_bboxes_results = icon_model.predict_and_export_bboxes_batch(screenshot_paths)
        cls.logger.info(f"Completed Icon bounding box prediction, found {len(icon_bboxes_results)} results")
        
        return icon_bboxes_results
    
    @classmethod
    def get_merged_ui_icon_bboxes(cls, screenshot_events: List[ScreenshotEvent]) -> Dict[str, BoundingBoxResult]:
        """
        Get merged UI and icon bounding boxes from screenshot events.
        
        Parameters:
            screenshot_events (List[ScreenshotEvent]): List of screenshot events.

        Returns:
            Dict[str, BoundingBoxResult]: Dictionary mapping event IDs to their merged UI and icon bounding boxes.
        """
        cls.logger.info(f"Processing {len(screenshot_events)} screenshot events")
        
        # get the ui_bboxes and icon_bboxes from the screenshot paths
        screenshot_paths = [event.screenshot_path for event in screenshot_events]
        event_ids = [event.event_id for event in screenshot_events]
        cls.logger.info(f"Found {len(screenshot_paths)} screenshot paths")
        
        # Get UI and icon bounding boxes
        ui_bboxes_results = cls.get_ui_bboxes(screenshot_paths)
        icon_bboxes_results = cls.get_icon_bboxes(screenshot_paths)
        
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
    def get_merged_ui_icon_bboxes_from_json(cls, json_file_path: str) -> Dict[str, BoundingBoxResult]:
        """
        Load screenshot events from a JSON file and get merged UI and icon bounding boxes.
        
        Parameters:
            json_file_path (str): Path to the JSON file containing screenshot events.
            
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
        return cls.get_merged_ui_icon_bboxes(screenshot_events)