import logging
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np
import math
from datetime import datetime
from services.screen_capture_service import ScreenshotEvent
from inference.omniparser.util.omniparser import OmniparserResult
from inference.omniparser.omni_helper import OmniParserResultModel

logger = logging.getLogger(__name__)

# Default render bounding box for the viewport
renderBBox = {
    "x": 952,
    "y": 121,
    "width": 960,
    "height": 927
}

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

class AttentionFieldController:
    """
    Controller for simulating human visual attention using click history.
    
    This class tracks recent clicks and builds a dynamic attention field (bounding box)
    around them, with the ability to infer movement direction and suggest the next
    area of attention.
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
        self.click_history: List[Tuple[int, int, datetime]] = []
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
        self.click_history.append((x, y, timestamp))
        
        # Limit history size
        if len(self.click_history) > self.click_history_limit:
            self.click_history = self.click_history[-self.click_history_limit:]
        
        # Update attention field
        self._update_attention_field()
        
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
        x, y, _ = self.click_history[0]
        
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
        Infer the movement direction from the entire click history using a weighted trend analysis.
        
        This method analyzes all available clicks in the history (up to click_history_limit),
        giving more weight to recent movements. It calculates a weighted average direction
        vector and converts it to one of the four cardinal directions.
        
        Returns:
            Direction as 'up', 'down', 'left', 'right', or None if can't determine
        """
        # Need at least 2 clicks to determine a direction
        if len(self.click_history) < 2:
            return None
        
        # Initialize weighted direction accumulators
        weighted_dx = 0.0
        weighted_dy = 0.0
        total_weight = 0.0
        
        # Number of movement vectors (pairs of clicks)
        num_pairs = len(self.click_history) - 1
        
        # Process each consecutive pair of clicks
        for i in range(num_pairs):
            # Get current and next click coordinates (reversed order in list indexing)
            # More recent clicks are at the end of the list
            current_idx = -(i + 2)  # Second-to-last, third-to-last, etc.
            next_idx = -(i + 1)     # Last, second-to-last, etc.
            
            # Get the coordinates
            x1, y1, _ = self.click_history[current_idx]
            x2, y2, _ = self.click_history[next_idx]
            
            # Calculate movement vector
            dx = x2 - x1
            dy = y2 - y1
            
            # Calculate weight based on recency
            # More recent pairs get higher weights using power-based decay
            # i=0 is the most recent pair
            pair_index = num_pairs - i  # Convert to 1-based index (most recent = highest)
            weight = (pair_index / num_pairs) ** 1.5  # Power factor gives more emphasis to recent pairs
            
            # Accumulate weighted vectors
            weighted_dx += dx * weight
            weighted_dy += dy * weight
            total_weight += weight
        
        # Avoid division by zero
        if total_weight == 0:
            return None
        
        # Compute average direction vector
        avg_dx = weighted_dx / total_weight
        avg_dy = weighted_dy / total_weight
        
        # Calculate vector magnitude
        magnitude = math.sqrt(avg_dx**2 + avg_dy**2)
        
        # If the movement is too small, consider it no meaningful direction
        MIN_MAGNITUDE = 5.0  # Minimum pixels of movement to consider significant
        if magnitude < MIN_MAGNITUDE:
            return None
        
        # Calculate angle in degrees
        # Note: We negate dy because screen Y-axis increases downward
        angle_rad = math.atan2(-avg_dy, avg_dx)
        angle_deg = math.degrees(angle_rad)
        
        # Normalize to 0-360° range
        if angle_deg < 0:
            angle_deg += 360
        
        # Convert angle to cardinal direction
        if 45 <= angle_deg < 135:
            return 'up'
        elif 135 <= angle_deg < 225:
            return 'left'
        elif 225 <= angle_deg < 315:
            return 'down'
        else:  # 315 <= angle_deg < 360 or 0 <= angle_deg < 45
            return 'right'
    
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
            x, y, _ = self.click_history[0]
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
        click_coords = [(x, y) for x, y, _ in self.click_history]
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





