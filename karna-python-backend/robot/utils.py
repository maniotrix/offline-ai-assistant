import os
import subprocess
import platform
import webbrowser
from pathlib import Path
import json
import time
import urllib.parse
import requests
from urllib.error import URLError

CHROME_SYSTEM_BOUNDING_BOXES_HTML_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'calculate_chrome_system_bboxes.html')
CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'chrome_system_bounding_boxes.json')
# its the url of html file served as static file in backend
CHROME_SYSTEM_BOUNDING_BOXES_URL = "http://localhost:8000/data/calculate_chrome_system_bboxes.html"

# ===== Utils =====
def open_html_in_chrome(html_file_path):
    """
    Opens an HTML file in Chrome browser.
    
    Args:
        html_file_path (str): Path to the HTML file to open
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        FileNotFoundError: If the HTML file doesn't exist
        Exception: For other errors during opening
    """
    try:
        # Convert to absolute path and check if file exists
        html_path = Path(html_file_path).resolve()
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_path}")
        
        # Convert to file URI
        file_uri = f"file://{html_path}"
        
        # Determine the operating system and use appropriate method
        system = platform.system()
        
        if system == "Windows":
            # Try to find Chrome in common locations
            chrome_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break
            
            if chrome_path:
                subprocess.Popen([chrome_path, file_uri])
            else:
                # Fallback to webbrowser module
                webbrowser.get('chrome').open(file_uri)
                
        elif system == "Darwin":  # macOS
            chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            if os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, file_uri])
            else:
                # Fallback to webbrowser module
                webbrowser.get('chrome').open(file_uri)
                
        elif system == "Linux":
            # Try common Chrome executable names on Linux
            chrome_candidates = ['google-chrome', 'chrome', 'chromium', 'chromium-browser']
            
            for candidate in chrome_candidates:
                try:
                    subprocess.Popen([candidate, file_uri])
                    break
                except FileNotFoundError:
                    continue
            else:
                # Fallback to webbrowser module
                webbrowser.get('chrome').open(file_uri)
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error opening HTML file in Chrome: {e}")
        return False

def open_default_system_bboxes_html():
    """
    Opens the default system bboxes HTML file in Chrome.
    """
    open_html_in_chrome(CHROME_SYSTEM_BOUNDING_BOXES_HTML_FILE_PATH)
    
def open_default_system_bboxes_url(max_retries=3, retry_delay=2):
    """
    Opens the default system bboxes URL in Chrome.
    
    Args:
        max_retries (int): Maximum number of retry attempts if opening fails
        retry_delay (int): Delay in seconds between retries
        
    Returns:
        bool: True if successful, False otherwise
    """
    def validate_url(url):
        """Validate if URL is properly formatted and accessible"""
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    try:
        # Validate URL format
        if not validate_url(CHROME_SYSTEM_BOUNDING_BOXES_URL):
            print(f"Error: Invalid URL format: {CHROME_SYSTEM_BOUNDING_BOXES_URL}")
            return False
            
        # Try to open URL with retries
        for attempt in range(max_retries):
            try:
                # Check if server is accessible
                requests.head(CHROME_SYSTEM_BOUNDING_BOXES_URL, timeout=5)
                
                # Try to open specifically in Chrome
                if platform.system() == "Windows":
                    chrome_paths = [
                        os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
                        os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
                        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
                    ]
                    
                    for path in chrome_paths:
                        if os.path.exists(path):
                            # Add --start-maximized flag to ensure Chrome opens maximized
                            subprocess.Popen([path, '--start-maximized', CHROME_SYSTEM_BOUNDING_BOXES_URL])
                            return True
                            
                # Fallback to system default Chrome
                browser = webbrowser.get('chrome')
                browser.open(CHROME_SYSTEM_BOUNDING_BOXES_URL)
                return True
                
            except (requests.RequestException, webbrowser.Error) as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to open URL after {max_retries} attempts: {str(e)}")
                    return False
                    
    except Exception as e:
        print(f"Unexpected error opening system bboxes URL: {str(e)}")
        return False

