import os
import json
import logging
from typing import List
from datetime import datetime
from services.screen_capture_service import ScreenshotEvent

logger = logging.getLogger(__name__)

# Define a simple exception for the utility function
class ScreenCaptureUtilError(Exception):
    """Base exception for screen capture utility errors"""
    pass

def load_screenshot_events_from_cache(project_uuid: str, command_uuid: str) -> List[ScreenshotEvent]:
    """Load screenshot events from the workspace data directory cache.
    
    This is a standalone utility function that loads screenshot events from a JSON file
    in the data directory without requiring a screen capture session or service.
    
    Args:
        project_uuid: Project identifier
        command_uuid: Command identifier
        
    Returns:
        List[ScreenshotEvent]: List of screenshot events loaded from cache
        
    Raises:
        ScreenCaptureUtilError: If directory or file not found, or if JSON is invalid
    """
    try:
        base_dir = os.path.join('data', project_uuid, command_uuid)
        if not os.path.exists(base_dir):
            raise ScreenCaptureUtilError(f"Directory not found for project {project_uuid}, command {command_uuid}")
        
        json_path = os.path.join(base_dir, f'screenshot_events_{command_uuid}.json')
        
        # Check if JSON file exists
        if not os.path.exists(json_path):
            raise ScreenCaptureUtilError(f"Screenshot events file not found: {json_path}")
        
        # Load events from JSON file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ScreenCaptureUtilError(f"Invalid JSON in screenshot events file: {str(e)}")
        
        # Convert JSON data back to ScreenshotEvent objects
        screenshot_events = []
        for event_dict in events_data:
            # Convert ISO format string back to datetime
            if 'timestamp' in event_dict:
                event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp'])
            
            # Create ScreenshotEvent object
            try:
                event = ScreenshotEvent(**event_dict)
                screenshot_events.append(event)
            except (TypeError, ValueError) as e:
                logger.warning(f"Skipping invalid event: {str(e)}")
        
        logger.info(f"Loaded {len(screenshot_events)} screenshot events from cache for {project_uuid}/{command_uuid}")
        return screenshot_events
        
    except ScreenCaptureUtilError:
        # Re-raise specific errors
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading screenshot events from cache: {str(e)}")
        raise ScreenCaptureUtilError(f"Screenshot events loading failed: {str(e)}")
