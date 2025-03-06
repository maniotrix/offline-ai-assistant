from base import SingletonMeta
from typing import List, Optional
import logging
from datetime import datetime
import os
import json
from PIL import Image
import uuid

from inference import VisionDetectResultModelList
from inference.yolo.yolo_ui_icon_merged_inference import Merged_UI_IconBBoxes
from services.screen_capture_service import ScreenshotEvent
from services.base_service import BaseService

# Create a logger for this service
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class VisionDetectService(BaseService[VisionDetectResultModelList], metaclass=SingletonMeta):
    """
    Service for processing screenshot events and storing VisionDetectResultModelList.
    This service uses the Merged_UI_IconBBoxes class to process screenshot events
    and generate VisionDetectResultModel objects.
    
    This service implements the observer pattern through BaseService[VisionDetectResultModelList],
    allowing observers to be notified when vision detection results change.
    """
    
    def __init__(self, screenshot_events: Optional[List[ScreenshotEvent]] = None):
        """
        Initialize the VisionDetectService.
        
        Args:
            screenshot_events: Optional list of screenshot events to process.
        """
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._screenshot_events: List[ScreenshotEvent] = screenshot_events or []
            self._vision_detect_results: Optional[VisionDetectResultModelList] = None
            self._initialized = True
            # Set initial state
            self.set_state('has_results', False)
            self.set_state('processing', False)
            logger.info("VisionDetectService instance created")
    
    async def initialize(self) -> None:
        """Initialize service resources"""
        try:
            logger.info("Initializing VisionDetectService...")
            # No specific initialization needed at this point
            logger.info("VisionDetectService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VisionDetectService: {str(e)}")
            raise
    
    async def shutdown(self) -> None:
        """Clean up service resources"""
        logger.info("Shutting down VisionDetectService...")
        # Clear any stored results to free memory
        self._vision_detect_results = None
        self.set_state('has_results', False)
        logger.info("VisionDetectService shutdown complete")
    
    def set_screenshot_events(self, screenshot_events: List[ScreenshotEvent]) -> None:
        """
        Set the list of screenshot events to process.
        
        Args:
            screenshot_events: List of screenshot events to process.
        """
        logger.info(f"Setting {len(screenshot_events)} screenshot events")
        self._screenshot_events = screenshot_events
        # Notify observers that the state has changed
        self.set_state('screenshot_events_count', len(screenshot_events))
    
    def add_screenshot_event(self, screenshot_event: ScreenshotEvent) -> None:
        """
        Add a screenshot event to the list of events to process.
        
        Args:
            screenshot_event: Screenshot event to add.
        """
        logger.info(f"Adding screenshot event: {screenshot_event.event_id}")
        self._screenshot_events.append(screenshot_event)
        # Notify observers that the state has changed
        self.set_state('screenshot_events_count', len(self._screenshot_events))
    
    def process_screenshot_events(self, should_crop: bool = True) -> VisionDetectResultModelList:
        """
        Process the screenshot events and generate VisionDetectResultModelList.
        
        Args:
            should_crop: Whether to crop the screenshots before processing.
            
        Returns:
            VisionDetectResultModelList: The processed vision detect results.
        """
        if not self._screenshot_events:
            logger.warning("No screenshot events to process")
            # Create an empty result list with default UUIDs
            project_uuid = str(uuid.uuid4())
            command_uuid = str(uuid.uuid4())
            self._vision_detect_results = VisionDetectResultModelList(
                project_uuid=project_uuid,
                command_uuid=command_uuid,
                vision_detect_result_models=[]
            )
            # Notify observers of the empty results
            self.set_state('has_results', True)
            self.set_state('results_count', 0)
            self.notify_observers(self._vision_detect_results)
            return self._vision_detect_results
        
        try:
            logger.info(f"Processing {len(self._screenshot_events)} screenshot events")
            # Set processing state to true
            self.set_state('processing', True)
            
            # Extract project_uuid and command_uuid from the first event if available
            project_uuid = self._screenshot_events[0].project_uuid if self._screenshot_events else str(uuid.uuid4())
            command_uuid = self._screenshot_events[0].command_uuid if self._screenshot_events else str(uuid.uuid4())
            
            # Use the Merged_UI_IconBBoxes class to process the screenshot events
            vision_detect_result_models = Merged_UI_IconBBoxes.get_inference_result_models_pil(
                self._screenshot_events,
                should_crop=should_crop
            )
            
            # Create a VisionDetectResultModelList from the result models
            self._vision_detect_results = VisionDetectResultModelList(
                project_uuid=project_uuid,
                command_uuid=command_uuid,
                vision_detect_result_models=vision_detect_result_models
            )
            
            logger.info(f"Processed {len(vision_detect_result_models)} screenshot events successfully")
            
            # Update state and notify observers
            self.set_state('processing', False)
            self.set_state('has_results', True)
            self.set_state('results_count', len(vision_detect_result_models))
            self.set_state('last_processed', datetime.now().isoformat())
            
            # Notify observers with the new results
            self.notify_observers(self._vision_detect_results)
            
            return self._vision_detect_results
        
        except Exception as e:
            logger.error(f"Error processing screenshot events: {str(e)}")
            # Update state to indicate processing failed
            self.set_state('processing', False)
            self.set_state('last_error', str(e))
            raise
    
    def get_vision_detect_results(self) -> Optional[VisionDetectResultModelList]:
        """
        Get the processed vision detect results.
        
        Returns:
            Optional[VisionDetectResultModelList]: The processed vision detect results, or None if not processed.
        """
        if not self._vision_detect_results:
            logger.warning("No vision detect results available. Call process_screenshot_events first.")
            return None
        
        return self._vision_detect_results
    
    def export_vision_detect_results_to_json(self, output_dir: str) -> Optional[str]:
        """
        Export the vision detect results to a JSON file.
        
        Args:
            output_dir: Directory to save the JSON file.
            
        Returns:
            Optional[str]: Path to the JSON file, or None if export failed.
        """
        if not self._vision_detect_results:
            logger.warning("No vision detect results available to export")
            return None
        
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"vision_detect_results_{timestamp}.json"
            json_path = os.path.join(output_dir, json_filename)
            
            # Convert the results to a dictionary
            results_dict = {
                "project_uuid": self._vision_detect_results.project_uuid,
                "command_uuid": self._vision_detect_results.command_uuid,
                "results": [model.to_dict() for model in self._vision_detect_results.vision_detect_result_models]
            }
            
            # Write the results to a JSON file
            with open(json_path, "w") as f:
                json.dump(results_dict, f, indent=2, default=lambda o: None if isinstance(o, Image.Image) else o)
            
            logger.info(f"Exported vision detect results to: {json_path}")
            
            # Update state to indicate export was successful
            self.set_state('last_export_path', json_path)
            self.set_state('last_export_time', datetime.now().isoformat())
            
            return json_path
        
        except Exception as e:
            logger.error(f"Error exporting vision detect results: {str(e)}")
            # Update state to indicate export failed
            self.set_state('last_export_error', str(e))
            return None
    
    def get_status(self) -> str:
        """
        Get the status of the service.
        
        Returns:
            str: The status of the service.
        """
        if not self._screenshot_events:
            return "No screenshot events set"
        
        if not self._vision_detect_results:
            return f"Ready to process {len(self._screenshot_events)} screenshot events"
        
        return f"Processed {len(self._vision_detect_results.vision_detect_result_models)} vision detect results"
    
    def clear_results(self) -> None:
        """
        Clear the vision detect results.
        """
        logger.info("Clearing vision detect results")
        self._vision_detect_results = None
        self.set_state('has_results', False)
        self.set_state('results_count', 0)
        # Notify observers that results have been cleared
        self.notify_observers(None)


def get_vision_detect_service_instance(screenshot_events: Optional[List[ScreenshotEvent]] = None):
    """
    Get the singleton instance of the VisionDetectService.
    
    Args:
        screenshot_events: Optional list of screenshot events to process.
        
    Returns:
        VisionDetectService: The singleton instance of the VisionDetectService.
    """
    return VisionDetectService(screenshot_events) 