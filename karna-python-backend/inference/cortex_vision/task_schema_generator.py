import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from PIL import Image

# Import required components from the existing cortex_vision module
from inference.cortex_vision.task_schema import (
    Task, Step, MouseStep, KeyboardActionStep, WaitStep, StepWithTarget,
    Target, ScreenObjectType, ActionType, Attention
)
from inference.cortex_vision.omni_helper import (
    get_omniparser_inference_data_from_json,
    OmniParserResultModel,
    ParsedContentResult,
    get_omniparser_inference_data,
    OmniParserResultModelList
)
from config.paths import workspace_dir
from services.screen_capture_service import ScreenshotEvent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run_omniparser_inference(json_file_path: str) -> Tuple[OmniParserResultModelList, List[ScreenshotEvent]]:
    logger.info(f"Loading screenshot events from JSON file: {json_file_path}")
        
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file: {str(e)}")
    
    if not events_data or not isinstance(events_data, list):
        raise ValueError("JSON file does not contain a list of screenshot events")
    
    # Convert JSON data to ScreenshotEvent objects
    screenshot_events = []
    for event_dict in events_data:
        # Convert ISO format string back to datetime
        if 'timestamp' in event_dict:
            event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
        
        screenshot_path = event_dict["screenshot_path"] # type: ignore
        # convert screenshot_path to proper path using paths config
        screenshot_path = workspace_dir / screenshot_path
        event_dict["screenshot_path"] = screenshot_path # type: ignore
        # Create ScreenshotEvent object
        try:
            event = ScreenshotEvent(**event_dict)
            screenshot_events.append(event)
        except (TypeError, ValueError) as e:
            logger.warning(f"Skipping invalid event: {str(e)}")
    
    logger.info(f"Loaded {len(screenshot_events)} screenshot events from JSON file")
    return get_omniparser_inference_data(screenshot_events, caption_icons=True), screenshot_events

