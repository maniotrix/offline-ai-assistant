from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import logging
from modules.command_handler.command_processor import get_command_service_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from modules.command_handler.command_keys import CommandKeys
from services.status_keys import StatusKeys, StatusStates, OperationTypes

@dataclass
class TaskExecutorContext:
    command_text: str
    command_result: Dict[str, Any]
    action_prediction: Optional[Any] = None
    final_results: List[Any] = None

class TaskExecutorService:
    def __init__(self):
        self.command_processor = get_command_service_instance()
        self.logger = logging.getLogger(__name__)
        self._initialize_status()

    def _initialize_status(self) -> None:
        """Initialize the current status state"""
        self.current_status = {
            StatusKeys.OPERATION.value: None,
            StatusKeys.STATUS.value: StatusStates.IDLE.value,
            StatusKeys.MESSAGE.value: "",
            StatusKeys.PROGRESS.value: 0,
            StatusKeys.RESULT.value: {}
        }

    async def execute_command(self, command_text: str) -> Dict[str, Any]:
        """Main entry point for command execution"""
        context = TaskExecutorContext(
            command_text=command_text,
            command_result={}
        )

        try:
            await self._start_command_execution(context)
            await self._process_command(context)
            
            if not context.command_result.get(CommandKeys.IS_IN_CACHE.value):
                return await self._handle_command_not_in_cache(context)
            
            await self._predict_actions(context)
            
            if not context.action_prediction or not context.action_prediction.actions:
                return await self._handle_no_actions(context)

            await self._execute_actions(context)
            return await self._finalize_command_execution(context)

        except Exception as e:
            return self._handle_error(str(e))

    async def _start_command_execution(self, context: TaskExecutorContext) -> None:
        self.logger.info(f"Processing command: {context.command_text}")
        self._update_status({
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.RUNNING.value,
            StatusKeys.MESSAGE.value: f"Processing command: {context.command_text}",
            StatusKeys.PROGRESS.value: 0
        })

    async def _process_command(self, context: TaskExecutorContext) -> None:
        self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Processing command through command service...",
            StatusKeys.PROGRESS.value: 20
        })
        context.command_result = await self.command_processor.process_command(context.command_text)
        self.logger.info(f"Command processed: {context.command_result}")
        self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Command processed, checking cache...",
            StatusKeys.PROGRESS.value: 30
        })

    async def _handle_command_not_in_cache(self, context: TaskExecutorContext) -> Dict[str, Any]:
        self.logger.info("Command not found in cache")
        status = {
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
            StatusKeys.MESSAGE.value: "Command not found in cache, needs training data collection",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: context.command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: context.command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: context.command_result.get(CommandKeys.UUID.value),
                "needs_training": True
            }
        }
        self._update_status(status)
        return self.current_status

    async def _predict_actions(self, context: TaskExecutorContext) -> None:
        self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Command found in cache, predicting actions...",
            StatusKeys.PROGRESS.value: 40
        })

        language_service = get_language_service_instance()
        context.action_prediction = await language_service.recognize_intent(
            command_id=context.command_result[CommandKeys.UUID.value]
        )

        self._update_status({
            StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
            StatusKeys.MESSAGE.value: "Actions predicted, preparing execution...",
            StatusKeys.PROGRESS.value: 50
        })

    async def _handle_no_actions(self, context: TaskExecutorContext) -> Dict[str, Any]:
        self.logger.info("No actions found in prediction cache")
        status = {
            StatusKeys.STATUS.value: StatusStates.COMPLETED.value,
            StatusKeys.MESSAGE.value: "No actions found in cache",
            StatusKeys.PROGRESS.value: 100,
            StatusKeys.RESULT.value: {
                CommandKeys.USER_COMMAND.value: context.command_result.get(CommandKeys.USER_COMMAND.value),
                CommandKeys.TASK_DOMAIN_ID.value: context.command_result.get(CommandKeys.TASK_DOMAIN_ID.value),
                CommandKeys.UUID.value: context.command_result.get(CommandKeys.UUID.value)
            }
        }
        self._update_status(status)
        return self.current_status

    async def _execute_actions(self, context: TaskExecutorContext) -> None:
        total_actions = len(context.action_prediction.actions)
        self.logger.info(f"Executing {total_actions} actions")
        
        action_service = get_action_service_instance()
        context.final_results = []

        for i, action in enumerate(context.action_prediction.actions, 1):
            progress = 50 + (i / total_actions * 40)
            self.logger.info(f"Executing action {i}/{total_actions}: {action.type}")
            
            self._update_status({
                StatusKeys.STATUS.value: StatusStates.PROCESSING.value,
                StatusKeys.MESSAGE.value: f"Executing action {i}/{total_actions}: {action.type}",
                StatusKeys.PROGRESS.value: int(progress)
            })

            params = {
                'x': action.coordinates.get('x'),
                'y': action.coordinates.get('y'),
                'text': action.text
            }
            result = await action_service.execute_action(action.type, params)
            self.logger.info(f"Action {i} result: {result}")
            context.final_results.append(result)

    async def _finalize_command_execution(self, context: TaskExecutorContext) -> Dict[str, Any]:
        success = all(result.success for result in context.final_results)
        status = {
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
        }
        self._update_status(status)
        return self.current_status

    def _handle_error(self, error_message: str) -> Dict[str, Any]:
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        status = {
            StatusKeys.OPERATION.value: OperationTypes.COMMAND_EXECUTION.value,
            StatusKeys.STATUS.value: StatusStates.ERROR.value,
            StatusKeys.MESSAGE.value: error_message,
            StatusKeys.PROGRESS.value: 0
        }
        self._update_status(status)
        return self.current_status

    def _update_status(self, status_update: dict) -> None:
        self.current_status.update(status_update)

    def get_current_status(self) -> Dict[str, Any]:
        return self.current_status