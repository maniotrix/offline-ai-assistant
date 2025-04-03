import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import numpy as np
from PIL import Image
import tempfile
import json

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(current_dir)))

from inference.omniparser.dynamic_area_detector import DynamicAreaDetector
from inference.omniparser.image_comparison import ResNetImageEmbedder
from inference.omniparser.image_diff_creator import ImageDiffCreator
from inference.omniparser.omni_helper import (
    OmniParserResultModelList,
    get_omniparser_inference_data, 
    get_omniparser_inference_data_from_json
)
from config.paths import workspace_dir
from services.screen_capture_service import ScreenshotEvent

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Use the same JSON file path as in test_attention_controller.py
DEFAULT_DATA_DIR = workspace_dir / "data" / "chatgpt" / "883c46f5-c62d-4799-baa1-5e3b12f12e8c"
JSON_FILE_PATH = str(DEFAULT_DATA_DIR / "screenshot_events_883c46f5-c62d-4799-baa1-5e3b12f12e8c.json")
OUTPUT_DIR = Path(current_dir) / "detection_output"

def visualize_detection_results(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Visualize the detected main areas on the last frame.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from DynamicAreaDetector
    """
    if not results_list.omniparser_result_models:
        logger.warning("No frames in results list, cannot visualize")
        return
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Visualize the last frame with detected areas
    try:
        # Get the last frame
        last_model = results_list.omniparser_result_models[-1]
        screenshot_path = last_model.omniparser_result.original_image_path
        
        plt.figure(figsize=(15, 10))
        img = plt.imread(screenshot_path)
        plt.imshow(img)
        
        # Get image dimensions from the omniparser result
        img_width = last_model.omniparser_result.original_image_width
        img_height = last_model.omniparser_result.original_image_height
        
        # Draw bounding boxes for elements in the last frame (lighter style)
        for pcr in last_model.parsed_content_results:
            x1, y1, x2, y2 = pcr.bbox
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=1, edgecolor='blue', facecolor='none', alpha=0.3
            )
            plt.gca().add_patch(rect)
        
        # Draw detected main areas with different colors for each rule
        colors = {
            'largest_area': 'red',
            'center_weighted': 'green',
            'highest_frequency': 'purple'
        }
        
        handles = []  # For legend
        
        for rule_name, bbox in main_areas.items():
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = colors.get(rule_name, 'orange')
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=3, edgecolor=color, facecolor=color, alpha=0.3
                )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"Main Area ({rule_name})"))
                
                # Add label text
                plt.text(x1, y1-5, rule_name, color=color, fontsize=12, fontweight='bold')
        
        plt.title("Dynamic Area Detection Results - Final Frame", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"dynamic_area_detection_final.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved final frame visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing final frame results: {e}")
    
    # Create a visualization of all frames with frame difference heatmap
    try:
        # Calculate the number of frames to visualize (up to 9)
        num_frames = len(results_list.omniparser_result_models)
        num_frames_to_show = min(num_frames, 9)
        
        # Calculate grid dimensions
        grid_size = int(np.ceil(np.sqrt(num_frames_to_show)))
        
        plt.figure(figsize=(grid_size * 6, grid_size * 5))
        
        # Define colors for different area types
        colors = {
            'largest_area': 'red',
            'center_weighted': 'green',
            'highest_frequency': 'purple'
        }
        
        # Plot each frame with its dynamic areas
        for i in range(num_frames_to_show):
            frame_idx = i * (num_frames // num_frames_to_show) if num_frames > num_frames_to_show else i
            frame_model = results_list.omniparser_result_models[frame_idx]
            frame_path = frame_model.omniparser_result.original_image_path
            
            # Create subplot
            plt.subplot(grid_size, grid_size, i + 1)
            img = plt.imread(frame_path)
            plt.imshow(img)
            
            # Add frame information
            plt.title(f"Frame {frame_idx}", fontsize=12)
            plt.axis('off')
            
            # Draw main areas if it's the last frame
            if frame_idx == num_frames - 1:
                for rule_name, bbox in main_areas.items():
                    if bbox is not None:
                        x1, y1, x2, y2 = bbox
                        
                        # Convert normalized coordinates to absolute if needed
                        if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                            img_width = frame_model.omniparser_result.original_image_width
                            img_height = frame_model.omniparser_result.original_image_height
                            x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                        
                        color = colors.get(rule_name, 'orange')
                        rect = patches.Rectangle(
                            (x1, y1), x2 - x1, y2 - y1,
                            linewidth=3, edgecolor=color, facecolor=color, alpha=0.3
                        )
                        plt.gca().add_patch(rect)
        
        plt.suptitle("Dynamic Area Detection - Frame Sequence", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"dynamic_area_detection_sequence.png"
        plt.savefig(str(output_file), dpi=200, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved frame sequence visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing frame sequence: {e}")
    
    # Create a detailed visualization showing the dynamic regions
    try:
        # Create a heatmap of dynamic activity using the first and last frame
        if len(results_list.omniparser_result_models) >= 2:
            first_model = results_list.omniparser_result_models[0]
            last_model = results_list.omniparser_result_models[-1]
            
            # Create ImageDiffCreator to visualize differences
            diff_creator = ImageDiffCreator()
            
            # Compare first and last frame
            diff_result = diff_creator.compare_results(first_model, last_model)
            
            # Visualize the differences
            plt.figure(figsize=(15, 10))
            img = plt.imread(last_model.omniparser_result.original_image_path)
            plt.imshow(img)
            
            # Get image dimensions
            img_width = last_model.omniparser_result.original_image_width
            img_height = last_model.omniparser_result.original_image_height
            
            # Define colors for different area types
            colors = {
                'largest_area': 'red',
                'center_weighted': 'green',
                'highest_frequency': 'purple'
            }
            
            # Draw all the changes with different colors based on change type
            change_colors = {
                "added": "lime",
                "removed": "red",
                "text-changed": "orange",
                "visual-changed": "magenta"
            }
            
            handles = []
            for change_type, color in change_colors.items():
                changes = getattr(diff_result, change_type if change_type != "visual-changed" else "visual_changed")
                if changes:
                    for change in changes:
                        x1, y1, x2, y2 = change.bbox
                        
                        # Convert normalized coordinates to absolute if needed
                        if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                            x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                        
                        rect = patches.Rectangle(
                            (x1, y1), x2 - x1, y2 - y1,
                            linewidth=2, edgecolor=color, facecolor=color, alpha=0.3
                        )
                        plt.gca().add_patch(rect)
                    
                    # Add to legend handles
                    handles.append(patches.Patch(color=color, alpha=0.5, label=f"{change_type.replace('-', ' ').title()}"))
            
            # Now overlay the main dynamic areas
            for rule_name, bbox in main_areas.items():
                if bbox is not None:
                    x1, y1, x2, y2 = bbox
                    
                    # Convert normalized coordinates to absolute if needed
                    if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                        x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                    
                    color = colors.get(rule_name, 'orange')
                    rect = patches.Rectangle(
                        (x1, y1), x2 - x1, y2 - y1,
                        linewidth=3, edgecolor=color, facecolor='none', alpha=0.8
                    )
                    plt.gca().add_patch(rect)
                    
                    # Add to legend handles if not already there
                    if rule_name not in [h.get_label().replace("Main Area (", "").replace(")", "") for h in handles if "Main Area" in h.get_label()]:
                        handles.append(patches.Patch(color=color, alpha=0.8, label=f"Main Area ({rule_name})"))
            
            plt.title("Dynamic Changes Detection (First to Last Frame)", fontsize=14)
            if handles:
                plt.legend(handles=handles, fontsize=12)
            
            # Save the visualization
            output_file = OUTPUT_DIR / f"dynamic_area_changes.png"
            plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Saved changes visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing changes: {e}")

def load_screenshot_events(json_path: str, viewport: Dict = None) -> List[ScreenshotEvent]:
    """
    Load screenshot events from the specified JSON file.
    
    Args:
        json_path: Path to the JSON file.
        viewport: Optional dictionary with x, y, width, height keys for cropping screenshots.

    Returns:
        List of ScreenshotEvent objects sorted by timestamp.
    """
    logger.info(f"Loading screenshot events from JSON file: {json_path}")
    
    # Create temporary directory for cropped images if viewport is provided
    temp_dir = None
    if viewport:
        temp_dir = Path(tempfile.mkdtemp(prefix="omni_viewport_"))
        logger.info(f"Created temporary directory for cropped images: {temp_dir}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading JSON file: {str(e)}")
        return []
    
    if not isinstance(events_data, list):
        logger.error("JSON file does not contain a valid list of events")
        return []
    
    screenshot_events = []
    for event_dict in events_data:
        if not isinstance(event_dict, dict):
            logger.warning(f"Skipping non-dictionary item in events list: {event_dict}")
            continue
            
        # Get and process screenshot_path safely
        screenshot_path_str = event_dict.get("screenshot_path")
        if not screenshot_path_str or not isinstance(screenshot_path_str, str):
             logger.warning(f"Skipping event with missing or invalid screenshot_path: {event_dict.get('timestamp')}")
             continue
        event_screenshot_path = workspace_dir / screenshot_path_str
        if viewport:
            # Filter screenshot path by viewport if provided
            try:
                # Check if original screenshot exists
                if not os.path.exists(event_screenshot_path):
                    logger.warning(f"Original screenshot not found: {event_screenshot_path}")
                    continue
                
                # Load the image
                img = Image.open(event_screenshot_path)
                
                # Crop image according to viewport
                cropped_img = img.crop((
                    viewport["x"],
                    viewport["y"],
                    viewport["x"] + viewport["width"],
                    viewport["y"] + viewport["height"]
                ))
                
                # Create filename for cropped image
                original_filename = os.path.basename(event_screenshot_path)
                cropped_filename = f"cropped_{original_filename}"
                # Ensure temp_dir is not None before using / operator
                if temp_dir is not None:
                    cropped_path = temp_dir / cropped_filename
                    
                    # Save the cropped image
                    cropped_img.save(cropped_path)
                    logger.debug(f"Saved cropped image to {cropped_path}")
                    
                    # Update screenshot path in event dictionary
                    event_dict["screenshot_path"] = str(cropped_path)
                    event_screenshot_path = cropped_path
                else:
                    logger.error("Temporary directory is None, cannot save cropped image")
            except Exception as e:
                logger.error(f"Error cropping image {event_screenshot_path}: {e}")
                # Continue with original image if cropping fails
                event_dict["screenshot_path"] = str(event_screenshot_path)
        else:
            event_dict["screenshot_path"] = str(event_screenshot_path)
        
        # Get and process timestamp safely
        timestamp_val = event_dict.get('timestamp')
        processed_timestamp: Optional[datetime] = None
        if isinstance(timestamp_val, str):
            try:
                processed_timestamp = datetime.fromisoformat(timestamp_val)
            except ValueError:
                logger.warning(f"Skipping event with invalid timestamp format: {timestamp_val}")
                continue
        elif isinstance(timestamp_val, datetime):
            processed_timestamp = timestamp_val
        
        if processed_timestamp is None:
            logger.warning(f"Skipping event with missing or invalid timestamp: {timestamp_val}")
            continue
        event_dict['timestamp'] = processed_timestamp # Update dict with datetime object
        
        # Create ScreenshotEvent object, checking for required fields
        try:
            # Ensure mouse coords are present before creating event
            mouse_x = event_dict.get('mouse_x')
            mouse_y = event_dict.get('mouse_y')

            if mouse_x is not None and mouse_y is not None:
                # Check screenshot path existence again after making it absolute
                if os.path.exists(event_dict["screenshot_path"]):
                    # Create event only if essential fields seem valid
                    event = ScreenshotEvent(**event_dict)
                    screenshot_events.append(event)
                else:
                    logger.warning(f"Skipping event - screenshot file not found: {event_dict['screenshot_path']}")
            else:
                logger.debug(f"Skipping event without mouse coordinates: {event_dict['timestamp']}")
                
        except TypeError as e:
            logger.warning(f"Skipping event due to TypeError (likely missing fields or type mismatch): {e} - Event data: {event_dict}")
        except Exception as e:
            logger.warning(f"Skipping invalid event during creation: {str(e)}")
    
    # Sort events by timestamp
    screenshot_events.sort(key=lambda e: e.timestamp)
    
    logger.info(f"Loaded {len(screenshot_events)} valid mouse events with screenshots")
    return screenshot_events

def test_dynamic_area_detector(use_viewport=False):
    """
    Test the DynamicAreaDetector using real data from JSON file.
    
    Args:
        use_viewport: Whether to crop screenshots according to viewport rendering area
    """
    logger.info("Starting DynamicAreaDetector test...")
    
    try:
        # Check if the JSON file exists
        if not os.path.exists(JSON_FILE_PATH):
            logger.error(f"JSON file not found: {JSON_FILE_PATH}")
            return

        # Define viewport if needed
        viewport = None
        if use_viewport:
            viewport = {
                "x": 0,
                "y": 121,
                "width": 1920,
                "height": 919
            }
            logger.info(f"Using viewport for cropping: {viewport}")

        # Load real data from JSON file using omni_helper function
        logger.info(f"Loading data from: {JSON_FILE_PATH}")
        screenshot_events = load_screenshot_events(JSON_FILE_PATH, viewport=viewport)
        test_data = get_omniparser_inference_data(screenshot_events)
        
        if not test_data.omniparser_result_models:
            logger.error("No valid models loaded from JSON file.")
            return
            
        logger.info(f"Successfully loaded {len(test_data.omniparser_result_models)} models from JSON file")
        
        # Initialize the ImageDiffCreator with default parameters
        diff_creator = ImageDiffCreator(
            saliency_threshold=0.1,
            text_similarity_threshold=0.8,
            visual_change_threshold=0.1
        )
        
        # Initialize the detector with the new implementation
        detector = DynamicAreaDetector(
            image_diff_creator=diff_creator,
            min_change_frequency=0.3,
            min_area_size=0.01,
            grouping_distance=0.1,
            min_saliency=0.1
        )
        
        # Run detection
        logger.info("Running dynamic area detection...")
        main_areas = detector.detect_main_areas(test_data)
        
        # Print results
        logger.info("Detection Results:")
        for rule_name, bbox in main_areas.items():
            if bbox is not None:
                logger.info(f"  {rule_name}: {[round(coord, 3) for coord in bbox]}")
            else:
                logger.info(f"  {rule_name}: None")
        
        # Visualize results
        visualize_detection_results(test_data, main_areas)
        
        # Verify results
        success = False
        for bbox in main_areas.values():
            if bbox is not None:
                logger.info("Test PASSED: Successfully detected at least one dynamic area")
                success = True
                break
        
        if not success:
            logger.warning("Test FAILED: No dynamic areas detected")
        
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}", exc_info=True)

if __name__ == "__main__":
    test_dynamic_area_detector()
