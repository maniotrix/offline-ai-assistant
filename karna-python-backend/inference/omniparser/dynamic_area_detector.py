import os
import numpy as np
from PIL import Image, ImageDraw # Added ImageDraw for potential visualization/debugging
from typing import List, Dict, Tuple, Optional, Set, Any
import logging
import itertools # For unique IDs
from datetime import datetime # Import datetime globally
from dataclasses import dataclass
from sklearn.cluster import DBSCAN  # For better element clustering
from scipy.ndimage import gaussian_filter  # For heatmap generation
from scipy.spatial.distance import cdist  # For distance calculations
from scipy.stats import entropy  # For measuring content variation
from scipy.ndimage import label as scipy_label  # Fixed import for label function

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
    
    @property
    def content_variation(self) -> float:
        """Calculate the variation in content across occurrences."""
        if not self.occurrences:
            return 0.0
            
        # Count occurrences with same content vs different
        contents = [occ.content for occ in self.occurrences if occ.content]
        if not contents:
            return 0.0
            
        # If all contents are the same, variation is 0
        if len(set(contents)) == 1:
            return 0.0
            
        # Otherwise, calculate entropy of content distribution
        content_counts = {}
        for content in contents:
            if content in content_counts:
                content_counts[content] += 1
            else:
                content_counts[content] = 1
                
        # Calculate normalized entropy (0-1)
        counts = list(content_counts.values())
        probabilities = [count / len(contents) for count in counts]
        return min(1.0, entropy(probabilities) / np.log(len(probabilities)) if len(probabilities) > 1 else 0.0)


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
                 min_persistence_fraction: float = 0.5,
                 dynamic_threshold: float = 0.3,  # New: threshold for considering content dynamic
                 heatmap_sigma: float = 0.02,     # New: sigma for gaussian blur on heatmap
                 dbscan_epsilon: float = 0.1,     # New: DBSCAN clustering epsilon
                 dbscan_min_samples: int = 5):    # New: DBSCAN min samples
        """
        Initializes the detector with enhanced parameters.

        Args:
            embedder: An initialized ResNetImageEmbedder instance.
            similarity_threshold: Cosine similarity threshold (0-1) for tracking.
            proximity_threshold: Maximum normalized distance between element centers.
            min_persistence_fraction: Minimum fraction of frames for persistent elements.
            dynamic_threshold: Content variation threshold for dynamic elements.
            heatmap_sigma: Sigma for Gaussian blur when creating heatmaps.
            dbscan_epsilon: DBSCAN clustering distance parameter.
            dbscan_min_samples: DBSCAN minimum samples for core points.
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
        self.dynamic_threshold = dynamic_threshold
        self.heatmap_sigma = heatmap_sigma
        self.dbscan_epsilon = dbscan_epsilon
        self.dbscan_min_samples = dbscan_min_samples
        self._track_id_counter = itertools.count() # For generating unique track IDs

        logger.info(f"DynamicAreaDetector initialized with similarity>={similarity_threshold}, "
                    f"proximity<={proximity_threshold}, persistence>={min_persistence_fraction}, "
                    f"dynamic_threshold>={dynamic_threshold}")

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

    def _get_persistent_tracks(self, tracks: List[ElementTrack], total_valid_frames: int) -> Tuple[List[ElementTrack], List[ElementTrack]]:
        """
        Filters tracks into persistent (static) and dynamic tracks based on:
        1. Persistence across frames
        2. Content variation
        
        Returns both static and dynamic track lists.
        """
        if total_valid_frames == 0: 
            return [], []
            
        min_occurrences = max(2, int(total_valid_frames * self.min_persistence_fraction))
        
        # First filter by persistence only
        persistent_candidates = [
            track for track in tracks if len(track.occurrences) >= min_occurrences
        ]
        
        # Then separate into static vs dynamic based on content variation
        static_tracks = []
        dynamic_tracks = []
        
        for track in persistent_candidates:
            # Calculate content variation for this track
            variation = track.content_variation
            
            if variation < self.dynamic_threshold:
                # Low variation = static content
                static_tracks.append(track)
            else:
                # High variation = dynamic content
                dynamic_tracks.append(track)
        
        logger.info(f"Classified {len(static_tracks)} static tracks and {len(dynamic_tracks)} dynamic tracks "
                   f"out of {len(persistent_candidates)} persistent candidates.")
        
        return static_tracks, dynamic_tracks

    def _create_element_heatmap(self, tracks: List[ElementTrack], grid_size: int = 100) -> np.ndarray:
        """
        Create a heatmap representing element density across the screen.
        
        Args:
            tracks: List of element tracks to visualize
            grid_size: Size of the grid for the heatmap (higher = more detailed)
            
        Returns:
            np.ndarray: 2D heatmap array
        """
        # Initialize empty heatmap
        heatmap = np.zeros((grid_size, grid_size))
        
        # Add each element occurrence to the heatmap
        for track in tracks:
            for occ in track.occurrences:
                try:
                    # Get element bbox and convert to heatmap coordinates
                    x1, y1, x2, y2 = occ.bbox
                    
                    # Ensure values are within [0,1]
                    x1 = max(0.0, min(1.0, x1))
                    y1 = max(0.0, min(1.0, y1))
                    x2 = max(0.0, min(1.0, x2))
                    y2 = max(0.0, min(1.0, y2))
                    
                    # Convert to grid coordinates
                    grid_x1 = int(x1 * (grid_size - 1))
                    grid_y1 = int(y1 * (grid_size - 1))
                    grid_x2 = int(x2 * (grid_size - 1)) 
                    grid_y2 = int(y2 * (grid_size - 1))
                    
                    # Ensure at least 1 pixel width/height
                    grid_x2 = max(grid_x1 + 1, grid_x2)
                    grid_y2 = max(grid_y1 + 1, grid_y2)
                    
                    # Add weight to the heatmap in this rectangle
                    heatmap[grid_y1:grid_y2, grid_x1:grid_x2] += 1
                    
                except Exception as e:
                    logger.error(f"Error adding element to heatmap: {e}")
                    continue
                    
        # Apply Gaussian blur to smooth the heatmap
        sigma = self.heatmap_sigma * grid_size  # Scale sigma based on grid size
        heatmap = gaussian_filter(heatmap, sigma=sigma)
        
        # Normalize to [0,1]
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
            
        return heatmap

    def _cluster_elements_by_location(self, tracks: List[ElementTrack]) -> List[List[ElementTrack]]:
        """
        Cluster elements by their spatial location using DBSCAN.
        
        Args:
            tracks: List of element tracks to cluster
            
        Returns:
            List of lists, where each inner list contains tracks in one cluster
        """
        if not tracks:
            return []
            
        # Extract the center point of each track's first occurrence
        centers = []
        for track in tracks:
            try:
                bbox = track.first_occurrence.bbox
                center = self._get_element_center(bbox)
                centers.append(center)
            except Exception as e:
                logger.error(f"Error getting center for track {track.track_id}: {e}")
                # Add a placeholder to maintain index alignment
                centers.append((0.5, 0.5))
                
        # Convert to numpy array for DBSCAN
        centers = np.array(centers)
        
        # Apply DBSCAN clustering
        clustering = DBSCAN(eps=self.dbscan_epsilon, min_samples=self.dbscan_min_samples).fit(centers)
        
        # Get unique cluster labels (excluding noise points labeled as -1)
        unique_clusters = set(clustering.labels_)
        if -1 in unique_clusters:
            unique_clusters.remove(-1)
            
        # Group tracks by cluster
        clusters = []
        for cluster_id in unique_clusters:
            cluster_tracks = [track for i, track in enumerate(tracks) if clustering.labels_[i] == cluster_id]
            clusters.append(cluster_tracks)
            
        # Add a "noise" cluster if there are any
        noise_tracks = [track for i, track in enumerate(tracks) if clustering.labels_[i] == -1]
        if noise_tracks:
            clusters.append(noise_tracks)
            
        logger.info(f"Clustered {len(tracks)} tracks into {len(clusters)} spatial clusters")
        return clusters

    def _identify_dynamic_regions_advanced(self, static_tracks: List[ElementTrack], 
                                           dynamic_tracks: List[ElementTrack],
                                           grid_size: int = 100) -> List[List[float]]:
        """
        Identify dynamic regions using a more advanced approach:
        1. Create heatmaps for static and dynamic elements
        2. Find areas with high dynamic-to-static ratio
        3. Cluster these areas into coherent regions
        
        Args:
            static_tracks: Tracks classified as static
            dynamic_tracks: Tracks classified as dynamic
            grid_size: Size of the heatmap grid
            
        Returns:
            List of bounding boxes representing dynamic regions
        """
        # Create heatmaps for static and dynamic elements
        static_heatmap = self._create_element_heatmap(static_tracks, grid_size)
        dynamic_heatmap = self._create_element_heatmap(dynamic_tracks, grid_size)
        
        # Find ratio of dynamic to static+dynamic (avoid division by zero)
        combined_heatmap = static_heatmap + dynamic_heatmap
        ratio_heatmap = np.zeros_like(combined_heatmap)
        
        # Only calculate ratio where there are elements
        valid_mask = combined_heatmap > 0.05  # Small threshold to avoid noise
        ratio_heatmap[valid_mask] = dynamic_heatmap[valid_mask] / combined_heatmap[valid_mask]
        
        # If we don't have enough dynamic content, fall back to the original approach
        if np.sum(ratio_heatmap > 0.5) < (grid_size * grid_size * 0.01):  # At least 1% of pixels
            logger.info("Not enough clear dynamic content, falling back to geometric approach")
            static_bbox = self._calculate_static_region_bbox(static_tracks)
            return self._calculate_dynamic_regions(static_bbox)
            
        # Threshold the ratio heatmap to find dynamic areas
        dynamic_area_mask = ratio_heatmap > 0.5  # Areas where dynamic > 50% of content
        
        # Group connected dynamic areas using connected component labeling
        # Ensure dynamic_area_mask is correct type (integer) to avoid Literal iteration errors
        dynamic_area_mask_int = np.asarray(dynamic_area_mask, dtype=np.int32)
        labeled_array, num_features = scipy_label(dynamic_area_mask_int)
        
        if num_features == 0:
            logger.info("No clear dynamic regions found in the ratio heatmap")
            # Fall back to geometric approach
            static_bbox = self._calculate_static_region_bbox(static_tracks)
            return self._calculate_dynamic_regions(static_bbox)
            
        # Convert each labeled region to a bounding box
        dynamic_regions = []
        for i in range(1, num_features + 1):  # Start from 1 as 0 is background
            # Get coordinates of this region
            y_indices, x_indices = np.where(labeled_array == i)
            
            if len(y_indices) == 0 or len(x_indices) == 0:
                continue
                
            # Calculate bounding box in grid coordinates
            grid_y1 = np.min(y_indices) if len(y_indices) > 0 else 0
            grid_x1 = np.min(x_indices) if len(x_indices) > 0 else 0
            grid_y2 = np.max(y_indices) + 1 if len(y_indices) > 0 else 0  # +1 because upper bound is exclusive
            grid_x2 = np.max(x_indices) + 1 if len(x_indices) > 0 else 0
            
            # Convert to normalized coordinates
            x1 = grid_x1 / grid_size
            y1 = grid_y1 / grid_size
            x2 = grid_x2 / grid_size
            y2 = grid_y2 / grid_size
            
            # Add to list if area is significant
            area = (x2 - x1) * (y2 - y1)
            if area > 0.01:  # At least 1% of the screen
                dynamic_regions.append([x1, y1, x2, y2])
                
        logger.info(f"Identified {len(dynamic_regions)} dynamic regions using heatmap approach")
        
        # If no significant regions found, fall back to geometric approach
        if not dynamic_regions:
            static_bbox = self._calculate_static_region_bbox(static_tracks)
            return self._calculate_dynamic_regions(static_bbox)
            
        return dynamic_regions

    def _calculate_static_region_bbox(self, static_tracks: List[ElementTrack]) -> Optional[List[float]]:
        """
        Calculates the overall bounding box for static elements.
        Now uses only tracks classified as static rather than all persistent tracks.
        """
        if not static_tracks:
            logger.info("No static tracks found, cannot define static region.")
            return None

        # Collect all bounding boxes from all occurrences in static tracks
        all_bboxes = [occ.bbox for track in static_tracks for occ in track.occurrences]

        if not all_bboxes:
             logger.warning("Static tracks found, but they contain no bounding boxes.")
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

            # Handle potential edge cases
            if max_x2 <= min_x1 or max_y2 <= min_y1:
                 logger.warning(f"Static region calculation resulted in invalid bbox. Returning None.")
                 return None

            static_bbox = [min_x1, min_y1, max_x2, max_y2]
            logger.info(f"Calculated static region union bbox: " 
                        f"[ {static_bbox[0]:.3f}, {static_bbox[1]:.3f}, {static_bbox[2]:.3f}, {static_bbox[3]:.3f} ]")
            return static_bbox

        except Exception as e:
            logger.error(f"Error calculating static region bounding box: {e}", exc_info=True)
            return None

    def _calculate_dynamic_regions(self, static_bbox: Optional[List[float]]) -> List[List[float]]:
        """
        Calculates potential dynamic regions by subtracting the static region
        from the full screen area.
        """
        screen_bbox = [0.0, 0.0, 1.0, 1.0]

        if static_bbox is None:
            logger.info("No static region defined, considering entire screen dynamic.")
            return [screen_bbox]

        sx1, sy1, sx2, sy2 = static_bbox
        dynamic_regions: List[List[float]] = []

        # Region above static area
        if sy1 > 1e-6:
            dynamic_regions.append([0.0, 0.0, 1.0, sy1])
        # Region below static area
        if sy2 < 1.0 - 1e-6:
            dynamic_regions.append([0.0, sy2, 1.0, 1.0])
        # Region left of static area
        if sx1 > 1e-6:
            dynamic_regions.append([0.0, sy1, sx1, sy2])
        # Region right of static area
        if sx2 < 1.0 - 1e-6:
            dynamic_regions.append([sx2, sy1, 1.0, sy2])

        # Filter out invalid or zero-area regions
        valid_dynamic_regions = []
        min_area = 1e-5
        for r in dynamic_regions:
            if r[0] < r[2] - 1e-6 and r[1] < r[3] - 1e-6:
                 r = [max(0.0, min(1.0, coord)) for coord in r]
                 width = r[2] - r[0]
                 height = r[3] - r[1]
                 if width > 1e-6 and height > 1e-6 and (width * height) > min_area:
                     valid_dynamic_regions.append(r)

        logger.info(f"Identified {len(valid_dynamic_regions)} potential dynamic regions based on static area.")
        return valid_dynamic_regions

    def _apply_selection_rules(self,
                              dynamic_regions: List[List[float]],
                              all_frame_data: List[List[FrameElement]]) -> Dict[str, Optional[List[float]]]:
        """
        Applies deterministic rules to select the 'main' dynamic area.
        """
        results: Dict[str, Optional[List[float]]] = {}
        rule_names = ["largest_area", "most_elements", "highest_variation"]

        # Initialize results
        for rule_name in rule_names:
            results[rule_name] = None

        if not dynamic_regions:
            logger.warning("No dynamic regions provided to apply selection rules.")
            return results

        if len(dynamic_regions) == 1:
            # If only one region, it's the main area by default for all rules
            main_bbox = dynamic_regions[0]
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

        # --- Rule B: Most Elements ---
        max_avg_elements = -1.0
        most_elements_bbox = None
        total_valid_frames = len(all_frame_data)

        if total_valid_frames > 0:
            for region_bbox in dynamic_regions:
                total_elements_in_region = 0
                rx1, ry1, rx2, ry2 = region_bbox

                for frame_data in all_frame_data:
                    count_in_frame = 0
                    for element in frame_data:
                        try:
                            ex, ey = self._get_element_center(element.bbox)
                            if rx1 <= ex < rx2 and ry1 <= ey < ry2:
                                 count_in_frame += 1
                        except Exception as e:
                             logger.error(f"Error checking element against region: {e}")
                    total_elements_in_region += count_in_frame

                avg_elements = total_elements_in_region / total_valid_frames
                if avg_elements > max_avg_elements:
                     max_avg_elements = avg_elements
                     most_elements_bbox = region_bbox

            results["most_elements"] = most_elements_bbox
        else:
             results["most_elements"] = None

        # --- New Rule C: Highest Content Variation ---
        highest_variation = -1.0
        highest_variation_bbox = None
        
        if total_valid_frames > 0:
            for region_bbox in dynamic_regions:
                region_variation = 0.0
                rx1, ry1, rx2, ry2 = region_bbox
                
                # Look at elements in all frames and calculate content variation
                all_elements_in_region = []
                for frame_index, frame_data in enumerate(all_frame_data):
                    frame_elements = []
                    for element in frame_data:
                        try:
                            ex, ey = self._get_element_center(element.bbox)
                            if rx1 <= ex < rx2 and ry1 <= ey < ry2:
                                frame_elements.append(element)
                        except Exception:
                            continue
                    all_elements_in_region.append(frame_elements)
                
                # Skip if too few frames have elements
                if sum(1 for frame in all_elements_in_region if frame) < 2:
                    continue
                
                # Calculate content variation across frames
                content_sets = [
                    set(element.content for element in frame if element.content)
                    for frame in all_elements_in_region
                ]
                
                # Skip if no content
                if not any(content_sets):
                    continue
                
                # Count unique contents
                all_contents = set()
                for content_set in content_sets:
                    all_contents.update(content_set)
                
                # Calculate Jaccard distance between frame contents
                num_frames_with_content = sum(1 for s in content_sets if s)
                if num_frames_with_content >= 2:
                    total_distance = 0
                    comparisons = 0
                    content_sets = [s for s in content_sets if s]  # Only consider non-empty sets
                    
                    for i in range(len(content_sets)):
                        for j in range(i+1, len(content_sets)):
                            set1 = content_sets[i]
                            set2 = content_sets[j]
                            if set1 and set2:
                                # Jaccard distance = 1 - (intersection / union)
                                intersection = len(set1.intersection(set2))
                                union = len(set1.union(set2))
                                if union > 0:
                                    distance = 1.0 - (intersection / union)
                                    total_distance += distance
                                    comparisons += 1
                    
                    if comparisons > 0:
                        region_variation = total_distance / comparisons
                
                if region_variation > highest_variation:
                    highest_variation = region_variation
                    highest_variation_bbox = region_bbox
        
        results["highest_variation"] = highest_variation_bbox
        logger.debug(f"Rule 'highest_variation' selected bbox with variation score {highest_variation:.2f}")

        return results

    # === Main Detection Method ===
    def detect_main_areas(self, results_list: OmniParserResultModelList) -> Dict[str, Optional[List[float]]]:
        """
        Detects the main dynamic content area(s) from a sequence of OmniParser results.
        
        This improved version uses:
        1. Content variation to distinguish static vs. dynamic elements
        2. Spatial clustering with DBSCAN for better region detection
        3. Heatmap-based approach for identifying dynamic areas
        """
        logger.info(f"Starting dynamic area detection for {len(results_list.omniparser_result_models)} pre-parsed frames.")
        default_result: Dict[str, Optional[List[float]]] = {
            "largest_area": None, 
            "most_elements": None,
            "highest_variation": None
        }

        if not isinstance(results_list, OmniParserResultModelList) or len(results_list.omniparser_result_models) < 2:
            logger.warning("Input must be an OmniParserResultModelList with at least 2 results.")
            return default_result

        # --- Step 1: Extract FrameElement Data ---
        all_frame_data: List[List[FrameElement]] = []
        valid_frame_count = 0

        for frame_index, omni_model in enumerate(results_list.omniparser_result_models):
            frame_elements: List[FrameElement] = []
            screenshot_path = omni_model.omniparser_result.original_image_path
            logger.info(f"Extracting elements for frame {frame_index}: {os.path.basename(screenshot_path)}")

            try:
                if not os.path.exists(screenshot_path):
                    logger.error(f"Screenshot file not found for frame {frame_index}: {screenshot_path}")
                    continue

                img = Image.open(screenshot_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width == 0 or height == 0:
                    logger.error(f"Invalid image dimensions ({width}x{height}) for frame {frame_index}")
                    continue

                if not omni_model.parsed_content_results:
                     logger.warning(f"No parsed content results found for frame {frame_index}.")
                     all_frame_data.append(frame_elements)
                     valid_frame_count += 1
                     continue

                for pcr in omni_model.parsed_content_results:
                    bbox_normalized = pcr.bbox

                    if not isinstance(bbox_normalized, list) or len(bbox_normalized) != 4:
                        continue
                    if not all(isinstance(coord, (int, float)) for coord in bbox_normalized):
                        continue
                    
                    if max(bbox_normalized) <= 1.0 + 1e-6:
                        x1_abs = int(bbox_normalized[0] * width)
                        y1_abs = int(bbox_normalized[1] * height)
                        x2_abs = int(bbox_normalized[2] * width)
                        y2_abs = int(bbox_normalized[3] * height)
                    else:
                        x1_abs, y1_abs, x2_abs, y2_abs = map(int, bbox_normalized)

                    if x1_abs >= x2_abs or y1_abs >= y2_abs:
                        if not (np.isclose(bbox_normalized[0], bbox_normalized[2]) or 
                                np.isclose(bbox_normalized[1], bbox_normalized[3])):
                            continue
                        x2_abs = max(x1_abs + 1, x2_abs)
                        y2_abs = max(y1_abs + 1, y2_abs)
                        x1_abs, y1_abs = max(0, x1_abs), max(0, y1_abs)
                        x2_abs, y2_abs = min(width, x2_abs), min(height, y2_abs)
                        if x1_abs >= x2_abs or y1_abs >= y2_abs:
                            continue

                    try:
                        patch = img.crop((x1_abs, y1_abs, x2_abs, y2_abs))
                        if patch.width < 5 or patch.height < 5:
                            continue

                        embedding = self.embedder.get_embedding(patch)

                        frame_elements.append(FrameElement(
                            frame_index=frame_index,
                            element_id=pcr.id,
                            parsed_content_result=pcr,
                            embedding=embedding
                        ))
                    except Exception as e:
                        logger.error(f"Failed to process element ID {pcr.id} in frame {frame_index}: {e}")
                        continue

                logger.info(f"Extracted {len(frame_elements)} valid elements from frame {frame_index}")
                all_frame_data.append(frame_elements)
                valid_frame_count += 1

            except Exception as e:
                logger.error(f"Unexpected error processing frame {frame_index}: {e}")
                continue

        if valid_frame_count < 2:
             logger.error(f"Failed to process enough frames ({valid_frame_count}) for analysis. Need at least 2.")
             return default_result

        # --- Step 2: Track Elements ---
        self._track_id_counter = itertools.count()
        try:
            all_tracks = self._track_elements(all_frame_data)
            # Now we get both static and dynamic tracks
            static_tracks, dynamic_tracks = self._get_persistent_tracks(all_tracks, valid_frame_count)
        except Exception as e:
             logger.error(f"Error during element tracking: {e}", exc_info=True)
             return default_result

        # --- Step 3: Identify Dynamic Regions (Enhanced Method) ---
        try:
            # Use the enhanced method that leverages both static and dynamic tracks
            dynamic_regions = self._identify_dynamic_regions_advanced(static_tracks, dynamic_tracks)
            
            # If that didn't work, fall back to traditional approach
            if not dynamic_regions:
                logger.info("Advanced detection found no regions, falling back to traditional method")
                static_region_bbox = self._calculate_static_region_bbox(static_tracks)
                dynamic_regions = self._calculate_dynamic_regions(static_region_bbox)
        except Exception as e:
             logger.error(f"Error calculating dynamic regions: {e}", exc_info=True)
             return default_result

        # --- Step 4: Apply Selection Rules ---
        try:
             main_area_results = self._apply_selection_rules(dynamic_regions, all_frame_data)
        except Exception as e:
             logger.error(f"Error applying selection rules: {e}", exc_info=True)
             return default_result

        logger.info("Dynamic area detection completed successfully.")
        return main_area_results