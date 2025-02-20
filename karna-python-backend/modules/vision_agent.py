from base import BaseService, SingletonMeta
import numpy as np
import torch
from typing import Optional, Dict, Tuple
import asyncio
import mss
import cv2
from PIL import Image

class VisionService(BaseService, metaclass=SingletonMeta):
    def __init__(self, model_path: str, config_path: str):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.model_path = model_path
            self.config_path = config_path
            self.screen_capture = mss.mss()
            self.model: Optional[torch.nn.Module] = None
            self._last_frame: Optional[np.ndarray] = None
            self._frame_lock = asyncio.Lock()
            self._initialized = True
        
    async def initialize(self) -> None:
        """Initialize YOLO model with ONNX optimization"""
        try:
            # Load model weights lazily and optimize for inference
            self.model = torch.load(self.model_path)
            if torch.cuda.is_available():
                self.model.cuda()
            self.model.eval()
            self._resources['model'] = self.model
        except Exception as e:
            self.logger.error(f"Failed to initialize vision model: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Clean up resources"""
        self.screen_capture.close()
        self.model = None
        self._last_frame = None
        self._resources.clear()

    async def capture_screen(self, monitor: int = 1) -> np.ndarray:
        """Capture screen content efficiently"""
        async with self._frame_lock:
            screenshot = self.screen_capture.grab(self.screen_capture.monitors[monitor])
            frame = np.array(screenshot)
            self._last_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            return self._last_frame

    async def detect_ui_elements(self, frame: Optional[np.ndarray] = None) -> Dict:
        """Detect UI elements in the given frame or last captured frame"""
        if self.model is None:
            raise RuntimeError("Vision model not initialized")
            
        if frame is None:
            frame = self._last_frame
        if frame is None:
            raise ValueError("No frame available for detection")

        with torch.no_grad():
            # Preprocess frame
            input_tensor = self._preprocess_frame(frame)
            if torch.cuda.is_available():
                input_tensor = input_tensor.cuda()
                
            # Run inference
            detections = self.model(input_tensor)
            return self._postprocess_detections(detections)

    def _preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess frame for model input"""
        image = Image.fromarray(frame)
        # Add preprocessing steps here based on model requirements
        # This is a placeholder implementation
        tensor = torch.from_numpy(np.array(image)).float()
        tensor = tensor.permute(2, 0, 1).unsqueeze(0) / 255.0
        return tensor

    def _postprocess_detections(self, detections: torch.Tensor) -> Dict:
        """Convert model output to usable format"""
        # Add postprocessing steps here based on model output format
        # This is a placeholder implementation
        return {
            "boxes": detections[0] if isinstance(detections, tuple) else detections,
            "timestamp": asyncio.get_event_loop().time()
        }

# Singleton instance getter
_vision_service_instance = None

def get_vision_service_instance(model_path: str = None, config_path: str = None):
    global _vision_service_instance
    if _vision_service_instance is None:
        if model_path is None or config_path is None:
            raise ValueError("model_path and config_path are required for first initialization")
        _vision_service_instance = VisionService(model_path, config_path)
    return _vision_service_instance