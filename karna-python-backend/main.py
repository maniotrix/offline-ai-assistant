import asyncio
import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
import uvicorn
from pydantic import BaseModel
from base import SingletonMeta, ServiceManager
from modules.command_handler.command_processor import get_command_processor_instance
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

# Initialize components using singleton getters
command_processor = get_command_processor_instance()

# Store active websocket connections
active_connections: Dict[int, WebSocket] = {}

# Store current operation status
current_status = {
    "operation": None,
    "status": "idle",
    "message": "",
    "progress": 0
}

class Command(BaseModel):
    text: str

class Status(BaseModel):
    operation: Optional[str]
    status: str
    message: str
    progress: int

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection_id = id(websocket)
    active_connections[connection_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different types of messages
            if data["type"] == "command":
                # Process AI command
                result = await command_processor.process_command(data["command"])
                await websocket.send_json({
                    "type": "command_response",
                    "data": result
                })
                
            elif data["type"] == "status_request":
                # Get service instances
                vision_service = get_vision_service_instance()
                language_service = get_language_service_instance()
                command_processor = get_command_processor_instance()
                
                # Send current AI system status
                status = {
                    "vision": vision_service.get_status() if hasattr(vision_service, 'get_status') else "running",
                    "language": language_service.get_status() if hasattr(language_service, 'get_status') else "running",
                    "command": command_processor.get_status() if hasattr(command_processor, 'get_status') else "running"
                }
                await websocket.send_json({
                    "type": "status_update",
                    "data": status
                })
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        del active_connections[connection_id]

@app.get("/api/status")
async def get_status():
    return current_status

@app.post("/api/execute_command")
async def execute_command(command: Command, background_tasks: BackgroundTasks):
    global current_status
    current_status = {
        "operation": "command_execution",
        "status": "running",
        "message": f"Processing command: {command.text}",
        "progress": 0
    }
    
    # Process command in background
    background_tasks.add_task(process_command, command.text)
    return {"message": "Command execution started"}

async def process_command(command_text: str):
    global current_status
    try:
        # Process command using existing modules
        result = command_processor.process_command(command_text)
        current_status = {
            "operation": "command_execution",
            "status": "completed",
            "message": "Command executed successfully",
            "progress": 100
        }
    except Exception as e:
        current_status = {
            "operation": "command_execution",
            "status": "error",
            "message": str(e),
            "progress": 0
        }

@app.get("/api/screenshot")
async def get_screenshot():
    vision_service = get_vision_service_instance()
    screenshot = await vision_service.capture_screen()
    return {"screenshot": screenshot}

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

async def main():
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

    # Initialize orchestrator
    assistant = get_orchestrator_instance(model_paths)
    
    try:
        # Start services
        await assistant.start()
        
        # Main loop
        while True:
            command = input("Enter command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break
                
            result = await assistant.process_command(command)
            print(f"Command result: {result}")
            
    finally:
        # Cleanup
        await assistant.stop()

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=8000)