from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID, uuid4

@dataclass
class ActionCoordinates:
    """Coordinates for an action on screen."""
    x: int
    y: int

@dataclass
class Action:
    """Action domain model representing a single action to be executed."""
    type: str
    coordinates: ActionCoordinates
    text: Optional[str] = None
    uuid: UUID = uuid4()

@dataclass
class ActionResult:
    """Result of an action execution."""
    action: Action
    success: bool
    message: Optional[str] = None