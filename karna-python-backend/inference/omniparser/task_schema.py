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
    
class Attention(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    
class Target(BaseModel):
    type: ScreenObjectType
    value: Optional[str] = None # can be text or image path

class Step(BaseModel):
    """_summary_
    Schema for chat_with_chatgpt.json file
    Args:
        BaseModel (_type_): _description_
    """
    step_id: int
    description: str
    action_type: ActionType
    action: str
    attention: Attention
    

class KeyboardActionStep(Step):
    action_type: ActionType = ActionType.KEYBOARD_ACTION
    
class StepWithTarget(Step):
    target: Target
    
class MouseStep(StepWithTarget):
    action_type: ActionType = ActionType.MOUSE_ACTION
    
class WaitStep(StepWithTarget):
    action_type: ActionType = ActionType.WAIT
    


class Task(BaseModel):
    task: str
    description: str
    app_name: str
    app_type: str
    app_url: str
    steps: List[Step]
    
    def model_dump_json(self, **kwargs):
        """
        Override model_dump_json to properly include all fields from Step subclasses
        """
        # Extract JSON-specific parameters (like indent) that don't belong in model_dump
        json_kwargs = {}
        model_kwargs = {}
        
        for key, value in kwargs.items():
            if key in ['indent', 'separators', 'default', 'sort_keys', 'cls']:
                json_kwargs[key] = value
            else:
                model_kwargs[key] = value
                
        data = self.model_dump(**model_kwargs)
        
        # Properly serialize steps with all their fields
        steps_data = []
        for step in self.steps:
            step_data = step.model_dump(**model_kwargs)
            # For steps with target, make sure target is included
            if isinstance(step, StepWithTarget) and hasattr(step, 'target'):
                step_data['target'] = step.target.model_dump(**model_kwargs)
            steps_data.append(step_data)
        
        data['steps'] = steps_data
        
        import json
        return json.dumps(data, **json_kwargs)
    
    def get_mouse_steps(self) -> List[MouseStep]:
        """Get all mouse action steps in this task."""
        return [step for step in self.steps 
                if step.action_type == ActionType.MOUSE_ACTION and isinstance(step, MouseStep)]
    
    def get_keyboard_steps(self) -> List[KeyboardActionStep]:
        """Get all keyboard action steps in this task."""
        return [step for step in self.steps 
                if step.action_type == ActionType.KEYBOARD_ACTION and isinstance(step, KeyboardActionStep)]
    
    def get_wait_steps(self) -> List[WaitStep]:
        """Get all wait steps in this task."""
        return [step for step in self.steps 
                if step.action_type == ActionType.WAIT and isinstance(step, WaitStep)]
    
    def get_steps_with_target(self) -> List[StepWithTarget]:
        """Get all steps that have targets (mouse and wait steps)."""
        return [step for step in self.steps if isinstance(step, StepWithTarget)]
    
    @staticmethod
    def get_step_instance(step_data: dict) -> Step:
        """
        Create the appropriate Step subclass instance based on the action_type.
        
        Args:
            step_data: Dictionary containing step data
            
        Returns:
            An instance of the appropriate Step subclass
        """
        action_type = step_data.get("action_type")
        
        # Add default target if not present for steps that require it
        if action_type in [ActionType.MOUSE_ACTION, ActionType.WAIT] and "target" not in step_data:
            step_data["target"] = {"type": ScreenObjectType.NONE, "value": None}
        
        if action_type == ActionType.MOUSE_ACTION:
            return MouseStep.model_validate(step_data)
        elif action_type == ActionType.KEYBOARD_ACTION:
            return KeyboardActionStep.model_validate(step_data)
        elif action_type == ActionType.WAIT:
            return WaitStep.model_validate(step_data)
        else:
            # Default to base Step
            return Step.model_validate(step_data)

def load_task_schema_from_json(json_file_path: str) -> Task:
    """
    Load a task schema from a JSON file with proper step type handling.
    
    Args:
        json_file_path: Path to the JSON file containing the task schema
        
    Returns:
        A Task instance with properly typed steps
    """
    import json
    
    with open(json_file_path, 'r') as file:
        task_data = json.load(file)
        
        # Process steps to ensure proper subclass instantiation
        if "steps" in task_data:
            steps_data = task_data["steps"]
            task_data["steps"] = []  # Clear steps to add properly typed ones
            
            for step_data in steps_data:
                step_instance = Task.get_step_instance(step_data)
                task_data["steps"].append(step_instance)
        
        return Task.model_validate(task_data)

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


