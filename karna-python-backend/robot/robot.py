"""
Robot module for automating mouse and keyboard actions on the user's system.

This module provides a comprehensive set of functions to control the mouse,
keyboard, and perform screen operations using PyAutoGUI.
"""

import pyautogui
import time
import logging
from typing import Tuple, List, Optional, Dict, Any, Union
import platform
import os
from dataclasses import dataclass

# Configure PyAutoGUI settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Add small pause between PyAutoGUI commands

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class Point:
    """Represents a point on the screen with x and y coordinates."""
    x: int
    y: int


@dataclass
class Region:
    """Represents a rectangular region on the screen."""
    x: int
    y: int
    width: int
    height: int


class Robot:
    """
    Robot class for automating mouse and keyboard actions on the user's system.
    
    This class provides methods to:
    - Control mouse movements and clicks
    - Perform keyboard actions (typing, pressing keys)
    - Take screenshots and find images on screen
    - Get screen information
    - Perform drag and drop operations
    - Execute system-specific actions
    """
    
    def __init__(self):
        """Initialize the Robot with system information."""
        self.os_name = platform.system()
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"Robot initialized on {self.os_name} with screen size: {self.screen_width}x{self.screen_height}")
    
    # ===== Mouse Control Methods =====
    
    def move_mouse(self, x: int, y: int, duration: float = 0.2) -> None:
        """
        Move the mouse to the specified coordinates.
        
        Args:
            x: X-coordinate to move to
            y: Y-coordinate to move to
            duration: Time (in seconds) the movement should take
        """
        try:
            if not self._is_coordinate_safe(x, y):
                logger.warning(f"Unsafe coordinates: ({x}, {y})")
                return
            
            pyautogui.moveTo(x, y, duration=duration)
            logger.debug(f"Mouse moved to ({x}, {y})")
        except Exception as e:
            logger.error(f"Failed to move mouse: {str(e)}")
            raise
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', clicks: int = 1, interval: float = 0.0,
              duration: float = 0.0) -> None:
        """
        Click at the current or specified position.
        
        Args:
            x: X-coordinate to click (current position if None)
            y: Y-coordinate to click (current position if None)
            button: Mouse button to click ('left', 'middle', 'right')
            clicks: Number of clicks
            interval: Seconds between clicks
            duration: Seconds to move mouse to position
        """
        try:
            if x is not None and y is not None:
                if not self._is_coordinate_safe(x, y):
                    logger.warning(f"Unsafe click coordinates: ({x}, {y})")
                    return
                pyautogui.click(x, y, clicks=clicks, interval=interval, button=button, duration=duration)
                logger.debug(f"{button.capitalize()} click at ({x}, {y})")
            else:
                pyautogui.click(clicks=clicks, interval=interval, button=button)
                logger.debug(f"{button.capitalize()} click at current position")
        except Exception as e:
            logger.error(f"Failed to click: {str(e)}")
            raise
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Right-click at the current or specified position.
        
        Args:
            x: X-coordinate to right-click (current position if None)
            y: Y-coordinate to right-click (current position if None)
        """
        self.click(x, y, button='right')
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Double-click at the current or specified position.
        
        Args:
            x: X-coordinate to double-click (current position if None)
            y: Y-coordinate to double-click (current position if None)
        """
        self.click(x, y, clicks=2)
    
    def drag_to(self, x: int, y: int, button: str = 'left', duration: float = 0.2) -> None:
        """
        Drag the mouse from current position to the specified coordinates.
        
        Args:
            x: X-coordinate to drag to
            y: Y-coordinate to drag to
            button: Mouse button to hold during drag
            duration: Time (in seconds) the drag should take
        """
        try:
            if not self._is_coordinate_safe(x, y):
                logger.warning(f"Unsafe drag coordinates: ({x}, {y})")
                return
            
            pyautogui.dragTo(x, y, button=button, duration=duration)
            logger.debug(f"Dragged to ({x}, {y})")
        except Exception as e:
            logger.error(f"Failed to drag: {str(e)}")
            raise
    
    def drag_rel(self, xOffset: int, yOffset: int, button: str = 'left', duration: float = 0.2) -> None:
        """
        Drag the mouse relative to its current position.
        
        Args:
            xOffset: X-offset to drag
            yOffset: Y-offset to drag
            button: Mouse button to hold during drag
            duration: Time (in seconds) the drag should take
        """
        try:
            current_x, current_y = pyautogui.position()
            target_x, target_y = current_x + xOffset, current_y + yOffset
            
            if not self._is_coordinate_safe(target_x, target_y):
                logger.warning(f"Unsafe relative drag target: ({target_x}, {target_y})")
                return
            
            pyautogui.dragRel(xOffset, yOffset, button=button, duration=duration)
            logger.debug(f"Dragged relatively by ({xOffset}, {yOffset})")
        except Exception as e:
            logger.error(f"Failed to drag relatively: {str(e)}")
            raise
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Scroll the mouse wheel.
        
        Args:
            clicks: Number of "clicks" to scroll (positive = up, negative = down)
            x: X-coordinate to move to before scrolling
            y: Y-coordinate to move to before scrolling
        """
        try:
            if x is not None and y is not None:
                if not self._is_coordinate_safe(x, y):
                    logger.warning(f"Unsafe scroll coordinates: ({x}, {y})")
                    return
                pyautogui.moveTo(x, y)
            
            pyautogui.scroll(clicks)
            logger.debug(f"Scrolled {clicks} clicks")
        except Exception as e:
            logger.error(f"Failed to scroll: {str(e)}")
            raise
    
    def get_mouse_position(self) -> Point:
        """
        Get the current mouse position.
        
        Returns:
            Point object with current x, y coordinates
        """
        x, y = pyautogui.position()
        return Point(x, y)
    
    # ===== Keyboard Control Methods =====
    
    def type_text(self, text: str, interval: float = 0.0) -> None:
        """
        Type the given text with the keyboard.
        
        Args:
            text: The text to type
            interval: Seconds between keypresses
        """
        try:
            pyautogui.write(text, interval=interval)
            logger.debug(f"Typed text: '{text[:10]}{'...' if len(text) > 10 else ''}'")
        except Exception as e:
            logger.error(f"Failed to type text: {str(e)}")
            raise
    
    def press_key(self, key: str) -> None:
        """
        Press and release a key.
        
        Args:
            key: The key to press (e.g., 'enter', 'tab', 'a', etc.)
        """
        try:
            pyautogui.press(key)
            logger.debug(f"Pressed key: {key}")
        except Exception as e:
            logger.error(f"Failed to press key: {str(e)}")
            raise
    
    def hold_key(self, key: str) -> None:
        """
        Hold down a key.
        
        Args:
            key: The key to hold down
        """
        try:
            pyautogui.keyDown(key)
            logger.debug(f"Holding key: {key}")
        except Exception as e:
            logger.error(f"Failed to hold key: {str(e)}")
            raise
    
    def release_key(self, key: str) -> None:
        """
        Release a held key.
        
        Args:
            key: The key to release
        """
        try:
            pyautogui.keyUp(key)
            logger.debug(f"Released key: {key}")
        except Exception as e:
            logger.error(f"Failed to release key: {str(e)}")
            raise
    
    def hotkey(self, *keys: str) -> None:
        """
        Press a hotkey combination (multiple keys at once).
        
        Args:
            *keys: The keys to press (e.g., 'ctrl', 'c' for copy)
        """
        try:
            pyautogui.hotkey(*keys)
            logger.debug(f"Pressed hotkey: {'+'.join(keys)}")
        except Exception as e:
            logger.error(f"Failed to press hotkey: {str(e)}")
            raise
    
    # ===== Screen and Image Methods =====
    
    def take_screenshot(self, region: Optional[Region] = None) -> Any:
        """
        Take a screenshot of the entire screen or a region.
        
        Args:
            region: Optional Region object specifying area to capture
        
        Returns:
            Screenshot image object
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=(region.x, region.y, region.width, region.height))
                logger.debug(f"Took screenshot of region: {region}")
            else:
                screenshot = pyautogui.screenshot()
                logger.debug("Took full screen screenshot")
            return screenshot
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def save_screenshot(self, filename: str, region: Optional[Region] = None) -> str:
        """
        Take a screenshot and save it to a file.
        
        Args:
            filename: Path to save the screenshot
            region: Optional Region object specifying area to capture
        
        Returns:
            Path to the saved screenshot
        """
        try:
            screenshot = self.take_screenshot(region)
            screenshot.save(filename)
            logger.debug(f"Saved screenshot to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save screenshot: {str(e)}")
            raise
    
    def locate_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Point]:
        """
        Find an image on the screen and return its position.
        
        Args:
            image_path: Path to the image file to find
            confidence: Matching confidence threshold (0-1)
        
        Returns:
            Point object with coordinates of the center of the found image, or None if not found
        """
        try:
            result = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if result:
                x, y = pyautogui.center(result)
                logger.debug(f"Found image '{image_path}' at ({x}, {y})")
                return Point(x, y)
            else:
                logger.debug(f"Image '{image_path}' not found on screen")
                return None
        except Exception as e:
            logger.error(f"Failed to locate image on screen: {str(e)}")
            raise
    
    def wait_for_image(self, image_path: str, timeout: int = 10, confidence: float = 0.9) -> Optional[Point]:
        """
        Wait for an image to appear on screen.
        
        Args:
            image_path: Path to the image file to wait for
            timeout: Maximum seconds to wait
            confidence: Matching confidence threshold (0-1)
        
        Returns:
            Point object with coordinates of the center of the found image, or None if timeout
        """
        try:
            start_time = time.time()
            while time.time() - start_time < timeout:
                result = self.locate_on_screen(image_path, confidence)
                if result:
                    return result
                time.sleep(0.5)
            
            logger.debug(f"Timeout waiting for image '{image_path}'")
            return None
        except Exception as e:
            logger.error(f"Failed while waiting for image: {str(e)}")
            raise
    
    # ===== Utility Methods =====
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the screen size.
        
        Returns:
            Tuple of (width, height)
        """
        return (self.screen_width, self.screen_height)
    
    def wait(self, seconds: float) -> None:
        """
        Wait for the specified number of seconds.
        
        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)
        logger.debug(f"Waited for {seconds} seconds")
    
    # ===== Helper Methods =====
    
    def _is_coordinate_safe(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within screen bounds.
        
        Args:
            x: X-coordinate to check
            y: Y-coordinate to check
        
        Returns:
            True if coordinates are safe, False otherwise
        """
        return 0 <= x < self.screen_width and 0 <= y < self.screen_height