def generate_system_bounding_boxes(results):
    """
    Generates the system bounding boxes JSON file.
    
    Args:
        results (dict or list): The bounding box data to be saved as JSON.
            Expected to contain valid JSON-serializable data.
            
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        TypeError: If results is not a valid JSON-serializable type
        IOError: If there's an issue writing to the file
    """
    if results is None:
        print("Error: Cannot save None results to bounding boxes file")
        return False
        
    try:
        # Ensure the directory exists
        output_dir = os.path.dirname(CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH)
        os.makedirs(output_dir, exist_ok=True)
        
        # Validate that results is JSON serializable
        try:
            json.dumps(results)
        except (TypeError, OverflowError) as e:
            print(f"Error: Results contain non-JSON-serializable data: {e}")
            return False
            
        # Write to a temporary file first to avoid corrupting the original file
        # in case of write errors
        temp_file_path = f"{CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH}.tmp"
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)  # Use indentation for better readability
            
        # Rename the temporary file to the target file (atomic operation)
        os.replace(temp_file_path, CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH)
        
        print(f"Successfully saved bounding boxes to {CHROME_SYSTEM_BOUNDING_BOXES_JSON_FILE_PATH}")
        return True
        
    except IOError as e:
        print(f"Error writing to bounding boxes file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error generating system bounding boxes: {e}")
        return False

def open_chrome_maximized_then_navigate(url_or_file_path, wait_time=2.0):
    """
    Opens Chrome on Windows by pressing the Windows key, typing "Google Chrome",
    selecting the first profile, and maximizing the window before navigating to the URL.
    
    Args:
        url_or_file_path (str): URL or file path to open in Chrome
        wait_time (float): Time to wait between actions in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    from .robot import Robot
    import os
    import platform
    
    # Check if running on Windows
    if platform.system() != "Windows":
        print("This function currently only supports Windows.")
        return False
    
    try:
        # Determine if input is a file path or URL
        is_file = os.path.exists(url_or_file_path)
        
        # Convert file path to URL if needed
        if is_file:
            from pathlib import Path
            file_path = Path(url_or_file_path).resolve()
            url = f"file://{file_path}"
        else:
            url = url_or_file_path
            
        # Initialize robot
        robot = Robot()
        
        # Press Windows key
        robot.press_key('win')
        robot.wait(wait_time)
        
        # Type "Google Chrome"
        robot.type_text("Google Chrome")
        robot.wait(wait_time)
        
        # Press Enter to launch Chrome
        robot.press_key('enter')
        robot.wait(wait_time * 2)  # Wait longer for Chrome to start
        
        # Press Tab to select the first profile (if profile selection appears)
        robot.press_key('tab')
        robot.wait(0.5)
        
        # Press Space to open the selected profile
        robot.press_key('space')
        robot.wait(wait_time * 2)  # Wait for Chrome to fully open
        
        # Press Windows + Up arrow to maximize
        robot.hotkey('win', 'up')
        robot.wait(wait_time)
        
        # Open new tab
        robot.hotkey('ctrl', 't')
        robot.wait(1)
        
        # Focus on the address bar with Ctrl+L
        robot.hotkey('ctrl', 'l')
        robot.wait(0.5)
        
        # Clear any existing text
        robot.hotkey('ctrl', 'a')
        robot.wait(0.2)
        
        # Type the URL
        robot.type_text(url)
        robot.wait(0.2)
        
        # Press Enter to navigate
        robot.press_key('enter')
        
        return True
        
    except Exception as e:
        print(f"Error opening Chrome and navigating: {str(e)}")
        return False

def open_default_system_bboxes_html_maximized():
    """
    Opens the default system bboxes HTML file in Chrome with a maximized window.
    """
    return open_chrome_maximized_then_navigate(CHROME_SYSTEM_BOUNDING_BOXES_HTML_FILE_PATH)
    
def open_default_system_bboxes_url_maximized():
    """
    Opens the default system bboxes URL in Chrome with a maximized window.
    """
    return open_chrome_maximized_then_navigate(CHROME_SYSTEM_BOUNDING_BOXES_URL)

if __name__ == "__main__":
    # Example usage
    # open_default_system_bboxes_html()
    open_chrome_maximized_then_navigate("https://www.google.com")
