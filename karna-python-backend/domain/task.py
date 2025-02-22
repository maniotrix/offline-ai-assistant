from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from .action import Action, ActionResult
from .command import Command, CommandResult

class TaskStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class TaskContext:
    """Context for task execution."""
    command_text: str
    command: Optional[Command] = None
    command_result: Optional[CommandResult] = None
    actions: List[Action] = field(default_factory=list)
    action_results: List[ActionResult] = field(default_factory=list)
    status: TaskStatus = TaskStatus.IDLE
    progress: int = 0
    message: str = ""