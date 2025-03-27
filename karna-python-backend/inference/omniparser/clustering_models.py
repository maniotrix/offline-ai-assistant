from dataclasses import dataclass
from typing import List
import json
@dataclass
class CropArea:
    """
    This class represents a crop area.
    """
    x: int
    y: int
    width: int
    height: int
    

@dataclass
class BaseCluster:
    """
    This class represents a base cluster.
    """
    cluster_id: str
    cluster_name: str
    cluster_layout: str
    # List of child clusters that belong to this cluster
    # The forward reference "BaseCluster" allows recursive cluster definitions
    children: List["BaseCluster"]
    visibility_type: str
    
@dataclass
class RootCluster(BaseCluster):
    """
    This class represents a root cluster.
    """
    root_crop_area: CropArea
    

class ClusterModelHeirarchy:
    """
    This class represents a cluster hierarchy.
    {
    "cluster_rules": [
        {
            "cluster_id": "1",
            "cluster_name": "App Root",
            "root_crop_area": {
                "x": 0,
                "y": 0,
                "width": 1920,
                "height": 1080
            },
            "visibility_type": "persistent",
            "children": [
                {
                    "cluster_id": "1.1",
                    "cluster_name": "Header",
                    "cluster_layout": "horizontal",
                    "visibility_type": "persistent",
                    "children": [
                        {
                            "cluster_id": "1.1.1",
                            "cluster_name": "Left Sidebar Controls Container",
                            "cluster_layout": "horizontal",
                            "visibility_type": "persistent",
                            "children": []
                        },
                        {
                            "cluster_id": "1.1.2",
                            "cluster_name": "Model Selection Container",
                            "cluster_layout": "vertical",
                            "visibility_type": "persistent",
                            "children": [
                                {
                                    "cluster_id": "1.1.2.1",
                                    "cluster_name": "Model Selection Menu Container",
                                    "cluster_layout": "vertical",
                                    "visibility_type": "dynamic",
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "cluster_id": "1.2",
                    "cluster_name": "Main Area",
                    "cluster_layout": "vertical",
                    "visibility_type": "persistent",
                    "children": [
                        {
                            "cluster_id": "1.2.1",
                            "cluster_name": "Chat List Container",
                            "cluster_layout": "vertical",
                            "visibility_type": "persistent",
                            "children": [
                                {
                                    "cluster_id": "1.2.1.1",
                                    "cluster_name": "User Assistant Container",
                                    "cluster_layout": "vertical",
                                    "visibility_type": "dynamic",
                                    "children": [
                                        {
                                            "cluster_id": "1.2.1.1.1",
                                            "cluster_name": "User Container",
                                            "cluster_layout": "vertical",
                                            "visibility_type": "persistent",
                                            "children": []
                                        },
                                        {
                                            "cluster_id": "1.2.1.1.2",
                                            "cluster_name": "Assistant Container",
                                            "cluster_layout": "vertical",
                                            "visibility_type": "persistent",
                                            "children": [
                                                {
                                                    "cluster_id": "1.2.1.1.2.1",
                                                    "cluster_name": "Assistant Controls Container",
                                                    "cluster_layout": "horizontal",
                                                    "visibility_type": "dynamic",
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "cluster_id": "1.2.2",
                            "cluster_name": "Chat Controls Container",
                            "cluster_layout": "vertical",
                            "visibility_type": "persistent",
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
    }
    """
    
    # store a root cluster with all children clusters
    # loads root cluster and nested children clusters from json file
    root_cluster: RootCluster

    def __init__(self, json_file_path: str):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        # get the root cluster from the data
        cluster_rules = data['cluster_rules']
        root_cluster_data = cluster_rules[0]
        
        # Process root crop area
        crop_area_data = root_cluster_data.pop('root_crop_area')
        root_crop_area = CropArea(**crop_area_data)
        
        # Ensure root cluster has a layout property (default to 'container' if not specified)
        if 'cluster_layout' not in root_cluster_data:
            root_cluster_data['cluster_layout'] = 'container'
        
        # Process children recursively
        children_data = root_cluster_data.pop('children', [])
        children = self._create_children_clusters(children_data)
        
        # Create the root cluster with processed data
        self.root_cluster = RootCluster(
            **root_cluster_data,
            children=children,
            root_crop_area=root_crop_area
        )
    
    def _create_children_clusters(self, children_data: List[dict]) -> List[BaseCluster]:
        """
        Recursively create child clusters from nested dictionary data.
        
        Args:
            children_data: List of dictionaries containing child cluster data
            
        Returns:
            List of BaseCluster objects
        """
        children = []
        for child_data in children_data:
            # Extract nested children data before creating the cluster
            nested_children_data = child_data.pop('children', [])
            
            # Recursively process nested children
            nested_children = self._create_children_clusters(nested_children_data)
            
            # Create the child cluster and add it to the list
            child_cluster = BaseCluster(
                **child_data,
                children=nested_children
            )
            children.append(child_cluster)
            
            # Put 'children' back in the dictionary for completeness
            child_data['children'] = nested_children_data
            
        return children

    def to_dict(self) -> dict:
        """
        Convert the cluster hierarchy back to a dictionary representation.
        
        Returns:
            Dictionary representation of the cluster hierarchy
        """
        return {
            "cluster_rules": [
                self._cluster_to_dict(self.root_cluster)
            ]
        }
    
    def _cluster_to_dict(self, cluster: BaseCluster) -> dict:
        """
        Recursively convert a cluster and its children to dictionary representation.
        
        Args:
            cluster: The cluster to convert
            
        Returns:
            Dictionary representation of the cluster
        """
        # Create a base dictionary with all attributes
        cluster_dict = {
            "cluster_id": cluster.cluster_id,
            "cluster_name": cluster.cluster_name,
            "cluster_layout": cluster.cluster_layout,
            "visibility_type": cluster.visibility_type,
            "children": []  # Initialize as an empty list
        }
        
        # Process children recursively
        children_list = []
        for child in cluster.children:
            child_dict = self._cluster_to_dict(child)
            children_list.append(child_dict)
        
        # Assign the complete children list to the dictionary
        cluster_dict["children"] = children_list
        
        # Add root_crop_area if this is a RootCluster
        if isinstance(cluster, RootCluster):
            cluster_dict["root_crop_area"] = {
                "x": cluster.root_crop_area.x,
                "y": cluster.root_crop_area.y,
                "width": cluster.root_crop_area.width,
                "height": cluster.root_crop_area.height
            }
            
        return cluster_dict
    

if __name__ == "__main__":
    import os
    json_dir = os.path.dirname(os.path.abspath(__file__))
    cluster_model_heirarchy = ClusterModelHeirarchy(os.path.join(json_dir, "sample_cluster_rules.json"))
    print(f"Root Cluster Model Object: \n{cluster_model_heirarchy.root_cluster}")
    print("-"*100)
    # change Root cluster name
    cluster_model_heirarchy.root_cluster.cluster_name = "Root Cluster"
    cluster_model_heirarchy_dict = cluster_model_heirarchy.to_dict()
    # pretty print the dictionary
    print("Root Cluster Model Dictionary:")
    print(json.dumps(cluster_model_heirarchy_dict, indent=4))

