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

def prepare_visualization(results_list: OmniParserResultModelList):
    """
    Prepare for visualization by setting up the output directory and getting common data.
    
    Args:
        results_list: The OmniParserResultModelList to visualize
        
    Returns:
        Tuple of (timestamp, last_model, img, img_width, img_height) or None if error
    """
    if not results_list.omniparser_result_models:
        logger.warning("No frames in results list, cannot visualize")
        return None
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create timestamp for unique filenames - don't clear directory here
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Get the last frame
        last_model = results_list.omniparser_result_models[-1]
        screenshot_path = last_model.omniparser_result.original_image_path
        
        # Read the image
        img = plt.imread(screenshot_path)
        
        # Get image dimensions
        img_width = last_model.omniparser_result.original_image_width
        img_height = last_model.omniparser_result.original_image_height
        
        return timestamp, last_model, img, img_width, img_height
    
    except Exception as e:
        logger.error(f"Error preparing visualization: {e}")
        return None

def visualize_all_ui_elements(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Visualize all UI elements on a single plot.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
    """
    # Prepare visualization data
    viz_data = prepare_visualization(results_list)
    if not viz_data:
        return
    
    timestamp, last_model, img, img_width, img_height = viz_data
    
    try:
        # Create figure
        plt.figure(figsize=(15, 10))
        plt.imshow(img)
        
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
        
        plt.title("All Dynamic Areas (Standard + UI-Optimized)", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"all_detection_areas_.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved all areas visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing all UI elements: {e}")

def visualize_standard_areas(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Visualize only the standard dynamic areas.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
    """
    # Prepare visualization data
    viz_data = prepare_visualization(results_list)
    if not viz_data:
        return
    
    timestamp, last_model, img, img_width, img_height = viz_data
    
    try:
        # Create figure
        plt.figure(figsize=(15, 10))
        plt.imshow(img)
        
        # Standard dynamic areas
        standard_colors = {
            'largest_area': 'red',
            'center_weighted': 'green',
            'highest_frequency': 'purple'
        }
        
        handles = []  # For legend
        
        # Draw only standard areas
        for rule_name, bbox in main_areas.items():
            if bbox is not None and rule_name in standard_colors:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = standard_colors.get(rule_name)
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=3, edgecolor=color, facecolor=color, alpha=0.3
                )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"Standard ({rule_name})"))
                
                # Add label text
                plt.text(x1, y1-5, rule_name, color=color, fontsize=12, fontweight='bold')
        
        plt.title("Standard Dynamic Areas (Base Detector)", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"standard_areas_.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved standard areas visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing standard areas: {e}")

