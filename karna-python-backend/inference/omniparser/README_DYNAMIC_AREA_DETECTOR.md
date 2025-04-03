# Dynamic Area Detector

## Overview
The `DynamicAreaDetector` is a component for identifying dynamic content areas within UI screenshots by analyzing changes across multiple frames. It detects regions that change frequently, helping to isolate the main content areas from static UI elements like headers, sidebars, and navigation.

## Features
- **Change tracking** across multiple consecutive frames
- **Heatmap generation** to visualize change frequency
- **Region extraction** based on significant change frequency
- **Intelligent grouping** of nearby change regions
- **Multiple selection criteria** for identifying key areas:
  - Largest area
  - Center-weighted importance
  - Highest change frequency
- **Saliency scoring** to prioritize important regions based on size, position, and change frequency

## Main Classes
- `ChangeFrequencyRegion`: Represents a region with change frequency data
- `DynamicAreaDetector`: Main detector class implementing the detection algorithm

## Usage

```python
from dynamic_area_detector import DynamicAreaDetector
from omni_helper import OmniParserResultModelList

# Initialize detector with custom parameters
detector = DynamicAreaDetector(
    min_change_frequency=0.3,  # Minimum change frequency to consider dynamic (0-1)
    min_area_size=0.01,        # Minimum area size as fraction of screen  
    grouping_distance=0.1      # Distance threshold for grouping regions
)

# Detect main dynamic areas
result = detector.detect_main_areas(omniparser_results_list)

# Access different area selections
largest_area = result["largest_area"]        # Largest dynamic area by size
center_area = result["center_weighted"]      # Area prioritizing center position
highest_freq = result["highest_frequency"]   # Area with highest change frequency
all_regions = result["all_regions"]          # All detected dynamic regions
```

## Parameters

### Constructor Parameters
- `image_diff_creator`: Optional ImageDiffCreator instance (created if None)
- `min_change_frequency`: Minimum frequency of changes to consider an area dynamic (0-1)
- `min_area_size`: Minimum area size as fraction of screen area (0-1)
- `grouping_distance`: Distance threshold for grouping nearby regions (0-1)
- `min_saliency`: Minimum saliency threshold for regions (0-1)

## How It Works

1. **Frame Comparison**:
   - Each consecutive frame pair is compared using the ImageDiffCreator
   - Changes between frames are recorded with their positions and types

2. **Change Heatmap Generation**:
   - A 2D heatmap is generated to visualize change frequency across all frames
   - Higher values indicate areas that change more frequently

3. **Region Extraction**:
   - Regions with significant change frequency are extracted
   - Regions that are too small or change too infrequently are filtered out

4. **Region Grouping**:
   - Nearby regions are grouped to form larger coherent areas
   - Groups are formed based on proximity and intersection

5. **Main Area Selection**:
   - Different selection criteria are applied to identify key dynamic areas
   - Results include largest area, center-weighted, and highest frequency

## Result Format

The result is a dictionary with the following keys:
- `largest_area`: Bounding box of the largest dynamic area [x1, y1, x2, y2]
- `center_weighted`: Bounding box prioritizing center position and size
- `highest_frequency`: Bounding box of the area with highest change frequency
- `all_regions`: List of all detected dynamic region bounding boxes

## Integration Notes

- The detector works with OmniParserResultModelList containing results for multiple frames
- It requires at least 2 frames for meaningful detection
- It leverages ImageDiffCreator for frame comparison
- Regions are normalized to the range [0,1] relative to image dimensions 