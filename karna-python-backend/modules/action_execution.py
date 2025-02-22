from base import BaseService, SingletonMeta
import pyautogui
from typing import Dict, Optional
import asyncio
import logging
from domain.action import Action, ActionResult, ActionCoordinates

class ActionService(BaseService, metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._action_queue = asyncio.Queue()
            self._running_actions = set()
            pyautogui.FAILSAFE = True
            self._initialized = True
        
    async def initialize(self) -> None:
        """Initialize action service"""
        self.logger.info("Initializing action service")
        self._worker_task = asyncio.create_task(self._action_worker())
        self._resources['worker'] = self._worker_task

    async def shutdown(self) -> None:
        """Clean up resources"""
        if hasattr(self, '_worker_task'):
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        self._running_actions.clear()
        self._resources.clear()

    async def execute_action(self, action: Action) -> ActionResult:
        """Queue an action for execution"""
        try:
            if not self._is_action_safe(action):
                return ActionResult(
                    action=action,
                    success=False,
                    message="Action validation failed"
                )

            future = asyncio.Future()
            await self._action_queue.put((action, future))
            return await future
            
        except Exception as e:
            self.logger.error(f"Action execution error: {str(e)}")
            return ActionResult(
                action=action,
                success=False,
                message=f"Execution error: {str(e)}"
            )

    def _is_action_safe(self, action: Action) -> bool:
        """Validate action safety"""
        try:
            if action.type == "click":
                if not isinstance(action.coordinates, ActionCoordinates):
                    return False
                # Ensure coordinates are within screen bounds
                screen_width, screen_height = pyautogui.size()
                return (0 <= action.coordinates.x <= screen_width and 
                       0 <= action.coordinates.y <= screen_height)
                
            elif action.type == "type":
                return isinstance(action.text, str)
                
            elif action.type == "scroll":
                return True  # Implement scroll validation if needed
                
            return False  # Unknown action type
            
        except Exception as e:
            self.logger.error(f"Action validation error: {str(e)}")
            return False

    async def _action_worker(self) -> None:
        """Background worker to process queued actions"""
        while True:
            try:
                action, future = await self._action_queue.get()
                
                if action.type in self._running_actions:
                    future.set_result(ActionResult(
                        action=action,
                        success=False,
                        message="Similar action already in progress"
                    ))
                    continue
                    
                self._running_actions.add(action.type)
                try:
                    result = await self._execute_single_action(action)
                    if not future.done():
                        future.set_result(result)
                finally:
                    self._running_actions.remove(action.type)
                    
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.logger.error(f"Action worker error: {str(e)}")

    async def _execute_single_action(self, action: Action) -> ActionResult:
        """Execute a single action"""
        try:
            if action.type == "click":
                # Move mouse smoothly
                # pyautogui.moveTo(action.coordinates.x, action.coordinates.y, duration=0.2)
                # pyautogui.click()
                return ActionResult(
                    action=action,
                    success=True,
                    message="Click successful"
                )
                
            elif action.type == "type":
                if not action.text:
                    return ActionResult(
                        action=action,
                        success=False,
                        message="No text provided for type action"
                    )
                # pyautogui.write(action.text)
                return ActionResult(
                    action=action,
                    success=True,
                    message="Text input successful"
                )
                
            elif action.type == "scroll":
                # pyautogui.scroll(amount)
                return ActionResult(
                    action=action,
                    success=True,
                    message="Scroll successful"
                )
                
            return ActionResult(
                action=action,
                success=False,
                message=f"Unknown action type: {action.type}"
            )
            
        except Exception as e:
            return ActionResult(
                action=action,
                success=False,
                message=f"Action execution failed: {str(e)}"
            )

    async def validate_action_result(self, result: ActionResult) -> bool:
        """Validate action result"""
        return result.success

# Singleton instance getter
_action_service_instance = None

def get_action_service_instance():
    global _action_service_instance
    if _action_service_instance is None:
        _action_service_instance = ActionService()
    return _action_service_instance