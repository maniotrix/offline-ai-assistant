from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional, Any, Union
import json
import logging
import time
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from modules.action_prediction import get_language_service_instance
from modules.command_handler.command_processor import get_command_service_instance
# from modules.vision_agent import get_vision_service_instance
from services.task_execution_service import TaskExecutorService
from domain.task import TaskContext, TaskStatus
from domain.command import Command, CommandResult
from domain.action import Action, ActionResult
from google.protobuf.message import Message
from generated.messages_pb2 import (
    RPCRequest, 
    RPCResponse, 
    CommandRequest, 
    StatusRequest, 
    Status, 
    CommandResult as ProtoCommandResult, 
    Action as ProtoAction,
    TaskStatus as ProtoTaskStatus
)

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
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if v is not None}
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@dataclass
class WebSocketMessage:
    type: str
    data: Union[str, Dict, TaskContext, CommandResult, ActionResult]

    def to_dict(self) -> dict:
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
            'execute_command': self._handle_command_execution,
            'get_status': self._handle_status_request
        }

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
            if (client_id in self.active_connections):
                del self.active_connections[client_id]
                # Clean up rate limiter store
                if client_id in self.rate_limiter.requests:
                    del self.rate_limiter.requests[client_id]
                self.logger.info(f"WebSocket connection closed: {client_id}")
        except Exception as e:
            self.logger.warning(f"Error during disconnect: {e}")

    async def broadcast(self, response: RPCResponse) -> None:
        """Broadcast protobuf message to all connected clients"""
        if not isinstance(response, RPCResponse):
            self.logger.error("Invalid response type for broadcast")
            return
            
        message = response.SerializeToString()
        disconnected = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_bytes(message)
            except WebSocketDisconnect:
                disconnected.append(client_id)
            except Exception as e:
                self.logger.error(f"Error broadcasting message to {client_id}: {e}")
                disconnected.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected:
            if client_id in self.active_connections:
                self.disconnect(self.active_connections[client_id])

    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        """Route incoming protobuf messages to appropriate handlers"""
        client_id = str(id(websocket))
        
        try:
            if not self.rate_limiter.is_allowed(client_id):
                response = RPCResponse()
                response.error = "Rate limit exceeded. Please try again later."
                await websocket.send_bytes(response.SerializeToString())
                return

            try:
                request = RPCRequest()
                request.ParseFromString(data)
            except Exception as e:
                response = RPCResponse()
                response.error = f"Invalid protobuf message format: {str(e)}"
                await websocket.send_bytes(response.SerializeToString())
                return
            
            method = request.WhichOneof('method')
            if not method or method not in self.message_handlers:
                response = RPCResponse()
                response.error = f"Unknown message type: {method}"
                await websocket.send_bytes(response.SerializeToString())
                return
            
            message_content = getattr(request, method)
            self.logger.info(f"Received message from client {client_id}:")
            self.logger.info(f"Method: {method}")
            self.logger.info(f"Content: {message_content}")
            handler = self.message_handlers[method]
            await handler(websocket, getattr(request, method))
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}", exc_info=True)
            response = RPCResponse()
            response.error = f"Error processing message: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())

    def _task_status_to_proto(self, status: TaskStatus) -> ProtoTaskStatus:
        """Convert domain TaskStatus to protobuf TaskStatus"""
        status_map = {
            TaskStatus.PENDING: ProtoTaskStatus.PENDING,
            TaskStatus.IN_PROGRESS: ProtoTaskStatus.IN_PROGRESS,
            TaskStatus.COMPLETED: ProtoTaskStatus.COMPLETED,
            TaskStatus.FAILED: ProtoTaskStatus.FAILED
        }
        return status_map.get(status, ProtoTaskStatus.FAILED)

    def _action_to_proto(self, action: Action) -> ProtoAction:
        """Convert domain Action to protobuf Action"""
        proto_action = ProtoAction()
        proto_action.type = action.type
        if action.coordinates:
            proto_action.coordinates["x"] = str(action.coordinates.x)
            proto_action.coordinates["y"] = str(action.coordinates.y)
        if action.text:
            proto_action.text = action.text
        return proto_action

    async def _handle_command_execution(self, websocket: WebSocket, command_request: CommandRequest) -> None:
        """Handle command execution using protobuf"""
        try:
            context = await self.task_exec_service.execute_command(
                command_request.command + ", domain " + command_request.domain
                )
            
            response = RPCResponse()
            command_result = ProtoCommandResult()
            command_result.command_text = context.command_text
            command_result.status = self._task_status_to_proto(context.status)
            command_result.message = context.message or ""
            
            if hasattr(context, 'actions') and context.actions:
                for action in context.actions:
                    proto_action = command_result.actions.add()
                    proto_action.CopyFrom(self._action_to_proto(action))
            
            response.command_response.CopyFrom(command_result)
            await self.broadcast(response)
            
        except Exception as e:
            self.logger.error(f"Command execution error: {e}", exc_info=True)
            response = RPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())

    async def _handle_status_request(self, websocket: WebSocket, status_request: StatusRequest) -> None:
        """Handle status request using protobuf"""
        try:
            services_status = {
                # "vision": get_vision_service_instance().get_status(),
                "language": get_language_service_instance().get_status(),
                "command": get_command_service_instance().get_status(),
                "task_execution": self.task_exec_service.get_current_status()
            }
            
            response = RPCResponse()
            status = Status()
            # status.vision = services_status["vision"] or ""
            status.vision = ""
            status.language = services_status["language"] or ""
            status.command = services_status["command"] or ""
            
            response.status_update.CopyFrom(status)
            await self.broadcast(response)
            
        except Exception as e:
            self.logger.error(f"Status request error: {e}", exc_info=True)
            response = RPCResponse()
            response.error = f"Error getting status: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())