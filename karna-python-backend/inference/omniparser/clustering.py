from typing import List, Dict, Any
from dataclasses import dataclass
from omniparser.omni_helper import ParsedContentResult, OmniparserResult
from omniparser.clustering_models import ClusterModelHeirarchy, get_crop_area_from_bbox_type
from logging import getLogger

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

    def cluster(self) -> List[ClusterResult]:
        raise NotImplementedError("This method should be implemented by the subclass")
        return self.cluster_results

