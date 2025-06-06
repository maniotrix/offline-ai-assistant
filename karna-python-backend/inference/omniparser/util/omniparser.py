from dataclasses import dataclass
from typing import Any
from inference.omniparser.util.utils import get_som_labeled_img, get_caption_model_processor, get_yolo_model, check_ocr_box
import torch
from PIL import Image
import io
import base64
import os
import logging
logger = logging.getLogger(__name__)

weights_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'weights')
# Config for the Omniparser
_config = {
    'som_model_path': os.path.join(weights_dir, 'icon_detect/model.pt'),
    'caption_model_name': 'florence2',
    'caption_model_path': os.path.join(weights_dir, 'icon_caption_florence'),
    'device': 'cpu',
    'BOX_TRESHOLD': 0.05,
}
import base64

def is_image_path(text : str) -> bool:
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif")
    # AttributeError: 'WindowsPath' object has no attribute 'endswith'
    try:
        if isinstance(text, str) and text.endswith(image_extensions):
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error checking if {text} is an image path: {e}")
        return False

def encode_image(image_path : str) -> str:
    """Encode image file to base64."""
    try:
        if not is_image_path(image_path):
            # even if the image path is not a valid image path, we will try to encode it
            # this is to avoid the error when the image path is not a valid image path
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except Exception as e:
                logger.error(f"Error encoding image path: {image_path}: {e}")
                raise ValueError(f"Invalid image path: {image_path}")
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error encoding image path: {image_path}: {e}")
        raise ValueError(f"Invalid image path: {image_path}")
    
@dataclass
class OmniparserResult(object):
    dino_labled_img: Any
    label_coordinates: Any
    parsed_content_list: Any
    original_image_path: str
    original_image_width: int
    original_image_height: int
    phrases: list[str]
    
    def to_dict(self):
        return {
            'dino_labled_img': self.dino_labled_img,
            'label_coordinates': self.label_coordinates,
            'parsed_content_list': self.parsed_content_list,
            'original_image_path': self.original_image_path,
            'original_image_width': self.original_image_width,
            'original_image_height': self.original_image_height,
            'phrases': self.phrases
        }

# TODO: Disable image captioning as soon as possible
class Omniparser(object):
    def __init__(self):
        self.config = _config
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.som_model = get_yolo_model(model_path=self.config['som_model_path'])
        self.caption_model_processor = get_caption_model_processor(model_name=self.config['caption_model_name'], model_name_or_path=self.config['caption_model_path'], device=device)
        print('Omniparser initialized!!!')

    def parse(self, image_base64: str):
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        print('image size:', image.size)
        
        box_overlay_ratio = max(image.size) / 3200
        draw_bbox_config = {
            'text_scale': 0.8 * box_overlay_ratio,
            'text_thickness': max(int(2 * box_overlay_ratio), 1),
            'text_padding': max(int(3 * box_overlay_ratio), 1),
            'thickness': max(int(3 * box_overlay_ratio), 1),
        }

        (text, ocr_bbox), _ = check_ocr_box(image, display_img=False, output_bb_format='xyxy', easyocr_args={'text_threshold': 0.8}, use_paddleocr=False)
        dino_labled_img, label_coordinates, parsed_content_list, phrases = get_som_labeled_img(image, self.som_model, BOX_TRESHOLD = self.config['BOX_TRESHOLD'], 
                                                                                      output_coord_in_ratio=True, ocr_bbox=ocr_bbox,draw_bbox_config=draw_bbox_config, 
                                                                                      caption_model_processor=self.caption_model_processor, ocr_text=text,use_local_semantics=True, 
                                                                                      iou_threshold=0.7, scale_img=False, batch_size=128)

        return dino_labled_img, label_coordinates, parsed_content_list, phrases
    
    def parse_without_local_semantics(self, image_base64: str):
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        print('image size:', image.size)
        
        box_overlay_ratio = max(image.size) / 3200
        draw_bbox_config = {
            'text_scale': 0.8 * box_overlay_ratio,
            'text_thickness': max(int(2 * box_overlay_ratio), 1),
            'text_padding': max(int(3 * box_overlay_ratio), 1),
            'thickness': max(int(3 * box_overlay_ratio), 1),
        }

        (text, ocr_bbox), _ = check_ocr_box(image, display_img=False, output_bb_format='xyxy', easyocr_args={'text_threshold': 0.8}, use_paddleocr=False)
        dino_labled_img, label_coordinates, parsed_content_list, phrases = get_som_labeled_img(image, self.som_model, BOX_TRESHOLD = self.config['BOX_TRESHOLD'], 
                                                                                      output_coord_in_ratio=True, ocr_bbox=ocr_bbox,draw_bbox_config=draw_bbox_config, 
                                                                                      caption_model_processor=self.caption_model_processor, ocr_text=text,use_local_semantics=False, 
                                                                                      iou_threshold=0.7, scale_img=False, batch_size=128)

        return dino_labled_img, label_coordinates, parsed_content_list, phrases
    
    def parse_image_path(self, image_path: str) -> OmniparserResult:
        image_base64 = encode_image(image_path)
        image = Image.open(image_path)
        dino_labled_img, label_coordinates, parsed_content_list, phrases = self.parse(image_base64)
        return OmniparserResult(dino_labled_img, label_coordinates, parsed_content_list, image_path, image.size[0], image.size[1], phrases)
    
    def parse_image_path_without_local_semantics(self, image_path: str) -> OmniparserResult:
        image_base64 = encode_image(image_path)
        image = Image.open(image_path)
        dino_labled_img, label_coordinates, parsed_content_list, phrases = self.parse_without_local_semantics(image_base64)
        return OmniparserResult(dino_labled_img, label_coordinates, parsed_content_list, image_path, image.size[0], image.size[1], phrases)
    
    # def parse_batch_image_path(self, image_paths: list[str]) -> list[OmniparserResult]:
    #     return [self.parse_image_path(image_path) for image_path in image_paths]

