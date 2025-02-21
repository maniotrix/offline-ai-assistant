from fastapi import APIRouter, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
from .websocket import WebSocketManager
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance

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
    # Initialize services and logging
    logging.basicConfig(level=logging.INFO)
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
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Processing command: {command_text}")
        
        # Step 1: Process command through command processor
        command_processor = get_command_processor_instance()
        command_result = await command_processor.process_command(command_text)
        logger.info("Command processed through command processor")
        
        # Update status for command processing
        current_status.update({
            "status": "processing",
            "message": "Command processed, predicting actions...",
            "progress": 33
        })
        logger.info(f"Status update: {current_status}")
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })

        # Step 2: Get action predictions
        language_service = get_language_service_instance()
        action_predictions = await language_service.recognize_intent(command_text)
        logger.info(f"Action predictions received: {len(action_predictions.actions)} actions")
        
        # Update status for action prediction
        current_status.update({
            "status": "processing",
            "message": "Actions predicted, executing...",
            "progress": 66
        })
        logger.info(f"Status update: {current_status}")
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })

        # Step 3: Execute predicted actions
        action_service = get_action_service_instance()
        final_results = []
        
        for i, action in enumerate(action_predictions.actions, 1):
            logger.info(f"Executing action {i}/{len(action_predictions.actions)}: {action.type}")
            params = {
                "coordinates": action.coordinates,
                "text": action.text
            }
            result = await action_service.execute_action(action.type, params)
            logger.info(f"Action {i} result: {result}")
            final_results.append(result)

        # Update final status
        success = all(result.success for result in final_results)
        current_status = {
            "operation": "command_execution",
            "status": "completed" if success else "error",
            "message": "Command executed successfully" if success else "Some actions failed",
            "progress": 100,
            "result": {
                "command_result": command_result,
                "actions_executed": [
                    {"type": action.type, "success": result.success, "message": result.message}
                    for action, result in zip(action_predictions.actions, final_results)
                ]
            }
        }
        logger.info(f"Final status update: {current_status}")
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })
    except Exception as e:
        logger.error(f"Error during command execution: {str(e)}", exc_info=True)
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