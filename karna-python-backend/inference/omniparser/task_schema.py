from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
from robot.chrome_robot import ChromeRobot
import tempfile
import os
from datetime import datetime
from robot.base_robot import Region
from util.omniparser import OmniparserResult, Omniparser
from inference.omniparser.omni_helper import get_omniparser_result_model_from_image_path, OmniParserResultModel
import logging
from vertical_patch_matcher import VerticalPatchMatcher
from vertical_patch_matcher import PatchMatchResult
from PIL import Image
import time
logger = logging.getLogger(__name__)
from clipboard_utils import *

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

DEFAULT_VIEWPORT = {
    "x": 952,
    "y": 121,
    "width": 960,
    "height": 927
}
class TaskPlanner():
    task_schema: Task
    def __init__(self, task_schema: Task):
        self.task_schema = task_schema

class TaskExecutor():
    task_planner: TaskPlanner
    chrome_robot: ChromeRobot
    omniparser: Omniparser
    omniparser_results_list: List[OmniParserResultModel]
    chrome_robot_ready: bool
    vertical_patch_matcher: VerticalPatchMatcher
    viewport: Dict[str, int]
    current_directory: str
    
    def __init__(self, task_planner: TaskPlanner, viewport: Dict[str, int] = DEFAULT_VIEWPORT):
        self.task_planner = task_planner
        self.chrome_robot = ChromeRobot()
        self.omniparser = Omniparser()
        self.omniparser_results_list = []
        self.chrome_robot_ready = False
        self.vertical_patch_matcher = VerticalPatchMatcher()
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.viewport = viewport
        
    def set_viewport(self, viewport: Dict[str, int]):
        self.viewport = viewport
        
    def send_text_to_clipboard(self, text: str):
        """
        Send text to clipboard.
        """
        send_text_to_clipboard(text)
        
    def send_image_to_clipboard(self, image_path: str):
        """
        Send image to clipboard.
        """
        copy_files_with_powershell([image_path])
        time.sleep(1)
        self.chrome_robot.paste()
    
    def prepare_for_task(self):
        """
        Prepare for the task.
        """
        self.chrome_robot_ready = self.open_app_snapped_right()
        if not self.chrome_robot_ready:
            raise Exception("Chrome robot not ready")
        else:
            logger.info("Chrome robot ready")
        
    def find_match_for_target(self, target: Target, omniparser_result_model: OmniParserResultModel) -> Optional[PatchMatchResult]:
        """
        Find the patch for the target.
        
        Args:
            target: Target containing the type and value
            omniparser_result_model: OmniParserResultModel containing parsed elements
            
        Returns:
            Optional[PatchMatchResult]: The match result if found, None otherwise
        """
        logger.info(f"Finding match for target: {target}")
        target_type = target.type
        target_value = target.value
        
        if target_type == ScreenObjectType.NONE:
            logger.info("Target type is NONE, no patch matching required")
            return None
        
        if target_value is None:
            logger.warning(f"Target value is None for target type {target_type}")
            return None
        
        # Construct full patch path
        patch_path = os.path.join(self.current_directory, target_value)
        
        # Check if patch file exists
        if not os.path.exists(patch_path):
            logger.error(f"Patch image not found: {patch_path}")
            return None
        
        # Load patch image with proper error handling
        try:
            patch_img = Image.open(patch_path)
            logger.info(f"Loaded patch image: {patch_path} ({patch_img.size})")
        except Exception as e:
            logger.error(f"Failed to load patch image {patch_path}: {e}")
            return None
            
        # Select appropriate matching method based on target type
        # Convert ScreenObjectType enum to string value for source_types
        source_types = [str(target_type)]  # This converts the enum to its string value
        use_identical_match = False  # Flag for using identical matching
        
        # For certain target types, we might want exact matches
        if target_type == ScreenObjectType.BOX_YOLO_CONTENT_YOLO:
            use_identical_match = True
        
        # Perform matching
        try:
            if use_identical_match:
                # Use higher threshold for exact matches
                result = self.vertical_patch_matcher.find_identical_element(
                    patch_img, 
                    omniparser_result_model, 
                    # source_types=source_types
                )
            else:
                # Use standard matching
                result = self.vertical_patch_matcher.find_matching_element(
                    patch_img, 
                    omniparser_result_model, 
                    # source_types=source_types
                )
                
            # Log the result
            if result and result.match_found:
                logger.info(f"Found match for {target_type} with score {result.similarity_score:.4f} (ID: {result.matched_element_id})")
            else:
                logger.warning(f"No match found for {target_type}")
                
            return result
            
        except Exception as e:
            logger.error(f"Error during patch matching: {e}")
            return None
    
    def execute_task(self):
        # execute the task
        for step in self.task_planner.task_schema.steps:
            if isinstance(step, MouseStep):
                self.execute_mouse_step(step)
                break
    
    def execute_mouse_step(self, mouse_step: MouseStep):
        """
        Execute a mouse step.
        Args:
            mouse_step: MouseStep
        """
        if mouse_step.target.type == ScreenObjectType.NONE:
            logger.info("Target type is NONE, no patch matching required")
            # click at the center of the screen
            if mouse_step.attention == Attention.CENTER:
                self.chrome_robot.click(self.viewport["x"] + self.viewport["width"] // 2, self.viewport["y"] + self.viewport["height"] // 2)
            else:
                logger.error(f"Invalid attention: {mouse_step.attention}")
            return
        # get the omniparser result model
        omniparser_result_model = self.get_omniparser_result_model()
        # get the match for the target
        match : Optional[PatchMatchResult] = self.find_match_for_target(mouse_step.target, omniparser_result_model)
        # execute the mouse step
        parsed_content_result = match.parsed_content_result if match else None
        if parsed_content_result:
            logger.info(f"Parsed content result: {parsed_content_result}")
            normalized_bbox = self.normalize_bbox(parsed_content_result.bbox)
            x = normalized_bbox[0]
            y = normalized_bbox[1]
            print(f"Clicking at: {x}, {y}")
            self.chrome_robot.click(int(x), int(y))
        else:
            logger.error(f"Could not find patch for target: {mouse_step.target}")
    def execute_keyboard_step(self, keyboard_step: KeyboardActionStep):
        """
        Execute a keyboard step.
        Args:
            keyboard_step: KeyboardActionStep
        """
        pass
    
    def execute_wait_step(self, wait_step: WaitStep):
        """
        Execute a wait step.
        Args:
            wait_step: WaitStep
        """
        default_time_interval = 2.0
        default_timeout = 30.0
        # get the omniparser result model
        omniparser_result_model = self.get_omniparser_result_model()
        # get the match for the target
        match : Optional[PatchMatchResult] = self.find_match_for_target(wait_step.target, omniparser_result_model)
        # execute the mouse step
        parsed_content_result = match.parsed_content_result if match else None
        if parsed_content_result:
            logger.info(f"Parsed content result: {parsed_content_result}")
            normalized_bbox = self.normalize_bbox(parsed_content_result.bbox)
            x = normalized_bbox[0]
            y = normalized_bbox[1]
            print(f"Found the target at: {x}, {y}")
        else:
            logger.error(f"Could not find patch for target: {wait_step.target}")
            
    def normalize_bbox(self, bbox: List[float]) -> List[int]:
        """
        Normalize the bbox to the screen size coordinates from viewport coordinates.
        """
        # Convert from viewport-relative coordinates to absolute screen coordinates
        # by adding the viewport's position offset
        viewport_x = self.viewport["x"]
        viewport_y = self.viewport["y"]
        
        # Calculate absolute screen coordinates
        absolute_x1 = int(viewport_x + bbox[0])
        absolute_y1 = int(viewport_y + bbox[1])
        absolute_x2 = int(viewport_x + bbox[2])
        absolute_y2 = int(viewport_y + bbox[3])
        
        return [absolute_x1, absolute_y1, absolute_x2, absolute_y2]
    
    def open_app_snapped_right(self) -> bool:
        """
        Open the app snapped to the right.
        """
        url = self.task_planner.task_schema.app_url
        return self.chrome_robot.open_url_snapped_right(url, wait_time=2.0)

    def capture_viewport_screenshot(self) -> str:
        """
        Takes a full screen screenshot using chrome_robot, crops it according to 
        self.viewport, saves in a temp directory, and returns the absolute path.
        
        Returns:
            str: Absolute path to the cropped screenshot file
        """
        
        # Create temporary directory if it doesn't exist
        temp_dir = os.path.join(tempfile.gettempdir(), "karna_screenshots")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = os.path.join(temp_dir, f"viewport_screenshot_{timestamp}.png")
        
        # Create a Region object from self.viewport for cropping
        viewport_region = Region(
            x=self.viewport["x"],
            y=self.viewport["y"],
            width=self.viewport["width"],
            height=self.viewport["height"]
        )
        
        # Take and save cropped screenshot
        self.chrome_robot.save_screenshot(screenshot_path, region=viewport_region)
        
        # Return absolute path to the saved screenshot
        return os.path.abspath(screenshot_path)
    
    def get_omniparser_result_model(self) -> OmniParserResultModel:
        """
        Get the omniparser result model.
        """
        image_path = self.capture_viewport_screenshot()
        logger.info(f"Image path: {image_path}")
        # save the image to the current directory
        v_image_path = os.path.join(self.current_directory, "viewport_screenshot.png")
        v_image = Image.open(image_path)
        v_image.save(v_image_path)
        # get the omniparser result model
        return get_omniparser_result_model_from_image_path(image_path, self.omniparser)


