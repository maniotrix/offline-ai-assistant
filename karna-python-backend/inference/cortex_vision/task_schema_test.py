import os
import time
#  add karna-python-backend to the path
import sys
import datetime
import io
import contextlib
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

sys.path.append('C:/Users/Prince/Documents/GitHub/Proejct-Karna/offline-ai-assistant/karna-python-backend')
from inference.cortex_vision.task_schema import load_task_schema_from_json, TaskPlanner, MouseStep, WaitStep, KeyboardActionStep, TaskExecutor

import logging

# Configure logging to suppress all logs except critical errors
logging.basicConfig(
    level=logging.CRITICAL,  # Only show critical errors
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Disable all loggers from imported modules
for name in logging.root.manager.loggerDict:
    logging.getLogger(name).setLevel(logging.CRITICAL)
    logging.getLogger(name).propagate = False

# Suppress more specific loggers that might be created later
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("timm").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# Only enable our own logger if needed
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

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

# Original print function, so we can use it in our controlled contexts
original_print = print

# Override print for the whole module to make sure our prints still work
def karna_print(*args, **kwargs):
    # Our custom print function that will be used throughout the module
    original_print(*args, **kwargs)

# Context manager to suppress stdout/stderr temporarily
@contextlib.contextmanager
def suppress_output():
    # Save the original stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    # Use StringIO to capture output
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        # Restore stdout/stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def test_task_schema(): 
    # load the task schema from the json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    karna_print("Loading chat with chatgpt task schema...")
    # Suppress output during initialization
    with suppress_output():
        task_schema = load_task_schema_from_json(os.path.join(current_dir, "chat_with_chatgpt.json"))
        task_planner = TaskPlanner(task_schema)
    
    # Only display the main interface, skip all the technical details
    with suppress_output():
        task_executor = TaskExecutor(task_planner)
    # task_executor.prepare_for_task()
    
    # Question loop interface
    karna_print("\n" + Colors.BOLD + Colors.HEADER + "╔═══════════════════════════════════════════════════════════╗" + Colors.ENDC)
    karna_print(Colors.BOLD + Colors.HEADER + "║                   KARNA CHATGPT INTERFACE                   ║" + Colors.ENDC)
    karna_print(Colors.BOLD + Colors.HEADER + "╚═══════════════════════════════════════════════════════════╝" + Colors.ENDC)
    karna_print(Colors.BOLD + Colors.YELLOW + "\n• Type " + Colors.CYAN + "'exit'" + Colors.YELLOW + " or " + Colors.CYAN + "'quit'" + Colors.YELLOW + " to end the conversation" + Colors.ENDC)
    
    question_count = 0
    use_as_vlm = True
    show_tasks_viz = True
    directory_path = os.path.join(current_dir, "test_chatgpt_upload_dir")
    
    while True:
        task_executor.task_log.reset_task_log()
        karna_print(Colors.BOLD + Colors.GREEN + "\n╭─────────────────────────────────────────────────────────────╮" + Colors.ENDC)
        user_question = input(Colors.BOLD + Colors.GREEN + "│ " + Colors.ENDC + Colors.BOLD + "Enter your question: " + Colors.ENDC)
        karna_print(Colors.BOLD + Colors.GREEN + "╰─────────────────────────────────────────────────────────────╯" + Colors.ENDC)
        
        if user_question.lower() in ["exit", "quit"]:
            karna_print(Colors.BOLD + Colors.YELLOW + "\nExiting conversation. Thank you for using Karna!" + Colors.ENDC)
            break
        
        question_count += 1
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with suppress_output():
            if question_count == 1 and use_as_vlm:
                # only for the first question, we will upload the files to chatgpt
                task_executor.set_clipboard(user_question, directory_path)
                karna_print(Colors.BOLD + Colors.UNDERLINE + f"User question: {user_question} and directory path: {directory_path}" + Colors.ENDC)
            else:
                # for all other questions, we will just send the question to chatgpt
                task_executor.set_clipboard(user_question)
            # task_executor.set_clipboard(user_question)    
            

        karna_print(Colors.CYAN + "\nAsking and Waiting for ChatGPT..." + Colors.ENDC)
        
        # Record start time
        start_time = time.time()
        
        # Suppress any print statements during task execution
        with suppress_output():
            task_executor.execute_task()
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        with suppress_output():
            result = task_executor.get_clipboard_text()
        
        karna_print("\n" + Colors.BOLD + Colors.BLUE + "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓" + Colors.ENDC)
        karna_print(Colors.BOLD + Colors.BLUE + "┃ " + Colors.YELLOW + f"CONVERSATION #{question_count} - {timestamp}" + Colors.BLUE + " ┃" + Colors.ENDC)
        karna_print(Colors.BOLD + Colors.BLUE + "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛" + Colors.ENDC)
        
        karna_print(Colors.BOLD + "\n🙋 " + Colors.GREEN + "YOU ASKED:" + Colors.ENDC)
        karna_print(f"{user_question}\n")
        
        karna_print(Colors.BOLD + "🤖 " + Colors.CYAN + f"CHATGPT RESPONSE (took {elapsed_time:.2f}s):" + Colors.ENDC)
        karna_print(f"{result}")
        
        karna_print(Colors.BOLD + Colors.BLUE + "─────────────────────────────────────────────────────────────" + Colors.ENDC)
        task_executor.chrome_robot.press_alt_key("tab")
        if question_count == 1 and show_tasks_viz:
            task_executor.task_log.visualize_task_log()
            break
        #task_executor.task_log.visualize_task_log()

if __name__ == "__main__":
    # Override standard print globally
    print = karna_print
    
    # Redirect stderr and stdout to devnull for any stray prints that bypass our controls
    with open(os.devnull, 'w') as devnull:
        # For the execution of the script, redirect all standard output
        # Only temporarily swap these for initialization 
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        
        try:
            # Reset for our actual code execution so our prints work
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            test_task_schema()
        except Exception as e:
            # Make sure to restore stdout/stderr even on errors
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            karna_print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr