from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from .action import Action

@dataclass
class Intent:
    """Intent domain model representing predicted actions for a command."""
    command_uuid: UUID
    actions: List[Action] = field(default_factory=list)
    uuid: UUID = uuid4()
    created_at: datetime = datetime.now()

@dataclass
class IntentPrediction:
    """Result of intent prediction."""
    intent: Intent
    confidence: float
    metadata: dict = field(default_factory=dict)