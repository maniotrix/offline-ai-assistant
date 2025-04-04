import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
from pathlib import Path
import numpy as np
from PIL import Image
import tempfile
import json
import argparse

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(current_dir)))

from inference.omniparser.anchor_based_main_area_detector import AnchorBasedMainAreaDetector
from inference.omniparser.anchor_based_main_area_detector_runtime import AnchorBasedMainAreaDetectorRuntime
from inference.omniparser.dynamic_area_detector_test import (
    load_screenshot_events,
    DEFAULT_DATA_DIR,
    JSON_FILE_PATH
)
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
OUTPUT_DIR = Path(current_dir) / "anchor_detector_output"

def ensure_output_dir():
    """Ensure output directory exists and return timestamp."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def visualize_main_area_references(
    main_area_references: List[Dict[str, Any]], 
    main_area: List[float],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize all main area reference patches.
    
    Args:
        main_area_references: List of main area reference dictionaries
        main_area: Main area bounding box
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    # Prepare a 2x2 grid figure (or adjust based on number of references)
    n_refs = len(main_area_references)
    if n_refs == 0:
        logger.warning("No main area references to visualize")
        return
    
    # Determine grid dimensions
    cols = min(2, n_refs)
    rows = (n_refs + cols - 1) // cols
    
    # Create figure
    fig, axes = plt.subplots(rows, cols, figsize=(12, 10))
    
    # Set title for the figure
    fig.suptitle("Main Area Reference Patches", fontsize=16)
    
    # Make axes iterable if only one row/column
    if n_refs == 1:
        axes = np.array([axes])
    elif n_refs <= 2:
        axes = axes.reshape(1, -1)
    
    # Plot each reference patch
    for i, ref in enumerate(main_area_references):
        row, col = i // cols, i % cols
        ax = axes[row, col] if rows > 1 else axes[col]
        
        # Display the patch
        ax.imshow(ref["patch"])
        ax.set_title(f"Frame {ref['frame_index']}")
        ax.axis('off')
    
    # Remove empty subplots
    for i in range(n_refs, rows * cols):
        row, col = i // cols, i % cols
        ax = axes[row, col] if rows > 1 else axes[col]
        ax.axis('off')
    
    # Also create a plot showing the main area on the original image
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    ax2.imshow(original_image)
    
    # Draw main area rectangle
    x1, y1, x2, y2 = main_area
    rect = patches.Rectangle(
        (x1, y1), x2 - x1, y2 - y1,
        linewidth=3, edgecolor='green', facecolor='green', alpha=0.3
    )
    ax2.add_patch(rect)
    ax2.set_title("Main Area Location", fontsize=14)
    ax2.axis('off')
    
    # Add text dimensions
    width = x2 - x1
    height = y2 - y1
    ax2.text(
        x1, y1 - 10, 
        f"Width: {width:.1f}px, Height: {height:.1f}px", 
        color='white', fontsize=12, 
        bbox=dict(facecolor='green', alpha=0.7)
    )
    
    # Save the figures
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{timestamp}_main_area_references.png", dpi=150)
    fig2.savefig(OUTPUT_DIR / f"{timestamp}_main_area_location.png", dpi=150)
    plt.close(fig)
    plt.close(fig2)
    logger.info(f"Saved main area references visualization")

def visualize_anchor_points(
    anchor_points: List[Dict[str, Any]],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize all anchor points.
    
    Args:
        anchor_points: List of anchor point dictionaries
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    # First create a visualization of all anchors on the original image
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(original_image)
    
    # Define colors for each constraint direction
    direction_colors = {
        'top': 'red',
        'bottom': 'blue',
        'left': 'orange',
        'right': 'purple'
    }
    
    # Add each anchor point to the original image
    for i, anchor in enumerate(anchor_points):
        x1, y1, x2, y2 = anchor["bbox"]
        direction = anchor["constraint_direction"]
        color = direction_colors.get(direction, 'white')
        
        # Draw rectangle
        rect = patches.Rectangle(
            (x1, y1), x2 - x1, y2 - y1,
            linewidth=2, edgecolor=color, facecolor=color, alpha=0.4
        )
        ax.add_patch(rect)
        
        # Add text label with index and direction
        ax.text(
            x1, y1 - 5, 
            f"#{i} - {direction}", 
            color='white', fontsize=10, 
            bbox=dict(facecolor=color, alpha=0.7)
        )
    
    # Add legend
    handles = [
        patches.Patch(color=color, alpha=0.5, label=direction)
        for direction, color in direction_colors.items()
    ]
    ax.legend(handles=handles, loc='lower right')
    
    ax.set_title("Anchor Points by Direction", fontsize=14)
    ax.axis('off')
    
    # Save the figure
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{timestamp}_anchor_points.png", dpi=150)
    plt.close(fig)
    
    # Now create a grid visualization showing each anchor patch
    n_anchors = len(anchor_points)
    if n_anchors == 0:
        logger.warning("No anchor points to visualize")
        return
    
    # Determine grid dimensions (up to 3x3)
    cols = min(3, n_anchors)
    rows = min(3, (n_anchors + cols - 1) // cols)
    
    # Create figure for the grid
    fig2, axes = plt.subplots(rows, cols, figsize=(15, 12))
    fig2.suptitle("Anchor Point Patches", fontsize=16)
    
    # Make axes iterable if only one row/column
    if n_anchors == 1:
        axes = np.array([axes])
    elif cols == 1:
        axes = axes.reshape(-1, 1)
    elif rows == 1:
        axes = axes.reshape(1, -1)
    
    # Plot each anchor patch
    for i, anchor in enumerate(anchor_points[:rows*cols]):  # Limit to grid size
        row, col = i // cols, i % cols
        ax = axes[row, col]
        
        # Display the patch
        ax.imshow(anchor["patch"])
        
        # Get direction and stability
        direction = anchor["constraint_direction"]
        stability = anchor["stability_score"]
        element_type = anchor["element_type"]
        
        # Set title with info
        ax.set_title(
            f"#{i} - {direction}\n" + 
            f"Type: {element_type}\n" +
            f"Stability: {stability:.2f}"
        )
        
        # Add colored border based on direction
        color = direction_colors.get(direction, 'white')
        for spine in ax.spines.values():
            spine.set_color(color)
            spine.set_linewidth(3)
        
        ax.axis('off')
    
    # Remove empty subplots
    for i in range(min(n_anchors, rows*cols), rows * cols):
        row, col = i // cols, i % cols
        axes[row, col].axis('off')
    
    # Save the grid figure
    plt.tight_layout()
    fig2.savefig(OUTPUT_DIR / f"{timestamp}_anchor_patches.png", dpi=150)
    plt.close(fig2)
    
    logger.info(f"Saved anchor points visualization")

def visualize_anchor_relationships(
    anchor_points: List[Dict[str, Any]],
    main_area: List[float],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize anchor point relationships to the main area.
    
    Args:
        anchor_points: List of anchor point dictionaries
        main_area: Main area bounding box
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(original_image)
    
    # Main area coordinates
    main_x1, main_y1, main_x2, main_y2 = main_area
    main_center_x = (main_x1 + main_x2) / 2
    main_center_y = (main_y1 + main_y2) / 2
    
    # Draw main area rectangle
    main_rect = patches.Rectangle(
        (main_x1, main_y1), main_x2 - main_x1, main_y2 - main_y1,
        linewidth=3, edgecolor='green', facecolor='green', alpha=0.3
    )
    ax.add_patch(main_rect)
    
    # Draw main area center
    ax.plot(main_center_x, main_center_y, 'go', markersize=8)
    
    # Add directional constraints from each anchor
    for i, anchor in enumerate(anchor_points):
        # Get anchor coordinates and center
        anchor_x1, anchor_y1, anchor_x2, anchor_y2 = anchor["bbox"]
        anchor_center_x = (anchor_x1 + anchor_x2) / 2
        anchor_center_y = (anchor_y1 + anchor_y2) / 2
        
        # Get relationship info
        direction = anchor["constraint_direction"]
        h_relation = anchor["horizontal_relation"]
        v_relation = anchor["vertical_relation"]
        
        # Define colors for relationships
        h_color = 'orange' if h_relation == 'left' else 'purple'
        v_color = 'red' if v_relation == 'top' else 'blue'
        
        # Draw anchor rectangle
        anchor_rect = patches.Rectangle(
            (anchor_x1, anchor_y1), anchor_x2 - anchor_x1, anchor_y2 - anchor_y1,
            linewidth=2, edgecolor='white', facecolor='black', alpha=0.2
        )
        ax.add_patch(anchor_rect)
        
        # Draw anchor center
        ax.plot(anchor_center_x, anchor_center_y, 'ko', markersize=6)
        
        # Draw arrows for horizontal relationship
        if h_relation == 'left':
            # Anchor is left of main area
            arrow = patches.FancyArrowPatch(
                (anchor_center_x, anchor_center_y), 
                (main_center_x, anchor_center_y),
                connectionstyle="arc3,rad=0.2", 
                arrowstyle="-|>", 
                color=h_color, 
                linewidth=2
            )
            ax.add_patch(arrow)
        else:  # right
            # Anchor is right of main area
            arrow = patches.FancyArrowPatch(
                (anchor_center_x, anchor_center_y), 
                (main_center_x, anchor_center_y),
                connectionstyle="arc3,rad=-0.2", 
                arrowstyle="-|>", 
                color=h_color, 
                linewidth=2
            )
            ax.add_patch(arrow)
        
        # Draw arrows for vertical relationship
        if v_relation == 'top':
            # Anchor is above main area
            arrow = patches.FancyArrowPatch(
                (anchor_center_x, anchor_center_y), 
                (anchor_center_x, main_center_y),
                connectionstyle="arc3,rad=0.2", 
                arrowstyle="-|>", 
                color=v_color, 
                linewidth=2
            )
            ax.add_patch(arrow)
        else:  # bottom
            # Anchor is below main area
            arrow = patches.FancyArrowPatch(
                (anchor_center_x, anchor_center_y), 
                (anchor_center_x, main_center_y),
                connectionstyle="arc3,rad=-0.2", 
                arrowstyle="-|>", 
                color=v_color, 
                linewidth=2
            )
            ax.add_patch(arrow)
        
        # Add text label with index
        ax.text(
            anchor_x1, anchor_y1 - 5, 
            f"#{i}", 
            color='white', fontsize=10, 
            bbox=dict(facecolor='black', alpha=0.7)
        )
    
    # Add legend
    handles = [
        patches.Patch(color='green', alpha=0.5, label="Main Area"),
        patches.Patch(color='black', alpha=0.5, label="Anchor Point"),
        patches.Patch(color='orange', alpha=0.7, label="Left Relation"),
        patches.Patch(color='purple', alpha=0.7, label="Right Relation"),
        patches.Patch(color='red', alpha=0.7, label="Top Relation"),
        patches.Patch(color='blue', alpha=0.7, label="Bottom Relation"),
    ]
    ax.legend(handles=handles, loc='lower right')
    
    ax.set_title("Anchor Point Relationships to Main Area", fontsize=14)
    ax.axis('off')
    
    # Save the figure
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{timestamp}_anchor_relationships.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved anchor relationships visualization")

def visualize_reconstruction_simulation(
    anchor_points: List[Dict[str, Any]],
    main_area: List[float],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize a simulation of the reconstruction process.
    
    Args:
        anchor_points: List of anchor point dictionaries
        main_area: Main area bounding box
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    # Create a figure with 2x2 grid: original, h-constraints, v-constraints, final
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("Main Area Reconstruction Simulation", fontsize=16)
    
    # Extract dimensions
    img_width, img_height = original_image.size
    
    # Original image with main area
    axes[0, 0].imshow(original_image)
    main_x1, main_y1, main_x2, main_y2 = main_area
    main_rect = patches.Rectangle(
        (main_x1, main_y1), main_x2 - main_x1, main_y2 - main_y1,
        linewidth=3, edgecolor='green', facecolor='green', alpha=0.3
    )
    axes[0, 0].add_patch(main_rect)
    axes[0, 0].set_title("Original Main Area", fontsize=12)
    axes[0, 0].axis('off')
    
    # Horizontal constraints visualization
    axes[0, 1].imshow(original_image)
    # Initialize with image bounds and shrink based on constraints
    left_bound = 0
    right_bound = img_width
    
    # Draw anchor points
    for i, anchor in enumerate(anchor_points):
        anchor_x1, anchor_y1, anchor_x2, anchor_y2 = anchor["bbox"]
        h_relation = anchor["horizontal_relation"]
        
        # Draw anchor rectangle (semi-transparent)
        anchor_rect = patches.Rectangle(
            (anchor_x1, anchor_y1), anchor_x2 - anchor_x1, anchor_y2 - anchor_y1,
            linewidth=1, edgecolor='white', facecolor='gray', alpha=0.2
        )
        axes[0, 1].add_patch(anchor_rect)
        
        # Apply constraints with padding
        padding = img_width * 0.05
        if h_relation == 'left':
            potential_bound = anchor_x2 + padding
            if potential_bound > left_bound:
                left_bound = potential_bound
                # Draw vertical line showing constraint
                axes[0, 1].axvline(x=left_bound, color='orange', linestyle='--', linewidth=2)
                # Add label
                axes[0, 1].text(
                    left_bound + 5, img_height - 20, 
                    f"Left bound from #{i}", 
                    color='black', fontsize=8, 
                    bbox=dict(facecolor='orange', alpha=0.7)
                )
        else:  # right
            potential_bound = anchor_x1 - padding
            if potential_bound < right_bound:
                right_bound = potential_bound
                # Draw vertical line showing constraint
                axes[0, 1].axvline(x=right_bound, color='purple', linestyle='--', linewidth=2)
                # Add label
                axes[0, 1].text(
                    right_bound - 100, img_height - 20, 
                    f"Right bound from #{i}", 
                    color='black', fontsize=8, 
                    bbox=dict(facecolor='purple', alpha=0.7)
                )
    
    # Highlight the resulting horizontal region
    h_rect = patches.Rectangle(
        (left_bound, 0), right_bound - left_bound, img_height,
        linewidth=0, facecolor='yellow', alpha=0.15
    )
    axes[0, 1].add_patch(h_rect)
    axes[0, 1].set_title("Horizontal Constraints", fontsize=12)
    axes[0, 1].axis('off')
    
    # Vertical constraints visualization
    axes[1, 0].imshow(original_image)
    # Initialize with image bounds and shrink based on constraints
    top_bound = 0
    bottom_bound = img_height
    
    # Draw anchor points
    for i, anchor in enumerate(anchor_points):
        anchor_x1, anchor_y1, anchor_x2, anchor_y2 = anchor["bbox"]
        v_relation = anchor["vertical_relation"]
        
        # Draw anchor rectangle (semi-transparent)
        anchor_rect = patches.Rectangle(
            (anchor_x1, anchor_y1), anchor_x2 - anchor_x1, anchor_y2 - anchor_y1,
            linewidth=1, edgecolor='white', facecolor='gray', alpha=0.2
        )
        axes[1, 0].add_patch(anchor_rect)
        
        # Apply constraints with padding
        padding = img_height * 0.05
        if v_relation == 'top':
            potential_bound = anchor_y2 + padding
            if potential_bound > top_bound:
                top_bound = potential_bound
                # Draw horizontal line showing constraint
                axes[1, 0].axhline(y=top_bound, color='red', linestyle='--', linewidth=2)
                # Add label
                axes[1, 0].text(
                    5, top_bound + 15, 
                    f"Top bound from #{i}", 
                    color='black', fontsize=8, 
                    bbox=dict(facecolor='red', alpha=0.7)
                )
        else:  # bottom
            potential_bound = anchor_y1 - padding
            if potential_bound < bottom_bound:
                bottom_bound = potential_bound
                # Draw horizontal line showing constraint
                axes[1, 0].axhline(y=bottom_bound, color='blue', linestyle='--', linewidth=2)
                # Add label
                axes[1, 0].text(
                    5, bottom_bound - 15, 
                    f"Bottom bound from #{i}", 
                    color='black', fontsize=8, 
                    bbox=dict(facecolor='blue', alpha=0.7)
                )
    
    # Highlight the resulting vertical region
    v_rect = patches.Rectangle(
        (0, top_bound), img_width, bottom_bound - top_bound,
        linewidth=0, facecolor='yellow', alpha=0.15
    )
    axes[1, 0].add_patch(v_rect)
    axes[1, 0].set_title("Vertical Constraints", fontsize=12)
    axes[1, 0].axis('off')
    
    # Final reconstruction visualization
    axes[1, 1].imshow(original_image)
    
    # Draw all constraints
    axes[1, 1].axvline(x=left_bound, color='orange', linestyle=':', linewidth=1)
    axes[1, 1].axvline(x=right_bound, color='purple', linestyle=':', linewidth=1)
    axes[1, 1].axhline(y=top_bound, color='red', linestyle=':', linewidth=1)
    axes[1, 1].axhline(y=bottom_bound, color='blue', linestyle=':', linewidth=1)
    
    # Draw original main area for comparison
    main_rect = patches.Rectangle(
        (main_x1, main_y1), main_x2 - main_x1, main_y2 - main_y1,
        linewidth=2, edgecolor='green', facecolor='green', alpha=0.2
    )
    axes[1, 1].add_patch(main_rect)
    
    # Draw reconstructed main area
    recon_rect = patches.Rectangle(
        (left_bound, top_bound), right_bound - left_bound, bottom_bound - top_bound,
        linewidth=3, edgecolor='cyan', facecolor='cyan', alpha=0.3
    )
    axes[1, 1].add_patch(recon_rect)
    
    # Add legend
    handles = [
        patches.Patch(color='green', alpha=0.5, label="Original Main Area"),
        patches.Patch(color='cyan', alpha=0.5, label="Reconstructed Area"),
    ]
    axes[1, 1].legend(handles=handles, loc='lower right')
    
    # Calculate and display IOU
    def calculate_iou(box1, box2):
        # Calculate intersection area
        x1_i = max(box1[0], box2[0])
        y1_i = max(box1[1], box2[1])
        x2_i = min(box1[2], box2[2])
        y2_i = min(box1[3], box2[3])
        
        if x2_i < x1_i or y2_i < y1_i:
            return 0.0  # No intersection
            
        intersection = (x2_i - x1_i) * (y2_i - y1_i)
        
        # Calculate union area
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = box1_area + box2_area - intersection
        
        return intersection / union if union > 0 else 0.0
    
    reconstructed_box = [left_bound, top_bound, right_bound, bottom_bound]
    iou = calculate_iou(main_area, reconstructed_box)
    
    # Add IOU and dimension metrics
    original_width = main_x2 - main_x1
    original_height = main_y2 - main_y1
    recon_width = right_bound - left_bound
    recon_height = bottom_bound - top_bound
    
    metrics_text = (
        f"IOU: {iou:.2f}\n"
        f"Original: {original_width:.0f}x{original_height:.0f}px\n"
        f"Reconstructed: {recon_width:.0f}x{recon_height:.0f}px"
    )
    
    axes[1, 1].text(
        0.05, 0.05, metrics_text,
        transform=axes[1, 1].transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(facecolor='white', alpha=0.7)
    )
    
    axes[1, 1].set_title("Reconstructed Main Area", fontsize=12)
    axes[1, 1].axis('off')
    
    # Save the figure
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / f"{timestamp}_reconstruction_simulation.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved reconstruction simulation visualization")

def test_anchor_based_detector(use_viewport=False):
    """
    Test the AnchorBasedMainAreaDetector to verify its functionality and visualize results.
    
    Args:
        use_viewport: Whether to crop screenshots according to viewport rendering area
    """
    logger.info("Starting AnchorBasedMainAreaDetector test...")
    
    try:
        # Ensure output directory and get timestamp
        timestamp = ensure_output_dir()
        
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
        
        # Get a sample main area (you would normally get this from user input or another detector)
        # For this test, we'll use a hardcoded main area covering the central portion of the screen
        sample_model = test_data.omniparser_result_models[0]
        image_path = sample_model.omniparser_result.original_image_path
        img = Image.open(image_path).convert("RGB")
        img_width, img_height = img.size
        
        # Define a sample main area (adjust as needed)
        main_area = [
            img_width * 0.2,  # x1 (20% from left)
            img_height * 0.2,  # y1 (20% from top)
            img_width * 0.8,   # x2 (20% from right)
            img_height * 0.8,  # y2 (20% from bottom)
        ]
        
        # Create a temporary directory for the model
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize the detector
            detector = AnchorBasedMainAreaDetector(
                max_anchor_points=8,
                max_main_area_references=4
            )
            
            # Train the detector
            logger.info("Training the detector...")
            training_result = detector.train(
                result_model=sample_model,
                frames=test_data.omniparser_result_models,
                main_area=main_area,
                save_dir=temp_dir
            )
            
            # Verify training result
            if not training_result["success"]:
                logger.error("Training failed.")
                return
                
            logger.info(f"Training successful. Found {len(training_result['anchor_points'])} anchor points.")
            
            # Load and test the runtime detector
            runtime_detector = AnchorBasedMainAreaDetectorRuntime()
            
            # Don't run full detection as part of this test, but we'll visualize the trained model
            # Create visualizations
            logger.info("Creating visualizations...")
            
            # 1. Main area references visualization
            # Get the main area references from the training result
            results_list = OmniParserResultModelList(
                omniparser_result_models=test_data.omniparser_result_models,
                project_uuid="",  # Placeholder
                command_uuid=""   # Placeholder
            )
            main_area_references = detector._extract_main_area_references(
                results_list, main_area
            )
            visualize_main_area_references(main_area_references, main_area, img, timestamp)
            
            # 2. Anchor points visualization
            anchor_points = training_result["anchor_points"]
            visualize_anchor_points(anchor_points, img, timestamp)
            
            # 3. Anchor relationships visualization
            visualize_anchor_relationships(anchor_points, main_area, img, timestamp)
            
            # 4. Reconstruction simulation
            visualize_reconstruction_simulation(anchor_points, main_area, img, timestamp)
            
            # Log success and list visualization files
            vis_files = list(OUTPUT_DIR.glob(f"{timestamp}_*.png"))
            logger.info(f"Test completed. Created {len(vis_files)} visualization files:")
            for file in vis_files:
                logger.info(f"  - {file.name}")
    
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)

if __name__ == "__main__":
    # Add command line argument parsing for viewport
    parser = argparse.ArgumentParser(description="Test the AnchorBasedMainAreaDetector with visualizations")
    parser.add_argument("--viewport", action="store_true", help="Use viewport for cropping screenshots")
    args = parser.parse_args()
    
    test_anchor_based_detector(use_viewport=args.viewport) 