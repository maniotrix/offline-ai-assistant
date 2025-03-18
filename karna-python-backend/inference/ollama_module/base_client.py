import ollama
from typing import Dict, List, Optional, Union, AsyncIterator, Any
import logging
import uuid
import utils

# Setup logging
logger = logging.getLogger(__name__)

# Base async client from ollama
ollama_client = ollama.AsyncClient()

class BaseOllamaClient:
    """Base client for Ollama API interactions.
    
    This class provides common functionality for all model types,
    including basic operations.
    """
    
    def __init__(self, host: Optional[str] = None, timeout: int = 120):
        """Initialize the Ollama client.
        
        Args:
            host (str, optional): The host URL for the Ollama server. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 120.
        """
        if not host:
            host = utils.get_ollama_host()
            
        if host:
            self.ollama_client = ollama.AsyncClient(host=host)
        else:
            self.ollama_client = ollama_client
        self.timeout = timeout
    
    async def list_models(self) -> Any:
        """List all available models on the Ollama server."""
        try:
            return await self.ollama_client.list()
        except Exception as e:
            utils.handle_api_error(e, "listing models")
            raise
    
    async def get_model_info(self, model_name: str) -> Any:
        """Get information about a specific model.
        
        Args:
            model_name (str): The name of the model
        """
        try:
            return await self.ollama_client.show(model_name)
        except Exception as e:
            utils.handle_api_error(e, f"getting model info for {model_name}")
            raise
    
    async def check_model_status(self, model_name: str) -> bool:
        """Check if a model is available locally.
        
        Args:
            model_name (str): The name of the model to check
            
        Returns:
            bool: True if model is available, False otherwise
        """
        try:
            models = await self.list_models()
            for model in models.get("models", []):
                if model.get("name") == model_name:
                    return True
            return False
        except Exception as e:
            utils.handle_api_error(e, f"checking model status for {model_name}")
            return False
    
    async def health_check(self) -> bool:
        """Check if the Ollama server is up and running.
        
        Returns:
            bool: True if server is healthy, False otherwise
        """
        try:
            # Try to list models as a basic health check
            await self.list_models()
            return True
        except Exception as e:
            utils.handle_api_error(e, "health check")
            return False
            
    async def get_model_metrics(self, model_name: str) -> Dict[str, Any]:
        """Get usage metrics for a model.
        
        This is a custom implementation since Ollama API doesn't directly provide this.
        
        Args:
            model_name (str): The name of the model
            
        Returns:
            dict: Metrics information
        """
        try:
            # Get model info which includes some basic metrics
            model_info = await self.get_model_info(model_name)
            
            # Extract relevant metrics
            metrics = {
                "model_size": model_info.get("size", 0),
                "parameters": model_info.get("parameters", 0),
                "quantization_level": model_info.get("details", {}).get("quantization_level", "unknown"),
                "format": model_info.get("details", {}).get("format", "unknown")
            }
            
            return metrics
        except Exception as e:
            utils.handle_api_error(e, f"getting model metrics for {model_name}")
            raise
            
    async def create_session(self, model_name: str) -> str:
        """Create a new session ID for tracking conversation state.
        
        Args:
            model_name (str): The model to associate with this session
            
        Returns:
            str: A unique session ID
        """
        session_id = str(uuid.uuid4())
        logger.info(f"Created new session {session_id} for model {model_name}")
        return session_id