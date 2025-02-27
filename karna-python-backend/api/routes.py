from fastapi import APIRouter, WebSocket
import logging
from api.websockets.websocket_manager import get_websocket_manager_instance
from api.constants import REST, WS
# from modules.vision_agent import get_vision_service_instance

router = APIRouter()
websocket_manager = get_websocket_manager_instance()

@router.get(REST.HEALTH)
async def health_check():
    return {"status": "healthy"}

@router.on_event("startup")
async def startup_event():
    # Initialize services and logging
    logging.basicConfig(level=logging.INFO)

@router.on_event("shutdown")
async def shutdown_event():
    pass

@router.websocket(WS.COMMAND)
async def websocket_command_endpoint(websocket: WebSocket):
    """WebSocket endpoint for command channel"""
    await websocket_manager.handle_command_connection(websocket)

@router.websocket(WS.STATUS)
async def websocket_status_endpoint(websocket: WebSocket):
    """WebSocket endpoint for status channel"""
    await websocket_manager.handle_status_connection(websocket)
    
@router.websocket(WS.SCREEN_CAPTURE)
async def websocket_screen_capture_endpoint(websocket: WebSocket):
    """WebSocket endpoint for screen capture channel"""
    await websocket_manager.handle_screen_capture_connection(websocket)

# @router.get(REST.ACTIVE_CLIENTS)
# async def get_active_clients():
#     """Get count of active WebSocket clients per channel"""
#     return websocket_manager.report_active_clients()

@router.get(REST.SCREENSHOT)
async def get_screenshot():
    # vision_service = get_vision_service_instance()
    # screenshot = await vision_service.capture_screen()
    # return {"screenshot": screenshot}
    pass