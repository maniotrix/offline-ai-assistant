from attr import dataclass

@dataclass
class StatusContext:
    """Context for status updates."""

    language: str = ""
    command: str = ""