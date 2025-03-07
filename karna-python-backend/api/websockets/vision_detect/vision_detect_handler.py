import asyncio
from fastapi import WebSocket
from typing import List, Optional, Dict, Any, cast
import logging
from datetime import datetime

from api.websockets.base_handler import BaseWebSocketHandler
from services.vision_detect_service import VisionDetectService, get_vision_detect_service_instance
from inference import VisionDetectResultModelList, VisionDetectResultModel
from services.screen_capture_service import ScreenshotEvent

# Import the generated protobuf classes
# Note: These will be generated after running the protoc compiler on vision_detect.proto
from generated.vision_detect_pb2 import (
    VisionDetectRPCRequest,
    VisionDetectRPCResponse,
    GetResultsRequest,
    UpdateResultsRequest,
    VisionDetectResultsList,
    VisionDetectResultModel as ProtoVisionDetectResultModel,
    BoundingBox as ProtoBoundingBox,
    VisionDetectStatus
)

logger = logging.getLogger(__name__)

class VisionDetectWebSocketHandler(BaseWebSocketHandler[VisionDetectResultModelList]):
    """WebSocket handler for vision detection service."""
    
    service: VisionDetectService  # Type annotation to help type checker
    
    def __init__(self):
        """Initialize the WebSocket handler with the VisionDetectService."""
        super().__init__(service=get_vision_detect_service_instance())
        self.rate_limiter.max_requests = 10  # Moderate rate limit
        self.rate_limiter.time_window = 60   # 10 requests per minute
        logger.info("VisionDetectWebSocketHandler initialized")
    
    async def _default_observer_callable(self, data: VisionDetectResultModelList) -> None:
        """Default implementation for handling vision detection result updates.
        
        Args:
            data: The updated vision detection results.
        """
        logger.info("Observer received vision detection results update")
        await self.broadcast_results(data)
    
    async def handle_message(self, websocket: WebSocket, data: bytes) -> None:
        """Handle incoming WebSocket messages.
        
        Args:
            websocket: The WebSocket connection.
            data: The binary message data.
        """
        client_id = str(id(websocket))
        
        # Check rate limiting
        if not self.rate_limiter.is_allowed(client_id):
            response = VisionDetectRPCResponse()
            response.error = "Rate limit exceeded for vision detection channel"
            await websocket.send_bytes(response.SerializeToString())
            return
        
        try:
            # Parse the request
            request = VisionDetectRPCRequest()
            request.ParseFromString(data)
            
            # Determine which method was called
            method = request.WhichOneof("method")
            if method == "get_results_request":
                await self._handle_get_results_request(websocket, request.get_results_request)
            elif method == "update_results_request":
                await self._handle_update_results_request(websocket, request.update_results_request)
            else:
                response = VisionDetectRPCResponse()
                response.error = f"Unknown vision detection method: {method}"
                await websocket.send_bytes(response.SerializeToString())
        
        except Exception as e:
            logger.error(f"Error processing vision detection message: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error processing vision detection request: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    async def _handle_get_results_request(self, websocket: WebSocket, get_results_request: GetResultsRequest) -> None:
        """Handle a request to get vision detection results.
        
        Args:
            websocket: The WebSocket connection.
            get_results_request: The get results request.
        """
        client_id = str(id(websocket))
        logger.info("Received get results request from client: %s", client_id)
        try:
            # Convert RpcScreenshotEvent objects to ScreenshotEvent objects
            logger.info("Converting RPC screenshot events to Python model")
            screenshot_events = []
            for rpc_event in get_results_request.screenshot_events:
                # Convert timestamp string to datetime
                timestamp = datetime.fromisoformat(rpc_event.timestamp)
                
                # Create ScreenshotEvent from RpcScreenshotEvent
                screenshot_event = ScreenshotEvent(
                    event_id=rpc_event.event_id,
                    project_uuid=rpc_event.project_uuid,
                    command_uuid=rpc_event.command_uuid,
                    timestamp=timestamp,
                    description=rpc_event.description,
                    screenshot_path=rpc_event.screenshot_path,
                    annotation_path=rpc_event.annotation_path if rpc_event.annotation_path else None,
                    mouse_x=rpc_event.mouse_x if rpc_event.mouse_x else None,
                    mouse_y=rpc_event.mouse_y if rpc_event.mouse_y else None,
                    key_char=rpc_event.key_char if rpc_event.key_char else None,
                    key_code=rpc_event.key_code if rpc_event.key_code else None,
                    is_special_key=rpc_event.is_special_key
                )
                screenshot_events.append(screenshot_event)
            
            # ask service to process screenshot events
            logger.info("Asking service to process screenshot events with length: %d", len(screenshot_events))
            # The service method is synchronous, not a coroutine, so we can't use create_task directly
            # Instead, run it in a thread pool to avoid blocking
            await asyncio.to_thread(self.service.set_and_process_screenshot_events, screenshot_events)
        
        except Exception as e:
            logger.error(f"Error getting vision detection results: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error getting vision detection results: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    async def _handle_update_results_request(self, websocket: WebSocket, update_request: UpdateResultsRequest) -> None:
        """Handle a request to update vision detection results.
        
        Args:
            websocket: The WebSocket connection.
            update_request: The update results request.
        """
        client_id = str(id(websocket))
        logger.info("Received update results request from client: %s", client_id)
        try:
            # Convert proto results to Python model
            python_results = self._convert_from_proto_results(update_request.results)
            
            # Update the results in the service
            self.service.update_vision_detect_results(python_results)
            
            # Send success response
            response = VisionDetectRPCResponse()
            status = VisionDetectStatus()
            status.status = "Results updated successfully"
            status.has_results = True
            status.results_count = len(python_results.vision_detect_result_models)
            response.status.CopyFrom(status)
            
            await websocket.send_bytes(response.SerializeToString())
        
        except Exception as e:
            logger.error(f"Error updating vision detection results: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error updating vision detection results: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    def _convert_to_proto_results(self, results: VisionDetectResultModelList) -> VisionDetectResultsList:
        """Convert VisionDetectResultModelList to protobuf VisionDetectResultsList.
        
        Args:
            results: The vision detection results.
            
        Returns:
            VisionDetectResultsList: The protobuf vision detection results.
        """
        proto_results = VisionDetectResultsList()
        proto_results.project_uuid = results.project_uuid
        proto_results.command_uuid = results.command_uuid
        
        for result in results.vision_detect_result_models:
            proto_result = ProtoVisionDetectResultModel()
            proto_result.event_id = result.event_id
            proto_result.project_uuid = result.project_uuid
            proto_result.command_uuid = result.command_uuid
            proto_result.timestamp = result.timestamp.isoformat()
            proto_result.description = result.description
            proto_result.original_image_path = result.original_image_path
            proto_result.original_width = result.original_width
            proto_result.original_height = result.original_height
            proto_result.is_cropped = result.is_cropped
            
            # Convert bounding boxes
            for bbox in result.merged_ui_icon_bboxes:
                proto_bbox = ProtoBoundingBox()
                proto_bbox.id = bbox.id
                proto_bbox.x = bbox.x
                proto_bbox.y = bbox.y
                proto_bbox.width = bbox.width
                proto_bbox.height = bbox.height
                proto_bbox.class_name = bbox.class_name
                proto_bbox.confidence = bbox.confidence
                proto_result.merged_ui_icon_bboxes.append(proto_bbox)
            
            # Add cropped image data if available
            if result.cropped_image:
                # Convert PIL Image to bytes
                import io
                img_byte_arr = io.BytesIO()
                result.cropped_image.save(img_byte_arr, format='PNG')
                proto_result.cropped_image = img_byte_arr.getvalue()
                
            if result.cropped_width is not None:
                proto_result.cropped_width = result.cropped_width
                
            if result.cropped_height is not None:
                proto_result.cropped_height = result.cropped_height
            
            proto_results.results.append(proto_result)
        
        return proto_results
    
    def _convert_from_proto_results(self, proto_results: VisionDetectResultsList) -> VisionDetectResultModelList:
        """Convert protobuf VisionDetectResultsList to VisionDetectResultModelList.
        
        Args:
            proto_results: The protobuf vision detection results.
            
        Returns:
            VisionDetectResultModelList: The Python vision detection results.
        """
        from PIL import Image
        import io
        
        results = VisionDetectResultModelList(
            project_uuid=proto_results.project_uuid,
            command_uuid=proto_results.command_uuid,
            vision_detect_result_models=[]
        )
        
        for proto_result in proto_results.results:
            # Convert bounding boxes
            bboxes = []
            for proto_bbox in proto_result.merged_ui_icon_bboxes:
                from inference import BoundingBox
                bbox = BoundingBox(
                    x=proto_bbox.x,
                    y=proto_bbox.y,
                    width=proto_bbox.width,
                    height=proto_bbox.height,
                    class_name=proto_bbox.class_name,
                    confidence=proto_bbox.confidence,
                    id=proto_bbox.id
                )
                bboxes.append(bbox)
            
            # Convert cropped image if available
            cropped_image = None
            if proto_result.cropped_image:
                cropped_image = Image.open(io.BytesIO(proto_result.cropped_image))
            
            # Create the result model
            result = VisionDetectResultModel(
                event_id=proto_result.event_id,
                project_uuid=proto_result.project_uuid,
                command_uuid=proto_result.command_uuid,
                timestamp=datetime.fromisoformat(proto_result.timestamp),
                description=proto_result.description,
                original_image_path=proto_result.original_image_path,
                original_width=proto_result.original_width,
                original_height=proto_result.original_height,
                is_cropped=proto_result.is_cropped,
                merged_ui_icon_bboxes=bboxes,
                cropped_image=cropped_image,
                cropped_width=proto_result.cropped_width if proto_result.is_cropped else None,
                cropped_height=proto_result.cropped_height if proto_result.is_cropped else None
            )
            
            results.vision_detect_result_models.append(result)
        
        return results
    
    async def broadcast_results(self, results: VisionDetectResultModelList) -> None:
        """Broadcast vision detection results to all connected clients.
        
        Args:
            results: The vision detection results to broadcast.
        """
        logger.info("Broadcasting vision detection results to all connected clients")
        response = VisionDetectRPCResponse()
        response.results.CopyFrom(self._convert_to_proto_results(results))
        await self.broadcast(response)
    
    async def broadcast_status(self) -> None:
        """Broadcast vision detection service status to all connected clients."""
        response = VisionDetectRPCResponse()
        status = VisionDetectStatus()
        status.status = self.service.get_status()
        status.screenshot_events_count = len(self.service._screenshot_events)
        status.has_results = self.service.get_state("has_results") or False
        status.results_count = self.service.get_state("results_count") or 0
        status.is_processing = self.service.get_state("processing") or False
        
        last_processed = self.service.get_state("last_processed")
        if last_processed:
            status.last_processed = last_processed
        
        last_error = self.service.get_state("last_error")
        if last_error:
            status.last_error = last_error
        
        response.status.CopyFrom(status)
        await self.broadcast(response) 