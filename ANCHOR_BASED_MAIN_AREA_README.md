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
