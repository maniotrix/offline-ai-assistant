# Attention Field Controller

## Overview

The Attention Field Controller simulates human visual attention in user interfaces. It tracks click history, builds dynamic attention fields (bounding boxes) representing user focus, infers movement direction using a hybrid approach, predicts the next likely attention area, and tracks the cumulative screen area covered.

Configuration parameters are loaded from a JSON file and can be dynamically adjusted based on the viewport's aspect ratio (e.g., biasing towards vertical movement in tall, narrow windows).

## Components

### 1. AttentionFieldController

The core controller class. Key capabilities include:
- Loading configuration from JSON via a Pydantic model.
- Dynamically adjusting configuration based on viewport aspect ratio.
- Tracking recent user clicks with timestamps.
- Calculating the center of the core bounding box encompassing recent clicks.
- Building dynamic attention fields centered on the core click area.
- Inferring movement direction using a hybrid approach (last dominant axial shift, then weighted average of center movements).
- Predicting the next area of attention based on inferred direction.
- Tracking the cumulative bounding box covering all generated attention fields.
- Handling cold starts with reasonable defaults.
- Allowing dynamic adjustment of the base attention box size based on clicked UI elements (via `set_base_box_size_from_omniparser`).

### 2. AttentionField

A dataclass representing a single field of visual attention with properties:
- Bounding box coordinates (x, y, width, height)
- Confidence score
- Inferred direction of movement leading to this field (if applicable)
- Helper methods for center point (`center`), alternative bbox formats (`bbox`, `xyxy`), and point containment checks (`contains_point`).

### 3. AttentionConfig

A Pydantic `BaseModel` defining the controller's configurable parameters, loaded from JSON:
- `dominance_ratio_horizontal`: Ratio for detecting dominant horizontal movement in the hybrid check.
- `dominance_ratio_vertical`: Ratio for detecting dominant vertical movement.
- `recency_power_factor`: Exponent controlling recency bias in the weighted average fallback.
- `expansion_factor_horizontal`: Factor for expanding the core box horizontally.
- `expansion_factor_vertical`: Factor for expanding the core box vertically.

## Implementation Logic

### Initialization

```python
def __init__(self,
             click_history_limit: int = 5,
             screen_width: int = 1920,
             screen_height: int = 1080,
             default_box_size: int = 200,
             viewport_bbox: Dict = renderBBox,
             config_path: str = "default_attention_config.json"):
```
The controller initializes with:
- Basic parameters: `click_history_limit`, `screen_width/height`, `default_box_size`.
- `viewport_bbox`: Defines the primary interaction area.
- `config_path`: Path to the JSON configuration file (`default_attention_config.json` by default).
- **Configuration Loading**: Reads the JSON file, parses it into an `AttentionConfig` object (`self.config`). Handles file not found or parsing errors by using default values.
- **Dynamic Adjustment**: Calculates the viewport's aspect ratio. Based on whether it's tall (>1.2), wide (<0.8), or balanced, it overrides the loaded/default configuration values in `self.config` to better suit the likely interaction pattern (e.g., lower vertical dominance ratio and higher vertical expansion for tall viewports). Logs the final active configuration.
- Initializes empty click and center histories.
- Resets cumulative coverage tracking.

### Adding Clicks

```python
def add_click(self, x: int, y: int, timestamp: datetime = None)
def add_click_from_event(self, event: ScreenshotEvent)
```
When a click is added:
1. It's stored in `click_history`.
2. History is trimmed if `click_history_limit` is exceeded (corresponding center is also removed from `center_history`).
3. `_update_attention_field()` is called to recalculate the current field and update `center_history`.
4. `_update_cumulative_coverage()` is called using the newly calculated `current_attention_field`.

### Attention Field Updates (`_update_attention_field`)

1. **Determine Core Box & Center**:
   - If 1 click: Core center is the click coordinates.
   - If >1 click: Calculates the minimal bounding box around all clicks in history. The center of *this* box is the core center. Core dimensions are derived from this box (or `base_box_size` if larger).
2. **Update Center History**: Adds or updates the latest entry in `center_history` with the calculated core center coordinates. Handles potential mismatches between click and center history lengths (e.g., during processing).
3. **Calculate Expanded Field**:
   - Takes the core dimensions (`core_width`, `core_height`).
   - Expands them using `self.config.expansion_factor_horizontal` and `self.config.expansion_factor_vertical`.
4. **Create `AttentionField` Object**:
   - Creates the `current_attention_field` instance, centered on the `core_center`, with the calculated `expanded_width` and `expanded_height`.
   - Ensures the field stays within screen bounds.
   - Calls `_infer_movement_direction()` to get the direction.
   - Sets confidence (0.8 for first click, 0.9 otherwise).

### Movement Direction Inference (`_infer_movement_direction`)

Uses a **hybrid approach**:
1. **Check Last Axial Movement**:
   - Calculates the vector between the last two points in `center_history`.
   - If its magnitude is significant (> `MIN_MAGNITUDE`):
     - Compares `abs(dy_last)` to `self.config.dominance_ratio_vertical * abs(dx_last)`. If `dy` dominates, returns `up` or `down`.
     - Compares `abs(dx_last)` to `self.config.dominance_ratio_horizontal * abs(dy_last)`. If `dx` dominates, returns `left` or `right`.
