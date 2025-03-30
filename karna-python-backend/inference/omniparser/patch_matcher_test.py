import os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from patch_matcher import PatchMatcher, PatchMatchResult
from omni_helper import get_omniparser_inference_data_from_image_path, OmniParserResultModel

def test_patch_matching_across_themes():
    """
    Test the PatchMatcher class by:
    1. Loading a specific icon patch (38_Up or down.png)
    2. Comparing it against elements in both ChatGPT light and dark theme screenshots
    """
    # Initialize the matcher with ResNet-50 (recommended for accuracy)
    patch_matcher = PatchMatcher(model_name='resnet50', similarity_threshold=0.70)  # Lower threshold for cross-theme matching
    
    # Path to test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to patch file
    patch_path = os.path.join(test_dir, "38_Up or down.png")
    if not os.path.exists(patch_path):
        print(f"Patch file not found: {patch_path}")
        return
    
    # Load the patch image
    try:
        patch_image = Image.open(patch_path)
        print(f"Loaded patch image: {patch_path}")
    except Exception as e:
        print(f"Error loading patch image: {e}")
        return
    
    # ChatGPT theme files to compare against
    theme_files = ["chatgpt_light_theme_test.png", "chatgpt_dark_theme_test.png"]
    theme_results = []
    
    # Process each theme file
    for theme_file in theme_files:
        theme_path = os.path.join(test_dir, theme_file)
        if not os.path.exists(theme_path):
            print(f"Theme file not found: {theme_path}")
            continue
        
        try:
            print(f"\nProcessing theme file: {theme_file}...")
            start_time = time.time()
            theme_result = get_omniparser_inference_data_from_image_path(theme_path)
            processing_time = time.time() - start_time
            print(f"OmniParser processing completed in {processing_time:.2f} seconds")
            print(f"Found {len(theme_result.parsed_content_results)} UI elements")
            
            theme_results.append((theme_file, theme_result))
        except Exception as e:
            print(f"Error processing theme file {theme_file}: {e}")
    
    if not theme_results:
        print("No theme files were successfully processed. Exiting test.")
        return
    
    # Display information about the patch
    print(f"\nPatch details - {os.path.basename(patch_path)}:")
    print(f"Image size: {patch_image.size}")
    
    # Create a figure to display all images and results
    plt.figure(figsize=(15, 10))
    plt.subplot(1, len(theme_results) + 1, 1)
    plt.imshow(patch_image)
    plt.title("Patch Image\n38_Up or down.png")
    plt.axis('off')
    
    # Match the patch against each theme
    match_results = []
    
    for idx, (theme_file, theme_result) in enumerate(theme_results):
        print(f"\nMatching patch against {theme_file}...")
        start_time = time.time()
        match_result = patch_matcher.find_matching_element(patch_image, theme_result)
        matching_time = time.time() - start_time
        
        match_results.append((theme_file, match_result))
        print(f"Matching completed in {matching_time:.2f} seconds")
        
        # Load the full theme image for visualization
        theme_image = Image.open(os.path.join(test_dir, theme_file))
        
        # Display match result
        if match_result.match_found:
            print(f"Match found in {theme_file}!")
            print(f"Matched element ID: {match_result.matched_element_id}")
            print(f"Similarity score: {match_result.similarity_score:.4f}")
            print(f"Classification: {match_result.classification}")
            print(f"Matched content: {match_result.parsed_content_result.content}")
            
            # Extract the matched element for visualization
            matched_bbox = match_result.parsed_content_result.bbox
            matched_img = patch_matcher.extract_image_from_bbox(theme_image, matched_bbox)
            
            # Add to visualization
            plt.subplot(1, len(theme_results) + 1, idx + 2)
            plt.imshow(matched_img)
            plt.title(f"Match in {theme_file}\nID: {match_result.matched_element_id}\nScore: {match_result.similarity_score:.4f}\nClass: {match_result.classification}")
            plt.axis('off')
        else:
            print(f"No match found in {theme_file}")
            
            # Add empty placeholder to visualization
            plt.subplot(1, len(theme_results) + 1, idx + 2)
            plt.text(0.5, 0.5, "No match found", horizontalalignment='center', verticalalignment='center')
            plt.axis('off')
    
    # Save the visualization
    plt.tight_layout()
    plt.savefig(os.path.join(test_dir, "patch_matching_themes_test.png"))
    print("\nTest visualization saved to patch_matching_themes_test.png")
    
    # Compare results across themes
    if len(match_results) > 1:
        print("\n=== Cross-Theme Comparison ===")
        found_matches = [result for _, result in match_results if result.match_found]
        
        if len(found_matches) > 1:
            print(f"Successfully found matches in {len(found_matches)} theme variations")
            
            # Compare the content of matched elements
            contents = [result.parsed_content_result.content for result in found_matches]
            if len(set(contents)) == 1:
                print(f"All matched elements have the same content: '{contents[0]}'")
            else:
                print("Matched elements have different content:")
                for idx, (theme_file, match_result) in enumerate(match_results):
                    if match_result.match_found:
                        print(f"  {theme_file}: '{match_result.parsed_content_result.content}'")
            
            # Compare similarity scores
            scores = [result.similarity_score for result in found_matches]
            print(f"Similarity scores: {[f'{score:.4f}' for score in scores]}")
            print(f"Average similarity: {sum(scores) / len(scores):.4f}")
            print(f"Score difference: {max(scores) - min(scores):.4f}")
        elif len(found_matches) == 1:
            matched_theme = next(theme_file for theme_file, result in match_results if result.match_found)
            print(f"Found match only in {matched_theme}")
            print(f"Consider lowering the similarity threshold for cross-theme matching")
        else:
            print("No matches found in any theme variation")
            print("Consider lowering the similarity threshold or checking if the element exists in the screenshots")

def main():
    """Main function to run the tests"""
    print("Testing PatchMatcher for cross-theme UI element matching...")
    
    # Measure total execution time
    start_time = time.time()
    test_patch_matching_across_themes()
    end_time = time.time()
    
    total_time = end_time - start_time
    print(f"\nTests completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main() 