import subprocess
import os
import pyperclip

def copy_files_with_powershell(file_paths):
    # WARNING: You can copy multiple files to the clipboard with this function, but
    # it will only paste the first file on the clipboard.
    # Ensure file_paths are absolute
    abs_paths = [os.path.abspath(path) for path in file_paths]
    # Build the full path to the PowerShell script
    ps_script = os.path.join(os.path.dirname(__file__), 'copy_files_to_clipboard.ps1')
    # Construct the command exactly as in CMD
    command = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", ps_script
    ] + abs_paths

    print("Running command:", command)

    # Run the PowerShell script and wait for it to complete
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    
    print("STDOUT:\n", result.stdout)
    if result.stderr:
        print("STDERR:\n", result.stderr)
        
def send_text_to_clipboard(text: str):
    try:
        pyperclip.copy(text)
        print("Text copied to clipboard")
    except Exception as e:
        print(f"Error copying text to clipboard: {e}")
        
def paste_text_from_clipboard(text: str | None = None):
    try:
        pyperclip.paste()
        print("Text pasted from clipboard")
    except Exception as e:
        print(f"Error pasting text from clipboard: {e}")

def get_text_from_clipboard() -> str:
    """
    Gets text from clipboard using pyperclip.
    
    Returns:
        str: Text content of clipboard
    """
    try:
        print("Getting text from clipboard")
        return pyperclip.paste()
    except Exception as e:
        print(f"Error getting text from clipboard: {e}")
        return ""
# Example usage:
if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    screenshot_raw_dir = os.path.join(dir_path, "ground_data", "screenshots", "raw")
    try:
        # Get absolute paths for image files
        image_files = [os.path.join(screenshot_raw_dir, f)
                       for f in os.listdir(screenshot_raw_dir)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        image_files.sort(key=lambda x: os.path.getmtime(x))
        copy_files_with_powershell(image_files)
        print("Files copied to clipboard successfully.")
    except Exception as e:
        print(f"Error copying files to clipboard: {e}")
