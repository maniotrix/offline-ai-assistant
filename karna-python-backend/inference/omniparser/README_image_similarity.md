# Image Similarity for Icon Comparison

This module provides functionality for comparing icons across different themes by generating embeddings and calculating similarity scores.

## Overview

The `ResNetImageEmbedder` class is designed to generate embeddings for images, particularly UI icons, and compare their similarity regardless of visual style differences. This allows detecting functionally similar icons (e.g., search icons) across different themes (light/dark) or visual designs.

## Features

- Generate embeddings for images using pre-trained ResNet models
- Support for multiple ResNet variants (ResNet-18, ResNet-34, ResNet-50)
- Extract features from intermediate layers for better semantic representation
- Calculate cosine similarity between images
- Automatic classification of similarity scores into meaningful categories
- Batch processing for multiple images
- Generation of similarity matrices

## Implementation Details

The implementation:
1. Uses pre-trained ResNet models from torchvision
2. Extracts features from the 'avgpool' layer by default, which provides good semantic representation
3. Normalizes embeddings to unit length for reliable similarity calculations
4. Provides cosine similarity as the similarity metric
5. Includes pre-calibrated thresholds for similarity classifications

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

# Get similarity with automatic classification
result = embedder.get_similarity_with_classification(img1, img2)
print(f"Score: {result['score']:.4f}, Classification: {result['classification']}")
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

# Get classification matrix
classification_matrix = embedder.batch_classify_similarity_matrix(similarity_matrix)
```

### Similarity Classification

The embedder uses model-specific thresholds to classify similarity scores into four categories:

1. **identical**: Icons are functionally the same with high confidence (same icon in different themes)
2. **similar**: Icons likely have the same functionality (high likelihood of functional equivalence)
3. **related**: Icons may be related or have similar functionality
4. **different**: Icons likely have different functionality

Example usage:
```python
classification = embedder.classify_similarity(0.83)  # Returns "similar" or "identical" depending on model
```

## Testing

The `image_comparison_test.py` script demonstrates:
- Comparing different models (ResNet-18 vs ResNet-50)
- Testing similarities between light and dark theme versions of the same icon
- Measuring performance metrics (time taken for embedding generation and comparison)
- Visualizing similarity results
- Demonstrating similarity classification for different icon pairs

Run the test script with:
```
python image_comparison_test.py
```

## Performance Benchmarking

A dedicated benchmarking script (`benchmarking.py`) is provided to help evaluate and compare the performance of different models and configurations:

- Measures initialization time, embedding generation time, and similarity calculation time
- Compares different ResNet variants (ResNet-18, ResNet-34, ResNet-50)
- Tests different feature extraction layers (avgpool, layer4, layer3)
- Generates visualizations of performance metrics
- Outputs a comprehensive performance report

Run the benchmarking script with:
```
python benchmarking.py
```

## Test Results and Findings

Our testing revealed several important insights:

### Similarity Detection Performance

- Both ResNet-18 and ResNet-50 successfully identified light/dark theme variations of the same icon
- ResNet-50 produced similarity scores of ~0.85 for theme variations (vs ~0.83 for ResNet-18)
- Layer choice affects discrimination capability - avgpool provides the best balance

### Model Performance Comparison

| Model     | Layer   | Embedding Size | Avg Time/Image | Similarity Accuracy |
|-----------|---------|----------------|----------------|---------------------|
| ResNet-18 | avgpool | 512           | 30-60ms        | Good                |
| ResNet-18 | layer4  | 25,088        | 10-15ms        | Very Good           |
| ResNet-18 | layer3  | 50,176        | 8-12ms         | Good                |
| ResNet-50 | avgpool | 2,048         | 60-90ms        | Very Good           |
| ResNet-50 | layer4  | 100,352       | 18-25ms        | Excellent           |
| ResNet-50 | layer3  | 200,704       | 15-20ms        | Good                |

### Recommended Similarity Thresholds

#### For ResNet-18 with avgpool:
- **>0.80**: High confidence these are the same functional icons
- **0.65-0.80**: Likely functional similarity
- **0.45-0.65**: Moderate similarity
- **<0.45**: Different functionality

#### For ResNet-50 with avgpool:
- **>0.85**: Very high confidence these are functionally identical icons
- **0.70-0.85**: High likelihood of functional similarity
- **0.50-0.70**: Moderate similarity
- **<0.50**: Likely different functionality

*Note: These thresholds should be validated with your specific icon dataset.*

## Guidelines for Model Selection

### Choose ResNet-18 with avgpool when:
- You need a good balance between speed and accuracy
- Processing large numbers of icons quickly is important
- Memory usage is a concern
- Basic functional similarity detection is sufficient

### Choose ResNet-18 with layer4 when:
- You need faster processing with high accuracy
- You can handle larger embedding dimensions
- Your application requires more detailed feature extraction

### Choose ResNet-50 with avgpool when:
- Accuracy is more important than speed
- You need higher discrimination between similar icons
- The additional processing time (2-3x slower than ResNet-18) is acceptable
- You want the most reliable similarity scores

### Choose ResNet-50 with layer4 when:
- You need the highest possible accuracy
- You can handle very large embedding dimensions
- Your hardware supports efficient processing of larger models
- Performance is not the primary concern

## Performance Considerations

Based on benchmarking results:

- ResNet-18 offers the fastest embedding generation (typically 20-50ms per image on CPU)
- ResNet-50 provides larger embeddings but is 2-3x slower than ResNet-18
- The 'avgpool' layer offers a good balance between semantic representation and speed
- Using 'layer3' or 'layer4' may capture more detailed features but generates much larger embeddings
- For most icon comparison tasks, ResNet-18 with the default 'avgpool' layer provides the best speed/accuracy tradeoff

### Typical Performance Metrics (CPU)

| Model    | Embedding Time | Comparison Time | Embedding Dimension |
|----------|----------------|----------------|---------------------|
| ResNet-18 | 20-50ms        | 0.1-0.5ms      | 512                 |
| ResNet-34 | 40-80ms        | 0.1-0.5ms      | 512                 |
| ResNet-50 | 60-120ms       | 0.2-0.6ms      | 2048                |

*Note: These are approximate values. Actual performance depends on hardware and image size.*

## Unexpected Findings

Our testing revealed some surprising results:

1. **Deeper layers sometimes faster**: In some tests, extracting from deeper layers (layer3, layer4) was faster than avgpool, despite producing larger embeddings.

2. **Initialization time variance**: Model initialization time varied significantly between models (ResNet-18: ~380ms, ResNet-34: ~5000ms).

3. **Batch vs. single processing**: For some configurations, batch processing showed minimal advantage over sequential processing.

## Future Improvements

Potential enhancements:
1. Support for more backbone models (EfficientNet, MobileNet)
2. Add CLIP-based embeddings for better semantic understanding
3. Fine-tuning options for specific icon comparison tasks
4. Threshold-based similarity grouping for icon clustering
5. Model quantization for improved inference speed
6. Adaptive thresholding based on specific icon categories 