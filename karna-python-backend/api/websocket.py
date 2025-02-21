from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional, Any
import json
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.command_handler.command_processor import get_command_service_instance
from services.task_execution_service import TaskExecutorService

class WebSocketMessageType(str, Enum):
    COMMAND = 'execute_command'
    STATUS = 'get_status'
    STATUS_UPDATE = 'status_update'
    ERROR = 'error'

@dataclass
class WebSocketMessage:
    type: str
    data: Any

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.task_exec_service = TaskExecutorService()
        self.logger = logging.getLogger(__name__)
        self._setup_message_handlers()

    def _setup_message_handlers(self) -> None:
        """Set up message type handlers"""
        self.message_handlers = {
            WebSocketMessageType.COMMAND: self._handle_command_execution,
            WebSocketMessageType.STATUS: self._handle_status_request
        }

    async def connect(self, websocket: WebSocket) -> None:
        """Handle new WebSocket connection"""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.logger.info("New WebSocket connection established")
        except Exception as e:
            self.logger.error(f"Failed to establish WebSocket connection: {e}")
            raise

    def disconnect(self, websocket: WebSocket) -> None:
        """Handle WebSocket disconnection"""
        try:
            self.active_connections.remove(websocket)
            self.logger.info("WebSocket connection closed")
        except ValueError:
            self.logger.warning("Attempted to remove non-existent WebSocket connection")

    async def broadcast(self, message: WebSocketMessage) -> None:
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(asdict(message))
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                self.logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def handle_message(self, websocket: WebSocket, data: dict) -> None:
        """Route incoming messages to appropriate handlers"""
        try:
            method = data.get('method')
            handler = self.message_handlers.get(method)
            
            if not handler:
                raise ValueError(f"Unknown message type: {method}")
            
            await handler(websocket, data.get('params', {}))
        except Exception as e:
            await self._handle_error(str(e))

    async def _handle_command_execution(self, websocket: WebSocket, params: dict) -> None:
        """Handle command execution by delegating to CommandExecutionService"""
        try:
            command = params['command']
            result = await self.task_exec_service.execute_command(command)
            await self.broadcast(WebSocketMessage(
                type=WebSocketMessageType.STATUS_UPDATE,
                data=result
            ))
        except Exception as e:
            await self._handle_error(str(e))

    async def _handle_status_request(self, websocket: WebSocket, params: dict) -> None:
        """Handle status request"""
        try:
            vision_service = get_vision_service_instance()
            language_service = get_language_service_instance()
            command_service = get_command_service_instance()
            
            status = {
                "vision": vision_service.get_status() if hasattr(vision_service, 'get_status') else "running",
                "language": language_service.get_status() if hasattr(language_service, 'get_status') else "running",
                "command": command_service.get_status() if hasattr(command_service, 'get_status') else "running"
            }
            await websocket.send_json(WebSocketMessage(
                type=WebSocketMessageType.STATUS_UPDATE,
                data=status
            ).__dict__)
        except Exception as e:
            await self._handle_error(f"Error getting status: {str(e)}")

    async def _handle_error(self, error_message: str) -> None:
        """Handle and broadcast errors"""
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        await self.broadcast(WebSocketMessage(
            type=WebSocketMessageType.ERROR,
            data=error_message
        ))