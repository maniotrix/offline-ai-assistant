import unittest
import os
import shutil
import time
import logging
from datetime import datetime, timedelta
from modules.screen_capture import (
    ScreenCaptureService, 
    ScreenCaptureEvent,
    EventType,
    ScreenCaptureSession,
    ScreenCaptureError,
    SessionError,
    DirectoryError,
    CaptureError,
    SessionStatistics
)
from base.base_observer import Observer, Priority
import math
from PIL import Image, ImageDraw, ImageFont

class TestObserver(Observer[ScreenCaptureEvent]):
    def __init__(self):
        super().__init__(Priority.NORMAL)
        self.notifications: list[ScreenCaptureEvent] = []
    
    def update(self, data: ScreenCaptureEvent) -> None:
        self.notifications.append(data)

class TestScreenCaptureService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure logs directory exists
        logs_dir = os.path.join('data', 'logs')
        os.makedirs(logs_dir, exist_ok=True)

    def setUp(self):
        self.service = ScreenCaptureService()
        self.observer = TestObserver()
        self.service.add_observer(self.observer)
        self.test_project = "test_project_123"
        self.test_uuid = "test_capture_123"
        
        # Clean up test directories if they exist
        self.cleanup_test_dirs()

    def tearDown(self):
        self.service.stop_capture()
        self.cleanup_test_dirs()

    def cleanup_test_dirs(self):
        test_dir = os.path.join('data', self.test_project, self.test_uuid)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        # Clean up project directory if empty
        project_dir = os.path.join('data', self.test_project)
        if os.path.exists(project_dir) and not os.listdir(project_dir):
            os.rmdir(project_dir)

    def test_session_creation(self):
        """Test that a new session is properly created"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        self.assertTrue(self.service.is_capturing)
        self.assertIsNotNone(self.service.current_session)
        self.assertEqual(self.service.current_session.project_uuid, self.test_project)
        self.assertEqual(self.service.current_session.command_uuid, self.test_uuid)
        self.assertTrue(self.service.current_session.is_active)
        self.assertIsNotNone(self.service.current_session.start_time)
        
    def test_session_directories(self):
        """Test that session directories are created correctly"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        self.assertIsNotNone(self.service.current_session)
        self.assertTrue(os.path.exists(self.service.current_session.raw_dir))
        self.assertTrue(os.path.exists(self.service.current_session.annotated_dir))
        
        # Verify correct path structure
        expected_raw = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'raw')
        expected_annotated = os.path.join('data', self.test_project, self.test_uuid, 'screenshots', 'annotated')
        self.assertEqual(self.service.current_session.raw_dir, expected_raw)
        self.assertEqual(self.service.current_session.annotated_dir, expected_annotated)

    def test_session_events(self):
        """Test that session events are properly created and notified"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Test start event
        start_events = [n for n in self.observer.notifications 
                       if n.type == EventType.CAPTURE_STARTED]
        self.assertEqual(len(start_events), 1)
        self.assertEqual(start_events[0].command_uuid, self.test_uuid)
        
        # Simulate some events
        screenshot_path = self.service._take_screenshot("Test screenshot")
        self.assertIsNotNone(screenshot_path)
        
        self.service._annotate_screenshot(screenshot_path, x=100, y=100, text="Test annotation")
        
        # Stop capture
        self.service.stop_capture()
        
        # Verify event sequence
        events = self.observer.notifications
        event_types = [e.type for e in events]
        
        self.assertIn(EventType.CAPTURE_STARTED, event_types)
        self.assertIn(EventType.SCREENSHOT, event_types)
        self.assertIn(EventType.ANNOTATION, event_types)
        self.assertIn(EventType.CAPTURE_STOPPED, event_types)

    def test_session_duration(self):
        """Test that session duration is calculated correctly"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Wait a bit to ensure measurable duration
        time.sleep(0.1)
        self.service.stop_capture()
        
        stats = self.service.get_current_session_stats()
        self.assertIsNotNone(stats)
        self.assertGreater(stats.duration_seconds, 0.1)

    def test_session_cleanup(self):
        """Test that starting a new session cleans up old files"""
        # Create initial session with dummy files
        self.service.start_capture(self.test_project, self.test_uuid)
        screenshot_path = self.service._take_screenshot("Test screenshot")
        self.service.stop_capture()
        
        # Verify files exist
        self.assertTrue(os.path.exists(screenshot_path))
        
        # Start new session with same UUID
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Verify old files are cleaned up
        self.assertFalse(os.path.exists(screenshot_path))
        
        # Verify directories are recreated
        self.assertTrue(os.path.exists(os.path.dirname(screenshot_path)))

    def test_concurrent_session_prevention(self):
        """Test that concurrent sessions are prevented"""
        self.service.start_capture(self.test_project, self.test_uuid)
        original_session = self.service.current_session
        
        # Try to start another session
        second_uuid = "test_capture_456"
        self.service.start_capture(self.test_project, second_uuid)
        
        # Verify original session is still active
        self.assertEqual(self.service.current_session, original_session)
        self.assertEqual(self.service.current_session.command_uuid, self.test_uuid)
        
        # Verify only one start event
        start_events = [n for n in self.observer.notifications 
                       if n.type == EventType.CAPTURE_STARTED]
        self.assertEqual(len(start_events), 1)

    def test_session_state_transitions(self):
        """Test session state transitions"""
        # Test initial state
        self.assertFalse(self.service.is_capturing)
        
        # Test state after start
        self.service.start_capture(self.test_project, self.test_uuid)
        self.assertTrue(self.service.is_capturing)
        self.assertTrue(self.service.get_state('capturing'))
        
        # Test state after stop
        self.service.stop_capture()
        self.assertFalse(self.service.is_capturing)
        self.assertFalse(self.service.get_state('capturing'))

    def test_session_validation(self):
        """Test session validation errors"""
        # Test without starting session
        with self.assertRaises(SessionError):
            self.service._validate_session()

        # Test with inactive session
        self.service.start_capture(self.test_project, self.test_uuid)
        self.service.stop_capture()
        with self.assertRaises(SessionError):
            self.service._validate_session()

    def test_concurrent_session_error(self):
        """Test error handling for concurrent session attempts"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Try to start another session
        with self.assertRaises(SessionError) as context:
            self.service.start_capture(self.test_project, "another_uuid")
        self.assertIn("Cannot start new session while another is active", str(context.exception))

    def test_directory_error_handling(self):
        """Test error handling for directory operations"""
        # Create a file where we expect a directory
        base_dir = os.path.join('data', self.test_project, self.test_uuid)
        os.makedirs(os.path.dirname(base_dir), exist_ok=True)
        with open(base_dir, 'w') as f:
            f.write('blocking file')
            
        # Try to start capture
        with self.assertRaises(DirectoryError):
            self.service.start_capture(self.test_project, self.test_uuid)
            
        # Clean up
        os.remove(base_dir)

    def test_capture_error_handling(self):
        """Test error handling during screen capture"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Simulate a directory removal during active session
        shutil.rmtree(self.service.current_session.raw_dir)
        
        with self.assertRaises(DirectoryError):
            self.service._validate_session()

    def test_stop_inactive_session(self):
        """Test stopping an already stopped session"""
        # Try to stop without starting
        with self.assertRaises(SessionError):
            self.service.stop_capture()
            
        # Try to stop twice
        self.service.start_capture(self.test_project, self.test_uuid)
        self.service.stop_capture()
        with self.assertRaises(SessionError):
            self.service.stop_capture()

    def test_session_state_recovery(self):
        """Test service state after error conditions"""
        # Simulate failed start
        try:
            # Create invalid directory structure
            base_dir = os.path.join('data', self.test_project, self.test_uuid)
            os.makedirs(base_dir)
            with open(os.path.join(base_dir, 'raw'), 'w') as f:
                f.write('blocking file')
                
            self.service.start_capture(self.test_project, self.test_uuid)
        except DirectoryError:
            pass
            
        # Verify service state is clean
        self.assertIsNone(self.service.current_session)
        self.assertFalse(self.service.is_capturing)
        
        # Clean up
        shutil.rmtree(base_dir)
        
        # Verify service can start new session
        self.service.start_capture(self.test_project, self.test_uuid)
        self.assertTrue(self.service.is_capturing)

    def test_session_statistics(self):
        """Test session statistics collection"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Generate some events
        self.service._take_screenshot("Test screenshot 1")
        self.service._take_screenshot("Test screenshot 2")
        self.service._on_click(100, 100, "left", True)
        
        # Get current stats
        stats = self.service.get_current_session_stats()
        self.assertIsNotNone(stats)
        self.assertEqual(stats.project_uuid, self.test_project)
        self.assertEqual(stats.command_uuid, self.test_uuid)
        self.assertGreaterEqual(stats.total_screenshots, 3)
        self.assertGreaterEqual(stats.total_annotations, 1)
        
        # Stop capture and check history
        self.service.stop_capture()
        history = self.service.get_session_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].project_uuid, self.test_project)
        self.assertEqual(history[0].command_uuid, self.test_uuid)

    def test_event_statistics(self):
        """Test event statistics tracking"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Simulate events
        self.service._on_click(100, 100, "left", True)
        self.service._on_key_press('a')
        
        # Check event stats
        event_stats = self.service.get_total_event_stats()
        self.assertGreaterEqual(event_stats[EventType.MOUSE_CLICK], 1)
        self.assertGreaterEqual(event_stats[EventType.KEY_PRESS], 1)
        self.assertGreaterEqual(event_stats[EventType.SCREENSHOT], 2)  # One for each event
        self.assertGreaterEqual(event_stats[EventType.ANNOTATION], 1)  # From mouse click

    def test_session_cleanup(self):
        """Test cleanup of old session directories"""
        # Create some test sessions in different projects
        old_project = "old_project"
        new_project = "new_project"
        old_cmd = "old_session_123"
        
        self.service.start_capture(old_project, old_cmd)
        self.service.stop_capture()
        
        self.service.start_capture(new_project, self.test_uuid)
        self.service.stop_capture()
        
        # Modify the old session directory's timestamp
        old_dir = os.path.join('data', old_project, old_cmd)
        old_time = datetime.now() - timedelta(days=8)
        os.utime(old_dir, (old_time.timestamp(), old_time.timestamp()))
        
        # Run cleanup
        self.service.cleanup_old_sessions(days_to_keep=7)
        
        # Verify old session is removed but current remains
        self.assertFalse(os.path.exists(old_dir))
        self.assertFalse(os.path.exists(os.path.join('data', old_project)))  # Project dir should be removed
        self.assertTrue(os.path.exists(os.path.join('data', new_project, self.test_uuid)))

    def test_empty_project_cleanup(self):
        """Test that empty project directories are removed during cleanup"""
        project_dir = os.path.join('data', self.test_project)
        cmd_dir = os.path.join(project_dir, self.test_uuid)
        
        # Create and then remove command directory
        os.makedirs(cmd_dir)
        old_time = datetime.now() - timedelta(days=8)
        os.utime(cmd_dir, (old_time.timestamp(), old_time.timestamp()))
        
        self.service.cleanup_old_sessions(days_to_keep=7)
        
        # Verify both command and project directories are removed
        self.assertFalse(os.path.exists(cmd_dir))
        self.assertFalse(os.path.exists(project_dir))

    def test_multiple_projects(self):
        """Test handling multiple projects"""
        projects = ["project1", "project2"]
        commands = ["cmd1", "cmd2"]
        
        for project in projects:
            for cmd in commands:
                self.service.start_capture(project, cmd)
                self.service._take_screenshot("Test")
                self.service.stop_capture()
                
                # Verify directory structure
                raw_dir = os.path.join('data', project, cmd, 'screenshots', 'raw')
                annotated_dir = os.path.join('data', project, cmd, 'screenshots', 'annotated')
                self.assertTrue(os.path.exists(raw_dir))
                self.assertTrue(os.path.exists(annotated_dir))
                
                # Clean up after verification
                shutil.rmtree(os.path.join('data', project))

    def test_project_isolation(self):
        """Test that projects are properly isolated"""
        # Create sessions in different projects
        project1 = "project1"
        project2 = "project2"
        cmd = "same_command"
        
        # Create content in project1
        self.service.start_capture(project1, cmd)
        screenshot1 = self.service._take_screenshot("Test project1")
        self.service.stop_capture()
        
        # Create content in project2
        self.service.start_capture(project2, cmd)
        screenshot2 = self.service._take_screenshot("Test project2")
        self.service.stop_capture()
        
        # Verify files exist in correct locations
        self.assertTrue(os.path.exists(screenshot1))
        self.assertTrue(os.path.exists(screenshot2))
        self.assertNotEqual(os.path.dirname(screenshot1), os.path.dirname(screenshot2))
        
        # Clean up
        shutil.rmtree(os.path.join('data', project1))
        shutil.rmtree(os.path.join('data', project2))

    def test_long_running_session(self):
        """Test statistics for a longer running session"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Simulate passage of time
        start_time = self.service.current_session.start_time
        if start_time:
            self.service.current_session.start_time = start_time - timedelta(minutes=5)
        
        stats = self.service.get_current_session_stats()
        self.assertIsNotNone(stats)
        self.assertEqual(stats.project_uuid, self.test_project)
        self.assertGreater(stats.duration_seconds, 290)  # Almost 5 minutes

    def test_multiple_session_history(self):
        """Test maintaining history of multiple sessions"""
        # Create multiple sessions across different projects
        test_data = [
            ("project1", "cmd1"),
            ("project1", "cmd2"),
            ("project2", "cmd1")
        ]
        
        for project_id, cmd_id in test_data:
            self.service.start_capture(project_id, cmd_id)
            self.service._take_screenshot("Test")
            self.service.stop_capture()
            # Clean up directories
            shutil.rmtree(os.path.join('data', project_id))
        
        # Check history
        history = self.service.get_session_history()
        self.assertEqual(len(history), len(test_data))
        
        # Verify each session has correct project and command IDs
        for session_stats, (project_id, cmd_id) in zip(history, test_data):
            self.assertEqual(session_stats.project_uuid, project_id)
            self.assertEqual(session_stats.command_uuid, cmd_id)
            self.assertGreater(session_stats.total_screenshots, 0)

    def test_session_visualization(self):
        """Test creating a visual summary of all screenshots and annotations in sequence"""
        self.service.start_capture(self.test_project, self.test_uuid)
        
        # Generate some test events with meaningful content
        self.service._take_screenshot("Initial state")
        self.service._on_click(100, 100, "left", True)  # This creates both screenshot and annotation
        self.service._on_key_press('a')  # Creates screenshot with key press
        self.service._on_click(200, 200, "right", True)  # Creates another screenshot and annotation
        
        # Test mid-session summary
        mid_session_summary = self.service.create_session_summary()
        self.assertIsNotNone(mid_session_summary)
        self.assertTrue(os.path.exists(mid_session_summary))
        
        # Continue with more events
        self.service._take_screenshot("Final state")
        
        # Stop capture (which automatically creates another summary)
        self.service.stop_capture()
        
        summary_path = os.path.join('data', self.test_project, self.test_uuid, 'summary', 'session_summary.png')
        
        # Verify the summary exists and contains content
        self.assertTrue(os.path.exists(summary_path))
        self.assertGreater(os.path.getsize(summary_path), 0)
        
        # Verify summary contains expected number of images
        summary_img = Image.open(summary_path)
        # The summary should be large enough to contain all screenshots and annotations
        min_expected_width = 640  # At least two thumbnails wide (320 * 2)
        self.assertGreater(summary_img.width, min_expected_width)
        
        # Verify the stop event contains the summary path
        stop_events = [n for n in self.observer.notifications 
                      if n.type == EventType.CAPTURE_STOPPED]
        self.assertEqual(len(stop_events), 1)
        self.assertIn('Summary available at:', stop_events[0].description)

if __name__ == '__main__':
    unittest.main()