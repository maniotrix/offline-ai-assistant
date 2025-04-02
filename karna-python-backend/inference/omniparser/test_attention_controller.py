import os
import sys
import json
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import io
from pathlib import Path
from config.paths import workspace_dir

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.screen_capture_service import ScreenshotEvent
from inference.omniparser.attention_controller import AttentionFieldController

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded JSON file path
JSON_FILE_PATH = r"C:\Users\Prince\Documents\GitHub\Proejct-Karna\offline-ai-assistant\data\chatgpt\883c46f5-c62d-4799-baa1-5e3b12f12e8c\screenshot_events_883c46f5-c62d-4799-baa1-5e3b12f12e8c.json"
OUTPUT_DIR = "attention_visualization"

def print_interpretation_guide():
    """
    Print a user guide explaining how to interpret the attention field test results.
    """
    guide = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     ATTENTION FIELD ANALYSIS: USER GUIDE                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

This test visualizes how the AttentionFieldController tracks and predicts user attention
based on mouse click sequences. Below is a guide to help you interpret the results:

KEY CONCEPTS:
------------
• Top-Left Corner: (x, y) coordinates where the attention field begins
• Dimensions: Width × Height of the attention field in pixels
• Center Point: The focal point of the attention field (calculated from corner + dimensions/2)
• Confidence Score: How certain the controller is about this attention area (0-1 scale)
• Movement Direction: The inferred direction based on user's click patterns (UP/DOWN/LEFT/RIGHT)

INTERPRETING CONSOLE OUTPUT:
-------------------------
For each mouse click event, you'll see:

🔍 ATTENTION EVENT #N
  Shows which event in the sequence is being analyzed

⏰ Time: [timestamp]
🖱️ Mouse Click: (x, y)
  The exact time and position of the current mouse click

📌 CURRENT ATTENTION FIELD:
  • Top-Left Corner: (x, y)
  • Dimensions: width × height pixels
  • Center Point: (center_x, center_y)
  • Confidence Score: 0.XX / 1.00
  Details about where the system believes user attention is currently focused

🔮 PREDICTED NEXT ATTENTION:
  • Movement Direction: [DIRECTION]
  • Top-Left Corner: (x, y)
  • Dimensions: width × height pixels
  • Center Point: (center_x, center_y)
  • Prediction Confidence: 0.XX / 1.00
  The system's prediction about where attention will move next

⬇️ MOVEMENT ANALYSIS:
  • Inferred Direction: [DIRECTION SYMBOL] [DIRECTION]
  The system's interpretation of click movement patterns

VISUALIZATION IMAGES:
------------------
• Red Rectangle: Current attention field
• Blue Dashed Rectangle: Predicted next attention field
• Red Dot: Current mouse click
• Blue Dots: Previous mouse clicks
• Green Arrow: Inferred movement direction

CONFIDENCE SCORES:
---------------
• 0.70-1.00: High confidence (multiple consistent clicks)
• 0.40-0.70: Medium confidence (limited click history)
• <0.40: Low confidence (cold start or inconsistent clicks)

The combination of detailed console output and saved visualization images provides
a complete picture of how the attention tracking system works in real-world scenarios.
"""
    print(guide)

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

def print_attention_info(event_num: int, event: ScreenshotEvent, 
                        current_field, next_field=None) -> None:
    """
    Print attention field information to the console.
    
    Args:
        event_num: The event number in sequence
        event: The screenshot event
        current_field: The current attention field
        next_field: The predicted next attention field (optional)
    """
    print("\n" + "═"*80)
    print(f"🔍 ATTENTION EVENT #{event_num}")
    print("═"*80)
    
    # Event information
    event_time = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    print(f"⏰ Time: {event_time}")
    print(f"🖱️  Mouse Click: ({event.mouse_x}, {event.mouse_y})")
    
    # Current attention field
    print("\n📌 CURRENT ATTENTION FIELD:")
    print(f"  • Top-Left Corner: ({current_field.x}, {current_field.y})")
    print(f"  • Dimensions: {current_field.width} × {current_field.height} pixels")
    print(f"  • Center Point: ({current_field.center[0]}, {current_field.center[1]})")
    print(f"  • Confidence Score: {current_field.confidence:.2f} / 1.00")
    
    # Next predicted field if available
    if next_field:
        print("\n🔮 PREDICTED NEXT ATTENTION:")
        print(f"  • Movement Direction: {next_field.direction.upper()}")
        print(f"  • Top-Left Corner: ({next_field.x}, {next_field.y})")
        print(f"  • Dimensions: {next_field.width} × {next_field.height} pixels")
        print(f"  • Center Point: ({next_field.center[0]}, {next_field.center[1]})")
        print(f"  • Prediction Confidence: {next_field.confidence:.2f} / 1.00")
    else:
        print("\n🔮 PREDICTED NEXT ATTENTION: Not available yet (need more clicks)")
    
    # Displacement from previous field center to current
    print("\n⬇️  MOVEMENT ANALYSIS:")
    if hasattr(current_field, 'direction') and current_field.direction:
        direction_symbol = {
            'up': '⬆️',
            'down': '⬇️',
            'left': '⬅️',
            'right': '➡️'
        }.get(current_field.direction, '◯')
        print(f"  • Inferred Direction: {direction_symbol} {current_field.direction.upper()}")
    else:
        print("  • Inferred Direction: None (not enough clicks yet)")
    
    print("─"*80)

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
    
    # Print header for console output
    print("\n" + "═"*80)
    print("🔍 ATTENTION FIELD ANALYSIS")
    print("═"*80)
    print(f"Processing {len(events)} events in sequence...")
    
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
        
        # Print attention information to console
        print_attention_info(i+1, event, current_field, next_field)
        
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
            
            # Save the figure
            output_path = os.path.join(OUTPUT_DIR, f"attention_field_{i+1:03d}.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Saved visualization {i+1}/{len(events)} to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to process event {i+1}: {str(e)}")
            plt.close()

def main():
    """Main function to visualize attention fields for mouse events by drawing on screenshots."""
    # Print interpretation guide
    print_interpretation_guide()
    
    # Load events from JSON file
    events = load_screenshot_events()
    
    if not events:
        logger.error("No valid mouse events with screenshots found")
        return
    
    # Visualize attention fields
    visualize_attention_fields(events)
    
    # Print summary
    print("\n" + "═"*80)
    print(f"📊 SUMMARY: Processed {len(events)} attention events")
    print(f"📁 Output saved to: {os.path.abspath(OUTPUT_DIR)}")
    print("═"*80)
    print("\nTip: Open the saved images to see visual representations of attention fields.")
    print("     Each image shows both current attention and predicted next attention areas.")
    
    logger.info(f"Completed visualization of attention fields for {len(events)} events")
    logger.info(f"Output saved to directory: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
