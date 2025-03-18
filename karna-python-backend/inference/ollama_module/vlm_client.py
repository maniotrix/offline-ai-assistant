from typing import Dict, List, Optional, AsyncIterator, Any, Union
import logging
import base64
from pathlib import Path
from base_client import BaseOllamaClient
import utils

logger = logging.getLogger(__name__)

class OllamaVLMClient(BaseOllamaClient):
    """Specialized client for vision language models via Ollama."""
    
    def __init__(self, model_name: str, host: Optional[str] = None, timeout: int = 120):
        """Initialize the VLM client.
        
        Args:
            model_name (str): The name of the VLM model to use
            host (str, optional): The host URL for the Ollama server. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 120.
        """
        super().__init__(host=host, timeout=timeout)
        self.model_name = model_name
        
    async def get_default_options(self) -> Dict[str, Any]:
        """Get default options optimized for VLMs.
        
        Returns:
            dict: Default VLM options
        """
        return utils.get_default_vlm_options()
    
    def _process_image(self, image: Union[str, bytes]) -> str:
        """Process image to base64 format.
        
        Args:
            image (Union[str, bytes]): Image path or raw bytes
            
        Returns:
            str: Base64 encoded image
        """
        return utils.process_image(image)
    
    def _process_images(self, images: List[Union[str, bytes]]) -> List[str]:
        """Process multiple images to base64 format.
        
        Args:
            images (List[Union[str, bytes]]): List of image paths or raw bytes
            
        Returns:
            List[str]: List of base64 encoded images
        """
        return utils.process_images(images)
        
    async def complete_with_vision(self, 
                                prompt: str, 
                                images: List[Union[str, bytes]],
                                system: Optional[str] = None,
                                template: Optional[str] = None,
                                options: Optional[Dict[str, Any]] = None,
                                keep_alive: Optional[str] = None) -> Any:
        """Generate a response from the VLM using text and images.
        
        Args:
            prompt (str): The text prompt to send to the model
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        # Process images
        processed_images = self._process_images(images)
        
        try:
            return await self.ollama_client.generate(
                model=self.model_name,
                prompt=prompt,
                system=system,
                template=template,
                images=processed_images,
                options=options,
                keep_alive=keep_alive
            ) # type: ignore
        except Exception as e:
            logger.error(f"Error generating vision response: {e}")
            raise
            
    async def stream_complete_with_vision(self, 
                                       prompt: str, 
                                       images: List[Union[str, bytes]],
                                       system: Optional[str] = None,
                                       template: Optional[str] = None,
                                       options: Optional[Dict[str, Any]] = None,
                                       keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a response from the VLM using text and images.
        
        Args:
            prompt (str): The text prompt to send to the model
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        # Process images
        processed_images = self._process_images(images)
        
        try:
            async for chunk in await self.ollama_client.generate(
                model=self.model_name,
                prompt=prompt,
                system=system,
                template=template,
                images=processed_images,
                options=options,
                keep_alive=keep_alive,
                stream=True
            ): # type: ignore
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream vision generate: {e}")
            raise
    
    async def chat_with_vision(self, 
                            messages: List[Dict[str, str]], 
                            images: List[Union[str, bytes]],
                            system: Optional[str] = None,
                            template: Optional[str] = None,
                            options: Optional[Dict[str, Any]] = None,
                            keep_alive: Optional[str] = None) -> Any:
        """Chat with the VLM using a conversation history and images.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        # Find the last user message and add the image to it
        processed_images = self._process_images(images)
        
        # Modify messages to include images in the last user message
        updated_messages = messages.copy()
        for i in range(len(updated_messages) - 1, -1, -1):
            if updated_messages[i].get("role") == "user":
                updated_messages[i]["images"] = processed_images
                break
                
        try:
            return await self.ollama_client.chat(
                model=self.model_name,
                messages=updated_messages,
                system=system,
                template=template,
                options=options,
                keep_alive=keep_alive
            ) # type: ignore
        except Exception as e:
            logger.error(f"Error in vision chat: {e}")
            raise
            
    async def stream_chat_with_vision(self, 
                                   messages: List[Dict[str, str]], 
                                   images: List[Union[str, bytes]],
                                   system: Optional[str] = None,
                                   template: Optional[str] = None,
                                   options: Optional[Dict[str, Any]] = None,
                                   keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a chat response from the VLM with images.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        # Find the last user message and add the image to it
        processed_images = self._process_images(images)
        
        # Modify messages to include images in the last user message
        updated_messages = messages.copy()
        for i in range(len(updated_messages) - 1, -1, -1):
            if updated_messages[i].get("role") == "user":
                updated_messages[i]["images"] = processed_images
                break
                
        try:
            async for chunk in await self.ollama_client.chat(
                model=self.model_name,
                messages=updated_messages,
                system=system,
                template=template,
                options=options,
                keep_alive=keep_alive,
                stream=True
            ): # type: ignore
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream vision chat: {e}")
            raise 