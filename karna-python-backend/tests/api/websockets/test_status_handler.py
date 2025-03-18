# type: ignore
import pytest
import pytest_asyncio
from api.websockets.status.status_handler import StatusWebSocketHandler
from generated.status_pb2 import StatusRPCRequest
from domain.status import StatusContext

@pytest_asyncio.fixture
async def status_handler():
    """Create a StatusWebSocketHandler instance"""
    handler = StatusWebSocketHandler()
    return handler

@pytest.mark.asyncio
async def test_connect_websocket(status_handler, mock_websocket):
    """Test WebSocket connection handling"""
    await status_handler.connect(mock_websocket)
    
    mock_websocket.accept.assert_called_once()
    client_id = str(id(mock_websocket))
    assert client_id in status_handler.active_connections

@pytest.mark.asyncio
async def test_disconnect_websocket(status_handler, mock_websocket):
    """Test WebSocket disconnection handling"""
    await status_handler.connect(mock_websocket)
    status_handler.disconnect(mock_websocket)
    
    client_id = str(id(mock_websocket))
    assert client_id not in status_handler.active_connections

@pytest.mark.asyncio
async def test_handle_status_request(status_handler, mock_websocket):
    """Test status request handling"""
    await status_handler.connect(mock_websocket)
    
    # Create status request
    request = StatusRPCRequest()
    status_req = request.get_status
    
    await status_handler._handle_status_request(mock_websocket, status_req)
    
    # Verify response was sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    assert isinstance(args[0], bytes)

@pytest.mark.asyncio
async def test_broadcast_system_status(status_handler, mock_websocket):
    """Test system status broadcasting"""
    await status_handler.connect(mock_websocket)
    
    # Create test status context
    context = StatusContext()
    context.language = "test_language"
    context.command = "test_command"
    
    await status_handler.broadcast_system_status(context)
    
    # Verify broadcast was sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    assert isinstance(args[0], bytes)

@pytest.mark.asyncio
async def test_handle_invalid_message(status_handler, mock_websocket):
    """Test handling of invalid messages"""
    await status_handler.connect(mock_websocket)
    
    # Send invalid data
    await status_handler.handle_message(mock_websocket, b"invalid data")
    
    # Verify error response sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    assert isinstance(args[0], bytes)

@pytest.mark.asyncio
async def test_rate_limit_exceeded(status_handler, mock_websocket):
    """Test rate limiting functionality"""
    await status_handler.connect(mock_websocket)
    client_id = str(id(mock_websocket))
    
    # Exhaust rate limit
    for _ in range(status_handler.rate_limiter.max_requests):
        status_handler.rate_limiter.is_allowed(client_id)
    
    # Create status request
    request = StatusRPCRequest()
    request.get_status.SetInParent()
    
    # Try to send message after rate limit exceeded
    await status_handler.handle_message(mock_websocket, request.SerializeToString())
    
    # Verify rate limit error sent
    mock_websocket.send_bytes.assert_called_once()
    args = mock_websocket.send_bytes.call_args[0]
    assert len(args) > 0
    response = args[0]
    assert b"Rate limit exceeded" in response