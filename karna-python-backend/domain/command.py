from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

@dataclass
class Command:
    """Command domain model representing a user command."""
    name: str
    domain: str
    uuid: UUID = uuid4()
    is_in_cache: bool = False
    created_at: datetime = datetime.now()

@dataclass
class CommandResult:
    """Result of command processing."""
    command: Command
    success: bool
    message: Optional[str] = None