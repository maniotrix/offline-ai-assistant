# API module initialization
from fastapi import FastAPI
from api.routes import router
from api.websockets.websocket_manager import WebSocketManager

def setup_routes(app: FastAPI):
    """Setup all API routes with the FastAPI application"""
    app.include_router(router)

__all__ = ['setup_routes', 'WebSocketManager']