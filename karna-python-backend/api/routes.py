from fastapi import APIRouter, WebSocket, Request, HTTPException, status
import logging
from api.websockets.websocket_manager import get_websocket_manager_instance
from api.constants import REST, WS
from robot.utils import generate_system_bounding_boxes # type: ignore
import traceback
from typing import Dict, Any
# from modules.vision_agent import get_vision_service_instance

router = APIRouter()
websocket_manager = get_websocket_manager_instance()
logger = logging.getLogger(__name__)

# ===== Routes =====

# post route to generate the system bboxes json file
@router.post(
    REST.GENERATE_SYSTEM_BOUNDING_BOXES, 
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, Any]
)
async def generate_system_bounding_boxes_route(request: Request):
    """
    Generate the system bounding boxes JSON file from post request data.
    
    This endpoint accepts a JSON payload containing bounding box data and 
    processes it to generate system bounding boxes.
    
    Returns:
        Dict: A JSON response with status and details of the operation
        
    Raises:
        HTTPException: If the request is invalid or processing fails
    """
    try:
        # Log the incoming request
        logger.info(f"Received request to generate system bounding boxes")
        
        # Parse and validate the request data
        try:
            data = await request.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON data in request"
            )
        
        # Validate required fields in the data
        if not isinstance(data, dict):
            logger.error(f"Invalid data format: expected dictionary, got {type(data)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data format: expected JSON object"
            )
        
        # Process the data
        try:
            generate_system_bounding_boxes(data)
            logger.info("Successfully generated system bounding boxes")
        except Exception as e:
            logger.error(f"Error generating system bounding boxes: {str(e)}")
            logger.debug(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate system bounding boxes: {str(e)}"
            )
        
        # Return success response
        return {
            "status": "success", 
            "message": "System bounding boxes generated successfully",
            "data": {"processed": True}
        }
    
    except HTTPException:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in generate_system_bounding_boxes_route: {str(e)}")
        logger.debug(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get(REST.HEALTH)
async def health_check():
    return {"status": "healthy"}

@router.on_event("startup")
async def startup_event():
    # Initialize services and logging
    logging.basicConfig(level=logging.INFO)

@router.on_event("shutdown")
async def shutdown_event():
    pass

@router.websocket(WS.COMMAND)
async def websocket_command_endpoint(websocket: WebSocket):
    """WebSocket endpoint for command channel"""
    await websocket_manager.handle_command_connection(websocket)

@router.websocket(WS.STATUS)
async def websocket_status_endpoint(websocket: WebSocket):
    """WebSocket endpoint for status channel"""
    await websocket_manager.handle_status_connection(websocket)
    
@router.websocket(WS.SCREEN_CAPTURE)
async def websocket_screen_capture_endpoint(websocket: WebSocket):
    """WebSocket endpoint for screen capture channel"""
    await websocket_manager.handle_screen_capture_connection(websocket)

# @router.get(REST.ACTIVE_CLIENTS)
# async def get_active_clients():
#     """Get count of active WebSocket clients per channel"""
#     return websocket_manager.report_active_clients()

@router.get(REST.SCREENSHOT)
async def get_screenshot():
    # vision_service = get_vision_service_instance()
    # screenshot = await vision_service.capture_screen()
    # return {"screenshot": screenshot}
    pass