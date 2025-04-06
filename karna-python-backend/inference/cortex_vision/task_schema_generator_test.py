import os
import sys
import logging
from datetime import datetime

# Add the root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from inference.cortex_vision.task_schema_generator import TaskSchemaGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def example_usage():
    """
    Demonstrates how to use the TaskSchemaGenerator in a real-world scenario.
    
    Workflow:
    1. Record user interaction with an application using ScreenCaptureService
    2. Export the screenshot events to a JSON file
    3. Create a training JSON file with steps
    4. Use TaskSchemaGenerator to create a fully-specified task schema
    """
    # Step 1: Assume we've already recorded the user interactions using ScreenCaptureService
    # This would typically be done via your application's UI
    
    # Step 2: Get paths to the exported screenshot events JSON and training JSON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_events_json = os.path.join(current_dir, "sample_chatgpt_screenshots_events.json")
    training_json_path = os.path.join(current_dir, "chat_with_chatgpt_steps_train.json")
    
    # Optional: Define an output directory (will be created if doesn't exist)
    output_dir = os.path.join(current_dir, f"generated_task_schema_sample_chatgpt")
    
    # Step 3: Create a TaskSchemaGenerator instance
    generator = TaskSchemaGenerator(output_dir=output_dir)
    
    # Step 4: Generate the task schema
    try:
        output_file = generator.generate_task_schema(
            training_json_path=training_json_path,
            screenshot_events_json=screenshot_events_json
        )
        print(f"Successfully generated task schema: {output_file}")
        
        # Step 5: The generated schema can now be used with TaskExecutor
        print(f"Task schema is ready for use with TaskExecutor.")
        print(f"Extracted UI element patches are saved in: {os.path.join(output_dir, 'patches')}")
        
    except Exception as e:
        print(f"Error generating task schema: {str(e)}")

if __name__ == "__main__":
    example_usage()
