from typing import Dict, List, Optional, AsyncIterator, Any
import logging
from base_client import BaseOllamaClient
import utils

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
                    options: Optional[Dict[str, Any]] = None,
                    keep_alive: Optional[str] = None) -> Any:
        """Generate a completion from the LLM.
        
        Args:
            prompt (str): The prompt to send to the model
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            context (List[int], optional): Previous context for continuing generation. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        try:
            return await self.ollama_client.generate( # type: ignore
                model=self.model_name,
                prompt=prompt,
                system=system,
                template=template,
                context=context,
                options=options,
                keep_alive=keep_alive,
                stream=False
            )
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
            
    async def stream_complete(self, 
                           prompt: str, 
                           system: Optional[str] = None,
                           template: Optional[str] = None,
                           context: Optional[List[int]] = None,
                           options: Optional[Dict[str, Any]] = None,
                           keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a completion from the LLM.
        
        Args:
            prompt (str): The prompt to send to the model
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            context (List[int], optional): Previous context for continuing generation. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        try:
            async for chunk in await self.ollama_client.generate( 
                model=self.model_name,
                prompt=prompt,
                system=system,
                template=template,
                context=context,
                options=options,
                keep_alive=keep_alive,
                stream=True
            ): # type: ignore
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream generate: {e}")
            raise
            
    async def chat(self, 
                 messages: List[Dict[str, str]], 
                 system: Optional[str] = None,
                 template: Optional[str] = None,
                 options: Optional[Dict[str, Any]] = None,
                 keep_alive: Optional[str] = None) -> Any:
        """Chat with the LLM using a conversation history.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
        
        Returns:
            Any: The model's response
        """
        try:
            return await self.ollama_client.chat( # type: ignore
                model=self.model_name,
                messages=messages,
                system=system,
                template=template,
                options=options,
                keep_alive=keep_alive,
                stream=False
            )
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise
            
    async def stream_chat(self, 
                        messages: List[Dict[str, str]], 
                        system: Optional[str] = None,
                        template: Optional[str] = None,
                        options: Optional[Dict[str, Any]] = None,
                        keep_alive: Optional[str] = None) -> AsyncIterator[Any]:
        """Stream a chat response from the LLM.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            system (str, optional): System prompt to use. Defaults to None.
            template (str, optional): Custom prompt template. Defaults to None.
            options (dict, optional): Additional model parameters. Defaults to None.
            keep_alive (str, optional): Duration to keep the model loaded (e.g., "5m", "1h"). Defaults to None.
            
        Yields:
            Any: Chunks of the model's response
        """
        try:
            async for chunk in await self.ollama_client.chat(
                model=self.model_name,
                messages=messages,
                system=system,
                template=template,
                options=options,
                keep_alive=keep_alive,
                stream=True
            ): # type: ignore
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")
            raise 