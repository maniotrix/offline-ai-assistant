# Content Detection System

This package provides a content-based segmentation system for detecting the most relevant content areas within UI screenshots. It builds on top of the dynamic area detection to provide more accurate and granular content identification.

## Components

### 1. Main Area Segmenter (`main_area_segmenter.py`)

The `MainAreaSegmenter` class takes a detected main area from the dynamic area detector and performs content-based clustering to identify meaningful content regions within it.

Key features:
- Divides the main area into a grid of patches
- Extracts multi-modal features (text, visual, structural)
- Uses clustering to group similar content regions
- Scores clusters based on content significance
- Generates a content probability heatmap

### 2. Content Detector (`content_detector.py`)

The `ContentDetector` integrates the dynamic area detection with content-based segmentation to provide a complete content detection solution.

Key features:
- First uses the `UIOptimizedDynamicAreaDetector` to find the main area
- Then applies the `MainAreaSegmenter` to identify content clusters within that area
- Falls back to dynamic detection results if segmentation fails
- Provides visualization utilities

## How It Works

1. **Dynamic Area Detection**: First identifies the general main content area using frame differencing and UI-specific optimizations.

2. **Grid-based Feature Extraction**: Divides the main area into a grid and extracts features from each cell:
   - Text features (density, length)
   - Visual features (color variance, edge density)
   - Structural features (UI element density and types)
   - Spatial features (position within the main area)

3. **Multi-level Clustering**:
   - Initial DBSCAN clustering based on feature similarity
   - Hierarchical merging of related clusters

4. **Content Scoring**:
   - Scores clusters based on weighted feature importance
   - Prioritizes text-rich, visually complex, structurally coherent regions
   - Considers spatial positioning (center bias)

5. **Content Map Generation**:
   - Creates a heatmap showing content probability distribution
   - Identifies a primary content area as most significant cluster

## Usage

```python
from omniparser.content_detector import ContentDetector
from PIL import Image

# Initialize detector
detector = ContentDetector()

# Run detection on a sequence of frames
result = detector.detect(omniparser_results)

# Access the detected main content area
main_content_bbox = result["main_content_bbox"]

# Access content clusters for more detailed analysis
clusters = result["content_segmentation"]["clusters"]

# Generate visualization
detector.visualize(result, image_path, output_path)
```

## Example

See `examples/content_detection_example.py` for a complete example of how to use the content detection system.

## Benefits

- Works across different UI types without app-specific templates
- Focuses on actual content characteristics rather than just UI structure
- Provides both coarse (main area) and fine-grained (content clusters) detection
- Combines multiple feature types for more robust detection
- Generates visual feedback for inspection and debugging

## Future Improvements

- Neural feature extraction for better content characterization
- Temporal analysis across frames for content tracking
- User feedback integration for model refinement
- App-specific templates as optional enhancement 