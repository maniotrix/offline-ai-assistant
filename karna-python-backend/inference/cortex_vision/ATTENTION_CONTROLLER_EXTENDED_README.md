# Extended Attention Field Controller

## Overview

The Extended Attention Field Controller builds upon the base AttentionFieldController to provide a framework for advanced attention modeling capabilities. This extended version preserves all the core functionality of the base controller while adding placeholders for future enhancements that will be implemented in phases.

## Base Functionality

The extended controller inherits all capabilities from the base AttentionFieldController:

- Tracking click history
- Building dynamic attention fields (bounding boxes)
- Inferring movement directions
- Predicting next attention areas
- Handling cold starts

For detailed documentation of the base functionality, please refer to `ATTENTION_CONTROLLER_README.md`.

## Enhanced Implementation

### ClickPoint Class

The extended controller replaces the tuple representation of clicks with a dedicated `ClickPoint` dataclass:

```python
@dataclass
class ClickPoint:
    """Represents a click point with timestamp."""
    x: int
    y: int
    timestamp: datetime
    relative_to_field: Optional[Tuple[float, float]] = None
    
    @property
    def age(self) -> timedelta:
        """Get the age of the click (time since it happened)."""
        return datetime.now() - self.timestamp
```

Key advantages of this approach:
- Better type safety and code readability
- Ability to attach additional metadata to clicks
- Support for relative positioning within attention fields
- Helper methods for time-based operations

## Phased Enhancement Plan

The extended controller is designed for incremental enhancement in four phases:

### Phase 1: Core Functionality (Current)

The initial phase includes all base functionality plus the enhanced `ClickPoint` data structure and necessary interface adjustments to support future enhancements.

### Phase 2: Attention Heatmap Generation

```python
def generate_attention_heatmap(self, resolution: Tuple[int, int] = (100, 100)) -> np.ndarray:
```

Phase 2 will implement continuous attention heatmap generation:

1. **Gaussian Click Distribution**: Each click generates a 2D Gaussian distribution of attention, creating "heat" around click points
2. **Recency Weighting**: More recent clicks contribute more heat to the map
3. **Directional Biasing**: Heat spreads more in the direction of movement
4. **Adaptive Scaling**: Heatmap adapts to screen dimensions and UI density
5. **Time Decay**: Heat diminishes over time for inactive areas

The heatmap provides a more nuanced view of attention than discrete bounding boxes, allowing for graduated levels of attention across the screen.

### Phase 3: Weighted Patch Scanning

```python
def get_patch_scanning_priorities(self, patches: List[Dict]) -> List[float]:
```

Phase 3 will prioritize UI elements based on the attention model:

1. **Patch Priority Calculation**: Each UI element (patch) gets a priority score based on its position within the attention heatmap
2. **OCR/Patch Matching Prioritization**: Elements with higher priority are processed first by OCR and patch matching operations
3. **Adaptive Scanning**: The system can adapt its scanning pattern based on attention distribution
4. **Context-Aware Priorities**: Priorities consider element type, recency of interaction, and directional context
5. **Confidence-Based Processing**: Lower confidence areas might trigger more thorough scanning

This prioritization enhances efficiency by focusing computational resources on areas most likely to be relevant to the user.

### Phase 4: Machine Learning Enhancements

```python
def train_from_interaction_history(self, interaction_data: List[Dict]) -> None:
def save_model(self, file_path: str) -> None:
def load_model(self, file_path: str) -> None:
```

Phase 4 will introduce machine learning to improve prediction accuracy:

1. **Interaction Pattern Learning**: The system learns from patterns in user interaction history
2. **Parameter Optimization**: ML adjusts attention parameters (expansion factors, confidence thresholds, etc.) dynamically
3. **Personalized Modeling**: Adaptation to individual user behavior patterns
4. **Predictive Analysis**: Advanced prediction of next attention areas beyond simple directional inference
5. **Transfer Learning**: Potential to apply knowledge from one UI context to another

The ML enhancements will make the attention model more adaptive and accurate over time.

## Technical Design

### Architecture

The extended controller uses a modular design:

```
AttentionFieldController
├── Core Attention Management
│   ├── Click History Tracking
│   ├── Attention Field Generation
│   └── Direction Inference
├── Phase 2: Heatmap Generation
├── Phase 3: Patch Prioritization
└── Phase 4: ML Components
```

This separation allows for:
- Independent development and testing of each phase
- Backward compatibility as new features are added
- Clear interfaces between components

### Data Structures

- `AttentionField`: Dataclass for attention bounding boxes
- `ClickPoint`: Enhanced click representation with metadata
- `np.ndarray`: 2D array for heatmap representation
- Various dictionaries for context and metadata

## Usage Examples

### Basic Usage (Same as Base Controller)

```python
controller = AttentionFieldController()
controller.add_click(500, 300)
current_field = controller.get_current_attention_field()
```

### Phase 2: Heatmap Generation

```python
# Generate a 100x100 resolution heatmap
heatmap = controller.generate_attention_heatmap((100, 100))

# Visualize the heatmap
import matplotlib.pyplot as plt
plt.imshow(heatmap, cmap='hot', interpolation='nearest')
plt.colorbar(label='Attention Intensity')
plt.title('Attention Heatmap')
plt.show()
```

### Phase 3: Weighted Patch Scanning

```python
# Define UI element patches
ui_patches = [
    {'bbox': (100, 200, 150, 50), 'id': 'button_1'},
    {'bbox': (300, 150, 200, 80), 'id': 'input_field'},
    {'bbox': (50, 400, 500, 100), 'id': 'navigation_bar'}
]

# Get scanning priorities
priorities = controller.get_patch_scanning_priorities(ui_patches)

# Process elements in priority order
sorted_elements = [p for _, p in sorted(
    zip(priorities, ui_patches), 
    key=lambda pair: pair[0], 
    reverse=True
)]
```

### Phase 4: ML Enhancements

```python
# Train the model from interaction history
controller.train_from_interaction_history(interaction_data)

# Save the trained model
controller.save_model('attention_model.pkl')

# Load a previously trained model
controller.load_model('attention_model.pkl')
```

## Implementation Notes

- The extended controller maintains backward compatibility with the base controller
- Each phase builds upon previous phases but can still function if later phases are not yet implemented
- Placeholder implementations return reasonable defaults when a feature is not yet implemented
- The design prioritizes modularity and clear interfaces between components

## Next Steps

1. **Complete Phase 2 Implementation**: Implement the heatmap generation algorithms
2. **Visualization Tools**: Develop tools to visualize both attention fields and heatmaps
3. **Phase 3 Development**: Implement weighted patch scanning
4. **Data Collection**: Gather interaction data for ML training
5. **Phase 4 Development**: Implement and train ML components 