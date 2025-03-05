"""
This class loads the system bounding boxes from the json file 
and provides a method to get the bounding boxes for the system, chrome and task bar.
"""

import json
import os
from enum import Enum
import pyautogui
# base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# json file path
JSON_FILE_PATH = os.path.join(BASE_PATH, "chrome_system_bounding_boxes.json")

class BoundingBoxType(Enum):
    SYSTEM = "system"
    CHROME = "chrome"
    TASK_BAR = "task_bar"
    WEBSITE_RENDER = "website_render"

class AbstractBoundingBox:
    def __init__(self, type, x, y, width, height):
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class BBoxFactory:
    """
    This class is used to create a factory for the bounding boxes.
    """
    def __init__(self):
        self.bboxes : dict[BoundingBoxType, AbstractBoundingBox] = {}
        self.load_bboxes()

    def get_bbox(self, type : BoundingBoxType) -> AbstractBoundingBox:
        return self.bboxes[type]
    
    def get_system_bbox(self) -> AbstractBoundingBox:
        return self.bboxes[BoundingBoxType.SYSTEM]

    def get_chrome_bbox(self) -> AbstractBoundingBox:
        return self.bboxes[BoundingBoxType.CHROME]

    def get_task_bar_bbox(self) -> AbstractBoundingBox:
        return self.bboxes[BoundingBoxType.TASK_BAR]
    
    def get_website_render_bbox(self) -> AbstractBoundingBox:
        return self.bboxes[BoundingBoxType.WEBSITE_RENDER]
    
    
    def load_bboxes(self):
        """
        This method loads the bounding boxes from the json file.
        The json file is expected to be in the following format:
        {
            "taskbarBBox": {
                "x": 0,
                "y": 1040,
                "width": 1920,
                "height": 40
            },
            "chromeBBox": {
                "x": 0,
                "y": 0,
                "width": 1920,
                "height": 1040
            },
            "renderBBox": {
                "x": 0,
                "y": 121,
                "width": 1920,
                "height": 919
            }
        }
        
        The system bbox is calculated as the sum of the chrome and task bar bboxes.
        Also verifies system dimensions with pyautogui.
        """
        # Get system screen size using pyautogui
        system_width, system_height = pyautogui.size()
        
        # Map JSON keys to BoundingBoxType
        json_to_bbox_type = {
            "taskbarBBox": BoundingBoxType.TASK_BAR,
            "chromeBBox": BoundingBoxType.CHROME,
            "renderBBox": BoundingBoxType.WEBSITE_RENDER
        }
        
        # Load bounding boxes from JSON file
        with open(JSON_FILE_PATH, 'r') as f:
            bbox_data = json.load(f)
        
        # Create bounding boxes for each type
        for json_key, bbox_type in json_to_bbox_type.items():
            if json_key in bbox_data:
                data = bbox_data[json_key]
                self.bboxes[bbox_type] = AbstractBoundingBox(
                    bbox_type,
                    data["x"],
                    data["y"],
                    data["width"],
                    data["height"]
                )
        
        # Create system bounding box
        chrome_bbox = self.bboxes[BoundingBoxType.CHROME]
        taskbar_bbox = self.bboxes[BoundingBoxType.TASK_BAR]
        
        calculated_width = max(chrome_bbox.width, taskbar_bbox.width)
        calculated_height = chrome_bbox.height + taskbar_bbox.height
        
        # Compare calculated dimensions with pyautogui dimensions
        if calculated_width != system_width or calculated_height != system_height:
            raise ValueError(f"System dimension mismatch: Calculated ({calculated_width}x{calculated_height}) " 
                  f"doesn't match actual screen dimensions ({system_width}x{system_height})")
        
        # Create system bounding box
        self.bboxes[BoundingBoxType.SYSTEM] = AbstractBoundingBox(
            BoundingBoxType.SYSTEM,
            0,  # Assuming system starts at (0,0)
            0,
            system_width,  # Use actual system dimensions from pyautogui
            system_height
        )


if __name__ == "__main__":
    bbox_factory = BBoxFactory()
    print(bbox_factory.get_system_bbox().height)
    print(bbox_factory.get_chrome_bbox().height)
    print(bbox_factory.get_task_bar_bbox().height)
    print(bbox_factory.get_website_render_bbox().height)












