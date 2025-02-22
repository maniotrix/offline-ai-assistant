from base import BaseService, SingletonMeta
import numpy as np
import torch
import torch.nn.functional as F
from typing import Optional, Dict, Tuple, List
import asyncio
import mss
import cv2
from PIL import Image
import yaml
import torchvision

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
            self._load_config()
            self._initialized = True
    
    def _load_config(self) -> None:
        """Load YOLO configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.input_size = self.config.get('input_size', (640, 640))
            self.confidence_threshold = self.config.get('confidence_threshold', 0.5)
            self.iou_threshold = self.config.get('iou_threshold', 0.45)
            self.classes = self.config.get('classes', {})
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            raise
        
    async def initialize(self) -> None:
        """Initialize YOLO model with ONNX optimization"""
        try:
            # Load model weights and optimize for inference
            self.model = torch.load(self.model_path)
            if torch.cuda.is_available():
                self.model.cuda()
            self.model.eval()
            
            # Warmup run
            dummy_input = torch.zeros((1, 3, *self.input_size))
            if torch.cuda.is_available():
                dummy_input = dummy_input.cuda()
            with torch.no_grad():
                self.model(dummy_input)
                
            self._resources['model'] = self.model
            self.logger.info("Vision model initialized successfully")
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

        try:
            with torch.no_grad():
                # Preprocess frame
                input_tensor = self._preprocess_frame(frame)
                if torch.cuda.is_available():
                    input_tensor = input_tensor.cuda()
                    
                # Run inference
                detections = self.model(input_tensor)
                processed_detections = self._postprocess_detections(detections)
                
                return {
                    "ui_elements": processed_detections,
                    "frame_shape": frame.shape[:2],  # height, width
                    "timestamp": asyncio.get_event_loop().time()
                }
        except Exception as e:
            self.logger.error(f"Detection error: {str(e)}")
            raise

    def _preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess frame for model input"""
        # Convert to PIL for consistent resizing
        image = Image.fromarray(frame)
        
        # Resize maintaining aspect ratio with padding
        target_size = self.input_size
        ratio = min(target_size[0] / image.size[0], target_size[1] / image.size[1])
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.BILINEAR)
        
        # Create padded image
        padded = Image.new("RGB", target_size, (114, 114, 114))
        padded.paste(image, ((target_size[0] - new_size[0]) // 2,
                            (target_size[1] - new_size[1]) // 2))
        
        # Convert to tensor and normalize
        tensor = torch.from_numpy(np.array(padded)).float()
        tensor = tensor.permute(2, 0, 1).unsqueeze(0)
        tensor = tensor / 255.0
        
        return tensor

    def _postprocess_detections(self, detections: torch.Tensor) -> List[Dict]:
        """Convert model output to usable format with NMS"""
        if isinstance(detections, (tuple, list)):
            detections = detections[0]
            
        # Apply sigmoid to predictions
        pred = detections.sigmoid()
        
        # Get boxes, scores, and class predictions
        boxes = pred[..., :4]
        scores = pred[..., 4:]
        
        # Convert boxes from centered to corner format
        boxes = self._center_to_corner(boxes)
        
        # Non-maximum suppression
        nms_indices = torchvision.ops.batched_nms(
            boxes.view(-1, 4),
            scores.max(dim=1)[0].view(-1),
            scores.max(dim=1)[1].view(-1),
            self.iou_threshold
        )
        
        results = []
        for idx in nms_indices:
            if scores[idx].max() > self.confidence_threshold:
                class_id = scores[idx].argmax().item()
                box = boxes[idx].tolist()
                score = scores[idx].max().item()
                
                results.append({
                    "bbox": box,
                    "class": self.classes.get(class_id, "unknown"),
                    "confidence": score
                })
        
        return results

    def _center_to_corner(self, boxes: torch.Tensor) -> torch.Tensor:
        """Convert boxes from center format (cx, cy, w, h) to corner format (x1, y1, x2, y2)"""
        cx, cy = boxes[..., 0], boxes[..., 1]
        w, h = boxes[..., 2], boxes[..., 3]
        
        x1 = cx - w/2
        y1 = cy - h/2
        x2 = cx + w/2
        y2 = cy + h/2
        
        return torch.stack([x1, y1, x2, y2], dim=-1)

    def get_status(self) -> str:
        """Get service status"""
        if not self._initialized:
            return "not_initialized"
        if self.model is None:
            return "model_not_loaded"
        return "running"

# Singleton instance getter
_vision_service_instance = None

def get_vision_service_instance(model_path: str = None, config_path: str = None):
    global _vision_service_instance
    if _vision_service_instance is None:
        if model_path is None or config_path is None:
            raise ValueError("model_path and config_path are required for first initialization")
        _vision_service_instance = VisionService(model_path, config_path)
    return _vision_service_instance