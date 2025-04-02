# Attention Field Controller

## Overview

The Attention Field Controller simulates human visual attention in user interfaces. It tracks click history and builds dynamic attention fields (bounding boxes) that represent areas of user focus. The controller can infer movement directions and predict next attention areas, providing context for UI navigation.

## Components

### 1. AttentionFieldController

The core controller class that manages visual attention based on click history.

#### Key Capabilities

- Track recent user clicks
- Build dynamic attention fields (bounding boxes)
- Infer movement directions based on click patterns
- Predict next areas of attention
- Handle cold starts with reasonable defaults

### 2. AttentionField

A dataclass representing a field of visual attention with properties:

- Bounding box coordinates (x, y, width, height)
- Confidence score
- Direction of movement (if applicable)
- Helper methods for center point, containment checks, etc.

## Implementation Logic

### Initialization

```python
def __init__(self, 
             expansion_factor: float = 1.5, 
             click_history_limit: int = 5,
             screen_width: int = 1920, 
             screen_height: int = 1080,
             default_box_size: int = 200):
```

The controller initializes with:
- `expansion_factor`: Controls how much the attention field expands beyond click points
- `click_history_limit`: Maximum number of clicks to remember
- `screen_width/height`: Screen dimensions for boundary checks
- `default_box_size`: Default size for attention fields

### Adding Clicks

```python
def add_click(self, x: int, y: int, timestamp: datetime = None)
def add_click_from_event(self, event: ScreenshotEvent)
```

When a click is added:
1. It's stored in the click history as a tuple (x, y, timestamp)
2. History is trimmed if it exceeds the limit
3. The attention field is updated based on the new click

### Attention Field Updates

```python
def _update_attention_field(self)
```

The attention field is updated using these rules:
- **Cold start**: Uses a default viewport
- **Single click**: Centers a fixed-size field on the click
- **Multiple clicks**: Creates a bounding box containing recent clicks, then expands it by the expansion factor

### Movement Direction Inference

```python
def _infer_movement_direction(self)
```

Direction is inferred by:
1. Comparing the two most recent clicks
2. Calculating the delta in x and y coordinates
3. Determining primary direction (up/down/left/right) based on the largest delta

### Next Attention Field Prediction

```python
def predict_next_attention_field(self)
```

The next field is predicted by:
1. Taking the current field and inferred direction
2. Shifting the field by ~30% of its dimensions in that direction
3. Ensuring the field stays within screen boundaries
4. Setting a slightly lower confidence score for the prediction

### Dynamic Sizing

```python
def set_base_box_size_from_omniparser(self, omniparser_result)
```

The controller can dynamically adjust the base attention field size based on UI element dimensions:
1. It uses the first click location to find containing UI elements
2. Sets the base box size based on the element's dimensions
3. This creates more natural attention fields that match UI component scales

## Usage Examples

### Basic Usage

```python
# Initialize controller
controller = AttentionFieldController()

# Add clicks (either directly or from events)
controller.add_click(500, 300)
controller.add_click_from_event(screenshot_event)

# Get current attention field
current_field = controller.get_current_attention_field()
print(f"Current attention centered at {current_field.center} with confidence {current_field.confidence}")

# Get predicted next field
next_field = controller.predict_next_attention_field()
if next_field:
    print(f"Predicted movement direction: {next_field.direction}")
```

## Design Principles

The Attention Field Controller implements these key principles:

1. **Recency Bias**: More recent clicks have more influence on attention
2. **Spatial Coherence**: Attention tends to be focused in spatially coherent regions
3. **Directional Momentum**: Attention tends to continue in the same direction
4. **Expansion**: Visual attention extends beyond exact click points
5. **Confidence Decay**: Confidence in predictions decreases with distance and time

## Implementation Notes

- The controller uses a deterministic, rule-based approach that doesn't require training data
- It's designed to be lightweight and efficient for real-time use
- The base implementation handles cold starts gracefully 