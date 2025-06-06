import os
import sys
import json
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import io
from pathlib import Path
from config.paths import workspace_dir

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.screen_capture_service import ScreenshotEvent
from inference.cortex_vision.attention_controller_extended import AttentionFieldController

"""
Extended Attention Controller Test
---------------------------------
This file is a copy of the original test_attention_controller.py with additions
for testing future phases:

- Phase 2: Testing and visualizing attention heatmaps
- Phase 3: Testing weighted patch scanning
- Phase 4: Testing ML-enhanced predictions

These test extensions will be added without changing the core testing functionality.
"""

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded JSON file path
JSON_FILE_PATH = r"C:\Users\Prince\Documents\GitHub\Proejct-Karna\offline-ai-assistant\data\chatgpt\883c46f5-c62d-4799-baa1-5e3b12f12e8c\screenshot_events_883c46f5-c62d-4799-baa1-5e3b12f12e8c.json"
OUTPUT_DIR = "attention_visualization_extended"

def load_screenshot_events() -> List[ScreenshotEvent]:
    """
    Load screenshot events from the specified JSON file.
    
    Returns:
        List of ScreenshotEvent objects
    """
    logger.info(f"Loading screenshot events from JSON file: {JSON_FILE_PATH}")
    
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading JSON file: {str(e)}")
        return []
    
    if not events_data or not isinstance(events_data, list):
        logger.error("JSON file does not contain a list of screenshot events")
        return []
    
    # Convert JSON data to ScreenshotEvent objects
    screenshot_events = []
    for event_dict in events_data:
        if "screenshot_path" in event_dict:
            event_dict["screenshot_path"] = str(workspace_dir / event_dict["screenshot_path"]) # type: ignore
        # Convert ISO format string back to datetime
        if 'timestamp' in event_dict and isinstance(event_dict['timestamp'], str):
            try:
                event_dict['timestamp'] = datetime.fromisoformat(event_dict['timestamp'])
            except ValueError:
                continue
        
        # Create ScreenshotEvent object
        try:
            event = ScreenshotEvent(**event_dict)
            # Only add events with mouse coordinates
            if event.mouse_x is not None and event.mouse_y is not None:
                # Make sure screenshot path is valid
                if event.screenshot_path and os.path.exists(event.screenshot_path):
                    screenshot_events.append(event)
                else:
                    logger.warning(f"Skipping event with invalid screenshot path: {event.screenshot_path}")
        except Exception as e:
            logger.warning(f"Skipping invalid event: {str(e)}")
    
    # Sort events by timestamp
    screenshot_events.sort(key=lambda e: e.timestamp)
    
    logger.info(f"Loaded {len(screenshot_events)} valid mouse events with screenshots")
    return screenshot_events

