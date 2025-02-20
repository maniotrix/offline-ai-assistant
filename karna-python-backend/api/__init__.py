# API module initialization
from fastapi import FastAPI
from .routes import router
from .websocket import WebSocketManager

def setup_routes(app: FastAPI):
    """Setup all API routes with the FastAPI application"""
    app.include_router(router)

__all__ = ['setup_routes', 'WebSocketManager']