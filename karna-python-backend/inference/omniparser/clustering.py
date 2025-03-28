from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from omniparser.omni_helper import ParsedContentResult
from omniparser.util.omniparser import OmniparserResult
from omniparser.clustering_models import ClusterModelHeirarchy, get_crop_area_from_bbox_type, CropArea
from logging import getLogger
import numpy as np
from sklearn.cluster import DBSCAN

logger = getLogger(__name__)
class ClusterPreprocessor:
    """
    This class contains the code for clustering the parsed content results.
    
    The clustering is done by the following steps:
    1. Get the parsed content results of an image
    2. Get clustering heirarchy dict with nested clusters, top level crop area of image for clustering
    3. Cluster the parsed content results based on the clustering heirarchy
    4. Return the clustered results
    """

    def __init__(self, parsed_content_results: List[ParsedContentResult],
                 clustering_heirarchy: ClusterModelHeirarchy,
                 omniparser_result: OmniparserResult):
        self.parsed_content_results = parsed_content_results
        self.clustering_heirarchy = clustering_heirarchy
        self.omniparser_result = omniparser_result
        self.clustering_worker_attention_bbox = get_crop_area_from_bbox_type(self.clustering_heirarchy.root_cluster.root_crop_area_type)
        try:
            self._pre_process_parsed_content_results()
        except Exception as e:
            logger.error(f"Error pre-processing parsed content results: {e}")
            raise e
        
    def _pre_process_parsed_content_results(self):
        """
        This method pre-processes the parsed content results.
        """
        for parsed_content_result in self.parsed_content_results:
            parsed_content_result.bbox = self._convert_relative_bbox_to_absolute_bbox(
                parsed_content_result.bbox, 
                self.omniparser_result.original_image_width, 
                self.omniparser_result.original_image_height)
            
    def _convert_relative_bbox_to_absolute_bbox(self, relative_bbox: List[float], image_width: int, image_height: int) -> List[float]:
        """
        This method converts the relative bbox to absolute bbox.
        original_realtive_bbox: [0.7447916865348816, 0.6000000238418579, 0.8177083134651184, 0.6222222447395325]
        convert to absolute bbox
        """
        absolute_bbox = [
            relative_bbox[0] * image_width,
            relative_bbox[1] * image_height,
            relative_bbox[2] * image_width,
            relative_bbox[3] * image_height
        ]
        # round the bbox to the nearest integer
        absolute_bbox = [float(round(coord)) for coord in absolute_bbox]
        # convert to absolute bbox
        return absolute_bbox

@dataclass
class ClusterResult:
    """
    This class contains the cluster id and the parsed content results within the cluster.
    """
    cluster_result_id: str
    parsed_content_results: List[ParsedContentResult]

class ClusterWorker:
    """
    This cluster worker takes ClusterPreprocessor object and clusters the parsed content results,
    within the worker attention bbox, with the help of ClusterModelHeirarchy object and 
    returns the clustered results containing the cluster id and the parsed content results within the cluster.
    
    Guidelines:
    1. Get the clustering heirarchy
    2. Get the parsed content results
    3. Get the worker attention bbox
    4. Remove parsed content results that are not within the worker attention bbox
    5. Using a clustering algorithm, find all horizontal and vertical clusters within the worker attention bbox
    6. For cluster in clustering heirarchy, Where the cluster layout is container, 
    just return all bboxes which are within the cluster
    """
    cluster_results: List[ClusterResult]
    
    def __init__(self, cluster_preprocessor: ClusterPreprocessor):
        self.cluster_preprocessor = cluster_preprocessor
        self.cluster_results = []

    def cluster(self) -> List[ClusterResult]:
        raise NotImplementedError("This method should be implemented by the subclass")
        return self.cluster_results