class TaskSchemaGenerator:
    """
    Generates a fully specified task schema JSON file from a simplified training JSON file
    by analyzing screenshots and extracting UI element patches.
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the TaskSchemaGenerator with optional output directory.
        
        Args:
            output_dir: Directory to save extracted patches and output JSON
        """
        self.output_dir = output_dir
        self.patches_dir: Optional[str] = None
    
    def _ensure_output_directory(self, training_json_path: str) -> str:
        """
        Ensure the output directory exists. If not provided, create one based on the training file name.
        
        Args:
            training_json_path: Path to the training JSON file
            
        Returns:
            str: Path to the output directory
        """
        if self.output_dir:
            output_dir = self.output_dir
        else:
            # Create directory based on training file name
            training_file_name = os.path.basename(training_json_path)
            training_name = os.path.splitext(training_file_name)[0]
            output_dir = f"generated_{training_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create full path
        output_path = os.path.abspath(output_dir)
        os.makedirs(output_path, exist_ok=True)
        
        # Create patches subdirectory
        patches_dir = os.path.join(output_path, "patches")
        os.makedirs(patches_dir, exist_ok=True)
        self.patches_dir = patches_dir
        
        logger.info(f"Created output directory: {output_path}")
        return output_path
    
    def load_training_json(self, file_path: str) -> Dict[str, Any]:
        """Load the simplified training JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def extract_patch_from_coordinates(self, 
                                      event: Dict[str, Any],
                                      omni_result: OmniParserResultModel) -> Tuple[Optional[ParsedContentResult], Optional[Image.Image]]:
        """
        Extract a patch for the UI element containing the mouse coordinates from a screenshot event.
        
        Args:
            event: Screenshot event with mouse coordinates
            omni_result: OmniParser result for the screenshot
            
        Returns:
            Tuple of (ParsedContentResult, Image) if found, (None, None) otherwise
        """
        # Get mouse coordinates
        x = event.get('mouse_x')
        y = event.get('mouse_y')
        
        if x is None or y is None:
            logger.warning(f"Event {event.get('event_id')} has no mouse coordinates")
            return None, None
        
        # Find containing element - use the first element whose bounding box contains the coordinates
        element = None
        
        for parsed_element in omni_result.parsed_content_results:
            bbox = parsed_element.bbox
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            
            # Check if point is inside the element
            if x1 <= x <= x2 and y1 <= y <= y2:
                element = parsed_element
                break
        
        if element is None:
            logger.warning(f"No element found containing coordinates ({x}, {y})")
            return None, None
        
        # Extract the patch
        try:
            image_path = omni_result.omniparser_result.original_image_path
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Original image not found: {image_path}")
            
            # Load the image
            full_image = Image.open(image_path).convert("RGB")
            
            # Extract the patch
            bbox = element.bbox
            x1, y1, x2, y2 = [int(coord) for coord in bbox]
            patch = full_image.crop((x1, y1, x2, y2))
            
            return element, patch
            
        except Exception as e:
            logger.error(f"Error extracting patch: {str(e)}")
            return element, None
    
    def save_patch(self, patch: Image.Image, element_id: int, element_type: str, element_content: str) -> str:
        """
        Save a patch image to the patches directory.
        
        Args:
            patch: The image patch to save
            element_id: The ID of the element
            element_type: The type of the element (for filename)
            
        Returns:
            str: The path to the saved patch image
        """
        if not self.patches_dir:
            raise ValueError("Patches directory not initialized. Call _ensure_output_directory first.")
            
        # Create a filename based on element type and ID
        filename = f"{element_id}_{element_type}_{element_content}.png"
        filepath = os.path.join(self.patches_dir, filename)
        
        # Save the image
        patch.save(filepath)
        logger.info(f"Saved patch to {filepath}")
        
        return filepath
    
    def process_non_wait_step(self, step_data: Dict[str, Any], 
                             screenshot_event: Dict[str, Any],
                             omni_result: OmniParserResultModel) -> Step:
        """
        Process a non-wait step by matching it with a screenshot event.
        
        Args:
            step_data: Step data from the training JSON
            screenshot_event: Corresponding screenshot event
            omni_result: OmniParser result for the screenshot
            
        Returns:
            Step: Processed step object
        """
        # Extract basic step properties
        step_id = int(step_data["step_id"])
        description = str(step_data["description"])
        
        # Get attention or use default from step_data
        attention_str = step_data.get("attention", None)
        if attention_str is None:
            # If no attention in step, use default_attention from training JSON
            attention_str = self.training_data.get("default_attention", "bottom")
        attention = Attention(attention_str)
        
        # Determine action type based on screenshot event
        action_type = None
        action = None
        target = None
        keyboard_shortcut = step_data.get("keyboard_shortcut")
        
        # Check for mouse events
        if screenshot_event.get('mouse_x') is not None and screenshot_event.get('mouse_y') is not None:
            action_type = ActionType.MOUSE_ACTION
            action = "click"
            
            # Extract UI element at mouse coordinates
            element, patch = self.extract_patch_from_coordinates(screenshot_event, omni_result)
            
            if element and patch:
                # Save the patch
                patch_path = self.save_patch(
                    patch, 
                    element.id, 
                    element.type.replace(" ", "_"),
                    element.content.replace(" ", "_")
                )
                
                # Create target
                target = Target(
                    type=self._determine_screen_object_type(element),
                    value=os.path.basename(patch_path)
                )
            else:
                # No element found, use NONE type
                target = Target(type=ScreenObjectType.NONE)
                
        # Check for keyboard events
        elif screenshot_event.get('key_char') is not None or screenshot_event.get('key_code') is not None:
            action_type = ActionType.KEYBOARD_ACTION
            key = screenshot_event.get('key_char') or screenshot_event.get('key_code', '')
            
            # Determine action based on key
            if key.lower() in ['end', 'pagedown']:
                action = "end"
            else:
                action = "paste"  # Default for keyboard actions
        else:
            # Default action type if not determined from event
            action_type = ActionType.MOUSE_ACTION
            action = "click"
            target = Target(type=ScreenObjectType.NONE)
            
        # Override with explicit values from training data if provided
        if "action_type" in step_data:
            action_type = ActionType(step_data["action_type"])
        if "action" in step_data:
            action = step_data["action"]
            
        # Create appropriate step type based on action_type
        if action_type == ActionType.MOUSE_ACTION:
            if target is None:
                target = Target(type=ScreenObjectType.NONE)
                
            return MouseStep(
                step_id=step_id,
                description=description,
                action=action,
                attention=attention,
                target=target,
                keyboard_shortcut=keyboard_shortcut
            )
        elif action_type == ActionType.KEYBOARD_ACTION:
            return KeyboardActionStep(
                step_id=step_id,
                description=description,
                action=action,
                attention=attention
            )
        else:
            # Default to base Step if action_type is undefined
            return Step(
                step_id=step_id,
                description=description,
                action_type=action_type,
                action=action,
                attention=attention
            )
    
    def _determine_screen_object_type(self, element: ParsedContentResult) -> ScreenObjectType:
        """
        Determine the screen object type based on the element.
        
        Args:
            element: ParsedContentResult to check
            
        Returns:
            ScreenObjectType: Appropriate screen object type
        """
        if element.source == 'box_yolo_content_ocr':
            return ScreenObjectType.BOX_YOLO_CONTENT_OCR
        elif element.source == 'box_yolo_content_yolo':
            return ScreenObjectType.BOX_YOLO_CONTENT_YOLO
        elif element.source == 'box_ocr_content_ocr':
            return ScreenObjectType.BOX_OCR_CONTENT_OCR
        else:
            return ScreenObjectType.NONE
            
    def process_wait_step(self, step_data: Dict[str, Any], steps_map: Dict[int, Step]) -> Step:
        """
        Process a wait step, copying target from referenced step if needed.
        
        Args:
            step_data: Wait step data from training JSON
            steps_map: Dictionary mapping step IDs to processed steps
            
        Returns:
            Step: Processed wait step
        """
        # Extract basic properties
        step_id = int(step_data["step_id"])
        description = str(step_data["description"])
        
        # Get attention or use default
        attention_str = step_data.get("attention")
        if attention_str is None:
            attention_str = self.training_data.get("default_attention", "center")
        attention = Attention(attention_str)
        
        # Get action or use default for wait
        action = step_data.get("action", "none")
        
        # Get target from referenced step if needed
        target = None
        import_target_step = step_data.get("import_target_from_step")
        if import_target_step is not None:
            ref_step_id = int(import_target_step)
            ref_step = steps_map.get(ref_step_id)
            
            if ref_step and isinstance(ref_step, StepWithTarget):
                target = ref_step.target
            else:
                logger.warning(f"Referenced step {ref_step_id} not found or has no target")
        
        if target is None:
            target = Target(type=ScreenObjectType.NONE)
        
        # Create wait step
        return WaitStep(
            step_id=step_id,
            description=description,
            action=action,
            attention=attention,
            target=target
        )
    
    def generate_task_schema(self, training_json_path: str, 
                           screenshot_events_json: str,
                           output_file: Optional[str] = None) -> str:
        """
        Generate a task schema from a training JSON and screenshot events.
        
        Args:
            training_json_path: Path to the training JSON file
            screenshot_events_json: Path to screenshot events JSON file
            output_file: Optional path to save the output JSON
            
        Returns:
            str: Path to the generated task schema JSON file
        """
        # Ensure output directory exists
        output_dir = self._ensure_output_directory(training_json_path)
        
        # Load training JSON and screenshot events
        self.training_data = self.load_training_json(training_json_path)
        omni_results, screenshot_events = run_omniparser_inference(screenshot_events_json)
        
        # Categorize steps into wait steps and non-wait steps
        wait_steps_data = []
        non_wait_steps_data = []
        
        for step_data in self.training_data["steps"]:
            if "action_type" in step_data and step_data["action_type"] == "wait":
                wait_steps_data.append(step_data)
            elif "wait" in step_data.get("description", "").lower() and "action_type" not in step_data:
                wait_steps_data.append(step_data)
            else:
                non_wait_steps_data.append(step_data)
        
        # Validate screenshot event count
        if len(screenshot_events) != len(non_wait_steps_data):
            raise ValueError(f"Number of screenshot events ({len(screenshot_events)}) does not match number of non-wait steps ({len(non_wait_steps_data)})")
        
        # Process non-wait steps first
        processed_steps_map = {}  # Maps step_id to processed Step
        
        for i, step_data in enumerate(non_wait_steps_data):
            screenshot_event = screenshot_events[i]
            omni_result = omni_results.omniparser_result_models[i]
            
            step = self.process_non_wait_step(step_data, screenshot_event, omni_result)
            processed_steps_map[step.step_id] = step
        
        # Process wait steps
        for step_data in wait_steps_data:
            step = self.process_wait_step(step_data, processed_steps_map)
            processed_steps_map[step.step_id] = step
        
        # Combine all steps in original order
        all_steps = []
        for step_data in self.training_data["steps"]:
            step_id = int(step_data["step_id"])
            if step_id in processed_steps_map:
                all_steps.append(processed_steps_map[step_id])
            else:
                logger.warning(f"Step {step_id} was not processed")
        
        # Create Task
        task = Task(
            task=self.training_data["task"],
            description=self.training_data["description"],
            app_name=self.training_data["app_name"],
            app_type=self.training_data["app_type"],
            app_url=self.training_data["app_url"],
            steps=all_steps
        )
        
        # Determine output file path
        if not output_file:
            training_name = os.path.splitext(os.path.basename(training_json_path))[0]
            output_file = os.path.join(output_dir, f"{training_name}_generated.json")
        
        # Save task schema
        with open(output_file, 'w') as f:
            f.write(task.model_dump_json(indent=4))
            
        logger.info(f"Generated task schema saved to {output_file}")
        return output_file

# Add a main function to allow running from command line
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate task schema from training JSON and screenshot events')
    parser.add_argument('training_json', help='Path to training JSON file')
    parser.add_argument('screenshot_events', help='Path to screenshot events JSON file')
    parser.add_argument('--output-dir', '-o', help='Optional output directory')
    parser.add_argument('--output-file', '-f', help='Optional output file path')
    
    args = parser.parse_args()
    
    generator = TaskSchemaGenerator(output_dir=args.output_dir)
    output_file = generator.generate_task_schema(
        args.training_json,
        args.screenshot_events,
        args.output_file
    )
    
    print(f"Generated task schema: {output_file}")

if __name__ == "__main__":
    main()