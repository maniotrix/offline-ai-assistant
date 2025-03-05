import logging
import threading
import time
import os
from robot.utils import open_default_system_bboxes_url_maximized, CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH

def open_browser_and_get_system_bboxes(max_retries=5, retry_delay=2):
    """
    Opens the browser with retry logic in a separate thread
    """
    def _open_browser():
        for attempt in range(max_retries):
            try:
                # Wait for server to start
                time.sleep(retry_delay)
                # check if chrome_system_bounding_boxes.json exists
                if not os.path.exists(CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH):
                    logging.info("Opening browser...")
                    open_default_system_bboxes_url_maximized()
                    logging.info("Successfully opened browser")
                    break
                else:
                    logging.info("Chrome system bounding boxes already exists...skipping getting system bounding boxes")
                    break
            except Exception as e:
                if attempt < max_retries - 1:
                    logging.warning(f"Failed to open browser (attempt {attempt + 1}): {e}")
                    time.sleep(retry_delay)
                else:
                    logging.error(f"Failed to open browser after {max_retries} attempts: {e}")

    # Start browser opening in a separate thread
    browser_thread = threading.Thread(target=_open_browser, daemon=True)
    browser_thread.start()
    return browser_thread 