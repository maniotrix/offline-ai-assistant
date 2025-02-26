import pytest
from fastapi import WebSocket
from unittest.mock import MagicMock, AsyncMock
from api.websockets.websocket_manager import WebSocketManager

@pytest.fixture
def mock_websocket() -> MagicMock:
    """Create a mock WebSocket instance"""
    mock = MagicMock(spec=WebSocket)
    # Setup async mock methods
    mock.accept = AsyncMock()
    mock.receive_bytes = AsyncMock()
    mock.send_bytes = AsyncMock()
    mock.close = AsyncMock()
    return mock

@pytest.fixture
def websocket_manager() -> WebSocketManager:
    """Create a WebSocketManager instance"""
    manager = WebSocketManager()
    return manager