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