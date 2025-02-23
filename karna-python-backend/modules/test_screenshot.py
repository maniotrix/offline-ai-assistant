import os
import time
import threading
import pyautogui
from datetime import datetime
from pynput import keyboard, mouse
import re
from PIL import Image, ImageDraw, ImageFont

# Create a folder to store screenshots
screenshots_folder = os.path.join(os.getcwd(), 'screenshots')
os.makedirs(screenshots_folder, exist_ok=True)

# Clean the screenshots folder at the start
for file in os.listdir(screenshots_folder):
    file_path = os.path.join(screenshots_folder, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Open event log file for recording events
log_file_name = 'screenshot_events.txt'
log_lock = threading.Lock()
log_file = open(log_file_name, 'w')

# Added a global variable for mouse_listener
m_listener = None

def log_event(event_description, screenshot_filename):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    entry = f"[{timestamp}] {event_description} - Screenshot: {screenshot_filename}\n"
    with log_lock:
        log_file.write(entry)
        log_file.flush()
    print(entry.strip())


def take_screenshot(event_description):
    # Create a unique filename for the screenshot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f'screenshot_{timestamp}.png'
    screenshot_path = os.path.join(screenshots_folder, filename)
    
    # Capture and save the screenshot
    image = pyautogui.screenshot()
    image.save(screenshot_path)
    
    # Log the event along with the screenshot reference
    log_event(event_description, screenshot_path)


def on_key_press(key):
    global m_listener  # allow access to the global mouse listener
    try:
        event_desc = f"Key pressed: {key.char}"
    except AttributeError:
        event_desc = f"Special key pressed: {key}"
    take_screenshot(event_desc)
    
    if key == keyboard.Key.esc:
        if m_listener is not None:
            m_listener.stop()
        return False


def on_click(x, y, button, pressed):
    if pressed:
        event_desc = f"Mouse clicked at ({x}, {y}) with {button}"
        take_screenshot(event_desc)


def test_verification():
    """Test function for verification after escape key is pressed.
    It reads the log file, then for each screenshot event:
      - if it's a mouse event, it draws a red circle at the click location.
      - if it's a key event, it overlays the event text on the image.
    The modified images are displayed for verification.
    """
    # Read the events from the log file
    log_filename = 'screenshot_events.txt'
    if not os.path.exists(log_filename):
        print(f"Log file {log_filename} does not exist.")
        return
    with open(log_filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Each line format: [timestamp] event_description - Screenshot: screenshot_path
        try:
            header, screenshot_part = line.strip().split(' - Screenshot: ')
            # Remove timestamp from header
            event_desc = header.split('] ')[1]
            screenshot_path = screenshot_part
        except Exception as e:
            print(f"Skipping malformed line: {line}")
            continue

        if not os.path.exists(screenshot_path):
            print(f"Screenshot not found: {screenshot_path}")
            continue

        # Open the screenshot image
        try:
            image = Image.open(screenshot_path)
        except Exception as e:
            print(f"Error opening image {screenshot_path}: {e}")
            continue

        draw = ImageDraw.Draw(image)

        if event_desc.startswith('Mouse clicked at'):
            # Parse coordinates from string: expected format "Mouse clicked at (x, y) with ..."
            match = re.search(r"\((\d+),\s*(\d+)\)", event_desc)
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                # Draw a red circle at the mouse pointer location
                radius = 20
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline='red', width=5)
        elif event_desc.startswith('Key pressed') or event_desc.startswith('Special key pressed'):
            # Overlay the event text on the image
            text = event_desc
            # Choose a font size relative to image
            font_size = max(20, image.width // 30)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
            text_position = (10, 10)
            draw.text(text_position, text, fill='red', font=font)

        # Display the modified image for verification
        image.show()
        # Pause to let the user view the image, if needed
        time.sleep(2)


def main():
    global m_listener
    # Set up keyboard and mouse listeners concurrently
    with keyboard.Listener(on_press=on_key_press) as k_listener, \
         mouse.Listener(on_click=on_click) as m_listener_local:
        m_listener = m_listener_local
        k_listener.join()
        m_listener.join()
    
    # Run test verification after escape key is pressed
    test_verification()

    log_file.close()
    print('Application terminated.')


if __name__ == "__main__":
    main()
