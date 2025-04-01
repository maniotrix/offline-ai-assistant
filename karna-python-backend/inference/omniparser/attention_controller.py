import logging
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class Direction(Enum):
    """Enum for movement directions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UNKNOWN = "unknown"
    
renderBBox = {
    "x": 952,
    "y": 121,
    "width": 960,
    "height": 927
  }

@dataclass
class BoundingBox:
    """Represents a bounding box in screen coordinates"""
    x: int
    y: int
    width: int
    height: int
    
    @property
    def left(self) -> int:
        return self.x
    
    @property
    def right(self) -> int:
        return self.x + self.width
    
    @property
    def top(self) -> int:
        return self.y
    
    @property
    def bottom(self) -> int:
        return self.y + self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if the box contains the given point"""
        return (self.left <= x <= self.right and self.top <= y <= self.bottom)
    
    def expand(self, factor: float) -> 'BoundingBox':
        """Return a new expanded bounding box by the given factor"""
        width_increase = int(self.width * (factor - 1))
        height_increase = int(self.height * (factor - 1))
        
        return BoundingBox(
            x=max(0, self.x - width_increase // 2),
            y=max(0, self.y - height_increase // 2),
            width=self.width + width_increase,
            height=self.height + height_increase
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }


class AttentionFieldController:
    """Controls and simulates human visual attention field based on click history."""
    
    def __init__(
        self, 
        max_click_history: Optional[int] = None,  # Now optional, can be None for unlimited history
        expansion_factor: float = 1.5,
        direction_threshold: float = 0.6,
        recency_weight: float = 0.8,  # Weight factor for more recent clicks
        velocity_smoothing_window: int = 5  # Window size for velocity smoothing
    ):
        """Initialize the AttentionFieldController.
        
        Args:
            max_click_history: Maximum number of clicks to track (None for unlimited)
            expansion_factor: Factor to expand the bounding box by
            direction_threshold: Threshold for direction classification
            recency_weight: Weight factor for emphasizing more recent clicks (0-1)
            velocity_smoothing_window: Number of recent velocity samples to use for smoothing
        """
        self.click_history: List[Tuple[int, int, datetime]] = []
        self.max_click_history = max_click_history
        self.expansion_factor = expansion_factor
        self.direction_threshold = direction_threshold
        self.recency_weight = recency_weight
        self.velocity_smoothing_window = velocity_smoothing_window
        
        # Use renderBBox to define the screen boundaries
        self.screen_bounds = BoundingBox(
            x=renderBBox["x"],
            y=renderBBox["y"],
            width=renderBBox["width"],
            height=renderBBox["height"]
        )
        
        # Base box size will be set dynamically from first OmniParser result
        self.base_box_size: Optional[Tuple[int, int]] = None
        self.current_attention_box: Optional[BoundingBox] = None
        self.inferred_direction: Direction = Direction.UNKNOWN
        
        # Track click velocities for improved direction inference
        self.click_velocities: List[Tuple[float, float]] = []
    
    def _ensure_within_screen_bounds(self, box: BoundingBox) -> BoundingBox:
        """Ensure that a bounding box is within the screen boundaries.
        
        Args:
            box: The bounding box to check and adjust
            
        Returns:
            Adjusted bounding box that fits within screen bounds
        """
        # Calculate adjusted position and dimensions to fit within screen bounds
        x = max(self.screen_bounds.x, min(box.x, self.screen_bounds.right - 1))
        y = max(self.screen_bounds.y, min(box.y, self.screen_bounds.bottom - 1))
        
        # Ensure the box doesn't extend beyond screen bounds
        width = min(box.width, self.screen_bounds.right - x)
        height = min(box.height, self.screen_bounds.bottom - y)
        
        # Create new box with adjusted values
        return BoundingBox(x=x, y=y, width=width, height=height)
    
    def _get_weighted_click_points(self) -> List[Tuple[int, int, float]]:
        """Get click points with recency weights.
        
        More recent clicks get higher weights to influence the attention box more.
        For large histories, uses an exponential decay function to weight recent clicks.
        
        Returns:
            List of (x, y, weight) tuples
        """
        if not self.click_history:
            return []
        
        n = len(self.click_history)
        
        # For very large histories, we need a more aggressive weighting scheme
        # to ensure that ancient clicks don't dominate
        if n > 20:  # Consider 20+ clicks as "large history"
            # Use a modified weight calculation that decays more aggressively
            # for older clicks but still considers them
            weights = []
            for i in range(n):
                # Position from the end (0 is the most recent)
                pos_from_end = n - i - 1
                
                # Apply exponential decay with faster decay for older clicks
                if pos_from_end < 5:  # Very recent clicks (last 5)
                    # Strong weight for the most recent clicks
                    weight = self.recency_weight ** pos_from_end
                else:
                    # Steeper decay for older clicks
                    weight = self.recency_weight ** 5 * (self.recency_weight ** 2) ** (pos_from_end - 5)
                
                weights.append(weight)
        else:
            # For smaller histories, use the standard weighting
            weights = [self.recency_weight ** (n - i - 1) for i in range(n)]
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        
        # Apply weights to click points
        weighted_points = []
        for i, (x, y, _) in enumerate(self.click_history):
            weighted_points.append((x, y, weights[i]))
        
        return weighted_points
    
    def _update_attention_box(self) -> None:
        """Update the current attention box based on click history.
        
        Uses weighted averaging for multiple clicks to prioritize recent clicks.
        Handles both small and large click histories effectively.
        Ensures the attention box stays within screen boundaries.
        """
        if len(self.click_history) < 2:
            # Cold start: use full screen or default box
            if self.click_history and self.base_box_size is not None:
                # We have a base box size from the first click
                x, y, _ = self.click_history[0]
                width, height = self.base_box_size
                
                # Center the box on the click
                initial_box = BoundingBox(
                    x=max(0, x - width // 2),
                    y=max(0, y - height // 2),
                    width=width,
                    height=height
                )
                
                # Ensure it's within screen bounds
                self.current_attention_box = self._ensure_within_screen_bounds(initial_box)
            else:
                # No base box size yet, use full render bounds
                self.current_attention_box = BoundingBox(
                    x=self.screen_bounds.x,
                    y=self.screen_bounds.y,
                    width=self.screen_bounds.width,
                    height=self.screen_bounds.height
                )
        else:
            # Get weighted click points based on recency
            weighted_points = self._get_weighted_click_points()
            
            if not weighted_points:
                return
            
            # Filter out points that are outside screen bounds
            filtered_points = []
            for x, y, w in weighted_points:
                if self.screen_bounds.contains_point(x, y):
                    filtered_points.append((x, y, w))
            
            # If all points were filtered out, use the screen bounds
            if not filtered_points:
                self.current_attention_box = BoundingBox(
                    x=self.screen_bounds.x,
                    y=self.screen_bounds.y,
                    width=self.screen_bounds.width,
                    height=self.screen_bounds.height
                )
                return
            
            # For large datasets, we can use clustering or simply focus on recent clicks
            # Here, we'll use a hybrid approach considering all clicks but giving much more
            # weight to recent ones
            
            # Initialize with full range first
            x_coords = [x for x, _, _ in filtered_points]
            y_coords = [y for _, y, _ in filtered_points]
            weights = [w for _, _, w in filtered_points]
            
            # Calculate bounding box from min/max
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)
            
            # For very large datasets, check if the bounding box is too large (scattered clicks)
            # In such cases, prioritize recent clicks more strongly
            if len(filtered_points) > 10:
                # Calculate weighted centroid
                total_weight = sum(weights)
                if total_weight > 0:
                    weighted_x = sum(x * w for (x, _, w) in filtered_points) / total_weight
                    weighted_y = sum(y * w for (_, y, w) in filtered_points) / total_weight
                    
                    # Calculate weighted variance to detect scatter
                    weighted_var_x = sum(w * ((x - weighted_x) ** 2) for (x, _, w) in filtered_points) / total_weight
                    weighted_var_y = sum(w * ((y - weighted_y) ** 2) for (_, y, w) in filtered_points) / total_weight
                    
                    # If variance is high (scattered clicks), focus more on recent clicks
                    scatter_threshold = self.screen_bounds.width * self.screen_bounds.height * 0.1  # Adjust based on screen size
                    if weighted_var_x + weighted_var_y > scatter_threshold:
                        logger.debug("High click scatter detected, focusing on recent clicks")
                        
                        # Use just the most recent clicks for the bounding box
                        recent_n = min(5, len(filtered_points) // 2)
                        recent_points = filtered_points[-recent_n:]
                        
                        x_coords = [x for x, _, _ in recent_points]
                        y_coords = [y for _, y, _ in recent_points]
                        
                        min_x, max_x = min(x_coords), max(x_coords)
                        min_y, max_y = min(y_coords), max(y_coords)
            
            # Create bounding box that encompasses all relevant clicks
            width = max(max_x - min_x, 1)  # Ensure at least 1px width
            height = max(max_y - min_y, 1)  # Ensure at least 1px height
            
            # If width or height is too small, use base box size as minimum
            if self.base_box_size is not None:
                base_width, base_height = self.base_box_size
                min_width = base_width // 2
                min_height = base_height // 2
                
                # Only apply minimums for very small bounding boxes
                if width < min_width:
                    # Center the smaller dimension
                    center_x = (min_x + max_x) / 2
                    min_x = int(center_x - min_width / 2)
                    width = min_width
                
                if height < min_height:
                    # Center the smaller dimension
                    center_y = (min_y + max_y) / 2
                    min_y = int(center_y - min_height / 2)
                    height = min_height
            
            # Calculate weighted centroid to adjust the box position
            total_weight = sum(w for _, _, w in filtered_points)
            if total_weight > 0:
                weighted_x = sum(x * w for x, _, w in filtered_points) / total_weight
                weighted_y = sum(y * w for _, y, w in filtered_points) / total_weight
                
                # Ensure the weighted centroid is within the box
                # If not, adjust the box to include it
                if weighted_x < min_x:
                    width += (min_x - weighted_x)
                    min_x = int(weighted_x)
                elif weighted_x > max_x:
                    width += (weighted_x - max_x)
                    # min_x stays the same
                
                if weighted_y < min_y:
                    height += (min_y - weighted_y)
                    min_y = int(weighted_y)
                elif weighted_y > max_y:
                    height += (weighted_y - max_y)
                    # min_y stays the same
            
            # Create initial box
            initial_box = BoundingBox(
                x=min_x,
                y=min_y,
                width=width,
                height=height
            )
            
            # Expand the box by the expansion factor
            expanded_box = initial_box.expand(self.expansion_factor)
            
            # Ensure the box stays within screen bounds
            self.current_attention_box = self._ensure_within_screen_bounds(expanded_box)
        
    def _infer_direction(self) -> None:
        """Infer the direction of attention movement from click history.
        
        Uses both recent clicks and velocity data for more accurate direction inference.
        Handles large click histories by focusing on recent movement patterns.
        """
        if len(self.click_history) < 2:
            self.inferred_direction = Direction.UNKNOWN
            return
        
        # Use velocity data if available
        if self.click_velocities:
            # For large velocity histories, focus on a window of recent velocities
            velocities_to_use = self.click_velocities
            if self.velocity_smoothing_window and len(velocities_to_use) > self.velocity_smoothing_window:
                velocities_to_use = velocities_to_use[-self.velocity_smoothing_window:]
            
            # Average the velocities with more weight on recent ones
            vx_sum = 0
            vy_sum = 0
            weights_sum = 0
            
            # Compute weighted average of velocities
            for i, (vx, vy) in enumerate(velocities_to_use):
                # More recent velocities get higher weights
                weight = self.recency_weight ** (len(velocities_to_use) - i - 1)
                vx_sum += vx * weight
                vy_sum += vy * weight
                weights_sum += weight
            
            if weights_sum > 0:
                avg_vx = vx_sum / weights_sum
                avg_vy = vy_sum / weights_sum
                
                # Calculate magnitude for normalization
                magnitude = max(abs(avg_vx) + abs(avg_vy), 1)  # Avoid division by zero
                
                # Normalize
                norm_vx = abs(avg_vx) / magnitude
                norm_vy = abs(avg_vy) / magnitude
                
                # Determine direction using threshold
                if norm_vx > self.direction_threshold:
                    self.inferred_direction = Direction.RIGHT if avg_vx > 0 else Direction.LEFT
                elif norm_vy > self.direction_threshold:
                    self.inferred_direction = Direction.DOWN if avg_vy > 0 else Direction.UP
                else:
                    # For mixed directions, take the dominant one
                    if abs(avg_vx) > abs(avg_vy):
                        self.inferred_direction = Direction.RIGHT if avg_vx > 0 else Direction.LEFT
                    else:
                        self.inferred_direction = Direction.DOWN if avg_vy > 0 else Direction.UP
                
                return
        
        # Fallback to click deltas if velocity calculation failed
        # For large click histories, just consider the most recent movement
        x2, y2, _ = self.click_history[-1]
        x1, y1, _ = self.click_history[-2]
        
        dx = x2 - x1
        dy = y2 - y1
        
        # Calculate the total movement distance
        total_distance = max(abs(dx) + abs(dy), 1)  # Avoid division by zero
        
        # Calculate normalized movement components
        normalized_dx = abs(dx) / total_distance
        normalized_dy = abs(dy) / total_distance
        
        # Determine the primary direction based on threshold
        if normalized_dx > self.direction_threshold:
            # Primarily horizontal movement
            self.inferred_direction = Direction.RIGHT if dx > 0 else Direction.LEFT
        elif normalized_dy > self.direction_threshold:
            # Primarily vertical movement
            self.inferred_direction = Direction.DOWN if dy > 0 else Direction.UP
        else:
            # Mixed movement - choose the dominant direction
            if abs(dx) > abs(dy):
                self.inferred_direction = Direction.RIGHT if dx > 0 else Direction.LEFT
            else:
                self.inferred_direction = Direction.DOWN if dy > 0 else Direction.UP
    
    def get_current_attention_field(self) -> Optional[BoundingBox]:
        """Get the current attention field bounding box.
        
        Returns:
            BoundingBox or None if not enough data
        """
        return self.current_attention_box
    
    def predict_next_attention_area(self, pan_percentage: float = 0.5) -> Optional[BoundingBox]:
        """Predict the next attention area based on movement direction.
        
        Args:
            pan_percentage: How much to pan in the inferred direction (0.0-1.0)
            
        Returns:
            BoundingBox or None if not enough data
        """
        if self.current_attention_box is None or self.inferred_direction == Direction.UNKNOWN:
            return self.current_attention_box
        
        # Clone the current box
        box = self.current_attention_box
        
        # For boxes built from many clicks, use adaptive panning based on click count and distribution
        click_count = len(self.click_history)
        adaptive_pan = pan_percentage
        
        # Adjust panning based on click count - more clicks should lead to more conservative panning
        # to avoid jumping too far, especially with scattered clicks
        if click_count > 3:
            # Calculate a damping factor that decreases as click count increases
            # but stabilizes for very large numbers to avoid becoming too small
            damping = 1.0 - min(0.7, (click_count - 3) / (click_count + 10))
            adaptive_pan = pan_percentage * damping
        
        # Calculate pan distance based on box dimensions
        pan_x = int(box.width * adaptive_pan)
        pan_y = int(box.height * adaptive_pan)
        
        # Create a new box panned in the inferred direction
        if self.inferred_direction == Direction.RIGHT:
            panned_box = BoundingBox(
                x=box.x + pan_x,
                y=box.y,
                width=box.width,
                height=box.height
            )
        elif self.inferred_direction == Direction.LEFT:
            panned_box = BoundingBox(
                x=max(0, box.x - pan_x),
                y=box.y,
                width=box.width,
                height=box.height
            )
        elif self.inferred_direction == Direction.DOWN:
            panned_box = BoundingBox(
                x=box.x,
                y=box.y + pan_y,
                width=box.width,
                height=box.height
            )
        elif self.inferred_direction == Direction.UP:
            panned_box = BoundingBox(
                x=box.x,
                y=max(0, box.y - pan_y),
                width=box.width,
                height=box.height
            )
        else:
            panned_box = box  # Fallback
        
        # Ensure the panned box stays within screen bounds
        return self._ensure_within_screen_bounds(panned_box)
    
    def add_click(self, x: int, y: int, timestamp: datetime, omni_parser_result_size: Optional[Tuple[int, int]] = None) -> None:
        """Add a new click to the history.
        
        Args:
            x: X coordinate of the click
            y: Y coordinate of the click
            timestamp: Timestamp of the click
            omni_parser_result_size: Size (width, height) from OmniParser result if available
        """
        # Check if click is within screen bounds
        if not self.screen_bounds.contains_point(x, y):
            logger.warning(f"Click at ({x}, {y}) is outside screen bounds - adjusting to nearest valid position")
            # Adjust to nearest valid position
            x = max(self.screen_bounds.x, min(x, self.screen_bounds.right - 1))
            y = max(self.screen_bounds.y, min(y, self.screen_bounds.bottom - 1))
            
        # Set base box size from first click's OmniParser result
        if self.base_box_size is None and omni_parser_result_size is not None:
            self.base_box_size = omni_parser_result_size
            logger.info(f"Set base box size to {self.base_box_size} from OmniParser result")
        
        # Calculate velocity if we have previous clicks
        if self.click_history:
            prev_x, prev_y, prev_time = self.click_history[-1]
            
            # Time delta in seconds
            time_delta = (timestamp - prev_time).total_seconds()
            if time_delta > 0:
                # Calculate velocity components (pixels per second)
                vx = (x - prev_x) / time_delta
                vy = (y - prev_y) / time_delta
                self.click_velocities.append((vx, vy))
                
                # If max_click_history is set, limit velocity history
                if self.max_click_history is not None:
                    max_velocities = self.max_click_history - 1  # One less than the click history
                    if len(self.click_velocities) > max_velocities:
                        self.click_velocities = self.click_velocities[-max_velocities:]
        
        # Add to click history
        self.click_history.append((x, y, timestamp))
        
        # If max_click_history is set, limit the history
        if self.max_click_history is not None and len(self.click_history) > self.max_click_history:
            self.click_history = self.click_history[-self.max_click_history:]
        
        # Update the attention box
        self._update_attention_box()
        
        # Infer direction from click history
        if len(self.click_history) >= 2:
            self._infer_direction()
    
    def reset(self) -> None:
        """Reset the controller state."""
        self.click_history = []
        self.base_box_size = None
        self.current_attention_box = None
        self.inferred_direction = Direction.UNKNOWN
    
    def from_screenshot_events(self, screenshot_events: List) -> None:
        """Initialize controller from a list of screenshot events.
        
        Args:
            screenshot_events: List of ScreenshotEvent objects with click data
        """
        # Reset first
        self.reset()
        
        # Process events that have mouse clicks
        for event in screenshot_events:
            if hasattr(event, 'mouse_x') and hasattr(event, 'mouse_y') and \
               event.mouse_x is not None and event.mouse_y is not None:
                # Extract OmniParser result size if available (this depends on your data structure)
                omni_size = None
                if hasattr(event, 'omni_parser_result') and event.omni_parser_result:
                    if hasattr(event.omni_parser_result, 'patch_size'):
                        omni_size = event.omni_parser_result.patch_size
                
                # Add the click
                self.add_click(
                    x=event.mouse_x, 
                    y=event.mouse_y, 
                    timestamp=event.timestamp,
                    omni_parser_result_size=omni_size
                )
    
    def get_current_state(self) -> Dict:
        """Get the current state of the attention controller.
        
        Returns:
            Dictionary with current state information
        """
        state = {
            "click_count": len(self.click_history),
            "inferred_direction": self.inferred_direction.value if self.inferred_direction else "unknown",
            "base_box_size": self.base_box_size,
        }
        
        if self.current_attention_box:
            state["current_attention_box"] = self.current_attention_box.to_dict()
        
        return state
