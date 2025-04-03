import base64
from datetime import datetime
from dataclasses import dataclass
import io
from typing import List, Union, Tuple
import numpy as np
import pandas as pd
import torch
from util.omniparser import OmniparserResult, Omniparser
from services.screen_capture_service import ScreenshotEvent
import logging
import os
import json
from PIL import Image
import supervision as sv
from util.utils import annotate, box_convert
from util.box_annotator import BoxAnnotator
logger = logging.getLogger(__name__)
import re

@dataclass
class ParsedContentResult:
    """
    Bounding box class.
    type	bbox	interactivity	content	source	ID 
    """
    type: str
    bbox: List[float]
    interactivity: bool
    content: str # WARNING: is inaccurate for source type box_yolo_content_yolo
    source: str
    id: int
    
    def to_dict(self):
        """
        Convert the bounding box to a dictionary.
        Uses 'class' instead of 'class_name' in the output dictionary.
        """
        return {
            "type": self.type,
            "bbox": self.bbox,
            "interactivity": self.interactivity,
            "content": self.content,
            "source": self.source,
            "id": self.id
        }
    
@dataclass
class OmniParserResultModel:
    """
    Result of inference.
    """
    event_id: str
    project_uuid: str
    command_uuid: str
    timestamp: datetime
    description: str
    omniparser_result: OmniparserResult
    parsed_content_results: List[ParsedContentResult]
    
    def to_dict(self):
        """
        Convert the inference result model to a dictionary.
        """
        result = {
            "event_id": self.event_id,
            "project_uuid": self.project_uuid,
            "command_uuid": self.command_uuid,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description,
            "omniparser_result": self.omniparser_result.to_dict(),
            "parsed_content_results": [result.to_dict() for result in self.parsed_content_results]
        }
        return result
        
@dataclass
class OmniParserResultModelList:
    """
    List of omniparser result models.
    """
    project_uuid: str
    command_uuid: str
    omniparser_result_models: List[OmniParserResultModel]
    
class PreProcessor:
    def __init__(self, omniparser_result: OmniparserResult, parsed_content_results: List[ParsedContentResult],):
        self.omniparser_result = omniparser_result
        self.parsed_content_results = parsed_content_results
        
    def pre_process_parsed_content_results(self):
        """
        This method pre-processes the parsed content results.
        """
        for parsed_content_result in self.parsed_content_results:
            parsed_content_result.bbox = self._convert_relative_bbox_to_absolute_bbox(
                parsed_content_result.bbox, 
                self.omniparser_result.original_image_width, 
                self.omniparser_result.original_image_height)
            
    def _convert_relative_bbox_to_absolute_bbox(self, relative_bbox: List[float], image_width: int, image_height: int) -> List[float]:
        """
        This method converts the relative bbox to absolute bbox.
        original_realtive_bbox: [0.7447916865348816, 0.6000000238418579, 0.8177083134651184, 0.6222222447395325]
        convert to absolute bbox
        """
        absolute_bbox = [
            relative_bbox[0] * image_width,
            relative_bbox[1] * image_height,
            relative_bbox[2] * image_width,
            relative_bbox[3] * image_height
        ]
        # round the bbox to the nearest integer
        absolute_bbox = [float(round(coord)) for coord in absolute_bbox]
        # convert to absolute bbox
        return absolute_bbox
    
    
def get_parsed_content_df(omniparser_result: OmniparserResult) -> pd.DataFrame:
    df = pd.DataFrame(omniparser_result.parsed_content_list)
    df['id'] = range(len(df)) # type: ignore
    df = df[['id', 'type', 'bbox', 'interactivity', 'content', 'source']] # type: ignore
    return df

def convert_parsed_content_df_to_bounding_boxes(parsed_content_df: pd.DataFrame) -> List[ParsedContentResult]:
    return parsed_content_df.apply(lambda row: ParsedContentResult(**row), axis=1).tolist() # type: ignore

