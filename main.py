import asyncio
import logging
from pathlib import Path
from base import ServiceManager
from modules.vision_agent import VisionService
from modules.action_prediction import LanguageService
from modules.action_execution import ActionService
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn
from modules.command_handler.command_processor import CommandProcessor
from modules.vision_agent import VisionAgent
from modules.action_prediction import ActionPredictor

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
command_processor = CommandProcessor()
vision_agent = VisionAgent()
action_predictor = ActionPredictor()

# Store active websocket connections
active_connections: Dict[int, WebSocket] = {}

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
                # Send current AI system status
                status = {
                    "vision_agent": vision_agent.get_status(),
                    "action_predictor": action_predictor.get_status(),
                    "command_processor": command_processor.get_status()
                }
                await websocket.send_json({
                    "type": "status_update",
                    "data": status
                })
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        del active_connections[connection_id]

class AssistantOrchestrator:
    def __init__(self, model_paths: dict):
        self.service_manager = ServiceManager()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize core services
        vision_service = VisionService(
            model_paths['yolo_model'],
            model_paths['yolo_config']
        )
        
        language_service = LanguageService(
            model_paths['language_model'],
            model_paths['language_config'],
            model_paths['tokenizer']
        )
        
        action_service = ActionService()
        
        # Register services
        self.service_manager.register_service('vision', vision_service)
        self.service_manager.register_service('language', language_service)
        self.service_manager.register_service('action', action_service)

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
    assistant = AssistantOrchestrator(model_paths)
    
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