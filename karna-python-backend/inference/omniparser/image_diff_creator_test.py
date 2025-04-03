import os
import sys
import time
import logging
import argparse
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
from pathlib import Path

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(current_dir)))

from image_diff_creator import ImageDiffCreator, DiffResult, ImageDiffResults
from omni_helper import get_omniparser_inference_data_from_image_path, OmniParserResultModel
from omni_helper import get_omniparser_inference_data
from services.screen_capture_service import ScreenshotEvent
from config.paths import workspace_dir

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('image_diff_creator_test.log')
    ]
)
logger = logging.getLogger('image_diff_creator_test')

# Default data path for testing
DEFAULT_DATA_DIR = workspace_dir / "data" / "chatgpt" / "883c46f5-c62d-4799-baa1-5e3b12f12e8c"
JSON_FILE_PATH = str(DEFAULT_DATA_DIR / "screenshot_events_883c46f5-c62d-4799-baa1-5e3b12f12e8c.json")
OUTPUT_DIR = Path(current_dir) / "diff_output"

# Color mappings for visualization
CHANGE_COLORS = {
    'added': (0, 255, 0),     # Green
    'removed': (255, 0, 0),   # Red
    'text-changed': (0, 0, 255),  # Blue
    'visual-changed': (255, 255, 0)  # Yellow
}

def load_screenshot_events(json_path: str) -> List[ScreenshotEvent]:
    """
    Load screenshot events from the specified JSON file.
    
    Args:
        json_path: Path to the JSON file.

    Returns:
        List of ScreenshotEvent objects sorted by timestamp.
    """
    logger.info(f"Loading screenshot events from JSON file: {json_path}")
    
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
        abs_path = workspace_dir / screenshot_path_str
        event_dict["screenshot_path"] = str(abs_path)
        
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

