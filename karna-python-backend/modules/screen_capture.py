import os
import pyautogui
from datetime import datetime, timedelta
from pynput import keyboard, mouse
import threading
from PIL import Image, ImageDraw, ImageFont
import re
import logging
from typing import Optional, Dict, Any, List, NamedTuple
from collections import defaultdict
from base.base_observer import Observable, StateChange
import shutil
from dataclasses import dataclass
from enum import Enum, auto
import math

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ScreenCaptureError(Exception):
    """Base exception for screen capture errors"""
    pass

class SessionError(ScreenCaptureError):
    """Raised when there's an error with session management"""
    pass

class DirectoryError(ScreenCaptureError):
    """Raised when there's an error with directory operations"""
    pass

class CaptureError(ScreenCaptureError):
    """Raised when there's an error during screen capture"""
    pass

class EventType(Enum):
    """Enum for different types of screen capture events"""
    CAPTURE_STARTED = auto()
    CAPTURE_STOPPED = auto()
    SCREENSHOT = auto()
    ANNOTATION = auto()
    KEY_PRESS = auto()
    MOUSE_CLICK = auto()

@dataclass
class ScreenCaptureEvent:
    """Represents a screen capture event with its metadata"""
    type: EventType
    project_uuid: str
    command_uuid: str
    timestamp: datetime
    description: str
    screenshot_path: Optional[str] = None
    annotated_path: Optional[str] = None
    mouse_x: Optional[int] = None
    mouse_y: Optional[int] = None
    key_char: Optional[str] = None
    key_code: Optional[str] = None
    is_special_key: bool = False

@dataclass
class SessionStatistics:
    """Statistics for a screen capture session"""
    project_uuid: str = ""
    command_uuid: str = ""
    total_screenshots: int = 0
    total_annotations: int = 0
    total_key_events: int = 0
    total_mouse_events: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    raw_directory_size: int = 0  # in bytes
    annotated_directory_size: int = 0  # in bytes

@dataclass
class ScreenCaptureSession:
    """Represents the state of a screen capture session"""
    project_uuid: str
    command_uuid: str
    is_active: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    raw_dir: Optional[str] = None
    annotated_dir: Optional[str] = None
    keyboard_listener: Optional[keyboard.Listener] = None
    mouse_listener: Optional[mouse.Listener] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate session duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return None

    def get_statistics(self) -> SessionStatistics:
        """Get statistics for the current session"""
        stats = SessionStatistics(
            project_uuid=self.project_uuid,
            command_uuid=self.command_uuid,
            start_time=self.start_time,
            end_time=self.end_time
        )
        
        if self.raw_dir and os.path.exists(self.raw_dir):
            stats.raw_directory_size = sum(
                os.path.getsize(os.path.join(self.raw_dir, f))
                for f in os.listdir(self.raw_dir)
                if os.path.isfile(os.path.join(self.raw_dir, f))
            )
            stats.total_screenshots = len([
                f for f in os.listdir(self.raw_dir)
                if f.endswith('.png')
            ])
            
        if self.annotated_dir and os.path.exists(self.annotated_dir):
            stats.annotated_directory_size = sum(
                os.path.getsize(os.path.join(self.annotated_dir, f))
                for f in os.listdir(self.annotated_dir)
                if os.path.isfile(os.path.join(self.annotated_dir, f))
            )
            stats.total_annotations = len([
                f for f in os.listdir(self.annotated_dir)
                if f.endswith('.png')
            ])
            
        if self.start_time:
            end = self.end_time if self.end_time else datetime.now()
            stats.duration_seconds = (end - self.start_time).total_seconds()
            
        return stats

