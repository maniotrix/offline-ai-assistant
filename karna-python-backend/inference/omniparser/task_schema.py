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
import pyperclip
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from clipboard_utils import *
from dataclasses import dataclass

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
    keyboard_shortcut: Optional[str] = None
    
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

@dataclass
class StepLog():
    step_id: int
    omni_image: str # base64 encoded image
    patch_image_path: str
    match_result: PatchMatchResult
    
class TaskLog():
    task_steps: List[StepLog]
    
    def __init__(self):
        self.task_steps = []
        
    def add_step_log(self, step_log: StepLog):
        self.task_steps.append(step_log)
        
    def get_step_log(self, step_id: int) -> StepLog:
        return self.task_steps[step_id]
    
    def get_all_step_logs(self) -> List[StepLog]:
        return self.task_steps
    
    def print_task_log(self):
        for step_log in self.task_steps:
            print(f"Step id: {step_log.step_id}")
            print(f"  Omni image: {step_log.omni_image}")
            print(f"  Patch image: {step_log.patch_image_path}")
            print(f"  Match result: {step_log.match_result}")
            
    def reset_task_log(self):
        self.task_steps = []
            
    def visualize_task_log(self):
        """
        Visualize all task steps in a single image showing omni images, patch images and match results.
        Displays the visualization in a matplotlib window with bounding boxes drawn around matches.
        """
        if not self.task_steps:
            logger.warning("No task steps to visualize")
            return
            
        import base64
        import io
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from PIL import Image, ImageDraw, ImageFont
        
        # Determine the number of steps to visualize
        num_steps = len(self.task_steps)
        
        # Create a figure with subplots for each step (2 images per step)
        fig, axes = plt.subplots(num_steps, 2, figsize=(15, 5 * num_steps))
        
        # Ensure axes is always a 2D array, even with a single step
        if num_steps == 1:
            axes = np.array([axes])
            
        # Set up the figure title
        fig.suptitle(f"Task Execution Visualization ({num_steps} steps)", fontsize=16)
        
        for i, step_log in enumerate(self.task_steps):
            # Step info text
            step_info = f"Step {step_log.step_id}"
            
            # Process omni image (base64 to PIL Image)
            try:
                omni_img_data = base64.b64decode(step_log.omni_image)
                omni_img = Image.open(io.BytesIO(omni_img_data))
                omni_array = np.array(omni_img)
            except Exception as e:
                logger.error(f"Error decoding omni image for step {step_log.step_id}: {e}")
                omni_img = Image.new('RGB', (400, 300), color='gray')
                draw = ImageDraw.Draw(omni_img)
                draw.text((10, 10), f"Error loading omni image: {str(e)}", fill="white")
                omni_array = np.array(omni_img)
            
            # Load patch image
            try:
                patch_img = Image.open(step_log.patch_image_path)
                patch_array = np.array(patch_img)
            except Exception as e:
                logger.error(f"Error loading patch image for step {step_log.step_id}: {e}")
                patch_img = Image.new('RGB', (200, 150), color='gray')
                draw = ImageDraw.Draw(patch_img)
                draw.text((10, 10), f"Error loading patch image: {str(e)}", fill="white")
                patch_array = np.array(patch_img)
            
            # Display the images
            axes[i, 0].imshow(omni_array)
            axes[i, 0].set_title(f"{step_info} - Omni Image")
            axes[i, 0].axis('off')
            
            axes[i, 1].imshow(patch_array)
            axes[i, 1].set_title(f"{step_info} - Patch Image")
            axes[i, 1].axis('off')
            
            # Add match result info as text and draw bbox if match was found
            if step_log.match_result and step_log.match_result.match_found:
                match_info = (
                    f"Match found: ID={step_log.match_result.matched_element_id}, "
                    f"Score={step_log.match_result.similarity_score:.4f}"
                )
                
                # If the match result has parsed content with a bbox, draw it
                if (hasattr(step_log.match_result, 'parsed_content_result') and 
                    step_log.match_result.parsed_content_result and 
                    hasattr(step_log.match_result.parsed_content_result, 'bbox')):
                    
                    bbox = step_log.match_result.parsed_content_result.bbox
                    match_info += f"\nBBox: {[round(b, 2) for b in bbox]}"
                    
                    # Draw rectangle on the omni image
                    # Convert bbox [x1, y1, x2, y2] to [x, y, width, height]
                    rect_x = bbox[0]
                    rect_y = bbox[1]
                    rect_width = bbox[2] - bbox[0]
                    rect_height = bbox[3] - bbox[1]
                    
                    # Create a Rectangle patch with a distinct color and linewidth
                    rect = patches.Rectangle(
                        (rect_x, rect_y), rect_width, rect_height, 
                        linewidth=3, edgecolor='red', facecolor='none'
                    )
                    
                    # Add the patch to the omni image axes
                    axes[i, 0].add_patch(rect)
            else:
                match_info = "No match found"
                
            # Add text below the patch image
            axes[i, 1].text(0, 1.05, match_info, transform=axes[i, 1].transAxes, 
                           fontsize=10, verticalalignment='bottom')
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for suptitle
        
        # Display the plot
        plt.show()
    
