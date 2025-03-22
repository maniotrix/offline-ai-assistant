from typing import Dict, List, Optional, Any, Union
import logging
import numpy as np
from inference.ollama_module.base_client import BaseOllamaClient
import inference.ollama_module.ollama_utils as ollama_utils

logger = logging.getLogger(__name__)

class OllamaEmbeddingClient(BaseOllamaClient):
    """Specialized client for generating embeddings via Ollama."""
    
    def __init__(self, model_name: str, host: Optional[str] = None, timeout: int = 120):
        """Initialize the embedding client.
        
        Args:
            model_name (str): The name of the embedding model to use
            host (str, optional): The host URL for the Ollama server. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 120.
        """
        super().__init__(host=host, timeout=timeout)
        self.model_name = model_name
        
    async def get_default_options(self) -> Dict[str, Any]:
        """Get default options optimized for embedding models.
        
        Returns:
            dict: Default embedding options
        """
        return ollama_utils.get_default_embedding_options()
        
    async def get_embeddings(self, 
                           text: str, 
                           options: Optional[Dict[str, Any]] = None,
                           keep_alive: Optional[str] = None) -> Any:
        """Generate embeddings from text.
        
        Args:
            text (str): The text to embed
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Returns:
            Any: The embedding response containing the vector
        """
        try:
            return await self.ollama_client.embeddings(
                model=self.model_name,
                prompt=text,
                options=options,
                keep_alive=keep_alive
            ) # type: ignore
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
            
    async def get_embeddings_batch(self, 
                                 texts: List[str], 
                                 options: Optional[Dict[str, Any]] = None,
                                 keep_alive: Optional[str] = None) -> List[Any]:
        """Generate embeddings for multiple texts.
        
        Args:
            texts (List[str]): The list of texts to embed
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Returns:
            List[Any]: List of embedding responses
        """
        results = []
        for text in texts:
            result = await self.get_embeddings(text, options, keep_alive)
            results.append(result)
        return results
        
    async def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two text embeddings.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Cosine similarity (0-1, where 1 is most similar)
        """
        try:
            # Get embeddings
            embedding1 = await self.get_embeddings(text1)
            embedding2 = await self.get_embeddings(text2)
            
            # Extract vectors
            vector1 = np.array(embedding1.get("embedding", []))
            vector2 = np.array(embedding2.get("embedding", []))
            
            # Calculate cosine similarity
            dot_product = np.dot(vector1, vector2)
            norm1 = np.linalg.norm(vector1)
            norm2 = np.linalg.norm(vector2)
            
            # Avoid division by zero
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            raise
            
    async def find_most_similar(self, query: str, candidates: List[str]) -> Dict[str, Union[str, float, int]]:
        """Find the most similar text from a list of candidates.
        
        Args:
            query (str): The query text
            candidates (List[str]): List of candidate texts to compare against
            
        Returns:
            Dict[str, Union[str, float, int]]: Dictionary with the most similar text and its score
        """
        try:
            # Get query embedding
            query_embedding = await self.get_embeddings(query)
            query_vector = np.array(query_embedding.get("embedding", []))
            
            # Get embeddings for all candidates
            candidate_embeddings = await self.get_embeddings_batch(candidates)
            
            max_similarity = -1
            most_similar_text = ""
            most_similar_index = -1
            
            # Find the most similar
            for i, emb in enumerate(candidate_embeddings):
                candidate_vector = np.array(emb.get("embedding", []))
                
                # Calculate cosine similarity
                dot_product = np.dot(query_vector, candidate_vector)
                norm1 = np.linalg.norm(query_vector)
                norm2 = np.linalg.norm(candidate_vector)
                
                # Avoid division by zero
                if norm1 == 0 or norm2 == 0:
                    similarity = 0.0
                else:
                    similarity = dot_product / (norm1 * norm2)
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_text = candidates[i]
                    most_similar_index = i
            
            return {
                "text": most_similar_text,
                "similarity": float(max_similarity),
                "index": most_similar_index
            }
        except Exception as e:
            logger.error(f"Error finding most similar text: {e}")
            raise 