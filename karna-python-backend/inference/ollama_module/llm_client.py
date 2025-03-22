# type: ignore
from typing import Dict, List, Optional, AsyncIterator, Any, Union
import logging
from inference.ollama_module.base_client import BaseOllamaClient
import inference.ollama_module.ollama_utils as utils

logger = logging.getLogger(__name__)

class OllamaLLMClient(BaseOllamaClient):
    """Specialized client for text-only language models via Ollama."""
    
    def __init__(self, model_name: str, host: Optional[str] = None, timeout: int = 120):
        """Initialize the LLM client.
        
        Args:
            model_name (str): The name of the LLM model to use
            host (str, optional): The host URL for the Ollama server. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 120.
        """
        super().__init__(host=host, timeout=timeout)
        self.model_name = model_name
        
    async def get_default_options(self) -> Dict[str, Any]:
        """Get default options optimized for LLMs.
        
        Returns:
            dict: Default LLM options
        """
        return utils.get_default_llm_options()
        
    async def complete(self, 
                    prompt: str, 
                    system: Optional[str] = None,
                    template: Optional[str] = None,
                    context: Optional[List[int]] = None,
                    tools: Optional[List[Dict[str, Any]]] = None,
                    options: Optional[Dict[str, Any]] = None,
                    keep_alive: Optional[str] = None) -> Any:
        """Generate a completion from the LLM.
        
        Args:
            prompt (str): The prompt to send to the model
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            context (List[int], optional): Not used when using chat API, kept for compatibility. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        try:
            # Convert single prompt to messages format
            messages = [{"role": "user", "content": prompt}]
            
            # If system prompt is provided, include it as first message with system role
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            logger.info(f"Using chat API with LLM model: {self.model_name}")
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
            logger.error(f"Error generating response: {e}")
            raise
            
    async def stream_complete(self, 
                           prompt: str, 
                           system: Optional[str] = None,
                           template: Optional[str] = None,
                           context: Optional[List[int]] = None,
                           tools: Optional[List[Dict[str, Any]]] = None,
                           options: Optional[Dict[str, Any]] = None,
                           keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a completion from the LLM.
        
        Args:
            prompt (str): The prompt to send to the model
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            context (List[int], optional): Not used when using chat API, kept for compatibility. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        try:
            # Convert single prompt to messages format
            messages = [{"role": "user", "content": prompt}]
            
            # If system prompt is provided, include it as first message with system role
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            logger.info(f"Using streaming chat API with LLM model: {self.model_name}")
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
                
            # Stream the response
            async for chunk in await self.ollama_client.chat(**request_params):
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream generate: {e}")
            raise
            
    async def chat(self, 
                 messages: List[Dict[str, Any]], 
                 system: Optional[str] = None,
                 template: Optional[str] = None,
                 tools: Optional[List[Dict[str, Any]]] = None,
                 options: Optional[Dict[str, Any]] = None,
                 keep_alive: Optional[str] = None) -> Any:
        """Chat with the LLM using a conversation history.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        try:
            # If system prompt is provided, include it as first message with system role
            if system:
                # Check if the first message is already a system message
                if messages and messages[0].get("role") == "system":
                    # Replace existing system message
                    updated_messages = messages.copy()
                    updated_messages[0]["content"] = system
                else:
                    # Add new system message at the beginning
                    updated_messages = [{"role": "system", "content": system}] + messages
            else:
                updated_messages = messages
                
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
            logger.error(f"Error in chat: {e}")
            raise
            
    async def stream_chat(self, 
                        messages: List[Dict[str, Any]], 
                        system: Optional[str] = None,
                        template: Optional[str] = None,
                        tools: Optional[List[Dict[str, Any]]] = None,
                        options: Optional[Dict[str, Any]] = None,
                        keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a chat response from the LLM.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            tools (List[Dict[str, Any]], optional): List of tool definitions. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        try:
            # If system prompt is provided, include it as first message with system role
            if system:
                # Check if the first message is already a system message
                if messages and messages[0].get("role") == "system":
                    # Replace existing system message
                    updated_messages = messages.copy()
                    updated_messages[0]["content"] = system
                else:
                    # Add new system message at the beginning
                    updated_messages = [{"role": "system", "content": system}] + messages
            else:
                updated_messages = messages
                
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
            logger.error(f"Error in stream chat: {e}")
            raise 