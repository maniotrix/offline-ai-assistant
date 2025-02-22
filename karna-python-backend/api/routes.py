from fastapi import APIRouter, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, List
import logging
from .websocket import WebSocketManager
# from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from domain.task import TaskContext, TaskStatus
from domain.command import Command
from domain.action import Action, ActionCoordinates

router = APIRouter()
websocket_manager = WebSocketManager()

class ActionRequest(BaseModel):
    type: str
    coordinates: dict
    text: Optional[str] = None

class CommandRequest(BaseModel):
    command: str
    domain: str
    uuid: Optional[str] = None

class TaskStatusResponse(BaseModel):
    command_text: str
    status: TaskStatus
    message: str
    progress: int
    actions: Optional[List[Action]] = None

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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket_manager.handle_message(websocket, data)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        websocket_manager.disconnect(websocket)

@router.get("/api/status")
async def get_status() -> TaskStatusResponse:
    context = websocket_manager.current_status
    return TaskStatusResponse(
        command_text=context.command_text,
        status=context.status,
        message=context.message,
        progress=context.progress,
        actions=context.actions if hasattr(context, 'actions') else None
    )

@router.get("/api/screenshot")
async def get_screenshot():
    # vision_service = get_vision_service_instance()
    # screenshot = await vision_service.capture_screen()
    # return {"screenshot": screenshot}
    pass