def visualize_ui_optimized_areas(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Visualize only the UI-optimized dynamic areas.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
    """
    # Prepare visualization data
    viz_data = prepare_visualization(results_list)
    if not viz_data:
        return
    
    timestamp, last_model, img, img_width, img_height = viz_data
    
    try:
        # Create figure
        plt.figure(figsize=(15, 10))
        plt.imshow(img)
        
        # UI-specific areas
        ui_colors = {
            'vertical_union': 'orange',
            'main_content_area': 'cyan'
        }
        
        handles = []  # For legend
        
        # Draw only UI-optimized areas
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
        
        plt.title("UI-Optimized Dynamic Areas", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"ui_optimized_areas_.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved UI-optimized areas visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing UI-optimized areas: {e}")

def visualize_comparison_largest_to_vertical(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Create a focused comparison between largest_area and vertical_union/main_content_area.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
    """
    # Prepare visualization data
    viz_data = prepare_visualization(results_list)
    if not viz_data:
        return
    
    timestamp, last_model, img, img_width, img_height = viz_data
    
    # Skip if we don't have both largest_area and at least one UI area
    largest_area = main_areas.get('largest_area')
    has_ui_area = main_areas.get('vertical_union') is not None or main_areas.get('main_content_area') is not None
    
    if not largest_area or not has_ui_area:
        logger.warning("Cannot create largest-to-vertical comparison - missing required areas")
        return
    
    try:
        # Create figure
        plt.figure(figsize=(15, 10))
        plt.imshow(img)
        
        handles = []  # For legend
        
        # First draw the largest area
        x1, y1, x2, y2 = largest_area
        
        # Convert normalized coordinates to absolute if needed
        if max(x1, y1, x2, y2) <= 1.0:  # Normalized
            x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
        
        rect = patches.Rectangle(
            (x1, y1), x2 - x1, y2 - y1,
            linewidth=3, edgecolor='red', facecolor='red', alpha=0.2
        )
        plt.gca().add_patch(rect)
        
        # Add to legend
        handles.append(patches.Patch(color='red', alpha=0.5, label="Largest Area"))
        
        # Add label
        plt.text(x1, y1-5, "largest_area", color='red', fontsize=12, fontweight='bold')
        
        # Draw the UI areas with different styles
        ui_areas = {
            'vertical_union': ('orange', 'Vertical Union'),
            'main_content_area': ('cyan', 'Main Content Area')
        }
        
        for area_name, (color, label) in ui_areas.items():
            bbox = main_areas.get(area_name)
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=4, edgecolor=color, facecolor='none', alpha=0.7,
                    linestyle='--'
                )
                plt.gca().add_patch(rect)
                
                # Add to legend
                handles.append(patches.Patch(color=color, alpha=0.7, label=label))
                
                # Add label
                plt.text(x1, y1-5, area_name, color=color, fontsize=12, fontweight='bold')
        
        plt.title("Comparison: Largest Area vs UI-Optimized Areas", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"largest_to_vertical_comparison_.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved largest-to-vertical comparison to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing largest-to-vertical comparison: {e}")

def visualize_ui_detection_results(results_list: OmniParserResultModelList, main_areas: Dict[str, Optional[List[float]]]):
    """
    Create multiple separate visualizations of the UI detector results.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        main_areas: The detection results from UIOptimizedDynamicAreaDetector
    """
    # Clear previous visualization output
    try:
        for file in OUTPUT_DIR.glob("*.png"):
            file.unlink()
        logger.info(f"Cleared previous visualization files from {OUTPUT_DIR}")
    except Exception as e:
        logger.error(f"Error clearing visualization directory: {e}")
    
    # Create all the different visualizations as separate plots
    logger.info("Creating all visualization types...")
    
    # Run each visualization in sequence with explicit error handling
    try:
        visualize_all_ui_elements(results_list, main_areas)
        logger.info("Created all elements visualization")
    except Exception as e:
        logger.error(f"Failed to create all elements visualization: {e}")
    
    try:
        visualize_standard_areas(results_list, main_areas)
        logger.info("Created standard areas visualization")
    except Exception as e:
        logger.error(f"Failed to create standard areas visualization: {e}")
    
    try:
        visualize_ui_optimized_areas(results_list, main_areas)
        logger.info("Created UI optimized areas visualization")
    except Exception as e:
        logger.error(f"Failed to create UI optimized areas visualization: {e}")
    
    try:
        visualize_comparison_largest_to_vertical(results_list, main_areas)
        logger.info("Created largest to vertical comparison visualization")
    except Exception as e:
        logger.error(f"Failed to create largest to vertical comparison: {e}")
    
    # Log final status
    try:
        files = list(OUTPUT_DIR.glob("*.png"))
        logger.info(f"Created {len(files)} visualization files: {', '.join(f.name for f in files)}")
    except Exception as e:
        logger.error(f"Error checking output files: {e}")

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
            x_overlap_threshold=0.3,  # Updated to match the detector's default
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
        
        # Visualize results with multiple separate plots
        logger.info("Creating visualizations...")
        # Force output directory to exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
        
        # Verify visualization files created
        vis_files = list(OUTPUT_DIR.glob("*.png"))
        logger.info(f"Visualization complete. Created {len(vis_files)} files at {OUTPUT_DIR}")
        
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}", exc_info=True)

if __name__ == "__main__":
    test_ui_dynamic_area_detector() 