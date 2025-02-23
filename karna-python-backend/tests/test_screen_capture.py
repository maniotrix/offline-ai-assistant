import unittest
import os
import shutil
import time
from datetime import datetime
from modules.screen_capture import (
    ScreenCaptureService, 
    ScreenshotEvent,
    EventType,
    SessionError
)
from base.base_observer import Observer, Priority
from PIL import Image

class TestObserver(Observer[ScreenshotEvent]):
    """Observer to track and display screen capture events"""
    def __init__(self):
        super().__init__(Priority.NORMAL)
        self.notifications: list[ScreenshotEvent] = []
    
    def update(self, data: ScreenshotEvent) -> None:
        self.notifications.append(data)
        # Print real-time feedback for the test user
        print(f"\nEvent: {data.type.name}")
        print(f"Description: {data.description}")
        if data.screenshot_path:
            print(f"Screenshot: {data.screenshot_path}")
        if data.annotated_path:
            print(f"Annotated: {data.annotated_path}")

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
        
        # Test basic session start
        self.service.start_capture(self.test_project, self.test_uuid)
        self.assertTrue(self.service.is_capturing)
        
        # Verify directory structure
        expected_raw = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'raw')
        expected_annotated = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'annotated')
        self.assertTrue(os.path.exists(expected_raw))
        self.assertTrue(os.path.exists(expected_annotated))

    def test_concurrent_session_prevention(self):
        """Test that we cannot start multiple capture sessions simultaneously"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Try to start another session
        with self.assertRaises(SessionError) as context:
            self.service.start_capture(self.test_project, "another_uuid")
        self.assertIn("Cannot start new session while another is active", str(context.exception))

    def test_interactive_capture_session(self):
        """
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
        self.service.start_capture(self.test_project, self.test_uuid)
        
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

        # Verify we captured some events
        events = self.observer.notifications
        self.assertGreater(len(events), 2)  # Should have at least start and stop events
        self.assertIn(EventType.CAPTURE_STARTED, [e.type for e in events])
        self.assertIn(EventType.CAPTURE_STOPPED, [e.type for e in events])

if __name__ == '__main__':
    unittest.main()