import os
import uuid
import pyautogui
from datetime import datetime, timedelta
from pynput import keyboard, mouse
import threading
from PIL import Image, ImageDraw, ImageFont
import logging
from typing import Optional, Dict, List
from collections import defaultdict
from services.base_service import BaseService
import shutil
from dataclasses import dataclass, asdict
from enum import Enum, auto
import math
import json

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
class KeyCaptureConfig:
    """Configuration for key capture"""
    is_capture_enabled: bool = True
    is_normal_key_capture_enabled: bool = False
    is_special_key_capture_enabled: bool = True
    should_process_only_by_key_release: bool = True

@dataclass
class SessionEvent:
    """Represents events that occur during a screen capture session"""
    type: EventType
    project_uuid: str
    command_uuid: str
    timestamp: datetime
    description: str
    key_char: Optional[str] = None
    key_code: Optional[str] = None
    mouse_x: Optional[int] = None
    mouse_y: Optional[int] = None
    is_special_key: bool = False

@dataclass
class ScreenshotEvent:
    """Represents a screen capture with its metadata"""
    event_id: str
    project_uuid: str
    command_uuid: str
    timestamp: datetime
    description: str
    screenshot_path: str  # This is now required since this event is only for captures
    annotation_path: Optional[str] = None
    mouse_x: Optional[int] = None
    mouse_y: Optional[int] = None
    mouse_event_tool_tip: Optional[str] = None
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
    session_events: List[SessionEvent] = None  # For storing session events
    screenshot_events: List[ScreenshotEvent] = None  # For storing screenshot events
    key_capture_config: KeyCaptureConfig = None
    
    def __post_init__(self):
        """Initialize event lists after dataclass initialization"""
        self.session_events = []
        self.screenshot_events = []
        self.key_capture_config = KeyCaptureConfig()
    @property
    def duration(self) -> Optional[float]:
        """Calculate session duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return None

    def add_screenshot_event(self, event: ScreenshotEvent) -> None:
        """Add a screenshot event to the session"""
        self.screenshot_events.append(event)

    def add_session_event(self, event: SessionEvent) -> None:
        """Add a session event to the session"""
        self.session_events.append(event)

    def get_statistics(self) -> SessionStatistics:
        """Get statistics for the current session based on captured events"""
        stats = SessionStatistics(
            project_uuid=self.project_uuid,
            command_uuid=self.command_uuid,
            start_time=self.start_time,
            end_time=self.end_time
        )
        
        # Calculate statistics from both event lists
        screenshot_paths = set()
        annotated_paths = set()
        key_events = 0
        mouse_events = 0
        
        # Process screenshot events
        for event in self.screenshot_events:
            if event.screenshot_path:
                screenshot_paths.add(event.screenshot_path)
                if event.annotation_path:
                    annotated_paths.add(event.annotation_path)

        # Process session events
        for event in self.session_events:
            if event.type == EventType.KEY_PRESS:
                key_events += 1
            elif event.type == EventType.MOUSE_CLICK:
                mouse_events += 1
        
        # Update statistics
        stats.total_screenshots = len(screenshot_paths)
        stats.total_annotations = len(annotated_paths)
        stats.total_key_events = key_events
        stats.total_mouse_events = mouse_events
        
        # Calculate directory sizes
        if self.raw_dir and os.path.exists(self.raw_dir):
            stats.raw_directory_size = sum(
                os.path.getsize(path) for path in screenshot_paths if os.path.exists(path)
            )
        
        if self.annotated_dir and os.path.exists(self.annotated_dir):
            stats.annotated_directory_size = sum(
                os.path.getsize(path) for path in annotated_paths if os.path.exists(path)
            )
            
        if self.start_time:
            end = self.end_time if self.end_time else datetime.now()
            stats.duration_seconds = (end - self.start_time).total_seconds()
            
        return stats

class ScreenCaptureService(BaseService[List[ScreenshotEvent]]):
    """Service for capturing screen interactions with annotation capability.
    Notifies observers about changes to the screenshot event list."""
    
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

    def export_screenshot_events_to_json(self) -> str:
        """Export screenshot events to a JSON file.
        
        Returns:
            str: Path to the exported JSON file
        
        Raises:
            SessionError: If no session exists or is not properly initialized
            DirectoryError: If unable to create or write to export directory
        """
        try:
            
            if not self.current_session or not self.current_session.screenshot_events:
                raise SessionError("No screenshot events to export")

            # Create export path under screenshots directory
            base_dir = os.path.join('data', self.current_session.project_uuid, 
                                  self.current_session.command_uuid)
            os.makedirs(base_dir, exist_ok=True)
            
            export_path = os.path.join(base_dir, f'screenshot_events_{self.current_session.command_uuid}.json')
            
            # Convert events to serializable format
            events_data = []
            for event in self.current_session.screenshot_events:
                event_dict = asdict(event)
                # Convert datetime to ISO format string
                event_dict['timestamp'] = event_dict['timestamp'].isoformat()
                events_data.append(event_dict)
            
            # Write to JSON file with proper formatting
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(events_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Screenshot events exported to: {export_path}")
            return export_path
            
        except (SessionError, DirectoryError) as e:
            logger.error(f"Failed to export screenshot events: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during screenshot events export: {str(e)}")
            raise DirectoryError(f"Screenshot events export failed: {str(e)}")

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

    def _create_session_event(self, event_type: EventType, description: str, **kwargs) -> Optional[SessionEvent]:
        """Create a session event with current session context"""
        if not self.current_session or not self.current_session.is_active:
            return None
        
        self._increment_event_stat(event_type)
        
        event = SessionEvent(
            type=event_type,
            project_uuid=self.current_session.project_uuid,
            command_uuid=self.current_session.command_uuid,
            timestamp=datetime.now(),
            description=description,
            **kwargs
        )
        
        # Add event to session's events list
        self.current_session.add_session_event(event)
        return event

    def _create_capture_event(self, description: str, screenshot_path: str, **kwargs) -> Optional[ScreenshotEvent]:
        """Create a screen capture event"""
        if not self.current_session or not self.current_session.is_active:
            return None
        
        event = ScreenshotEvent(
            event_id=str(uuid.uuid4()),
            project_uuid=self.current_session.project_uuid,
            command_uuid=self.current_session.command_uuid,
            timestamp=datetime.now(),
            description=description,
            screenshot_path=screenshot_path,
            **kwargs
        )
        
        # Add event to session's screenshots list
        self.current_session.add_screenshot_event(event)
        return event

    def _take_screenshot(self, event_description: str, x: Optional[int] = None, y: Optional[int] = None, 
                       key_char: Optional[str] = None, key_code: Optional[str] = None, 
                       is_special_key: bool = False, mouse_event_tool_tip: Optional[str] = None) -> str:
        """Take a screenshot and create a capture event"""
        try:
            self._validate_session()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f'screenshot_{timestamp}.png'
            if not self.current_session or not self.current_session.raw_dir:
                raise SessionError("Session raw directory not initialized")
            filepath = os.path.join(str(self.current_session.raw_dir), filename)
            
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
            except Exception as e:
                raise CaptureError(f"Failed to capture or save screenshot: {str(e)}")
            
            logger.debug(f"Screenshot saved: {filepath}")
            
            # Create capture event with any provided input context
            event = self._create_capture_event(
                description=event_description,
                screenshot_path=filepath,
                mouse_x=x,
                mouse_y=y,
                key_char=key_char,
                key_code=key_code,
                is_special_key=is_special_key,
                mouse_event_tool_tip=mouse_event_tool_tip
            )
            if event:
                # Instead of notifying for each event, notify about the updated list
                self.notify_session_observers()
            
            return filepath
        except Exception as e:
            logger.error(f"Screenshot capture failed: {str(e)}")
            raise

    def _on_key_event_handler(self, key):
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
        
        should_capture = False
        if self.current_session and self.current_session.key_capture_config and self.current_session.key_capture_config.is_capture_enabled:
            if self.current_session.key_capture_config.is_normal_key_capture_enabled and not is_special:
                should_capture = True
            elif self.current_session.key_capture_config.is_special_key_capture_enabled and is_special:
                should_capture = True
        
        if key == keyboard.Key.esc:
            should_capture = True
            
        if should_capture:
            # Create key press session event
            self._create_session_event(
                event_type=EventType.KEY_PRESS,
                description=event_desc,
                key_char=key_char,
                key_code=str(key),
                is_special_key=is_special
            )
            
            # Take screenshot with key context
            self._take_screenshot(
                event_description=event_desc,
                key_char=key_char,
                key_code=str(key),
                is_special_key=is_special
            )
        else:
            logger.debug(f"Key event {event_desc} not captured, disabled by config")
        
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
            
            # Extract the button information for tooltip
            # Default to "Left Button" if button is None or not parsable
            try:
                mouse_tooltip = f"{button}"
                # Handle case where button might be None or empty
                if not mouse_tooltip or mouse_tooltip.lower() == "none":
                    mouse_tooltip = "Left Click"
            except:
                mouse_tooltip = "Left Click"
            
            # Create mouse click session event
            self._create_session_event(
                event_type=EventType.MOUSE_CLICK,
                description=event_desc,
                mouse_x=x,
                mouse_y=y
            )
            
            # Take screenshot with mouse context
            self._take_screenshot(
                event_description=event_desc,
                x=x,
                y=y,
                mouse_event_tool_tip=mouse_tooltip
            )

    def _annotate_screenshot(self, event: ScreenshotEvent, x: Optional[int] = None, y: Optional[int] = None, 
                           text: Optional[str] = None):
        """Create an annotated version of the screenshot"""
        screenshot_path = event.screenshot_path
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
            event.annotation_path = annotated_path
            
            # Create annotation event
            self._create_session_event(
                event_type=EventType.ANNOTATION,
                description=f"Screenshot annotated: {os.path.basename(screenshot_path)}",
            )
                
        except Exception as e:
            logger.error(f"Failed to annotate screenshot: {str(e)}")

    def pre_start_capture(self, project_uuid: str, command_uuid: str) -> None:
        """Pre-start capture setup
        
        This method is called before the capture starts.
        It can be used to perform any necessary setup or checks before the capture starts.
        
        Maximise chrome browser window
        """
        try:
            # Maximise chrome browser window
            self.maximise_chrome_browser_window()
        except Exception as e:
            logger.error(f"Failed to maximise chrome browser window: {str(e)}")
            raise
        
    def maximise_chrome_browser_window(self) -> None:
        """Maximise chrome browser window"""
        try:
            # Maximise chrome browser window using chrome robot
            from robot.chrome_robot import ChromeRobot
            chrome_robot = ChromeRobot()
            chrome_robot.maximize_window()
            logger.info("Maximised chrome browser window")
        except Exception as e:
            logger.error(f"Failed to maximise chrome browser window: {str(e)}")
            raise
        
    
    def start_capture(self, project_uuid: str, command_uuid: str) -> None:
        """Start capturing screenshots for a specific command"""
        self.pre_start_capture(project_uuid, command_uuid)
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
                    if self.current_session.key_capture_config.should_process_only_by_key_release:
                        self.current_session.keyboard_listener = keyboard.Listener(
                            on_release=self._on_key_event_handler
                        )
                    else:
                        self.current_session.keyboard_listener = keyboard.Listener(
                            on_press=self._on_key_event_handler
                        )
                    self.current_session.mouse_listener = mouse.Listener(on_click=self._on_click)
                    
                    self.current_session.keyboard_listener.start()
                    self.current_session.mouse_listener.start()
                except Exception as e:
                    raise SessionError(f"Failed to initialize input listeners: {str(e)}")
                
                # Create session start event
                event = self._create_session_event(
                    event_type=EventType.CAPTURE_STARTED,
                    description=f"Screen capture started for project: {project_uuid}, command: {command_uuid}"
                )
                if event:
                    self.set_state('capturing', True)
                    
                self.notify_session_observers()
                    
            except Exception as e:
                self.current_session = None
                logger.error(f"Failed to start capture: {str(e)}")
                raise

    def create_session_summary(self, show_preview: bool = False) -> Optional[str]:
        """Create a visual summary of all screenshots and annotations in the current session."""
        try:
            self._validate_session()
            
            # Get screenshots with their annotations
            screenshot_pairs = []
            for event in self.current_session.screenshot_events:
                if event.screenshot_path:
                    screenshot_pairs.append((event.screenshot_path, event.annotation_path))
            
            if not screenshot_pairs:
                logger.warning("No screenshots found for session summary")
                return None
            
            # Sort screenshots by timestamp to maintain order
            screenshot_pairs.sort(key=lambda x: os.path.basename(x[0])) # type: ignore
            
            # Create a grid layout
            n_images = len(screenshot_pairs) * 2  # Both raw and annotated versions
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
            for idx, (raw_path, annotated_path) in enumerate(screenshot_pairs):
                # Position for raw screenshot
                row = (idx * 2) // grid_size
                col = (idx * 2) % grid_size
                x = col * (thumb_width + padding)
                y = row * (thumb_height + padding)
                
                try:
                    if os.path.exists(raw_path):
                        # Add raw screenshot
                        raw_img = Image.open(raw_path)
                        raw_thumb = raw_img.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
                        canvas.paste(raw_thumb, (x, y))
                        draw.text((x + 5, y + 5), f"Raw #{idx + 1}", fill='red', font=font)
                    
                    # Add annotated version if it exists
                    if annotated_path and os.path.exists(annotated_path):
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
        """Stop the current capture session and process annotations"""
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
                
                # Process all screenshots and create annotations
                for event in self.current_session.screenshot_events:
                    if isinstance(event, ScreenshotEvent) and event.screenshot_path:
                        if event.mouse_x is not None and event.mouse_y is not None:
                            self._annotate_screenshot(event, event.mouse_x, event.mouse_y, event.description)
                        else:
                            self._annotate_screenshot(event, text=event.description)
                
                # Create session summary
                summary_path = self.create_session_summary()
                
                self.current_session.is_active = False
                self.current_session.end_time = datetime.now()
                
                # Include summary path in stop event if available
                event_desc = f"Screen capture stopped after {self.current_session.duration:.2f} seconds"
                if summary_path:
                    event_desc += f"\nSummary available at: {summary_path}"
                
                # Create session stop event
                event = self._create_session_event(
                    event_type=EventType.CAPTURE_STOPPED,
                    description=event_desc
                )
                if event:
                    self.set_state('capturing', False)
                
                # Save session statistics before clearing
                if self.current_session:
                    stats = self.current_session.get_statistics()
                    stats.total_key_events = self._event_stats[EventType.KEY_PRESS]
                    stats.total_mouse_events = self._event_stats[EventType.MOUSE_CLICK]
                    self._session_history.append(stats)
                    
                self.notify_session_observers()
                # export screenshot events list to a json file
                self.export_screenshot_events_to_json()
                
            except Exception as e:
                logger.error(f"Error during capture stop: {str(e)}")
                raise

    def stop_capture_special_click_event_from_client_input(self) -> None:
        """Stop the current capture session and process annotations, removing the last event (client's stop click)"""
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
                
                # Remove the latest event which would be the click that initiated the stop request
                if self.current_session.screenshot_events and len(self.current_session.screenshot_events) > 0:
                    logger.info("Removing last screenshot event that triggered the stop capture")
                    # delete the last screenshot file
                    if self.current_session.screenshot_events[-1].screenshot_path:
                        os.remove(self.current_session.screenshot_events[-1].screenshot_path)
                    self.current_session.screenshot_events.pop()
                
                # Process all screenshots and create annotations
                for event in self.current_session.screenshot_events:
                    if isinstance(event, ScreenshotEvent) and event.screenshot_path:
                        if event.mouse_x is not None and event.mouse_y is not None:
                            self._annotate_screenshot(event, event.mouse_x, event.mouse_y, event.description)
                        else:
                            self._annotate_screenshot(event, text=event.description)
                
                # Create session summary
                summary_path = self.create_session_summary()
                
                self.current_session.is_active = False
                self.current_session.end_time = datetime.now()
                
                # Include summary path in stop event if available
                event_desc = f"Screen capture stopped after {self.current_session.duration:.2f} seconds"
                if summary_path:
                    event_desc += f"\nSummary available at: {summary_path}"
                
                # Create session stop event
                event = self._create_session_event(
                    event_type=EventType.CAPTURE_STOPPED,
                    description=event_desc
                )
                if event:
                    self.set_state('capturing', False)
                
                # Save session statistics before clearing
                if self.current_session:
                    stats = self.current_session.get_statistics()
                    stats.total_key_events = self._event_stats[EventType.KEY_PRESS]
                    stats.total_mouse_events = self._event_stats[EventType.MOUSE_CLICK]
                    self._session_history.append(stats)
                    
                self.notify_session_observers()
                # export screenshot events list to a json file
                self.export_screenshot_events_to_json()
                
            except Exception as e:
                logger.error(f"Error during capture stop: {str(e)}")
                raise

    def update_screenshot_events_json_file(self, project_uuid: str, command_uuid: str, 
                                        updated_events: Optional[List[ScreenshotEvent]] = None,
                                        deleted_events_ids: Optional[List[str]] = None) -> List[ScreenshotEvent]:
        """Update screenshot events after client-side editing.
        
        This method:
        1. Loads the existing screenshot events from the JSON file
        2. If deleted_events_ids provided:
           - Deletes screenshots and annotations from filesystem for those events
           - Updates the JSON with remaining events
        3. If updated_events provided:
           - Merges updates with existing events (replacing events with same ID)
           - Identifies and removes events that exist in original but not in updated list
        
        Args:
            project_uuid: Project identifier
            command_uuid: Command identifier
            updated_events: List of updated screenshot events (with edited tooltips etc.)
            deleted_events_ids: List of event ids to delete (for backward compatibility)
        
        Returns:
            List[ScreenshotEvent]: Updated list of screenshot events
        
        Raises:
            DirectoryError: If directory operations fail
            SessionError: If event data is invalid
        """
        try:
            if not self.current_session or not self.current_session.screenshot_events:
                raise SessionError("No screenshot events to export")
            
            base_dir = os.path.join('data', project_uuid, command_uuid)
            if not os.path.exists(base_dir):
                raise DirectoryError(f"Directory not found for project {project_uuid}, command {command_uuid}")
            
            json_path = os.path.join(base_dir, f'screenshot_events_{command_uuid}.json')
            
            # Load existing events from JSON file
            if not os.path.exists(json_path):
                raise SessionError(f"Screenshot events file not found: {json_path}")
            
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    original_events_data = json.load(f)
            except json.JSONDecodeError as e:
                raise SessionError(f"Invalid JSON in screenshot events file: {str(e)}")
            
            # For backward compatibility: Handle deleted_events_ids
            if deleted_events_ids:
                # Delete files and filter events
                new_events_data = []
                for event_dict in original_events_data:
                    if event_dict['event_id'] in deleted_events_ids:
                        if event_dict['screenshot_path'] and os.path.exists(event_dict['screenshot_path']):
                            os.remove(event_dict['screenshot_path'])
                        if event_dict['annotation_path'] and os.path.exists(event_dict['annotation_path']):
                            os.remove(event_dict['annotation_path'])
                    else:
                        new_events_data.append(event_dict)
                
                logger.info(f"Deleted {len(deleted_events_ids)} events from {project_uuid}/{command_uuid}")
            
            # Handle updated events (includes tooltip edits)
            elif updated_events:
                # Create a map of original events by ID for quick lookups
                original_events_by_id = {event['event_id']: event for event in original_events_data}
                
                # Convert updated events to dict format
                updated_events_data = []
                updated_event_ids = set()
                
                for event in updated_events:
                    event_dict = asdict(event)
                    # Convert datetime to ISO format string if it's a datetime object
                    if isinstance(event_dict['timestamp'], datetime):
                        event_dict['timestamp'] = event_dict['timestamp'].isoformat()
                    updated_events_data.append(event_dict)
                    updated_event_ids.add(event_dict['event_id'])
                
                # Find events that were deleted (in original but not in updated)
                deleted_ids = set(original_events_by_id.keys()) - updated_event_ids
                
                # Delete files for events that were removed
                for event_id in deleted_ids:
                    event_dict = original_events_by_id[event_id]
                    if event_dict['screenshot_path'] and os.path.exists(event_dict['screenshot_path']):
                        os.remove(event_dict['screenshot_path'])
                    if event_dict['annotation_path'] and os.path.exists(event_dict['annotation_path']):
                        os.remove(event_dict['annotation_path'])
                
                new_events_data = updated_events_data
                logger.info(f"Updated {len(updated_events)} events for {project_uuid}/{command_uuid}")
                logger.info(f"Deleted {len(deleted_ids)} events that were removed")
            else:
                # No updates or deletions specified
                logger.warning("No updates or deletions specified in update request")
                new_events_data = original_events_data
            
            # Write updated event data back to file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(new_events_data, f, indent=2, ensure_ascii=False)
                
            # Convert JSON data back to ScreenshotEvent objects
            updated_events_list = []
            for event_dict in new_events_data:
                # Convert ISO format string back to datetime if needed
                if isinstance(event_dict.get('timestamp'), str):
                    event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
                event = ScreenshotEvent(**event_dict)
                updated_events_list.append(event)
            
            logger.info(f"Successfully updated screenshot events for {project_uuid}/{command_uuid}")
            self.current_session.screenshot_events = updated_events_list
            return updated_events_list
            
        except Exception as e:
            logger.error(f"Failed to update screenshot events: {str(e)}")
            raise DirectoryError(f"Screenshot events update failed: {str(e)}")

    def notify_session_observers(self):
        """Notify observers with the current list of screenshots"""
        if self.current_session:
            self.notify_observers(self.current_session.screenshot_events)

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