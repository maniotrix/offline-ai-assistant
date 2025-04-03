import os
import numpy as np
from PIL import Image, ImageDraw # Added ImageDraw for potential visualization/debugging
from typing import List, Dict, Tuple, Optional, Set, Any
import logging
import itertools # For unique IDs
from datetime import datetime # Import datetime globally
from dataclasses import dataclass

# Define logger early to be available in except blocks
logger = logging.getLogger(__name__)
# Configure logger basic settings if run standalone
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Keep Omniparser for type hint if needed
from .image_comparison import ResNetImageEmbedder
from .omni_helper import OmniParserResultModel, OmniParserResultModelList, ParsedContentResult # Import new input types


# Define a structure for element info within a frame
@dataclass
class FrameElement:
    """Represents a detected element within a single frame."""
    frame_index: int
    # Use parsed_content_result.id directly or store original index if needed
    element_id: int # ID from ParsedContentResult
    parsed_content_result: ParsedContentResult # Keep original data
    embedding: np.ndarray # ResNet embedding of the element's patch

    @property
    def bbox(self) -> List[float]: # Helper to access bbox easily
        return self.parsed_content_result.bbox

    @property
    def content(self) -> Optional[str]: # Helper to access content easily
        return self.parsed_content_result.content


# Define a structure for tracking persistent elements across frames
@dataclass
class ElementTrack:
    """Represents an element tracked across multiple frames."""
    track_id: int
    first_occurrence: FrameElement # Details of the first time this element was seen
    occurrences: List[FrameElement] # List of all FrameElement instances in the track

