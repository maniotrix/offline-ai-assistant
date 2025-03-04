from abc import ABC
import logging
from dataclasses import dataclass, field
import uuid
from typing import List

@dataclass
class BoundingBox:
    """
    Bounding box class.
    """
    x: int
    y: int
    width: int
    height: int
    class_name: str
    confidence: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Default to a new UUID
    
    def to_dict(self):
        """
        Convert the bounding box to a dictionary.
        Uses 'class' instead of 'class_name' in the output dictionary.
        """
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "class": self.class_name,  # Use 'class' instead of 'class_name'
            "confidence": self.confidence,
            "id": self.id
        }

@dataclass
class BoundingBoxResult:
    """
    Result of bounding box detection.
    """
    image_path: str
    original_width: int
    original_height: int
    bounding_boxes: List[BoundingBox]

class BaseInference(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        pass