class TaskExecutor():
    task_planner: TaskPlanner
    chrome_robot: ChromeRobot
    omniparser: Omniparser
    omniparser_results_list: List[OmniParserResultModel]
    chrome_robot_ready: bool
    vertical_patch_matcher: VerticalPatchMatcher
    viewport: Dict[str, int]
    current_directory: str
    task_log: TaskLog

    def __init__(self, task_planner: TaskPlanner, viewport: Dict[str, int] = DEFAULT_VIEWPORT):
        self.task_planner = task_planner
        self.chrome_robot = ChromeRobot()
        self.omniparser = Omniparser()
        self.omniparser_results_list = []
        self.chrome_robot_ready = False
        self.vertical_patch_matcher = VerticalPatchMatcher()
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.viewport = viewport
        self.task_log = TaskLog()

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
        
    def find_match_for_target(self, target: Target, omniparser_result_model: OmniParserResultModel, custom_threshold: float | None = None) -> Optional[PatchMatchResult]:
        """
        Find the patch for the target.
        
        Args:
            target: Target containing the type and value
            omniparser_result_model: OmniParserResultModel containing parsed elements
            custom_threshold: Custom threshold for the match
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
        
        # Perform matching
        try:
            # Use standard matching
            result = self.vertical_patch_matcher.find_matching_element(
                patch_img, 
                omniparser_result_model, 
                # source_types=source_types
                custom_threshold=custom_threshold
            )
                
            # Log the result
            # print(f"Patch match result: {result}")
            if result and result.match_found:
                logger.info(f"Found match for {target_type} with score {result.similarity_score:.4f} (ID: {result.matched_element_id})")
            else:
                logger.warning(f"No match found for {target_type}")
                
            return result
            
        except Exception as e:
            logger.error(f"Error during patch matching: {e}")
            return None
    
    def execute_task(self):
        """
        Execute all steps in the task sequentially.
        """
        for i, step in enumerate(self.task_planner.task_schema.steps):
            # if i > 2:
            #     logger.info("Ending task execution")
            #     return
            
            # if(i != 6):
            #     continue
            # if(i is not None and i not in [6]):
            #     continue
            print("--------------------------------")
            print(f"EXECUTING STEP: {i}")
            print("--------------------------------")
            if isinstance(step, MouseStep):
                logger.info(f"Executing mouse step {step.step_id}: {step.description}")
                success = self.execute_mouse_step(step)
                if not success:
                    logger.warning(f"Mouse step {step.step_id} failed - stopping execution")
                    return
            elif isinstance(step, KeyboardActionStep):
                logger.info(f"Executing keyboard step {step.step_id}: {step.description}")
                self.execute_keyboard_step(step)
            elif isinstance(step, WaitStep):
                logger.info(f"Executing wait step {step.step_id}: {step.description}")
                success = self.execute_wait_step(step)
                if not success:
                    logger.warning(f"Wait step {step.step_id} failed - stopping execution")
                    return
            else:
                logger.warning(f"Unknown step type: {type(step)}")
                
            # Add a small delay between steps for stability
            time.sleep(0.2)
    
    def execute_mouse_step(self, mouse_step: MouseStep) -> bool:
        """
        Execute a mouse step.
        Args:
            mouse_step: MouseStep
        """
        if mouse_step.target.type == ScreenObjectType.NONE:
            logger.info("Target type is NONE, no patch matching required")
            # click at the center of the screen
            if mouse_step.attention == Attention.CENTER:
                logger.info("Clicking at the center of the screen")
                self.chrome_robot.click(self.viewport["x"] + self.viewport["width"] // 2, 
                                        self.viewport["y"] + self.viewport["height"] // 2)
            else:
                logger.error(f"Invalid attention: {mouse_step.attention}")
                return False
            return True
        
        if mouse_step.keyboard_shortcut:
            # WARNING: This is a hack to press the keyboard shortcut
            # its not device independent and will not work on all devices
            self.chrome_robot.press_key(mouse_step.keyboard_shortcut)
            return True
        
        # get the omniparser result model
        omniparser_result_model = self.get_omniparser_result_model()
        # get the match for the target
        match : Optional[PatchMatchResult] = self.find_match_for_target(mouse_step.target, omniparser_result_model)
        # execute the mouse step
        parsed_content_result = match.parsed_content_result if match else None
        if parsed_content_result:
            logger.info(f"Parsed content result: {parsed_content_result}")
            centre_x, centre_y = self.get_centre_of_bbox(parsed_content_result.bbox)
            print(f"Clicking at: {centre_x}, {centre_y}")
            self.chrome_robot.click(centre_x, centre_y, clicks=2, duration=0.1, interval=0.1)
            # add the step log
            if mouse_step.target.value:
                step_log = StepLog(
                    step_id=mouse_step.step_id,
                    omni_image=omniparser_result_model.omniparser_result.dino_labled_img,
                    patch_image_path = os.path.join(self.current_directory, mouse_step.target.value),
                    match_result=match
                )
                self.task_log.add_step_log(step_log)
        else:
            logger.error(f"Could not find patch for target: {mouse_step.target}")
            return False
        return True
    
    def execute_keyboard_step(self, keyboard_step: KeyboardActionStep):
        """
        Execute a keyboard step.
        Args:
            keyboard_step: KeyboardActionStep
        """
        action = keyboard_step.action.lower()
        
        if action == "paste":
            logger.info("Executing paste action")
            self.chrome_robot.paste()
        elif action == "end":
            logger.info("Executing end action")
            self.chrome_robot.press_end()
        else:
            # Handle other keyboard actions as needed
            logger.info(f"Executing keyboard action: {action}")
            
        return False  # Continue task execution
    
    def execute_wait_step(self, wait_step: WaitStep):
        """
        Execute a wait step.
        Args:
            wait_step: WaitStep
        """
        default_time_interval = 0.5
        default_timeout = 30.0
        start_time = time.time()
        
        while True:
            # Check if timeout has been reached
            elapsed_time = time.time() - start_time
            if elapsed_time > default_timeout:
                logger.error(f"Timeout reached ({default_timeout}s) while waiting for target: {wait_step.target}")
                return False
                
            # Get a fresh omniparser result model for each attempt
            omniparser_result_model = self.get_omniparser_result_model()
            
            # Try to find the match for the target
            match = self.find_match_for_target(wait_step.target, omniparser_result_model, custom_threshold=0.92)
            parsed_content_result = match.parsed_content_result if match else None
            
            if parsed_content_result:
                logger.info(f"Found target after {elapsed_time:.2f}s: {parsed_content_result}")
                normalized_bbox = self.normalize_bbox(parsed_content_result.bbox)
                x = normalized_bbox[0]
                y = normalized_bbox[1]
                print(f"Found the target at: {x}, {y}")
                # add the step log
                if wait_step.target.value:
                    step_log = StepLog(
                        step_id=wait_step.step_id,
                        omni_image=omniparser_result_model.omniparser_result.dino_labled_img,
                        patch_image_path = os.path.join(self.current_directory, wait_step.target.value),
                        match_result=match
                    )
                    self.task_log.add_step_log(step_log)
                return True
            else:
                logger.info(f"Target not found, waiting {default_time_interval}s before trying again ({elapsed_time:.2f}s elapsed)")
                time.sleep(default_time_interval)
                
            # Continue the loop to try again
    
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
    
    def get_centre_of_bbox(self, bbox: List[float]) -> List[int]:
        """
        Get the centre of the bbox.
        """
        normalized_bbox = self.normalize_bbox(bbox)
        centre_x = (normalized_bbox[0] + normalized_bbox[2]) / 2
        centre_y = (normalized_bbox[1] + normalized_bbox[3]) / 2
        return [int(centre_x), int(centre_y)]
    
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
        result = get_omniparser_result_model_from_image_path(image_path, self.omniparser, local_semantics=False)
        #result = get_omniparser_result_model_from_image_path(v_image_path, self.omniparser)
        return result

    def get_clipboard_text(self) -> str:
        """
        Gets the current text from clipboard.
        
        Returns:
            str: The text content from clipboard
        """
        clipboard_text = get_text_from_clipboard()
        logger.info(f"Got text from clipboard: {clipboard_text[:50]}{'...' if len(clipboard_text) > 50 else ''}")
        return clipboard_text
