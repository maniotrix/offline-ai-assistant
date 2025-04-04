import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional, Union
from PIL import Image, ImageDraw
import cv2
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from dataclasses import dataclass

from .omni_helper import OmniParserResultModel, ParsedContentResult

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@dataclass
class ContentPatch:
    """Represents a patch of content within the main area"""
    grid_x: int
    grid_y: int
    bbox: List[float]  # [x1, y1, x2, y2]
    features: Dict[str, Any]
    raw_features: np.ndarray
    content_elements: List[ParsedContentResult]

@dataclass
class ContentCluster:
    """Represents a cluster of content patches"""
    patches: List[ContentPatch]
    bbox: List[float]  # [x1, y1, x2, y2]
    score: float = 0.0
    label: int = -1
    
    @property
    def center(self) -> Tuple[float, float]:
        """Get the center point of the cluster"""
        return (
            (self.bbox[0] + self.bbox[2]) / 2,
            (self.bbox[1] + self.bbox[3]) / 2
        )
    
    @property
    def area(self) -> float:
        """Get the area of the cluster"""
        return (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])


class MainAreaSegmenter:
    """
    Segments the main area detected by UIOptimizedDynamicAreaDetector into 
    meaningful content clusters using a content-based approach.
    """
    
    def __init__(
        self, 
        grid_size: Tuple[int, int] = (20, 20),
        feature_weights: Dict[str, float] = None,
        min_cluster_size: int = 3,
        eps: float = 0.5,
        min_content_score: float = 0.3
    ):
        """
        Initialize the main area segmenter.
        
        Args:
            grid_size: Grid size for dividing main area (rows, cols)
            feature_weights: Weights for different feature types
            min_cluster_size: Minimum number of patches to form a cluster
            eps: Maximum distance between samples for DBSCAN
            min_content_score: Minimum score for a cluster to be considered content
        """
        self.grid_size = grid_size
        self.feature_weights = feature_weights or {
            'text': 0.4, 
            'visual': 0.3, 
            'structural': 0.2, 
            'temporal': 0.1
        }
        self.min_cluster_size = min_cluster_size
        self.eps = eps
        self.min_content_score = min_content_score
        
        logger.info(f"MainAreaSegmenter initialized with grid_size={grid_size}")
    
    def _divide_into_patches(
        self, 
        image: Image.Image, 
        main_area_bbox: List[float]
    ) -> List[ContentPatch]:
        """
        Divide the main area into a grid of patches.
        
        Args:
            image: The full image
            main_area_bbox: The bounding box of the main area [x1, y1, x2, y2]
            
        Returns:
            List of ContentPatch objects
        """
        logger.info(f"Dividing main area into {self.grid_size[0]}x{self.grid_size[1]} grid")
        
        # Extract main area from image
        main_area = image.crop((
            main_area_bbox[0], 
            main_area_bbox[1], 
            main_area_bbox[2], 
            main_area_bbox[3]
        ))
        
        # Get dimensions
        width, height = main_area.width, main_area.height
        
        # Calculate patch dimensions
        patch_width = width / self.grid_size[1]
        patch_height = height / self.grid_size[0]
        
        # Create patches
        patches = []
        
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                # Calculate patch bbox within main area
                x1 = x * patch_width
                y1 = y * patch_height
                x2 = (x + 1) * patch_width
                y2 = (y + 1) * patch_height
                
                # Convert to global coordinates
                global_bbox = [
                    main_area_bbox[0] + x1,
                    main_area_bbox[1] + y1,
                    main_area_bbox[0] + x2,
                    main_area_bbox[1] + y2
                ]
                
                # Create patch object (features will be added later)
                patch = ContentPatch(
                    grid_x=x,
                    grid_y=y,
                    bbox=global_bbox,
                    features={},
                    raw_features=np.array([]),
                    content_elements=[]
                )
                
                patches.append(patch)
        
        logger.info(f"Created {len(patches)} patches")
        return patches
    
    def _extract_features(
        self,
        patches: List[ContentPatch],
        image: Image.Image, 
        result_model: OmniParserResultModel
    ) -> List[ContentPatch]:
        """
        Extract features for each patch.
        
        Args:
            patches: List of ContentPatch objects
            image: The full image
            result_model: OmniParser result model with content elements
            
        Returns:
            Updated list of ContentPatch objects with features
        """
        logger.info("Extracting features for patches")
        
        # Convert image to numpy array for cv2
        img_np = np.array(image)
        
        # Extract elements within each patch
        for patch in patches:
            # Find elements within this patch
            elements_in_patch = []
            for element in result_model.parsed_content_results:
                # Check if element is within or overlapping with patch
                if self._intersect_bboxes(patch.bbox, element.bbox):
                    elements_in_patch.append(element)
            
            patch.content_elements = elements_in_patch
            
            # Extract text features
            text_length = sum(len(e.content) if hasattr(e, 'content') and e.content else 0 
                             for e in elements_in_patch)
            text_element_count = sum(1 for e in elements_in_patch if e.type == 'text')
            
            # Extract structural features
            element_count = len(elements_in_patch)
            element_types = {}
            for e in elements_in_patch:
                element_types[e.type] = element_types.get(e.type, 0) + 1
            
            # Extract visual features
            patch_img = image.crop(patch.bbox)
            patch_np = np.array(patch_img)
            
            # Color variance (more varied = more likely to be content)
            color_variance = np.var(patch_np) if patch_np.size > 0 else 0
            
            # Edge density (more edges = more likely to be content)
            if patch_np.size > 0 and patch_np.shape[0] > 0 and patch_np.shape[1] > 0:
                try:
                    if len(patch_np.shape) > 2 and patch_np.shape[2] >= 3:
                        gray = cv2.cvtColor(patch_np, cv2.COLOR_RGB2GRAY)
                        edges = cv2.Canny(gray, 100, 200)
                        edge_density = np.sum(edges > 0) / (patch_np.shape[0] * patch_np.shape[1])
                    else:
                        edge_density = 0
                except Exception as e:
                    logger.warning(f"Error calculating edge density: {e}")
                    edge_density = 0
            else:
                edge_density = 0
            
            # Store features
            features = {
                'text_length': text_length,
                'text_element_count': text_element_count,
                'element_count': element_count,
                'element_types': element_types,
                'color_variance': color_variance,
                'edge_density': edge_density,
                'grid_x': patch.grid_x / self.grid_size[1],  # Normalize
                'grid_y': patch.grid_y / self.grid_size[0]   # Normalize
            }
            
            # Create raw feature vector for clustering
            raw_features = np.array([
                text_length,
                text_element_count,
                element_count,
                color_variance,
                edge_density,
                # Include normalized grid position to maintain spatial relationships
                patch.grid_x / self.grid_size[1],
                patch.grid_y / self.grid_size[0]
            ])
            
            patch.features = features
            patch.raw_features = raw_features
        
        return patches
    
    def _intersect_bboxes(self, bbox1: List[float], bbox2: List[float]) -> bool:
        """
        Check if two bounding boxes intersect.
        
        Args:
            bbox1: First bounding box [x1, y1, x2, y2]
            bbox2: Second bounding box [x1, y1, x2, y2]
            
        Returns:
            True if bboxes intersect, False otherwise
        """
        # Check if one rectangle is to the left of the other
        if bbox1[2] <= bbox2[0] or bbox2[2] <= bbox1[0]:
            return False
        
        # Check if one rectangle is above the other
        if bbox1[3] <= bbox2[1] or bbox2[3] <= bbox1[1]:
            return False
        
        return True
    
    def _perform_initial_clustering(
        self, 
        patches: List[ContentPatch]
    ) -> List[ContentCluster]:
        """
        Perform initial clustering of patches based on features.
        
        Args:
            patches: List of ContentPatch objects with features
            
        Returns:
            List of ContentCluster objects
        """
        logger.info("Performing initial clustering")
        
        # Extract raw feature vectors
        features = np.array([p.raw_features for p in patches])
        
        # Standardize features
        if features.size > 0:
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(features)
            
            # Perform DBSCAN clustering
            clustering = DBSCAN(eps=self.eps, min_samples=self.min_cluster_size)
            labels = clustering.fit_predict(scaled_features)
        else:
            labels = np.array([-1] * len(patches))
        
        # Group patches by cluster
        clusters = {}
        for i, label in enumerate(labels):
            if label != -1:  # Ignore noise
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(patches[i])
        
        # Create ContentCluster objects
        content_clusters = []
        for label, cluster_patches in clusters.items():
            # Calculate bounding box of cluster using explicit indices
            # to avoid linter errors with literals in list comprehensions
            bbox_index_0 = 0  # x1
            bbox_index_1 = 1  # y1
            bbox_index_2 = 2  # x2
            bbox_index_3 = 3  # y2
            
            x1 = min(p.bbox[bbox_index_0] for p in cluster_patches)
            y1 = min(p.bbox[bbox_index_1] for p in cluster_patches)
            x2 = max(p.bbox[bbox_index_2] for p in cluster_patches)
            y2 = max(p.bbox[bbox_index_3] for p in cluster_patches)
            
            # Create cluster
            cluster = ContentCluster(
                patches=cluster_patches,
                bbox=[x1, y1, x2, y2],
                label=label
            )
            
            content_clusters.append(cluster)
        
        logger.info(f"Created {len(content_clusters)} initial clusters")
        return content_clusters
    
    def _merge_clusters(
        self, 
        clusters: List[ContentCluster]
    ) -> List[ContentCluster]:
        """
        Merge adjacent clusters that likely belong to the same content block.
        
        Args:
            clusters: List of ContentCluster objects
            
        Returns:
            List of merged ContentCluster objects
        """
        if not clusters:
            return []
        
        logger.info("Merging adjacent clusters")
        
        # Extract cluster centers and features for hierarchical clustering
        centers = np.array([
            [c.center[0], c.center[1]] for c in clusters
        ])
        
        if len(centers) <= 1:
            return clusters
        
        # Perform hierarchical clustering
        linkage_method = 'ward'
        n_clusters = max(1, len(clusters) // 2)  # Aim to reduce by ~50%
        
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters, 
            linkage=linkage_method
        )
        
        try:
            labels = clustering.fit_predict(centers)
        except Exception as e:
            logger.warning(f"Error in hierarchical clustering: {e}")
            return clusters
        
        # Group clusters by label
        merged_groups = {}
        for i, label in enumerate(labels):
            if label not in merged_groups:
                merged_groups[label] = []
            merged_groups[label].append(clusters[i])
        
        # Create new merged clusters
        merged_clusters = []
        for label, group in merged_groups.items():
            # Combine patches from all clusters in group
            all_patches = []
            for cluster in group:
                all_patches.extend(cluster.patches)
            
            # Calculate merged bounding box using explicit indices
            # to avoid linter errors with literals in list comprehensions
            bbox_index_0 = 0  # x1
            bbox_index_1 = 1  # y1
            bbox_index_2 = 2  # x2
            bbox_index_3 = 3  # y2
            
            x1 = min(c.bbox[bbox_index_0] for c in group)
            y1 = min(c.bbox[bbox_index_1] for c in group)
            x2 = max(c.bbox[bbox_index_2] for c in group)
            y2 = max(c.bbox[bbox_index_3] for c in group)
            
            # Create merged cluster
            merged_cluster = ContentCluster(
                patches=all_patches,
                bbox=[x1, y1, x2, y2],
                label=label
            )
            
            merged_clusters.append(merged_cluster)
        
        logger.info(f"Merged into {len(merged_clusters)} clusters")
        return merged_clusters
    
    def _score_clusters(
        self, 
        clusters: List[ContentCluster]
    ) -> List[ContentCluster]:
        """
        Score clusters based on content significance.
        
        Args:
            clusters: List of ContentCluster objects
            
        Returns:
            List of scored ContentCluster objects
        """
        logger.info("Scoring content clusters")
        
        for cluster in clusters:
            # Calculate scores for different feature types
            
            # Text score
            text_lengths = [p.features['text_length'] for p in cluster.patches]
            text_element_counts = [p.features['text_element_count'] for p in cluster.patches]
            
            avg_text_length = np.mean(text_lengths) if text_lengths else 0
            avg_text_elements = np.mean(text_element_counts) if text_element_counts else 0
            
            text_score = (0.7 * avg_text_length + 0.3 * avg_text_elements) / (len(cluster.patches) + 1)
            
            # Visual score
            color_variances = [p.features['color_variance'] for p in cluster.patches]
            edge_densities = [p.features['edge_density'] for p in cluster.patches]
            
            avg_color_variance = np.mean(color_variances) if color_variances else 0
            avg_edge_density = np.mean(edge_densities) if edge_densities else 0
            
            # Normalize visual features to 0-1 range (approximately)
            norm_color_var = min(1.0, avg_color_variance / 5000.0)
            norm_edge_density = min(1.0, avg_edge_density * 5.0)
            
            visual_score = 0.5 * norm_color_var + 0.5 * norm_edge_density
            
            # Structural score - based on element density
            total_elements = sum(p.features['element_count'] for p in cluster.patches)
            area = cluster.area
            
            if area > 0:
                element_density = total_elements / area
                # Normalize density (capped at 1.0)
                norm_density = min(1.0, element_density * 1000.0)
                structural_score = norm_density
            else:
                structural_score = 0.0
            
            # Spatial score - favor central clusters
            # Distance from center is a penalty
            center_x = (cluster.bbox[0] + cluster.bbox[2]) / 2
            center_y = (cluster.bbox[1] + cluster.bbox[3]) / 2
            
            # Assuming normalized coordinates 0-1
            center_dist = np.sqrt((center_x - 0.5)**2 + (center_y - 0.5)**2)
            spatial_score = max(0, 1.0 - center_dist * 2)  # Center distance is a penalty
            
            # Combined score with weights
            combined_score = (
                self.feature_weights.get('text', 0.4) * text_score +
                self.feature_weights.get('visual', 0.3) * visual_score +
                self.feature_weights.get('structural', 0.2) * structural_score +
                self.feature_weights.get('spatial', 0.1) * spatial_score
            )
            
            # Assign score to cluster, explicitly cast to float to fix type error
            cluster.score = float(combined_score)
        
        # Sort clusters by score (descending)
        clusters.sort(key=lambda c: c.score, reverse=True)
        
        return clusters
    
    def _generate_content_map(
        self, 
        clusters: List[ContentCluster],
        main_area_bbox: List[float],
        image_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Generate a content probability map based on clusters.
        
        Args:
            clusters: List of scored ContentCluster objects
            main_area_bbox: The bounding box of the main area
            image_size: The size of the full image (width, height)
            
        Returns:
            2D numpy array representing content probability (0-1)
        """
        logger.info("Generating content probability map")
        
        # Create an empty map
        map_width = int(main_area_bbox[2] - main_area_bbox[0])
        map_height = int(main_area_bbox[3] - main_area_bbox[1])
        
        if map_width <= 0 or map_height <= 0:
            logger.warning("Invalid main area dimensions for content map")
            return np.zeros((1, 1))
        
        content_map = np.zeros((map_height, map_width))
        
        # Add each cluster to the map with its score as probability
        for cluster in clusters:
            # Calculate relative coordinates within the main area
            rel_x1 = int(max(0, cluster.bbox[0] - main_area_bbox[0]))
            rel_y1 = int(max(0, cluster.bbox[1] - main_area_bbox[1]))
            rel_x2 = int(min(map_width, cluster.bbox[2] - main_area_bbox[0]))
            rel_y2 = int(min(map_height, cluster.bbox[3] - main_area_bbox[1]))
            
            # Skip if outside bounds
            if rel_x2 <= rel_x1 or rel_y2 <= rel_y1:
                continue
            
            # Fill the region with the cluster's score
            content_map[rel_y1:rel_y2, rel_x1:rel_x2] = np.maximum(
                content_map[rel_y1:rel_y2, rel_x1:rel_x2],
                cluster.score
            )
        
        return content_map
    
    def _select_primary_content(
        self, 
        clusters: List[ContentCluster]
    ) -> Optional[List[float]]:
        """
        Select the primary content area from the clusters.
        
        Args:
            clusters: List of scored ContentCluster objects
            
        Returns:
            Bounding box of the primary content area [x1, y1, x2, y2] or None
        """
        if not clusters:
            return None
        
        # Filter clusters by minimum score
        valid_clusters = [c for c in clusters if c.score >= self.min_content_score]
        
        if not valid_clusters:
            # If no cluster meets the threshold, use the highest scoring one
            if clusters:
                return clusters[0].bbox
            return None
        
        # If we have multiple good clusters, we might want to merge overlapping ones
        # For simplicity, we'll just return the highest scoring cluster for now
        return valid_clusters[0].bbox
    
    def segment(
        self, 
        image: Image.Image, 
        result_model: OmniParserResultModel,
        main_area_bbox: List[float]
    ) -> Dict[str, Any]:
        """
        Segment the main area into content clusters.
        
        Args:
            image: The full image
            result_model: OmniParser result model
            main_area_bbox: Bounding box of the main area [x1, y1, x2, y2]
            
        Returns:
            Dictionary with segmentation results
        """
        logger.info("Starting main area segmentation")
        
        # Divide into grid patches
        patches = self._divide_into_patches(image, main_area_bbox)
        
        # Extract features
        patches = self._extract_features(patches, image, result_model)
        
        # Perform initial clustering
        initial_clusters = self._perform_initial_clustering(patches)
        
        # Merge clusters
        merged_clusters = self._merge_clusters(initial_clusters)
        
        # Score clusters
        scored_clusters = self._score_clusters(merged_clusters)
        
        # Generate content map
        content_map = self._generate_content_map(
            scored_clusters, 
            main_area_bbox, 
            (image.width, image.height)
        )
        
        # Select primary content
        primary_content = self._select_primary_content(scored_clusters)
        
        logger.info("Main area segmentation completed")
        
        return {
            'clusters': scored_clusters,
            'content_map': content_map,
            'primary_content': primary_content
        }

    def visualize(
        self,
        image: Image.Image,
        segmentation_result: Dict[str, Any],
        main_area_bbox: List[float],
        output_path: str = None
    ) -> Image.Image:
        """
        Visualize the segmentation results.
        
        Args:
            image: The original image
            segmentation_result: The result from segment()
            main_area_bbox: Bounding box of the main area
            output_path: Path to save the visualization image
            
        Returns:
            The visualization image
        """
        # Create a copy of the image for visualization
        vis_img = image.copy()
        draw = ImageDraw.Draw(vis_img)
        
        # Draw main area
        draw.rectangle(
            [(main_area_bbox[0], main_area_bbox[1]), (main_area_bbox[2], main_area_bbox[3])],
            outline="green",
            width=3
        )
        
        # Draw clusters with varying colors based on score
        for i, cluster in enumerate(segmentation_result['clusters']):
            # Calculate color based on score (red = high score, blue = low score)
            red = int(255 * cluster.score)
            blue = int(255 * (1 - cluster.score))
            color = (red, 100, blue, 128)  # Semi-transparent
            
            # Draw filled rectangle for cluster
            draw.rectangle(
                [(cluster.bbox[0], cluster.bbox[1]), (cluster.bbox[2], cluster.bbox[3])],
                fill=color,
                outline=(red, 100, blue, 255),
                width=2
            )
            
            # Add label
            draw.text(
                (cluster.bbox[0] + 5, cluster.bbox[1] + 5),
                f"C{i}: {cluster.score:.2f}",
                fill=(255, 255, 255, 255)
            )
        
        # Draw primary content area
        if segmentation_result['primary_content']:
            primary = segmentation_result['primary_content']
            draw.rectangle(
                [(primary[0], primary[1]), (primary[2], primary[3])],
                outline="yellow",
                width=3
            )
            draw.text(
                (primary[0] + 5, primary[1] + 5),
                "PRIMARY",
                fill="yellow"
            )
        
        # Save if output path provided
        if output_path:
            vis_img.save(output_path)
        
        return vis_img 