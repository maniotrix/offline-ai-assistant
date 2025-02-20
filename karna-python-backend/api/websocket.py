from fastapi import FastAPI, WebSocket
from typing import Dict, List
import json
from modules.command_handler.command_processor import get_command_processor_instance
from modules.vision_agent import get_vision_service_instance
from modules.action_prediction import get_language_service_instance

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.command_processor = get_command_processor_instance()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def handle_message(self, websocket: WebSocket, data: dict):
        try:
            if data.get('method') == 'execute_command':
                result = await self.command_processor.process_command(data['params']['command'])
                await websocket.send_json({
                    "type": "command_response",
                    "data": result
                })
            elif data.get('method') == 'get_status':
                vision_service = get_vision_service_instance()
                language_service = get_language_service_instance()
                
                status = {
                    "vision": vision_service.get_status() if hasattr(vision_service, 'get_status') else "running",
                    "language": language_service.get_status() if hasattr(language_service, 'get_status') else "running",
                    "command": self.command_processor.get_status() if hasattr(self.command_processor, 'get_status') else "running"
                }
                await websocket.send_json({
                    "type": "status_update",
                    "data": status
                })
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "data": str(e)
            })