import os
#  add karna-python-backend to the path
import sys
sys.path.append('C:/Users/Prince/Documents/GitHub/Proejct-Karna/offline-ai-assistant/karna-python-backend')
from task_schema import load_task_schema_from_json, TaskPlanner

def test_task_schema(): 
    # load the task schema from the json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    task_schema = load_task_schema_from_json(os.path.join(current_dir, "chat_with_chatgpt.json"))
    task_planner = TaskPlanner(task_schema)
    # pretty print the task schema
    print(task_planner.task_schema.model_dump_json(indent=4))
test_task_schema()