from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional, Any, Union
import json
import logging
import time
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
# from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.command_handler.command_processor import get_command_service_instance
from services.task_execution_service import TaskExecutorService
from domain.task import TaskContext, TaskStatus
from domain.command import Command, CommandResult
from domain.action import Action, ActionResult
from pydantic import BaseModel, ValidationError

class WebSocketMessageType(str, Enum):
    COMMAND = 'execute_command'
    STATUS = 'get_status'
    STATUS_UPDATE = 'status_update'
    ERROR = 'error'

class MessageParams(BaseModel):
    command: Optional[str] = None
    domain: Optional[str] = None

class RateLimit:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []

        # Remove old requests outside the time window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.time_window
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@dataclass
class WebSocketMessage:
    type: WebSocketMessageType
    data: Union[str, Dict, TaskContext, CommandResult, ActionResult]

    def to_dict(self) -> dict:
        if isinstance(self.data, (TaskContext, Command, Action)):
            return {
                "type": self.type,
                "data": json.loads(json.dumps(asdict(self.data), default=datetime_handler))
            }
        return {
            "type": self.type,
            "data": json.loads(json.dumps(self.data, default=datetime_handler))
        }

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.task_exec_service = TaskExecutorService()
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimit()
        self._setup_message_handlers()

    def _setup_message_handlers(self) -> None:
        """Set up message type handlers"""
        self.message_handlers = {
            WebSocketMessageType.COMMAND: self._handle_command_execution,
            WebSocketMessageType.STATUS: self._handle_status_request
        }

    def _validate_message(self, data: dict) -> Optional[str]:
        """Validate incoming message structure"""
        required_fields = ['method']
        if not all(field in data for field in required_fields):
            return "Missing required fields in message"
        
        try:
            if 'params' in data:
                MessageParams(**data['params'])
        except ValidationError as e:
            return f"Invalid message parameters: {str(e)}"
        
        return None

    async def connect(self, websocket: WebSocket) -> None:
        """Handle new WebSocket connection"""
        try:
            await websocket.accept()
            client_id = str(id(websocket))
            self.active_connections[client_id] = websocket
            self.logger.info(f"New WebSocket connection established: {client_id}")
        except Exception as e:
            self.logger.error(f"Failed to establish WebSocket connection: {e}")
            raise

    def disconnect(self, websocket: WebSocket) -> None:
        """Handle WebSocket disconnection"""
        try:
            client_id = str(id(websocket))
            if client_id in self.active_connections:
                del self.active_connections[client_id]
                self.logger.info(f"WebSocket connection closed: {client_id}")
        except Exception as e:
            self.logger.warning(f"Error during disconnect: {e}")

    async def broadcast(self, message: WebSocketMessage) -> None:
        """Broadcast message to all connected clients"""
        disconnected = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message.to_dict())
            except WebSocketDisconnect:
                disconnected.append(client_id)
            except Exception as e:
                self.logger.error(f"Error broadcasting message to {client_id}: {e}")
                disconnected.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected:
            if client_id in self.active_connections:
                self.disconnect(self.active_connections[client_id])

    async def handle_message(self, websocket: WebSocket, data: dict) -> None:
        """Route incoming messages to appropriate handlers"""
        client_id = str(id(websocket))
        
        try:
            # Rate limiting check
            if not self.rate_limiter.is_allowed(client_id):
                await self._handle_error("Rate limit exceeded. Please try again later.", websocket)
                return

            # Message validation
            validation_error = self._validate_message(data)
            if validation_error:
                await self._handle_error(validation_error, websocket)
                return

            method = data.get('method')
            if not method or method not in WebSocketMessageType.__members__.values():
                await self._handle_error(f"Unknown message type: {method}", websocket)
                return
            
            handler = self.message_handlers.get(method)
            await handler(websocket, data.get('params', {}))
            
        except Exception as e:
            await self._handle_error(f"Error processing message: {str(e)}", websocket)

    async def _handle_command_execution(self, websocket: WebSocket, params: dict) -> None:
        """Handle command execution by delegating to TaskExecutorService"""
        try:
            command = params.get('command')
            if not command:
                raise ValueError("Command parameter is required")
                
            context = await self.task_exec_service.execute_command(command)
            await self.broadcast(WebSocketMessage(
                type=WebSocketMessageType.STATUS_UPDATE,
                data=context
            ))
        except Exception as e:
            await self._handle_error(str(e), websocket)

    async def _handle_status_request(self, websocket: WebSocket, params: dict) -> None:
        """Handle status request"""
        try:
            services_status = {
                # "vision": get_vision_service_instance().get_status(),
                "language": get_language_service_instance().get_status(),
                "command": get_command_service_instance().get_status(),
                "task_execution": self.task_exec_service.get_current_status()
            }
            await self.broadcast(WebSocketMessage(
                type=WebSocketMessageType.STATUS_UPDATE,
                data=services_status
            ))
        except Exception as e:
            await self._handle_error(f"Error getting status: {str(e)}", websocket)

    async def _handle_error(self, error_message: str, websocket: Optional[WebSocket] = None) -> None:
        """Handle and broadcast errors"""
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        error_msg = WebSocketMessage(
            type=WebSocketMessageType.ERROR,
            data={"message": error_message}
        )
        
        if websocket:
            # Send error only to the affected client
            try:
                await websocket.send_json(error_msg.to_dict())
            except Exception as e:
                self.logger.error(f"Failed to send error message: {e}")
        else:
            # Broadcast error to all clients
            await self.broadcast(error_msg)

    @property
    def current_status(self) -> TaskContext:
        """Get current task execution status"""
        return self.task_exec_service.get_current_status()