def visualize_attention_fields(events: List[ScreenshotEvent]) -> None:
    """
    Visualize attention fields for each mouse event by drawing directly on the screenshots.
    Also shows predicted next attention area based on movement direction.
    
    Args:
        events: List of ScreenshotEvent objects with mouse coordinates and valid screenshot paths
    """
    if not events:
        logger.warning("No events to visualize")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create controller
    controller = AttentionFieldController()
    
    # Process each event
    for i, event in enumerate(events):
        # Skip if screenshot doesn't exist
        if not event.screenshot_path or not os.path.exists(event.screenshot_path):
            logger.warning(f"Skipping event {i+1}: Screenshot not found at {event.screenshot_path}")
            continue
            
        # Add current click to controller
        controller.add_click_from_event(event)
        
        # Get current attention field
        current_field = controller.get_current_attention_field()
        
        # Get predicted next attention field based on movement direction
        next_field = controller.predict_next_attention_field()
        
        # Create a figure with the screenshot as background
        plt.figure(figsize=(15, 10))
        
        # Load screenshot image
        try:
            img = plt.imread(event.screenshot_path)
            plt.imshow(img)
            
            # Get image dimensions for plot limits
            img_height, img_width = img.shape[0], img.shape[1]
            plt.xlim(0, img_width)
            plt.ylim(img_height, 0)  # Invert y-axis to match image coordinates
            
            # Draw current attention field as a solid red rectangle
            current_rect = patches.Rectangle(
                (current_field.x, current_field.y),
                current_field.width, current_field.height,
                linewidth=3, edgecolor='r', facecolor='none', alpha=0.7,
                label=f"Current Attention (conf={current_field.confidence:.2f})"
            )
            plt.gca().add_patch(current_rect)
            
            # Draw predicted next attention field as a dashed blue rectangle if available
            if next_field:
                next_rect = patches.Rectangle(
                    (next_field.x, next_field.y),
                    next_field.width, next_field.height,
                    linewidth=2, edgecolor='b', facecolor='none', alpha=0.5,
                    linestyle='--',
                    label=f"Predicted Next (dir={next_field.direction}, conf={next_field.confidence:.2f})"
                )
                plt.gca().add_patch(next_rect)
                
                # Draw an arrow indicating movement direction if available
                if next_field.direction and i > 0:
                    center_x, center_y = current_field.center
                    arrow_length = min(current_field.width, current_field.height) * 0.3
                    
                    dx, dy = 0, 0
                    if next_field.direction == 'right':
                        dx = arrow_length
                    elif next_field.direction == 'left':
                        dx = -arrow_length
                    elif next_field.direction == 'down':
                        dy = arrow_length
                    elif next_field.direction == 'up':
                        dy = -arrow_length
                    
                    if dx != 0 or dy != 0:
                        plt.arrow(center_x, center_y, dx, dy, 
                                 head_width=15, head_length=15, 
                                 fc='g', ec='g', alpha=0.7,
                                 label="Movement Direction")
            
            # Plot all clicks so far
            for j, prev_event in enumerate(events[:i+1]):
                x, y = prev_event.mouse_x, prev_event.mouse_y
                if j == i:  # Current click (red)
                    plt.plot(x, y, 'ro', markersize=12, label='Current Click')
                else:  # Previous clicks (blue)
                    plt.plot(x, y, 'bo', markersize=7, alpha=0.6)
            
            # Add informative title
            event_time = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            click_count = i + 1
            direction_info = f", Predicted Direction: {next_field.direction}" if next_field and next_field.direction else ""
            plt.title(f"Attention Field after Click {click_count}/{len(events)} ({event_time}){direction_info}", fontsize=14)
            
            # Add legend
            plt.legend(loc='upper right', fontsize=12)
            
            # Add information about attention context in text box
            attention_info = [
                f"Current Click: ({event.mouse_x}, {event.mouse_y})",
                f"Attention Field: ({current_field.x}, {current_field.y}, w={current_field.width}, h={current_field.height})",
                f"Confidence: {current_field.confidence:.2f}"
            ]
            
            if next_field:
                attention_info.extend([
                    f"Direction: {next_field.direction}",
                    f"Next Field: ({next_field.x}, {next_field.y}, w={next_field.width}, h={next_field.height})",
                    f"Next Confidence: {next_field.confidence:.2f}"
                ])
            
            plt.gcf().text(0.02, 0.02, '\n'.join(attention_info), fontsize=10, 
                        bbox=dict(facecolor='white', alpha=0.7))
            
            # Phase 2: Generate and visualize the attention heatmap as a subplot
            if len(controller.click_history) >= 2:
                # Create a smaller axis for the heatmap in the lower right corner
                heatmap_ax = plt.gcf().add_axes([0.75, 0.05, 0.2, 0.2])
                
                # Get a heatmap from the controller (placeholder for now)
                attention_heatmap = controller.generate_attention_heatmap((50, 50))
                
                # Display the heatmap (this will be an empty heatmap in Phase 1)
                heatmap_ax.imshow(attention_heatmap, 
                                cmap=LinearSegmentedColormap.from_list('attention_cmap', 
                                                                    ['blue', 'cyan', 'yellow', 'red']),
                                alpha=0.7, 
                                extent=[0, controller.screen_width, controller.screen_height, 0])
                heatmap_ax.set_title("Attention Heatmap", fontsize=8)
                heatmap_ax.axis('off')
            
            # Save the figure
            output_path = os.path.join(OUTPUT_DIR, f"attention_field_{i+1:03d}.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Saved visualization {i+1}/{len(events)} to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to process event {i+1}: {str(e)}")
            plt.close()

