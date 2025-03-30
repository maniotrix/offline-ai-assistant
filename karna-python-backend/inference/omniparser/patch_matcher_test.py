import os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from patch_matcher import PatchMatcher, PatchMatchResult, KNOWN_SOURCE_TYPES
from omni_helper import get_omniparser_inference_data_from_image_path, OmniParserResultModel

def test_patch_matching_across_themes():
    """
    Test the PatchMatcher class with source filtering by:
    1. Loading a specific icon patch (38_Up or down.png)
    2. Comparing it against elements in both ChatGPT light and dark theme screenshots
    3. Testing with different source type filters
    """
    # Initialize the matcher with ResNet-50 (recommended for accuracy)
    # Initially accept all source types
    patch_matcher = PatchMatcher(
        model_name='resnet50', 
        similarity_threshold=0.70,  # Lower threshold for cross-theme matching
        source_types=None  # Use all source types initially
    )
    
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
    
    # Test with different source type configurations
    source_type_tests = [
        ("All Sources", None),
        ("OCR Source", ["box_ocr_content_ocr"]),
        ("YOLO Sources", ["box_yolo_content_yolo", "box_yolo_content_ocr"])
    ]
    
    print("\n=== Source Type Filtering Tests ===")
    
    for test_name, source_types in source_type_tests:
        print(f"\n{test_name} Test:")
        print(f"Source types: {source_types or 'All'}")
        
        # Set source types for this test
        if source_types:
            patch_matcher.set_source_types(source_types)
        else:
            patch_matcher.set_source_types(KNOWN_SOURCE_TYPES)
        
        # Create a figure for this test
        plt.figure(figsize=(15, 10))
        plt.suptitle(f"Source Filter Test: {test_name}", fontsize=16)
        
        plt.subplot(1, len(theme_results) + 1, 1)
        plt.imshow(patch_image)
        plt.title("Patch Image\n38_Up or down.png")
        plt.axis('off')
        
        # Match the patch against each theme with current source types
        for idx, (theme_file, theme_result) in enumerate(theme_results):
            # Get available source types in this result
            available_sources = patch_matcher.get_available_source_types(theme_result)
            print(f"\n{theme_file} has source types: {available_sources}")
            
            print(f"Matching patch against {theme_file} with {test_name} filter...")
            start_time = time.time()
            match_result = patch_matcher.find_matching_element(patch_image, theme_result)
            matching_time = time.time() - start_time
            
            print(f"Matching completed in {matching_time:.2f} seconds")
            
            # Load the full theme image for visualization
            theme_image = Image.open(os.path.join(test_dir, theme_file))
            
            # Display match result
            if match_result.match_found:
                print(f"Match found in {theme_file}!")
                print(f"Matched element ID: {match_result.matched_element_id}")
                print(f"Source type: {match_result.parsed_content_result.source}")
                print(f"Similarity score: {match_result.similarity_score:.4f}")
                print(f"Classification: {match_result.classification}")
                print(f"Matched content: {match_result.parsed_content_result.content}")
                
                # Extract the matched element for visualization
                matched_bbox = match_result.parsed_content_result.bbox
                matched_img = patch_matcher.extract_image_from_bbox(theme_image, matched_bbox)
                
                # Add to visualization
                plt.subplot(1, len(theme_results) + 1, idx + 2)
                plt.imshow(matched_img)
                plt.title(f"Match in {theme_file}\nID: {match_result.matched_element_id}\nSource: {match_result.parsed_content_result.source}\nScore: {match_result.similarity_score:.4f}")
                plt.axis('off')
            else:
                print(f"No match found in {theme_file} with {test_name} filter")
                
                # Add empty placeholder to visualization
                plt.subplot(1, len(theme_results) + 1, idx + 2)
                plt.text(0.5, 0.5, f"No match found\nusing {test_name}", horizontalalignment='center', verticalalignment='center')
                plt.axis('off')
        
        # Save the visualization for this test
        plt.tight_layout()
        plt.savefig(os.path.join(test_dir, f"patch_matching_source_filter_{test_name.replace(' ', '_')}.png"))
        print(f"Test visualization saved to patch_matching_source_filter_{test_name.replace(' ', '_')}.png")
    
    # Demo dynamic source types during matching
    print("\n=== Dynamic Source Type Test ===")
    
    # Create multiplot figure for comparing different source types
    plt.figure(figsize=(15, 5 * len(KNOWN_SOURCE_TYPES)))
    plt.suptitle("Individual Source Type Comparison", fontsize=16)
    
    # For a single theme file, test each source type individually
    theme_file, theme_result = theme_results[0]  # Use first theme
    theme_image = Image.open(os.path.join(test_dir, theme_file))
    
    print(f"\nComparing individual source types for {theme_file}:")
    
    for i, source_type in enumerate(KNOWN_SOURCE_TYPES):
        print(f"\nTesting source type: {source_type}")
        
        # Match with just this source type
        start_time = time.time()
        match_result = patch_matcher.find_matching_element(patch_image, theme_result, [source_type])
        matching_time = time.time() - start_time
        
        print(f"Matching completed in {matching_time:.2f} seconds")
        
        # Plot the patch
        plt.subplot(len(KNOWN_SOURCE_TYPES), 2, i*2 + 1)
        plt.imshow(patch_image)
        plt.title(f"Patch Image\n38_Up or down.png")
        plt.axis('off')
        
        # Plot the match result for this source type
        plt.subplot(len(KNOWN_SOURCE_TYPES), 2, i*2 + 2)
        
        if match_result.match_found:
            print(f"Match found using source type '{source_type}'!")
            print(f"Matched element ID: {match_result.matched_element_id}")
            print(f"Similarity score: {match_result.similarity_score:.4f}")
            
            # Extract the matched element for visualization
            matched_bbox = match_result.parsed_content_result.bbox
            matched_img = patch_matcher.extract_image_from_bbox(theme_image, matched_bbox)
            
            plt.imshow(matched_img)
            plt.title(f"Source: {source_type}\nID: {match_result.matched_element_id}\nScore: {match_result.similarity_score:.4f}")
        else:
            print(f"No match found using source type '{source_type}'")
            plt.text(0.5, 0.5, f"No match found\nfor source: {source_type}", horizontalalignment='center', verticalalignment='center')
            
        plt.axis('off')
    
    # Save the source type comparison visualization
    plt.tight_layout()
    plt.savefig(os.path.join(test_dir, "patch_matching_source_comparison.png"))
    print("\nSource comparison visualization saved to patch_matching_source_comparison.png")

def main():
    """Main function to run the tests"""
    print("Testing PatchMatcher with source type filtering...")
    
    # Measure total execution time
    start_time = time.time()
    test_patch_matching_across_themes()
    end_time = time.time()
    
    total_time = end_time - start_time
    print(f"\nTests completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main() 