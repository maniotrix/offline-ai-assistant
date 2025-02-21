from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional, Any, Callable
import json
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from modules.command_handler.command_keys import CommandKeys
from .status_keys import StatusKeys, StatusStates, OperationTypes

"""copilot last edit response:
Let me explain the key improvements made to the WebSocketManager class:

Added proper type hints and docstrings for better code maintainability
Introduced enums for message types to prevent string literal usage
Created dataclasses for structured message and context objects
Improved error handling with dedicated error handler method
Split command execution into smaller, focused methods following single responsibility principle
Added connection state management with proper cleanup of disconnected clients
Improved logging throughout the class
Made the code more maintainable by using proper Python idioms and patterns
We can further improve this implementation by:

Adding connection heartbeat monitoring
Implementing retry mechanisms for failed actions
Adding rate limiting for commands
Adding message queuing for handling high load
Implementing connection pooling for services
Would you like me to implement any of these additional improvements?
    """
    
class WebSocketMessageType(str, Enum):
    COMMAND = 'execute_command'
    STATUS = 'get_status'
    STATUS_UPDATE = 'status_update'
    ERROR = 'error'

@dataclass
class WebSocketMessage:
    type: str
    data: Any

@dataclass
class CommandExecutionContext:
    command_text: str
    command_result: Dict[str, Any]
    action_prediction: Optional[Any] = None
    final_results: List[Any] = None

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.command_processor = get_command_processor_instance()
        self.logger = logging.getLogger(__name__)
        self._initialize_status()
        self._setup_message_handlers()

    def _initialize_status(self) -> None:
        """Initialize the current status state"""
        self.current_status = {
            StatusKeys.OPERATION.value: None,
            StatusKeys.STATUS.value: StatusStates.IDLE.value,
            StatusKeys.MESSAGE.value: "",
            StatusKeys.PROGRESS.value: 0,
            StatusKeys.RESULT.value: {}
        }

    def _setup_message_handlers(self) -> None:
        """Set up message type handlers"""
        self.message_handlers = {
            WebSocketMessageType.COMMAND: self._handle_command_execution,
            WebSocketMessageType.STATUS: self._handle_status_request
        }

    async def connect(self, websocket: WebSocket) -> None:
        """Handle new WebSocket connection"""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.logger.info("New WebSocket connection established")
        except Exception as e:
            self.logger.error(f"Failed to establish WebSocket connection: {e}")
            raise

    def disconnect(self, websocket: WebSocket) -> None:
        """Handle WebSocket disconnection"""
        try:
            self.active_connections.remove(websocket)
            self.logger.info("WebSocket connection closed")
        except ValueError:
            self.logger.warning("Attempted to remove non-existent WebSocket connection")

    async def broadcast(self, message: WebSocketMessage) -> None:
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(asdict(message))
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                self.logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def handle_message(self, websocket: WebSocket, data: dict) -> None:
        """Route incoming messages to appropriate handlers"""
        try:
            method = data.get('method')
            handler = self.message_handlers.get(method)
            
            if not handler:
                raise ValueError(f"Unknown message type: {method}")
            
            await handler(websocket, data.get('params', {}))
        except Exception as e:
            await self._handle_error(str(e))

    async def _update_status(self, status_update: dict) -> None:
        """Update current status and broadcast to clients"""
        self.current_status.update(status_update)
        await self.broadcast(WebSocketMessage(
            type=WebSocketMessageType.STATUS_UPDATE,
            data=self.current_status
        ))

    async def _handle_command_execution(self, websocket: WebSocket, params: dict) -> None:
        """Handle command execution workflow"""
        context = CommandExecutionContext(
            command_text=params['command'],
            command_result={}
        )

        try:
            await self._start_command_execution(context)
            await self._process_command(context)
            
            if not context.command_result.get(CommandKeys.IS_IN_CACHE.value):
                await self._handle_command_not_in_cache(context)
                return

            await self._predict_actions(context)
            
            if not context.action_prediction or not context.action_prediction.actions:
                await self._handle_no_actions(context)
                return

            await self._execute_actions(context)
            await self._finalize_command_execution(context)

        except Exception as e:
            await self._handle_error(str(e))

    async def _start_command_execution(self, context: CommandExecutionContext) -> None:
        """Initialize command execution process"""
        self.logger.info(f"Processing command: {context.command_text}")
        await self._update_status({
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.RUNNING.value,
            StatusKeys.MESSAGE.value: f"Processing command: {context.command_text}",
            StatusKeys.PROGRESS.value: 0
        })

    async def _process_command(self, context: CommandExecutionContext) -> None:
        """Process command through command processor"""
        context.command_result = await self.command_processor.process_command(context.command_text)
        self.logger.info(f"Command processed: {context.command_result}")

    async def _handle_command_not_in_cache(self, context: CommandExecutionContext) -> None:
        """Handle case when command is not found in cache"""
        self.logger.info("Command not found in cache")
        await self._update_status({
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
            StatusKeys.MESSAGE.value: "Command not found in cache",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: context.command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: context.command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: context.command_result.get(CommandKeys.UUID.value)
            }
        })

    async def _predict_actions(self, context: CommandExecutionContext) -> None:
        """Predict actions for the command"""
        await self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Command found in cache, predicting actions...",
            StatusKeys.PROGRESS.value: 33
        })

        language_service = get_language_service_instance()
        context.action_prediction = await language_service.recognize_intent(
            command_id=context.command_result[CommandKeys.UUID.value],
            uuid=context.command_result[CommandKeys.UUID.value]
        )

    async def _handle_no_actions(self, context: CommandExecutionContext) -> None:
        """Handle case when no actions are found"""
        self.logger.info("No actions found in prediction cache")
        await self._update_status({
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
            StatusKeys.MESSAGE.value: "No actions found in cache",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: context.command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: context.command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: context.command_result.get(CommandKeys.UUID.value)
            }
        })

    async def _execute_actions(self, context: CommandExecutionContext) -> None:
        """Execute predicted actions"""
        self.logger.info(f"Executing {len(context.action_prediction.actions)} actions")
        await self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Actions found in cache, executing...",
            StatusKeys.PROGRESS.value: 66
        })

        action_service = get_action_service_instance()
        context.final_results = []

        for i, action in enumerate(context.action_prediction.actions, 1):
            self.logger.info(f"Executing action {i}/{len(context.action_prediction.actions)}: {action.type}")
            params = {
                'x': action.coordinates.get('x'),
                'y': action.coordinates.get('y'),
                'text': action.text
            }
            result = await action_service.execute_action(action.type, params)
            self.logger.info(f"Action {i} result: {result}")
            context.final_results.append(result)

    async def _finalize_command_execution(self, context: CommandExecutionContext) -> None:
        """Finalize command execution and update status"""
        success = all(result.success for result in context.final_results)
        await self._update_status({
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value if success else StatusStates.ERROR.value,
            StatusKeys.MESSAGE.value: "Cached actions executed successfully" if success else "Some cached actions failed",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: context.command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: context.command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: context.action_prediction.uuid,
                StatusKeys.ACTIONS_EXECUTED.value: [
                    {
                        "type": action.type,
                        "coordinates": action.coordinates,
                        "text": action.text if hasattr(action, 'text') else None,
                        "success": result.success,
                        "message": result.message
                    }
                    for action, result in zip(context.action_prediction.actions, context.final_results)
                ]
            }
        })

    async def _handle_status_request(self, websocket: WebSocket, params: dict) -> None:
        """Handle status request"""
        try:
            vision_service = get_vision_service_instance()
            language_service = get_language_service_instance()
            
            # Get command status based on current operation state
            command_status = ""
            if self.current_status[StatusKeys.OPERATION.value] == OperationTypes.COMMAND_EXECUTION.value:
                command_status = "running"
            
            status = {
                "vision": vision_service.get_status() if hasattr(vision_service, 'get_status') else "running",
                "language": language_service.get_status() if hasattr(language_service, 'get_status') else "running",
                "command": command_status
            }
            await websocket.send_json(WebSocketMessage(
                type=WebSocketMessageType.STATUS_UPDATE,
                data=status
            ).__dict__)
        except Exception as e:
            await self._handle_error(f"Error getting status: {str(e)}")

    async def _handle_error(self, error_message: str) -> None:
        """Handle and broadcast errors"""
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        self.current_status.update({
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.ERROR.value,
            StatusKeys.MESSAGE.value: error_message,
            StatusKeys.PROGRESS.value: 0
        })
        await self.broadcast(WebSocketMessage(
            type=WebSocketMessageType.ERROR,
            data=error_message
        ))