2. **Fallback to Weighted Average**:
   - If the last movement wasn't significant or wasn't strongly axial, it proceeds.
   - Calculates movement vectors between *all* consecutive pairs in `center_history`.
   - Applies weights to these vectors based on recency using `weight = (pair_index / num_pairs) ** self.config.recency_power_factor`.
   - Computes the weighted average vector.
   - If the magnitude of the average vector is significant, determines the direction based on its angle (divided into four 90-degree quadrants).

### Cumulative Coverage Tracking

- `_min_x/y_covered`, `_max_x/y_covered` store the bounds.
- `_coverage_initialized` flag tracks if any field has been added.
- `_update_cumulative_coverage(field)`: Updates bounds based on a new field's `xyxy`. Called by `add_click`.
- `_reset_cumulative_coverage()`: Resets bounds. Called by `process_click_history`.
- `cumulative_coverage_bbox` (property): Returns the current cumulative box `(x, y, w, h)` or `None`.

### Next Attention Field Prediction (`predict_next_attention_field`)

- Uses the `direction` stored in the `current_attention_field`.
- Shifts the current field's position by ~30% of its dimensions in that direction.
- Clamps the result to screen boundaries.
- Assigns a lower confidence (0.7).

### Dynamic Sizing (`set_base_box_size_from_omniparser`)

- *Optional step*, typically called after processing the *first* click if UI element info (`OmniParserResultModel`) is available.
- Finds the UI element containing the first click.
- Adjusts `self.base_box_size` based on the element's average dimension (clamped by the initial `default_box_size`).
- Sets `self.base_box_initialized = True` to prevent re-running.

## Usage Examples

### Basic Usage

```python
from attention_controller import AttentionFieldController, ScreenshotEvent # (assuming appropriate imports)

# Initialize controller (loads default config, adjusts based on default viewport)
controller = AttentionFieldController()

# Alternatively, provide specific viewport or config path
# tall_viewport = {"x": 100, "y": 100, "width": 400, "height": 800}
# controller = AttentionFieldController(viewport_bbox=tall_viewport, config_path="my_config.json")

# Add clicks (either directly or from events)
# Simulating events... replace with actual ScreenshotEvent objects
event1 = ScreenshotEvent(mouse_x=500, mouse_y=300, timestamp=datetime.now(), ...)
event2 = ScreenshotEvent(mouse_x=550, mouse_y=600, timestamp=datetime.now(), ...)

controller.add_click_from_event(event1)
controller.add_click_from_event(event2)

# Get current attention field
current_field = controller.get_current_attention_field()
if current_field:
  print(f"Current attention: BBox={current_field.bbox}, Center={current_field.center}, Conf={current_field.confidence:.2f}, Dir={current_field.direction}")

# Get predicted next field
next_field = controller.predict_next_attention_field()
if next_field:
    print(f"Predicted next: BBox={next_field.bbox}, Dir={next_field.direction}")

# Get full context including cumulative coverage
context = controller.get_attention_context()
print(f"Context: {context}")
coverage = context.get("cumulative_coverage", {}).get("bbox")
if coverage:
    print(f"Cumulative Coverage: {coverage}")

# Process a whole sequence (clears history first)
all_events: List[ScreenshotEvent] = [...]
controller.process_click_history(all_events)
```

## Design Principles

1.  **Configuration Flexibility**: Defaults loaded from JSON, adaptable based on viewport.
2.  **Hybrid Inference**: Prioritizes clear recent axial shifts, falls back on smoothed trend.
3.  **Center-Based Modeling**: Focuses on the movement of the center of recent click clusters.
4.  **Recency Bias**: Recent center movements have more influence in the weighted average.
5.  **Contextual Expansion**: Attention field shape adapts based on viewport aspect ratio.
6.  **Cumulative Tracking**: Maintains awareness of the total interaction area.
7.  **Noise Resistance**: Minimum magnitude thresholds prevent spurious direction changes.

## Implementation Notes

- Requires `pydantic`.
- Assumes `default_attention_config.json` exists relative to the script or provided path.
- Logging provides insight into dynamic config selection and direction inference steps.
- Cumulative coverage is reset when `process_click_history` is called.

## Planned Enhancements

### Phase 2: Heatmap Generation
- Generate 2D attention heatmaps based on click density
- Apply Gaussian distribution around click points
- Weight heat by recency and movement direction
- Support configurable resolution and decay rates

### Phase 3: Weighted Patch Scanning
- Calculate priority scores for UI patches
- Use heatmap values to weight patch importance
- Optimize OCR and patch matching order
- Support dynamic threshold adjustment

### Phase 4: Machine Learning Integration
- Train on user interaction patterns
- Adjust weights and parameters automatically
- Improve direction prediction accuracy
- Adapt to user-specific navigation styles

## Design Principles

The Attention Field Controller implements these key principles:

1. **Recency Bias**: More recent clicks have exponentially higher influence on attention
2. **Spatial Coherence**: Attention tends to be focused in spatially coherent regions
3. **Directional Momentum**: Attention follows weighted historical movement patterns
4. **Expansion**: Visual attention extends beyond exact click points
5. **Confidence Decay**: Confidence in predictions decreases with distance and time
6. **Historical Context**: Movement patterns consider all available click history
7. **Noise Resistance**: Minimum movement thresholds prevent spurious direction changes

## Implementation Notes

- The controller uses a deterministic, rule-based approach that doesn't require training data
- It's designed to be lightweight and efficient for real-time use
- The base implementation handles cold starts gracefully
- Movement direction inference now considers weighted historical patterns
- Future enhancements will add heatmap generation and weighted patch scanning 