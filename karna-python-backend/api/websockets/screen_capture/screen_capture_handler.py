from fastapi import WebSocket
from generated.screen_capture_pb2 import (
    CaptureUpdateRequest,
    ScreenCaptureRPCRequest,
    ScreenCaptureRPCResponse,
    CaptureRequest,
    CaptureResult,
    RpcScreenshotEvent,
    CaptureCacheRequest,
)
from services.screen_capture_service import ScreenCaptureService, ScreenshotEvent
from api.websockets.base_handler import BaseWebSocketHandler
from typing import List
from utils.screen_capture_utils import load_screenshot_events_from_cache, ScreenCaptureUtilError

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
                if event.mouse_event_tool_tip:
                    proto_event.mouse_event_tool_tip = event.mouse_event_tool_tip
                
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
                self.logger.info(f"Project UUID: {message_content.project_uuid}")
                self.logger.info(f"Command UUID: {message_content.command_uuid}")
                if self.service.is_capturing:
                    await self._handle_stop_capture(websocket, request.stop_capture)
                # else:
                #     response = ScreenCaptureRPCResponse()
                #     response.error = "No active screen capture session to stop"
                #     await websocket.send_bytes(response.SerializeToString())
            elif method == "update_capture":
                message_content = getattr(request, method)
                self.logger.info(f"Received update capture request from client {client_id}")
                self.logger.info(f"Project UUID: {message_content.project_uuid}")
                self.logger.info(f"Command UUID: {message_content.command_uuid}")
                await self.handle_update_capture(websocket, request.update_capture)
            elif method == "get_cache":
                message_content = getattr(request, method)
                self.logger.info(f"Received get cache request from client {client_id}")
                self.logger.info(f"Project UUID: {message_content.project_uuid}")
                self.logger.info(f"Command UUID: {message_content.command_uuid}")
                await self.handle_get_cache(websocket, request.get_cache)
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
            # Check if the request includes full screenshot events
            if update_capture_request.screenshot_events and len(update_capture_request.screenshot_events) > 0:
                # Convert proto events to domain events
                updated_events = []
                for proto_event in update_capture_request.screenshot_events:
                    # Convert from proto format to domain model
                    from datetime import datetime
                    domain_event = ScreenshotEvent(
                        event_id=proto_event.event_id,
                        project_uuid=proto_event.project_uuid,
                        command_uuid=proto_event.command_uuid,
                        timestamp=datetime.fromisoformat(proto_event.timestamp),
                        description=proto_event.description,
                        screenshot_path=proto_event.screenshot_path,
                        annotation_path=proto_event.annotation_path if proto_event.annotation_path else None,
                        mouse_x=proto_event.mouse_x if proto_event.HasField('mouse_x') else None,
                        mouse_y=proto_event.mouse_y if proto_event.HasField('mouse_y') else None,
                        key_char=proto_event.key_char if proto_event.HasField('key_char') else None,
                        key_code=proto_event.key_code if proto_event.HasField('key_code') else None,
                        is_special_key=proto_event.is_special_key,
                        mouse_event_tool_tip=proto_event.mouse_event_tool_tip if proto_event.HasField('mouse_event_tool_tip') else None
                    )
                    updated_events.append(domain_event)
                
                self.logger.info(f"Updating {len(updated_events)} screenshot events")
                result_events = self.service.update_screenshot_events_json_file(
                    project_uuid=update_capture_request.project_uuid,
                    command_uuid=update_capture_request.command_uuid,
                    updated_events=updated_events
                )
            else:
                self.logger.warning("Update capture request contains no events")
                result_events = []
            
            if result_events and len(result_events) > 0 and self.service.current_session:
                await self.broadcast_capture_events(result_events)
                self.logger.info(f"Updated screenshot events for {update_capture_request.project_uuid}/{update_capture_request.command_uuid}")
            else:
                self.logger.info(f"No events to broadcast after update for {update_capture_request.project_uuid}/{update_capture_request.command_uuid}")
        except Exception as e:
            self.logger.error(f"Error updating screenshot events: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())

    async def handle_get_cache(self, websocket: WebSocket, cache_request: CaptureCacheRequest) -> None:
        """
        Handle get cache request by loading screenshot events from cache and sending them back.
        
        Args:
            websocket: The WebSocket connection
            cache_request: The cache request containing project_uuid and command_uuid
        """
        try:
            self.logger.info(f"Loading screenshot events from cache for project {cache_request.project_uuid}, command {cache_request.command_uuid}")
            screenshot_events = load_screenshot_events_from_cache(
                project_uuid=cache_request.project_uuid,
                command_uuid=cache_request.command_uuid
            )
            
            if screenshot_events and len(screenshot_events) > 0:
                await self.broadcast_capture_events(screenshot_events)
                self.logger.info(f"Sent {len(screenshot_events)} screenshot events from cache to client")
            else:
                response = ScreenCaptureRPCResponse()
                response.error = f"No screenshot events found in cache for project {cache_request.project_uuid}, command {cache_request.command_uuid}"
                await websocket.send_bytes(response.SerializeToString())
                self.logger.info(f"No screenshot events found in cache for project {cache_request.project_uuid}, command {cache_request.command_uuid}")
            
        except Exception as e:
            self.logger.error(f"Error updating screenshot events: {e}", exc_info=True)
            response = ScreenCaptureRPCResponse()
            response.error = str(e)
            await websocket.send_bytes(response.SerializeToString())