def visualize_patches_with_priorities(events: List[ScreenshotEvent], sequence_index: int = -1):
    """
    PHASE 3: Visualize mock UI patches with their scanning priorities.
    
    Args:
        events: List of screenshot events
        sequence_index: Index to select which event to visualize (-1 for last)
    """
    # This will be completed in Phase 3
    # For now, just create a placeholder visualization
    
    if not events:
        logger.warning("No events to visualize for patch priorities")
        return
    
    # Select the event to use
    if sequence_index < 0:
        event = events[len(events) + sequence_index]  # -1 gives the last event
    else:
        event = events[min(sequence_index, len(events) - 1)]
    
    if not event.screenshot_path or not os.path.exists(event.screenshot_path):
        logger.warning(f"Cannot visualize patches: Screenshot not found at {event.screenshot_path}")
        return
    
    # Create controller and process all events up to the selected one
    controller = AttentionFieldController()
    for e in events[:events.index(event) + 1]:
        controller.add_click_from_event(e)
    
    # Create a figure for visualization
    plt.figure(figsize=(15, 10))
    
    # Load screenshot image
    try:
        img = plt.imread(event.screenshot_path)
        plt.imshow(img)
        
        # Get image dimensions for plot limits
        img_height, img_width = img.shape[0], img.shape[1]
        plt.xlim(0, img_width)
        plt.ylim(img_height, 0)  # Invert y-axis to match image coordinates
        
        # Generate some mock UI patches for demonstration
        # (In real Phase 3, these would come from UI element detection)
        mock_patches = [
            {'bbox': (event.mouse_x - 100, event.mouse_y - 50, 200, 100), 'id': 1},
            {'bbox': (event.mouse_x + 150, event.mouse_y - 100, 300, 150), 'id': 2},
            {'bbox': (event.mouse_x - 250, event.mouse_y + 100, 150, 80), 'id': 3},
            {'bbox': (event.mouse_x + 50, event.mouse_y + 150, 250, 120), 'id': 4},
        ]
        
        # Get priorities for patches using the controller
        # (This returns dummy values in Phase 1, real values in Phase 3)
        priorities = controller.get_patch_scanning_priorities(mock_patches)
        
        # Draw patches with colors based on their priorities
        for i, (patch, priority) in enumerate(zip(mock_patches, priorities)):
            x, y, w, h = patch['bbox']
            # Use priority to determine alpha (transparency)
            rect = patches.Rectangle(
                (x, y), w, h,
                linewidth=2,
                edgecolor='purple',
                facecolor='purple',
                alpha=min(0.1 + priority * 0.4, 0.5),  # Vary transparency by priority
                label=f"Patch {patch['id']} (priority={priority:.2f})"
            )
            plt.gca().add_patch(rect)
            plt.text(x + w/2, y + h/2, f"{patch['id']}: {priority:.2f}", 
                   ha='center', va='center', color='white', fontsize=10)
        
        plt.title("UI Patch Scanning Priorities (Phase 3 Preview)", fontsize=14)
        plt.legend(loc='upper right')
        
        # Save the figure
        output_path = os.path.join(OUTPUT_DIR, "patch_priorities_preview.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved patch priorities preview to {output_path}")
        
    except Exception as e:
        logger.error(f"Failed to create patch priorities visualization: {str(e)}")
        plt.close()

def main():
    """Main function to visualize attention fields for mouse events by drawing on screenshots."""
    # Load events from JSON file
    events = load_screenshot_events()
    
    if not events:
        logger.error("No valid mouse events with screenshots found")
        return
    
    # Visualize attention fields
    visualize_attention_fields(events)
    
    # Phase 3 preview: Visualize UI patch scanning priorities
    visualize_patches_with_priorities(events)
    
    logger.info(f"Completed visualization of attention fields for {len(events)} events")
    logger.info(f"Output saved to directory: {os.path.abspath(OUTPUT_DIR)}")
    logger.info("Note: Phase 2-4 features are placeholders and will be implemented in future updates")

if __name__ == "__main__":
    main() 