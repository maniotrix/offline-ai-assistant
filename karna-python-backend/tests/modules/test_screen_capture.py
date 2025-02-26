import unittest
import os
import shutil
import time
from typing import List
from modules.screen_capture import (
    ScreenCaptureService, 
    ScreenshotEvent,
    SessionError
)
from base.base_observer import Observer, Priority
from PIL import Image

class TestObserver(Observer[List[ScreenshotEvent]]):
    """Observer to track and display screen capture events.
    
    This observer handles lists of screen capture events and provides
    detailed feedback about each event type, including session state changes,
    screenshots, annotations, and input events.
    """
    def __init__(self):
        super().__init__(Priority.NORMAL)
    
    def update(self, data: List[ScreenshotEvent]) -> None:
        """Handle list of screen capture events and provide detailed feedback.
        
        Args:
            events: List of screen capture events to process
        """
        for event in data:
            # Print event-specific details
            if event.screenshot_path:
                print(f"[Observer] - Screenshot: {os.path.basename(event.screenshot_path)}")
            if event.annotation_path:
                print(f"[Observer] - Annotated: {os.path.basename(event.annotation_path)}")
            if event.key_char or event.key_code:
                print(f"[Observer] - Key: {event.key_char or event.key_code} {'(Special)' if event.is_special_key else ''}")
            if event.mouse_x is not None and event.mouse_y is not None:
                print(f"[Observer] - Mouse Position: ({event.mouse_x}, {event.mouse_y})")
            
class TestScreenCapture(unittest.TestCase):
    def setUp(self):
        self.service = ScreenCaptureService()
        self.observer = TestObserver()
        self.service.add_observer(self.observer)
        self.test_project = "test_project_123"
        self.test_uuid = "test_capture_123"
        self.cleanup_test_dirs()

    def tearDown(self):
        if self.service.is_capturing:
            self.service.stop_capture()
        self.cleanup_test_dirs()

    def cleanup_test_dirs(self):
        """Clean up any test directories"""
        test_dir = os.path.join('data', self.test_project)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_service_initialization(self):
        """Test basic service initialization and directory structure"""
        # Test initial state
        self.assertFalse(self.service.is_capturing)
        self.assertIsNone(self.service.get_current_session_stats())
        self.assertEqual(len(self.service.get_session_history()), 0)
        
        # Test basic session start
        self.service.start_capture(self.test_project, self.test_uuid)
        self.assertTrue(self.service.is_capturing)
        
        # Verify directory structure
        expected_raw = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'raw')
        expected_annotated = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'annotated')
        self.assertTrue(os.path.exists(expected_raw))
        self.assertTrue(os.path.exists(expected_annotated))
        
        # Test stop capture
        self.service.stop_capture()
        self.assertFalse(self.service.is_capturing)
        stats = self.service.get_current_session_stats()
        self.assertIsNotNone(stats)
        self.assertEqual(len(self.service.get_session_history()), 1)

    def test_concurrent_session_prevention(self):
        """Test that we cannot start multiple capture sessions simultaneously"""
        # Start first session
        self.service.start_capture(self.test_project, self.test_uuid)
        self.assertTrue(self.service.is_capturing)
        
        # Try to start another session
        with self.assertRaises(SessionError) as context:
            self.service.start_capture(self.test_project, "another_uuid")
        self.assertIn("Cannot start new session while another is active", str(context.exception))
        
        # Verify first session is still active
        self.assertTrue(self.service.is_capturing)
        stats = self.service.get_current_session_stats()
        self.assertIsNotNone(stats)
        self.assertEqual(stats.project_uuid, self.test_project)
        self.assertEqual(stats.command_uuid, self.test_uuid)
        
        # Stop the session and verify it can be started again
        self.service.stop_capture()
        self.assertFalse(self.service.is_capturing)
        try:
            self.service.start_capture(self.test_project, "another_uuid")
            self.assertTrue(self.service.is_capturing)
        except SessionError:
            self.fail("Should be able to start new session after stopping previous one")

    def test_interactive_capture_session(self):
        """
        'python -m pytest tests/modules/test_screen_capture.py -v -s -k test_interactive_capture_session'
        Main interactive test for screen capture session.
        This test will:
        1. Start a capture session
        2. Wait for user to interact (press keys, click mouse)
        3. Press ESC to end session
        4. Display the session summary
        """
        print("\n" + "="*80)
        print("Interactive Screen Capture Test")
        print("="*80)
        print("\nTest Instructions:")
        print("1. The capture session will start in 3 seconds")
        print("2. Interact with your screen (press keys, click mouse)")
        print("3. Each interaction will be captured and annotated")
        print("4. Press ESC key when you want to end the session")
        print("5. A summary of all captures will be displayed")
        print("\nStarting in...")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("\nStarting capture session...")
        try:
            self.service.start_capture(self.test_project, self.test_uuid)
            self.assertTrue(self.service.is_capturing)
            
            print("\nCapture session active - interact with your screen...")
            print("(Press ESC to end the session)")
            
            # Wait for the session to end (when user presses ESC)
            while self.service.is_capturing:
                time.sleep(0.1)

            # Verify the session completed successfully
            self.assertFalse(self.service.is_capturing)
            
            # Get and display session statistics
            stats = self.service.get_current_session_stats()
            self.assertIsNotNone(stats)
            
            print("\n" + "="*80)
            print("Session Summary")
            print("="*80)
            print(f"Total Screenshots: {stats.total_screenshots}")
            print(f"Total Annotations: {stats.total_annotations}")
            print(f"Key Events: {stats.total_key_events}")
            print(f"Mouse Events: {stats.total_mouse_events}")
            print(f"Session Duration: {stats.duration_seconds:.2f} seconds")
            print(f"Raw Directory Size: {stats.raw_directory_size/1024:.2f} KB")
            print(f"Annotated Directory Size: {stats.annotated_directory_size/1024:.2f} KB")
            
            # Show the visual summary
            summary_path = os.path.join('data', self.test_project, self.test_uuid, 'summary', 'session_summary.png')
            self.assertTrue(os.path.exists(summary_path))
            
            try:
                summary_img = Image.open(summary_path)
                print("\nDisplaying session summary image...")
                summary_img.show()
                
                print("\nPress Enter after reviewing the summary...")
                input()
                
            except Exception as e:
                print(f"Error displaying summary: {e}")
                self.fail(f"Failed to display summary image: {str(e)}")

        except Exception as e:
            self.fail(f"Interactive test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()