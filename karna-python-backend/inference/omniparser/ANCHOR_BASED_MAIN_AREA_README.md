# Anchor-Based Main Area Detector

## Overview

The Anchor-Based Main Area Detector is a sophisticated system designed to identify and track the main content area in UI screenshots across different frames and screen resolutions. It uses a hybrid approach combining visual matching and spatial constraints from anchor elements to ensure robust detection across diverse conditions.

## Architecture

The implementation follows a decoupled architecture with two main components:

1. **Training Component** (`anchor_based_main_area_detector.py`): Responsible for analyzing multiple frames, identifying stable UI elements as anchors, extracting main area references, and creating a serializable model.

2. **Runtime Component** (`anchor_based_main_area_detector_runtime.py`): Loads a trained model and performs detection on new screenshots without requiring the original training data.

## Key Concepts

- **Main Area**: The primary content region on a screen that contains the main UI/content (excluding navigation bars, menus, etc.)
- **Main Area References**: Visual samples of the main content area from multiple frames used for matching
- **Anchor Points**: Stable UI elements that maintain consistent positioning relative to the main content area
- **Constraint Directions**: How anchor points relate spatially to the main area (top, bottom, left, right)
- **Stability Score**: Metric measuring how stable an element is across frames
- **Sliding Window Matching**: Primary detection method using visual similarity with candidate regions
- **Anchor-based Reconstruction**: Fallback method using spatial constraints from anchor points

## Training Phase - `AnchorBasedMainAreaDetector`

### Initialization
```python
detector = AnchorBasedMainAreaDetector(
    model_name='resnet50',
    min_stability_score=0.7,
    anchor_match_threshold=0.8,
    max_anchor_points=10,
    max_main_area_references=4
)
```

### Training Process
1. **Main Area Detection**: Uses `UIOptimizedDynamicAreaDetector` to identify the main content area across frames
2. **Stable Element Identification**: Finds UI elements that maintain stable position and appearance across frames
3. **Anchor Point Selection**: Identifies elements near the main area borders with high stability scores
4. **Main Area Reference Extraction**: Takes visual samples of the main area from multiple frames
5. **Model Saving**: Serializes the model to disk, including:
   - Main area coordinates and screen dimensions
   - Anchor point data and patches
   - Main area reference patches

### Element Stability Algorithm
Elements are evaluated for stability using:
- **Presence Frequency**: Elements must appear in at least 75% of frames
- **Position Stability**: Lower position variance results in higher stability
- **Combined Score**: `stability_score = (appearance_count / total_frames) * position_stability`
- **Threshold Filtering**: Only elements with `stability_score >= min_stability_score` are considered

### Anchor Selection Strategy
1. **Border Proximity**: Elements near the borders of the main area are preferred (within 10% of edge)
2. **Direction Distribution**: The system aims to select anchors representing all four directions (top, bottom, left, right)
3. **Stability Priority**: Anchors are sorted by stability score and limited to `max_anchor_points`
4. **Reference Diversity**: Multiple main area references are stored from different frames (up to `max_main_area_references`)

## Detection Phase - `AnchorBasedMainAreaDetectorRuntime`

### Initialization
```python
detector = AnchorBasedMainAreaDetectorRuntime(
    model_name='resnet50',
    main_area_match_threshold=0.7,
    anchor_match_threshold=0.8,
    sliding_window_steps=5,
    sliding_window_sizes=[0.4, 0.5, 0.6, 0.7, 0.8]
)
```

### Detection Algorithm
The detection process follows a multi-tier approach:

1. **Sliding Window Matching (Primary Method)**:
   - Generates candidate regions at multiple scales using a sliding window approach
   - Creates candidate regions ranging from 40-80% of image size with overlapping steps
   - Compares each region with stored reference patches using visual embeddings
   - If a match is found with confidence >= 0.7, its bounding box is returned
   - Refines the match using UI elements if needed
   - Fast and effective when visual content is similar

2. **Anchor-based Reconstruction (First Fallback)**:
   - Used when sliding window matching fails or has low confidence
   - Matches anchor points in the current frame using visual similarity
   - Applies both horizontal and vertical constraints from each matched anchor:
     - For horizontal: left/right constraints based on horizontal_relation
     - For vertical: top/bottom constraints based on vertical_relation
   - Reconstructs the main area using available constraints
   - More resilient to visual changes but requires good anchor distribution

3. **Low-Confidence Matching (Second Fallback)**:
   - If anchor reconstruction fails but a low-confidence sliding window match exists,
     uses that match as a best-effort solution