class ClusterDBSCANWorker(ClusterWorker):
    """
    Implementation of ClusterWorker using DBSCAN for clustering.
    
    This implementation uses a two-step approach:
    1. First cluster vertically to find rows
    2. Then cluster horizontally within each vertical cluster
    
    The resulting cluster IDs are hierarchical, formatted as "v{vertical_id}_h{horizontal_id}"
    """
    
    def __init__(self, cluster_preprocessor: ClusterPreprocessor):
        super().__init__(cluster_preprocessor)
    
    def _is_within_attention_bbox(self, bbox: List[float]) -> bool:
        """
        Check if a bounding box is within the worker attention bbox.
        
        Args:
            bbox: [x1, y1, x2, y2] format bbox
            
        Returns:
            True if the bbox is within the attention bbox, False otherwise
        """
        attention_bbox: CropArea = self.cluster_preprocessor.clustering_worker_attention_bbox
        
        # Check if the center of the bbox is within the attention bbox
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        
        return (attention_bbox.x <= center_x <= attention_bbox.x + attention_bbox.width and
                attention_bbox.y <= center_y <= attention_bbox.y + attention_bbox.height)
    
    def _filter_parsed_content_results(self) -> List[ParsedContentResult]:
        """
        Filter the parsed content results to only include those within the worker attention bbox.
        
        Returns:
            List of filtered parsed content results
        """
        filtered_results = []
        for result in self.cluster_preprocessor.parsed_content_results:
            if self._is_within_attention_bbox(result.bbox):
                filtered_results.append(result)
        
        return filtered_results
    
    def _get_bbox_features(self, parsed_content_results: List[ParsedContentResult]) -> Dict[str, Any]:
        """
        Extract features from bounding boxes for clustering.
        
        Args:
            parsed_content_results: List of parsed content results
            
        Returns:
            Dictionary with different feature arrays:
            - centers: [n_boxes, 2] array of (x_center, y_center)
            - y_centers: [n_boxes, 1] array of y_centers for vertical clustering
            - heights: List of heights
            - widths: List of widths
        """
        centers = []
        y_centers = []
        heights = []
        widths = []
        
        for result in parsed_content_results:
            bbox = result.bbox
            x_center = (bbox[0] + bbox[2]) / 2
            y_center = (bbox[1] + bbox[3]) / 2
            height = bbox[3] - bbox[1]
            width = bbox[2] - bbox[0]
            
            centers.append([x_center, y_center])
            y_centers.append([y_center])
            heights.append(height)
            widths.append(width)
        
        return {
            'centers': np.array(centers),
            'y_centers': np.array(y_centers),
            'heights': heights,
            'widths': widths
        }
    
    def _cluster_vertically(self, parsed_content_results: List[ParsedContentResult]) -> Dict[int, List[ParsedContentResult]]:
        """
        Cluster the parsed content results vertically using DBSCAN.
        
        Args:
            parsed_content_results: List of parsed content results
            
        Returns:
            Dictionary mapping vertical cluster IDs to lists of parsed content results
        """
        if not parsed_content_results:
            return {}
        
        # Extract features for clustering
        features = self._get_bbox_features(parsed_content_results)
        y_centers = features['y_centers']
        heights = features['heights']
        
        # Compute dynamic epsilon based on median height
        median_height = np.median(heights) if heights else 50
        vertical_eps = median_height * 1.5  # dynamic threshold
        
        # Perform vertical clustering
        dbscan_vert = DBSCAN(eps=vertical_eps, min_samples=1)
        vert_labels = dbscan_vert.fit_predict(y_centers)
        
        # Group by vertical cluster
        vert_clusters = {}
        for i, result in enumerate(parsed_content_results):
            cluster_id = int(vert_labels[i])
            if cluster_id not in vert_clusters:
                vert_clusters[cluster_id] = []
            vert_clusters[cluster_id].append(result)
        
        # Sort clusters by average y-coordinate
        vert_clusters_with_avg = []
        for cluster_id, results in vert_clusters.items():
            y_coords = [(result.bbox[1] + result.bbox[3]) / 2 for result in results]
            avg_y = sum(y_coords) / len(y_coords) if y_coords else 0
            vert_clusters_with_avg.append((cluster_id, avg_y, results))
        
        # Sort by average y-coordinate
        vert_clusters_with_avg.sort(key=lambda x: x[1]) 
        
        # Rebuild the dictionary with sorted clusters
        vert_clusters = {}
        for i, (original_id, _, results) in enumerate(vert_clusters_with_avg):
            vert_clusters[i] = results
        
        return vert_clusters
    
    def _cluster_horizontally(self, parsed_content_results: List[ParsedContentResult]) -> Dict[int, List[ParsedContentResult]]:
        """
        Cluster the parsed content results horizontally using DBSCAN.
        
        Args:
            parsed_content_results: List of parsed content results
            
        Returns:
            Dictionary mapping horizontal cluster IDs to lists of parsed content results
        """
        if not parsed_content_results:
            return {}
        
        # Extract features for clustering
        features = self._get_bbox_features(parsed_content_results)
        centers = features['centers']
        x_centers = np.array([[center[0]] for center in centers])
        widths = features['widths']
        
        # Compute dynamic epsilon based on median width
        median_width = np.median(widths) if widths else 50
        horizontal_eps = median_width * 1.5  # dynamic threshold
        
        # Perform horizontal clustering
        dbscan_horiz = DBSCAN(eps=horizontal_eps, min_samples=1)
        horiz_labels = dbscan_horiz.fit_predict(x_centers)
        
        # Group by horizontal cluster
        horiz_clusters = {}
        for i, result in enumerate(parsed_content_results):
            cluster_id = int(horiz_labels[i])
            if cluster_id not in horiz_clusters:
                horiz_clusters[cluster_id] = []
            horiz_clusters[cluster_id].append(result)
        
        # Sort clusters by average x-coordinate
        horiz_clusters_with_avg = []
        for cluster_id, results in horiz_clusters.items():
            x_coords = [(result.bbox[0] + result.bbox[2]) / 2 for result in results]
            avg_x = sum(x_coords) / len(x_coords) if x_coords else 0
            horiz_clusters_with_avg.append((cluster_id, avg_x, results))
        
        # Sort by average x-coordinate
        horiz_clusters_with_avg.sort(key=lambda x: x[1])
        
        # Rebuild the dictionary with sorted clusters
        horiz_clusters = {}
        for i, (original_id, _, results) in enumerate(horiz_clusters_with_avg):
            horiz_clusters[i] = results
        
        return horiz_clusters
    
    def cluster(self) -> List[ClusterResult]:
        """
        Cluster the parsed content results and return the clustered results.
        
        Returns:
            List of ClusterResult objects
        """
        # Reset cluster results
        self.cluster_results = []
        
        # Filter parsed content results to only include those within the attention bbox
        filtered_results = self._filter_parsed_content_results()
        
        if not filtered_results:
            logger.warning("No parsed content results within the worker attention bbox")
            return self.cluster_results
        
        # Step 1: Vertical clustering
        vert_clusters = self._cluster_vertically(filtered_results)
        
        # Step 2: Horizontal clustering within each vertical cluster
        for vert_id, vert_content in vert_clusters.items():
            # Cluster horizontally within this vertical cluster
            horiz_clusters = self._cluster_horizontally(vert_content)
            
            # Create cluster results for each horizontal cluster
            for horiz_id, horiz_content in horiz_clusters.items():
                # Create a unique cluster ID
                cluster_id = f"v{vert_id}_h{horiz_id}"
                
                # Create a cluster result
                cluster_result = ClusterResult(
                    cluster_result_id=cluster_id,
                    parsed_content_results=horiz_content
                )
                
                self.cluster_results.append(cluster_result)
        
        return self.cluster_results
    


def test_cluster_dbscan_worker():
    # get omniparser result from image path
    import os
    from omniparser.omni_helper import get_omniparser_inference_data_from_image_path
    # get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "cluster_test.png")
    omniparser_result = get_omniparser_inference_data_from_image_path(image_path)
    # create cluster preprocessor
    parsed_content_results = omniparser_result.parsed_content_list
    cluster_model_heirarchy = ClusterModelHeirarchy(os.path.join(current_dir, "sample_cluster_rules.json"))
    cluster_preprocessor = ClusterPreprocessor(parsed_content_results, 
                                               cluster_model_heirarchy, 
                                               omniparser_result)
    # create cluster worker
    cluster_worker = ClusterDBSCANWorker(cluster_preprocessor)
    # cluster
    cluster_results = cluster_worker.cluster()
    
    # print the cluster results
    for cluster_result in cluster_results:
        print(cluster_result)

if __name__ == "__main__":
    test_cluster_dbscan_worker()

