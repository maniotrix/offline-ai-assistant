from typing import Dict, Any, Optional
import logging
from modules.command_handler.command_processor import get_command_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from domain.command import Command, CommandResult
from domain.task import TaskContext, TaskStatus
from domain.action import Action, ActionResult, ActionCoordinates
from domain.intent import Intent, IntentPrediction
from services.status_keys import StatusKeys, StatusStates, OperationTypes

class TaskExecutorService:
    def __init__(self):
        self.command_processor = get_command_service_instance()
        self.logger = logging.getLogger(__name__)
        self._initialize_status()

    def _initialize_status(self) -> None:
        """Initialize the current status state"""
        self.current_status = TaskContext(
            command_text="",
            status=TaskStatus.IDLE
        )

    async def execute_command(self, command_text: str) -> TaskContext:
        """Main entry point for command execution"""
        context = TaskContext(command_text=command_text)

        try:
            await self._start_command_execution(context)
            await self._process_command(context)
            
            if not context.command or not context.command.is_in_cache:
                return await self._handle_command_not_in_cache(context)
            
            await self._predict_actions(context)
            
            if not context.actions:
                return await self._handle_no_actions(context)

            await self._execute_actions(context)
            return await self._finalize_command_execution(context)

        except Exception as e:
            return self._handle_error(str(e))

    async def _start_command_execution(self, context: TaskContext) -> None:
        self.logger.info(f"Processing command: {context.command_text}")
        context.status = TaskStatus.RUNNING
        context.message = f"Processing command: {context.command_text}"
        context.progress = 0
        self._update_status(context)

    async def _process_command(self, context: TaskContext) -> None:
        context.status = TaskStatus.PROCESSING
        context.message = "Processing command through command service..."
        context.progress = 20
        self._update_status(context)

        result = await self.command_processor.process_command(context.command_text)
        if isinstance(result, CommandResult):
            context.command = result.command
            context.command_result = result
        
        self.logger.info(f"Command processed: {context.command}")
        context.message = "Command processed, checking cache..."
        context.progress = 30
        self._update_status(context)

    async def _handle_command_not_in_cache(self, context: TaskContext) -> TaskContext:
        self.logger.info("Command not found in cache")
        context.status = TaskStatus.COMPLETED
        context.message = "Command not found in cache, needs training data collection"
        context.progress = 100
        context.needs_training = True
        self._update_status(context)
        return self.current_status

    async def _predict_actions(self, context: TaskContext) -> None:
        context.status = TaskStatus.PROCESSING
        context.message = "Command found in cache, predicting actions..."
        context.progress = 40
        self._update_status(context)

        language_service = get_language_service_instance()
        prediction = await language_service.recognize_intent(
            command_id=str(context.command.uuid)
        )
        
        if prediction:
            # Convert prediction actions to domain model
            context.actions = [
                Action(
                    type=action.type,
                    coordinates=ActionCoordinates(
                        x=action.coordinates.get('x'),
                        y=action.coordinates.get('y')
                    ),
                    text=action.text if hasattr(action, 'text') else None
                ) for action in prediction.actions
            ]

        context.message = "Actions predicted, preparing execution..."
        context.progress = 50
        self._update_status(context)

    async def _handle_no_actions(self, context: TaskContext) -> TaskContext:
        self.logger.info("No actions found in prediction cache")
        context.status = TaskStatus.COMPLETED
        context.message = "No actions found in cache"
        context.progress = 100
        self._update_status(context)
        return self.current_status

    async def _execute_actions(self, context: TaskContext) -> None:
        total_actions = len(context.actions)
        self.logger.info(f"Executing {total_actions} actions")
        
        action_service = get_action_service_instance()
        context.action_results = []

        for i, action in enumerate(context.actions, 1):
            progress = 50 + (i / total_actions * 40)
            self.logger.info(f"Executing action {i}/{total_actions}: {action.type}")
            
            context.status = TaskStatus.PROCESSING
            context.message = f"Executing action {i}/{total_actions}: {action.type}"
            context.progress = int(progress)
            self._update_status(context)

            params = {
                'x': action.coordinates.x,
                'y': action.coordinates.y,
                'text': action.text
            }
            result = await action_service.execute_action(action.type, params)
            
            # Convert to ActionResult domain model
            action_result = ActionResult(
                action=action,
                success=result.get('success', False),
                message=result.get('message', '')
            )
            context.action_results.append(action_result)
            self.logger.info(f"Action {i} result: {action_result}")

    async def _finalize_command_execution(self, context: TaskContext) -> TaskContext:
        success = all(result.success for result in context.action_results)
        context.status = TaskStatus.COMPLETED if success else TaskStatus.ERROR
        context.message = "Cached actions executed successfully" if success else "Some cached actions failed"
        context.progress = 100
        self._update_status(context)
        return self.current_status

    def _handle_error(self, error_message: str) -> TaskContext:
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        self.current_status.status = TaskStatus.ERROR
        self.current_status.message = error_message
        self.current_status.progress = 0
        return self.current_status

    def _update_status(self, context: TaskContext) -> None:
        self.current_status = context

    def get_current_status(self) -> TaskContext:
        return self.current_status