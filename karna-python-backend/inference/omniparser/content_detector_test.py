import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
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

from inference.omniparser.content_detector import ContentDetector
from inference.omniparser.ui_dynamic_area_detector import UIOptimizedDynamicAreaDetector
from inference.omniparser.main_area_segmenter import MainAreaSegmenter
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
OUTPUT_DIR = Path(current_dir) / "content_detector_output"

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

def visualize_content_detection(results_list: OmniParserResultModelList, detection_results: Dict[str, Any]):
    """
    Visualize content detection results showing dynamic areas and content segmentation.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        detection_results: The results from ContentDetector.detect()
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
        
        # Get dynamic areas
        dynamic_areas = detection_results.get("dynamic_areas", {})
        
        # Draw dynamic areas with different colors
        colors = {
            'largest_area': 'red',
            'center_weighted': 'green',
            'highest_frequency': 'purple',
            'vertical_union': 'orange',
            'main_content_area': 'cyan'
        }
        
        handles = []  # For legend
        
        for rule_name, bbox in dynamic_areas.items():
            # Skip all_regions
            if rule_name == "all_regions":
                continue
                
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                color = colors.get(rule_name, 'gray')
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=2, edgecolor=color, facecolor=color, alpha=0.2
                )
                plt.gca().add_patch(rect)
                
                # Add to legend handles
                handles.append(patches.Patch(color=color, alpha=0.5, label=f"Dynamic Area ({rule_name})"))
        
        # Draw main content area with thicker border
        main_content_bbox = detection_results.get("main_content_bbox")
        if main_content_bbox is not None:
            x1, y1, x2, y2 = main_content_bbox
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=4, edgecolor='yellow', facecolor='none', alpha=0.8
            )
            plt.gca().add_patch(rect)
            
            # Add text label for main content
            plt.text(x1, y1-10, "MAIN CONTENT", color='yellow', fontsize=14, fontweight='bold')
            
            # Add to legend
            handles.append(patches.Patch(color='yellow', alpha=0.8, label="Main Content"))
        
        # Draw content segmentation results if available
        if "content_segmentation" in detection_results:
            content_segmentation = detection_results["content_segmentation"]
            
            # Draw clusters
            if "clusters" in content_segmentation:
                for i, cluster in enumerate(content_segmentation["clusters"]):
                    # Skip if no score in cluster (not properly formed)
                    if not hasattr(cluster, 'score'):
                        continue
                        
                    # Calculate color based on score (green = high score, blue = low score)
                    green = int(255 * cluster.score)
                    blue = int(255 * (1 - cluster.score))
                    
                    # Use matplotlib's color format
                    color = (0, green/255, blue/255)
                    
                    x1, y1, x2, y2 = cluster.bbox
                    
                    # Convert normalized coordinates to absolute if needed
                    if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                        x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                    
                    rect = patches.Rectangle(
                        (x1, y1), x2 - x1, y2 - y1,
                        linewidth=1, edgecolor=color, facecolor=color, alpha=0.3
                    )
                    plt.gca().add_patch(rect)
                    
                    # Add label text
                    plt.text(x1 + 5, y1 + 5, f"C{i}: {cluster.score:.2f}", color=color, fontsize=10)
            
            # Draw primary content if different from main_content_bbox
            primary_content = content_segmentation.get("primary_content")
            if primary_content is not None and primary_content != main_content_bbox:
                x1, y1, x2, y2 = primary_content
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=3, edgecolor='white', facecolor='none', alpha=0.7,
                    linestyle='--'
                )
                plt.gca().add_patch(rect)
                
                # Add to legend
                handles.append(patches.Patch(color='white', alpha=0.7, label="Primary Content (Segmentation)"))
        
        plt.title("Content Detection Results", fontsize=14)
        if handles:
            plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"content_detection_{timestamp}.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved content detection visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing content detection: {e}")

def visualize_content_segmentation(results_list: OmniParserResultModelList, detection_results: Dict[str, Any]):
    """
    Create a focused visualization of the content segmentation results.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        detection_results: The results from ContentDetector.detect()
    """
    # Check if content segmentation is available
    if "content_segmentation" not in detection_results:
        logger.warning("No content segmentation results available for visualization")
        return
    
    # Prepare visualization data
    viz_data = prepare_visualization(results_list)
    if not viz_data:
        return
    
    timestamp, last_model, img, img_width, img_height = viz_data
    
    try:
        # Create figure
        plt.figure(figsize=(15, 10))
        plt.imshow(img)
        
        content_segmentation = detection_results["content_segmentation"]
        
        # Draw main area for context
        main_area_bbox = detection_results.get("dynamic_areas", {}).get("main_content_area")
        if main_area_bbox is None:
            main_area_bbox = detection_results.get("dynamic_areas", {}).get("vertical_union")
            if main_area_bbox is None:
                main_area_bbox = detection_results.get("dynamic_areas", {}).get("largest_area")
        
        if main_area_bbox is not None:
            x1, y1, x2, y2 = main_area_bbox
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2, edgecolor='blue', facecolor='none', alpha=0.5,
                linestyle='--'
            )
            plt.gca().add_patch(rect)
            plt.text(x1, y1-10, "DYNAMIC AREA", color='blue', fontsize=12)
        
        # Draw clusters with color gradient based on score
        if "clusters" in content_segmentation:
            for i, cluster in enumerate(content_segmentation["clusters"]):
                # Skip if no score in cluster (not properly formed)
                if not hasattr(cluster, 'score'):
                    continue
                    
                # Calculate color based on score (red = high score, blue = low score)
                red = int(255 * cluster.score)
                blue = int(255 * (1 - cluster.score))
                
                # Use matplotlib's color format
                color = (red/255, 0, blue/255)
                
                x1, y1, x2, y2 = cluster.bbox
                
                # Convert normalized coordinates to absolute if needed
                if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                    x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
                
                rect = patches.Rectangle(
                    (x1, y1), x2 - x1, y2 - y1,
                    linewidth=2, edgecolor=color, facecolor=color, alpha=0.4
                )
                plt.gca().add_patch(rect)
                
                # Add label text
                plt.text(x1 + 5, y1 + 15, f"Cluster {i}: score={cluster.score:.2f}", 
                         color='white', fontsize=10, fontweight='bold',
                         bbox=dict(facecolor=color, alpha=0.6))
        
        # Draw primary content with prominent outline
        primary_content = content_segmentation.get("primary_content")
        if primary_content is not None:
            x1, y1, x2, y2 = primary_content
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=4, edgecolor='yellow', facecolor='none', alpha=0.9
            )
            plt.gca().add_patch(rect)
            
            plt.text(x1, y1-10, "PRIMARY CONTENT", color='yellow', fontsize=14, fontweight='bold')
        
        plt.title("Content Segmentation Results", fontsize=14)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"content_segmentation_{timestamp}.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved content segmentation visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing content segmentation: {e}")

def visualize_comparison(results_list: OmniParserResultModelList, detection_results: Dict[str, Any]):
    """
    Create a comparison visualization between dynamic area detection and content segmentation.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        detection_results: The results from ContentDetector.detect()
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
        
        # Get main areas from dynamic detection
        main_dynamic_area = detection_results.get("dynamic_areas", {}).get("main_content_area")
        if main_dynamic_area is None:
            main_dynamic_area = detection_results.get("dynamic_areas", {}).get("vertical_union")
            if main_dynamic_area is None:
                main_dynamic_area = detection_results.get("dynamic_areas", {}).get("largest_area")
        
        # Get primary content from segmentation if available
        primary_content = None
        content_segmentation = detection_results.get("content_segmentation", {})
        if content_segmentation:
            primary_content = content_segmentation.get("primary_content")
        
        # Draw main dynamic area
        if main_dynamic_area is not None:
            x1, y1, x2, y2 = main_dynamic_area
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=3, edgecolor='blue', facecolor='blue', alpha=0.3
            )
            plt.gca().add_patch(rect)
            
            plt.text(x1, y1-10, "Dynamic Detection", color='blue', fontsize=12, fontweight='bold')
        
        # Draw primary content area
        if primary_content is not None:
            x1, y1, x2, y2 = primary_content
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=3, edgecolor='red', facecolor='red', alpha=0.3,
                linestyle='--'
            )
            plt.gca().add_patch(rect)
            
            plt.text(x1, y1-10, "Content Segmentation", color='red', fontsize=12, fontweight='bold')
        
        # Draw final main content
        main_content_bbox = detection_results.get("main_content_bbox")
        if main_content_bbox is not None:
            x1, y1, x2, y2 = main_content_bbox
            
            # Convert normalized coordinates to absolute if needed
            if max(x1, y1, x2, y2) <= 1.0:  # Normalized
                x1, y1, x2, y2 = x1 * img_width, y1 * img_height, x2 * img_width, y2 * img_height
            
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=4, edgecolor='yellow', facecolor='none', alpha=0.8
            )
            plt.gca().add_patch(rect)
            
            plt.text(x1, y1-10, "FINAL MAIN CONTENT", color='yellow', fontsize=14, fontweight='bold')
        
        # Add comparisons and metrics if possible
        if main_dynamic_area is not None and primary_content is not None:
            # Calculate overlap ratio
            dynamic_area = (main_dynamic_area[2] - main_dynamic_area[0]) * (main_dynamic_area[3] - main_dynamic_area[1])
            
            intersection_x1 = max(main_dynamic_area[0], primary_content[0])
            intersection_y1 = max(main_dynamic_area[1], primary_content[1])
            intersection_x2 = min(main_dynamic_area[2], primary_content[2])
            intersection_y2 = min(main_dynamic_area[3], primary_content[3])
            
            if intersection_x2 > intersection_x1 and intersection_y2 > intersection_y1:
                intersection_area = (intersection_x2 - intersection_x1) * (intersection_y2 - intersection_y1)
                overlap_ratio = intersection_area / dynamic_area if dynamic_area > 0 else 0
                
                # Add metrics text
                plt.figtext(
                    0.5, 0.02, 
                    f"Overlap ratio: {overlap_ratio:.2f}\n"
                    f"Dynamic area height: {main_dynamic_area[3]-main_dynamic_area[1]:.2f}, Primary content height: {primary_content[3]-primary_content[1]:.2f}\n"
                    f"Dynamic area width: {main_dynamic_area[2]-main_dynamic_area[0]:.2f}, Primary content width: {primary_content[2]-primary_content[0]:.2f}",
                    ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8)
                )
        
        # Add legend
        handles = [
            patches.Patch(color='blue', alpha=0.3, label="Dynamic Area Detection"),
            patches.Patch(color='red', alpha=0.3, label="Content Segmentation"),
            patches.Patch(color='yellow', alpha=0.8, label="Final Main Content")
        ]
        
        plt.title("Comparison: Dynamic Detection vs Content Segmentation", fontsize=14)
        plt.legend(handles=handles, fontsize=12)
        
        # Save the visualization
        output_file = OUTPUT_DIR / f"comparison_{timestamp}.png"
        plt.savefig(str(output_file), dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved comparison visualization to {output_file}")
    
    except Exception as e:
        logger.error(f"Error visualizing comparison: {e}")

def visualize_content_detector_results(results_list: OmniParserResultModelList, detection_results: Dict[str, Any]):
    """
    Create multiple visualizations for the ContentDetector results.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        detection_results: The results from ContentDetector.detect()
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
        visualize_content_detection(results_list, detection_results)
        logger.info("Created overall content detection visualization")
    except Exception as e:
        logger.error(f"Failed to create content detection visualization: {e}")
    
    try:
        visualize_content_segmentation(results_list, detection_results)
        logger.info("Created content segmentation visualization")
    except Exception as e:
        logger.error(f"Failed to create content segmentation visualization: {e}")
    
    try:
        visualize_comparison(results_list, detection_results)
        logger.info("Created comparison visualization")
    except Exception as e:
        logger.error(f"Failed to create comparison visualization: {e}")
    
    # Log final status
    try:
        files = list(OUTPUT_DIR.glob("*.png"))
        logger.info(f"Created {len(files)} visualization files: {', '.join(f.name for f in files)}")
    except Exception as e:
        logger.error(f"Error checking output files: {e}")

def test_content_detector(use_viewport=False):
    """
    Test the ContentDetector using real data from JSON file.
    
    Args:
        use_viewport: Whether to crop screenshots according to viewport rendering area
    """
    logger.info("Starting ContentDetector test...")
    
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
        dynamic_detector = UIOptimizedDynamicAreaDetector(
            image_diff_creator=diff_creator,
            min_change_frequency=0.3,
            min_area_size=0.01,
            grouping_distance=0.1,
            min_saliency=0.1,
            x_overlap_threshold=0.3,
            min_vertical_region_height=0.1
        )
        
        # Initialize the main area segmenter
        segmenter = MainAreaSegmenter(
            grid_size=(20, 20),
            min_cluster_size=3,
            eps=0.5,
            min_content_score=0.3
        )
        
        # Initialize the content detector
        detector = ContentDetector(
            dynamic_detector=dynamic_detector,
            segmenter=segmenter
        )
        
        # Run detection
        logger.info("Running content detection...")
        detection_results = detector.detect(test_data)
        
        # Print results
        logger.info("Content Detection Results:")
        
        # Print dynamic areas
        if "dynamic_areas" in detection_results:
            logger.info("Dynamic Areas:")
            for rule_name, bbox in detection_results["dynamic_areas"].items():
                if rule_name == "all_regions":
                    logger.info(f"  {rule_name}: {len(bbox)} regions detected")
                    continue
                    
                if bbox is not None:
                    logger.info(f"  {rule_name}: {[round(coord, 3) for coord in bbox]}")
                else:
                    logger.info(f"  {rule_name}: None")
        
        # Print main content area
        if "main_content_bbox" in detection_results:
            logger.info(f"Main Content Area: {[round(coord, 3) for coord in detection_results['main_content_bbox']]}")
        
        # Print content segmentation results if available
        if "content_segmentation" in detection_results:
            content_seg = detection_results["content_segmentation"]
            
            if "clusters" in content_seg:
                logger.info(f"Content Clusters: {len(content_seg['clusters'])} clusters found")
                
                # Print top 3 clusters by score
                top_clusters = sorted(content_seg["clusters"], 
                                     key=lambda c: c.score if hasattr(c, 'score') else 0, 
                                     reverse=True)[:3]
                
                for i, cluster in enumerate(top_clusters):
                    if hasattr(cluster, 'score'):
                        logger.info(f"  Cluster {i}: score={cluster.score:.3f}, bbox={[round(coord, 3) for coord in cluster.bbox]}")
            
            if "primary_content" in content_seg and content_seg["primary_content"] is not None:
                logger.info(f"Primary Content: {[round(coord, 3) for coord in content_seg['primary_content']]}")
        
        # Visualize results with multiple separate plots
        logger.info("Creating visualizations...")
        # Force output directory to exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        visualize_content_detector_results(test_data, detection_results)
        
        # Verify results
        success = False
        
        if "main_content_bbox" in detection_results and detection_results["main_content_bbox"] is not None:
            success = True
            logger.info("Test PASSED: Successfully detected main content area")
        else:
            logger.warning("Test FAILED: No main content area detected")
            
        # Verify visualization files created
        vis_files = list(OUTPUT_DIR.glob("*.png"))
        logger.info(f"Visualization complete. Created {len(vis_files)} files at {OUTPUT_DIR}")
        
        return detection_results
        
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}", exc_info=True)
        return None

def visualize_with_pil(results_list: OmniParserResultModelList, detection_results: Dict[str, Any]):
    """
    Use the ContentDetector's built-in visualization methods.
    
    Args:
        results_list: The OmniParserResultModelList used for detection
        detection_results: The results from ContentDetector.detect()
    """
    if not results_list.omniparser_result_models:
        logger.warning("No frames in results list, cannot visualize with PIL")
        return
    
    try:
        # Create output directory if it doesn't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Get the last frame
        last_model = results_list.omniparser_result_models[-1]
        screenshot_path = last_model.omniparser_result.original_image_path
        
        # Initialize the ContentDetector for visualization
        detector = ContentDetector()
        
        # Generate the timestamp for the output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(OUTPUT_DIR / f"pil_visualization_{timestamp}.png")
        
        # Use the detector's visualize method
        detector.visualize(detection_results, screenshot_path, output_path)
        
        logger.info(f"Created PIL visualization at {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating PIL visualization: {e}")
        
def main():
    results = test_content_detector(use_viewport=True) 
    
    # If results are available, also test the built-in visualization
    if results:
        # Load data again for visualization test
        screenshot_events = load_screenshot_events(JSON_FILE_PATH)
        test_data = get_omniparser_inference_data(screenshot_events)
        visualize_with_pil(test_data, results)

if __name__ == "__main__":
    main()
