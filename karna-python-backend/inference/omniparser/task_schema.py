from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from robot.chrome_robot import ChromeRobot

class ScreenObjectType(str, Enum):
    """
    Screen object types found on the screen.
    """
    BOX_YOLO_CONTENT_OCR = "box_yolo_content_ocr"
    BOX_OCR_CONTENT_OCR = "box_ocr_content_ocr"
    BOX_YOLO_CONTENT_YOLO = "box_yolo_content_yolo"
    NONE = "none"

class ActionType(str, Enum):
    MOUSE_ACTION = "mouse_action"
    KEYBOARD_ACTION = "keyboard_action"
    WAIT = "wait"

class WaitUntilDependencyValueType(str, Enum):
    THIS_STEP = "this_step"
    PREVIOUS_STEP = "previous_step"

class Step(BaseModel):
    step_id: int
    description: str
    action_type: ActionType
    action: str
    target_type: Optional[ScreenObjectType] = None
    is_target_repeated: Optional[bool] = False
    target_repeated_layout_type: Optional[str] = None
    is_target_repeated_layout_index_fixed: Optional[bool] = None
    target_repeated_layout_index: Optional[int] = None


class Task(BaseModel):
    task: str
    description: str
    app_name: str
    app_type: str
    app_url: str
    steps: List[Step]
    
def load_task_schema_from_json(json_file_path: str):
    with open(json_file_path, 'r') as file:
        return Task.model_validate_json(file.read())

class TaskPlanner():
    task_schema: Task
    def __init__(self, task_schema: Task):
        self.task_schema = task_schema

class TaskExecutor():
    task_planner: TaskPlanner
    chrome_robot: ChromeRobot
    def __init__(self, task_planner: TaskPlanner):
        self.task_planner = task_planner
        self.chrome_robot = ChromeRobot()

    def execute_task(self):
        # execute the task
        pass