def get_omniparser_result_model(omniparser_result: OmniparserResult
                                , event_id: str 
                                , project_uuid: str
                                , command_uuid: str
                                , timestamp: datetime
                                , description: str
                                , pre_process: bool = True
                                ) -> OmniParserResultModel:
    logger.info(f"Getting omniparser result model for event_id: {event_id}")
    parsed_content_df = get_parsed_content_df(omniparser_result)
    logger.info(f"Converting parsed content df to bounding boxes for event_id: {event_id}")
    parsed_content_results = convert_parsed_content_df_to_bounding_boxes(parsed_content_df)
    # pre-process the parsed content results and convert relative bbox to absolute bbox
    if pre_process:
        pre_processor = PreProcessor(omniparser_result=omniparser_result, parsed_content_results=parsed_content_results)
        pre_processor.pre_process_parsed_content_results()
        logger.info(f"Pre-processed parsed content results for event_id: {event_id}")
    logger.info(f"Creating omniparser result model for event_id: {event_id}")
    result = OmniParserResultModel(
        event_id=event_id,
        project_uuid=project_uuid,
        command_uuid=command_uuid,
        timestamp=timestamp,
        description=description,
        omniparser_result=omniparser_result,
        parsed_content_results=parsed_content_results
    )
    logger.info(f"Created omniparser result model for event_id: {event_id}")
    return result
    
def get_omniparser_inference_data(screenshot_events: List[ScreenshotEvent], caption_icons: bool = True) -> OmniParserResultModelList:
    omniparser = Omniparser()
    result : List[OmniParserResultModel] = []
    for screenshot_event in screenshot_events:
        logger.info(f"Parsing image path: {screenshot_event.screenshot_path}")
        if caption_icons:
            omniparser_result = omniparser.parse_image_path(screenshot_event.screenshot_path)
        else:
            omniparser_result = omniparser.parse_image_path_without_local_semantics(screenshot_event.screenshot_path)
        logger.info(f"Created omniparser result for event_id: {screenshot_event.event_id}")
        result.append(get_omniparser_result_model(omniparser_result, 
                                                screenshot_event.event_id, 
                                                screenshot_event.project_uuid, 
                                                screenshot_event.command_uuid, 
                                                screenshot_event.timestamp, 
                                                screenshot_event.description))
    logger.info(f"Completed getting omniparser result models for {len(result)} events")
    result_list = OmniParserResultModelList(
        project_uuid=screenshot_events[0].project_uuid,
        command_uuid=screenshot_events[0].command_uuid,
        omniparser_result_models=result
    )
    return result_list

def get_omniparser_inference_data_from_image_path(image_path: str) -> OmniParserResultModel:
    omniparser = Omniparser()
    omniparser_result = omniparser.parse_image_path(image_path)
    return get_omniparser_result_model(omniparser_result, 
                                        event_id="-1", 
                                        project_uuid="-1", 
                                        command_uuid="-1", 
                                        timestamp=datetime.now(), 
                                        description="Omniparser result")

def get_omniparser_inference_data_from_json(json_file_path: str) -> OmniParserResultModelList:
    logger.info(f"Loading screenshot events from JSON file: {json_file_path}")
        
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file: {str(e)}")
    
    if not events_data or not isinstance(events_data, list):
        raise ValueError("JSON file does not contain a list of screenshot events")
    
    # Convert JSON data to ScreenshotEvent objects
    screenshot_events = []
    for event_dict in events_data:
        # Convert ISO format string back to datetime
        if 'timestamp' in event_dict:
            event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp']) # type: ignore
        
        # Create ScreenshotEvent object
        try:
            event = ScreenshotEvent(**event_dict)
            screenshot_events.append(event)
        except (TypeError, ValueError) as e:
            logger.warning(f"Skipping invalid event: {str(e)}")
    
    logger.info(f"Loaded {len(screenshot_events)} screenshot events from JSON file")
    return get_omniparser_inference_data(screenshot_events)

