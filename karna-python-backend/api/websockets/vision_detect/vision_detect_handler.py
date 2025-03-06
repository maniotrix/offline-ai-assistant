from fastapi import WebSocket
from typing import List, Optional
import logging
from datetime import datetime

from api.websockets.base_handler import BaseWebSocketHandler
from services.vision_detect_service import VisionDetectService, get_vision_detect_service_instance
from inference import VisionDetectResultModelList, VisionDetectResultModel

# Import the generated protobuf classes
# Note: These will be generated after running the protoc compiler on vision_detect.proto
from generated.vision_detect_pb2 import (
    VisionDetectRPCRequest,
    VisionDetectRPCResponse,
    ProcessRequest,
    GetResultsRequest,
    ExportRequest,
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
    
    async def _default_observer_callable(self, data: Optional[VisionDetectResultModelList]) -> None:
        """Default implementation for handling vision detection result updates.
        
        Args:
            data: The updated vision detection results.
        """
        logger.info("Observer received vision detection results update")
        if data is None:
            # Results were cleared, send status update
            await self.broadcast_status()
        else:
            # Results were updated, broadcast them
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
            if method == "process_request":
                await self._handle_process_request(websocket, request.process_request)
            elif method == "get_results_request":
                await self._handle_get_results_request(websocket, request.get_results_request)
            elif method == "export_request":
                await self._handle_export_request(websocket, request.export_request)
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
    
    async def _handle_process_request(self, websocket: WebSocket, process_request: ProcessRequest) -> None:
        """Handle a request to process screenshot events.
        
        Args:
            websocket: The WebSocket connection.
            process_request: The process request.
        """
        try:
            # Process the screenshot events
            results = self.service.process_screenshot_events(should_crop=process_request.should_crop)
            
            # Send the response
            response = VisionDetectRPCResponse()
            response.results.CopyFrom(self._convert_to_proto_results(results))
            await websocket.send_bytes(response.SerializeToString())
        
        except Exception as e:
            logger.error(f"Error processing screenshot events: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error processing screenshot events: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    async def _handle_get_results_request(self, websocket: WebSocket, get_results_request: GetResultsRequest) -> None:
        """Handle a request to get vision detection results.
        
        Args:
            websocket: The WebSocket connection.
            get_results_request: The get results request.
        """
        try:
            # Get the vision detection results
            results = self.service.get_vision_detect_results()
            
            # Send the response
            response = VisionDetectRPCResponse()
            if results:
                response.results.CopyFrom(self._convert_to_proto_results(results))
            else:
                # If no results, send status instead
                status = VisionDetectStatus()
                status.status = self.service.get_status()
                status.screenshot_events_count = len(self.service._screenshot_events)
                status.has_results = False
                status.results_count = 0
                status.is_processing = self.service.get_state("processing") or False
                response.status.CopyFrom(status)
            
            await websocket.send_bytes(response.SerializeToString())
        
        except Exception as e:
            logger.error(f"Error getting vision detection results: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error getting vision detection results: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    async def _handle_export_request(self, websocket: WebSocket, export_request: ExportRequest) -> None:
        """Handle a request to export vision detection results to JSON.
        
        Args:
            websocket: The WebSocket connection.
            export_request: The export request.
        """
        try:
            # Export the vision detection results
            export_path = self.service.export_vision_detect_results_to_json(output_dir=export_request.output_dir)
            
            # Send the response
            response = VisionDetectRPCResponse()
            if export_path:
                response.export_path = export_path
            else:
                response.error = "No vision detection results available to export"
            
            await websocket.send_bytes(response.SerializeToString())
        
        except Exception as e:
            logger.error(f"Error exporting vision detection results: {e}", exc_info=True)
            response = VisionDetectRPCResponse()
            response.error = f"Error exporting vision detection results: {str(e)}"
            await websocket.send_bytes(response.SerializeToString())
    
    async def _handle_update_results_request(self, websocket: WebSocket, update_request: UpdateResultsRequest) -> None:
        """Handle a request to update vision detection results.
        
        Args:
            websocket: The WebSocket connection.
            update_request: The update results request.
        """
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