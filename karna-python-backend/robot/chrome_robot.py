import logging
import os
import platform
from typing import Optional
from pathlib import Path
import webbrowser
import subprocess

from windows_robot import WindowsRobot, Point, Region

logger = logging.getLogger(__name__)

class ChromeRobot(WindowsRobot):
    """
    A specialized robot class for Chrome browser automation.
    Inherits from the WindowsRobot class and adds Chrome-specific functionality.
    """
    
    def __init__(self):
        """Initialize the ChromeRobot with the WindowsRobot functionality."""
        super().__init__()
    
    # ===== Browser Window Management =====
    
    def maximize_active_window(self) -> None:
        """Maximize the active window (Windows+Up)."""
        self.press_win_key('up')
        logger.debug("Maximized active window")
    
    def minimize_active_window(self) -> None:
        """Minimize the active window (Windows+Down)."""
        self.press_win_key('down')
        logger.debug("Minimized active window")
    
    def snap_window_left(self) -> None:
        """Snap the active window to the left (Windows+Left)."""
        self.press_win_key('left')
        logger.debug("Snapped window left")
    
    def snap_window_right(self) -> None:
        """Snap the active window to the right (Windows+Right)."""
        self.press_win_key('right')
        logger.debug("Snapped window right")
    
    def maximize_window(self, wait_time: float = 2.0) -> bool:
        """
        Maximize the current window using Windows+Up shortcut.
        
        Args:
            wait_time: Time to wait after maximizing
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Press Windows + Up arrow to maximize
            self.maximize_active_window()
            self.wait(wait_time)
            logger.debug("Window maximized")
            return True
        except Exception as e:
            logger.error(f"Failed to maximize window: {str(e)}")
            return False
    
    # ===== Tab Management =====
    
    def new_tab(self) -> None:
        """Open a new tab (Ctrl+T)."""
        self.press_ctrl_key('t')
        logger.debug("Opened new tab")
    
    def close_tab(self) -> None:
        """Close current tab (Ctrl+W)."""
        self.press_ctrl_key('w')
        logger.debug("Closed current tab")
    
    def close_current_tab(self) -> None:
        """Close the current tab (Ctrl+W)."""
        self.close_tab()
    
    def switch_to_next_tab(self) -> None:
        """Switch to the next tab (Ctrl+Tab)."""
        self.hotkey('ctrl', 'tab')
        logger.debug("Switched to next tab")
    
    def switch_to_previous_tab(self) -> None:
        """Switch to the previous tab (Ctrl+Shift+Tab)."""
        self.hotkey('ctrl', 'shift', 'tab')
        logger.debug("Switched to previous tab")
    
    def focus_address_bar(self) -> None:
        """Focus on the browser address bar (Ctrl+L)."""
        self.press_ctrl_key('l')
        logger.debug("Focused on address bar")
    
    # ===== Navigation =====
    
    def open_url_in_new_tab(self, url: str, wait_time: float = 1.0) -> bool:
        """
        Navigate to a URL in a new browser tab.
        
        Args:
            url: URL to navigate to
            wait_time: Time to wait between actions in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open new tab
            self.new_tab()
            self.wait(wait_time)
            
            # Navigate to URL in the current tab
            return self.navigate_in_current_tab(url, wait_time)
        except Exception as e:
            logger.error(f"Failed to navigate to URL: {str(e)}")
            return False
    
    def navigate_in_current_tab(self, url: str, wait_time: float = 0.5) -> bool:
        """
        Navigate to a URL in the current browser tab.
        
        Args:
            url: URL to navigate to
            wait_time: Time to wait between actions in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Focus on the address bar
            self.focus_address_bar()
            self.wait(wait_time)
            
            # Clear any existing text
            self.select_all()
            self.wait(0.2)
            
            # Type the URL
            self.type_text(url)
            self.wait(0.2)
            
            # Press Enter to navigate
            self.press_enter()
            
            logger.debug(f"Navigated to URL in current tab: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate in current tab: {str(e)}")
            return False
    
    def refresh_page(self) -> None:
        """Refresh the current page (F5)."""
        self.press_key('f5')
        logger.debug("Page refreshed")
    
    def go_back(self) -> None:
        """Go back to the previous page (Alt+Left)."""
        self.press_alt_key('left')
        logger.debug("Navigated back")
    
    def go_forward(self) -> None:
        """Go forward to the next page (Alt+Right)."""
        self.press_alt_key('right')
        logger.debug("Navigated forward")
    
    # ===== Zoom Control =====
    
    def zoom_in(self) -> None:
        """Zoom in on the page (Ctrl++)."""
        self.press_ctrl_key('+')
        logger.debug("Zoomed in")
    
    def zoom_out(self) -> None:
        """Zoom out on the page (Ctrl+-)."""
        self.press_ctrl_key('-')
        logger.debug("Zoomed out")
    
    def reset_zoom(self) -> None:
        """Reset zoom to 100% (Ctrl+0)."""
        self.press_ctrl_key('0')
        logger.debug("Zoom reset to 100%")
    
    # ===== Chrome Launch and Navigation =====
    
    def open_windows_search(self) -> None:
        """Open Windows search (Windows key)."""
        self.press_key('win')
        logger.debug("Opened Windows search")
    
    def search_and_launch_app(self, app_name: str, wait_time: float = 2.0) -> bool:
        """
        Search for and launch an application using Windows search.
        
        Args:
            app_name: Name of the application to search for
            wait_time: Time to wait between actions in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open Windows search
            self.open_windows_search()
            self.wait(wait_time)
            
            # Type the app name
            self.type_text(app_name)
            self.wait(wait_time)
            
            # Press Enter to launch the first result
            self.press_enter()
            self.wait(wait_time)
            
            logger.debug(f"Launched app: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to search and launch app: {str(e)}")
            return False
    
    def select_chrome_profile(self, wait_time: float = 2.0) -> bool:
        """
        Select the first Chrome profile if profile selection appears.
        
        Args:
            wait_time: Time to wait between actions in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Press Tab to select the first profile
            self.press_tab()
            self.wait(0.5)
            
            # Press Space to open the selected profile
            self.press_space()
            self.wait(wait_time)
            
            logger.debug("Chrome profile selected")
            return True
        except Exception as e:
            logger.error(f"Failed to select Chrome profile: {str(e)}")
            return False
    
    def launch_chrome(self, wait_time: float = 2.0) -> bool:
        """
        Launch Google Chrome browser using Windows key and search.
        
        Args:
            wait_time: Time to wait between actions in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.os_name != "Windows":
            logger.warning("This method currently only supports Windows.")
            return False
            
        try:
            # Search for and launch Chrome
            if not self.search_and_launch_app("Google Chrome", wait_time):
                return False
            
            # Wait longer for Chrome to start
            self.wait(wait_time)
            
            # Select Chrome profile if needed
            if not self.select_chrome_profile(wait_time):
                return False
            
            logger.debug("Chrome launched successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch Chrome: {str(e)}")
            return False
    
    def open_chrome_and_navigate(self, url: str, wait_time: float = 2.0, maximize: bool = True) -> bool:
        """
        Launch Chrome, maximize it, and navigate to the specified URL.
        
        Args:
            url: URL to navigate to
            wait_time: Time to wait between actions in seconds
            maximize: Whether to maximize the Chrome window
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.launch_chrome(wait_time):
            return False
            
        if maximize and not self.maximize_window(wait_time):
            return False
            
        return self.open_url_in_new_tab(url, wait_time)
    
    def open_html_file(self, html_file_path: str, wait_time: float = 2.0, maximize: bool = True) -> bool:
        """
        Open an HTML file in Chrome.
        
        Args:
            html_file_path: Path to the HTML file
            wait_time: Time to wait between actions in seconds
            maximize: Whether to maximize the Chrome window
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert to absolute path and check if file exists
            html_path = Path(html_file_path).resolve()
            if not html_path.exists():
                logger.error(f"HTML file not found: {html_path}")
                return False
            
            # Convert to file URI
            file_uri = f"file://{html_path}"
            
            # Open Chrome and navigate to the file URI
            return self.open_chrome_and_navigate(file_uri, wait_time, maximize)
        except Exception as e:
            logger.error(f"Failed to open HTML file in Chrome: {str(e)}")
            return False
    
    def launch_chrome_directly(self, url: Optional[str] = None) -> bool:
        """
        Launch Chrome directly using the executable path.
        
        Args:
            url: Optional URL to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
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
                    if url:
                        subprocess.Popen([chrome_path, url])
                    else:
                        subprocess.Popen([chrome_path])
                else:
                    # Fallback to webbrowser module
                    if url:
                        webbrowser.get('chrome').open(url)
                    else:
                        webbrowser.get('chrome').open('about:blank')
                    
            elif system == "Darwin":  # macOS
                chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                if os.path.exists(chrome_path):
                    if url:
                        subprocess.Popen([chrome_path, url])
                    else:
                        subprocess.Popen([chrome_path])
                else:
                    # Fallback to webbrowser module
                    if url:
                        webbrowser.get('chrome').open(url)
                    else:
                        webbrowser.get('chrome').open('about:blank')
                    
            elif system == "Linux":
                # Try common Chrome executable names on Linux
                chrome_candidates = ['google-chrome', 'chrome', 'chromium', 'chromium-browser']
                
                for candidate in chrome_candidates:
                    try:
                        if url:
                            subprocess.Popen([candidate, url])
                        else:
                            subprocess.Popen([candidate])
                        break
                    except FileNotFoundError:
                        continue
                else:
                    # Fallback to webbrowser module
                    if url:
                        webbrowser.get('chrome').open(url)
                    else:
                        webbrowser.get('chrome').open('about:blank')
            
            logger.debug(f"Launched Chrome directly{' with URL: ' + url if url else ''}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch Chrome directly: {str(e)}")
            return False
    
    def open_chrome_incognito(self, url: Optional[str] = None) -> bool:
        """
        Open Chrome in incognito mode.
        
        Args:
            url: Optional URL to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
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
                    if url:
                        subprocess.Popen([chrome_path, '--incognito', url])
                    else:
                        subprocess.Popen([chrome_path, '--incognito'])
                    return True
                else:
                    logger.error("Chrome executable not found")
                    return False
                    
            elif system == "Darwin":  # macOS
                chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                if os.path.exists(chrome_path):
                    if url:
                        subprocess.Popen([chrome_path, '--incognito', url])
                    else:
                        subprocess.Popen([chrome_path, '--incognito'])
                    return True
                else:
                    logger.error("Chrome executable not found")
                    return False
                    
            elif system == "Linux":
                # Try common Chrome executable names on Linux
                chrome_candidates = ['google-chrome', 'chrome', 'chromium', 'chromium-browser']
                
                for candidate in chrome_candidates:
                    try:
                        if url:
                            subprocess.Popen([candidate, '--incognito', url])
                        else:
                            subprocess.Popen([candidate, '--incognito'])
                        return True
                    except FileNotFoundError:
                        continue
                
                logger.error("Chrome executable not found")
                return False
            
            logger.debug(f"Launched Chrome in incognito mode{' with URL: ' + url if url else ''}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch Chrome in incognito mode: {str(e)}")
            return False 