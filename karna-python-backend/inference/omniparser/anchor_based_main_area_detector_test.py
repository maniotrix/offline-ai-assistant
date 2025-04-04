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

def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union between two bounding boxes.
    
    Args:
        box1: First bounding box [x1, y1, x2, y2]
        box2: Second bounding box [x1, y1, x2, y2]
        
    Returns:
        IoU value between 0 and 1
    """
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
    fig.savefig(OUTPUT_DIR / f"_main_area_references.png", dpi=150)
    fig2.savefig(OUTPUT_DIR / f"_main_area_location.png", dpi=150)
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
    fig.savefig(OUTPUT_DIR / f"_anchor_points.png", dpi=150)
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
    fig2.savefig(OUTPUT_DIR / f"_anchor_patches.png", dpi=150)
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
    fig.savefig(OUTPUT_DIR / f"_anchor_relationships.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved anchor relationships visualization")

def visualize_reconstruction_simulation_only_anchors(
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
    iou = calculate_iou(main_area, [left_bound, top_bound, right_bound, bottom_bound])
    
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
    fig.savefig(OUTPUT_DIR / f"_reconstruction_simulation_only_anchors.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved reconstruction simulation visualization")

def visualize_direct_matching(
    main_area_references: List[Dict[str, Any]],
    main_area: List[float],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize the direct matching process with main area references.
    
    Args:
        main_area_references: List of main area reference dictionaries
        main_area: Main area bounding box
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    # Create a figure with a 2x2 grid showing the direct matching process
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("Direct Matching with Main Area References", fontsize=16)
    
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
    
    # Reference patch to match
    if len(main_area_references) > 0:
        # Use the first reference as an example
        ref = main_area_references[0]
        axes[0, 1].imshow(ref["patch"])
        axes[0, 1].set_title(f"Reference Patch (Frame {ref['frame_index']})", fontsize=12)
        axes[0, 1].axis('off')
    else:
        axes[0, 1].text(0.5, 0.5, "No reference patches available", 
                        ha='center', fontsize=12)
        axes[0, 1].axis('off')
    
    # Illustration of embedding comparison process
    axes[1, 0].imshow(original_image, alpha=0.6)  # Semi-transparent original image
    
    # Create a heatmap-like overlay to represent similarity comparison
    # This is just a visualization representation of the process
    img_width, img_height = original_image.size
    heatmap = np.zeros((img_height, img_width))
    
    # Create a Gaussian peak centered at the main area
    x = np.arange(0, img_width, 1)
    y = np.arange(0, img_height, 1)
    X, Y = np.meshgrid(x, y)
    
    # Center of the main area
    center_x = (main_x1 + main_x2) / 2
    center_y = (main_y1 + main_y2) / 2
    
    # Create the heatmap with a peak at the center of the main area
    heatmap = np.exp(-0.5 * (((X - center_x) / (img_width * 0.1)) ** 2 + 
                             ((Y - center_y) / (img_height * 0.1)) ** 2))
    
    # Display the heatmap
    heatmap_display = axes[1, 0].imshow(heatmap, cmap='hot', alpha=0.5)
    
    # Add a colorbar
    cbar = plt.colorbar(heatmap_display, ax=axes[1, 0], orientation='vertical', shrink=0.7)
    cbar.set_label('Embedding Similarity')
    
    axes[1, 0].set_title("Similarity Matching Process", fontsize=12)
    axes[1, 0].axis('off')
    
    # Direct match result visualization
    axes[1, 1].imshow(original_image)
    
    # Show the match result - assuming success for visualization
    main_rect = patches.Rectangle(
        (main_x1, main_y1), main_x2 - main_x1, main_y2 - main_y1,
        linewidth=3, edgecolor='magenta', facecolor='magenta', alpha=0.3
    )
    axes[1, 1].add_patch(main_rect)
    
    # Add a text box explaining the process
    explanation = (
        "1. Extract patch from current screen\n"
        "2. Generate embedding\n"
        "3. Compare with reference embeddings\n"
        "4. If similarity ≥ 0.8, use directly\n"
        "5. Else fall back to anchor reconstruction"
    )
    
    axes[1, 1].text(
        0.05, 0.05, explanation,
        transform=axes[1, 1].transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(facecolor='white', alpha=0.7)
    )
    
    axes[1, 1].set_title("Direct Match Result", fontsize=12)
    axes[1, 1].axis('off')
    
    # Save the figure
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / f"_direct_matching.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved direct matching visualization")

def visualize_detection_workflow(
    main_area_references: List[Dict[str, Any]],
    anchor_points: List[Dict[str, Any]],
    main_area: List[float],
    original_image: Image.Image,
    timestamp: str
):
    """
    Visualize the complete detection workflow showing both direct matching and anchor-based methods.
    
    Args:
        main_area_references: List of main area reference dictionaries
        anchor_points: List of anchor point dictionaries
        main_area: Main area bounding box
        original_image: Original image for reference
        timestamp: Timestamp for filename
    """
    # Create a figure with flowchart style showing the detection pipeline
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Hide the actual axis
    ax.axis('off')
    
    # Set up the canvas for a flowchart-style visualization
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Add title
    ax.text(50, 95, "Detection Workflow", ha='center', fontsize=20, fontweight='bold')
    
    # Step 1: Input image
    img_box = patches.Rectangle((10, 75), 20, 15, linewidth=2, edgecolor='black', facecolor='lightblue', alpha=0.5)
    ax.add_patch(img_box)
    ax.text(20, 82.5, "Input Image", ha='center', fontsize=12)
    
    # Arrow down
    arrow1 = patches.FancyArrowPatch((20, 75), (20, 65), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow1)
    
    # Step 2: Load Model
    model_box = patches.Rectangle((10, 50), 20, 15, linewidth=2, edgecolor='black', facecolor='lightgreen', alpha=0.5)
    ax.add_patch(model_box)
    ax.text(20, 57.5, "Load Model", ha='center', fontsize=12)
    
    # Arrow down
    arrow2 = patches.FancyArrowPatch((20, 50), (20, 40), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow2)
    
    # Step 3: Direct Matching (left branch)
    direct_box = patches.Rectangle((5, 25), 15, 15, linewidth=2, edgecolor='black', facecolor='yellow', alpha=0.5)
    ax.add_patch(direct_box)
    ax.text(12.5, 32.5, "Direct\nMatching", ha='center', fontsize=10)
    
    # Step 3 alternative: Anchor Matching (right branch)
    anchor_box = patches.Rectangle((30, 25), 15, 15, linewidth=2, edgecolor='black', facecolor='orange', alpha=0.5)
    ax.add_patch(anchor_box)
    ax.text(37.5, 32.5, "Anchor\nReconstruction", ha='center', fontsize=10)
    
    # Branch arrows
    arrow3a = patches.FancyArrowPatch((20, 40), (12.5, 40), arrowstyle='-', linewidth=2, color='black')
    ax.add_patch(arrow3a)
    arrow3b = patches.FancyArrowPatch((12.5, 40), (12.5, 40), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow3b)
    arrow3c = patches.FancyArrowPatch((20, 40), (37.5, 40), arrowstyle='-', linewidth=2, color='black')
    ax.add_patch(arrow3c)
    arrow3d = patches.FancyArrowPatch((37.5, 40), (37.5, 40), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow3d)
    
    # Decision text
    ax.text(20, 45, "First try", ha='center', fontsize=10)
    ax.text(37.5, 45, "If direct match fails", ha='center', fontsize=10)
    
    # Arrows down
    arrow4a = patches.FancyArrowPatch((12.5, 25), (12.5, 15), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow4a)
    arrow4b = patches.FancyArrowPatch((37.5, 25), (37.5, 15), arrowstyle='->', linewidth=2, color='black')
    ax.add_patch(arrow4b)
    
    # Step 4: Results
    result_box1 = patches.Rectangle((5, 0), 15, 15, linewidth=2, edgecolor='black', facecolor='lightcoral', alpha=0.5)
    ax.add_patch(result_box1)
    ax.text(12.5, 7.5, "Direct\nMatch Result", ha='center', fontsize=10)
    
    result_box2 = patches.Rectangle((30, 0), 15, 15, linewidth=2, edgecolor='black', facecolor='lightcoral', alpha=0.5)
    ax.add_patch(result_box2)
    ax.text(37.5, 7.5, "Anchor\nReconstruction\nResult", ha='center', fontsize=10)
    
    # Right side: Visual examples from actual implementation
    # Direct matching example (thumbnail)
    if len(main_area_references) > 0:
        ref = main_area_references[0]
        ref_patch = ref["patch"]
        ref_height, ref_width = ref_patch.size[1], ref_patch.size[0]
        # Add a reference patch example
        ax_ref = fig.add_axes([0.6, 0.75, 0.15, 0.15])
        ax_ref.imshow(ref_patch)
        ax_ref.set_title("Reference Patch Example", fontsize=10)
        ax_ref.axis('off')
    
    # Anchor points example (thumbnail)
    if len(anchor_points) > 0:
        ax_anchor = fig.add_axes([0.6, 0.5, 0.15, 0.15])
        ax_anchor.imshow(original_image)
        # Draw a few sample anchors
        for i, anchor in enumerate(anchor_points[:3]):
            x1, y1, x2, y2 = anchor["bbox"]
            rect = patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2, edgecolor='red', facecolor='none'
            )
            ax_anchor.add_patch(rect)
        ax_anchor.set_title("Anchor Points Example", fontsize=10)
        ax_anchor.axis('off')
    
    # Direct matching result (thumbnail)
    ax_direct = fig.add_axes([0.6, 0.25, 0.15, 0.15])
    ax_direct.imshow(original_image)
    # Draw main area as would be found by direct matching
    main_x1, main_y1, main_x2, main_y2 = main_area
    direct_rect = patches.Rectangle(
        (main_x1, main_y1), main_x2 - main_x1, main_y2 - main_y1,
        linewidth=2, edgecolor='magenta', facecolor='magenta', alpha=0.3
    )
    ax_direct.add_patch(direct_rect)
    ax_direct.set_title("Direct Matching Result", fontsize=10)
    ax_direct.axis('off')
    
    # Anchor reconstruction result (thumbnail)
    ax_recon = fig.add_axes([0.8, 0.25, 0.15, 0.15])
    ax_recon.imshow(original_image)
    # Draw main area as reconstructed from anchors (with slight variation for visualization)
    # Add a small random variation for illustration
    recon_x1 = main_x1 * 0.95
    recon_y1 = main_y1 * 0.95
    recon_x2 = main_x2 * 1.05
    recon_y2 = main_y2 * 1.05
    recon_rect = patches.Rectangle(
        (recon_x1, recon_y1), recon_x2 - recon_x1, recon_y2 - recon_y1,
        linewidth=2, edgecolor='cyan', facecolor='cyan', alpha=0.3
    )
    ax_recon.add_patch(recon_rect)
    ax_recon.set_title("Anchor Reconstruction", fontsize=10)
    ax_recon.axis('off')
    
    # Add explanation text
    explanation = (
        "Detection Workflow:\n\n"
        "1. Load the input image\n"
        "2. Load the detection model\n"
        "3. First try direct matching with main area references\n"
        "   - Compare current screen with saved reference patches\n"
        "   - If similarity ≥ 0.8, use the matched main area\n\n"
        "4. If direct matching fails, use anchor-based reconstruction\n"
        "   - Find UI elements matching saved anchor points\n"
        "   - Apply directional constraints from each anchor\n"
        "   - Reconstruct main area using these constraints\n\n"
        "This two-tier approach provides both speed (direct matching)\n"
        "and robustness to content changes (anchor reconstruction)."
    )
    
    ax.text(80, 50, explanation, fontsize=10, va='center',
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=1'))
    
    # Save the figure
    plt.savefig(OUTPUT_DIR / f"_detection_workflow.png", dpi=150)
    plt.close(fig)
    logger.info(f"Saved detection workflow visualization")

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
        
        # Create OmniParserResultModelList once - we'll reuse this
        test_data = get_omniparser_inference_data(screenshot_events)
        
        if not test_data.omniparser_result_models:
            logger.error("No valid models loaded from JSON file.")
            return
            
        logger.info(f"Successfully loaded {len(test_data.omniparser_result_models)} models from JSON file")
        
        # Log frame information
        for i, model in enumerate(test_data.omniparser_result_models):
            logger.info(f"Frame {i}: {model.omniparser_result.original_image_path}")
            logger.info(f"  - Dimensions: {model.omniparser_result.original_image_width}x{model.omniparser_result.original_image_height}")
            logger.info(f"  - Elements: {len(model.parsed_content_results)}")
            
            # Count elements by type and source
            element_types = {}
            element_sources = {}
            for elem in model.parsed_content_results:
                element_types[elem.type] = element_types.get(elem.type, 0) + 1
                element_sources[elem.source] = element_sources.get(elem.source, 0) + 1
            
            logger.info(f"  - Element types: {element_types}")
            logger.info(f"  - Element sources: {element_sources}")
        
        # Get sample model for visualizations
        sample_model = test_data.omniparser_result_models[0]
        image_path = sample_model.omniparser_result.original_image_path
        img = Image.open(image_path).convert("RGB")
        
        # Create a temporary directory for the model
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize the detector
            detector = AnchorBasedMainAreaDetector(
                max_anchor_points=8,
                max_main_area_references=4
            )
            
            # Train the detector - now uses dynamic detector to find main area
            logger.info("Training the detector...")
            logger.info("-" * 50)
            logger.info("TRAINING PHASE")
            logger.info("-" * 50)
            
            training_result = detector.train_with_frames(
                results_list=test_data,
                save_dir=temp_dir
            )
            
            # Verify training result
            if not training_result["success"]:
                logger.error(f"Training failed: {training_result.get('error', 'Unknown error')}")
                return
                
            logger.info(f"Training successful. Found {len(training_result['anchor_points'])} anchor points.")
            logger.info(f"Detected main area: {training_result['main_area']} (source: {training_result['area_source']})")
            
            # Log detailed information about the main area
            main_area = training_result["main_area"]
            main_area_width = main_area[2] - main_area[0]
            main_area_height = main_area[3] - main_area[1]
            logger.info(f"Main area dimensions: {main_area_width}x{main_area_height} pixels")
            logger.info(f"Main area center: ({(main_area[0] + main_area[2])/2}, {(main_area[1] + main_area[3])/2})")
            logger.info(f"Main area relative size: {(main_area_width * main_area_height) / (sample_model.omniparser_result.original_image_width * sample_model.omniparser_result.original_image_height) * 100:.2f}% of screen")
            
            # Log detailed information about each anchor point
            logger.info("-" * 50)
            logger.info("ANCHOR POINTS DETAILS")
            logger.info("-" * 50)
            
            anchor_points = training_result["anchor_points"]
            
            # Count anchor points by direction
            direction_counts = {"top": 0, "bottom": 0, "left": 0, "right": 0}
            for anchor in anchor_points:
                direction = anchor["constraint_direction"]
                direction_counts[direction] += 1
            
            logger.info(f"Anchor points by direction: {direction_counts}")
            
            for i, anchor in enumerate(anchor_points):
                logger.info(f"Anchor #{i}:")
                logger.info(f"  - Element ID: {anchor['element_id']}")
                logger.info(f"  - Element Type: {anchor['element_type']}")
                logger.info(f"  - Source: {anchor['source']}")
                logger.info(f"  - Direction: {anchor['constraint_direction']}")
                logger.info(f"  - Position: {anchor['bbox']}")
                logger.info(f"  - Stability Score: {anchor['stability_score']:.4f}")
                logger.info(f"  - Horizontal Relation: {anchor['horizontal_relation']}")
                logger.info(f"  - Vertical Relation: {anchor['vertical_relation']}")
                
                # Calculate position relative to main area
                anchor_center_x = (anchor['bbox'][0] + anchor['bbox'][2]) / 2
                anchor_center_y = (anchor['bbox'][1] + anchor['bbox'][3]) / 2
                main_center_x = (main_area[0] + main_area[2]) / 2
                main_center_y = (main_area[1] + main_area[3]) / 2
                
                rel_x = (anchor_center_x - main_center_x) / main_area_width
                rel_y = (anchor_center_y - main_center_y) / main_area_height
                
                logger.info(f"  - Relative position to main area center: ({rel_x:.2f}, {rel_y:.2f})")
            
            # Log information about main area references
            main_area_references = detector._extract_main_area_references(
                test_data, main_area
            )
            
            logger.info("-" * 50)
            logger.info("MAIN AREA REFERENCES")
            logger.info("-" * 50)
            
            logger.info(f"Number of main area references: {len(main_area_references)}")
            for i, ref in enumerate(main_area_references):
                logger.info(f"Reference #{i}:")
                logger.info(f"  - Frame index: {ref['frame_index']}")
                logger.info(f"  - Bounding box: {ref['bbox']}")
                
                # Calculate patch dimensions
                patch_width, patch_height = ref['patch'].size
                logger.info(f"  - Patch dimensions: {patch_width}x{patch_height}")
            
            # Load and test the runtime detector
            logger.info("-" * 50)
            logger.info("RUNTIME DETECTION PHASE")
            logger.info("-" * 50)
            
            runtime_detector = AnchorBasedMainAreaDetectorRuntime()
            
            # Test the runtime detector on each frame
            for i, model in enumerate(test_data.omniparser_result_models):
                logger.info(f"Detecting main area in frame {i}...")
                detection_result = runtime_detector.detect(model, temp_dir)
                
                logger.info(f"  - Success: {detection_result['success']}")
                logger.info(f"  - Method: {detection_result.get('method', 'N/A')}")
                logger.info(f"  - Confidence: {detection_result.get('confidence', 0):.4f}")
                logger.info(f"  - Detected main area: {detection_result.get('main_area', 'None')}")
                
                if detection_result.get('method') == 'anchor_reconstruction':
                    logger.info(f"  - Anchors matched: {detection_result.get('anchors_matched', 0)}")
                    
                # Calculate IoU if both main areas are available
                if detection_result.get('main_area') and main_area:
                    iou = calculate_iou(detection_result['main_area'], main_area)
                    logger.info(f"  - IoU with reference main area: {iou:.4f}")
                
                # Skip remaining frames for brevity
                if i >= 2:
                    logger.info("Skipping remaining frames for brevity...")
                    break
            
            # Create visualizations
            logger.info("-" * 50)
            logger.info("CREATING VISUALIZATIONS")
            logger.info("-" * 50)
            
            # 1. Main area references visualization
            visualize_main_area_references(main_area_references, main_area, img, timestamp)
            
            # 2. Direct matching visualization
            visualize_direct_matching(main_area_references, main_area, img, timestamp)
            
            # 3. Anchor points visualization
            visualize_anchor_points(anchor_points, img, timestamp)
            
            # 4. Anchor relationships visualization
            visualize_anchor_relationships(anchor_points, main_area, img, timestamp)
            
            # 5. Reconstruction simulation
            visualize_reconstruction_simulation_only_anchors(anchor_points, main_area, img, timestamp)
            
            # 6. Create a detection workflow visualization showing the full pipeline
            visualize_detection_workflow(main_area_references, anchor_points, main_area, img, timestamp)
            
            # Log success and list visualization files
            vis_files = list(OUTPUT_DIR.glob(f"_*.png"))
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