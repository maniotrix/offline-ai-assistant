import os
import time
#  add karna-python-backend to the path
import sys
import datetime
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

# ANSI color codes for console formatting
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    print("\n" + Colors.BOLD + Colors.HEADER + "╔═══════════════════════════════════════════════════════════╗" + Colors.ENDC)
    print(Colors.BOLD + Colors.HEADER + "║                   KARNA CHATGPT INTERFACE                   ║" + Colors.ENDC)
    print(Colors.BOLD + Colors.HEADER + "╚═══════════════════════════════════════════════════════════╝" + Colors.ENDC)
    print(Colors.BOLD + Colors.YELLOW + "\n• Type " + Colors.CYAN + "'exit'" + Colors.YELLOW + " or " + Colors.CYAN + "'quit'" + Colors.YELLOW + " to end the conversation" + Colors.ENDC)
    
    question_count = 0
    
    while True:
        print(Colors.BOLD + Colors.GREEN + "\n╭─────────────────────────────────────────────────────────────╮" + Colors.ENDC)
        user_question = input(Colors.BOLD + Colors.GREEN + "│ " + Colors.ENDC + Colors.BOLD + "Enter your question: " + Colors.ENDC)
        print(Colors.BOLD + Colors.GREEN + "╰─────────────────────────────────────────────────────────────╯" + Colors.ENDC)
        
        if user_question.lower() in ["exit", "quit"]:
            print(Colors.BOLD + Colors.YELLOW + "\nExiting conversation. Thank you for using Karna!" + Colors.ENDC)
            break
        
        question_count += 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        task_executor.send_text_to_clipboard(user_question)
        print(Colors.CYAN + "\nConnecting to ChatGPT..." + Colors.ENDC)
        print("Executing task...")
        task_executor.execute_task()
        
        result = task_executor.get_clipboard_text()
        
        print("\n" + Colors.BOLD + Colors.BLUE + "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓" + Colors.ENDC)
        print(Colors.BOLD + Colors.BLUE + "┃ " + Colors.YELLOW + f"CONVERSATION #{question_count} - {timestamp}" + Colors.BLUE + " ┃" + Colors.ENDC)
        print(Colors.BOLD + Colors.BLUE + "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛" + Colors.ENDC)
        
        print(Colors.BOLD + "\n🙋 " + Colors.GREEN + "YOU ASKED:" + Colors.ENDC)
        print(f"{user_question}\n")
        
        print(Colors.BOLD + "🤖 " + Colors.CYAN + "CHATGPT RESPONSE:" + Colors.ENDC)
        print(f"{result}")
        
        print(Colors.BOLD + Colors.BLUE + "─────────────────────────────────────────────────────────────" + Colors.ENDC)
        #task_executor.task_log.visualize_task_log()

test_task_schema()