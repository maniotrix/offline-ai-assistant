from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum
from robot.chrome_robot import ChromeRobot
import tempfile
import os
from datetime import datetime
from robot.base_robot import Region
from inference.omniparser.util.omniparser import OmniparserResult, Omniparser
from inference.cortex_vision.omni_helper import get_omniparser_result_model_from_image_path, OmniParserResultModel
import logging
from inference.cortex_vision.vertical_patch_matcher import VerticalPatchMatcher
from inference.cortex_vision.vertical_patch_matcher import PatchMatchResult
from PIL import Image
import time
import pyperclip
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from clipboard_utils import *
from dataclasses import dataclass
import random
import math
import numpy as np
from functools import lru_cache
import pyautogui

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
    Schema for steps defined in the task schema json file file
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
    patches_dir: str
    def __init__(self, task_schema: Task, patches_dir: str):
        self.task_schema = task_schema
        self.patches_dir = patches_dir

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
        Visualize task steps by creating individual plots for each step log.
        Each plot shows the omni image (screen capture), patch image (template),
        and match information with bounding box visualization.
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
        from matplotlib.gridspec import GridSpec
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a directory for saving individual plots if needed
        # import os
        # plot_dir = os.path.join(self.current_directory, "step_visualizations")
        # os.makedirs(plot_dir, exist_ok=True)
        
        # Set up the overall figure style
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Create and display a separate figure for each step
        for step_log in self.task_steps:
            # Create a new figure with a specific layout using GridSpec
            fig = plt.figure(figsize=(15, 10))
            gs = GridSpec(3, 3, figure=fig, height_ratios=[6, 1, 3])
            
            # Add overall title for this step
            fig.suptitle(f"Step {step_log.step_id} Visualization", 
                        fontsize=18, fontweight='bold', y=0.98)
            
            # Main omni image panel - spans the entire width
            ax_main = fig.add_subplot(gs[0, :])
            
            # Patch image panel - placed in bottom left
            ax_patch = fig.add_subplot(gs[2, 0])
            
            # Match info panel - placed in bottom center and right
            ax_info = fig.add_subplot(gs[2, 1:])
            ax_info.axis('off')  # Hide axis for text display
            
            # Process omni image (base64 to PIL Image)
            try:
                omni_img_data = base64.b64decode(step_log.omni_image)
                omni_img = Image.open(io.BytesIO(omni_img_data))
                omni_array = np.array(omni_img)
            except Exception as e:
                logger.error(f"Error decoding omni image for step {step_log.step_id}: {e}")
                omni_img = Image.new('RGB', (800, 600), color='gray')
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
            
            # Display the omni image
            ax_main.imshow(omni_array)
            ax_main.set_title("Screen Capture", fontsize=14, fontweight='bold')
            ax_main.axis('off')
            
            # Display the patch image
            ax_patch.imshow(patch_array)
            ax_patch.set_title("Target Template", fontsize=12, fontweight='bold')
            ax_patch.axis('off')
            
            # Prepare match information display
            match_info = []
            match_found = False
            
            if step_log.match_result and step_log.match_result.match_found:
                match_found = True
                match_info.append(f"✓ Match found")
                match_info.append(f"Element ID: {step_log.match_result.matched_element_id}")
                match_info.append(f"Similarity Score: {step_log.match_result.similarity_score:.4f}")
                
                # If the match result has parsed content with a bbox, draw it
                if (hasattr(step_log.match_result, 'parsed_content_result') and 
                    step_log.match_result.parsed_content_result and 
                    hasattr(step_log.match_result.parsed_content_result, 'bbox')):
                    
                    bbox = step_log.match_result.parsed_content_result.bbox
                    match_info.append(f"Bounding Box: [{int(bbox[0])}, {int(bbox[1])}, {int(bbox[2])}, {int(bbox[3])}]")
                    
                    # Draw rectangle on the omni image
                    rect_x = bbox[0]
                    rect_y = bbox[1]
                    rect_width = bbox[2] - bbox[0]
                    rect_height = bbox[3] - bbox[1]
                    
                    # Create a Rectangle patch with better visibility
                    rect = patches.Rectangle(
                        (rect_x, rect_y), rect_width, rect_height, 
                        linewidth=2, edgecolor='red', facecolor='none', 
                        linestyle='-', alpha=0.8
                    )
                    
                    # Add the patch to the omni image axes
                    ax_main.add_patch(rect)
                    
                    # Calculate center point (for reference only)
                    center_x = rect_x + rect_width/2
                    center_y = rect_y + rect_height/2
            else:
                match_info.append("❌ No match found")
            
            # Display match information in a box
            info_box = '\n'.join(match_info)
            props = dict(boxstyle='round,pad=1', facecolor='white' if match_found else '#ffcccc',
                         alpha=0.8, edgecolor='#888888')
            ax_info.text(0.5, 0.5, info_box, fontsize=12,
                         ha='center', va='center',
                         bbox=props,
                         transform=ax_info.transAxes)
            
            ax_info.set_title("Match Information", fontsize=12, fontweight='bold')
            
            # Add a small summary below the patch
            ax_summary = fig.add_subplot(gs[1, :])
            ax_summary.axis('off')
            summary_text = f"Step {step_log.step_id}: {'Match found' if match_found else 'No match found'}"
            ax_summary.text(0.5, 0.5, summary_text, 
                            ha='center', va='center', fontsize=12, 
                            fontweight='bold', color='green' if match_found else 'red',
                            transform=ax_summary.transAxes)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for suptitle
            
            # Optional: Save the figure
            # fig.savefig(os.path.join(plot_dir, f"step_{step_log.step_id}.png"), dpi=150, bbox_inches='tight')
            
            # Display plot for this step
            plt.show()
        
        # Summary message
        print(f"Visualized {len(self.task_steps)} step logs")