class ScreenCaptureService(Observable[ScreenCaptureEvent]):
    """Service for capturing screen interactions with annotation capabilities"""
    
    def __init__(self):
        super().__init__()
        self.current_session: Optional[ScreenCaptureSession] = None
        self.lock = threading.Lock()
        self._event_stats: defaultdict[EventType, int] = defaultdict(int)
        self._session_history: List[SessionStatistics] = []
        
        # Setup logging
        logs_dir = os.path.join('data', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(os.path.join(logs_dir, 'screen_capture.log'), mode='a')
        
        # Create formatters and add it to handlers
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
        
        # Add handlers to the logger if they haven't been added
        if not logger.handlers:
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            
        logger.info("ScreenCaptureService initialized")

    def _validate_session(self) -> None:
        """Validate current session state"""
        if not self.current_session:
            raise SessionError("No active session")
        if not self.current_session.is_active:
            raise SessionError("Session is not active")
        if not self.current_session.raw_dir or not self.current_session.annotated_dir:
            raise SessionError("Session directories not properly initialized")
        if not os.path.exists(self.current_session.raw_dir) or not os.path.exists(self.current_session.annotated_dir):
            raise DirectoryError("Session directories do not exist")

    def _ensure_directories(self, project_uuid: str, command_uuid: str) -> tuple[str, str]:
        """Create necessary directories for screenshots and clean existing data"""
        try:
            # Create project and command specific paths
            base_dir = os.path.join('data', project_uuid, command_uuid, 'screenshots')
            raw_dir = os.path.join(base_dir, 'raw')
            annotated_dir = os.path.join(base_dir, 'annotated')
            
            if os.path.exists(base_dir):
                try:
                    shutil.rmtree(base_dir)
                except Exception as e:
                    raise DirectoryError(f"Failed to clean existing directory: {str(e)}")
            
            try:
                os.makedirs(raw_dir, exist_ok=True)
                os.makedirs(annotated_dir, exist_ok=True)
            except Exception as e:
                raise DirectoryError(f"Failed to create directories: {str(e)}")
                
            logger.debug(f"Created fresh directories for project {project_uuid}, command {command_uuid}")
            return raw_dir, annotated_dir
        except Exception as e:
            raise DirectoryError(f"Directory setup failed: {str(e)}")

    def _increment_event_stat(self, event_type: EventType) -> None:
        """Increment the count for a specific event type"""
        self._event_stats[event_type] += 1

    def _create_event(self, event_type: EventType, description: str, **kwargs) -> Optional[ScreenCaptureEvent]:
        """Create a screen capture event with current session context"""
        if not self.current_session or not self.current_session.is_active:
            return None
        
        self._increment_event_stat(event_type)
        
        return ScreenCaptureEvent(
            type=event_type,
            project_uuid=self.current_session.project_uuid,
            command_uuid=self.current_session.command_uuid,
            timestamp=datetime.now(),
            description=description,
            **kwargs
        )

    def _take_screenshot(self, event_description: str) -> str:
        """Take a screenshot and save it in the raw directory"""
        try:
            self._validate_session()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'screenshot_{timestamp}.png'
            filepath = os.path.join(self.current_session.raw_dir, filename)
            
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
            except Exception as e:
                raise CaptureError(f"Failed to capture or save screenshot: {str(e)}")
            
            logger.debug(f"Screenshot saved: {filepath}")
            
            event = self._create_event(
                event_type=EventType.SCREENSHOT,
                description=event_description,
                screenshot_path=filepath
            )
            if event:
                self.notify_observers(event)
            
            return filepath
        except Exception as e:
            logger.error(f"Screenshot capture failed: {str(e)}")
            raise

    def _on_key_press(self, key):
        """Handle keyboard events"""
        try:
            key_char = key.char
            event_desc = f"Key pressed: {key_char}"
            is_special = False
        except AttributeError:
            key_char = None
            key_code = str(key)
            event_desc = f"Special key pressed: {key_code}"
            is_special = True
        
        logger.debug(f"Key event: {event_desc}")
        
        # Take screenshot first to capture the state when key was pressed
        screenshot_path = self._take_screenshot(event_desc)
        
        # Create key press event
        event = self._create_event(
            event_type=EventType.KEY_PRESS,
            description=event_desc,
            screenshot_path=screenshot_path,
            key_char=key_char,
            key_code=str(key),
            is_special_key=is_special
        )
        if event:
            self.notify_observers(event)
        
        # Stop capturing if escape is pressed
        if key == keyboard.Key.esc:
            logger.info("Escape key pressed, stopping capture")
            self.stop_capture()
            return False

    def _on_click(self, x: int, y: int, button, pressed: bool):
        """Handle mouse click events"""
        if pressed:
            event_desc = f"Mouse clicked at ({x}, {y}) with {button}"
            logger.debug(f"Mouse event: {event_desc}")
            
            # Take screenshot first to capture the state when mouse was clicked
            screenshot_path = self._take_screenshot(event_desc)
            annotated_path = None
            
            # Create mouse click event
            event = self._create_event(
                event_type=EventType.MOUSE_CLICK,
                description=event_desc,
                screenshot_path=screenshot_path,
                mouse_x=x,
                mouse_y=y
            )
            if event:
                self.notify_observers(event)
            
            # Create annotation after the event is created
            if screenshot_path:
                self._annotate_screenshot(screenshot_path, x, y, event_desc)

    def _annotate_screenshot(self, screenshot_path: str, x: Optional[int] = None, y: Optional[int] = None, 
                           text: Optional[str] = None):
        """Create an annotated version of the screenshot"""
        if not self.current_session or not self.current_session.annotated_dir:
            logger.warning("Attempted to annotate screenshot without active session")
            return
        
        try:
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            # Draw click location if coordinates provided
            if x is not None and y is not None:
                radius = 20
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), 
                            outline='red', width=5)

            # Add text annotation if provided
            if text:
                font_size = max(20, image.width // 30)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    logger.warning("Arial font not found, using default font")
                    font = ImageFont.load_default()
                draw.text((10, 10), text, fill='red', font=font)

            # Save annotated version
            filename = os.path.basename(screenshot_path)
            annotated_path = os.path.join(self.current_session.annotated_dir, f'annotated_{filename}')
            image.save(annotated_path)
            logger.debug(f"Created annotated screenshot: {annotated_path}")
            
            # Create annotation event
            event = self._create_event(
                event_type=EventType.ANNOTATION,
                description="Screenshot annotated",
                screenshot_path=screenshot_path,
                annotated_path=annotated_path
            )
            if event:
                self.notify_observers(event)
                
        except Exception as e:
            logger.error(f"Failed to annotate screenshot: {str(e)}")

    def start_capture(self, project_uuid: str, command_uuid: str) -> None:
        """Start capturing screenshots for a specific command"""
        with self.lock:
            if self.current_session and self.current_session.is_active:
                raise SessionError("Cannot start new session while another is active")
            
            try:
                logger.info(f"Starting capture for project: {project_uuid}, command: {command_uuid}")
                raw_dir, annotated_dir = self._ensure_directories(project_uuid, command_uuid)
                
                self.current_session = ScreenCaptureSession(
                    project_uuid=project_uuid,
                    command_uuid=command_uuid,
                    is_active=True,
                    start_time=datetime.now(),
                    raw_dir=raw_dir,
                    annotated_dir=annotated_dir
                )
                
                try:
                    self.current_session.keyboard_listener = keyboard.Listener(on_press=self._on_key_press)
                    self.current_session.mouse_listener = mouse.Listener(on_click=self._on_click)
                    
                    self.current_session.keyboard_listener.start()
                    self.current_session.mouse_listener.start()
                except Exception as e:
                    raise SessionError(f"Failed to initialize input listeners: {str(e)}")
                
                event = self._create_event(
                    event_type=EventType.CAPTURE_STARTED,
                    description=f"Screen capture started for project: {project_uuid}, command: {command_uuid}"
                )
                if event:
                    self.notify_observers(event)
                    self.set_state('capturing', True)
                    
            except Exception as e:
                self.current_session = None
                logger.error(f"Failed to start capture: {str(e)}")
                raise

    def create_session_summary(self, show_preview: bool = False) -> Optional[str]:
        """Create a visual summary of all screenshots and annotations in the current session.
        
        Args:
            show_preview: Whether to display the summary image immediately
            
        Returns:
            str: Path to the generated summary image, or None if no screenshots exist
        """
        try:
            self._validate_session()
            
            # Collect all screenshots and annotations
            screenshots = []
            if self.current_session.raw_dir and self.current_session.annotated_dir:
                raw_files = sorted([f for f in os.listdir(self.current_session.raw_dir) 
                                  if f.endswith('.png')])
                
                for raw_file in raw_files:
                    raw_path = os.path.join(self.current_session.raw_dir, raw_file)
                    annotated_file = f'annotated_{raw_file}'
                    annotated_path = os.path.join(self.current_session.annotated_dir, annotated_file)
                    screenshots.append((raw_path, annotated_path if os.path.exists(annotated_path) else None))
            
            if not screenshots:
                logger.warning("No screenshots found for session summary")
                return None
                
            # Create a grid layout
            n_images = len(screenshots) * 2  # Both raw and annotated versions
            grid_size = math.ceil(math.sqrt(n_images))
            
            # Calculate thumbnail size and create canvas
            thumb_width = 320
            thumb_height = 180
            padding = 10
            
            canvas_width = (thumb_width + padding) * grid_size
            canvas_height = (thumb_height + padding) * grid_size
            canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
            draw = ImageDraw.Draw(canvas)
            
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                logger.warning("Arial font not found, using default font")
                font = ImageFont.load_default()
            
            # Place images in grid
            for idx, (raw_path, annotated_path) in enumerate(screenshots):
                # Position for raw screenshot
                row = (idx * 2) // grid_size
                col = (idx * 2) % grid_size
                x = col * (thumb_width + padding)
                y = row * (thumb_height + padding)
                
                try:
                    # Add raw screenshot
                    raw_img = Image.open(raw_path)
                    raw_thumb = raw_img.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
                    canvas.paste(raw_thumb, (x, y))
                    draw.text((x + 5, y + 5), f"Raw #{idx + 1}", fill='red', font=font)
                    
                    # Add annotated version if it exists
                    if annotated_path:
                        anno_img = Image.open(annotated_path)
                        anno_thumb = anno_img.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
                        canvas.paste(anno_thumb, (x + thumb_width + padding, y))
                        draw.text((x + thumb_width + padding + 5, y + 5), 
                                f"Annotated #{idx + 1}", fill='red', font=font)
                except Exception as e:
                    logger.error(f"Error processing image {raw_path}: {str(e)}")
                    continue
            
            # Save the visualization
            summary_dir = os.path.join('data', self.current_session.project_uuid, 
                                     self.current_session.command_uuid, 'summary')
            os.makedirs(summary_dir, exist_ok=True)
            
            summary_path = os.path.join(summary_dir, 'session_summary.png')
            canvas.save(summary_path)
            logger.info(f"Created session summary at: {summary_path}")
            
            if show_preview:
                canvas.show()
            
            return summary_path
            
        except Exception as e:
            logger.error(f"Failed to create session summary: {str(e)}")
            return None

    def stop_capture(self) -> None:
        """Stop the current capture session"""
        with self.lock:
            try:
                self._validate_session()
                logger.info(f"Stopping capture for command: {self.current_session.command_uuid}")
                
                try:
                    if self.current_session.keyboard_listener:
                        self.current_session.keyboard_listener.stop()
                    if self.current_session.mouse_listener:
                        self.current_session.mouse_listener.stop()
                except Exception as e:
                    logger.error(f"Error stopping listeners: {str(e)}")
                
                # Create session summary before stopping
                summary_path = self.create_session_summary()
                
                self.current_session.is_active = False
                self.current_session.end_time = datetime.now()
                
                # Include summary path in stop event if available
                event_desc = f"Screen capture stopped after {self.current_session.duration:.2f} seconds"
                if summary_path:
                    event_desc += f"\nSummary available at: {summary_path}"
                
                event = self._create_event(
                    event_type=EventType.CAPTURE_STOPPED,
                    description=event_desc
                )
                if event:
                    self.notify_observers(event)
                    self.set_state('capturing', False)
                
                # Save session statistics before clearing
                if self.current_session:
                    stats = self.current_session.get_statistics()
                    stats.total_key_events = self._event_stats[EventType.KEY_PRESS]
                    stats.total_mouse_events = self._event_stats[EventType.MOUSE_CLICK]
                    self._session_history.append(stats)
                
            except Exception as e:
                logger.error(f"Error during capture stop: {str(e)}")
                raise

    def get_current_session_stats(self) -> Optional[SessionStatistics]:
        """Get statistics for the current session"""
        if not self.current_session:
            return None
        return self.current_session.get_statistics()

    def get_session_history(self) -> List[SessionStatistics]:
        """Get statistics for all completed sessions"""
        return self._session_history.copy()

    def get_total_event_stats(self) -> Dict[EventType, int]:
        """Get total counts for each event type across all sessions"""
        return dict(self._event_stats)

    def cleanup_old_sessions(self, days_to_keep: int = 7) -> None:
        """Clean up screenshot directories older than specified days"""
        try:
            base_dir = os.path.join('data')
            if not os.path.exists(base_dir):
                return

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Iterate through project directories
            for project_uuid in os.listdir(base_dir):
                project_dir = os.path.join(base_dir, project_uuid)
                if not os.path.isdir(project_dir):
                    continue
                
                # Iterate through command directories
                for command_uuid in os.listdir(project_dir):
                    command_dir = os.path.join(project_dir, command_uuid)
                    if not os.path.isdir(command_dir):
                        continue
                    
                    # Check directory modification time
                    mod_time = datetime.fromtimestamp(os.path.getmtime(command_dir))
                    if mod_time < cutoff_date:
                        try:
                            shutil.rmtree(command_dir)
                            logger.info(f"Cleaned up old session directory: {project_uuid}/{command_uuid}")
                        except Exception as e:
                            logger.error(f"Failed to clean up directory {project_uuid}/{command_uuid}: {str(e)}")
                
                # Remove empty project directories
                try:
                    if not os.listdir(project_dir):
                        os.rmdir(project_dir)
                        logger.info(f"Removed empty project directory: {project_uuid}")
                except Exception as e:
                    logger.error(f"Failed to remove empty project directory {project_uuid}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error during session cleanup: {str(e)}")
            raise DirectoryError(f"Session cleanup failed: {str(e)}")

    @property
    def is_capturing(self) -> bool:
        """Check if a capture session is currently active"""
        return bool(self.current_session and self.current_session.is_active)