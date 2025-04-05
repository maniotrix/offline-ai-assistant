import os
import time
#  add karna-python-backend to the path
import sys
sys.path.append('C:/Users/Prince/Documents/GitHub/Proejct-Karna/offline-ai-assistant/karna-python-backend')
from inference.omniparser.task_schema import load_task_schema_from_json, TaskPlanner, MouseStep, WaitStep, KeyboardActionStep, TaskExecutor

import logging
# Configure logging to show messages on console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from clipboard_utils import paste_text_from_clipboard

def test_task_schema(): 
    # load the task schema from the json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    task_schema = load_task_schema_from_json(os.path.join(current_dir, "chat_with_chatgpt.json"))
    task_planner = TaskPlanner(task_schema)
    
    # Pretty print the task schema
    print(task_planner.task_schema.model_dump_json(indent=4))
    
    # Verify step types and targets
    print("\nVerifying step types:")
    for i, step in enumerate(task_schema.steps):
        print(f"Step {step.step_id}: {type(step).__name__}")
        from inference.omniparser.task_schema import StepWithTarget
        if isinstance(step, StepWithTarget):
            print(f"  Has target: {step.target.type}")
    
    # Verify helper methods
    print("\nMouse steps:", len(task_schema.get_mouse_steps()))
    print("Keyboard steps:", len(task_schema.get_keyboard_steps()))
    print("Wait steps:", len(task_schema.get_wait_steps()))
    print("Steps with target:", len(task_schema.get_steps_with_target()))
    
    task_executor = TaskExecutor(task_planner)
    # task_executor.prepare_for_task()
    
    # Question loop
    print("\n===== Question Loop =====")
    print("Type 'exit' or 'quit' to end the conversation")
    
    while True:
        user_question = input("\nEnter your question: ")
        
        if user_question.lower() in ["exit", "quit"]:
            print("Exiting question loop...")
            break
        task_executor.send_text_to_clipboard(user_question)
        print("Executing task...")
        task_executor.execute_task()
        
        result = task_executor.get_clipboard_text()
        print(f"Clipboard text: {result}")
        task_executor.task_log.visualize_task_log()

test_task_schema()