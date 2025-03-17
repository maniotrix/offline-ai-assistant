from datetime import datetime
from dataclasses import dataclass, field
import uuid
from typing import List
import pandas as pd
from util.omniparser import OmniparserResult, Omniparser
from services.screen_capture_service import ScreenshotEvent
import logging
import os
import json
logger = logging.getLogger(__name__)

@dataclass
class ParsedContentResult:
    """
    Bounding box class.
    type	bbox	interactivity	content	source	ID 
    """
    type: str
    bbox: List[int]
    interactivity: str
    content: str
    source: str
    id: str
    
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
                                ) -> OmniParserResultModel:
    logger.info(f"Getting omniparser result model for event_id: {event_id}")
    parsed_content_df = get_parsed_content_df(omniparser_result)
    logger.info(f"Converting parsed content df to bounding boxes for event_id: {event_id}")
    parsed_content_results = convert_parsed_content_df_to_bounding_boxes(parsed_content_df)
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
    
def get_omniparser_inference_data(screenshot_events: List[ScreenshotEvent]) -> List[OmniParserResultModel]:
    omniparser = Omniparser()
    result : List[OmniParserResultModel] = []
    for screenshot_event in screenshot_events:
        logger.info(f"Parsing image path: {screenshot_event.screenshot_path}")
        omniparser_result = omniparser.parse_image_path(screenshot_event.screenshot_path)
        logger.info(f"Created omniparser result for event_id: {screenshot_event.event_id}")
        result.append(get_omniparser_result_model(omniparser_result, 
                                                screenshot_event.event_id, 
                                                screenshot_event.project_uuid, 
                                                screenshot_event.command_uuid, 
                                                screenshot_event.timestamp, 
                                                screenshot_event.description))
    logger.info(f"Completed getting omniparser result models for {len(result)} events")
    return result

def get_omniparser_inference_data_from_json(json_file_path: str) -> List[OmniParserResultModel]:
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


