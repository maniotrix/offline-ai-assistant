import base64
import logging
import os
import io
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from PIL import Image

from utils.image_utils import crop_to_render_area

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64 for use with multimodal models.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {e}")
        raise

def process_image(image: Union[str, bytes], 
                should_crop_to_website_render_area: bool = False
                ) -> str:
    """Process image to base64 format.
    
    Args:
        image (Union[str, bytes]): Image path or raw bytes
        should_crop_to_website_render_area (bool): Whether to crop the image to the website render area
    Returns:
        str: Base64 encoded image
    """
    if isinstance(image, str):
        # Path to image file
        if Path(image).exists():
            if should_crop_to_website_render_area:
                # Crop image to website render area
                try:
                    cropped_img = crop_to_render_area(image, should_crop=True)
                    # Convert PIL Image to base64 in memory
                    buffer = io.BytesIO()
                    cropped_img.save(buffer, format=cropped_img.format or 'PNG')
                    buffer.seek(0)
                    return base64.b64encode(buffer.read()).decode("utf-8")
                except Exception as e:
                    logger.error(f"Error cropping image {image}: {e}")
                    # Fall back to original approach if cropping fails
                    with open(image, "rb") as f:
                        return base64.b64encode(f.read()).decode("utf-8")
            else:
                # Original approach without cropping
                with open(image, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
        # Already base64 encoded
        else:
            return image
    elif isinstance(image, bytes):
        # Raw image bytes
        return base64.b64encode(image).decode("utf-8")
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")

def process_images(images: List[Union[str, bytes]], should_crop_to_website_render_area: bool = False) -> List[str]:
    """Process multiple images to base64 format.
    
    Args:
        images (List[Union[str, bytes]]): List of image paths or raw bytes
        should_crop_to_website_render_area (bool): Whether to crop the images to the website render area
        
    Returns:
        List[str]: List of base64 encoded images
    """
    return [process_image(img, should_crop_to_website_render_area) for img in images]

def get_default_llm_options() -> Dict[str, Any]:
    """Get default options optimized for LLMs.
    
    Returns:
        dict: Default LLM options
    """
    return {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "num_predict": 256,
        "num_ctx": 4096
    }
    
def get_default_vlm_options() -> Dict[str, Any]:
    """Get default options optimized for VLMs.
    
    Returns:
        dict: Default VLM options
    """
    return {
        "temperature": 0.7,
        "top_p": 0.9,
        "num_predict": 512,
        "num_ctx": 8192  # VLMs often need larger context
    }
    
def get_default_embedding_options() -> Dict[str, Any]:
    """Get default options optimized for embedding models.
    
    Returns:
        dict: Default embedding options
    """
    return {
        "num_ctx": 4096
    }

def get_ollama_host() -> Optional[str]:
    """Get the Ollama host from environment variable.
    
    Returns:
        Optional[str]: Ollama host URL or None if not set
    """
    return os.environ.get("OLLAMA_HOST")

def handle_api_error(e: Exception, operation: str) -> None:
    """Log API errors consistently.
    
    Args:
        e (Exception): The exception that occurred
        operation (str): Description of the operation being performed
    """
    logger.error(f"Error during {operation}: {str(e)}")
    logger.debug(f"Error details: {e}", exc_info=True) 