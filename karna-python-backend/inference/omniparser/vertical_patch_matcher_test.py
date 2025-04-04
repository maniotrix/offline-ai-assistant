import os
import sys
import logging
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
from pathlib import Path
import json

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(current_dir)))

from inference.omniparser.patch_matcher import PatchMatcher, PatchMatchResult
from inference.omniparser.vertical_patch_matcher import VerticalPatchMatcher
from inference.omniparser.ui_dynamic_area_detector_test import (
    load_screenshot_events,
    DEFAULT_DATA_DIR,
    JSON_FILE_PATH
)
from inference.omniparser.omni_helper import (
    OmniParserResultModel,
    OmniParserResultModelList,
    get_omniparser_inference_data
)
from config.paths import workspace_dir

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test patches to use
TEST_PATCHES = ["38_Up_or_down.png", "44_Copy.png"]

# Output directory for results and visualizations
OUTPUT_DIR = Path(current_dir) / "patch_matcher_comparison"

class MatcherPerformanceTest:
    """
    Test class to compare performance between normal PatchMatcher and VerticalPatchMatcher
    """
    def __init__(self, patch_dir: str = None):
        """
        Initialize the test with optional custom patch directory
        """
        # Create output directory if it doesn't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Set default patch directory if not provided
        if not patch_dir:
            self.patch_dir = os.path.join(current_dir, "test_patches")
            # Create if it doesn't exist
            os.makedirs(self.patch_dir, exist_ok=True)
        else:
            self.patch_dir = patch_dir
            
        # Initialize matchers with identical parameters
        self.normal_matcher = PatchMatcher(
            model_name='resnet50',
            layer_name='avgpool',
            similarity_threshold=0.7
        )
        
        self.vertical_matcher = VerticalPatchMatcher(
            model_name='resnet50',
            layer_name='avgpool',
            similarity_threshold=0.7
        )
        
        # Performance results storage
        self.results = []
        
    def load_patches(self, patch_names: List[str]) -> Dict[str, Image.Image]:
        """
        Load test patch images
        
        Args:
            patch_names: List of patch image filenames
            
        Returns:
            Dict mapping patch names to PIL Image objects
        """
        patches = {}
        
        for patch_name in patch_names:
            patch_path = os.path.join(self.patch_dir, patch_name)
            if os.path.exists(patch_path):
                try:
                    patch_img = Image.open(patch_path)
                    patches[patch_name] = patch_img
                    logger.info(f"Loaded patch image: {patch_name} ({patch_img.size})")
                except Exception as e:
                    logger.error(f"Failed to load patch image {patch_name}: {e}")
            else:
                logger.warning(f"Patch image not found: {patch_path}")
                
        return patches
    
    def run_single_match_test(
        self,
        patch: Image.Image,
        patch_name: str,
        result_model: OmniParserResultModel,
        frame_idx: int
    ) -> Dict:
        """
        Run a single match test using both matchers on a specific frame
        
        Args:
            patch: The patch image to match
            patch_name: Name of the patch for reporting
            result_model: The OmniParserResultModel to search in
            frame_idx: Index of this frame in the sequence
            
        Returns:
            Dict with test results
        """
        # Run normal matcher with timing
        start_time_normal = time.time()
        normal_result = self.normal_matcher.find_matching_element(patch, result_model)
        end_time_normal = time.time()
        normal_duration = end_time_normal - start_time_normal
        
        # Run vertical matcher with timing
        start_time_vertical = time.time()
        vertical_result = self.vertical_matcher.find_matching_element(patch, result_model)
        end_time_vertical = time.time()
        vertical_duration = end_time_vertical - start_time_vertical
        
        # Compile results
        result = {
            "patch_name": patch_name,
            "frame_idx": frame_idx,
            "normal_match_found": normal_result.match_found,
            "normal_similarity": normal_result.similarity_score if normal_result.match_found else 0,
            "normal_element_id": normal_result.matched_element_id if normal_result.match_found else None,
            "normal_duration": normal_duration,
            "vertical_match_found": vertical_result.match_found,
            "vertical_similarity": vertical_result.similarity_score if vertical_result.match_found else 0,
            "vertical_element_id": vertical_result.matched_element_id if vertical_result.match_found else None,
            "vertical_duration": vertical_duration,
            "same_match": (normal_result.matched_element_id == vertical_result.matched_element_id)
                         if (normal_result.match_found and vertical_result.match_found) else False,
            "speedup": normal_duration / vertical_duration if vertical_duration > 0 else float('inf')
        }
        
        # Determine if matches are consistent
        result["consistent"] = (normal_result.match_found == vertical_result.match_found)
        
        return result
    
    def run_comparison_test(
        self,
        patches: Dict[str, Image.Image],
        results_list: OmniParserResultModelList
    ) -> List[Dict]:
        """
        Run comparison tests across all patches and frames
        
        Args:
            patches: Dict mapping patch names to patch images
            results_list: List of all OmniParserResultModel objects to test with
            
        Returns:
            List of test result dictionaries
        """
        self.results = []
        
        # For each patch
        for patch_name, patch_img in patches.items():
            logger.info(f"Testing with patch: {patch_name}")
            
            # For each frame/result model
            for idx, result_model in enumerate(results_list.omniparser_result_models):
                logger.info(f"  Matching against frame {idx+1}/{len(results_list.omniparser_result_models)}")
                
                # Run test and collect results
                test_result = self.run_single_match_test(
                    patch_img, patch_name, result_model, idx
                )
                
                # Print immediate results
                match_status_normal = "✓" if test_result["normal_match_found"] else "✗"
                match_status_vertical = "✓" if test_result["vertical_match_found"] else "✗"
                
                logger.info(f"    Normal:  {match_status_normal} {test_result['normal_duration']:.4f}s " + 
                           (f"(element {test_result['normal_element_id']})" if test_result["normal_match_found"] else ""))
                logger.info(f"    Vertical: {match_status_vertical} {test_result['vertical_duration']:.4f}s " + 
                           (f"(element {test_result['vertical_element_id']})" if test_result["vertical_match_found"] else ""))
                
                if test_result["normal_match_found"] and test_result["vertical_match_found"]:
                    consistency = "same" if test_result["same_match"] else "DIFFERENT"
                    logger.info(f"    Match consistency: {consistency}")
                    
                if test_result["vertical_duration"] > 0:
                    logger.info(f"    Speed comparison: {test_result['speedup']:.2f}x " + 
                              ("faster" if test_result['speedup'] > 1 else "slower") + 
                              " with vertical matcher")
                
                self.results.append(test_result)
        
        return self.results
    
    def generate_performance_summary(self) -> Dict:
        """
        Generate summary statistics from test results
        
        Returns:
            Dict with summary metrics
        """
        if not self.results:
            return {"status": "No results available"}
        
        summary = {
            "total_tests": len(self.results),
            "normal_matches_found": sum(1 for r in self.results if r["normal_match_found"]),
            "vertical_matches_found": sum(1 for r in self.results if r["vertical_match_found"]),
            "consistent_results": sum(1 for r in self.results if r["consistent"]),
            "same_match_when_found": sum(1 for r in self.results 
                                    if r["normal_match_found"] and r["vertical_match_found"] and r["same_match"]),
            "avg_normal_duration": np.mean([r["normal_duration"] for r in self.results]),
            "avg_vertical_duration": np.mean([r["vertical_duration"] for r in self.results]),
            "avg_speedup": np.mean([r["speedup"] for r in self.results if r["vertical_duration"] > 0]),
            "max_speedup": max([r["speedup"] for r in self.results if r["vertical_duration"] > 0], default=0)
        }
        
        # Add consistency percentage
        if summary["total_tests"] > 0:
            summary["consistency_percentage"] = (summary["consistent_results"] / summary["total_tests"]) * 100
        else:
            summary["consistency_percentage"] = 0
            
        # Calculate match agreement
        matches_both_found = sum(1 for r in self.results 
                               if r["normal_match_found"] and r["vertical_match_found"])
        
        if matches_both_found > 0:
            summary["match_agreement_percentage"] = (summary["same_match_when_found"] / matches_both_found) * 100
        else:
            summary["match_agreement_percentage"] = 0
            
        return summary
    
    def visualize_results(self):
        """
        Create visualization plots from the test results
        """
        if not self.results:
            logger.warning("No results to visualize")
            return
            
        # Create a DataFrame for easier plotting
        df = pd.DataFrame(self.results)
        
        # Create output directory if needed
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Plot 1: Performance comparison by frame
        plt.figure(figsize=(12, 6))
        plt.title("Performance Comparison by Frame", fontsize=16)
        plt.plot(df["frame_idx"], df["normal_duration"], 'ro-', label="Normal Matcher")
        plt.plot(df["frame_idx"], df["vertical_duration"], 'bo-', label="Vertical Matcher")
        plt.xlabel("Frame Index", fontsize=12)
        plt.ylabel("Duration (seconds)", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Add grouping by patch if we have multiple patches
        if len(df["patch_name"].unique()) > 1:
            for patch_name in df["patch_name"].unique():
                patch_start = df[df["patch_name"] == patch_name]["frame_idx"].min()
                plt.axvline(x=patch_start, color='gray', linestyle='--', alpha=0.5)
                plt.text(patch_start, plt.ylim()[1]*0.9, f" {patch_name}", 
                        rotation=90, verticalalignment='top')
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "performance_by_frame.png", dpi=150)
        
        # Plot 2: Speedup comparison
        plt.figure(figsize=(12, 6))
        plt.title("Speedup Factor (Normal/Vertical)", fontsize=16)
        
        # Create a bar chart of speedup by frame
        x = range(len(df))
        plt.bar(x, df["speedup"], color='g', alpha=0.6)
        plt.axhline(y=1.0, color='r', linestyle='-', label="Break-even")
        
        # Add labels
        plt.xlabel("Test Index", fontsize=12)
        plt.ylabel("Speedup Factor", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Add average line
        avg_speedup = np.mean(df["speedup"])
        plt.axhline(y=avg_speedup, color='blue', linestyle='--', 
                   label=f"Average: {avg_speedup:.2f}x")
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "speedup_comparison.png", dpi=150)
        
        # Plot 3: Match consistency
        plt.figure(figsize=(10, 6))
        
        # Count match result combinations
        match_categories = [
            (True, True, True),   # Both found, same element
            (True, True, False),  # Both found, different elements
            (True, False, None),  # Only normal found
            (False, True, None),  # Only vertical found
            (False, False, None)  # Neither found
        ]
        
        labels = [
            "Both found\n(same element)",
            "Both found\n(different elements)", 
            "Only normal\nfound",
            "Only vertical\nfound",
            "Neither found"
        ]
        
        counts = []
        for n_found, v_found, same in match_categories:
            if same is None:
                count = sum(1 for r in self.results 
                          if r["normal_match_found"] == n_found and 
                             r["vertical_match_found"] == v_found)
            else:
                count = sum(1 for r in self.results 
                          if r["normal_match_found"] == n_found and 
                             r["vertical_match_found"] == v_found and
                             r["same_match"] == same)
            counts.append(count)
        
        colors = ['green', 'orange', 'red', 'blue', 'gray']
        plt.pie(counts, labels=labels, autopct='%1.1f%%', 
               startangle=90, colors=colors)
        plt.axis('equal')
        plt.title("Match Consistency Between Matchers", fontsize=14)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "match_consistency.png", dpi=150)
        
        logger.info(f"Saved result visualizations to {OUTPUT_DIR}")
    
    def print_summary(self, summary: Dict):
        """
        Print a formatted summary of test results to console
        
        Args:
            summary: Dict with summary metrics
        """
        print("\n" + "="*80)
        print(" PATCH MATCHER PERFORMANCE COMPARISON SUMMARY ".center(80, "="))
        print("="*80)
        
        print(f"\nTotal tests run: {summary['total_tests']}")
        print(f"Match consistency: {summary['consistency_percentage']:.1f}% consistent results")
        
        print("\nMatch Statistics:")
        print(f"  Normal matcher found {summary['normal_matches_found']} matches")
        print(f"  Vertical matcher found {summary['vertical_matches_found']} matches")
        
        if summary.get('match_agreement_percentage') is not None:
            print(f"  When both matchers found matches, they agreed on the same element "
                 f"{summary['match_agreement_percentage']:.1f}% of the time")
        
        print("\nPerformance Statistics:")
        print(f"  Average time for normal matcher:  {summary['avg_normal_duration']:.4f} seconds")
        print(f"  Average time for vertical matcher: {summary['avg_vertical_duration']:.4f} seconds")
        print(f"  Average speedup with vertical matcher: {summary['avg_speedup']:.2f}x")
        print(f"  Maximum speedup observed: {summary['max_speedup']:.2f}x")
        
        # Determine overall recommendation
        is_faster = summary['avg_speedup'] > 1.0
        is_consistent = summary['match_agreement_percentage'] > 90 if 'match_agreement_percentage' in summary else False
        
        print("\nConclusion:")
        if is_faster and is_consistent:
            print("  The VerticalPatchMatcher is FASTER and maintains high match consistency.")
            print("  RECOMMENDATION: Use VerticalPatchMatcher for better performance.")
        elif is_faster and not is_consistent:
            print("  The VerticalPatchMatcher is FASTER but has lower match consistency.")
            print("  RECOMMENDATION: Evaluate if speed or match consistency is more important for your use case.")
        elif not is_faster and is_consistent:
            print("  The VerticalPatchMatcher is SLOWER but has high match consistency.")
            print("  RECOMMENDATION: Stick with the normal PatchMatcher for better performance.")
        else:
            print("  The VerticalPatchMatcher is SLOWER and has lower match consistency.")
            print("  RECOMMENDATION: Use the normal PatchMatcher.")
            
        print("\nSee visualizations for more details:")
        print(f"  {OUTPUT_DIR}")
        print("="*80 + "\n")

