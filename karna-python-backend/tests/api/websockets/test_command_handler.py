# type: ignore
import pytest
import pytest_asyncio
import asyncio
from api.websockets.command.command_handler import CommandWebSocketHandler
from generated.command_pb2 import CommandRPCRequest, CommandRPCResponse, CommandExecutionStatus

@pytest_asyncio.fixture
async def command_handler():
    """Create a CommandWebSocketHandler instance"""
    handler = CommandWebSocketHandler()
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
    
    # Start command execution
    execution_task = asyncio.create_task(
        command_handler._handle_command_execution(mock_websocket, command)
    )
    
    # Wait for all status updates
    await asyncio.sleep(0.1)  # Give time for updates to be sent
    
    # Get all calls to send_bytes
    calls = mock_websocket.send_bytes.call_args_list
    assert len(calls) > 0, "Expected at least one status update"
    
    # Verify progression of status updates
    status_sequence = []
    for args in calls:
        response_bytes = args[0][0]
        response = CommandRPCResponse()
        response.ParseFromString(response_bytes)
        if hasattr(response, 'command_response'):
            status_sequence.append(response.command_response.status)
    
    # Verify we got status updates in the expected sequence
    assert len(status_sequence) > 0, "Expected status updates"
    assert CommandExecutionStatus.PENDING in status_sequence, "Expected PENDING status"
    assert CommandExecutionStatus.IN_PROGRESS in status_sequence, "Expected IN_PROGRESS status"
    assert CommandExecutionStatus.COMPLETED in status_sequence, "Expected COMPLETED status"
    
    await execution_task

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