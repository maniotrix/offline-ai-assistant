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

from inference.omniparser.ui_dynamic_area_detector import UIOptimizedDynamicAreaDetector
from inference.omniparser.dynamic_area_detector_test import (
    load_screenshot_events,
    DEFAULT_DATA_DIR,
    JSON_FILE_PATH
)
from inference.omniparser.image_diff_creator import ImageDiffCreator
from inference.omniparser.omni_helper import (
    OmniParserResultModelList,
    get_omniparser_inference_data
)
from config.paths import workspace_dir

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Output directory for visualizations 
OUTPUT_DIR = Path(current_dir) / "ui_detection_output"

def visualize_ui_detection_results(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Visualize the UI-optimized detection results on the last frame.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
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
            'highest_frequency': 'purple',
            'vertical_union': 'orange',
            'main_content_area': 'cyan'
        }
        
        handles = []  # For legend
        
        for rule_name, bbox in main_areas.items():
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = colors.get(rule_name, 'gray')
                
                # Use different styles to distinguish UI-specific detections
                if rule_name in ['vertical_union', 'main_content_area']:
                    # Thicker lines with dash pattern for UI-specific regions
                    rect = patches.Rectangle(
                        (x1, y1), x2 - x1, y2 - y1,
                        linewidth=4, edgecolor=color, facecolor=color, alpha=0.3, 
                        linestyle='--'
                    )
                else:
                    rect = patches.Rectangle(
                        (x1, y1), x2 - x1, y2 - y1,
                        linewidth=3, edgecolor=color, facecolor=color, alpha=0.3
                    )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"Main Area ({rule_name})"))
                
                # Add label text
                plt.text(x1, y1-5, rule_name, color=color, fontsize=12, fontweight='bold')
        
        plt.title("UI-Optimized Dynamic Area Detection Results", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"ui_dynamic_area_detection_{timestamp}.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved UI detection visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing UI detection results: {e}")
    
    # Create a comparison visualization showing both standard and UI-optimized regions
    try:
        # Get the last frame
        last_model = results_list.omniparser_result_models[-1]
        screenshot_path = last_model.omniparser_result.original_image_path
        
        plt.figure(figsize=(15, 10))
        img = plt.imread(screenshot_path)
        plt.imshow(img)
        
        # Get image dimensions
        img_width = last_model.omniparser_result.original_image_width
        img_height = last_model.omniparser_result.original_image_height
        
        # Draw detected main areas with different colors for each rule
        standard_colors = {
            'largest_area': 'red',
            'center_weighted': 'green',
            'highest_frequency': 'purple'
        }
        
        ui_colors = {
            'vertical_union': 'orange',
            'main_content_area': 'cyan'
        }
        
        handles = []  # For legend
        
        # First draw standard areas with solid lines
        for rule_name, bbox in main_areas.items():
            if bbox is not None and rule_name in standard_colors:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = standard_colors.get(rule_name)
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=3, edgecolor=color, facecolor=color, alpha=0.2
                )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"Standard ({rule_name})"))
        
        # Then draw UI-optimized areas with dashed lines and higher alpha
        for rule_name, bbox in main_areas.items():
            if bbox is not None and rule_name in ui_colors:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = ui_colors.get(rule_name)
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=4, edgecolor=color, facecolor=color, alpha=0.4,
                    linestyle='--'
                )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"UI-Optimized ({rule_name})"))
                
                # Add label text
                plt.text(x1, y1-5, rule_name, color=color, fontsize=12, fontweight='bold')
        
        plt.title("Comparison: Standard vs. UI-Optimized Dynamic Areas", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"ui_vs_standard_comparison_{timestamp}.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved comparison visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing comparison: {e}")

def test_ui_dynamic_area_detector(use_viewport=False):
    """
    Test the UIOptimizedDynamicAreaDetector using real data from JSON file.
    
    Args:
        use_viewport: Whether to crop screenshots according to viewport rendering area
    """
    logger.info("Starting UIOptimizedDynamicAreaDetector test...")
    
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

        # Load real data from JSON file
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
        
        # Initialize the UI-optimized detector
        detector = UIOptimizedDynamicAreaDetector(
            image_diff_creator=diff_creator,
            min_change_frequency=0.3,
            min_area_size=0.01,
            grouping_distance=0.1,
            min_saliency=0.1,
            x_overlap_threshold=0.5,
            min_vertical_region_height=0.1
        )
        
        # Run detection
        logger.info("Running UI-optimized dynamic area detection...")
        main_areas = detector.detect_main_areas(test_data)
        
        # Print results
        logger.info("UI-Optimized Detection Results:")
        for rule_name, bbox in main_areas.items():
            if bbox is not None:
                logger.info(f"  {rule_name}: {[round(coord, 3) for coord in bbox]}")
            else:
                logger.info(f"  {rule_name}: None")
        
        # Visualize results
        visualize_ui_detection_results(test_data, main_areas)
        
        # Verify results
        success = False
        ui_specific_results = False
        
        for rule_name, bbox in main_areas.items():
            if bbox is not None:
                success = True
                if rule_name in ['vertical_union', 'main_content_area']:
                    ui_specific_results = True
        
        if success:
            logger.info("Test PASSED: Successfully detected dynamic areas")
            if ui_specific_results:
                logger.info("UI-specific areas detected successfully")
            else:
                logger.warning("No UI-specific areas detected (vertical_union, main_content_area)")
        else:
            logger.warning("Test FAILED: No dynamic areas detected")
        
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}", exc_info=True)

if __name__ == "__main__":
    test_ui_dynamic_area_detector() 