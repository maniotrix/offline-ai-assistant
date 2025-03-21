# type: ignore
from typing import Dict, List, Optional, AsyncIterator, Any, Union, Callable
import logging
import base64
from pathlib import Path
from base_client import BaseOllamaClient
import ollama_utils

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
        return ollama_utils.get_default_vlm_options()
    
    def _process_image(self, image: Union[str, bytes], should_crop_to_website_render_area: bool = False) -> str:
        """Process image to base64 format.
        
        Args:
            image (Union[str, bytes]): Image path or raw bytes
            should_crop_to_website_render_area (bool): Whether to crop the image to the website render area
            
        Returns:
            str: Base64 encoded image
        """
        return ollama_utils.process_image(image, should_crop_to_website_render_area=should_crop_to_website_render_area)
    
    def _process_images(self, images: List[Union[str, bytes]], should_crop_to_website_render_area: bool = False) -> List[str]:
        """Process multiple images to base64 format.
        
        Args:
            images (List[Union[str, bytes]]): List of image paths or raw bytes
            should_crop_to_website_render_area (bool): Whether to crop the image to the website render area
            
        Returns:
            List[str]: List of base64 encoded images
        """
        return [self._process_image(img, should_crop_to_website_render_area) for img in images]
        
    async def complete_with_vision(self, 
                                prompt: str, 
                                images: List[Union[str, bytes]],
                                system: Optional[str] = None,
                                template: Optional[str] = None,
                                tools: Optional[List[Dict[str, Any]]] = None,
                                options: Optional[Dict[str, Any]] = None,
                                keep_alive: Optional[str] = None,
                                should_crop_to_website_render_area: bool = False) -> Any:
        """Generate a response from the VLM using text and images.
        
        Args:
            prompt (str): The text prompt to send to the model
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            should_crop_to_website_render_area (bool, optional): Whether to crop images to website render area. Defaults to False.
        
        Returns:
            Any: The model's response
        """
        # Process images
        processed_images = self._process_images(images, should_crop_to_website_render_area)
        
        try:
            # Always use chat API with modern features
            messages = [{"role": "user", "content": prompt, "images": processed_images}]
            
            # If system prompt is provided, include it as first message with system role
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            logger.info(f"Using chat API with VLM model: {self.model_name}")
            if tools:
                logger.info(f"Including {len(tools)} tools in the request")
                
            # Create request parameters without system as a direct parameter
            request_params = {
                "model": self.model_name,
                "messages": messages,
                "tools": tools,
                "options": options,
                "keep_alive": keep_alive
            }
            
            # Add template if provided
            if template:
                request_params["template"] = template
                
            return await self.ollama_client.chat(**request_params)
        except Exception as e:
            logger.error(f"Error generating vision response: {e}")
            raise
            
    async def stream_complete_with_vision(self, 
                                       prompt: str, 
                                       images: List[Union[str, bytes]],
                                       system: Optional[str] = None,
                                       template: Optional[str] = None,
                                       tools: Optional[List[Dict[str, Any]]] = None,
                                       options: Optional[Dict[str, Any]] = None,
                                       keep_alive: Optional[str] = None,
                                       should_crop_to_website_render_area: bool = False) -> AsyncIterator[Any]:
        """Stream a response from the VLM using text and images.
        
        Args:
            prompt (str): The text prompt to send to the model
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            should_crop_to_website_render_area (bool, optional): Whether to crop images to website render area. Defaults to False.
            
        Yields:
            Any: Chunks of the model's response
        """
        # Process images
        processed_images = self._process_images(images, should_crop_to_website_render_area)
        
        try:
            # Always use chat API with modern features and streaming
            messages = [{"role": "user", "content": prompt, "images": processed_images}]
            
            # If system prompt is provided, include it as first message with system role
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            logger.info(f"Using streaming chat API with VLM model: {self.model_name}")
            if tools:
                logger.info(f"Including {len(tools)} tools in the streaming request")
                
            # Create request parameters without system as a direct parameter
            request_params = {
                "model": self.model_name,
                "messages": messages,
                "tools": tools,
                "options": options,
                "keep_alive": keep_alive,
                "stream": True
            }
            
            # Add template if provided
            if template:
                request_params["template"] = template
                
            async for chunk in await self.ollama_client.chat(**request_params):
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream vision generate: {e}")
            raise
            
    async def chat_with_vision(self, 
                            messages: List[Dict[str, Any]],
                            images: List[Union[str, bytes]], 
                            system: Optional[str] = None,
                            template: Optional[str] = None,
                            tools: Optional[List[Dict[str, Any]]] = None,
                            options: Optional[Dict[str, Any]] = None,
                            keep_alive: Optional[str] = None,
                            should_crop_to_website_render_area: bool = False) -> Any:
        """Chat with the VLM using a conversation history and images.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            should_crop_to_website_render_area (bool, optional): Whether to crop images to website render area. Defaults to False.
        
        Returns:
            Any: The model's response
        """
        # Process images
        processed_images = self._process_images(images, should_crop_to_website_render_area)
        
        # Modify messages to include images in the last user message
        updated_messages = messages.copy()
        for i in range(len(updated_messages) - 1, -1, -1):
            if updated_messages[i].get("role") == "user":
                updated_messages[i]["images"] = processed_images
                break
        
        # If system prompt is provided, include it as first message with system role
        if system:
            # Check if the first message is already a system message
            if updated_messages and updated_messages[0].get("role") == "system":
                # Replace existing system message
                updated_messages[0]["content"] = system
            else:
                # Add new system message at the beginning
                updated_messages = [{"role": "system", "content": system}] + updated_messages
                
        try:
            logger.info(f"Using chat API with {len(updated_messages)} messages")
            if tools:
                logger.info(f"Including {len(tools)} tools in the chat request")
                
            # Create request parameters without system as a direct parameter
            request_params = {
                "model": self.model_name,
                "messages": updated_messages,
                "tools": tools,
                "options": options,
                "keep_alive": keep_alive
            }
            
            # Add template if provided
            if template:
                request_params["template"] = template
                
            return await self.ollama_client.chat(**request_params)
        except Exception as e:
            logger.error(f"Error in chat with vision: {e}")
            raise
            
    async def stream_chat_with_vision(self, 
                                   messages: List[Dict[str, Any]], 
                                   images: List[Union[str, bytes]],
                                   system: Optional[str] = None,
                                   template: Optional[str] = None,
                                   tools: Optional[List[Dict[str, Any]]] = None,
                                   options: Optional[Dict[str, Any]] = None,
                                   keep_alive: Optional[str] = None,
                                   should_crop_to_website_render_area: bool = False) -> AsyncIterator[Any]:
        """Stream a chat response from the VLM with images.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            images (List[Union[str, bytes]]): Images as file paths, base64 strings, or bytes
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            should_crop_to_website_render_area (bool, optional): Whether to crop images to website render area. Defaults to False.
            
        Yields:
            Any: Chunks of the model's response
        """
        # Process images
        processed_images = self._process_images(images, should_crop_to_website_render_area)
        
        # Modify messages to include images in the last user message
        updated_messages = messages.copy()
        for i in range(len(updated_messages) - 1, -1, -1):
            if updated_messages[i].get("role") == "user":
                updated_messages[i]["images"] = processed_images
                break
        
        # If system prompt is provided, include it as first message with system role
        if system:
            # Check if the first message is already a system message
            if updated_messages and updated_messages[0].get("role") == "system":
                # Replace existing system message
                updated_messages[0]["content"] = system
            else:
                # Add new system message at the beginning
                updated_messages = [{"role": "system", "content": system}] + updated_messages
                
        try:
            logger.info(f"Using streaming chat API with {len(updated_messages)} messages")
            if tools:
                logger.info(f"Including {len(tools)} tools in the streaming chat request")
                
            # Create request parameters without system as a direct parameter
            request_params = {
                "model": self.model_name,
                "messages": updated_messages,
                "tools": tools,
                "options": options,
                "keep_alive": keep_alive,
                "stream": True
            }
            
            # Add template if provided
            if template:
                request_params["template"] = template
                
            async for chunk in await self.ollama_client.chat(**request_params):
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream vision chat: {e}")
            raise 