import asyncio
from abc import ABC, abstractmethod
from typing import Awaitable, Dict, TypeVar, Generic, Any, Optional, Callable
from weakref import WeakSet
from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime
import copy

# Define generic types for Observable and Observer
ObserverDataType = TypeVar('ObserverDataType')

class Priority(IntEnum):
    """Priority levels for observers."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class StateChange:
    """Represents a state change in the observable."""
    key: str
    old_value: Any
    new_value: Any
    timestamp: datetime
    
    
# create a base abstract class for the observer
class Observer(Generic[ObserverDataType], ABC):
    def __init__(self, priority: Priority = Priority.NORMAL):
        self.priority = priority

    @abstractmethod
    def update(self, data: ObserverDataType) -> None:
        """Method to be called when the observable's state changes."""
        pass

class AsyncCapableObserver(Observer[ObserverDataType]):
    """Base class for observers that need to handle async operations."""
    def __init__(self, handle_update: Callable[[ObserverDataType], Awaitable[None]], priority: Priority = Priority.NORMAL):
        super().__init__(priority)
        # Verify that handle_update is an async function
        if not asyncio.iscoroutinefunction(handle_update):
            raise TypeError("handle_update must be an async function")
        self._handle_update = handle_update
    
    def _schedule_async(self, coro):
        """Helper method to schedule any coroutine in the event loop"""
        try:
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(coro)
            # else:
            #     asyncio.run(coro)
        except RuntimeError:
            raise RuntimeError("Cannot schedule async operation from a running event loop.")
            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            # loop.create_task(coro)

    def update(self, data: ObserverDataType) -> None:
        """Method to be called when the observable's state changes."""
        self._schedule_async(self._handle_update(data)) # type: ignore

class Observable(Generic[ObserverDataType]):
    """Base class for objects that need to be observed."""
    
    def __init__(self):
        """Initialize the observable with an empty set of observers."""
        self._observers: Dict[Priority, WeakSet[Observer[ObserverDataType]]] = {
            priority: WeakSet() for priority in Priority
        }
        self._state: Dict[str, Any] = {}
        self._state_history: list[StateChange] = []
        self._conditions: Dict[int, Callable[[ObserverDataType], bool]] = {}

    def add_observer(self, observer: Observer[ObserverDataType], condition: Optional[Callable[[ObserverDataType], bool]] = None) -> None:
        """Add an observer with optional notification condition.
        
        Args:
            observer (Observer[T]): The observer to add
            condition (Optional[Callable[[T], bool]]): Condition for when to notify this observer
        """
        self._observers[observer.priority].add(observer)
        if condition:
            self._conditions[id(observer)] = condition

    def remove_observer(self, observer: Observer[ObserverDataType]) -> None:
        """Remove an observer from this observable."""
        try:
            self._observers[observer.priority].remove(observer)
            self._conditions.pop(id(observer), None)
        except KeyError:
            pass
        
    def remove_all_observers(self) -> None:
        """Remove all observers from this observable."""
        for priority in Priority:
            self._observers[priority].clear()
        self._conditions.clear()

    def notify_observers(self, data: ObserverDataType) -> None:
        """Notify all observers with the provided data in priority order."""
        # Notify observers in priority order (CRITICAL to LOW)
        for priority in reversed(Priority):
            for observer in self._observers[priority]:
                try:
                    condition = self._conditions.get(id(observer))
                    if condition is None or condition(data):
                        observer.update(copy.deepcopy(data))
                except Exception as e:
                    print(f"Error notifying observer {observer}: {str(e)}")

    def get_state(self, key: str) -> Any:
        """Get a value from the observable's state."""
        return self._state.get(key)

    def set_state(self, key: str, value: Any) -> None:
        """Set a value in the observable's state and track the change."""
        old_value = self._state.get(key)
        self._state[key] = value
        
        change = StateChange(
            key=key,
            old_value=old_value,
            new_value=value,
            timestamp=datetime.now()
        )
        self._state_history.append(change)

    def get_state_history(self, key: Optional[str] = None) -> list[StateChange]:
        """Get state change history, optionally filtered by key."""
        if key is None:
            return self._state_history
        return [change for change in self._state_history if change.key == key]

    @property
    def observerCount(self) -> Dict[Priority, int]:
        """Get the current number of observers per priority level."""
        return {
            priority: len(observers)
            for priority, observers in self._observers.items()
        }
