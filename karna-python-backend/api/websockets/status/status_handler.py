from typing import Coroutine
from attr import dataclass
from fastapi import WebSocket

from api.websockets.base_handler import BaseWebSocketHandler
from generated.status_pb2 import (
    StatusRequest,
    StatusRPCRequest,
    StatusRPCResponse,
    StatusResult,
)
from modules.action_prediction import get_language_service_instance
from modules.command_handler.command_processor import get_command_service_instance
from base.base_observer import AsyncCapableObserver, Observable
from api.websockets.base_models import Connection


@dataclass
class StatusContext:
    """Context for status updates."""

    language: str = ""
    command: str = ""


class StatusService(Observable[StatusContext]):
    async def update_system_status(self) -> None:
        context = StatusContext(
            language=get_language_service_instance().get_status(),
            command=get_command_service_instance().get_status(),
        )
        self.notify_observers(context)


class StatusWebSocketHandler(BaseWebSocketHandler):
    def __init__(self):
        super().__init__()
        self.status_service = StatusService()
        self.rate_limiter.max_requests = 20  # More permissive rate limit for status
        self.rate_limiter.time_window = 60  # 20 requests per minute

    def _create_connection(
        self, websocket: WebSocket, client_id: str, observer: AsyncCapableObserver
    ) -> Connection[StatusContext]:
        return Connection[StatusContext](
            websocket=websocket, client_id=client_id, observer=observer
        )
        
    async def _post_connect(self, connection: Connection[StatusContext]) -> None:
        """Post-connection setup - to be overridden by subclasses"""
        observer = connection.observer
        if observer is None:
            observer = self.get_default_observer()
        self.status_service.add_observer(observer)
    
    def _pre_disconnect(self, connection: Connection[StatusContext]) -> None:
        """Pre-disconnection cleanup - to be overridden by subclasses"""
        self.status_service.remove_observer(connection.observer)

    def get_default_observer(self) -> AsyncCapableObserver[StatusContext]:
        observer = AsyncCapableObserver[StatusContext](self.broadcast_system_status)
        return observer

    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        client_id = str(id(websocket))

        if not self.rate_limiter.is_allowed(client_id):
            response = StatusRPCResponse()
            response.error = "Rate limit exceeded for status channel"
            await websocket.send_bytes(response.SerializeToString())
            return

        try:
            request = StatusRPCRequest()
            request.ParseFromString(data)

            method = request.WhichOneof("method")
            if method == "get_status":
                await self._handle_status_request(websocket, request.get_status)
            else:
                response = StatusRPCResponse()
                response.error = f"Unknown status method: {method}"
                await websocket.send_bytes(response.SerializeToString())

        except Exception as e:
            self.logger.error(f"Error processing status message: {e}", exc_info=True)
            response = StatusRPCResponse()
            response.error = f"Error processing status request: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())

    async def _handle_status_request(
        self, websocket: WebSocket, status_request: StatusRequest
    ) -> None:
        try:
            await self.status_service.update_system_status()

        except Exception as e:
            self.logger.error(f"Status request error: {e}", exc_info=True)
            response = StatusRPCResponse()
            response.error = f"Error getting status: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())

    async def broadcast_system_status(self, context: StatusContext):
        response = StatusRPCResponse()
        status = StatusResult()
        # status.vision = services_status["vision"] or ""
        status.vision = ""
        status.language = context.language or ""
        status.command = context.command or ""

        response.status_update.CopyFrom(status)
        await self.broadcast(response)
