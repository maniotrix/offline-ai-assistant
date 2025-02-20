import asyncio
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from base import SingletonMeta, ServiceManager
from api import setup_routes
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routes
setup_routes(app)

class AssistantOrchestrator(metaclass=SingletonMeta):
    def __init__(self, model_paths: dict):
        if not hasattr(self, '_initialized'):
            self.service_manager = ServiceManager()
            self.logger = logging.getLogger(self.__class__.__name__)
            
            # Initialize core services using singleton getters
            vision_service = get_vision_service_instance(
                model_paths['yolo_model'],
                model_paths['yolo_config']
            )
            
            language_service = get_language_service_instance(
                model_paths['language_model'],
                model_paths['language_config'],
                model_paths['tokenizer']
            )
            
            action_service = get_action_service_instance()
            
            # Register services
            self.service_manager.register_service('vision', vision_service)
            self.service_manager.register_service('language', language_service)
            self.service_manager.register_service('action', action_service)
            self._initialized = True

    async def start(self):
        """Start all services"""
        await self.service_manager.start_all()

    async def stop(self):
        """Stop all services"""
        await self.service_manager.stop_all()

    async def process_command(self, command: str):
        """Process a user command through the pipeline"""
        try:
            # Get services
            vision_service = self.service_manager.get_service('vision')
            language_service = self.service_manager.get_service('language')
            action_service = self.service_manager.get_service('action')

            # Capture current screen state
            screen = await vision_service.capture_screen()
            
            # Detect UI elements
            ui_elements = await vision_service.detect_ui_elements(screen)
            
            # Recognize intent
            intent = await language_service.recognize_intent(command)
            
            # Execute action based on intent
            if intent and intent.action_type:
                result = await action_service.execute_action(
                    intent.action_type,
                    intent.parameters
                )
                return result
            
            return None

        except Exception as e:
            self.logger.error(f"Command processing error: {str(e)}")
            raise

# Singleton instance getter
_orchestrator_instance = None

def get_orchestrator_instance(model_paths: dict = None):
    global _orchestrator_instance
    if (_orchestrator_instance is None):
        if (model_paths is None):
            raise ValueError("model_paths is required for first initialization")
        _orchestrator_instance = AssistantOrchestrator(model_paths)
    return _orchestrator_instance

@app.on_event("startup")
async def startup_event():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Setup model paths
    base_path = Path(__file__).parent
    model_paths = {
        'yolo_model': str(base_path / 'models/vision/yolo_model/weights.pth'),
        'yolo_config': str(base_path / 'models/vision/yolo_model/config.yaml'),
        'language_model': str(base_path / 'models/language/smol_lm2/weights.pth'),
        'language_config': str(base_path / 'models/language/smol_lm2/config.json'),
        'tokenizer': str(base_path / 'models/language/smol_lm2/tokenizer'),
    }

    # Initialize and start orchestrator
    assistant = get_orchestrator_instance(model_paths)
    await assistant.start()

@app.on_event("shutdown")
async def shutdown_event():
    assistant = get_orchestrator_instance()
    await assistant.stop()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)