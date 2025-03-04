import json
import pytest
from inference.yolo.ui.yolo_prediction import YOLOPrediction
from config.paths import workspace_data_dir, workspace_dir


@pytest.fixture
def yolo_prediction():
    return YOLOPrediction()

@pytest.fixture
def screenshot_events():
    screenshot_events_json_path = workspace_data_dir / "youtube.com/123e4567-e89b-12d3-a456-426614174000/screenshot_events_123e4567-e89b-12d3-a456-426614174000.json"
    with open(screenshot_events_json_path, "r") as f:
        return json.load(f)

@pytest.fixture
def screenshot_paths(screenshot_events):
    return [event["screenshot_path"] for event in screenshot_events] # type: ignore

def test_predict_and_export_bboxes_batch(yolo_prediction, screenshot_paths):
    # convert screenshot_paths to proper paths using paths config
    screenshot_paths = [workspace_dir / path for path in screenshot_paths]
    
    results = yolo_prediction.predict_and_export_bboxes_batch(screenshot_paths)
    assert len(results) > 0
    assert isinstance(results, list)