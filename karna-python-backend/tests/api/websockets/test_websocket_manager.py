import pytest
from fastapi import WebSocketDisconnect
from api.websockets.websocket_manager import WebSocketManager, get_websocket_manager_instance

@pytest.mark.asyncio
async def test_singleton_behavior():
    """Test that WebSocketManager maintains singleton behavior"""
    manager1 = WebSocketManager()
    manager2 = WebSocketManager()
    assert manager1 is manager2
    
    # Test singleton getter
    manager3 = get_websocket_manager_instance()
    assert manager1 is manager3

@pytest.mark.asyncio
async def test_handle_command_connection(mock_websocket):
    """Test command connection handling"""
    manager = WebSocketManager()
    
    # Setup mock to raise disconnect after one message
    mock_websocket.receive_bytes.side_effect = WebSocketDisconnect()
    
    await manager.handle_command_connection(mock_websocket)
    
    # Verify connection was accepted and then disconnected
    mock_websocket.accept.assert_called_once()
    assert str(id(mock_websocket)) not in manager.command_handler.active_connections

@pytest.mark.asyncio
async def test_handle_status_connection(mock_websocket):
    """Test status connection handling"""
    manager = WebSocketManager()
    
    # Setup mock to raise disconnect after one message
    mock_websocket.receive_bytes.side_effect = WebSocketDisconnect()
    
    await manager.handle_status_connection(mock_websocket)
    
    # Verify connection was accepted and then disconnected
    mock_websocket.accept.assert_called_once()
    assert str(id(mock_websocket)) not in manager.status_handler.active_connections

@pytest.mark.asyncio
async def test_handle_connection_error(mock_websocket):
    """Test error handling in connections"""
    manager = WebSocketManager()
    
    # Setup mock to raise an error
    mock_websocket.receive_bytes.side_effect = Exception("Test error")
    
    await manager.handle_command_connection(mock_websocket)
    
    # Verify connection was accepted and then disconnected
    mock_websocket.accept.assert_called_once()
    assert str(id(mock_websocket)) not in manager.command_handler.active_connections

def test_report_active_clients(mock_websocket):
    """Test active clients reporting"""
    manager = WebSocketManager()
    
    # Initially should have no connections
    report = manager.report_active_clients()
    assert report["command_channel"] == 0
    assert report["status_channel"] == 0