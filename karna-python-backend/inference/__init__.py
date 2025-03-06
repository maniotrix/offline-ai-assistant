from abc import ABC
from datetime import datetime
import logging
from dataclasses import dataclass, field
import uuid
from typing import List
from PIL import Image

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
    
@dataclass
class VisionDetectResultModel:
    """
    Result of inference.
    """
    event_id: str
    project_uuid: str
    command_uuid: str
    timestamp: datetime
    description: str
    original_image_path: str
    original_width: int
    original_height: int
    is_cropped: bool
    merged_ui_icon_bboxes: List[BoundingBox]
    cropped_image: Image.Image | None = None  # Will be None if is_cropped is False
    cropped_width: int | None = None  # Will be None if is_cropped is False
    cropped_height: int | None = None  # Will be None if is_cropped is False
    
    def to_dict(self):
        """
        Convert the inference result model to a dictionary.
        """
        result = {
            "event_id": self.event_id,
            "project_uuid": self.project_uuid,
            "command_uuid": self.command_uuid,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "original_image_path": self.original_image_path,
            "original_width": self.original_width,
            "original_height": self.original_height,
            "is_cropped": self.is_cropped,
            "cropped_image": self.cropped_image,
            "cropped_width": self.cropped_width,
            "cropped_height": self.cropped_height,
            "merged_ui_icon_bboxes": [bbox.to_dict() for bbox in self.merged_ui_icon_bboxes]
        }
        return result
        
@dataclass
class VisionDetectResultModelList:
    """
    List of vision detect result models.
    """
    project_uuid: str
    command_uuid: str
    vision_detect_result_models: List[VisionDetectResultModel]
    
    


class BaseInference(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        pass
    
    
__all__ = ["BoundingBox", "BoundingBoxResult", "VisionDetectResultModel", "VisionDetectResultModelList"]