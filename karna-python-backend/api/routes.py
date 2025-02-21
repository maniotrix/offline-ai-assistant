from fastapi import APIRouter, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from .websocket import WebSocketManager
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance

router = APIRouter()
websocket_manager = WebSocketManager()

class Command(BaseModel):
    text: str

class Status(BaseModel):
    operation: Optional[str]
    status: str
    message: str
    progress: int

# Store current operation status
current_status = {
    "operation": None,
    "status": "idle",
    "message": "",
    "progress": 0
}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.on_event("startup")
async def startup_event():
    # Initialize services
    command_processor = get_command_processor_instance()
    await command_processor.initialize()

@router.on_event("shutdown")
async def shutdown_event():
    # Cleanup services
    command_processor = get_command_processor_instance()
    await command_processor.shutdown()

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
async def get_status():
    return current_status

@router.post("/api/execute_command")
async def execute_command(command: Command, background_tasks: BackgroundTasks):
    global current_status
    current_status = {
        "operation": "command_execution",
        "status": "running",
        "message": f"Processing command: {command.text}",
        "progress": 0
    }
    background_tasks.add_task(process_command, command.text)
    return {"message": "Command execution started"}

@router.get("/api/screenshot")
async def get_screenshot():
    vision_service = get_vision_service_instance()
    screenshot = await vision_service.capture_screen()
    return {"screenshot": screenshot}

async def process_command(command_text: str):
    global current_status
    try:
        command_processor = get_command_processor_instance()
        result = await command_processor.process_command(command_text)
        current_status = {
            "operation": "command_execution",
            "status": "completed",
            "message": "Command executed successfully",
            "progress": 100,
            "result": result
        }
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })
    except Exception as e:
        current_status = {
            "operation": "command_execution",
            "status": "error",
            "message": str(e),
            "progress": 0
        }
        await websocket_manager.broadcast({
            "type": "error",
            "data": str(e)
        })