"""
API Route Constants

This module defines constants for all API endpoints used in the application.
"""

class RestEndpoints:
    """Constants for REST API endpoints"""
    HEALTH = "/health"
    GENERATE_SYSTEM_BOUNDING_BOXES = "/generate-system-bboxes"
    ACTIVE_CLIENTS = "/ws/clients"
class WebSocketEndpoints:
    """Constants for WebSocket endpoints"""
    COMMAND = "/ws/command"
    STATUS = "/ws/status"
    SCREEN_CAPTURE = "/ws/screen_capture"
    VISION_DETECT = "/ws/vision_detect"
    
# Re-export for easier imports
REST = RestEndpoints
WS = WebSocketEndpoints