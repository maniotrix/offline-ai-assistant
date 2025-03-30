# PatchMatcher: UI Element Matching for OmniParser Results

The `PatchMatcher` class provides functionality for matching image patches against UI elements in `OmniParserResultModel` objects. It's particularly useful for identifying the same UI element across different screenshots or themes.

## Overview

PatchMatcher inherits from `ResNetImageEmbedder` and leverages the underlying image embedding capabilities to:

1. Take an image patch (e.g., a UI element from a screenshot)
2. Compare it against all UI elements in an OmniParserResultModel
3. Identify the best match based on visual similarity
4. Return detailed match information including the matched element ID and content

## Features

- **High-accuracy matching**: Uses ResNet-50 by default for robust visual similarity
- **Identical element detection**: Specialized method for finding exact matches
- **Threshold-based matching**: Configurable similarity threshold
- **Flexible comparison**: Works with elements of different sizes and visual appearances
- **Multi-model search**: Supports searching across multiple OmniParserResultModel objects
- **Detailed results**: Returns comprehensive match information, including the matched ParsedContentResult

## Usage

### Basic Usage

```python
from PIL import Image
from patch_matcher import PatchMatcher
from omni_helper import get_omniparser_inference_data_from_image_path

# Initialize the matcher
matcher = PatchMatcher(model_name='resnet50')

# Load an image patch to match
patch = Image.open("search_icon.png")

# Get OmniParser results for a screenshot
omniparser_result = get_omniparser_inference_data_from_image_path("screenshot.png")

# Find matching element
match_result = matcher.find_matching_element(patch, omniparser_result)

# Check if match was found
if match_result.match_found:
    print(f"Match found! Element ID: {match_result.matched_element_id}")
    print(f"Element content: {match_result.parsed_content_result.content}")
    print(f"Similarity score: {match_result.similarity_score:.4f}")
else:
    print("No match found")
```

### Finding Identical Elements

```python
# Use a higher threshold for identical matches
match_result = matcher.find_identical_element(patch, omniparser_result)
```

### Searching Across Multiple Results

```python
# Create list of OmniParserResultModel objects
result_models = [
    get_omniparser_inference_data_from_image_path("screenshot1.png"),
    get_omniparser_inference_data_from_image_path("screenshot2.png")
]

# Search for matches across all models
matches = matcher.match_patch_across_multiple_results(patch, result_models)

# Process all matches
for match in matches:
    print(f"Match found in model: {match.omniparser_result_model.event_id}")
    print(f"Element ID: {match.matched_element_id}")
```

### Extracting and Matching UI Elements

```python
# Load a screenshot
full_image = Image.open("screenshot.png")
omniparser_result = get_omniparser_inference_data_from_image_path("screenshot.png")

# Extract a UI element based on its bounding box
ui_element = omniparser_result.parsed_content_results[5]  # Any element
element_bbox = ui_element.bbox
element_image = matcher.extract_image_from_bbox(full_image, element_bbox)

# Now match this element in another screenshot
other_result = get_omniparser_inference_data_from_image_path("other_screenshot.png")
match_result = matcher.find_matching_element(element_image, other_result)
```

## Match Result Structure

The `PatchMatchResult` class provides detailed information about matches:

- `match_found`: Boolean indicating if a match was found
- `matched_element_id`: ID of the matched element (if found)
- `similarity_score`: Cosine similarity score (0-1 range)
- `classification`: Classification of the similarity ("identical", "similar", etc.)
- `parsed_content_result`: The full ParsedContentResult object that matched
- `omniparser_result_model`: The OmniParserResultModel containing the match

## Performance Considerations

- For highest accuracy, use ResNet-50 (default)
- For faster matching, use ResNet-18 (`model_name='resnet18'`)
- The default similarity threshold is 0.85, can be lowered for more permissive matching
- Matching is faster with fewer elements in the OmniParserResultModel
- Similarity scores are typically highest for identical elements (>0.9)
- Theme variations of the same element typically have scores around 0.7-0.85

## Testing

Run the included test script to see PatchMatcher in action:

```
python patch_matcher_test.py
```

The test demonstrates:
1. Loading a test image and parsing it with OmniParser
2. Extracting a UI element as a test patch
3. Finding the same element in the parsed results
4. Testing with a modified version of the patch (simulating theme variation)
5. Generating visualizations of the matching process

## Common Use Cases

1. **Theme-invariant element identification**: Find the same functional element across light/dark themes
2. **Cross-screen element tracking**: Track UI elements across different app screens
3. **Element verification**: Verify that a UI element exists in an app interface
4. **Similar functionality detection**: Group elements with similar functionality based on visual appearance 