def update_parsed_content_result_list(parsed_content_result_list: List[ParsedContentResult], 
                                    filter_id: int,
                                    update_content: str | None = None, # this is optional
                                    update_interactivity: bool | None = None, # this is optional
                                    update_bbox: List[float] | None = None # this is optional
                                    ) -> List[ParsedContentResult]:
    for result in parsed_content_result_list:
        if result.id == filter_id:
            if update_content is not None:
                result.content = update_content
            if update_interactivity is not None:
                result.interactivity = update_interactivity
            if update_bbox is not None:
                result.bbox = update_bbox
            break
    return parsed_content_result_list

def delete_item_from_parsed_content_result_list(parsed_content_result_list: List[ParsedContentResult], 
                                                filter_id: int) -> List[ParsedContentResult]:
    for result in parsed_content_result_list:
        if result.id == filter_id:
            parsed_content_result_list.remove(result)
            break
    return parsed_content_result_list

def add_item_to_parsed_content_result_list(parsed_content_result_list: List[ParsedContentResult], 
                                            item: ParsedContentResult) -> List[ParsedContentResult]:
    parsed_content_result_list.append(item)
    return parsed_content_result_list

# new functions for above functions to accept OmniParserResultModel
def update_omniparser_result_model(omniparser_result_model: OmniParserResultModel, 
                                    filter_id: int,
                                    update_content: str | None = None, # this is optional
                                    update_interactivity: bool | None = None, # this is optional
                                    update_bbox: List[int] | None = None # this is optional
                                    ) -> OmniParserResultModel:
    omniparser_result_model.parsed_content_results = update_parsed_content_result_list(omniparser_result_model.parsed_content_results, 
                                                                                        filter_id, 
                                                                                        update_content, 
                                                                                        update_interactivity, 
                                                                                        update_bbox)
    return omniparser_result_model  

def delete_item_from_omniparser_result_model(omniparser_result_model: OmniParserResultModel, 
                                            filter_id: int) -> OmniParserResultModel:
    omniparser_result_model.parsed_content_results = delete_item_from_parsed_content_result_list(omniparser_result_model.parsed_content_results, 
                                                                                                    filter_id)
    return omniparser_result_model

def add_item_to_omniparser_result_model(omniparser_result_model: OmniParserResultModel, 
                                        item: ParsedContentResult) -> OmniParserResultModel:
    omniparser_result_model.parsed_content_results = add_item_to_parsed_content_result_list(omniparser_result_model.parsed_content_results, 
                                                                                                item)
    return omniparser_result_model

def append_omniparser_result_model(omniparser_result_model: OmniParserResultModel, 
                                    content: str,
                                    bbox: List[int],
                                    interactivity: bool,
                                    source: str,
                                    type: str
                                    ) -> OmniParserResultModel:
    # find the max id
    max_id = max([result.id for result in omniparser_result_model.parsed_content_results])
    item = ParsedContentResult(id=max_id + 1, content=content, bbox=bbox, interactivity=interactivity, source=source, type=type)
    omniparser_result_model.parsed_content_results = add_item_to_parsed_content_result_list(omniparser_result_model.parsed_content_results, 
                                                                                                item)
    return omniparser_result_model

