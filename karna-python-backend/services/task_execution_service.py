from typing import Dict, Any, Optional
import logging
from uuid import UUID
from modules.command_handler.command_processor import get_command_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from domain.command import Command, CommandResult
from domain.task import TaskContext, TaskStatus
from domain.action import Action, ActionResult, ActionCoordinates
from domain.intent import Intent, IntentPrediction
from base.base_observer import Observable

class TaskExecutorService(Observable[TaskContext]):
    def __init__(self):
        super().__init__()
        self.command_processor = get_command_service_instance()
        self.logger = logging.getLogger(__name__)
        self._initialize_status()

    def _initialize_status(self) -> None:
        """Initialize the current status state"""
        self.current_status = TaskContext(
            command_text="",
            status=TaskStatus.PENDING
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
        context.status = TaskStatus.IN_PROGRESS
        context.message = f"Processing command: {context.command_text}"
        context.progress = 0
        self._update_status(context)

    async def _process_command(self, context: TaskContext) -> None:
        context.status = TaskStatus.IN_PROGRESS
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
        context.status = TaskStatus.IN_PROGRESS
        context.message = "Command found in cache, predicting actions..."
        context.progress = 40
        self._update_status(context)

        try:
            # Validate UUID before passing to recognize_intent
            command_uuid = str(context.command.uuid)
            try:
                UUID(command_uuid)
            except ValueError:
                raise ValueError(f"Invalid command UUID format: {command_uuid}")

            language_service = get_language_service_instance()
            prediction = await language_service.recognize_intent(command_uuid)
            
            if prediction:
                # Convert prediction actions to domain model
                context.actions = [
                    Action(
                        type=action.type,
                        coordinates=ActionCoordinates(
                            x=action.coordinates.x,
                            y=action.coordinates.y
                        ),
                        text=action.text if hasattr(action, 'text') else None
                    ) for action in prediction.intent.actions
                ]

            context.message = "Actions predicted, preparing execution..."
            context.progress = 50
            self._update_status(context)
        except ValueError as ve:
            self.logger.error(f"UUID validation error: {str(ve)}")
            context.status = TaskStatus.FAILED
            context.message = f"Invalid command format: {str(ve)}"
            context.progress = 0
            self._update_status(context)
        except Exception as e:
            self.logger.error(f"Error predicting actions: {str(e)}")
            context.status = TaskStatus.FAILED
            context.message = f"Error predicting actions: {str(e)}"
            context.progress = 0
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
            
            context.status = TaskStatus.IN_PROGRESS
            context.message = f"Executing action {i}/{total_actions}: {action.type}"
            context.progress = int(progress)
            self._update_status(context)

            # Pass the Action object directly
            result = await action_service.execute_action(action)
            
            # Result is already an ActionResult, no need to convert
            context.action_results.append(result)
            self.logger.info(f"Action {i} result: {result}")

    async def _finalize_command_execution(self, context: TaskContext) -> TaskContext:
        success = all(result.success for result in context.action_results)
        context.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        context.message = "Cached actions executed successfully" if success else "Some cached actions failed"
        context.progress = 100
        self._update_status(context)
        return self.current_status

    def _handle_error(self, error_message: str) -> TaskContext:
        self.logger.error(f"Error during execution: {error_message}", exc_info=True)
        self.current_status.status = TaskStatus.FAILED
        self.current_status.message = error_message
        self.current_status.progress = 0
        return self.current_status

    def _update_status(self, context: TaskContext) -> None:
        """Update current status and notify observers with a deep copy of the context"""
        self.current_status = context
        # Create a deep copy before notifying observers to prevent shared mutable state
        self.notify_observers(context.clone())

    def get_current_status(self) -> TaskContext:
        return self.current_status