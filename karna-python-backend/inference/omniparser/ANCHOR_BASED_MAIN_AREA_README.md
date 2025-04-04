# Anchor-Based Main Area Detector

## Overview

The Anchor-Based Main Area Detector is a sophisticated system designed to identify and track the main content area in UI screenshots across different frames and screen resolutions. It uses a decoupled architecture with separate components for training and runtime detection.

## Architecture

The implementation follows a decoupled architecture with two main components:

1. **Training Component** (`anchor_based_main_area_detector.py`): Responsible for analyzing multiple frames, identifying stable UI elements as anchors, and creating a serializable model.

2. **Runtime Component** (`anchor_based_main_area_detector_runtime.py`): Loads a trained model and performs detection on new screenshots without requiring the original training data.

## Key Concepts

- **Anchor Points**: Stable UI elements that maintain consistent positioning relative to the main content area.
- **Main Area References**: Visual samples of the main content area from training frames.
- **Constraint Directions**: How anchor points relate spatially to the main area (top, bottom, left, right).
- **Serialization**: Using Pydantic models to save and load all detection data.

## Technical Implementation Details

### Visual Embedding System

- **ResNet-based Embeddings**: The system uses ResNet50 (default) to generate high-dimensional embeddings of visual elements.
- **Similarity Metrics**: Cosine similarity between embedding vectors determines visual similarity.
- **Threshold-based Matching**: 
  - Main area matching threshold: 0.7 (configurable) 
  - Anchor matching threshold: 0.8 (configurable)

### Element Stability Algorithm

1. **Presence Tracking**: Elements are tracked across frames by counting their appearances.
2. **Position Variance**: 
   ```
   position_variance = np.mean(np.var(positions, axis=0))
   position_stability = 1.0 / (1.0 + position_variance)
   ```
3. **Combined Stability Score**:
   ```
   stability_score = (appearance_count / total_frames) * position_stability
   ```
4. **Threshold Filtering**: Only elements with stability scores above `min_stability_score` (default: 0.7) are considered.

### Anchor Selection Strategy

1. **Border Proximity**: Elements near the borders of the main area are preferred (within 10% of edge).
2. **Direction Distribution**: The system aims to select anchors representing all four directions (top, bottom, left, right).
3. **Stability Priority**: Anchors are sorted by stability score and limited to `max_anchor_points` (default: 10).
4. **Reference Diversity**: Multiple main area references are stored from different frames (up to `max_main_area_references`, default: 4).

### Spatial Constraint System

1. **Direction Determination**: For each anchor, the system calculates the closest edge of the main area.
2. **Constraint Ratio Calculation**:
   ```python
   # For left edge
   ratio = (elem_center_x - main_left) / main_width
   # For right edge
   ratio = (main_right - elem_center_x) / main_width
   # For top edge
   ratio = (elem_center_y - main_top) / main_height
   # For bottom edge
   ratio = (main_bottom - elem_center_y) / main_height
   ```
3. **Relative Positioning**: Constraint ratios preserve the proportional relationship between anchors and the main area.

### Main Area Reconstruction Algorithm

The reconstruction process follows these steps:

1. **Anchor Matching**: Match anchor points from the model with elements in the new frame.
2. **Direction Grouping**: Group matched anchors by constraint direction.
3. **Constraint Calculation**: 
   ```python
   # Example for top constraint
   constraints["top"] = element_center[1] + (
       (original_main_area[1] - anchor_center[1]) *
       (element_pos[3] - element_pos[1]) / (anchor_pos[3] - anchor_pos[1])
   )
   ```
4. **Boundary Reconstruction**:
   - Directly use constraints if available for opposite edges
   - Apply aspect ratio constraints when only some edges are constrained
   - Fall back to scaling if constraints are insufficient

5. **Confidence Calculation**:
   ```python
   anchor_count_factor = min(len(matched_anchors) / 4, 1.0)
   avg_score = sum(m["score"] for m in matched_anchors) / len(matched_anchors)
   confidence = 0.7 * anchor_count_factor + 0.3 * avg_score
   ```

### Fallback Strategy

The system implements a progressive fallback strategy:

1. **Direct Matching**: Try to match the entire main area directly (highest confidence).
2. **Anchor Reconstruction**: Use anchor points to reconstruct the main area (medium confidence).
3. **Low-Confidence Direct Match**: Use direct matching results even with low confidence.
4. **Scaled Original**: Scale the original main area proportionally to the new image size (lowest confidence).

### Error Handling Strategies

1. **Missing Model Files**: The system checks for file existence before loading and gracefully handles missing files.
2. **Failed Embedding Generation**: When embedding generation fails, the system logs warnings and continues with available data.
3. **Insufficient Anchor Matches**: If fewer than 2 anchors match, the system falls back to other detection methods.
4. **Boundary Conditions**: All coordinates are clamped to image boundaries to prevent out-of-bounds issues.
5. **Type Safety**: The system uses explicit type checking and defensive programming against dictionary key errors.