4. **Scaled Original (Last Resort)**:
   - If all methods fail, scales the original main area proportionally to the new image dimensions
   - Provides a basic fallback when no other method succeeds

### Confidence Calculation
- **Sliding Window Matching**: Cosine similarity between embeddings
- **Anchor Reconstruction**: Combination of anchor count and matching scores

## Integration and Usage

### Training
```python
# Create detector
detector = AnchorBasedMainAreaDetector()

# Train with frames
result = detector.train_with_frames(
    results_list=omniparser_results,
    save_dir="./model_directory"
)

if result["success"]:
    print(f"Training successful. Found {len(result['anchor_points'])} anchor points.")
    print(f"Main area: {result['main_area']} (source: {result['area_source']})")
```

### Detection
```python
# Create runtime detector
runtime_detector = AnchorBasedMainAreaDetectorRuntime()

# Detect main area in a new frame
detection_result = runtime_detector.detect(
    result_model=omniparser_result,
    model_dir="./model_directory"
)

if detection_result["success"]:
    print(f"Detection method: {detection_result['method']}")
    print(f"Confidence: {detection_result['confidence']}")
    print(f"Detected main area: {detection_result['main_area']}")
```

## Testing Implementation

The system includes a comprehensive test file (`anchor_based_main_area_detector_test.py`).

### Running the Test
```python
# Basic test
test_anchor_based_detector()

# Test with viewport
test_anchor_based_detector(use_viewport=True)
```

### Test Process
1. Loads real screenshot events from a JSON file
2. Trains the detector on multiple frames
3. Tests detection on the same frames
4. Creates visualizations to explain the system

### Visualizations
The test creates several visualizations to explain how the system works:

1. **Main Area References**: Shows the original main area and extracted reference patches
2. **Anchor Points**: Displays all anchor points on the original image and individual patches
3. **Anchor Relationships**: Illustrates spatial relationships between anchors and the main area
4. **Sliding Window Matching**: Visualizes the sliding window approach with multiple window sizes
5. **Reconstruction Simulation**: Shows how the system would reconstruct the main area using only anchor constraints
6. **Detection Workflow**: Comprehensive workflow diagram explaining the full detection pipeline

### Understanding the Reconstruction Simulation
The reconstruction simulation specifically shows what would happen if sliding window matching failed and the system had to rely only on anchor points. It's divided into four quadrants:

1. **Original Main Area** (top-left): The reference main area detected during training
2. **Horizontal Constraints** (top-right): Shows horizontal constraints from anchors
3. **Vertical Constraints** (bottom-left): Shows vertical constraints from anchors
4. **Reconstructed Main Area** (bottom-right): Shows the reconstructed area based only on anchor constraints compared to the original

The IoU (Intersection over Union) score shows the overlap between the original and reconstructed areas. This simulation helps identify if more or better-distributed anchor points are needed.

## Performance Considerations

- **Sliding Window Matching**: Fast and precise when configured correctly, but can be computationally intensive
- **Anchor Reconstruction**: More robust to content changes but requires good anchor distribution
- **Window Sizes**: Smaller sliding window steps yield more precise results but increase processing time
- **Training Frequency**: The system should be retrained periodically as the UI evolves
- **Anchor Diversity**: For best results, ensure anchors cover all four directions (top, bottom, left, right)

## Troubleshooting

### Poor Detection Performance
- **Check Anchor Distribution**: Ensure anchors represent all four directions
- **Examine Anchor Stability**: Look for high stability scores (ideally > 0.8)
- **Verify Main Area References**: Ensure references cover diverse states of the UI
- **Increase Training Frames**: More training frames can improve stability detection
- **Adjust Sliding Window Parameters**: Try different window sizes and step counts

### Failed Sliding Window Matching
- **Lower Match Threshold**: Try reducing `main_area_match_threshold`
- **Add More Window Sizes**: Expand the `sliding_window_sizes` range
- **Increase Window Steps**: More steps provide finer granularity in matching
- **Add More References**: Increase `max_main_area_references`
- **Retrain with Diverse Frames**: Include frames with different states of the UI

### Failed Anchor Reconstruction
- **Increase Anchor Points**: Try increasing `max_anchor_points`
- **Improve Anchor Distribution**: Ensure anchors cover all sides of the main area
- **Lower Anchor Match Threshold**: Try reducing `anchor_match_threshold`

## File Structure

```
inference/omniparser/
├── anchor_based_main_area_detector.py       # Training component
├── anchor_based_main_area_detector_runtime.py  # Detection component
├── anchor_based_main_area_detector_test.py  # Test implementation
└── ANCHOR_BASED_MAIN_AREA_README.md         # This documentation
```
