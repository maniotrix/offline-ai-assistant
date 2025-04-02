import logging
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np
from datetime import datetime, timedelta
from services.screen_capture_service import ScreenshotEvent
from inference.omniparser.util.omniparser import OmniparserResult
from inference.omniparser.omni_helper import OmniParserResultModel
import json
import math

logger = logging.getLogger(__name__)

# Default render bounding box for the viewport
renderBBox = {
    "x": 952,
    "y": 121,
    "width": 960,
    "height": 927
}

"""
Extended Attention Controller
-----------------------------
This file is a copy of the original attention_controller.py with room for extensions
in future phases:

- Phase 2: Generate attention heatmaps based on click density and movement direction
- Phase 3: Implement weighted patch scanning to prioritize OCR/patch match in hot zones
- Phase 4: Add machine learning to adjust weights and improve prediction

These extensions will be implemented without changing the core API of the original
AttentionFieldController, so consumers of this API won't need to change their code.
"""

@dataclass
class AttentionField:
    """Represents a visual attention field with a bounding box"""
    x: int  # Top-left corner x coordinate
    y: int  # Top-left corner y coordinate
    width: int  # Width of the attention field
    height: int  # Height of the attention field
    confidence: float = 1.0  # Confidence score for this attention field
    direction: Optional[str] = None  # Movement direction: 'up', 'down', 'left', 'right'
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get the center coordinates of the attention field"""
        return (self.x + self.width // 2, self.y + self.height // 2)
        
    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Get the bounding box in (x, y, width, height) format"""
        return (self.x, self.y, self.width, self.height)
    
    @property
    def xyxy(self) -> Tuple[int, int, int, int]:
        """Get the bounding box in (x1, y1, x2, y2) format"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if the attention field contains a point"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

@dataclass
class ClickPoint:
    """Represents a click point with timestamp."""
    x: int
    y: int
    timestamp: datetime
    relative_to_field: Optional[Tuple[float, float]] = None  # Position relative to current attention field
    
    @property
    def age(self) -> timedelta:
        """Get the age of the click (time since it happened)."""
        return datetime.now() - self.timestamp

class AttentionFieldController:
    """
    Controller for simulating human visual attention using click history.
    
    This class tracks recent clicks and builds a dynamic attention field (bounding box)
    around them, with the ability to infer movement direction and suggest the next
    area of attention.
    
    Extended version includes placeholders for future enhancements:
    - Heatmap generation based on click density
    - Movement-direction weighted attention
    - Prioritization for OCR/patch scanning
    """
    
    def __init__(self, 
                 expansion_factor: float = 1.5, 
                 click_history_limit: int = 5,
                 screen_width: int = 1920, 
                 screen_height: int = 1080,
                 default_box_size: int = 200):
        """
        Initialize the attention field controller.
        
        Args:
            expansion_factor: Factor to expand the bounding box by
            click_history_limit: Maximum number of clicks to consider in history
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            default_box_size: Default size for the attention field if no omniparser result is available
        """
        self.expansion_factor = expansion_factor
        self.click_history_limit = click_history_limit
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.default_box_size = default_box_size
        
        # Initialize click history and current attention field
        self.click_history: List[ClickPoint] = []
        self.current_attention_field: Optional[AttentionField] = None
        
        # Default to full screen attention field (fallback for cold start)
        self.full_screen_attention = AttentionField(
            x=0, 
            y=0, 
            width=self.screen_width,
            height=self.screen_height,
            confidence=0.5  # Lower confidence for default attention
        )
        
        # Set the render box as the default viewport area
        self.viewport = AttentionField(
            x=renderBBox["x"],
            y=renderBBox["y"],
            width=renderBBox["width"],
            height=renderBBox["height"],
            confidence=0.7  # Higher confidence than full screen
        )
        
        # Base box size is set dynamically with the first click
        self.base_box_size = default_box_size
        self.base_box_initialized = False
        
        # Phase 2: Placeholder for heatmap cache
        self._attention_heatmap = None
        self._heatmap_needs_update = True
    
    def add_click(self, x: int, y: int, timestamp: datetime = None) -> None:
        """
        Add a click to the history and update the attention field.
        
        Args:
            x: X coordinate of the click
            y: Y coordinate of the click
            timestamp: Timestamp of the click, defaults to now if not provided
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Add click to history
        self.click_history.append(ClickPoint(x, y, timestamp))
        
        # Limit history size
        if len(self.click_history) > self.click_history_limit:
            self.click_history = self.click_history[-self.click_history_limit:]
        
        # Update attention field
        self._update_attention_field()
        
        # Phase 2: Mark heatmap as needing an update
        self._heatmap_needs_update = True
        
        logger.debug(f"Added click at ({x}, {y}), updated attention field to {self.current_attention_field.bbox if self.current_attention_field else 'None'}")
    
    def add_click_from_event(self, event: ScreenshotEvent) -> None:
        """
        Add a click from a ScreenshotEvent to the history.
        
        Args:
            event: ScreenshotEvent containing click coordinates
        """
        if event.mouse_x is not None and event.mouse_y is not None:
            self.add_click(event.mouse_x, event.mouse_y, event.timestamp)
    
    def set_base_box_size_from_omniparser(self, omniparser_result: OmniParserResultModel) -> None:
        """
        Set the base box size from the OmniParser result at the first click location.
        This dynamically adjusts the base attention field size based on UI element dimensions.
        
        Args:
            omniparser_result: OmniParserResultModel containing UI element information
        """
        if not self.click_history or self.base_box_initialized:
            return
        
        # Get the first click location
        click_point = self.click_history[0]
        x, y = click_point.x, click_point.y
        
        # Find the UI element that contains this click
        closest_element = None
        min_distance = float('inf')
        closest_element_size = None
        
        for element in omniparser_result.parsed_content_results:
            # Check if click is inside element's bounding box
            bbox = element.bbox
            if len(bbox) == 4:
                # Convert from normalized coordinates if needed
                if max(bbox) <= 1.0:
                    # Normalized coordinates, convert to absolute
                    img_width = omniparser_result.omniparser_result.original_image_width
                    img_height = omniparser_result.omniparser_result.original_image_height
                    x1, y1, x2, y2 = int(bbox[0] * img_width), int(bbox[1] * img_height), \
                                     int(bbox[2] * img_width), int(bbox[3] * img_height)
                else:
                    # Already absolute coordinates
                    x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                
                width = x2 - x1
                height = y2 - y1
                
                # If click is inside this element
                if x1 <= x <= x2 and y1 <= y <= y2:
                    # Calculate distance to center
                    element_center_x = x1 + width // 2
                    element_center_y = y1 + height // 2
                    distance = ((x - element_center_x) ** 2 + (y - element_center_y) ** 2) ** 0.5
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_element = element
                        closest_element_size = (width, height)
        
        # If we found a containing element, use its size to set the base box size
        if closest_element_size:
            avg_dimension = (closest_element_size[0] + closest_element_size[1]) // 2
            # Set base box size to at least the element size but not smaller than default
            self.base_box_size = max(avg_dimension, self.default_box_size)
            self.base_box_initialized = True
            logger.info(f"Set base box size to {self.base_box_size} based on UI element at click location")
        
    def process_click_history(self, events: List[ScreenshotEvent], 
                              omniparser_result: Optional[OmniParserResultModel] = None) -> None:
        """
        Process a list of ScreenshotEvents to build the attention field.
        
        Args:
            events: List of ScreenshotEvents containing click coordinates
            omniparser_result: Optional OmniParserResultModel to set base box size
        """
        # Clear existing history
        self.click_history = []
        
        # Add clicks from events
        for event in events:
            self.add_click_from_event(event)
        
        # Set base box size from omniparser result if available
        if omniparser_result and not self.base_box_initialized:
            self.set_base_box_size_from_omniparser(omniparser_result)
            
    def _infer_movement_direction(self) -> Optional[str]:
        """
        Infer the movement direction from recent click history.
        
        Returns:
            Direction as 'up', 'down', 'left', 'right', or None if can't determine
        """
        if len(self.click_history) < 2:
            return None
        
        # Take the two most recent clicks
        click2 = self.click_history[-1]
        click1 = self.click_history[-2]
        x2, y2 = click2.x, click2.y
        x1, y1 = click1.x, click1.y
        
        # Calculate deltas
        dx = x2 - x1
        dy = y2 - y1
        
        # Determine primary direction based on largest delta
        if abs(dx) > abs(dy):
            # Horizontal movement dominates
            return 'right' if dx > 0 else 'left'
        else:
            # Vertical movement dominates
            return 'down' if dy > 0 else 'up'
    
    def _update_attention_field(self) -> None:
        """
        Update the attention field based on current click history.
        """
        if len(self.click_history) < 1:
            # Cold start: use viewport as attention field
            self.current_attention_field = self.viewport
            return
        elif len(self.click_history) == 1:
            # Single click: center attention field on it
            click_point = self.click_history[0]
            x, y = click_point.x, click_point.y
            half_size = self.base_box_size // 2
            
            self.current_attention_field = AttentionField(
                x=max(0, x - half_size),
                y=max(0, y - half_size),
                width=self.base_box_size,
                height=self.base_box_size,
                confidence=0.8
            )
            return
        
        # Multiple clicks: create bounding box containing all recent clicks
        click_coords = [(click.x, click.y) for click in self.click_history]
        min_x = max(0, min(x for x, _ in click_coords))
        min_y = max(0, min(y for _, y in click_coords))
        max_x = min(self.screen_width, max(x for x, _ in click_coords))
        max_y = min(self.screen_height, max(y for _, y in click_coords))
        
        # Ensure minimum size
        width = max(max_x - min_x, self.base_box_size)
        height = max(max_y - min_y, self.base_box_size)
        
        # Apply expansion factor to create a larger attention field
        center_x = min_x + width // 2
        center_y = min_y + height // 2
        
        expanded_width = int(width * self.expansion_factor)
        expanded_height = int(height * self.expansion_factor)
        
        # Create expanded attention field centered on the click bounding box
        x = max(0, center_x - expanded_width // 2)
        y = max(0, center_y - expanded_height // 2)
        
        # Ensure the field doesn't extend beyond screen bounds
        if x + expanded_width > self.screen_width:
            x = max(0, self.screen_width - expanded_width)
        if y + expanded_height > self.screen_height:
            y = max(0, self.screen_height - expanded_height)
        
        # Infer movement direction
        direction = self._infer_movement_direction()
        
        self.current_attention_field = AttentionField(
            x=x,
            y=y,
            width=expanded_width,
            height=expanded_height,
            confidence=0.9,
            direction=direction
        )
    
    def get_current_attention_field(self) -> AttentionField:
        """
        Get the current attention field.
        
        Returns:
            Current attention field, or fallback if none exists
        """
        if self.current_attention_field:
            return self.current_attention_field
        
        # Fallback to viewport if no attention field exists
        return self.viewport
    
    def predict_next_attention_field(self) -> Optional[AttentionField]:
        """
        Predict the next attention field based on the inferred direction.
        
        Returns:
            Predicted next attention field, or None if direction can't be determined
        """
        if not self.current_attention_field or not self.current_attention_field.direction:
            return None
        
        # Get current field
        current = self.current_attention_field
        direction = current.direction
        
        # Determine shift amount (30% of current dimension)
        x_shift = int(current.width * 0.3)
        y_shift = int(current.height * 0.3)
        
        # Create new attention field shifted in the inferred direction
        if direction == 'right':
            # Shift right
            x = min(self.screen_width - current.width, current.x + x_shift)
            next_field = AttentionField(
                x=x,
                y=current.y,
                width=current.width,
                height=current.height,
                confidence=0.7,  # Lower confidence for prediction
                direction=direction
            )
        elif direction == 'left':
            # Shift left
            x = max(0, current.x - x_shift)
            next_field = AttentionField(
                x=x,
                y=current.y,
                width=current.width,
                height=current.height,
                confidence=0.7,
                direction=direction
            )
        elif direction == 'down':
            # Shift down
            y = min(self.screen_height - current.height, current.y + y_shift)
            next_field = AttentionField(
                x=current.x,
                y=y,
                width=current.width,
                height=current.height,
                confidence=0.7,
                direction=direction
            )
        elif direction == 'up':
            # Shift up
            y = max(0, current.y - y_shift)
            next_field = AttentionField(
                x=current.x,
                y=y,
                width=current.width,
                height=current.height,
                confidence=0.7,
                direction=direction
            )
        else:
            # Unknown direction
            return None
        
        return next_field
    
    def get_attention_context(self) -> Dict:
        """
        Get the current attention context as a dictionary.
        
        Returns:
            Dictionary with current attention field, click history, and predicted next area
        """
        current = self.get_current_attention_field()
        next_field = self.predict_next_attention_field()
        
        return {
            "current_attention": {
                "bbox": current.bbox,
                "confidence": current.confidence,
                "direction": current.direction
            },
            "predicted_next_attention": {
                "bbox": next_field.bbox if next_field else None,
                "confidence": next_field.confidence if next_field else 0.0,
                "direction": next_field.direction if next_field else None
            },
            "click_history_size": len(self.click_history),
            "base_box_size": self.base_box_size,
        }
    
    # Phase 2: Addition - Heatmap generation
    def generate_attention_heatmap(self, resolution: Tuple[int, int] = (100, 100)) -> np.ndarray:
        """
        PHASE 2: Generate a heatmap of attention density based on click history and movement direction.
        
        Args:
            resolution: Resolution of the heatmap as (width_cells, height_cells)
            
        Returns:
            2D numpy array representing the attention heatmap (higher values = more attention)
        """
        # TODO: Implement heatmap generation in Phase 2
        # This is a placeholder for future implementation
        width_res, height_res = resolution
        heatmap = np.zeros((height_res, width_res))
        
        # Return empty heatmap for now - will be implemented in Phase 2
        return heatmap
    
    # Phase 3: Addition - Weighted patch scanning
    def get_patch_scanning_priorities(self, patches: List[Dict]) -> List[float]:
        """
        PHASE 3: Calculate priority scores for patches based on attention heatmap.
        
        Args:
            patches: List of patches with 'bbox' key containing (x, y, width, height)
            
        Returns:
            List of priority scores (higher = higher priority)
        """
        # TODO: Implement weighted patch scanning in Phase 3
        # This is a placeholder for future implementation
        return [1.0] * len(patches)  # Default equal priority for now 

    # ================== Phase 4: Machine Learning Adjustments ==================
    
    def train_from_interaction_history(self, interaction_data: List[Dict]) -> None:
        """
        PHASE 4: Train the attention model from historical interaction data.
        
        This method will be implemented in Phase 4 to allow the attention model
        to learn from past user interactions and improve its predictions.
        
        Args:
            interaction_data: List of interaction data points
        """
        # To be implemented in Phase 4
        logger.info("ML training not yet implemented (Phase 4)")
        pass
    
    def save_model(self, file_path: str) -> None:
        """
        PHASE 4: Save the trained attention model to a file.
        
        Args:
            file_path: Path to save the model
        """
        # To be implemented in Phase 4
        logger.info(f"Model saving not yet implemented (Phase 4)")
        pass
    
    def load_model(self, file_path: str) -> None:
        """
        PHASE 4: Load a trained attention model from a file.
        
        Args:
            file_path: Path to load the model from
        """
        # To be implemented in Phase 4
        logger.info(f"Model loading not yet implemented (Phase 4)")
        pass 