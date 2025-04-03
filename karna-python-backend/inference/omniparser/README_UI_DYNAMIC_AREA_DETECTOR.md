# UI-Optimized Dynamic Area Detector

## Overview
The `UIOptimizedDynamicAreaDetector` extends the base `DynamicAreaDetector` with specialized methods for identifying dynamic content areas in UI layouts. It is particularly optimized for vertical UI structures where content typically scrolls vertically, such as web pages, chat interfaces, and mobile apps.

## Features
All features from the base `DynamicAreaDetector`, plus:
- **Vertical union detection** for identifying content areas that span vertically
- **UI-optimized region grouping** based on horizontal overlap
- **Main content area detection** with special handling for vertical layouts
- **Integration with existing UI layout knowledge** to better isolate scrollable content areas

## Main Class
- `UIOptimizedDynamicAreaDetector`: Extends `DynamicAreaDetector` with UI-specific optimizations

## Usage

```python
from ui_dynamic_area_detector import UIOptimizedDynamicAreaDetector
from omni_helper import OmniParserResultModelList

# Initialize UI-optimized detector with custom parameters
detector = UIOptimizedDynamicAreaDetector(
    x_overlap_threshold=0.3,        # Minimum horizontal overlap required 
    min_vertical_region_height=0.1, # Minimum height for vertical regions
    min_change_frequency=0.3,       # From base class
    min_area_size=0.01,             # From base class
    grouping_distance=0.1           # From base class
)

# Detect main dynamic areas with UI optimizations
result = detector.detect_main_areas(omniparser_results_list)

# Access additional UI-optimized areas
vertical_union = result["vertical_union"]     # Union of regions that span vertically
main_content = result["main_content_area"]    # Main content area (optimized for UI)

# Base class results are also available
largest_area = result["largest_area"]        
center_area = result["center_weighted"]      
highest_freq = result["highest_frequency"]   
all_regions = result["all_regions"]          
```

## Parameters

### Constructor Parameters
- `x_overlap_threshold`: Minimum horizontal overlap required to merge regions vertically (0-1)
- `min_vertical_region_height`: Minimum height for vertical regions as fraction of screen (0-1)
- All parameters from the base `DynamicAreaDetector` class are also supported

## How It Works

1. **Base Detection**:
   - First, the base `DynamicAreaDetector` algorithm is applied to identify all dynamic regions

2. **Vertical Union Creation**:
   - Regions with significant horizontal overlap are grouped
   - For each group, a vertical union is created spanning the entire vertical range
   - The largest region is used as a seed to ensure it's included in a group

3. **X-Overlap Calculation**:
   - A specialized method calculates the percentage of horizontal overlap between regions
   - This helps identify regions that are vertically aligned in a UI layout

4. **Main Content Area Selection**:
   - A vertical union containing the largest dynamic area is prioritized
   - If no such union exists, one is created to encompass the largest area
   - Selection considers area size, central position, and vertical span
   - The goal is to identify the main scrollable content area in the UI

## Additional Result Fields

In addition to all fields from the base detector, the results include:
- `vertical_union`: Bounding box of the vertical union region [x1, y1, x2, y2]
- `main_content_area`: Bounding box of the detected main content area, optimized for UI layouts

## Use Cases

The UI-optimized detector is particularly useful for:
- Web pages with vertical scrolling content
- Chat applications where messages appear in a scrollable area
- Social media feeds with vertically arranged posts
- Mobile applications with vertical content layouts
- Any UI with a clear main content area that changes while surrounding UI elements remain static

## Integration Notes

- This detector is best used when you know the UI has a vertical layout structure
- It works well with OmniParserResultModelList containing results from multiple frames
- For best results, provide frames that show scrolling or content changes in the main area
- The detector automatically prioritizes larger vertical regions near the center of the screen 