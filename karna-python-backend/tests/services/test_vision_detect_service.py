import pytest
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import asyncio
import unittest
import shutil
import tempfile
import json
import copy

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.vision_detect_service import VisionDetectService, get_vision_detect_service_instance
from services.screen_capture_service import ScreenshotEvent
# Import directly from the modules where these classes are defined
from inference.__init__ import VisionDetectResultModelList, VisionDetectResultModel, BoundingBox
from base.base_observer import Observer, Priority, AsyncCapableObserver
from config.paths import workspace_data_dir, workspace_dir

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def screenshot_events_from_json() -> List[Dict[str, Any]]:
    """Load real screenshot events from a JSON file."""
    try:
        screenshot_events_json_path = workspace_data_dir / "youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
        with open(screenshot_events_json_path, "r") as f:
            events_data = json.load(f)
        return events_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load real screenshot events: {e}")
        pytest.skip(f"No screenshot events JSON file found: {e}")
        return []

@pytest.fixture
def screenshot_events(screenshot_events_from_json: List[Dict[str, Any]]) -> List[ScreenshotEvent]:
    """Convert JSON data to ScreenshotEvent objects with absolute paths."""
    events_copy = copy.deepcopy(screenshot_events_from_json)
    
    # Convert paths to absolute paths
    for event in events_copy:
        if "screenshot_path" in event:
            event["screenshot_path"] = str(workspace_dir / event["screenshot_path"])
        if "annotation_path" in event and event["annotation_path"]:
            event["annotation_path"] = str(workspace_dir / event["annotation_path"])
        
        # Ensure timestamp is a datetime object, not a string
        if "timestamp" in event and isinstance(event["timestamp"], str):
            event["timestamp"] = datetime.fromisoformat(event["timestamp"])
            
    # Convert to ScreenshotEvent objects
    return [ScreenshotEvent(**event) for event in events_copy]

def test_service_initialization():
    """Test that the service initializes correctly."""
    service = VisionDetectService()
    assert service is not None
    # The service status depends on whether screenshot events are set
    assert service.get_status() == "No screenshot events set"

def test_singleton_pattern():
    """Test that the service follows the singleton pattern."""
    service1 = get_vision_detect_service_instance()
    service2 = get_vision_detect_service_instance()
    assert service1 is service2

def test_process_screenshot_events(screenshot_events):
    """Test processing screenshot events with real screenshot files."""
    service = get_vision_detect_service_instance()
    service.set_screenshot_events(screenshot_events)
    
    # Process events directly without try/except to show full stacktrace
    result_list = service.process_screenshot_events()
    
    # Instead of checking type, check that it has the expected attributes/functionality
    assert hasattr(result_list, "project_uuid")
    assert hasattr(result_list, "command_uuid")
    assert hasattr(result_list, "vision_detect_result_models")
    assert len(result_list.vision_detect_result_models) == len(screenshot_events)
    
    # Check that each result has the expected structure
    for result in result_list.vision_detect_result_models:
        assert hasattr(result, "event_id")
        assert hasattr(result, "project_uuid")
        assert hasattr(result, "command_uuid")
        assert hasattr(result, "merged_ui_icon_bboxes")
        assert isinstance(result.merged_ui_icon_bboxes, list)

class TestObserver(Observer[VisionDetectResultModelList]):
    """Observer to track vision detection results."""
    def __init__(self):
        super().__init__(Priority.NORMAL)
        self.results: Optional[VisionDetectResultModelList] = None
        self.update_count = 0
    
    def update(self, data: Optional[VisionDetectResultModelList]) -> None:
        """Handle vision detection results updates.
        
        Args:
            data: Vision detection results to process
        """
        self.update_count += 1
        self.results = data

class TestVisionDetectService(unittest.TestCase):
    def setUp(self):
        # Load real screenshot events
        try:
            screenshot_events_json_path = workspace_data_dir / "youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
            with open(screenshot_events_json_path, "r") as f:
                events_data = json.load(f)
                
            # Convert paths to absolute paths
            for event in events_data:
                if "screenshot_path" in event:
                    event["screenshot_path"] = str(workspace_dir / event["screenshot_path"])
                if "annotation_path" in event and event["annotation_path"]:
                    event["annotation_path"] = str(workspace_dir / event["annotation_path"])
                    
            # Convert to ScreenshotEvent objects
            self.screenshot_events = [ScreenshotEvent(**event) for event in events_data]
            
            # Skip if no events
            if not self.screenshot_events:
                self.skipTest("No screenshot events available")
                
            # Initialize service and observer
            self.service = get_vision_detect_service_instance()
            self.observer = TestObserver()
            self.service.add_observer(self.observer)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.skipTest(f"Could not load real screenshot events: {e}")

    def tearDown(self):
        # Clear service state
        if hasattr(self, 'service') and hasattr(self, 'observer'):
            self.service._screenshot_events = []
            self.service._vision_detect_results = None
            self.service.remove_observer(self.observer)

    def test_observer_pattern(self):
        """Test that observers are notified when vision detection results change."""
        # Skip if no events
        if not hasattr(self, 'screenshot_events') or not self.screenshot_events:
            self.skipTest("No screenshot events available")
            
        # Initial state
        self.assertEqual(self.observer.update_count, 0)
        self.assertIsNone(self.observer.results)
        
        # Add screenshot events
        self.service.set_screenshot_events(self.screenshot_events[:1])  # Use just first event for speed
        
        # Process the screenshot events without try/except to show full stacktrace
        results = self.service.process_screenshot_events()
        
        # Check that the observer was notified
        self.assertEqual(self.observer.update_count, 2)
        self.assertIsNotNone(self.observer.results)
        self.assertEqual(self.observer.results, results)
        
        # Clear the results
        self.service.clear_results()

@pytest.mark.asyncio
async def test_async_observer(screenshot_events):
    """Test that async observers are notified when vision detection results change."""
    if not screenshot_events:
        pytest.skip("No screenshot events available")
        
    # Create the service
    service = get_vision_detect_service_instance()
    
    # Create an async observer
    update_count = 0
    results = None
    
    async def handle_update(data: Optional[VisionDetectResultModelList]) -> None:
        nonlocal update_count, results
        update_count += 1
        results = data
    
    # Set up the main event loop for the AsyncCapableObserver
    AsyncCapableObserver.set_main_loop(asyncio.get_event_loop())
    
    # Create and add the observer
    async_observer = AsyncCapableObserver[VisionDetectResultModelList](handle_update)
    service.add_observer(async_observer)
    
    try:
        # Add screenshot events
        service.set_screenshot_events(screenshot_events[:1])  # type: ignore # Use just first event for speed
        
        # Process the screenshot events without try/except to show full stacktrace
        service.process_screenshot_events()
        
        # Give the async observer time to process the update
        await asyncio.sleep(0.1)
        
        # Check that the observer was notified
        assert update_count == 2
        assert results is not None
        
        # Clear the results
        service.clear_results()
    
    finally:
        # Clean up
        service.remove_observer(async_observer)
        
        # Clear service state
        service._screenshot_events = []
        service._vision_detect_results = None

if __name__ == "__main__":
    # This allows running the tests directly with python\
    # python -m pytest tests/services/test_vision_detect_service.py -v
    pytest.main(["-xvs", __file__])
    unittest.main() 