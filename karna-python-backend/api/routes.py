from fastapi import APIRouter, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
import logging
from .websocket import WebSocketManager
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from modules.command_handler.command_keys import CommandKeys
from .status_keys import StatusKeys, StatusStates, OperationTypes

router = APIRouter()
websocket_manager = WebSocketManager()

class Command(BaseModel):
    text: str

class Status(BaseModel):
    operation: Optional[str]
    status: str
    message: str
    progress: int

# Store current operation status using proper enums
current_status = {
    StatusKeys.OPERATION.value: None,
    StatusKeys.STATUS.value: StatusStates.IDLE.value,
    StatusKeys.MESSAGE.value: "",
    StatusKeys.PROGRESS.value: 0,
    StatusKeys.RESULT.value: {}
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
        StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
        StatusKeys.STATUS.value: StatusStates.RUNNING.value,
        StatusKeys.MESSAGE.value: f"Processing command: {command.text}",
        StatusKeys.PROGRESS.value: 0
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
        logger.info(f"Command processed through command processor: {command_result}")
        
        if not command_result.get(CommandKeys.IS_IN_CACHE.value):
            logger.info("Command not found in cache, skipping action prediction")
            current_status.update({
                StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
                StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
                StatusKeys.MESSAGE.value: "Command not found in cache",
                StatusKeys.PROGRESS.value: 100,
                StatusKeys.RESULT.value: {
                    CommandKeys.USER_COMMAND.value: command_result.get(CommandKeys.USER_COMMAND.value),
                    CommandKeys.TASK_DOMAIN_ID.value: command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                    CommandKeys.UUID.value: command_result.get(CommandKeys.UUID.value)
                }
            })
            await websocket_manager.broadcast({
                "type": "status_update",
                "data": current_status
            })
            return

        # Update status for command processing
        current_status.update({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Command found in cache, predicting actions...",
            StatusKeys.PROGRESS.value: 33
        })
        logger.info(f"Status update: {current_status}")
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })

        # Step 2: Get action predictions using command UUID
        language_service = get_language_service_instance()
        action_prediction = await language_service.recognize_intent(
            command_id=command_result[CommandKeys.UUID.value],
            uuid=command_result[CommandKeys.UUID.value]
        )
        
        # Validate action prediction result
        if not action_prediction or not action_prediction.actions:
            logger.info("No actions found in prediction cache")
            current_status.update({
                StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
                StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
                StatusKeys.MESSAGE.value: "No actions found in cache",
                StatusKeys.PROGRESS.value: 100,
                StatusKeys.RESULT.value: {
                    CommandKeys.USER_COMMAND.value: command_result.get(CommandKeys.USER_COMMAND.value),
                    CommandKeys.TASK_DOMAIN_ID.value: command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                    CommandKeys.UUID.value: command_result.get(CommandKeys.UUID.value)
                }
            })
            await websocket_manager.broadcast({
                "type": "status_update",
                "data": current_status
            })
            return

        logger.info(f"Action predictions found in cache: {len(action_prediction.actions)} actions")
        
        # Update status for action prediction
        current_status.update({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Actions found in cache, executing...",
            StatusKeys.PROGRESS.value: 66
        })
        logger.info(f"Status update: {current_status}")
        await websocket_manager.broadcast({
            "type": "status_update",
            "data": current_status
        })

        # Step 3: Execute cached actions
        action_service = get_action_service_instance()
        final_results = []
        
        for i, action in enumerate(action_prediction.actions, 1):
            logger.info(f"Executing cached action {i}/{len(action_prediction.actions)}: {action.type}")
            params = {
                'x': action.coordinates.get('x'),
                'y': action.coordinates.get('y'),
                'text': action.text
            }
            result = await action_service.execute_action(action.type, params)
            logger.info(f"Action {i} result: {result}")
            final_results.append(result)

        # Update final status
        success = all(result.success for result in final_results)
        current_status = {
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value if success else StatusStates.ERROR.value,
            StatusKeys.MESSAGE.value: "Cached actions executed successfully" if success else "Some cached actions failed",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: action_prediction.uuid,
                StatusKeys.ACTIONS_EXECUTED.value: [
                    {
                        "type": action.type,
                        "coordinates": action.coordinates,
                        "text": action.text if hasattr(action, 'text') else None,
                        "success": result.success,
                        "message": result.message
                    }
                    for action, result in zip(action_prediction.actions, final_results)
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
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.ERROR.value,
            StatusKeys.MESSAGE.value: str(e),
            StatusKeys.PROGRESS.value: 0
        }
        await websocket_manager.broadcast({
            "type": "error",
            "data": str(e)
        })