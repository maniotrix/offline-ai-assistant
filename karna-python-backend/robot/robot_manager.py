import logging
import threading
import time
import os
from typing import Callable, Any, Optional
from robot.utils import open_default_system_bboxes_url_maximized, CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH

class TaskManager:
    """
    A generic task manager class that can execute tasks in separate threads.
    This class provides functionality to run any task in a background thread
    with retry logic.
    """
    
    def __init__(self):
        """Initialize the TaskManager."""
        self.threads = {}
        self.logger = logging.getLogger(__name__)
    
    def execute_in_thread(self, 
                         task_func: Callable[..., Any], 
                         task_name: str = "task",
                         max_retries: int = 5, 
                         retry_delay: int = 2,
                         daemon: bool = True,
                         *args, 
                         **kwargs) -> threading.Thread:
        """
        Execute a function in a separate thread with retry logic.
        
        Args:
            task_func: The function to execute
            task_name: A name for the task (used for logging and thread identification)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay in seconds between retries
            daemon: Whether the thread should be a daemon thread
            *args: Positional arguments to pass to the task function
            **kwargs: Keyword arguments to pass to the task function
            
        Returns:
            threading.Thread: The thread object running the task
        """
        def _execute_with_retry():
            for attempt in range(max_retries):
                try:
                    # Wait before starting the attempt
                    time.sleep(retry_delay)
                    
                    self.logger.info(f"Executing {task_name} (attempt {attempt + 1})...")
                    result = task_func(*args, **kwargs)
                    self.logger.info(f"Successfully executed {task_name}")
                    return result
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"Failed to execute {task_name} (attempt {attempt + 1}): {e}")
                        time.sleep(retry_delay)
                    else:
                        self.logger.error(f"Failed to execute {task_name} after {max_retries} attempts: {e}")
        
        # Create and start the thread
        thread = threading.Thread(target=_execute_with_retry, daemon=daemon)
        thread.start()
        
        # Store the thread for future reference
        self.threads[task_name] = thread
        
        return thread
    
    def wait_for_task(self, task_name: str, timeout: Optional[float] = None) -> bool:
        """
        Wait for a specific task to complete.
        
        Args:
            task_name: The name of the task to wait for
            timeout: Maximum time to wait in seconds (None means wait indefinitely)
            
        Returns:
            bool: True if the task completed, False if it timed out or wasn't found
        """
        if task_name not in self.threads:
            self.logger.warning(f"Task '{task_name}' not found")
            return False
            
        thread = self.threads[task_name]
        thread.join(timeout)
        
        if thread.is_alive():
            self.logger.warning(f"Task '{task_name}' did not complete within the timeout")
            return False
            
        return True
    
    def is_task_running(self, task_name: str) -> bool:
        """
        Check if a specific task is still running.
        
        Args:
            task_name: The name of the task to check
            
        Returns:
            bool: True if the task is running, False otherwise
        """
        if task_name not in self.threads:
            return False
            
        return self.threads[task_name].is_alive()


class RobotManager(TaskManager):
    """
    A specialized task manager for browser-related operations.
    Inherits from TaskManager and adds browser-specific functionality.
    """
    
    def __init__(self):
        """Initialize the BrowserManager."""
        super().__init__()
    
    def open_browser_and_get_system_bboxes(self, max_retries: int = 5, retry_delay: int = 2) -> threading.Thread:
        """
        Opens the browser with retry logic in a separate thread to get system bounding boxes.
        
        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Delay in seconds between retries
            
        Returns:
            threading.Thread: The thread object running the browser task
        """
        def _open_browser():
            # check if chrome_system_bounding_boxes.json exists
            if not os.path.exists(CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH):
                logging.info("Opening browser...")
                open_default_system_bboxes_url_maximized()
                logging.info("Successfully opened browser")
            else:
                logging.info("Chrome system bounding boxes already exists...skipping getting system bounding boxes")
        
        return self.execute_in_thread(
            task_func=_open_browser,
            task_name="browser_system_bboxes",
            max_retries=max_retries,
            retry_delay=retry_delay
        )


# For backward compatibility
def open_browser_and_get_system_bboxes(max_retries=5, retry_delay=2):
    """
    Legacy function for backward compatibility.
    Opens the browser with retry logic in a separate thread.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay in seconds between retries
        
    Returns:
        threading.Thread: The thread object running the browser task
    """
    browser_manager = RobotManager()
    return browser_manager.open_browser_and_get_system_bboxes(max_retries, retry_delay) 