import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, Optional
import asyncio

class GlobalLogger:
    def __init__(self, name="global_logger", level=logging.INFO):
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

def get_global_logger():
    return GlobalLogger().logger

global_logger = get_global_logger()

class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
        return instance

class BaseService(ABC):
    """Base class for all services in the AI assistant"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._is_running = False
        self._resources: Dict[str, Any] = {}

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize service resources"""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup service resources"""
        pass

    async def start(self) -> None:
        """Start the service"""
        if not self._is_running:
            await self.initialize()
            self._is_running = True
            self.logger.info(f"{self.__class__.__name__} started")

    async def stop(self) -> None:
        """Stop the service"""
        if self._is_running:
            await self.shutdown()
            self._is_running = False
            self.logger.info(f"{self.__class__.__name__} stopped")

    def get_resource(self, key: str) -> Optional[Any]:
        """Get a service resource by key"""
        return self._resources.get(key)

class ServiceManager:
    """Manages all service instances and their lifecycle"""
    
    def __init__(self):
        self._services: Dict[str, BaseService] = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_service(self, name: str, service: BaseService) -> None:
        """Register a new service"""
        self._services[name] = service
        self.logger.info(f"Registered service: {name}")

    async def start_all(self) -> None:
        """Start all registered services"""
        for name, service in self._services.items():
            try:
                await service.start()
            except Exception as e:
                self.logger.error(f"Failed to start {name}: {str(e)}")

    async def stop_all(self) -> None:
        """Stop all registered services"""
        for name, service in self._services.items():
            try:
                await service.stop()
            except Exception as e:
                self.logger.error(f"Failed to stop {name}: {str(e)}")

    def get_service(self, name: str) -> Optional[BaseService]:
        """Get a service by name"""
        return self._services.get(name)