class DynamicAreaDetector:
    """
    Analyzes a sequence of pre-processed OmniParser results to identify
    dynamic content areas by tracking persistent UI elements.
    """
    def __init__(self,
                 # Omniparser instance might not be strictly needed anymore if parsing is always pre-done,
                 # but keeping it for now in case of future utility or type hints.
                 # omniparser: Omniparser,
                 embedder: ResNetImageEmbedder,
                 similarity_threshold: float = 0.7,
                 proximity_threshold: float = 0.1,
                 min_persistence_fraction: float = 0.5):
        """
        Initializes the detector.

        Args:
            embedder: An initialized ResNetImageEmbedder instance.
            similarity_threshold: Cosine similarity threshold (0-1) to consider
                                   elements similar for tracking. Higher means stricter.
            proximity_threshold: Maximum normalized Euclidean distance between element
                                 centers to be considered for tracking.
            min_persistence_fraction: An element track must exist in at least this
                                      fraction of valid frames to be considered persistent.
        """
        # if not isinstance(omniparser, Omniparser):
        #     raise TypeError("omniparser must be an instance of Omniparser")
        if not isinstance(embedder, ResNetImageEmbedder):
            raise TypeError("embedder must be an instance of ResNetImageEmbedder")

        # self.omniparser = omniparser # Store if needed, otherwise remove
        self.embedder = embedder
        self.similarity_threshold = similarity_threshold
        self.proximity_threshold = proximity_threshold
        self.min_persistence_fraction = min_persistence_fraction
        self._track_id_counter = itertools.count() # For generating unique track IDs

        logger.info(f"DynamicAreaDetector initialized with similarity>={similarity_threshold}, "
                    f"proximity<={proximity_threshold}, persistence>={min_persistence_fraction}")

    def _get_element_center(self, bbox: List[float]) -> Tuple[float, float]:
        """Calculates the normalized center coordinates (x, y) of a bounding box."""
        if len(bbox) != 4:
            # Add logging for invalid bbox length
            logger.error(f"Invalid bounding box length: {len(bbox)}. Expected 4 coordinates.")
            raise ValueError("Bounding box must contain 4 coordinates (x1, y1, x2, y2)")
        x1, y1, x2, y2 = bbox
        # Ensure bbox coordinates are valid (x2 >= x1, y2 >= y1)
        if x2 < x1 or y2 < y1:
            logger.warning(f"Invalid bbox coordinates (x2<x1 or y2<y1): {[x1, y1, x2, y2]}. Center calculation might be incorrect.")
            # Attempt to correct or proceed with caution
            x2 = max(x1, x2)
            y2 = max(y1, y2)
        return ((x1 + x2) / 2, (y1 + y2) / 2)


    def _get_distance(self, center1: Tuple[float, float], center2: Tuple[float, float]) -> float:
        """Calculates the Euclidean distance between two normalized points."""
        return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

    # Method _extract_element_data_from_frame is REMOVED as parsing is pre-done.
    # The logic is moved into the main detect_main_areas method.

    def _track_elements(self, all_frame_data: List[List[FrameElement]]) -> List[ElementTrack]:
        """
        Tracks elements across frames using similarity and proximity.

        Args:
            all_frame_data: A list where each item is a list of FrameElements for a frame.

        Returns:
            A list of ElementTrack objects representing identified tracks.
        """
        if not all_frame_data or len(all_frame_data) < 2:
            logger.warning("Tracking requires at least 2 frames of data.")
            return []

        tracks: List[ElementTrack] = [] # Finished tracks
        active_tracks: List[ElementTrack] = [] # Tracks currently being extended

        # Initialize tracks with elements from the first valid frame
        first_frame_elements = all_frame_data[0]
        for element in first_frame_elements:
            track_id = next(self._track_id_counter)
            new_track = ElementTrack(track_id=track_id, first_occurrence=element, occurrences=[element])
            active_tracks.append(new_track)
        logger.debug(f"Initialized {len(active_tracks)} tracks from frame 0.")

        # Process subsequent frames
        for frame_index in range(1, len(all_frame_data)):
            current_frame_elements = all_frame_data[frame_index]
            if not current_frame_elements: # Skip empty frames
                 logger.debug(f"Skipping empty frame {frame_index} during tracking.")
                 continue

            matched_current_frame_ids: Set[int] = set() # Track by ParsedContentResult ID
            next_active_tracks: List[ElementTrack] = []

            # --- Try to extend existing active tracks ---
            for track in active_tracks:
                last_element_in_track = track.occurrences[-1]
                best_match_element = None
                best_match_id = -1 # Store ParsedContentResult ID
                highest_similarity = -1.0 # Initialize below valid similarity range

                # Find the best matching element in the current frame for this track
                for current_element in current_frame_elements:
                    # Avoid re-matching elements already assigned to a track in this frame
                    if current_element.element_id in matched_current_frame_ids:
                        continue

                    try:
                        # Calculate similarity (dot product of normalized vectors)
                        similarity = np.dot(last_element_in_track.embedding, current_element.embedding)

                        # Check similarity threshold first (major filter)
                        if similarity >= self.similarity_threshold:
                            # Calculate distance only if similarity is high enough
                            distance = self._get_distance(
                                self._get_element_center(last_element_in_track.bbox),
                                self._get_element_center(current_element.bbox)
                            )

                            # Check proximity threshold
                            if distance <= self.proximity_threshold:
                                # If this is a better match than previous candidates for this track
                                if similarity > highest_similarity:
                                     highest_similarity = similarity
                                     best_match_element = current_element
                                     best_match_id = current_element.element_id # Use ParsedContentResult ID

                    except ValueError as ve: # Catch specific errors like invalid bbox for center calc
                         logger.error(f"ValueError during comparison involving track {track.track_id} element ID "
                                      f"{last_element_in_track.element_id} and current element ID {current_element.element_id}: {ve}")
                         continue
                    except Exception as e:
                         logger.error(f"Error comparing track {track.track_id} element ID "
                                      f"{last_element_in_track.element_id} with current element ID {current_element.element_id}: {e}")
                         continue # Skip comparison if error occurs


                # If a suitable match was found, extend the track
                if best_match_element is not None:
                    track.occurrences.append(best_match_element)
                    matched_current_frame_ids.add(best_match_id)
                    next_active_tracks.append(track) # This track continues
                    # logger.debug(f"Extended track {track.track_id} with element ID {best_match_id} in frame {frame_index} sim={highest_similarity:.3f}")
                else:
                    # No match found, the track ends here
                    tracks.append(track)
                    # logger.debug(f"Ended track {track.track_id} at frame {frame_index - 1}")


            # --- Start new tracks for unmatched elements ---
            for current_element in current_frame_elements:
                if current_element.element_id not in matched_current_frame_ids:
                    track_id = next(self._track_id_counter)
                    new_track = ElementTrack(track_id=track_id, first_occurrence=current_element, occurrences=[current_element])
                    next_active_tracks.append(new_track) # Start a new active track
                    # logger.debug(f"Started new track {track_id} at frame {frame_index} with element ID {current_element.element_id}")


            active_tracks = next_active_tracks # Update active tracks for the next frame

        # Add any tracks still active after the last frame
        tracks.extend(active_tracks)
        logger.info(f"Generated {len(tracks)} element tracks in total.")
        return tracks

    def _get_persistent_tracks(self, tracks: List[ElementTrack], total_valid_frames: int) -> List[ElementTrack]:
        """Filters tracks to keep only those meeting the minimum persistence fraction."""
        if total_valid_frames == 0: return []
        # Ensure minimum occurrences is at least 2, even if fraction is low for few frames
        min_occurrences = max(2, int(total_valid_frames * self.min_persistence_fraction))

        persistent_tracks = [
            track for track in tracks if len(track.occurrences) >= min_occurrences
        ]
        logger.info(f"Filtered down to {len(persistent_tracks)} persistent tracks "
                    f"(required occurrences >= {min_occurrences} out of {total_valid_frames} valid frames).")
        return persistent_tracks

    def _calculate_static_region_bbox(self, persistent_tracks: List[ElementTrack]) -> Optional[List[float]]:
        """
        Calculates the overall bounding box encompassing all occurrences of
        elements deemed persistent (static).

        Args:
            persistent_tracks: List of ElementTrack objects identified as stable.

        Returns:
            A single bounding box [x1, y1, x2, y2] representing the union of
            all persistent element occurrences, or None if no persistent tracks exist.
        """
        if not persistent_tracks:
            logger.info("No persistent tracks found, cannot define static region.")
            return None

        # Collect all bounding boxes from all occurrences in persistent tracks
        all_bboxes = [occ.bbox for track in persistent_tracks for occ in track.occurrences]

        if not all_bboxes:
             logger.warning("Persistent tracks found, but they contain no bounding boxes.")
             return None

        try:
            # Calculate min/max coordinates across all boxes
            min_x1 = min(bbox[0] for bbox in all_bboxes)
            min_y1 = min(bbox[1] for bbox in all_bboxes)
            max_x2 = max(bbox[2] for bbox in all_bboxes)
            max_y2 = max(bbox[3] for bbox in all_bboxes)

            # Ensure coordinates are within the valid normalized range [0, 1]
            min_x1 = max(0.0, min_x1)
            min_y1 = max(0.0, min_y1)
            max_x2 = min(1.0, max_x2)
            max_y2 = min(1.0, max_y2)

            # Handle potential edge cases where max < min after clamping (should be rare)
            if max_x2 <= min_x1 or max_y2 <= min_y1:
                 logger.warning(f"Static region calculation resulted in invalid bbox "
                              f"([ {min_x1:.3f}, {min_y1:.3f}, {max_x2:.3f}, {max_y2:.3f} ]). Returning None.")
                 return None

            static_bbox = [min_x1, min_y1, max_x2, max_y2]
            logger.info(f"Calculated overall static region union bbox: "
                        f"[ {static_bbox[0]:.3f}, {static_bbox[1]:.3f}, {static_bbox[2]:.3f}, {static_bbox[3]:.3f} ]")
            return static_bbox

        except Exception as e:
            logger.error(f"Error calculating static region bounding box: {e}", exc_info=True)
            return None


    def _calculate_dynamic_regions(self, static_bbox: Optional[List[float]]) -> List[List[float]]:
        """
        Calculates potential dynamic regions by subtracting the static region
        from the full screen area ([0,0,1,1]). This is a simplified approach.

        Args:
            static_bbox: The bounding box [x1, y1, x2, y2] of the static area, or None.

        Returns:
            A list of bounding boxes for potential dynamic regions.
        """
        screen_bbox = [0.0, 0.0, 1.0, 1.0] # Normalized screen coordinates

        if static_bbox is None:
            # If no static region, the entire screen is considered dynamic
            logger.info("No static region defined, considering entire screen dynamic.")
            return [screen_bbox]

        sx1, sy1, sx2, sy2 = static_bbox
        dynamic_regions: List[List[float]] = []

        # --- Identify potential rectangular dynamic areas ---
        # 1. Region above static area
        if sy1 > 1e-6: # Use small epsilon for float comparison
            dynamic_regions.append([0.0, 0.0, 1.0, sy1])
        # 2. Region below static area
        if sy2 < 1.0 - 1e-6:
            dynamic_regions.append([0.0, sy2, 1.0, 1.0])
        # 3. Region left of static area (only within the vertical span of the static area)
        if sx1 > 1e-6:
            dynamic_regions.append([0.0, sy1, sx1, sy2])
        # 4. Region right of static area (only within the vertical span of the static area)
        if sx2 < 1.0 - 1e-6:
            dynamic_regions.append([sx2, sy1, 1.0, sy2])

        # --- Filter out invalid or zero-area regions ---
        valid_dynamic_regions = []
        min_area = 1e-5 # Define a minimum area threshold
        for r in dynamic_regions:
            # Check for valid coordinates and positive area
            if r[0] < r[2] - 1e-6 and r[1] < r[3] - 1e-6:
                 # Ensure bounds are within [0, 1] although they should be by construction here
                 r = [max(0.0, min(1.0, coord)) for coord in r]
                 # Double check area after potential clamping
                 width = r[2] - r[0]
                 height = r[3] - r[1]
                 if width > 1e-6 and height > 1e-6 and (width * height) > min_area:
                     valid_dynamic_regions.append(r)

        # This simplified geometric subtraction might miss complex cases or result
        # in overlapping regions if the static_bbox is small and central.
        # More robust geometric libraries (like Shapely) would be needed for perfect subtraction.
        logger.info(f"Identified {len(valid_dynamic_regions)} potential dynamic regions based on static area.")
        return valid_dynamic_regions


    def _apply_selection_rules(self,
                              dynamic_regions: List[List[float]],
                              all_frame_data: List[List[FrameElement]]) -> Dict[str, Optional[List[float]]]:
        """
        Applies deterministic rules to select the 'main' dynamic area if multiple
        candidates exist.

        Args:
            dynamic_regions: List of candidate dynamic region bounding boxes.
            all_frame_data: Processed element data for all valid frames.

        Returns:
            A dictionary mapping rule names to the selected main area bbox for that rule.
        """
        results: Dict[str, Optional[List[float]]] = {}
        rule_names = ["largest_area", "most_elements"] # Add more rules here

        # Initialize results
        for rule_name in rule_names:
            results[rule_name] = None

        if not dynamic_regions:
            logger.warning("No dynamic regions provided to apply selection rules.")
            return results

        if len(dynamic_regions) == 1:
            # If only one, it's the main area by default for all rules
            main_bbox = dynamic_regions[0]
            logger.info(f"Only one dynamic region found, selecting it for all rules: {main_bbox}")
            for rule_name in rule_names:
                 results[rule_name] = main_bbox
            return results

        logger.info(f"Applying selection rules to {len(dynamic_regions)} dynamic regions.")

        # --- Rule A: Largest Area ---
        largest_area = 0.0
        largest_bbox = None
        for bbox in dynamic_regions:
            try:
                 area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                 if area > largest_area:
                     largest_area = area
                     largest_bbox = bbox
            except Exception as e:
                 logger.error(f"Error calculating area for bbox {bbox}: {e}")
        results["largest_area"] = largest_bbox
        logger.debug(f"Rule 'largest_area' selected: {largest_bbox} (Area: {largest_area:.4f})")


        # --- Rule B: Most Elements (Average over frames) ---
        max_avg_elements = -1.0
        most_elements_bbox = None
        total_valid_frames = len(all_frame_data)

        if total_valid_frames > 0:
            for region_bbox in dynamic_regions:
                total_elements_in_region = 0
                rx1, ry1, rx2, ry2 = region_bbox

                # Count elements whose center falls within this region, averaged over frames
                for frame_data in all_frame_data:
                    count_in_frame = 0
                    for element in frame_data:
                        try:
                            # Check if element center is within the region bbox
                            ex, ey = self._get_element_center(element.bbox)
                            if rx1 <= ex < rx2 and ry1 <= ey < ry2:
                                 count_in_frame += 1
                        except ValueError: # Catch invalid bbox from center calc
                             logger.warning(f"Skipping element ID {element.element_id} in frame {element.frame_index} due to invalid bbox for center calculation.")
                             continue
                        except Exception as e:
                             logger.error(f"Error checking element ID {element.element_id} "
                                          f"in frame {element.frame_index} against region {region_bbox}: {e}")
                    total_elements_in_region += count_in_frame

                avg_elements = total_elements_in_region / total_valid_frames
                if avg_elements > max_avg_elements:
                     max_avg_elements = avg_elements
                     most_elements_bbox = region_bbox

            results["most_elements"] = most_elements_bbox
            logger.debug(f"Rule 'most_elements' selected: {most_elements_bbox} (Avg elements: {max_avg_elements:.2f})")
        else:
             logger.warning("Cannot apply 'most_elements' rule: No valid frame data.")
             results["most_elements"] = None # Cannot determine without frame data


        # --- Rule C: Highest Dissimilarity ---
        # This requires modifying the tracking logic to store and aggregate dissimilarity scores per region.
        # Placeholder:
        # results["highest_dissimilarity"] = self._calculate_highest_dissimilarity_region(...)
        # logger.debug(f"Rule 'highest_dissimilarity' selected: {results['highest_dissimilarity']}")

        return results

    # === Public Method ===
    def detect_main_areas(self, results_list: OmniParserResultModelList) -> Dict[str, Optional[List[float]]]:
        """
        Detects the main dynamic content area(s) from a sequence of OmniParser results.

        This is the main entry point for the class. It orchestrates the analysis
        pipeline: per-frame processing, element tracking, static/dynamic region
        calculation, and rule-based selection.

        Args:
            results_list: An OmniParserResultModelList object containing the pre-processed
                          results for a sequence of screenshots. Requires at least 2 results.

        Returns:
            A dictionary where keys are rule names (e.g., 'largest_area', 'most_elements')
            and values are the corresponding main area bounding box ([x1, y1, x2, y2] normalized)
            or None if no area could be determined for that rule or if an error occurred.
        """
        logger.info(f"Starting dynamic area detection for {len(results_list.omniparser_result_models)} pre-parsed frames.")
        default_result: Dict[str, Optional[List[float]]] = {"largest_area": None, "most_elements": None} # Match rule names in _apply_selection_rules

        if not isinstance(results_list, OmniParserResultModelList) or len(results_list.omniparser_result_models) < 2:
            logger.warning("Input must be an OmniParserResultModelList with at least 2 results.")
            return default_result

        # --- Step 1: Extract FrameElement Data (Embeddings & Patches) ---
        all_frame_data: List[List[FrameElement]] = []
        valid_frame_count = 0

        for frame_index, omni_model in enumerate(results_list.omniparser_result_models):
            frame_elements: List[FrameElement] = []
            screenshot_path = omni_model.omniparser_result.original_image_path
            logger.info(f"Extracting elements for frame {frame_index}: {os.path.basename(screenshot_path)}")

            try:
                if not os.path.exists(screenshot_path):
                    logger.error(f"Screenshot file not found for frame {frame_index}: {screenshot_path}")
                    continue # Skip this frame

                img = Image.open(screenshot_path)
                # Ensure image is RGB for consistency
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width == 0 or height == 0:
                    logger.error(f"Invalid image dimensions ({width}x{height}) for frame {frame_index}")
                    continue # Skip this frame

                if not omni_model.parsed_content_results:
                     logger.warning(f"No parsed content results found for frame {frame_index}.")
                     # Still append empty list to maintain frame count correspondence
                     all_frame_data.append(frame_elements)
                     valid_frame_count += 1 # Count as valid if parsing happened but found 0 elements
                     continue

                # Process each parsed element from the OmniParserResultModel
                for pcr in omni_model.parsed_content_results:
                    bbox_normalized = pcr.bbox

                    # Validate bbox format and values (already normalized, maybe pre-processed)
                    if not isinstance(bbox_normalized, list) or len(bbox_normalized) != 4:
                        logger.warning(f"Skipping element ID {pcr.id} in frame {frame_index}: invalid bbox format {bbox_normalized}.")
                        continue
                    if not all(isinstance(coord, (int, float)) for coord in bbox_normalized):
                        logger.warning(f"Skipping element ID {pcr.id} in frame {frame_index}: non-numeric bbox coords {bbox_normalized}.")
                        continue
                    # Check if bbox is already absolute (heuristic: check if values > 1.0)
                    # The helper expects absolute bboxes, so we convert if needed
                    if max(bbox_normalized) <= 1.0 + 1e-6: # Allow small tolerance over 1.0
                        # Convert normalized bbox to absolute pixel coords for cropping
                        x1_abs = int(bbox_normalized[0] * width)
                        y1_abs = int(bbox_normalized[1] * height)
                        x2_abs = int(bbox_normalized[2] * width)
                        y2_abs = int(bbox_normalized[3] * height)
                    else:
                         # Assume bbox was already absolute (e.g., from pre-processor in omni_helper)
                         x1_abs, y1_abs, x2_abs, y2_abs = map(int, bbox_normalized)


                    # Ensure valid bbox dimensions after conversion
                    if x1_abs >= x2_abs or y1_abs >= y2_abs:
                        # Allow zero-width/height if coords are almost equal
                        if not (np.isclose(bbox_normalized[0], bbox_normalized[2]) or np.isclose(bbox_normalized[1], bbox_normalized[3])):
                             logger.warning(f"Skipping invalid bbox {bbox_normalized} (abs: {[x1_abs, y1_abs, x2_abs, y2_abs]}) for element {pcr.id} frame {frame_index}")
                             continue
                        # Adjust slightly
                        x2_abs = max(x1_abs + 1, x2_abs)
                        y2_abs = max(y1_abs + 1, y2_abs)
                        x1_abs, y1_abs = max(0, x1_abs), max(0, y1_abs)
                        x2_abs, y2_abs = min(width, x2_abs), min(height, y2_abs)
                        if x1_abs >= x2_abs or y1_abs >= y2_abs:
                             logger.warning(f"Skipping element {pcr.id} frame {frame_index} even after bbox adjustment.")
                             continue


                    try:
                        # Extract Patch
                        patch = img.crop((x1_abs, y1_abs, x2_abs, y2_abs))
                        if patch.width < 5 or patch.height < 5:
                             logger.debug(f"Skipping very small patch (element ID {pcr.id}) in frame {frame_index}")
                             continue

                        # Compute Embedding
                        embedding = self.embedder.get_embedding(patch)

                        # Store Frame Element Data
                        frame_elements.append(FrameElement(
                            frame_index=frame_index,
                            element_id=pcr.id, # Use the ID from ParsedContentResult
                            parsed_content_result=pcr, # Store the whole object
                            embedding=embedding
                        ))
                    except ValueError as ve:
                         logger.error(f"ValueError processing element ID {pcr.id} in frame {frame_index}: {ve}")
                         continue
                    except Exception as e:
                        logger.error(f"Failed to extract/embed element ID {pcr.id} in frame {frame_index}: {e}", exc_info=True)
                        continue # Skip this element

                logger.info(f"Extracted {len(frame_elements)} valid elements from frame {frame_index}")
                all_frame_data.append(frame_elements)
                valid_frame_count += 1

            except FileNotFoundError: # Already logged
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing pre-parsed frame {frame_index}: {e}", exc_info=True)
                continue # Skip this frame entirely

        # --- End Per-Frame Loop ---

        if valid_frame_count < 2:
             logger.error(f"Failed to process enough frames ({valid_frame_count}) for analysis. Need at least 2.")
             return default_result

        # --- Step 2 & 3: Track Elements and Identify Persistent Ones ---
        # Reset track counter for this run
        self._track_id_counter = itertools.count()
        try:
            all_tracks = self._track_elements(all_frame_data)
            persistent_tracks = self._get_persistent_tracks(all_tracks, valid_frame_count)
        except Exception as e:
             logger.error(f"Error during element tracking or persistence filtering: {e}", exc_info=True)
             return default_result

        # --- Step 4: Define Static Region ---
        try:
             static_region_bbox = self._calculate_static_region_bbox(persistent_tracks)
        except Exception as e:
            logger.error(f"Error calculating static region: {e}", exc_info=True)
            return default_result


        # --- Step 5: Identify Dynamic Regions ---
        try:
            # Use normalized bbox from PCR if static_region_bbox is calculated from normalized values
            dynamic_regions = self._calculate_dynamic_regions(static_region_bbox)
        except Exception as e:
             logger.error(f"Error calculating dynamic regions: {e}", exc_info=True)
             return default_result

        # --- Step 6: Apply Selection Rules ---
        try:
             # Pass all_frame_data which contains FrameElement objects with PCRs
             main_area_results = self._apply_selection_rules(dynamic_regions, all_frame_data)
        except Exception as e:
             logger.error(f"Error applying selection rules: {e}", exc_info=True)
             return default_result


        logger.info("Dynamic area detection completed successfully.")
        return main_area_results