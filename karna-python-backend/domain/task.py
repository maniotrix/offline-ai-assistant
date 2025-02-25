from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import copy
from .action import Action, ActionResult
from .command import Command, CommandResult

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class TaskContext:
    """Context for task execution."""
    command_text: str
    command: Optional[Command] = None
    command_result: Optional[CommandResult] = None
    actions: List[Action] = field(default_factory=list)
    action_results: List[ActionResult] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    message: str = ""
    needs_training: bool = False