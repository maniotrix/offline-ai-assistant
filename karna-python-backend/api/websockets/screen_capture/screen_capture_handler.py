from fastapi import WebSocket
from generated.screen_capture_pb2 import (
    CaptureUpdateRequest,
    ScreenCaptureRPCRequest,
    ScreenCaptureRPCResponse,
    CaptureRequest,
    CaptureResult,
    RpcScreenshotEvent
)
from services.screen_capture_service import ScreenCaptureService, ScreenshotEvent
from api.websockets.base_handler import BaseWebSocketHandler
from typing import List

class ScreenCaptureWebSocketHandler(BaseWebSocketHandler[List[ScreenshotEvent]]):
    service: ScreenCaptureService  # Add type annotation to help type checker
    
    def __init__(self):
        super().__init__(service=ScreenCaptureService())
        self.rate_limiter.max_requests = 10  # Moderate rate limit for screen capture
        self.rate_limiter.time_window = 60  # 10 requests per minute

    async def _default_observer_callable(self, data: List[ScreenshotEvent]) -> None:
        """Default implementation for handling screenshot event updates"""
        await self.broadcast_capture_events(data)

    async def broadcast_capture_events(self, events: List[ScreenshotEvent]) -> None:
        """Broadcast screen capture events to all connected clients"""
        response = ScreenCaptureRPCResponse()
        result = CaptureResult()
        
        if events and len(events) > 0:
            # Get project and command UUIDs from first event
            result.project_uuid = events[0].project_uuid
            result.command_uuid = events[0].command_uuid
            result.is_active = self.service.is_capturing
            result.message = "Screen capture events updated"
            
            # Convert domain events to proto events
            for event in events:
                proto_event : RpcScreenshotEvent = result.screenshot_events.add()
                proto_event.event_id = event.event_id
                proto_event.project_uuid = event.project_uuid
                proto_event.command_uuid = event.command_uuid
                proto_event.timestamp = event.timestamp.isoformat()
                proto_event.description = event.description
                proto_event.screenshot_path = event.screenshot_path
                if event.annotation_path:
                    proto_event.annotation_path = event.annotation_path
                if event.mouse_x is not None:
                    proto_event.mouse_x = event.mouse_x
                if event.mouse_y is not None:
                    proto_event.mouse_y = event.mouse_y
                if event.key_char:
                    proto_event.key_char = event.key_char
                if event.key_code:
                    proto_event.key_code = event.key_code
                proto_event.is_special_key = event.is_special_key
                
        response.capture_response.CopyFrom(result)
        await self.broadcast(response)

    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        """Handle incoming WebSocket messages"""
        client_id = str(id(websocket))

        if not self.rate_limiter.is_allowed(client_id):
            response = ScreenCaptureRPCResponse()
            response.error = "Rate limit exceeded for screen capture channel"
            await websocket.send_bytes(response.SerializeToString())
            return

        try:
            request = ScreenCaptureRPCRequest()
            request.ParseFromString(data)

            method = request.WhichOneof("method")
            if method == "start_capture":
                message_content = getattr(request, method)
                self.logger.info(f"Received start capture request from client {client_id}:")
                self.logger.info(f"Project UUID: {message_content.project_uuid}")
                self.logger.info(f"Command UUID: {message_content.command_uuid}")
                await self._handle_start_capture(websocket, request.start_capture)
            elif method == "stop_capture":
                message_content = getattr(request, method)
                self.logger.info(f"Received stop capture request from client {client_id}")
                if self.service.is_capturing:
                    await self._handle_stop_capture(websocket, request.stop_capture)
                # else:
                #     response = ScreenCaptureRPCResponse()
                #     response.error = "No active screen capture session to stop"
                #     await websocket.send_bytes(response.SerializeToString())
            elif method == "update_capture":
                message_content = getattr(request, method)
                self.logger.info(f"Received update capture request from client {client_id}")
                await self.handle_update_capture(websocket, message_content.update_capture)
            else:
                response = ScreenCaptureRPCResponse()
                response.error = f"Unknown screen capture method: {method}"
                await websocket.send_bytes(response.SerializeToString())

        except Exception as e:
            self.logger.error(f"Error processing screen capture message: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = f"Error processing screen capture request: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())

    async def _handle_start_capture(
        self, websocket: WebSocket, capture_request: CaptureRequest
    ) -> None:
        """Handle start capture request"""
        try:
            self.service.start_capture(
                project_uuid=capture_request.project_uuid,
                command_uuid=capture_request.command_uuid
            )
        except Exception as e:
            self.logger.error(f"Screen capture start error: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())

    async def _handle_stop_capture(
        self, websocket: WebSocket, capture_request: CaptureRequest
    ) -> None:
        """Handle stop capture request"""
        try:
            self.service.stop_capture_special_click_event_from_client_input()
        except Exception as e:
            self.logger.error(f"Screen capture stop error: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())
            
    async def handle_update_capture(self, websocket: WebSocket, update_capture_request: CaptureUpdateRequest) -> None:
        try:
            deleted_events_ids = [str(event_id) for event_id in update_capture_request.screenshot_event_ids]
            updated_events = self.service.update_screenshot_events_json_file(
                project_uuid=update_capture_request.project_uuid,
                command_uuid=update_capture_request.command_uuid,
                deleted_events_ids=deleted_events_ids
            )
            if updated_events and len(updated_events) > 0 and self.service.current_session:
                await self.broadcast_capture_events(updated_events)
                self.logger.info(f"Updated screenshot events for {update_capture_request.project_uuid}/{update_capture_request.command_uuid}")
        except Exception as e:
            self.logger.error(f"Error updating screenshot events: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())