### Performance Optimizations

1. **Selective Embedding Generation**: Embeddings are only generated when needed, not for all elements.
2. **Embedding Caching**: Pre-computed embeddings are saved to disk to avoid regeneration.
3. **Prioritized Matching**: Elements are filtered by source type before visual matching to reduce computation.
4. **Early Exit**: Detection stops at the first high-confidence method rather than trying all methods.
5. **Selective Frame Sampling**: For main area references, a subset of evenly spaced frames is used instead of all frames.

### Dictionary Access Safety Measures

To address potential dictionary key errors and type checking issues:

1. **Defensive Key Access**: 
   ```python
   value = data.get("key", default_value) 
   ```
2. **Type Checking**:
   ```python
   if isinstance(data, dict) and "key" in data:
       # Access data safely
   ```
3. **Dictionary Initialization**: All dictionaries are initialized with expected keys before modification.

## Training Process

The training component (`anchor_based_main_area_detector.py`) implements these key steps:

1. Extract patches from UI elements in multiple frames
2. Identify stable elements that appear consistently across frames
3. Select anchor points based on stability and position relative to the main area
4. Create visual references of the main content area
5. Save the model with all necessary data for runtime detection

## Detection Process

The runtime component (`anchor_based_main_area_detector_runtime.py`) implements these key steps:

1. Load a trained model with anchor points and main area references
2. Try direct matching of the main area using visual references
3. If direct matching fails, find matches for anchor points
4. Reconstruct the main area position using matched anchors and their constraints
5. Fall back to scaled original area if other methods fail

## Usage

### Training

```python
from inference.omniparser.anchor_based_main_area_detector import AnchorBasedMainAreaDetector

# Initialize detector
detector = AnchorBasedMainAreaDetector()

# Train with omniparser results and main area bounding box
result = detector.train(
    result_model=current_frame_result,
    frames=all_frame_results,
    main_area=[x1, y1, x2, y2],
    save_dir="path/to/model_dir"
)
```

### Runtime Detection

```python
from inference.omniparser.anchor_based_main_area_detector_runtime import AnchorBasedMainAreaDetectorRuntime

# Initialize runtime detector
detector = AnchorBasedMainAreaDetectorRuntime()

# Load model and detect main area in new frame
detection_result = detector.detect(
    result_model=new_frame_result,
    model_dir="path/to/model_dir"
)

# Use the detected main area
main_area = detection_result["main_area"]
```

## Data Models

The implementation uses Pydantic for data serialization:

- `AnchorPointData`: Stores information about anchor points
- `MainAreaReferenceData`: Stores information about main area references
- `DetectionModelData`: Top-level model containing all detection data

```python
# Pydantic data models for serialization
class AnchorPointData(BaseModel):
    """Data model for anchor points to be serialized/deserialized."""
    element_id: str
    element_type: str
    bbox: List[float]
    source: str
    constraint_direction: str
    constraint_ratio: float
    stability_score: float
    patch_path: str
    embedding_path: str

class MainAreaReferenceData(BaseModel):
    """Data model for main area reference patches to be serialized/deserialized."""
    bbox: List[float]
    frame_index: int
    patch_path: str
    embedding_path: str

class DetectionModelData(BaseModel):
    """Data model for the complete detection model to be serialized/deserialized."""
    model_version: str = "1.0.0"
    model_created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    main_area: List[float]
    screen_dimensions: List[float]
    anchor_points: List[AnchorPointData] = []
    main_area_references: List[MainAreaReferenceData] = []
```

## Directory Structure

When a model is saved, it creates the following structure:

```
model_dir/
  ├── model.json             # Model metadata and configuration
  ├── anchors/               # Anchor point patch images
  ├── main_areas/            # Main area reference images
  └── embeddings/            # Neural network embeddings
```

## Dependencies

- Pydantic: For data serialization
- PIL/Pillow: For image processing
- NumPy: For numerical operations
- ResNet (via torchvision): For generating image embeddings

## Error Handling

The implementation includes robust error handling for:
- Missing or corrupted model files
- Failed embedding generation
- Insufficient anchor matches
- Boundary conditions

## Performance Considerations

- The training process is computationally intensive due to image embedding generation
- Runtime detection is optimized for speed with fallback mechanisms
- The system degrades gracefully when perfect matches aren't possible

## Known Issues and Future Improvements

1. **Type Checking**: Some linter errors related to type checking in dictionary access need to be addressed.
2. **Embedding Dimension Verification**: Verify embedding dimensions before comparison to prevent shape mismatches.
3. **Multi-threading**: Add optional multi-threading for embedding generation to improve training performance.
4. **Adaptive Thresholds**: Implement adaptive thresholds that adjust based on image quality and content.
5. **Visual Anchor Grouping**: Group visually similar anchors to improve robustness against UI element changes.
