# Image Similarity for Icon Comparison

This module provides functionality for comparing icons across different themes by generating embeddings and calculating similarity scores.

## Overview

The `ResNetImageEmbedder` class is designed to generate embeddings for images, particularly UI icons, and compare their similarity regardless of visual style differences. This allows detecting functionally similar icons (e.g., search icons) across different themes (light/dark) or visual designs.

## Features

- Generate embeddings for images using pre-trained ResNet models
- Support for multiple ResNet variants (ResNet-18, ResNet-34, ResNet-50)
- Extract features from intermediate layers for better semantic representation
- Calculate cosine similarity between images
- Batch processing for multiple images
- Generation of similarity matrices

## Implementation Details

The implementation:
1. Uses pre-trained ResNet models from torchvision
2. Extracts features from the 'avgpool' layer by default, which provides good semantic representation
3. Normalizes embeddings to unit length for reliable similarity calculations
4. Provides cosine similarity as the similarity metric

## Usage

### Basic Usage

```python
from PIL import Image
from image_comparison import ResNetImageEmbedder

# Initialize the embedder
embedder = ResNetImageEmbedder()

# Load two images
img1 = Image.open("light_theme_icon.png")
img2 = Image.open("dark_theme_icon.png")

# Calculate similarity score
similarity = embedder.get_similarity(img1, img2)
print(f"Similarity score: {similarity:.4f}")
```

### Advanced Options

```python
# Use a deeper model for potentially better accuracy
embedder = ResNetImageEmbedder(model_name='resnet50')

# Extract features from a different layer
embedder = ResNetImageEmbedder(layer_name='layer4')

# Specify the device to use
embedder = ResNetImageEmbedder(device='cuda:0')
```

### Batch Processing

```python
# Load multiple images
images = [Image.open(path) for path in image_paths]

# Get embeddings for all images
embeddings = embedder.batch_get_embeddings(images)

# Compute pairwise similarity matrix
similarity_matrix = embedder.batch_compute_similarity_matrix(images)
```

## Testing

The `image_comparison_test.py` script demonstrates:
- Comparing different models (ResNet-18 vs ResNet-50)
- Testing similarities between light and dark theme versions of the same icon
- Generating similarity matrices for multiple images
- Visualizing similarity results

Run the test script with:
```
python image_comparison_test.py
```

## Performance Considerations

- ResNet-18 offers a good balance between accuracy and speed
- Consider using smaller models for faster inference when processing many images
- For high-accuracy tasks, the deeper models like ResNet-50 may perform better

## Future Improvements

Potential enhancements:
1. Support for more backbone models (EfficientNet, MobileNet)
2. Add CLIP-based embeddings for better semantic understanding
3. Fine-tuning options for specific icon comparison tasks
4. Threshold-based similarity grouping for icon clustering 