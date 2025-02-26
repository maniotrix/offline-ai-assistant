import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocket
from typing import Generator, AsyncGenerator
import asyncio
from unittest.mock import MagicMock, AsyncMock
from api.websockets.websocket_manager import WebSocketManager
from services.task_execution_service import TaskExecutorService
from services.status_service import StatusService
from main import app

@pytest.fixture
def test_client() -> Generator:
    """Create a test client instance"""
    with TestClient(app) as client:
        yield client

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
def mock_task_service() -> MagicMock:
    """Create a mock TaskExecutorService"""
    mock = MagicMock(spec=TaskExecutorService)
    mock.execute_command = AsyncMock()
    mock.add_observer = MagicMock()
    mock.remove_observer = MagicMock()
    return mock

@pytest.fixture
def mock_status_service() -> MagicMock:
    """Create a mock StatusService"""
    mock = MagicMock(spec=StatusService)
    mock.update_system_status = AsyncMock()
    mock.add_observer = MagicMock()
    mock.remove_observer = MagicMock()
    return mock

@pytest.fixture
def websocket_manager() -> WebSocketManager:
    """Create a WebSocketManager instance"""
    manager = WebSocketManager()
    return manager