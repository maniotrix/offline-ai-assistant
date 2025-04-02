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
    "x": 0,
    "y": 121,
    "width": 1920,
    "height": 919
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
    around them, with the ability to infer movement direction based on the trend
    of the center of the core attention area, and suggest the next area of attention.
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
            click_history_limit: Maximum number of clicks/centers to consider in history
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            default_box_size: Default size for the attention field if no omniparser result is available
        """
        self.expansion_factor = expansion_factor
        self.click_history_limit = click_history_limit
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.default_box_size = default_box_size
        
        # Initialize click history, center history, and current attention field
        self.click_history: List[Tuple[int, int, datetime]] = []
        self.center_history: List[Tuple[int, int]] = [] # History of core bounding box centers
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
        
        logger.info(f"AttentionFieldController initialized with: expansion_factor={expansion_factor}, "
                   f"click_history_limit={click_history_limit}, screen_width={screen_width}, "
                   f"screen_height={screen_height}, default_box_size={default_box_size}")
        logger.debug(f"Default viewport set to: {self.viewport.bbox}")
    
    def add_click(self, x: int, y: int, timestamp: datetime = None) -> None:
        """
        Add a click to the history and update the attention field and center history.
        
        Args:
            x: X coordinate of the click
            y: Y coordinate of the click
            timestamp: Timestamp of the click, defaults to now if not provided
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        logger.debug(f"Adding click at ({x}, {y}) with timestamp {timestamp}")
        
        # Add click to history
        self.click_history.append((x, y, timestamp))
        
        # Limit history size for both clicks and centers
        if len(self.click_history) > self.click_history_limit:
            removed_click = self.click_history.pop(0)
            if self.center_history: # Remove corresponding center if it exists
                removed_center = self.center_history.pop(0)
                logger.debug(f"History limit reached. Removed oldest click at ({removed_click[0]}, {removed_click[1]}) and center {removed_center}")
            else:
                logger.debug(f"History limit reached. Removed oldest click at ({removed_click[0]}, {removed_click[1]})")
        
        # Update attention field (which also updates center history)
        self._update_attention_field()
        
        logger.debug(f"Added click at ({x}, {y}), updated attention field to {self.current_attention_field.bbox if self.current_attention_field else 'None'}")
        logger.debug(f"Center history size: {len(self.center_history)}")
    
    def add_click_from_event(self, event: ScreenshotEvent) -> None:
        """
        Add a click from a ScreenshotEvent to the history.
        
        Args:
            event: ScreenshotEvent containing click coordinates
        """
        if event.mouse_x is not None and event.mouse_y is not None:
            logger.debug(f"Adding click from event: mouse_x={event.mouse_x}, mouse_y={event.mouse_y}, timestamp={event.timestamp}")
            self.add_click(event.mouse_x, event.mouse_y, event.timestamp)
        else:
            logger.warning(f"Skipping event with missing mouse coordinates: {event}")
    
    def set_base_box_size_from_omniparser(self, omniparser_result: OmniParserResultModel) -> None:
        """
        Set the base box size from the OmniParser result at the first click location.
        This dynamically adjusts the base attention field size based on UI element dimensions.
        
        Args:
            omniparser_result: OmniParserResultModel containing UI element information
        """
        if not self.click_history:
            logger.warning("Cannot set base box size: No clicks in history")
            return
        
        if self.base_box_initialized:
            logger.debug("Base box size already initialized, skipping")
            return
        
        # Get the first click location
        x, y, _ = self.click_history[0]
        logger.debug(f"Setting base box size from omniparser result for first click at ({x}, {y})")
        
        # Find the UI element that contains this click
        closest_element = None
        min_distance = float('inf')
        closest_element_size = None
        
        logger.debug(f"Searching through {len(omniparser_result.parsed_content_results)} UI elements")
        
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
                    # logger.debug(f"Converting normalized coordinates to absolute: {bbox} -> ({x1}, {y1}, {x2}, {y2})") # Too verbose
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
                    
                    # logger.debug(f"Click is inside element: ({x1}, {y1}, {x2}, {y2}), distance to center: {distance}") # Too verbose
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_element = element
                        closest_element_size = (width, height)
                        # logger.debug(f"New closest element found: size={closest_element_size}, distance={min_distance}") # Too verbose
        
        # If we found a containing element, use its size to set the base box size
        if closest_element_size:
            avg_dimension = (closest_element_size[0] + closest_element_size[1]) // 2
            # Set base box size to at least the element size but not smaller than default
            old_size = self.base_box_size
            self.base_box_size = max(avg_dimension, self.default_box_size)
            self.base_box_initialized = True
            logger.info(f"Updated base box size from {old_size} to {self.base_box_size} based on UI element at click location (element size: {closest_element_size})")
        else:
            logger.warning(f"No containing UI element found for click at ({x}, {y}), keeping default box size: {self.base_box_size}")
        
    def process_click_history(self, events: List[ScreenshotEvent], 
                              omniparser_result: Optional[OmniParserResultModel] = None) -> None:
        """
        Process a list of ScreenshotEvents to build the attention field and center history.
        
        Args:
            events: List of ScreenshotEvents containing click coordinates
            omniparser_result: Optional OmniParserResultModel to set base box size
        """
        logger.info(f"Processing {len(events)} screenshot events with omniparser_result available: {omniparser_result is not None}")
        
        # Clear existing histories
        old_click_history_size = len(self.click_history)
        old_center_history_size = len(self.center_history)
        self.click_history = []
        self.center_history = []
        logger.debug(f"Cleared existing click history (size {old_click_history_size}) and center history (size {old_center_history_size})")
        
        # Add clicks from events (this will populate both histories)
        for i, event in enumerate(events):
            logger.debug(f"Processing event {i+1}/{len(events)}: {event}")
            self.add_click_from_event(event)
        
        # Set base box size from omniparser result if available (needs at least one click)
        if omniparser_result and self.click_history and not self.base_box_initialized:
            logger.debug("Setting base box size from omniparser result")
            self.set_base_box_size_from_omniparser(omniparser_result)
            
    def _infer_movement_direction(self) -> Optional[str]:
        """
        Infer the movement direction using a hybrid approach:
        1. Check the direction of the most recent center movement.
           If it's significant and strongly axial (horizontal/vertical), use that direction.
        2. Otherwise, fall back to a weighted trend analysis of the entire center history.

        This prioritizes responsiveness to clear recent shifts while smoothing ambiguous ones.

        Returns:
            Direction as 'up', 'down', 'left', 'right', or None if can't determine
        """
        # Need at least 2 centers to determine any direction
        if len(self.center_history) < 2:
            logger.debug("Cannot infer movement direction: Need at least 2 centers in history")
            return None

        # --- Hybrid Approach: Check last movement first ---
        cx_n_minus_1, cy_n_minus_1 = self.center_history[-2]
        cx_n, cy_n = self.center_history[-1]

        dx_last = cx_n - cx_n_minus_1
        dy_last = cy_n - cy_n_minus_1
        mag_last = math.sqrt(dx_last**2 + dy_last**2)

        logger.debug(f"Last center movement: ({cx_n_minus_1},{cy_n_minus_1}) -> ({cx_n},{cy_n}), delta=({dx_last},{dy_last}), mag={mag_last:.2f}")

        MIN_MAGNITUDE = 5.0  # Minimum pixels of movement to consider significant
        DOMINANCE_RATIO = 3.0 # How much larger one axis delta must be than the other

        if mag_last >= MIN_MAGNITUDE:
            # Check for dominant axial movement
            if abs(dy_last) > DOMINANCE_RATIO * abs(dx_last):
                direction = 'up' if dy_last < 0 else 'down'
                logger.info(f"Inferred direction from dominant last vertical movement: {direction}")
                return direction
            elif abs(dx_last) > DOMINANCE_RATIO * abs(dy_last):
                direction = 'left' if dx_last < 0 else 'right'
                logger.info(f"Inferred direction from dominant last horizontal movement: {direction}")
                return direction
            else:
                logger.debug("Last movement is significant but not strongly axial, proceeding to weighted average.")
        else:
            logger.debug(f"Last movement magnitude {mag_last:.2f} < {MIN_MAGNITUDE}, proceeding to weighted average.")

        # --- Fallback: Weighted Average Trend Analysis ---
        logger.debug(f"Inferring movement direction using weighted average of {len(self.center_history)} centers")

        # Initialize weighted direction accumulators
        weighted_dx = 0.0
        weighted_dy = 0.0
        total_weight = 0.0

        # Number of movement vectors (pairs of centers)
        num_pairs = len(self.center_history) - 1

        # Process each consecutive pair of centers
        for i in range(num_pairs):
            # Get current and next center coordinates
            cx1, cy1 = self.center_history[i]
            cx2, cy2 = self.center_history[i+1]

            # Calculate movement vector
            dx = cx2 - cx1
            dy = cy2 - cy1

            # Calculate weight based on recency (1-based index, more recent = higher index)
            pair_index = i + 1
            # Using power factor 1.5 as before for the weighted average part
            weight = (pair_index / num_pairs) ** 1.5

            # Accumulate weighted vectors
            weighted_dx += dx * weight
            weighted_dy += dy * weight
            total_weight += weight

            # logger.debug(f"Center movement vector {i+1}/{num_pairs}: ({cx1},{cy1}) -> ({cx2},{cy2}), "
            #            f"delta=({dx},{dy}), weight={weight:.3f}") # Can be verbose

        # Avoid division by zero (shouldn't happen if num_pairs >= 1)
        if total_weight == 0:
            logger.warning("Total weight is zero in weighted average, cannot determine direction")
            return None

        # Compute average direction vector
        avg_dx = weighted_dx / total_weight
        avg_dy = weighted_dy / total_weight

        # Calculate vector magnitude
        magnitude = math.sqrt(avg_dx**2 + avg_dy**2)

        logger.debug(f"Weighted average center movement vector: ({avg_dx:.2f}, {avg_dy:.2f}), magnitude: {magnitude:.2f}")

        # If the average movement is too small, consider it no meaningful direction
        if magnitude < MIN_MAGNITUDE:
            logger.debug(f"Weighted average magnitude {magnitude:.2f} < {MIN_MAGNITUDE}, considered insignificant")
            return None

        # Calculate angle in degrees
        # Note: We negate dy because screen Y-axis increases downward
        angle_rad = math.atan2(-avg_dy, avg_dx)
        angle_deg = math.degrees(angle_rad)

        # Normalize to 0-360° range
        if angle_deg < 0:
            angle_deg += 360

        logger.debug(f"Weighted average center movement angle: {angle_deg:.2f}°")

        # Convert angle to cardinal direction
        if 45 <= angle_deg < 135:
            direction = 'up'
        elif 135 <= angle_deg < 225:
            direction = 'left'
        elif 225 <= angle_deg < 315:
            direction = 'down'
        else:  # 315 <= angle_deg < 360 or 0 <= angle_deg < 45
            direction = 'right'

        logger.info(f"Inferred movement direction from weighted average: {direction} (angle: {angle_deg:.2f}°)")
        return direction
    
    def _update_attention_field(self) -> None:
        """
        Update the center history and the current attention field based on click history.
        Calculates the core bounding box center, stores it, then computes the
        expanded attention field for display/output.
        """
        logger.debug(f"Updating attention field and center history based on {len(self.click_history)} clicks")

        if len(self.click_history) < 1:
            # Cold start: use viewport as attention field, no center to add
            logger.debug("Cold start: using viewport as attention field. No center added.")
            self.current_attention_field = self.viewport
            # Ensure center history is also empty on cold start or reset
            if self.center_history:
                 logger.warning("Clearing non-empty center history during cold start update.")
                 self.center_history = []
            return

        # Get latest click coordinates for reference
        last_click_x, last_click_y, _ = self.click_history[-1]
        core_center_x, core_center_y = last_click_x, last_click_y # Default for single click
        # Initialize expanded dimensions here
        expanded_width = self.base_box_size
        expanded_height = self.base_box_size

        if len(self.click_history) == 1:
            # Single click: core center is the click itself.
            # Store the first center. Need to manage the history list directly here.
            if len(self.center_history) == 0:
                 self.center_history.append((core_center_x, core_center_y))
                 logger.debug(f"Added first center to history: ({core_center_x}, {core_center_y})")
            elif len(self.center_history) == 1:
                 # If add_click logic already added one, update it (e.g. during process_click_history loop)
                 self.center_history[-1] = (core_center_x, core_center_y)
                 logger.debug(f"Updated last center in history: ({core_center_x}, {core_center_y})")
            else:
                 # This case might occur if history limit logic runs before update
                 logger.warning(f"Center history size ({len(self.center_history)}) unexpected for single click.")
                 # Append anyway, history limit in add_click should handle it
                 self.center_history.append((core_center_x, core_center_y))


            # For the display/output field, center a base-sized box on the click
            # expanded_width and expanded_height already initialized to base_box_size
            logger.debug(f"Single click at ({last_click_x}, {last_click_y}): core center added. Using base size for attention field.")

        elif len(self.click_history) > 1:
            # Multiple clicks: create core bounding box first
            click_coords = [(x, y) for x, y, _ in self.click_history]
            min_x = max(0, min(x for x, _ in click_coords))
            min_y = max(0, min(y for _, y in click_coords))
            max_x = min(self.screen_width, max(x for x, _ in click_coords))
            max_y = min(self.screen_height, max(y for _, y in click_coords))

            logger.debug(f"Multiple clicks raw bounding box: ({min_x}, {min_y}, {max_x}, {max_y})")

            # Calculate the center of the *actual* click area, not clamped by base_box_size yet
            actual_width = max_x - min_x
            actual_height = max_y - min_y
            core_center_x = min_x + actual_width // 2
            core_center_y = min_y + actual_height // 2

            # Store the calculated core center. Need to manage history list.
            # If process_click_history called add_click multiple times, the list might grow
            # We want one center per click event added.
            # Check if the number of centers matches clicks. If not, likely processing history.
            if len(self.center_history) < len(self.click_history):
                self.center_history.append((core_center_x, core_center_y))
                logger.debug(f"Added new core center to history: ({core_center_x}, {core_center_y})")
            elif len(self.center_history) == len(self.click_history):
                # If lengths match, update the last one (consistent with single click logic)
                self.center_history[-1] = (core_center_x, core_center_y)
                logger.debug(f"Updated last core center in history: ({core_center_x}, {core_center_y})")
            else:
                 logger.warning(f"Center history size ({len(self.center_history)}) greater than click history ({len(self.click_history)})")
                 # Trim center history to match click history? Or append? Let's try appending and let limit handle it.
                 self.center_history.append((core_center_x, core_center_y))

            # Now calculate dimensions for the *expanded* box, ensuring minimum size
            core_width = max(actual_width, self.base_box_size)
            core_height = max(actual_height, self.base_box_size)

            # Apply expansion factor - update the initialized variables
            expanded_width = int(core_width * self.expansion_factor)
            expanded_height = int(core_height * self.expansion_factor)

            logger.debug(f"Core dimensions (min {self.base_box_size}): {core_width}x{core_height}, core center: ({core_center_x}, {core_center_y})")
            logger.debug(f"Expanded dimensions: {expanded_width}x{expanded_height} (factor: {self.expansion_factor})")


        # Create the final expanded attention field, centered on the *core* center
        # (Only if we have clicks, otherwise handled by cold start)
        # expanded_width and expanded_height are now guaranteed to be defined
        if len(self.click_history) >= 1:
            x = max(0, core_center_x - expanded_width // 2)
            y = max(0, core_center_y - expanded_height // 2)

            # Ensure the field doesn't extend beyond screen bounds (adjust top-left corner)
            if x + expanded_width > self.screen_width:
                original_x = x
                x = max(0, self.screen_width - expanded_width)
                logger.debug(f"Adjusted x from {original_x} to {x} to keep within screen bounds")

            if y + expanded_height > self.screen_height:
                original_y = y
                y = max(0, self.screen_height - expanded_height)
                logger.debug(f"Adjusted y from {original_y} to {y} to keep within screen bounds")

            # Infer movement direction using the center history
            direction = self._infer_movement_direction()
            confidence = 0.9 if len(self.click_history) > 1 else 0.8 # Slightly lower confidence for first click

            self.current_attention_field = AttentionField(
                x=x,
                y=y,
                width=expanded_width,
                height=expanded_height,
                confidence=confidence,
                direction=direction
            )

            logger.info(f"Updated attention field: {self.current_attention_field.bbox}, "
                      f"center: {self.current_attention_field.center}, "
                      f"direction: {direction}, confidence: {confidence:.1f}")
    
    def get_current_attention_field(self) -> AttentionField:
        """
        Get the current attention field.
        
        Returns:
            Current attention field, or fallback if none exists
        """
        if self.current_attention_field:
            # logger.debug(f"Returning current attention field: {self.current_attention_field.bbox}") # Too verbose
            return self.current_attention_field
        
        # Fallback to viewport if no attention field exists
        logger.debug(f"No current attention field, returning viewport: {self.viewport.bbox}")
        return self.viewport
    
    def predict_next_attention_field(self) -> Optional[AttentionField]:
        """
        Predict the next attention field based on the inferred direction from center history.
        
        Returns:
            Predicted next attention field, or None if direction can't be determined
        """
        if not self.current_attention_field:
            logger.debug("Cannot predict next field: No current attention field")
            return None
            
        # Use the direction stored in the current field (which came from _infer_movement_direction)
        direction = self.current_attention_field.direction
        if not direction:
            logger.debug("Cannot predict next field: No direction inferred for current field")
            return None
        
        # Get current field
        current = self.current_attention_field
        
        logger.debug(f"Predicting next attention field based on direction: {direction}")
        
        # Determine shift amount (30% of current dimension)
        x_shift = int(current.width * 0.3)
        y_shift = int(current.height * 0.3)
        
        logger.debug(f"Shift amounts: x_shift={x_shift}, y_shift={y_shift}")
        
        # Create new attention field shifted in the inferred direction
        next_x, next_y = current.x, current.y
        
        if direction == 'right':
            next_x = current.x + x_shift
        elif direction == 'left':
            next_x = current.x - x_shift
        elif direction == 'down':
            next_y = current.y + y_shift
        elif direction == 'up':
            next_y = current.y - y_shift
        else:
            # Unknown direction - should not happen if direction is not None
            logger.warning(f"Cannot predict next field: Unknown direction '{direction}'")
            return None
        
        # Clamp predicted field to screen bounds
        final_x = max(0, min(self.screen_width - current.width, next_x))
        final_y = max(0, min(self.screen_height - current.height, next_y))
        
        if final_x != next_x:
            logger.debug(f"Adjusted predicted x position from {next_x} to {final_x} to stay within screen bounds")
        if final_y != next_y:
             logger.debug(f"Adjusted predicted y position from {next_y} to {final_y} to stay within screen bounds")
        
        next_field = AttentionField(
            x=final_x,
            y=final_y,
            width=current.width,
            height=current.height,
            confidence=0.7,  # Lower confidence for prediction
            direction=direction
        )
        
        logger.info(f"Predicted next attention field: {next_field.bbox}, direction: {direction}, confidence: 0.7")
        return next_field
    
    def get_attention_context(self) -> Dict:
        """
        Get the current attention context as a dictionary.
        
        Returns:
            Dictionary with current attention field, click history size, center history size,
            base box size, and predicted next area.
        """
        logger.debug("Getting attention context")
        current = self.get_current_attention_field()
        next_field = self.predict_next_attention_field()
        
        context = {
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
            "center_history_size": len(self.center_history), # Added for debugging
            "base_box_size": self.base_box_size,
        }
        
        # logger.debug(f"Attention context: {context}") # Too verbose
        return context





