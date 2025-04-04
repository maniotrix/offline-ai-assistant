import os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from image_comparison import ResNetImageEmbedder

def test_icon_similarity():
    """
    Test the similarity calculation between icon images.
    The function will load test images, compute their embeddings,
    and calculate similarity scores.
    """
    # Initialize the embedder with different models for comparison
    embedders = {
        'resnet18': ResNetImageEmbedder(model_name='resnet18'),
        'resnet50': ResNetImageEmbedder(model_name='resnet50')
    }
    
    # Path to test images
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to load test images from the current directory
    try:
        # Test different theme variations if available
        light_dark_pairs = [
            ["chatgpt_light_theme_test.png", "chatgpt_dark_theme_test.png"],
        ]
        
        all_img_paths = []
        for pair in light_dark_pairs:
            for img_name in pair:
                img_path = os.path.join(test_dir, img_name)
                if os.path.exists(img_path):
                    all_img_paths.append(img_path)
                else:
                    print(f"Warning: Image file not found: {img_path}")
        
        # Add other test images if available
        additional_images = ["10_AAsk anything.png","38_Up_or_down.png", "44_Copy.png"]
        for img_name in additional_images:
            img_path = os.path.join(test_dir, img_name)
            if os.path.exists(img_path):
                all_img_paths.append(img_path)
            else:
                print(f"Warning: Image file not found: {img_path}")
        
        if not all_img_paths:
            print("No test images found. Please make sure the test images exist.")
            return
        
        # Load the images
        images = [Image.open(path) for path in all_img_paths]
        image_names = [os.path.basename(path) for path in all_img_paths]
        
        print(f"\nPerformance comparison - {len(images)} images:")
        print("-" * 60)
        print(f"{'Model':<10} | {'Avg Embed Time (ms)':<20} | {'Batch Time (ms)':<20} | {'Similarity Time (ms)':<20}")
        print("-" * 60)
        
        # Test each model
        for model_name, embedder in embedders.items():
            print(f"\n=== Testing {model_name} ===")
            
            # Time individual embedding generation
            embed_times = []
            for image in images:
                start_time = time.time()
                _ = embedder.get_embedding(image)
                end_time = time.time()
                embed_times.append((end_time - start_time) * 1000)  # Convert to ms
            
            avg_embed_time = sum(embed_times) / len(embed_times)
            
            # Time batch embedding generation
            start_time = time.time()
            embeddings = embedder.batch_get_embeddings(images)
            end_time = time.time()
            batch_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Time similarity matrix computation
            start_time = time.time()
            similarity_matrix = embedder.batch_compute_similarity_matrix(images)
            end_time = time.time()
            similarity_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Add to performance table
            print(f"{model_name:<10} | {avg_embed_time:<20.2f} | {batch_time:<20.2f} | {similarity_time:<20.2f}")
            
            # Time pairwise similarity
            print("\nPairwise timing tests:")
            for i in range(len(images)):
                for j in range(i+1, len(images)):
                    start_time = time.time()
                    similarity = embedder.get_similarity(images[i], images[j])
                    end_time = time.time()
                    comparison_time = (end_time - start_time) * 1000  # Convert to ms
                    print(f"  {image_names[i]} ↔ {image_names[j]}: {similarity:.4f} (took {comparison_time:.2f} ms)")
            
            # Print results
            print("\nSimilarity matrix:")
            print(np.round(similarity_matrix, 4))
            
            # Print pairwise similarity for each pair
            print("\nPairwise similarities with classification:")
            for i in range(len(images)):
                for j in range(i+1, len(images)):
                    similarity_result = embedder.get_similarity_with_classification(images[i], images[j])
                    score = similarity_result['score']
                    classification = similarity_result['classification']
                    print(f"  {image_names[i]} ↔ {image_names[j]}: {score:.4f} ({classification})")
            
            # Demonstrate the classification matrix
            print("\nClassification matrix:")
            classification_matrix = embedder.batch_classify_similarity_matrix(similarity_matrix)
            
            # Pretty print the classification matrix
            print("    " + " | ".join(f"{name:<12}" for name in image_names))
            print("    " + "-" * (16 * len(image_names)))
            for i, row_name in enumerate(image_names):
                row_values = " | ".join(f"{classification_matrix[i, j]:<12}" for j in range(len(image_names)))
                print(f"{row_name:<4} {row_values}")
            
            # Visualize the similarity matrix if we have matplotlib
            try:
                plt.figure(figsize=(10, 8))
                plt.imshow(similarity_matrix, cmap='viridis', vmin=0, vmax=1)
                plt.colorbar(label='Similarity')
                plt.xticks(range(len(image_names)), image_names, rotation=45, ha='right')
                plt.yticks(range(len(image_names)), image_names)
                plt.title(f'Image Similarity Matrix ({model_name})')
                plt.tight_layout()
                plt.savefig(os.path.join(test_dir, f"similarity_matrix_{model_name}.png"))
                print(f"\nSimilarity matrix visualization saved to similarity_matrix_{model_name}.png")
            except Exception as e:
                print(f"Could not visualize similarity matrix: {e}")
            
            # Test specific theme pairs
            print("\nTheme similarity tests with classification:")
            for pair in light_dark_pairs:
                if all(os.path.exists(os.path.join(test_dir, img)) for img in pair):
                    img1 = Image.open(os.path.join(test_dir, pair[0]))
                    img2 = Image.open(os.path.join(test_dir, pair[1]))
                    
                    start_time = time.time()
                    similarity_result = embedder.get_similarity_with_classification(img1, img2)
                    end_time = time.time()
                    theme_comparison_time = (end_time - start_time) * 1000  # Convert to ms
                    
                    score = similarity_result['score']
                    classification = similarity_result['classification']
                    print(f"  {pair[0]} ↔ {pair[1]}: {score:.4f} ({classification}) (took {theme_comparison_time:.2f} ms)")
                else:
                    print(f"  Skipping pair {pair} - files not found")
                
    except Exception as e:
        print(f"Error during test: {e}")

def main():
    """Main function to run the tests"""
    print("Testing ResNetImageEmbedder for icon similarity...")
    
    # Measure total execution time
    start_time = time.time()
    test_icon_similarity()
    end_time = time.time()
    
    total_time = end_time - start_time
    print(f"\nTests completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main() 