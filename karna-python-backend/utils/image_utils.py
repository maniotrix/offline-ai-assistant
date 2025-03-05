import os
import logging
from typing import Tuple, Optional, Union
from PIL import Image

from robot.bbox_factory import BBoxFactory, BoundingBoxType

logger = logging.getLogger("image_utils")

def crop_to_render_area(
    image_source: Union[str, Image.Image], 
    render_area: Optional[Tuple[int, int, int, int]] = None,
    should_crop: bool = True
) -> Image.Image:
    """
    Crop an image to the robot.bbox factory website render area.
    
    Parameters:
        image_source (Union[str, Image.Image]): Path to the image or PIL Image object.
        render_area (Optional[Tuple[int, int, int, int]]): The render area coordinates (left, top, right, bottom).
            If None, the render area from BBoxFactory will be used.
        should_crop (bool): Whether to crop the image or not. Default is True.
        
    Returns:
        Image.Image: Cropped PIL Image object or the original image if should_crop is False.
        
    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image cannot be opened.
    """
    # If should_crop is False, just return the original image
    if not should_crop:
        if isinstance(image_source, str):
            if not os.path.exists(image_source):
                raise FileNotFoundError(f"Image file not found: {image_source}")
            try:
                return Image.open(image_source)
            except Exception as e:
                raise ValueError(f"Failed to open image: {str(e)}")
        else:
            return image_source
    
    # Load the image if a path is provided
    if isinstance(image_source, str):
        if not os.path.exists(image_source):
            raise FileNotFoundError(f"Image file not found: {image_source}")
        try:
            image = Image.open(image_source)
        except Exception as e:
            raise ValueError(f"Failed to open image: {str(e)}")
    else:
        image = image_source
    
    # If render_area is not provided, get it from BBoxFactory
    if render_area is None:
        try:
            bbox_factory = BBoxFactory()
            website_render_bbox = bbox_factory.get_website_render_bbox()
            render_area = (
                website_render_bbox.x,
                website_render_bbox.y,
                website_render_bbox.x + website_render_bbox.width,
                website_render_bbox.y + website_render_bbox.height
            )
            logger.info(f"Using website render area from BBoxFactory: {render_area}")
        except Exception as e:
            # Fallback to default values if BBoxFactory fails
            logger.warning(f"Failed to get render area from BBoxFactory: {str(e)}. Using default values.")
            render_area = (0, 121, 1920, 1040)  # Default values from chrome_system_bounding_boxes.json
    
    # Ensure the render area is within the image bounds
    img_width, img_height = image.size
    left, top, right, bottom = render_area
    
    # Adjust the render area if it exceeds the image dimensions
    left = max(0, left)
    top = max(0, top)
    right = min(img_width, right)
    bottom = min(img_height, bottom)
    
    # Crop the image to the render area
    logger.info(f"Cropping image to render area: {(left, top, right, bottom)}")
    cropped_image = image.crop((left, top, right, bottom))
    
    return cropped_image

def save_cropped_image(
    image_source: Union[str, Image.Image],
    output_path: str,
    render_area: Optional[Tuple[int, int, int, int]] = None,
    should_crop: bool = True
) -> str:
    """
    Crop an image to the robot.bbox factory website render area and save it.
    
    Parameters:
        image_source (Union[str, Image.Image]): Path to the image or PIL Image object.
        output_path (str): Path to save the cropped image.
        render_area (Optional[Tuple[int, int, int, int]]): The render area coordinates (left, top, right, bottom).
            If None, the render area from BBoxFactory will be used.
        should_crop (bool): Whether to crop the image or not. Default is True.
        
    Returns:
        str: Path to the saved cropped image.
        
    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image cannot be opened.
    """
    # Crop the image
    cropped_image = crop_to_render_area(image_source, render_area, should_crop)
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the cropped image
    cropped_image.save(output_path)
    logger.info(f"Saved cropped image to: {output_path}")
    
    return output_path 