def draw_diff_results(
    img1: np.ndarray, 
    img2: np.ndarray, 
    diff_results: ImageDiffResults,
    output_dir: str = './diff_output'
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Draw bounding boxes on the images based on diff results.
    
    Args:
        img1: Original image as numpy array
        img2: New image as numpy array
        diff_results: Results from the ImageDiffCreator
        output_dir: Directory to save visualization images
        
    Returns:
        Tuple of annotated images (img1, img2)
    """
    # Make copies of images for drawing
    img1_annotated = img1.copy()
    img2_annotated = img2.copy()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Function to draw a box with label
    def draw_box(img, bbox, label, color, thickness=2):
        x1, y1, x2, y2 = [int(c) for c in bbox]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        
        # Prepare text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        text_size = cv2.getTextSize(label, font, font_scale, 1)[0]
        text_x = x1
        text_y = y1 - 5 if y1 > 20 else y1 + text_size[1] + 5
        
        # Draw text background
        cv2.rectangle(
            img, 
            (text_x, text_y - text_size[1]), 
            (text_x + text_size[0], text_y), 
            color, 
            -1
        )
        
        # Draw text
        cv2.putText(
            img, 
            label, 
            (text_x, text_y), 
            font, 
            font_scale, 
            (0, 0, 0), 
            1, 
            cv2.LINE_AA
        )
    
    # Draw removed elements on img1
    for diff in diff_results.removed:
        label = f"Removed: {diff.element_id}"
        draw_box(img1_annotated, diff.bbox, label, CHANGE_COLORS['removed'])
    
    # Draw added elements on img2
    for diff in diff_results.added:
        label = f"Added: {diff.element_id}"
        draw_box(img2_annotated, diff.bbox, label, CHANGE_COLORS['added'])
    
    # Draw text changes on img2
    for diff in diff_results.text_changed:
        label = f"Text: {diff.element_id}"
        draw_box(img2_annotated, diff.bbox, label, CHANGE_COLORS['text-changed'])
    
    # Draw visual changes on img2
    for diff in diff_results.visual_changed:
        label = f"Visual: {diff.element_id}"
        draw_box(img2_annotated, diff.bbox, label, CHANGE_COLORS['visual-changed'])
    
    # Save the annotated images
    timestamp = int(time.time())
    cv2.imwrite(os.path.join(output_dir, f"original_{timestamp}.png"), cv2.cvtColor(img1_annotated, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(output_dir, f"modified_{timestamp}.png"), cv2.cvtColor(img2_annotated, cv2.COLOR_RGB2BGR))
    
    return img1_annotated, img2_annotated

def visualize_diff(img1: np.ndarray, img2: np.ndarray, diff_results: ImageDiffResults, title: str = "Image Diff Visualization"):
    """
    Create a matplotlib visualization of the diff results.
    
    Args:
        img1: Original image as numpy array (annotated)
        img2: New image as numpy array (annotated)
        diff_results: Results from the ImageDiffCreator
        title: Title for the plot
    """
    plt.figure(figsize=(15, 10))
    
    # Plot original image with removed elements
    plt.subplot(1, 2, 1)
    plt.imshow(img1)
    plt.title("Original Image (Red = Removed)")
    plt.axis('off')
    
    # Plot new image with added, text, and visual changes
    plt.subplot(1, 2, 2)
    plt.imshow(img2)
    plt.title("Modified Image (Green = Added, Blue = Text, Yellow = Visual)")
    plt.axis('off')
    
    plt.suptitle(title)
    
    # Create legend
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor=tuple(c/255 for c in CHANGE_COLORS['removed']), markersize=15, label='Removed'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=tuple(c/255 for c in CHANGE_COLORS['added']), markersize=15, label='Added'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=tuple(c/255 for c in CHANGE_COLORS['text-changed']), markersize=15, label='Text Changed'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=tuple(c/255 for c in CHANGE_COLORS['visual-changed']), markersize=15, label='Visual Changed')
    ]
    plt.figlegend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=4)
    
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])
    
    # Save in the output directory
    timestamp = int(time.time())
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"diff_visualization_{timestamp}.png")
    plt.savefig(output_path, dpi=300)
    logger.info(f"Saved visualization to {output_path}")
    
    plt.show()

def create_diff_summary(diff_results: ImageDiffResults) -> str:
    """
    Create a text summary of the diff results.
    
    Args:
        diff_results: Results from ImageDiffCreator
        
    Returns:
        str: Formatted summary of changes
    """
    summary = []
    summary.append("=" * 50)
    summary.append("DIFF SUMMARY")
    summary.append("=" * 50)
    
    # Count total changes
    total_changes = len(diff_results.all_changes)
    summary.append(f"Total changes detected: {total_changes}")
    summary.append(f"- Added elements: {len(diff_results.added)}")
    summary.append(f"- Removed elements: {len(diff_results.removed)}")
    summary.append(f"- Text changes: {len(diff_results.text_changed)}")
    summary.append(f"- Visual changes: {len(diff_results.visual_changed)}")
    summary.append("-" * 50)
    
    # Added elements details
    if diff_results.added:
        summary.append("ADDED ELEMENTS:")
        for i, diff in enumerate(diff_results.added):
            summary.append(f"  {i+1}. ID: {diff.element_id}, Type: {diff.element_type}, Content: '{diff.new_content}'")
            summary.append(f"     Saliency: {diff.saliency:.3f}, Bbox: {diff.bbox}")
    
    # Removed elements details
    if diff_results.removed:
        summary.append("REMOVED ELEMENTS:")
        for i, diff in enumerate(diff_results.removed):
            summary.append(f"  {i+1}. ID: {diff.element_id}, Type: {diff.element_type}, Content: '{diff.old_content}'")
            summary.append(f"     Saliency: {diff.saliency:.3f}, Bbox: {diff.bbox}")
    
    # Text changed elements details
    if diff_results.text_changed:
        summary.append("TEXT CHANGES:")
        for i, diff in enumerate(diff_results.text_changed):
            summary.append(f"  {i+1}. ID: {diff.element_id}, Type: {diff.element_type}")
            summary.append(f"     Old text: '{diff.old_content}'")
            summary.append(f"     New text: '{diff.new_content}'")
            summary.append(f"     Similarity: {diff.similarity_score:.3f}, Saliency: {diff.saliency:.3f}")
    
    # Visual changed elements details
    if diff_results.visual_changed:
        summary.append("VISUAL CHANGES:")
        for i, diff in enumerate(diff_results.visual_changed):
            summary.append(f"  {i+1}. ID: {diff.element_id}, Type: {diff.element_type}")
            summary.append(f"     Classification: {diff.classification}")
            summary.append(f"     Similarity: {diff.similarity_score:.3f}, Diff ratio: {diff.visual_diff_ratio:.3f}")
            summary.append(f"     Saliency: {diff.saliency:.3f}")
    
    summary.append("=" * 50)
    return "\n".join(summary)

def test_with_json_data(
    json_path: str = JSON_FILE_PATH,
    output_dir: str = str(OUTPUT_DIR),
    source_types: Optional[List[str]] = None,
    saliency_threshold: float = 0.05,
    visualize: bool = True
) -> ImageDiffResults:
    """
    Test the ImageDiffCreator using real data from JSON file,
    comparing the first two screenshot results.
    
    Args:
        json_path: Path to the JSON file with screenshot events
        output_dir: Directory to save visualization
        source_types: List of source types to filter by
        saliency_threshold: Minimum saliency for changes
        visualize: Whether to visualize the results
        
    Returns:
        ImageDiffResults: Results of the comparison
    """
    logger.info(f"Starting image diff test with JSON data")
    logger.info(f"JSON path: {json_path}")
    
    # Check if JSON file exists
    if not os.path.exists(json_path):
        logger.error(f"JSON file not found: {json_path}")
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load screenshot events
    logger.info("Loading screenshot events from JSON")
    screenshot_events = load_screenshot_events(json_path)
    
    if len(screenshot_events) < 2:
        logger.error(f"Not enough valid screenshot events (found {len(screenshot_events)}, need at least 2)")
        raise ValueError("Not enough valid screenshot events")
    
    # Get OmniParser results
    logger.info("Generating OmniParser results")
    omniparser_results = get_omniparser_inference_data(screenshot_events)
    
    if len(omniparser_results.omniparser_result_models) < 2:
        logger.error(f"Not enough valid OmniParser models (found {len(omniparser_results.omniparser_result_models)}, need at least 2)")
        raise ValueError("Not enough valid OmniParser models")
    
    # Take the first two models for comparison
    result1 = omniparser_results.omniparser_result_models[0]
    result2 = omniparser_results.omniparser_result_models[1]
    
    logger.info(f"Using models from timestamps:")
    logger.info(f"  Model 1: {result1.timestamp}")
    logger.info(f"  Model 2: {result2.timestamp}")
    
    # Get image paths
    image_path1 = result1.omniparser_result.original_image_path
    image_path2 = result2.omniparser_result.original_image_path
    
    logger.info(f"Image 1: {image_path1}")
    logger.info(f"Image 2: {image_path2}")
    
    # Initialize the diff creator
    logger.info("Initializing ImageDiffCreator")
    logger.info(f"Source types filter: {source_types}")
    logger.info(f"Saliency threshold: {saliency_threshold}")
    diff_creator = ImageDiffCreator(
        source_types=source_types,
        saliency_threshold=saliency_threshold
    )
    
    # Run the diff detection
    logger.info("Running diff detection")
    diff_results = diff_creator.compare_images(image_path1, image_path2, result1, result2)
    
    # Log and print summary
    summary = create_diff_summary(diff_results)
    logger.info("Diff detection complete")
    logger.info("\n" + summary)
    print(summary)
    
    # Visualize if requested
    if visualize:
        logger.info("Creating visualizations")
        
        # Load images
        img1 = np.array(Image.open(image_path1).convert("RGB"))
        img2 = np.array(Image.open(image_path2).convert("RGB"))
        
        # Draw boxes on images
        img1_annotated, img2_annotated = draw_diff_results(img1, img2, diff_results, output_dir)
        
        # Create visualization
        try:
            visualize_diff(img1_annotated, img2_annotated, diff_results)
            logger.info(f"Visualization saved to {output_dir}")
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
    
    return diff_results

def test_image_diff_creator(
    image_path1: str,
    image_path2: str,
    output_dir: str = './diff_output',
    source_types: Optional[List[str]] = None,
    saliency_threshold: float = 0.05,
    visualize: bool = True
) -> ImageDiffResults:
    """
    Test the ImageDiffCreator on two images.
    
    Args:
        image_path1: Path to the original image
        image_path2: Path to the modified image
        output_dir: Directory to save visualization
        source_types: List of source types to filter by
        saliency_threshold: Minimum saliency for changes
        visualize: Whether to visualize the results
        
    Returns:
        ImageDiffResults: Results of the comparison
    """
    logger.info(f"Starting image diff test")
    logger.info(f"Original image: {image_path1}")
    logger.info(f"Modified image: {image_path2}")
    
    # Check if image files exist
    if not os.path.exists(image_path1):
        logger.error(f"Original image not found: {image_path1}")
        raise FileNotFoundError(f"Original image not found: {image_path1}")
    
    if not os.path.exists(image_path2):
        logger.error(f"Modified image not found: {image_path2}")
        raise FileNotFoundError(f"Modified image not found: {image_path2}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse images with OmniParser
    logger.info("Parsing original image with OmniParser")
    result1 = get_omniparser_inference_data_from_image_path(image_path1)
    logger.info(f"Parsed original image: {len(result1.parsed_content_results)} elements detected")
    
    logger.info("Parsing modified image with OmniParser")
    result2 = get_omniparser_inference_data_from_image_path(image_path2)
    logger.info(f"Parsed modified image: {len(result2.parsed_content_results)} elements detected")
    
    # Initialize the diff creator
    logger.info("Initializing ImageDiffCreator")
    logger.info(f"Source types filter: {source_types}")
    logger.info(f"Saliency threshold: {saliency_threshold}")
    diff_creator = ImageDiffCreator(
        source_types=source_types,
        saliency_threshold=saliency_threshold
    )
    
    # Run the diff detection
    logger.info("Running diff detection")
    diff_results = diff_creator.compare_images(image_path1, image_path2, result1, result2)
    
    # Log and print summary
    summary = create_diff_summary(diff_results)
    logger.info("Diff detection complete")
    logger.info("\n" + summary)
    print(summary)
    
    # Visualize if requested
    if visualize:
        logger.info("Creating visualizations")
        
        # Load images
        img1 = np.array(Image.open(image_path1).convert("RGB"))
        img2 = np.array(Image.open(image_path2).convert("RGB"))
        
        # Draw boxes on images
        img1_annotated, img2_annotated = draw_diff_results(img1, img2, diff_results, output_dir)
        
        # Create visualization
        try:
            visualize_diff(img1_annotated, img2_annotated, diff_results)
            logger.info(f"Visualization saved to {output_dir}")
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
    
    return diff_results

def main():
    test_with_json_data(
            json_path=JSON_FILE_PATH,
            output_dir=OUTPUT_DIR,
            saliency_threshold=0.05,
            visualize=True,
            source_types=None
        )

if __name__ == "__main__":
    main()
