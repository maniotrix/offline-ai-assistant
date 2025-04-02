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
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(current_dir)))

from services.screen_capture_service import ScreenshotEvent
from inference.omniparser.attention_controller import AttentionFieldController, AttentionField

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded JSON file path (adjust if needed)
DEFAULT_DATA_DIR = workspace_dir / "data" / "chatgpt" / "883c46f5-c62d-4799-baa1-5e3b12f12e8c"
JSON_FILE_PATH = str(DEFAULT_DATA_DIR / "screenshot_events_883c46f5-c62d-4799-baa1-5e3b12f12e8c.json")
OUTPUT_DIR = Path(current_dir) / "attention_visualization"

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

🗺️ CUMULATIVE COVERAGE:
  • Bounding Box: (x, y, w, h)
  The total area covered by all attention fields so far.

⬇️ MOVEMENT ANALYSIS:
  • Inferred Direction: [DIRECTION SYMBOL] [DIRECTION]
  The system's interpretation of click movement patterns

VISUALIZATION IMAGES:
------------------
• Red Rectangle: Current attention field
• Blue Dashed Rectangle: Predicted next attention field
• Grey Translucent Rectangle: Cumulative area covered by attention
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

def print_attention_info(event_num: int, event: ScreenshotEvent,
                         controller: AttentionFieldController) -> None:
    """
    Print attention field information to the console for a given event.

    Args:
        event_num: The event number in sequence.
        event: The screenshot event.
        controller: The AttentionFieldController after processing the event.
    """
    current_field = controller.get_current_attention_field()
    next_field = controller.predict_next_attention_field()
    cumulative_bbox = controller.cumulative_coverage_bbox

    print("\n" + "═"*80)
    print(f"🔍 ATTENTION EVENT #{event_num}")
    print("═"*80)

    # Event information
    event_time = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    print(f"⏰ Time: {event_time}")
    print(f"🖱️  Mouse Click: ({event.mouse_x}, {event.mouse_y})")

    # Current attention field
    print("\n📌 CURRENT ATTENTION FIELD:")
    if current_field:
        print(f"  • Top-Left Corner: ({current_field.x}, {current_field.y})")
        print(f"  • Dimensions: {current_field.width} × {current_field.height} pixels")
        # Ensure center is accessed correctly (it's a property returning a tuple)
        center_x, center_y = current_field.center
        print(f"  • Center Point: ({center_x}, {center_y})")
        print(f"  • Confidence Score: {current_field.confidence:.2f} / 1.00")
    else:
        print("  • Not available")

    # Next predicted field if available
    print("\n🔮 PREDICTED NEXT ATTENTION:")
    if next_field:
        print(f"  • Movement Direction: {next_field.direction.upper()}")
        print(f"  • Top-Left Corner: ({next_field.x}, {next_field.y})")
        print(f"  • Dimensions: {next_field.width} × {next_field.height} pixels")
        next_center_x, next_center_y = next_field.center
        print(f"  • Center Point: ({next_center_x}, {next_center_y})")
        print(f"  • Prediction Confidence: {next_field.confidence:.2f} / 1.00")
    else:
        print("  • Not available yet") # E.g., need more clicks or no direction inferred

    # Cumulative Coverage
    print("\n🗺️ CUMULATIVE COVERAGE:")
    if cumulative_bbox:
        cx, cy, cw, ch = cumulative_bbox
        print(f"  • Bounding Box: ({cx}, {cy}, w={cw}, h={ch})")
    else:
        print("  • Not available yet")

    # Movement Analysis
    print("\n⬇️ MOVEMENT ANALYSIS:")
    if current_field and current_field.direction:
        direction_symbol = {
            'up': '⬆️',
            'down': '⬇️',
            'left': '⬅️',
            'right': '➡️'
        }.get(current_field.direction, '◯')
        print(f"  • Inferred Direction: {direction_symbol} {current_field.direction.upper()}")
    else:
        print("  • Inferred Direction: None")

    print("─"*80)

