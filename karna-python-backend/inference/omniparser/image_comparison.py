import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from typing import Optional, Union, List, Tuple, Any, Callable, Dict, Literal

class ResNetImageEmbedder:
    """
    A class for generating embeddings for images using a pre-trained ResNet model.
    Specifically designed for comparing icons across different themes.
    """
    def __init__(
        self, 
        model_name: str = 'resnet18', 
        layer_name: str = 'avgpool',
        device: Optional[str] = None
    ):
        """
        Initialize the ResNetImageEmbedder.
        
        Args:
            model_name: Name of the ResNet model to use ('resnet18', 'resnet34', 'resnet50', etc.)
            layer_name: Name of the layer to extract features from
            device: Device to run inference on ('cuda', 'cpu'). If None, will use CUDA if available.
        """
        # Set device
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model
        if model_name == 'resnet18':
            self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            self.embedding_dim = 512
        elif model_name == 'resnet34':
            self.model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
            self.embedding_dim = 512
        elif model_name == 'resnet50':
            self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
            self.embedding_dim = 2048
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Save the model name and layer name for threshold selection
        self.model_name = model_name
        self.layer_name = layer_name
        
        # Create a hook to extract the features from the specified layer
        self.features = None
        self._register_hook()
        
        # Define the transformation pipeline
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _register_hook(self):
        """Register a forward hook to the target layer."""
        
        def hook_fn(module: nn.Module, input_: Any, output: Any):
            if isinstance(output, torch.Tensor):
                self.features = output.detach()
            else:
                # For some layers like avgpool, output can be a tuple
                self.features = output[0].detach()
        
        if self.layer_name == 'avgpool':
            # For avgpool, we can directly access it
            self.model.avgpool.register_forward_hook(hook_fn)
        else:
            # For other layers, we need to find them by name
            for name, module in self.model.named_modules():
                if name == self.layer_name:
                    module.register_forward_hook(hook_fn)
                    break
    
    def get_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Generate embedding for a single image.
        
        Args:
            image: PIL image to generate embedding for
            
        Returns:
            numpy.ndarray: Image embedding (feature vector)
        """
        # Ensure image is RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transformations
        img_tensor = self.transform(image)
        # Convert the transformed tensor to batch format
        img_tensor_batch = torch.unsqueeze(img_tensor, 0).to(self.device)
        
        # Forward pass through the model
        with torch.no_grad():
            _ = self.model(img_tensor_batch)
        
        # Get the features from the hook
        if self.features is not None:
            features = self.features.cpu().numpy()
            
            # Reshape the features to a flat vector
            embedding = features.reshape(-1)
            
            # Normalize the embedding to unit length
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding
        else:
            raise RuntimeError("Features were not captured by the hook during forward pass")
    
    def get_similarity(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Compute the cosine similarity between two images.
        
        Args:
            img1: First PIL image
            img2: Second PIL image
            
        Returns:
            float: Cosine similarity score (0-1 range, higher is more similar)
        """
        emb1 = self.get_embedding(img1)
        emb2 = self.get_embedding(img2)
        
        # Compute cosine similarity
        similarity = np.dot(emb1, emb2)
        
        return similarity
    
    def classify_similarity(self, score: float) -> Literal["identical", "similar", "related", "different"]:
        """
        Classify the similarity score based on recommended thresholds for the current model.
        
        Args:
            score: Similarity score from get_similarity() (0-1 range)
            
        Returns:
            str: Classification of the similarity ("identical", "similar", "related", or "different")
        """
        if self.model_name == 'resnet50' and self.layer_name == 'avgpool':
            # Thresholds for ResNet-50 with avgpool
            if score > 0.85:
                return "identical"
            elif score > 0.70:
                return "similar"
            elif score > 0.50:
                return "related"
            else:
                return "different"
        else:
            # Default thresholds for ResNet-18 with avgpool and other configurations
            if score > 0.80:
                return "identical"
            elif score > 0.65:
                return "similar"
            elif score > 0.45:
                return "related"
            else:
                return "different"
    
    def get_similarity_with_classification(self, img1: Image.Image, img2: Image.Image) -> Dict[str, Union[float, str]]:
        """
        Compute similarity between two images and return both the score and classification.
        
        Args:
            img1: First PIL image
            img2: Second PIL image
            
        Returns:
            dict: Dictionary with keys 'score' (float) and 'classification' (str)
        """
        score = self.get_similarity(img1, img2)
        classification = self.classify_similarity(score)
        
        return {
            'score': score,
            'classification': classification
        }
    
    def batch_get_embeddings(self, images: List[Image.Image]) -> np.ndarray:
        """
        Generate embeddings for a batch of images.
        
        Args:
            images: List of PIL images
            
        Returns:
            numpy.ndarray: Array of embeddings, shape (n_images, embedding_dim)
        """
        embeddings = []
        
        for image in images:
            embedding = self.get_embedding(image)
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def batch_compute_similarity_matrix(self, images: List[Image.Image]) -> np.ndarray:
        """
        Compute pairwise similarity matrix for a list of images.
        
        Args:
            images: List of PIL images
            
        Returns:
            numpy.ndarray: Similarity matrix, shape (n_images, n_images)
        """
        embeddings = self.batch_get_embeddings(images)
        
        # Compute pairwise cosine similarity matrix
        similarity_matrix = np.dot(embeddings, embeddings.T)
        
        return similarity_matrix
    
    def batch_classify_similarity_matrix(self, similarity_matrix: np.ndarray) -> np.ndarray:
        """
        Classify each value in a similarity matrix based on recommended thresholds.
        
        Args:
            similarity_matrix: Similarity matrix from batch_compute_similarity_matrix()
            
        Returns:
            numpy.ndarray: Matrix of classification labels (2D array of strings)
        """
        classification_matrix = np.empty_like(similarity_matrix, dtype=object)
        
        for i in range(similarity_matrix.shape[0]):
            for j in range(similarity_matrix.shape[1]):
                classification_matrix[i, j] = self.classify_similarity(similarity_matrix[i, j])
        
        return classification_matrix
