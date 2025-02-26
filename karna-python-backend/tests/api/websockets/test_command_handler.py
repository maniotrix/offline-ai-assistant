import pytest
from unittest.mock import MagicMock
import pytest_asyncio
from api.websockets.command.command_handler import CommandWebSocketHandler
from generated.command_pb2 import CommandRPCRequest, CommandRequest

@pytest_asyncio.fixture
async def command_handler(mock_task_service):
    """Create a CommandWebSocketHandler instance with mocked service"""
    handler = CommandWebSocketHandler()
    handler.service = mock_task_service
    return handler

@pytest.mark.asyncio
async def test_connect_websocket(command_handler, mock_websocket):
    """Test WebSocket connection handling"""
    await command_handler.connect(mock_websocket)
    
    mock_websocket.accept.assert_called_once()
    client_id = str(id(mock_websocket))
    assert client_id in command_handler.active_connections

@pytest.mark.asyncio
async def test_disconnect_websocket(command_handler, mock_websocket):
    """Test WebSocket disconnection handling"""
    await command_handler.connect(mock_websocket)
    command_handler.disconnect(mock_websocket)
    
    client_id = str(id(mock_websocket))
    assert client_id not in command_handler.active_connections

@pytest.mark.asyncio
async def test_handle_command_execution(command_handler, mock_websocket):
    """Test command execution handling"""
    await command_handler.connect(mock_websocket)
    
    # Create command request
    request = CommandRPCRequest()
    command = request.execute_command
    command.command = "test command"
    command.domain = "test"
    
    await command_handler._handle_command_execution(mock_websocket, command)
    
    # Verify service called with correct command
    command_handler.service.execute_command.assert_called_once_with(
        "test command, domain test"
    )

@pytest.mark.asyncio
async def test_handle_invalid_message(command_handler, mock_websocket):
    """Test handling of invalid messages"""
    await command_handler.connect(mock_websocket)
    
    # Send invalid data
    await command_handler.handle_message(mock_websocket, b"invalid data")
    
    # Verify error response sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    assert isinstance(args[0], bytes)

@pytest.mark.asyncio
async def test_rate_limit_exceeded(command_handler, mock_websocket):
    """Test rate limiting functionality"""
    await command_handler.connect(mock_websocket)
    client_id = str(id(mock_websocket))
    
    # Exhaust rate limit
    for _ in range(command_handler.rate_limiter.max_requests):
        command_handler.rate_limiter.is_allowed(client_id)
    
    # Create command request
    request = CommandRPCRequest()
    command = request.execute_command
    command.command = "test command"
    command.domain = "test"
    
    # Try to send message after rate limit exceeded
    await command_handler.handle_message(mock_websocket, request.SerializeToString())
    
    # Verify rate limit error sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    response = args[0]
    assert b"Rate limit exceeded" in response