class Clipboard():
    text: str
    directory_path: str | None
    
    def __init__(self):
        self.text = ""
        self.directory_path = None
        
    def set_text(self, text: str):
        self.text = text
        
    def set_directory(self, directory_path: str):
        self.directory_path = directory_path
        
    def set_all(self, text: str, directory_path: str | None = None):
        self.text = text
        self.directory_path = directory_path

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
    clipboard: Clipboard

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
        self.clipboard = Clipboard()
        
    def set_clipboard(self, text: str, directory_path: str | None = None):
        self.clipboard.set_all(text, directory_path)

    def set_viewport(self, viewport: Dict[str, int]):
        self.viewport = viewport
        
    def send_text_to_clipboard(self, text: str):
        """
        Send text to clipboard.
        """
        send_text_to_clipboard(text)
        
    def send_text_to_clipboard_and_paste(self, text: str):
        """
        Send text to clipboard and paste it.
        """
        self.send_text_to_clipboard(text)
        time.sleep(1)
        self.chrome_robot.paste()
        
    
    def send_image_to_clipboard_and_paste(self, image_path: str):
        """
        Send image to clipboard.
        """
        copy_files_with_powershell([image_path])
        time.sleep(1)
        self.chrome_robot.paste()
        time.sleep(2)
        
    def process_clipboard(self):
        self.send_directory_to_clipboard_and_paste(self.clipboard.text, self.clipboard.directory_path)
        
    def send_directory_to_clipboard_and_paste(self, text: str, directory_path: str | None = None):
        file_paths: List[str] | None = None
        if directory_path is not None:
            file_paths = []
            for file_path in os.listdir(directory_path):
                file_paths.append(os.path.join(directory_path, file_path))
        self.process_all_for_clipboard(text, file_paths)
            
    def process_all_for_clipboard(self, text: str, file_paths: List[str] | None = None):
        """
        Process all steps for clipboard.
        """
        if file_paths is not None:
            for file_path in file_paths:
                self.send_image_to_clipboard_and_paste(file_path)
        if text is not None:
            self.send_text_to_clipboard_and_paste(text)
    
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
        patch_path = os.path.join(self.task_planner.patches_dir, target_value)
        
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
                x = self.viewport["x"] + self.viewport["width"] // 2
                y = self.viewport["y"] + self.viewport["height"] // 2
                self.human_like_click(x, y, clicks=1)
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
            self.human_like_click(centre_x, centre_y, clicks=2)
            # add the step log
            if mouse_step.target.value:
                step_log = StepLog(
                    step_id=mouse_step.step_id,
                    omni_image=omniparser_result_model.omniparser_result.dino_labled_img,
                    patch_image_path = os.path.join(self.task_planner.patches_dir, mouse_step.target.value),
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
            self.process_clipboard()
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
        default_timeout = 120.0
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
                        patch_image_path = os.path.join(self.task_planner.patches_dir, wait_step.target.value),
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

    def human_like_click(self, x: int, y: int, clicks: int = 1, interval: float = 0.1) -> None:
        """
        Perform a human-like mouse click using pyautogui directly with our custom tween.
        
        Args:
            x: X-coordinate to click
            y: Y-coordinate to click
            clicks: Number of clicks
            interval: Interval between clicks
        """
        try:
            # Move to position with human-like movement
            pyautogui.moveTo(x, y, duration=0.15, tween=human_like_tween)
            time.sleep(0.05)  # Small pause after reaching target
            
            # Perform the click(s)
            pyautogui.click(clicks=clicks, interval=interval)
            logger.info(f"Human-like click at ({x}, {y})")
        except Exception as e:
            logger.error(f"Failed to perform human-like click: {str(e)}")
            raise

# Human-like tween function for mouse movements
def human_like_tween(t):
    """
    A human-like tween function for mouse movements.
    
    Args:
        t: A value between 0.0 and 1.0 representing the progress of the motion.
        
    Returns:
        A modified value between 0.0 and 1.0 that creates human-like motion.
    """
    # Base easeInOutQuad curve for natural acceleration/deceleration
    if t < 0.5:
        base = 2 * t * t  # Accelerate in first half
    else:
        base = -1 + (4 - 2 * t) * t  # Decelerate in second half
    
    # Add micro-adjustments (small random jitter)
    jitter_strength = 0.03  # How strong the micro-adjustments are
    jitter = random.uniform(-jitter_strength, jitter_strength) * math.sin(t * math.pi * random.uniform(5, 8))
    
    # Add occasional hesitation (slight pauses)
    hesitation_chance = 0.15  # Probability of hesitation
    hesitation_strength = 0.04  # How strong the hesitation effect is
    if random.random() < hesitation_chance:
        # Create a slight pause effect by pulling the curve back a tiny bit
        hesitation = -hesitation_strength * math.sin(t * math.pi)
    else:
        hesitation = 0
        
    # Occasional overshoot and correction near the target
    overshoot = 0
    if t > 0.85 and random.random() < 0.2:  # 20% chance of overshooting near the end
        overshoot = 0.05 * math.sin((t - 0.85) * 5 * math.pi)
    
    # Combine all effects, ensuring the result stays in the 0.0-1.0 range
    result = max(0.0, min(1.0, base + jitter + hesitation + overshoot))
    
    return result
