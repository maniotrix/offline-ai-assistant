import json
import pytest
import logging
from inference.yolo.ui.yolo_prediction import YOLO_UI_Prediction
from inference.yolo.icon.yolo_prediction import YOLO_ICON_Prediction
from inference.yolo.yolo_ui_icon_merged_inference import Merged_UI_IconBBoxes
from config.paths import workspace_data_dir, workspace_dir


@pytest.fixture
def yolo_ui_prediction():
    return YOLO_UI_Prediction()

@pytest.fixture
def yolo_icon_prediction():
    return YOLO_ICON_Prediction()

@pytest.fixture
def screenshot_events():
    screenshot_events_json_path = workspace_data_dir / "youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
    with open(screenshot_events_json_path, "r") as f:
        return json.load(f)

@pytest.fixture
def screenshot_paths(screenshot_events):
    screenshot_paths = [event["screenshot_path"] for event in screenshot_events] # type: ignore
    # convert screenshot_paths to proper paths using paths config
    screenshot_paths = [workspace_dir / path for path in screenshot_paths]
    return screenshot_paths


def test_predict_and_export_ui_bboxes_batch(yolo_ui_prediction, screenshot_paths):    
    results = yolo_ui_prediction.predict_and_export_bboxes_batch(screenshot_paths)
    assert len(results) > 0
    assert isinstance(results, list)

def test_predict_and_export_icon_bboxes_batch(yolo_icon_prediction, screenshot_paths):    
    results = yolo_icon_prediction.predict_and_export_bboxes_batch(screenshot_paths)
    assert len(results) > 0
    assert isinstance(results, list)

def test_merged_ui_icon_predictions(yolo_ui_prediction, yolo_icon_prediction, screenshot_paths):
    # Set up logging for this test
    logger = logging.getLogger("test_merged_ui_icon_predictions")
    logger.setLevel(logging.INFO)
    
    # Convert screenshot_paths to proper paths using paths config
    logger.info(f"Converting {len(screenshot_paths)} screenshot paths to absolute paths")
    
    # Get UI predictions
    logger.info("Getting UI predictions")
    ui_results = yolo_ui_prediction.predict_and_export_bboxes_batch(screenshot_paths)
    logger.info(f"Got {len(ui_results)} UI prediction results")
    
    # Get icon predictions
    logger.info("Getting icon predictions")
    icon_results = yolo_icon_prediction.predict_and_export_bboxes_batch(screenshot_paths)
    logger.info(f"Got {len(icon_results)} icon prediction results")
    
    # Merge predictions
    logger.info("Merging UI and icon predictions")
    merged_results = []
    for ui_result, icon_result in zip(ui_results, icon_results):
        merged_result = Merged_UI_IconBBoxes.merge_icon_ui_bboxes(icon_result, ui_result)
        merged_results.append(merged_result)
    
    # Validate results
    logger.info(f"Validating {len(merged_results)} merged results")
    assert len(merged_results) > 0
    assert isinstance(merged_results, list)
    
    # Check that each merged result has more bounding boxes than either UI or icon results alone
    for i, (merged, ui, icon) in enumerate(zip(merged_results, ui_results, icon_results)):
        logger.info(f"Result {i}: UI: {len(ui.bounding_boxes)} boxes, Icon: {len(icon.bounding_boxes)} boxes, Merged: {len(merged.bounding_boxes)} boxes")
        assert len(merged.bounding_boxes) == len(ui.bounding_boxes) + len(icon.bounding_boxes)

def test_merged_ui_icon_predictions_from_json(screenshot_events):
    # Set up logging for this test
    logger = logging.getLogger("test_merged_ui_icon_predictions_from_json")
    logger.setLevel(logging.INFO)
    
    # Create a temporary JSON file with screenshot events
    import tempfile
    import os
    import copy
    
    logger.info("Creating temporary JSON file with screenshot events")
    temp_dir = tempfile.gettempdir()
    json_file_path = os.path.join(temp_dir, "test_screenshot_events.json")
    
    # Make a deep copy of screenshot events to avoid modifying the original
    events_copy = copy.deepcopy(screenshot_events)
    
    # Convert screenshot_paths to proper paths using paths config
    logger.info("Converting screenshot paths to proper paths")
    for event in events_copy:
        if "screenshot_path" in event:
            # Convert relative path to absolute path
            event["screenshot_path"] = str(workspace_dir / event["screenshot_path"]) # type: ignore
        if "annotation_path" in event and event["annotation_path"]: # type: ignore
            # Convert relative path to absolute path
            event["annotation_path"] = str(workspace_dir / event["annotation_path"]) # type: ignore
    
    with open(json_file_path, "w") as f:
        json.dump(events_copy, f)
    
    logger.info(f"Temporary JSON file created at: {json_file_path}")
    
    try:
        # Get merged predictions from JSON file
        logger.info("Getting merged predictions from JSON file")
        merged_results = Merged_UI_IconBBoxes.get_merged_ui_icon_bboxes_from_json(json_file_path)
        
        # Validate results
        logger.info(f"Validating {len(merged_results)} merged results")
        assert len(merged_results) > 0
        assert isinstance(merged_results, dict)
        
        # Check that each result has the expected structure
        for event_id, result in merged_results.items():
            logger.info(f"Checking result for event {event_id}")
            assert hasattr(result, "image_path")
            assert hasattr(result, "original_width")
            assert hasattr(result, "original_height")
            assert hasattr(result, "bounding_boxes")
            assert len(result.bounding_boxes) > 0
    
    finally:
        # Clean up the temporary file
        logger.info("Cleaning up temporary JSON file")
        if os.path.exists(json_file_path):
            os.remove(json_file_path)

