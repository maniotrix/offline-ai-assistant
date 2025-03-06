from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import logging
from base import SingletonMeta
from api.websockets.command.command_handler import CommandWebSocketHandler
from api.websockets.status.status_handler import StatusWebSocketHandler
from api.websockets.screen_capture.screen_capture_handler import ScreenCaptureWebSocketHandler
from api.websockets.vision_detect.vision_detect_handler import VisionDetectWebSocketHandler

class WebSocketManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.command_handler = CommandWebSocketHandler()
            self.status_handler = StatusWebSocketHandler()
            self.screen_capture_handler = ScreenCaptureWebSocketHandler()
            self.vision_detect_handler = VisionDetectWebSocketHandler()
            self.logger = logging.getLogger(__name__)
            self._initialized = True

    async def handle_command_connection(self, websocket: WebSocket) -> None:
        """Handle command channel connection"""
        await self.command_handler.connect(websocket)
        try:
            while True:
                message = await websocket.receive_bytes()
                await self.command_handler.handle_message(websocket, message)
        except WebSocketDisconnect:
            self.command_handler.disconnect(websocket)
        except Exception as e:
            self.logger.error(f"Error in command connection: {e}", exc_info=True)
            self.command_handler.disconnect(websocket)

    async def handle_status_connection(self, websocket: WebSocket) -> None:
        """Handle status channel connection"""
        await self.status_handler.connect(websocket)
        try:
            while True:
                message = await websocket.receive_bytes()
                await self.status_handler.handle_message(websocket, message)
        except WebSocketDisconnect:
            self.status_handler.disconnect(websocket)
        except Exception as e:
            self.logger.error(f"Error in status connection: {e}", exc_info=True)
            self.status_handler.disconnect(websocket)

    async def handle_screen_capture_connection(self, websocket: WebSocket) -> None:
        """Handle screen capture channel connection"""
        await self.screen_capture_handler.connect(websocket)
        try:
            while True:
                message = await websocket.receive_bytes()
                await self.screen_capture_handler.handle_message(websocket, message)
        except WebSocketDisconnect:
            self.screen_capture_handler.disconnect(websocket)
        except Exception as e:
            self.logger.error(f"Error in screen capture connection: {e}", exc_info=True)
            self.screen_capture_handler.disconnect(websocket)
            
    async def handle_vision_detect_connection(self, websocket: WebSocket) -> None:
        """Handle vision detection channel connection"""
        await self.vision_detect_handler.connect(websocket)
        try:
            while True:
                message = await websocket.receive_bytes()
                await self.vision_detect_handler.handle_message(websocket, message)
        except WebSocketDisconnect:
            self.vision_detect_handler.disconnect(websocket)
        except Exception as e:
            self.logger.error(f"Error in vision detection connection: {e}", exc_info=True)
            self.vision_detect_handler.disconnect(websocket)

    def report_active_clients(self) -> Dict[str, int]:
        """Report number of active connections per channel"""
        return {
            "command": len(self.command_handler.active_connections),
            "status": len(self.status_handler.active_connections),
            "screen_capture": len(self.screen_capture_handler.active_connections),
            "vision_detect": len(self.vision_detect_handler.active_connections)
        }


# Singleton instance getter
_websocket_manager_instance = None

def get_websocket_manager_instance():
    global _websocket_manager_instance
    if _websocket_manager_instance is None:
        _websocket_manager_instance = WebSocketManager()
    return _websocket_manager_instance


