from base import BaseService, SingletonMeta
import pyautogui
from typing import Dict, Tuple, Optional
import asyncio
from dataclasses import dataclass
import logging

@dataclass
class ActionResult:
    success: bool
    message: str
    coordinates: Optional[Tuple[int, int]] = None
    element_id: Optional[str] = None

class ActionService(BaseService, metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._action_queue = asyncio.Queue()
            self._running_actions = set()
            pyautogui.FAILSAFE = True  # Enable failsafe
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

    async def execute_action(self, action_type: str, params: Dict) -> ActionResult:
        """Queue an action for execution"""
        try:
            if not self._is_action_safe(action_type, params):
                return ActionResult(False, "Action validation failed")

            future = asyncio.Future()
            await self._action_queue.put((action_type, params, future))
            return await future
            
        except Exception as e:
            self.logger.error(f"Action execution error: {str(e)}")
            return ActionResult(False, f"Execution error: {str(e)}")

    def _is_action_safe(self, action_type: str, params: Dict) -> bool:
        """Validate action safety"""
        try:
            if action_type == "click":
                x, y = params.get('x'), params.get('y')
                if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                    return False
                # Ensure coordinates are within screen bounds
                screen_width, screen_height = pyautogui.size()
                return 0 <= x <= screen_width and 0 <= y <= screen_height
                
            elif action_type == "type":
                return isinstance(params.get('text'), str)
                
            elif action_type == "scroll":
                return isinstance(params.get('amount'), (int, float))
                
            return False  # Unknown action type
            
        except Exception as e:
            self.logger.error(f"Action validation error: {str(e)}")
            return False

    async def _action_worker(self) -> None:
        """Background worker to process queued actions"""
        while True:
            try:
                action_type, params, future = await self._action_queue.get()
                
                if action_type in self._running_actions:
                    future.set_result(ActionResult(False, "Similar action already in progress"))
                    continue
                    
                self._running_actions.add(action_type)
                try:
                    result = await self._execute_single_action(action_type, params)
                    if not future.done():
                        future.set_result(result)
                finally:
                    self._running_actions.remove(action_type)
                    
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.logger.error(f"Action worker error: {str(e)}")

    async def _execute_single_action(self, action_type: str, params: Dict) -> ActionResult:
        """Execute a single action"""
        try:
            if action_type == "click":
                x, y = params['x'], params['y']
                # Move mouse smoothly
                # pyautogui.moveTo(x, y, duration=0.2)
                # pyautogui.click()
                return ActionResult(True, "Click successful", coordinates=(x, y))
                
            elif action_type == "type":
                text = params['text']
                # pyautogui.write(text)
                return ActionResult(True, "Text input successful")
                
            elif action_type == "scroll":
                amount = params['amount']
                # pyautogui.scroll(amount)
                return ActionResult(True, "Scroll successful")
                
            return ActionResult(False, f"Unknown action type: {action_type}")
            
        except Exception as e:
            return ActionResult(False, f"Action execution failed: {str(e)}")

    async def validate_action_result(self, result: ActionResult, expected_state: Dict) -> bool:
        """Validate action result against expected state"""
        # Implement validation logic based on your requirements
        # This is a placeholder implementation
        return result.success

# Singleton instance getter
_action_service_instance = None

def get_action_service_instance():
    global _action_service_instance
    if _action_service_instance is None:
        _action_service_instance = ActionService()
    return _action_service_instance