def visualize_attention_fields(events: List[ScreenshotEvent]) -> None:
    """
    Visualize attention fields, predictions, and cumulative coverage on screenshots.

    Args:
        events: List of ScreenshotEvent objects.
    """
    if not events:
        logger.warning("No events to visualize")
        return

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create controller (implicitly loads config & adjusts for viewport)
    # Assuming default viewport and config path for this test
    controller = AttentionFieldController()

    print("\n" + "═"*80)
    print("🔍 ATTENTION FIELD ANALYSIS")
    print("═"*80)
    print(f"Processing {len(events)} events in sequence...")

    for i, event in enumerate(events):
        if not event.screenshot_path or not os.path.exists(event.screenshot_path):
            logger.warning(f"Skipping event {i+1}: Screenshot missing at {event.screenshot_path}")
            continue

        # Add current click to controller
        controller.add_click_from_event(event)

        # Get current state from controller
        current_field = controller.get_current_attention_field()
        next_field = controller.predict_next_attention_field()
        cumulative_bbox = controller.cumulative_coverage_bbox

        # Print info for this step
        print_attention_info(i + 1, event, controller)

        # --- Visualization --- 
        try:
            plt.figure(figsize=(15, 10))
            img = plt.imread(event.screenshot_path)
            plt.imshow(img)
            img_height, img_width = img.shape[0], img.shape[1]
            plt.xlim(0, img_width)
            plt.ylim(img_height, 0) # Invert y-axis

            # Draw Cumulative Coverage Area (light grey, behind others)
            if cumulative_bbox:
                cc_x, cc_y, cc_w, cc_h = cumulative_bbox
                cumulative_rect = patches.Rectangle(
                    (cc_x, cc_y), cc_w, cc_h,
                    linewidth=1, edgecolor='grey', facecolor='grey', alpha=0.2,
                    label='Cumulative Coverage', zorder=1 # Draw behind others
                )
                plt.gca().add_patch(cumulative_rect)

            # Draw Current Attention Field (solid red)
            if current_field:
                current_rect = patches.Rectangle(
                    (current_field.x, current_field.y), current_field.width, current_field.height,
                    linewidth=3, edgecolor='r', facecolor='none', alpha=0.7,
                    label=f"Current Attention (conf={current_field.confidence:.2f})", zorder=3
                )
                plt.gca().add_patch(current_rect)

            # Draw Predicted Next Attention Field (dashed blue)
            if next_field:
                next_rect = patches.Rectangle(
                    (next_field.x, next_field.y), next_field.width, next_field.height,
                    linewidth=2, edgecolor='b', facecolor='none', alpha=0.5, linestyle='--',
                    label=f"Predicted Next (dir={next_field.direction}, conf={next_field.confidence:.2f})", zorder=4
                )
                plt.gca().add_patch(next_rect)

                # Draw Movement Arrow (only if direction exists)
                if current_field and current_field.direction:
                    center_x, center_y = current_field.center
                    arrow_length = min(current_field.width, current_field.height) * 0.3
                    dx, dy = 0, 0
                    if current_field.direction == 'right': dx = arrow_length
                    elif current_field.direction == 'left': dx = -arrow_length
                    elif current_field.direction == 'down': dy = arrow_length # Screen coords
                    elif current_field.direction == 'up': dy = -arrow_length # Screen coords

                    if dx != 0 or dy != 0:
                        plt.arrow(center_x, center_y, dx, dy,
                                  head_width=15, head_length=15,
                                  fc='g', ec='g', alpha=0.7,
                                  label="Movement Direction", zorder=5)

            # Plot click history (current click red, previous blue)
            # Accessing click_history directly from controller instance
            for j, click_data in enumerate(controller.click_history):
                x, y, _ = click_data # Unpack tuple
                if j == len(controller.click_history) - 1: # Most recent click
                    plt.plot(x, y, 'ro', markersize=12, label='Current Click', zorder=7)
                else:
                    plt.plot(x, y, 'bo', markersize=7, alpha=0.6, zorder=6)

            # Add title and legend
            event_time = event.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            direction_info = f", Dir: {current_field.direction}" if current_field and current_field.direction else ""
            plt.title(f"Attention Field after Click {i+1}/{len(events)} ({event_time}){direction_info}", fontsize=14)
            plt.legend(loc='upper right', fontsize=10)
            plt.axis('off') # Hide axes ticks/labels

            # Add information about attention context in text box (Re-added)
            if current_field: # Ensure current_field exists
                attention_info = [
                    f"Current Click: ({event.mouse_x}, {event.mouse_y})",
                    f"Attention Field: ({current_field.x}, {current_field.y}, w={current_field.width}, h={current_field.height})",
                    f"Confidence: {current_field.confidence:.2f}"
                ]
                if current_field.direction:
                    attention_info.append(f"Direction: {current_field.direction}")
                
                if next_field:
                    attention_info.extend([
                        f"Next Field: ({next_field.x}, {next_field.y}, w={next_field.width}, h={next_field.height})",
                        f"Next Confidence: {next_field.confidence:.2f}"
                    ])
                if cumulative_bbox:
                    cx, cy, cw, ch = cumulative_bbox
                    attention_info.append(f"Cumulative: ({cx}, {cy}, w={cw}, h={ch})")

                plt.gcf().text(0.02, 0.02, '\n'.join(attention_info), fontsize=10, 
                        bbox=dict(facecolor='white', alpha=0.7))

            # Save the figure
            output_path = OUTPUT_DIR / f"attention_field_{i+1:03d}.png"
            plt.savefig(str(output_path), dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Saved visualization {i+1}/{len(events)} to {output_path}")

        except Exception as e:
            logger.error(f"Failed to process or visualize event {i+1}: {str(e)}", exc_info=True)
            plt.close()

def main():
    """Main function to load data and run visualization."""
    print_interpretation_guide()

    # Load events
    events = load_screenshot_events(JSON_FILE_PATH)

    if not events:
        logger.error("No valid events loaded, exiting.")
        return

    # Visualize
    visualize_attention_fields(events)

    # Summary
    print("\n" + "═"*80)
    print(f"📊 SUMMARY: Processed {len(events)} attention events")
    print(f"📁 Output saved to: {OUTPUT_DIR.resolve()}")
    print("═"*80)
    print("\nTip: Open the saved images to see visual representations.")

    logger.info(f"Completed visualization. Output: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