def annotate_omniparser_result_model(omniparser_result_model: OmniParserResultModel):
    """Process either an image path or Image object
    
    Args:
        image_source: Either a file path (str) or PIL Image object
        ...
    """
    # get the parsed content results
    filtered_boxes_elem = omniparser_result_model.parsed_content_results
    
    #    get the image
    image_path = omniparser_result_model.omniparser_result.original_image_path
    image_source = Image.open(image_path)
    image_source = image_source.convert("RGB") # for CLIP
    image_source = np.asarray(image_source)
    h, w, _ = image_source.shape # type: ignore
    
    print("image size: ", w, h)
    
    filtered_boxes = torch.tensor([box.bbox for box in filtered_boxes_elem])
    filtered_boxes = box_convert(boxes=filtered_boxes, in_fmt="xyxy", out_fmt="cxcywh")

    phrases = [i for i in range(len(filtered_boxes))]
    
    box_overlay_ratio = max(w, h) / 3200
    draw_bbox_config = {
        'text_scale': 0.8 * box_overlay_ratio,
        'text_thickness': max(int(2 * box_overlay_ratio), 1),
        'text_padding': max(int(3 * box_overlay_ratio), 1),
        'thickness': max(int(3 * box_overlay_ratio), 1),
    }
    
    annotated_frame, label_coordinates = annotate(image_source=image_source, 
                                                boxes=filtered_boxes, 
                                                logits=None, 
                                                phrases=phrases, 
                                                **draw_bbox_config)
    
    pil_img = Image.fromarray(annotated_frame)
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('ascii')
    
    return encoded_image


def extract_bbox_patch(parsed_content_result_with_raw_coords: ParsedContentResult, omniparser_result_model: OmniParserResultModel) -> Tuple[str, Image.Image]:
    # check if the parsed content result id is in the omniparser result model
    if parsed_content_result_with_raw_coords.id not in [result.id for result in omniparser_result_model.parsed_content_results]:
        raise ValueError(f"Parsed content result id {parsed_content_result_with_raw_coords.id} not found in omniparser result model")
    
    image_path = omniparser_result_model.omniparser_result.original_image_path
    image_source = Image.open(image_path)
    image_source = image_source.convert("RGB") # for CLIP
    image_source = np.asarray(image_source)
    h, w, _ = image_source.shape # type: ignore
    
    # get the bbox from the parsed content result and convert to integers
    # format xyxy
    bbox_xyxy = [int(coord) for coord in parsed_content_result_with_raw_coords.bbox]
    x1, y1, x2, y2 = bbox_xyxy
    
    # Ensure coordinates are within image bounds
    x1 = max(0, min(x1, w))
    y1 = max(0, min(y1, h))
    x2 = max(0, min(x2, w))
    y2 = max(0, min(y2, h))
    
    # Ensure valid patch dimensions
    if x2 <= x1 or y2 <= y1:
        raise ValueError("Invalid bounding box dimensions")
    
    # Extract the patch using numpy slicing
    bbox_patch = image_source[y1:y2, x1:x2].copy()
    
    # Convert back to PIL Image
    bbox_patch_pil = Image.fromarray(bbox_patch)
    
    # Convert to base64
    buffered = io.BytesIO()
    bbox_patch_pil.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('ascii')
    
    return encoded_image, bbox_patch_pil

def save_pil_image_to_file(parsed_content_result: ParsedContentResult, pil_image: Image.Image, output_dir: str):
    # this takes in a PIL image and parse content result 
    # the file_name is the id+content of the parse content result in provided directory
    try:
        description = parsed_content_result.content
        # remove all special characters
        description = re.sub(r'[^a-zA-Z0-9\s]', '', description)
        file_path = os.path.join(output_dir, f"{parsed_content_result.id}_{description}.png")
        pil_image.save(file_path)
    except Exception as e:
        logger.error(f"Error saving PIL image to file: {e}")
        raise e
    
def export_and_save_pil_image_to_file(parsed_content_results: List[ParsedContentResult], 
                                    omniparser_result_model: OmniParserResultModel, output_dir: str):
    for parsed_content_result in parsed_content_results:
        # extract the bbox patch
        encoded_image, bbox_patch_pil = extract_bbox_patch(parsed_content_result, omniparser_result_model)
        # save the bbox patch to a file
        save_pil_image_to_file(parsed_content_result, bbox_patch_pil, output_dir)
    
    
    
    
    
    # this takes in a parse content result and omniparser result model
    # and saves the image to a file
    # the file_name is the id+content of the parse content result in provided directory
    # the file_name is the id+content of the parse content result in provided directory
    # the file_name is the id+content of the parse content result in provided directory
    
    
    
    
    
    
    
    
    
    
    
    
    
    






