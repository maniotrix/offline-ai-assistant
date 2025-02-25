from fastapi import WebSocket
from generated.command_pb2 import CommandRequest, CommandRPCRequest, CommandRPCResponse
from services.task_execution_service import TaskExecutorService
from domain.task import TaskContext
from api.websockets.base_handler import BaseWebSocketHandler
from api.websockets.command.command_utils import create_command_result


class CommandWebSocketHandler(BaseWebSocketHandler[TaskContext]):
    service: TaskExecutorService  # Add type annotation to help type checker

    def __init__(self):
        super().__init__(service=TaskExecutorService())
        self.rate_limiter.max_requests = 5  # More restrictive rate limit for commands
        self.rate_limiter.time_window = 60  # 5 requests per minute

    async def default_observer_handle_update(self, data: TaskContext) -> None:
        # Default implementation for handling updates
        await self.broadcast_task_status(data)

    async def broadcast_task_status(self, context: TaskContext) -> None:
        """Broadcast task status update to all connected clients"""
        response = CommandRPCResponse()
        response.command_response.CopyFrom(create_command_result(context))
        await self.broadcast(response)

    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        client_id = str(id(websocket))

        if not self.rate_limiter.is_allowed(client_id):
            response = CommandRPCResponse()
            response.error = "Rate limit exceeded for command channel"
            await websocket.send_bytes(response.SerializeToString())
            return

        try:
            request = CommandRPCRequest()
            request.ParseFromString(data)

            method = request.WhichOneof("method")
            if method == "execute_command":
                message_content = getattr(request, method)
                self.logger.info(f"Received message from client {client_id}:")
                self.logger.info(f"Method: {method}")
                self.logger.info(f"Content: {message_content}")
                await self._handle_command_execution(websocket, request.execute_command)
            else:
                response = CommandRPCResponse()
                response.error = f"Unknown command method: {method}"
                await websocket.send_bytes(response.SerializeToString())

        except Exception as e:
            self.logger.error(f"Error processing command message: {e}", exc_info=True)
            response = CommandRPCResponse()
            response.error = f"Error processing command: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())

    async def _handle_command_execution(
        self, websocket: WebSocket, command_request: CommandRequest
    ) -> None:
        try:
            await self.service.execute_command(
                command_request.command + ", domain " + command_request.domain
            )
        except Exception as e:
            self.logger.error(f"Command execution error: {e}", exc_info=True)
            response = CommandRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())
