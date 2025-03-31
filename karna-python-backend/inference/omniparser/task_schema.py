from typing import List, Optional
from pydantic import BaseModel


class Step(BaseModel):
    action_type: str
    action: str
    target_type: Optional[str] = None
    is_target_repeated: Optional[bool] = False
    target_repeated_layout_type: Optional[str] = None
    is_target_repeated_layout_index_fixed: Optional[bool] = None
    target_repeated_layout_index: Optional[int] = None


class Task(BaseModel):
    task: str
    description: str
    app_name: str
    app_type: str
    app_url: str
    steps: List[Step]
    
def load_task_schema_from_json(json_file_path: str):
    with open(json_file_path, 'r') as file:
        return Task.model_validate_json(file.read())

class TaskPlanner():
    task_schema: Task
    def __init__(self, task_schema: Task):
        self.task_schema = task_schema

if __name__ == "__main__":
    def test_task_schema(): 
        # load the task schema from the json file
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        task_schema = load_task_schema_from_json(os.path.join(current_dir, "chat_with_chatgpt.json"))
        task_planner = TaskPlanner(task_schema)
        # pretty print the task schema
        print(task_planner.task_schema.model_dump_json(indent=4))
    test_task_schema()


