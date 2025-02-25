from fastapi import APIRouter, WebSocket
import logging
from api.websocket import WebSocketManager
# from modules.vision_agent import get_vision_service_instance

router = APIRouter()
websocket_manager = WebSocketManager()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.on_event("startup")
async def startup_event():
    # Initialize services and logging
    logging.basicConfig(level=logging.INFO)

@router.on_event("shutdown")
async def shutdown_event():
    pass

@router.websocket("/ws/command")
async def websocket_command_endpoint(websocket: WebSocket):
    """WebSocket endpoint for command channel"""
    await websocket_manager.handle_command_connection(websocket)

@router.websocket("/ws/status")
async def websocket_status_endpoint(websocket: WebSocket):
    """WebSocket endpoint for status channel"""
    await websocket_manager.handle_status_connection(websocket)

@router.get("/ws/clients")
async def get_active_clients():
    """Get count of active WebSocket clients per channel"""
    return websocket_manager.report_active_clients()

@router.get("/api/screenshot")
async def get_screenshot():
    # vision_service = get_vision_service_instance()
    # screenshot = await vision_service.capture_screen()
    # return {"screenshot": screenshot}
    pass