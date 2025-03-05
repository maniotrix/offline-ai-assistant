import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from base import SingletonMeta, ServiceManager
from api import setup_routes
# from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance
from modules.action_execution import get_action_service_instance
from modules.command.command_processor import get_command_service_instance
import config.db.settings as db_settings
import asyncio
from base.base_observer import AsyncCapableObserver
from robot.robot_manager import open_browser_and_get_system_bboxes
# Store reference to the main event loop
loop = asyncio.get_event_loop()
AsyncCapableObserver.set_main_loop(loop)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
data_dir = Path(__file__).parent.parent / "data"
app.mount("/data", StaticFiles(directory=str(data_dir), html=True), name="data")

# Setup routes
setup_routes(app)

class AssistantOrchestrator(metaclass=SingletonMeta):
    def __init__(self, model_paths: dict):
        if not hasattr(self, '_initialized'):
            self.service_manager = ServiceManager()
            self.logger = logging.getLogger(self.__class__.__name__)
            
            # # Initialize core services using singleton getters
            # vision_service = get_vision_service_instance(
            #     model_paths['yolo_model'],
            #     model_paths['yolo_config']
            # )
            
            language_service = get_language_service_instance(
                model_paths['language_model'],
                model_paths['language_config'],
                model_paths['tokenizer']
            )
            
            command_service = get_command_service_instance()
            action_service = get_action_service_instance()
            
            # Register services
            # self.service_manager.register_service('vision', vision_service)
            self.service_manager.register_service('language', language_service)
            self.service_manager.register_service('command', command_service)
            self.service_manager.register_service('action', action_service)
            self._initialized = True
            self.logger.info("AssistantOrchestrator initialized with all core services")

    async def start(self):
        """Start all services"""
        self.logger.info("Starting all services...")
        await self.service_manager.start_all()
        self.logger.info("All services started successfully")

    async def stop(self):
        """Stop all services"""
        self.logger.info("Stopping all services...")
        await self.service_manager.stop_all()
        self.logger.info("All services stopped successfully")

    # async def process_command(self, command: str):
    #     """Process a user command through the pipeline"""
    #     try:
    #         # Get services
    #         # vision_service = self.service_manager.get_service('vision')
    #         language_service = ()self.service_manager.get_service('language')
    #         command_service = self.service_manager.get_service('command')
    #         action_service = self.service_manager.get_service('action')

    #         if not all([#vision_service, 
    #                     language_service, command_service, action_service]):
    #             self.logger.error("One or more required services are not available")
    #             raise RuntimeError("Required services not available")

    #         # Process the command
    #         command_result = await command_service.process_command(command)
    #         if not command_result:
    #             self.logger.warning("Command processing returned no result")
    #             return None

    #         # # Capture current screen state
    #         # screen = await vision_service.capture_screen()
    #         # self.logger.debug("Screen captured successfully")
            
    #         # # Detect UI elements
    #         # ui_elements = await vision_service.detect_ui_elements(screen)
    #         # self.logger.debug(f"Detected {len(ui_elements) if ui_elements else 0} UI elements")
            
    #         # Recognize intent
    #         intent = await language_service.recognize_intent(command)
            
    #         # Execute action based on intent
    #         if intent and intent.action_type:
    #             result = await action_service.execute_action(
    #                 intent.action_type,
    #                 intent.parameters
    #             )
    #             return result
            
    #         return command_result

    #     except Exception as e:
    #         self.logger.error(f"Command processing error: {str(e)}")
    #         raise

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

    # Initialize database with default settings
    db_settings.use_default_settings()

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
    try:
        assistant = get_orchestrator_instance()
        await assistant.stop()
    except Exception as e:
        logging.error(f"Error during shutdown: {e}")

def run_app():
    """
    Run the FastAPI application with proper setup and cleanup
    """
    try:
        # Initialize database settings
        db_settings.use_default_settings()
        
        # Start browser opening process in background
        open_browser_and_get_system_bboxes()
        
        # Run the FastAPI application
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
    except Exception as e:
        logging.error(f"Application startup error: {e}")
        raise
    finally:
        # Ensure proper cleanup
        logging.info("Shutting down application...")

if __name__ == "__main__":
    run_app()