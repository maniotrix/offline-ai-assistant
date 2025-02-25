from dataclasses import dataclass
from fastapi import WebSocket
from base.base_observer import AsyncCapableObserver
from typing import Generic, TypeVar, Dict, List
import time

ObserverContext = TypeVar('ObserverContext')

@dataclass
class Connection(Generic[ObserverContext]):
    websocket: WebSocket
    client_id: str
    observer: AsyncCapableObserver[ObserverContext]

class RateLimit:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []

        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.time_window
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True