def test_patch_matchers_performance(use_viewport=True):
    """
    Run a comprehensive performance test comparing PatchMatcher and VerticalPatchMatcher
    
    Args:
        use_viewport: Whether to crop screenshots according to viewport rendering area
    """
    logger.info("Starting patch matcher performance comparison test...")
    
    try:
        # Check if the JSON file exists
        if not os.path.exists(JSON_FILE_PATH):
            logger.error(f"JSON file not found: {JSON_FILE_PATH}")
            return

        # Define viewport if needed
        viewport = None
        if use_viewport:
            viewport = {
                "x": 0,
                "y": 121,
                "width": 1920,
                "height": 919
            }
            logger.info(f"Using viewport for cropping: {viewport}")

        # Load real data from JSON file
        logger.info(f"Loading data from: {JSON_FILE_PATH}")
        screenshot_events = load_screenshot_events(JSON_FILE_PATH, viewport=viewport)
        test_data = get_omniparser_inference_data(screenshot_events)
        
        if not test_data.omniparser_result_models:
            logger.error("No valid models loaded from JSON file.")
            return
            
        logger.info(f"Successfully loaded {len(test_data.omniparser_result_models)} models from JSON file")
        
        # Initialize test with default patch directory
        test = MatcherPerformanceTest()
        
        # Load the test patches
        patches = test.load_patches(TEST_PATCHES)
        
        if not patches:
            logger.error(f"No test patches found. Ensure {TEST_PATCHES} exist in the test_patches directory.")
            return
        
        # Run the comparison tests
        logger.info("Running comparison tests...")
        test.run_comparison_test(patches, test_data)
        
        # Generate and display summary
        summary = test.generate_performance_summary()
        test.print_summary(summary)
        
        # Create visualizations
        logger.info("Generating result visualizations...")
        test.visualize_results()
        
        logger.info("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}", exc_info=True)

if __name__ == "__main__":
    test_patch_matchers_performance() 