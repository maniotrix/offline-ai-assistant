from abc import ABC, abstractmethod
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, TypeVar, Generic
import logging

from api.websockets.base_models import Connection, RateLimit
from google.protobuf.message import Message

from base.base_observer import AsyncCapableObserver
from services.base_service import BaseService

T = TypeVar("T")


class BaseWebSocketHandler(Generic[T], ABC):
    def __init__(self, service: BaseService[T]):
        self.service = service
        self.active_connections: Dict[str, Connection[T]] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rate_limiter = RateLimit()
        
    async def default_observer_handle_update(self, data: T) -> None:
        # Default implementation for handling updates
        raise NotImplementedError("Default observer's handle_update not implemented")

    def get_default_observer(self) -> AsyncCapableObserver[T]:
        return AsyncCapableObserver[T](self.default_observer_handle_update)
    
    async def connect(
        self, websocket: WebSocket, observer: AsyncCapableObserver | None = None
    ) -> None:
        """Handle new WebSocket connection"""
        try:
            await websocket.accept()
            client_id = str(id(websocket))
            connection = self._create_connection(websocket, client_id, observer)
            self.active_connections[client_id] = connection
            self.logger.info(f"New WebSocket connection established: {client_id}")
            await self._post_connect(connection)
        except Exception as e:
            self.logger.error(f"Failed to establish WebSocket connection: {e}")
            raise

    @abstractmethod
    def _create_connection(
        self, websocket: WebSocket, client_id: str, observer: AsyncCapableObserver
    ) -> Connection:
        """Create a new connection instance - to be overridden by subclasses"""
        return Connection(websocket=websocket, client_id=client_id, observer=observer)


    @abstractmethod
    async def _post_connect(self, connection: Connection[T]) -> None:
        """Post-connection setup - to be overridden by subclasses"""
        observer = connection.observer
        if observer is None:
            observer = self.get_default_observer()
        self.service.add_observer(observer)

    def disconnect(self, websocket: WebSocket) -> None:
        """Handle WebSocket disconnection"""
        try:
            client_id = str(id(websocket))
            if client_id in self.active_connections:
                self._pre_disconnect(self.active_connections[client_id])
                del self.active_connections[client_id]
                if client_id in self.rate_limiter.requests:
                    del self.rate_limiter.requests[client_id]
                self.logger.info(f"WebSocket connection closed: {client_id}")
        except Exception as e:
            self.logger.warning(f"Error during disconnect: {e}")

    @abstractmethod
    def _pre_disconnect(self, connection: Connection[T]) -> None:
        """Pre-disconnection cleanup - to be overridden by subclasses"""
        self.service.remove_observer(connection.observer)

    async def broadcast(self, message: Message) -> None:  #
        """Broadcast protobuf message to all connected clients"""
        if not isinstance(message, Message):
            self.logger.error("Invalid message type for broadcast")
            return

        data = message.SerializeToString()
        disconnected: List[str] = []
        # log current active connections
        self.report_active_clients()
        for client_id, connection in self.active_connections.items():
            try:
                await connection.websocket.send_bytes(data)
            except WebSocketDisconnect:
                disconnected.append(client_id)
            except Exception as e:
                self.logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            if client_id in self.active_connections:
                self.disconnect(self.active_connections[client_id].websocket)

    def report_active_clients(self) -> None:
            self.logger.info(f"======{self.__class__.__name__} Connection Status ======")
            self.logger.info(f"🔌 Active Connections Count: {len(self.active_connections)}")
            self.logger.info(f"🆔 Connected Client IDs: {list(self.active_connections.keys())}")
            self.logger.info(f"📡 Active Connection Details: {self.active_connections}")
            self.logger.info("========================================")

    @abstractmethod
    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        """Handle incoming messages - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement handle_message")
