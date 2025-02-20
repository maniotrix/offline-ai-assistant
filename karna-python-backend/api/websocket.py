from typing import Dict
from fastapi import WebSocket
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.command_processor = get_command_processor_instance()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[id(websocket)] = websocket

    def disconnect(self, websocket: WebSocket):
        connection_id = id(websocket)
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

    async def handle_message(self, websocket: WebSocket, data: dict):
        if data["type"] == "command":
            result = await self.command_processor.process_command(data["command"])
            await websocket.send_json({
                "type": "command_response",
                "data": result
            })
        
        elif data["type"] == "status_request":
            vision_service = get_vision_service_instance()
            language_service = get_language_service_instance()
            command_processor = get_command_processor_instance()
            
            status = {
                "vision": vision_service.get_status() if hasattr(vision_service, 'get_status') else "running",
                "language": language_service.get_status() if hasattr(language_service, 'get_status') else "running",
                "command": command_processor.get_status() if hasattr(command_processor, 'get_status') else "running"
            }
            await websocket.send_json({
                "type": "status_update",
                "data": status
            })