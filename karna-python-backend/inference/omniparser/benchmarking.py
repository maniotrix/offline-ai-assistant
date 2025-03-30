import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from image_comparison import ResNetImageEmbedder

def load_test_images(directory):
    """Load test images from the given directory."""
    images = []
    image_names = []
    
    # First check if we have the ChatGPT test images
    test_pairs = [
        ["chatgpt_light_theme_test.png", "chatgpt_dark_theme_test.png"],
    ]
    for pair in test_pairs:
        for img_name in pair:
            img_path = os.path.join(directory, img_name)
            if os.path.exists(img_path):
                images.append(Image.open(img_path))
                image_names.append(img_name)
    
    # Then try to load any other PNG images in the directory
    for file in os.listdir(directory):
        if file.lower().endswith('.png') and file not in image_names:
            img_path = os.path.join(directory, file)
            try:
                img = Image.open(img_path)
                images.append(img)
                image_names.append(file)
            except Exception as e:
                print(f"Could not load {file}: {e}")
    
    print(f"Loaded {len(images)} test images: {', '.join(image_names)}")
    return images, image_names

def benchmark_models():
    """Benchmark different models and layers for embedding generation."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    images, image_names = load_test_images(test_dir)
    
    if not images:
        print("No test images found. Exiting.")
        return
    
    # Models and layers to test
    models_to_test = ['resnet18', 'resnet34', 'resnet50']
    layers_to_test = ['avgpool', 'layer4', 'layer3']
    
    # Prepare results dataframe
    results = []
    
    for model_name in models_to_test:
        for layer_name in layers_to_test:
            print(f"\nTesting {model_name} with {layer_name} layer...")
            
            # Initialize the model
            model_init_start = time.time()
            embedder = ResNetImageEmbedder(model_name=model_name, layer_name=layer_name)
            model_init_time = (time.time() - model_init_start) * 1000  # ms
            
            # Test single image embedding time (average of all images)
            single_embed_times = []
            for img in images:
                start_time = time.time()
                embedder.get_embedding(img)
                single_embed_times.append((time.time() - start_time) * 1000)  # ms
            avg_single_embed_time = sum(single_embed_times) / len(single_embed_times)
            
            # Test batch embedding time
            batch_start_time = time.time()
            embeddings = embedder.batch_get_embeddings(images)
            batch_time = (time.time() - batch_start_time) * 1000  # ms
            
            # Test similarity calculation time
            similarity_start_time = time.time()
            similarity_matrix = embedder.batch_compute_similarity_matrix(images)
            similarity_time = (time.time() - similarity_start_time) * 1000  # ms
            
            # Test pairwise similarity time (for the first two images if possible)
            pair_time = 0
            if len(images) >= 2:
                pair_start_time = time.time()
                embedder.get_similarity(images[0], images[1])
                pair_time = (time.time() - pair_start_time) * 1000  # ms
            
            # Calculate embedding dimension
            embedding_dim = embeddings[0].shape[0]
            
            # Store results
            results.append({
                'Model': model_name,
                'Layer': layer_name,
                'Initialization Time (ms)': model_init_time,
                'Single Embed Time (ms)': avg_single_embed_time,
                'Batch Embed Time (ms)': batch_time,
                'Similarity Matrix Time (ms)': similarity_time,
                'Pair Comparison Time (ms)': pair_time,
                'Embedding Dimension': embedding_dim
            })
    
    # Convert to DataFrame and show results
    results_df = pd.DataFrame(results)
    
    print("\n===== BENCHMARK RESULTS =====")
    print(results_df.to_string(index=False))
    
    # Save results
    results_df.to_csv(os.path.join(test_dir, 'embedding_benchmark_results.csv'), index=False)
    print(f"\nResults saved to {os.path.join(test_dir, 'embedding_benchmark_results.csv')}")
    
    # Visualize results
    try:
        # Create speed comparison plot
        plt.figure(figsize=(12, 6))
        
        # Set width of bars
        bar_width = 0.2
        
        # Set position on x-axis
        x = np.arange(len(models_to_test))
        
        for i, layer in enumerate(layers_to_test):
            # Filter data for this layer
            layer_data = results_df[results_df['Layer'] == layer]
            # Get the values by model
            values = [layer_data[layer_data['Model'] == model]['Single Embed Time (ms)'].values[0] 
                     for model in models_to_test]
            
            # Creating the bars
            plt.bar(x + i*bar_width, values, bar_width, label=f'{layer}')
        
        plt.xlabel('Model')
        plt.ylabel('Time (ms)')
        plt.title('Single Image Embedding Generation Time')
        plt.xticks(x + bar_width, models_to_test)
        plt.legend()
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(os.path.join(test_dir, 'embedding_speed_comparison.png'))
        print(f"Speed comparison visualization saved to {os.path.join(test_dir, 'embedding_speed_comparison.png')}")
        
        # Also visualize embedding dimensions
        plt.figure(figsize=(10, 5))
        for i, model in enumerate(models_to_test):
            dims = [results_df[(results_df['Model'] == model) & (results_df['Layer'] == layer)]['Embedding Dimension'].values[0]
                   for layer in layers_to_test]
            plt.bar(np.arange(len(layers_to_test)) + i*0.25, dims, 0.25, label=model)
        
        plt.xlabel('Layer')
        plt.ylabel('Embedding Dimension')
        plt.title('Embedding Dimensions by Model and Layer')
        plt.xticks(np.arange(len(layers_to_test)) + 0.25, layers_to_test)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(test_dir, 'embedding_dimensions.png'))
        print(f"Embedding dimensions visualization saved to {os.path.join(test_dir, 'embedding_dimensions.png')}")
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")
    
    return results_df

def main():
    """Main function to run the benchmarks."""
    print("Starting embedding model benchmarks...")
    start_time = time.time()
    
    benchmark_models()
    
    total_time = time.time() - start_time
    print(f"\nBenchmarks completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main() 