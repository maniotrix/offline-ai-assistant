# type: ignore
import asyncio
import json
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import os

# Use proper relative imports
from llm_client import OllamaLLMClient
from vlm_client import OllamaVLMClient
from services.screen_capture_service import ScreenshotEvent

async def async_llm_generate(prompt: str, model: str, stream: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Generate a text response from Ollama using the specified LLM model.
    
    Args:
        prompt: The text prompt to send to the model
        model: The name of the LLM model to use (e.g. "llama2", "smollm2")
        stream: Whether to stream the response (default: False)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    # Initialize the client
    client = OllamaLLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system')
    template = kwargs.get('template')
    context = kwargs.get('context')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')  # Extract tools parameter
    
    # If streaming is requested, collect all chunks into a single response
    if stream:
        full_response = {"response": ""}
        async for chunk in client.stream_complete(
            prompt=prompt,
            system=system,
            template=template,
            context=context,
            tools=tools,  # Pass tools parameter
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                full_response["response"] += chunk["response"]
            elif "message" in chunk and "content" in chunk["message"]:
                full_response["response"] += chunk["message"]["content"]
            
            # Include tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                if "tool_calls" not in full_response:
                    full_response["tool_calls"] = []
                
                for tool_call in chunk["message"]["tool_calls"]:
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in full_response.get("tool_calls", [])]
                    if tool_call_id not in existing_ids:
                        full_response.setdefault("tool_calls", []).append(tool_call)
                
        return full_response
    else:
        # Get a complete response at once
        response = await client.complete(
            prompt=prompt,
            system=system,
            template=template,
            context=context,
            tools=tools,  # Pass tools parameter
            options=options,
            keep_alive=keep_alive
        )
        
        # Process the response to ensure consistent format
        if "message" in response and "content" in response["message"]:
            response["response"] = response["message"]["content"]
            
        return response

def llm_generate(prompt: str, model: str, stream: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_llm_generate.
    """
    # Only use asyncio.run at the top level, not inside nested functions
    return asyncio.run(async_llm_generate(prompt, model, stream, **kwargs))

async def async_vlm_generate(prompt: str, image_path: str, model: str, stream: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Generate a response from Ollama using a vision language model (VLM).
    
    Args:
        prompt: The text prompt to send to the model
        image_path: Path to the image file to analyze
        model: The name of the VLM model to use (e.g. "llava")
        stream: Whether to stream the response (default: False)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system')
    template = kwargs.get('template')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')  # Extract tools parameter
    
    # Prepare the image as a list (the client expects a list of images)
    images = [image_path]
    
    # If streaming is requested, collect all chunks into a single response
    if stream:
        full_response = {"response": ""}
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,  # Pass tools parameter
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                full_response["response"] += chunk["response"]
            elif "message" in chunk and "content" in chunk["message"]:
                full_response["response"] += chunk["message"]["content"]
                
            # Handle tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                if "tool_calls" not in full_response:
                    full_response["tool_calls"] = []
                
                for tool_call in chunk["message"]["tool_calls"]:
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in full_response.get("tool_calls", [])]
                    if tool_call_id not in existing_ids:
                        full_response.setdefault("tool_calls", []).append(tool_call)
                
        return full_response
    else:
        # Get a complete response at once
        response = await client.complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,  # Pass tools parameter
            options=options,
            keep_alive=keep_alive
        )
        
        # Process the response to ensure consistent format
        if "message" in response and "content" in response["message"]:
            response["response"] = response["message"]["content"]
            
        return response

def vlm_generate(prompt: str, image_path: str, model: str, stream: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_vlm_generate.
    """
    # Only use asyncio.run at the top level, not inside nested functions
    return asyncio.run(async_vlm_generate(prompt, image_path, model, stream, **kwargs))

async def async_stream_llm_generate(
    prompt: str, 
    model: str, 
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None, 
    **kwargs
) -> None:
    """
    Generate a text response from Ollama using the specified LLM model and stream it in real-time.
    
    Args:
        prompt: The text prompt to send to the model
        model: The name of the LLM model to use (e.g. "llama2", "smollm2")
        callback: Optional callback function to process content and tool calls
        **kwargs: Additional parameters to pass to the Ollama API
    """
    # Initialize the client
    client = OllamaLLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system')
    template = kwargs.get('template')
    context = kwargs.get('context')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')  # Extract tools parameter
    
    print("\nStreaming response in real-time:")
    print("-" * 50)
    if system:
        print(f"Using system prompt: {system[:50]}..." if len(system) > 50 else system)
    if tools:
        print(f"Using {len(tools)} tools")
    
    full_text = ""
    collected_tool_calls = []
    
    try:
        async for chunk in client.stream_complete(
            prompt=prompt,
            system=system,
            template=template,
            context=context,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Debug chunk structure
            # print(f"Chunk: {chunk}")
            
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                chunk_text = chunk["response"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            elif "message" in chunk and "content" in chunk["message"]:
                chunk_text = chunk["message"]["content"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            
            # Handle tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                tool_calls = chunk["message"]["tool_calls"]
                
                for tool_call in tool_calls:
                    # Check if we've already processed this tool call
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                    
                    if tool_call_id not in existing_ids:
                        collected_tool_calls.append(tool_call)
                        function_info = tool_call.get("function", {})
                        function_name = function_info.get("name", "unknown")
                        function_args = function_info.get("arguments", "{}")
                        
                        # Pretty-print the tool call
                        print(f"\n\nTool Call: {function_name}")
                        try:
                            # Try to parse and pretty-print JSON arguments
                            args_obj = json.loads(function_args)
                            print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                        except json.JSONDecodeError:
                            # If not valid JSON, print as is
                            print(f"Arguments: {function_args}")
        
        # If there's a callback, call it with the content and tool calls
        if callback and (full_text or collected_tool_calls):
            callback(full_text, collected_tool_calls)
        
        print("\n" + "-" * 50)
        if collected_tool_calls:
            print(f"Streaming complete with {len(collected_tool_calls)} tool calls!")
        else:
            print("Streaming complete!")
    except Exception as e:
        print(f"\nError during streaming: {str(e)}")
        raise

def stream_llm_generate(
    prompt: str, 
    model: str, 
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None, 
    **kwargs
) -> None:
    """
    Synchronous wrapper for async_stream_llm_generate.
    """
    # Only use asyncio.run at the top level, not inside nested functions
    asyncio.run(async_stream_llm_generate(prompt, model, callback, **kwargs))

async def async_stream_vlm_generate(
    prompt: str, 
    image_path: str, 
    model: str, 
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    **kwargs
) -> None:
    """
    Generate a response from a VLM using text and image and stream it in real-time.
    
    Args:
        prompt: The text prompt to send to the model
        image_path: Path to the image file to analyze
        model: The name of the VLM model to use (e.g. "llava")
        callback: Optional callback function to process content and tool calls
        **kwargs: Additional parameters to pass to the Ollama API
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system')
    template = kwargs.get('template')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')  # Extract tools parameter
    
    # Prepare the image as a list (the client expects a list of images)
    images = [image_path]
    
    print("\nStreaming VLM response in real-time:")
    print("-" * 50)
    if system:
        print(f"Using system prompt: {system[:50]}..." if len(system) > 50 else system)
    if tools:
        print(f"Using {len(tools)} tools")
    
    full_text = ""
    collected_tool_calls = []
    
    try:
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                chunk_text = chunk["response"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            elif "message" in chunk and "content" in chunk["message"]:
                chunk_text = chunk["message"]["content"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            
            # Handle tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                tool_calls = chunk["message"]["tool_calls"]
                
                for tool_call in tool_calls:
                    # Check if we've already processed this tool call
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                    
                    if tool_call_id not in existing_ids:
                        collected_tool_calls.append(tool_call)
                        function_info = tool_call.get("function", {})
                        function_name = function_info.get("name", "unknown")
                        function_args = function_info.get("arguments", "{}")
                        
                        # Pretty-print the tool call
                        print(f"\n\nTool Call: {function_name}")
                        try:
                            # Try to parse and pretty-print JSON arguments
                            args_obj = json.loads(function_args)
                            print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                        except json.JSONDecodeError:
                            # If not valid JSON, print as is
                            print(f"Arguments: {function_args}")
        
        # If there's a callback, call it with the content and tool calls
        if callback and (full_text or collected_tool_calls):
            callback(full_text, collected_tool_calls)
        
        print("\n" + "-" * 50)
        if collected_tool_calls:
            print(f"VLM streaming complete with {len(collected_tool_calls)} tool calls!")
        else:
            print("VLM streaming complete!")
    except Exception as e:
        print(f"\nError during VLM streaming: {str(e)}")
        raise

def stream_vlm_generate(
    prompt: str, 
    image_path: str, 
    model: str, 
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    **kwargs
) -> None:
    """
    Synchronous wrapper for async_stream_vlm_generate.
    """
    # Only use asyncio.run at the top level, not inside nested functions
    asyncio.run(async_stream_vlm_generate(prompt, image_path, model, callback, **kwargs))

# New functions for VLM with tool calling capabilities

async def async_vlm_generate_with_tools(
    prompt: str, 
    image_path: str, 
    model: str, 
    tools: List[Dict[str, Any]],
    stream: bool = False, 
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a response from Ollama using a vision language model (VLM) with tool calling support.
    
    Args:
        prompt: The text prompt to send to the model
        image_path: Path to the image file to analyze
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        tools: List of tool definitions to provide to the model
        stream: Whether to stream the response (default: False)
        system: System prompt to use (default: None)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (e.g., "5m", "1h") (default: None)
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Prepare the image as a list (the client expects a list of images)
    images = [image_path]
    
    # If streaming is requested, collect all chunks into a single response
    if stream:
        full_response = {"response": "", "tool_calls": []}
        
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle direct response format
            if "response" in chunk:
                full_response["response"] += chunk["response"]
            
            # Handle message format
            elif "message" in chunk:
                message = chunk["message"]
                
                # Handle text response
                if "content" in message:
                    full_response["response"] += message["content"] or ""
                
                # Handle tool calls
                if "tool_calls" in message and message["tool_calls"]:
                    # For streaming, we collect tool calls as they come in
                    for tool_call in message["tool_calls"]:
                        # Check if this tool call is already in our list
                        tool_call_id = tool_call.get("id", "")
                        existing_ids = [tc.get("id", "") for tc in full_response["tool_calls"]]
                        if tool_call_id not in existing_ids:
                            full_response["tool_calls"].append(tool_call)
        
        return full_response
    else:
        # Get a complete response at once
        response = await client.complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        )
        
        # Process the response to ensure consistent format
        if "message" in response and "content" in response["message"]:
            response["response"] = response["message"]["content"]
        
        return response

def vlm_generate_with_tools(
    prompt: str, 
    image_path: str, 
    model: str, 
    tools: List[Dict[str, Any]],
    stream: bool = False, 
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_vlm_generate_with_tools.
    """
    return asyncio.run(async_vlm_generate_with_tools(
        prompt=prompt, 
        image_path=image_path, 
        model=model, 
        tools=tools,
        stream=stream, 
        system=system,
        template=template,
        options=options,
        keep_alive=keep_alive
    ))

async def async_stream_vlm_with_tools(
    prompt: str, 
    image_path: str, 
    model: str, 
    tools: List[Dict[str, Any]],
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> None:
    """
    Generate a response from a VLM using text and image with tools and stream it in real-time.
    
    Args:
        prompt: The text prompt to send to the model
        image_path: Path to the image file to analyze
        model: The name of the VLM model to use (e.g. "llava")
        tools: List of tool definitions to provide to the model
        callback: Optional callback function to process content and tool calls
        system: System prompt to use (default: None)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Prepare the image as a list (the client expects a list of images)
    images = [image_path]
    
    print("\nStreaming VLM response with tools in real-time:")
    print("-" * 50)
    print(f"Model: {model}")
    if system:
        print(f"Using system prompt: {system[:50]}..." if len(system) > 50 else system)
    print(f"Tools provided: {len(tools)}")
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    full_text = ""
    collected_tool_calls = []
    
    try:
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=images,
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle direct response format
            if "response" in chunk:
                content = chunk["response"]
                full_text += content
                print(content, end="", flush=True)
                
            # Handle message format    
            elif "message" in chunk:
                message = chunk["message"]
                
                # Handle text response
                if "content" in message and message["content"]:
                    content = message["content"]
                    full_text += content
                    print(content, end="", flush=True)
                
                # Handle tool calls
                if "tool_calls" in message and message["tool_calls"]:
                    tool_calls = message["tool_calls"]
                    
                    for tool_call in tool_calls:
                        # Check if tool call already processed
                        tool_call_id = tool_call.get("id", "")
                        existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                        
                        if tool_call_id not in existing_ids:
                            collected_tool_calls.append(tool_call)
                            function_info = tool_call.get("function", {})
                            function_name = function_info.get("name", "unknown")
                            function_args = function_info.get("arguments", "{}")
                            
                            # Pretty-print the tool call
                            print(f"\n\nTool Call: {function_name}")
                            try:
                                # Try to parse and pretty-print JSON arguments
                                args_obj = json.loads(function_args)
                                print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                            except json.JSONDecodeError:
                                # If not valid JSON, print as is
                                print(f"Arguments: {function_args}")
            
            # If there's a callback, call it with updated content and tool calls
            if callback:
                callback(full_text, collected_tool_calls)
        
        print("\n" + "-" * 50)
        if collected_tool_calls:
            print(f"VLM streaming complete with {len(collected_tool_calls)} tool calls!")
        else:
            print("VLM streaming complete!")
    except Exception as e:
        print(f"\nError during VLM streaming with tools: {str(e)}")
        raise

def stream_vlm_with_tools(
    prompt: str, 
    image_path: str, 
    model: str, 
    tools: List[Dict[str, Any]],
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> None:
    """
    Synchronous wrapper for async_stream_vlm_with_tools.
    """
    asyncio.run(async_stream_vlm_with_tools(
        prompt=prompt, 
        image_path=image_path, 
        model=model, 
        tools=tools,
        callback=callback,
        system=system,
        template=template,
        options=options,
        keep_alive=keep_alive
    ))

async def async_vlm_chat_with_tool_response(
    prompt: str,
    image_path: str,
    model: str,
    tool_responses: List[Dict[str, Any]],
    tools: List[Dict[str, Any]],
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a two-turn conversation where the model first generates tool calls and then
    processes the results of those tool calls with the VLM.
    
    Args:
        prompt: The text prompt to send to the model
        image_path: Path to the image file to analyze
        model: The name of the VLM model to use (e.g. "llava")
        tool_responses: List of dictionaries with tool responses 
                       (must have 'tool_call_id' and 'content' keys)
        tools: List of tool definitions to provide to the model
        system: System prompt to use (default: None)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        
    Returns:
        The final response from the Ollama API as a dictionary
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Prepare the image as a list
    images = [image_path]
    
    # Step 1: Get the assistant's response with potential tool calls
    first_response = await client.complete_with_vision(
        prompt=prompt,
        images=images,
        system=system,
        template=template,
        tools=tools,
        options=options,
        keep_alive=keep_alive
    )
    
    # Extract the message from the response
    if "message" not in first_response:
        raise ValueError("Invalid response format: 'message' key not found")
    
    # Build conversation history
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    # Add the assistant's response to the conversation
    assistant_message = first_response["message"]
    messages.append({"role": "assistant", **assistant_message})
    
    # Add tool responses to the conversation
    for tool_response in tool_responses:
        if "tool_call_id" not in tool_response or "content" not in tool_response:
            raise ValueError("Tool responses must have 'tool_call_id' and 'content' keys")
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_response["tool_call_id"],
            "content": tool_response["content"]
        })
    
    # Step 2: Get the final response incorporating tool results
    final_response = await client.chat_with_vision(
        messages=messages,
        images=images,  # We need to provide images again for context
        system=system,
        template=template,
        tools=tools,  # Keep tools available in case more tool calls are needed
        options=options,
        keep_alive=keep_alive
    )
    
    # Process the response to ensure consistent format
    if "message" in final_response and "content" in final_response["message"]:
        final_response["response"] = final_response["message"]["content"]
    
    return final_response

def vlm_chat_with_tool_response(
    prompt: str,
    image_path: str,
    model: str,
    tool_responses: List[Dict[str, Any]],
    tools: List[Dict[str, Any]],
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_vlm_chat_with_tool_response.
    """
    return asyncio.run(async_vlm_chat_with_tool_response(
        prompt=prompt,
        image_path=image_path,
        model=model,
        tool_responses=tool_responses,
        tools=tools,
        system=system,
        template=template,
        options=options,
        keep_alive=keep_alive
    ))

# Example tool definitions
def get_weather_tool_definition() -> Dict[str, Any]:
    """Get a pre-defined weather tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location visible in the image",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state or country (e.g., 'San Francisco, CA')"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature"
                    }
                },
                "required": ["location"]
            }
        }
    }

def get_search_tool_definition() -> Dict[str, Any]:
    """Get a pre-defined web search tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information about something visible in the image",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return"
                    }
                },
                "required": ["query"]
            }
        }
    }

def get_identify_object_tool_definition() -> Dict[str, Any]:
    """Get a pre-defined object identification tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "identify_object",
            "description": "Identify or get information about an object visible in the image",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_description": {
                        "type": "string",
                        "description": "Brief description of the object to identify"
                    },
                    "location_in_image": {
                        "type": "string",
                        "description": "Where in the image the object is located (e.g., 'top left', 'center')"
                    }
                },
                "required": ["object_description"]
            }
        }
    }

# New functions for continuous chat with LLM with streaming

async def async_continuous_chat_stream(
    messages: List[Dict[str, str]],
    new_user_message: str,
    model: str,
    callback: Optional[Callable[[str], None]] = None,
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Stream a response from an LLM in a continuous conversation, maintaining chat history.
    
    Args:
        messages: List of previous message dictionaries with 'role' and 'content' fields
        new_user_message: The new user message to add to the conversation
        model: The name of the LLM model to use (e.g. "llama2", "smollm2")
        callback: Optional callback function to process streamed content
        system: System prompt to use (default: None)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        
    Returns:
        Updated messages list with the new user message and assistant response
    """
    # Initialize the client
    client = OllamaLLMClient(model_name=model)
    
    # Create a working copy of the messages
    updated_messages = messages.copy()
    
    # Check if a system message exists and ensure it's first
    has_system_message = any(msg.get("role") == "system" for msg in updated_messages)
    
    # If system prompt is provided but no system message exists, add it at the beginning
    if system and not has_system_message:
        updated_messages.insert(0, {"role": "system", "content": system})
    # If system prompt is provided and there's already a system message, update it
    elif system and has_system_message:
        for msg in updated_messages:
            if msg.get("role") == "system":
                msg["content"] = system
                break
    
    # Add the new user message to the conversation
    updated_messages.append({"role": "user", "content": new_user_message})
    
    print("\nStreaming response in continuous chat:")
    print("-" * 50)
    print(f"Model: {model}")
    print(f"Chat history length: {len(updated_messages)} messages")
    print(f"Latest user message: {new_user_message}")
    print("-" * 50)
    
    # Stream the response
    full_response = ""
    
    try:
        async for chunk in client.stream_chat(
            messages=updated_messages,
            template=template,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content
            if "message" in chunk and "content" in chunk["message"]:
                chunk_text = chunk["message"]["content"]
                full_response += chunk_text
                print(chunk_text, end="", flush=True)
                
                # Call the callback if provided
                if callback:
                    callback(chunk_text)
            
        # After streaming completes, add the full response to the conversation
        updated_messages.append({"role": "assistant", "content": full_response})
        
        print("\n" + "-" * 50)
        print("Streaming complete!")
        
        return updated_messages
    
    except Exception as e:
        print(f"\nError during continuous chat streaming: {str(e)}")
        # Still add the partial response if we got one before the error
        if full_response:
            updated_messages.append({"role": "assistant", "content": full_response})
        raise

def continuous_chat_stream(
    messages: List[Dict[str, str]],
    new_user_message: str,
    model: str,
    callback: Optional[Callable[[str], None]] = None,
    system: Optional[str] = None,
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Synchronous wrapper for async_continuous_chat_stream.
    """
    return asyncio.run(async_continuous_chat_stream(
        messages=messages,
        new_user_message=new_user_message,
        model=model,
        callback=callback,
        system=system,
        template=template,
        options=options,
        keep_alive=keep_alive
    ))

async def async_interactive_chat_session(
    model: str,
    system_prompt: Optional[str] = "You are a helpful, friendly AI assistant.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True
) -> List[Dict[str, str]]:
    """
    Asynchronous implementation of an interactive chat session with an LLM.
    
    Args:
        model: The name of the LLM model to use (e.g. "llama2", "smollm2")
        system_prompt: System prompt to define assistant behavior (default: helpful assistant)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Initialize the client - one client for the entire session
    client = OllamaLLMClient(model_name=model)
    
    # Initialize conversation with system message
    conversation = []
    if system_prompt:
        conversation = [{"role": "system", "content": system_prompt}]
    
    # Keep a complete history for returning at the end
    full_history = conversation.copy()
    
    print(f"\nStarting interactive chat with model: {model}")
    print("-" * 50)
    if system_prompt:
        print(f"System prompt: {system_prompt[:100]}..." if len(system_prompt) > 100 else f"System prompt: {system_prompt}")
    print("Type 'exit' or 'quit' to end the conversation.")
    if not include_user_messages and not include_assistant_responses:
        print("Context retention: DISABLED (no conversation history will be sent to the model)")
    elif include_user_messages and not include_assistant_responses:
        print("Context retention: Only USER messages will be retained")
    elif not include_user_messages and include_assistant_responses:
        print("Context retention: Only ASSISTANT responses will be retained")
    else:
        print("Context retention: FULL (both user messages and assistant responses)")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_message = input("\nYou: ")
            
            # Check if user wants to exit
            if user_message.lower() in ['exit', 'quit']:
                print("Ending conversation.")
                break
            
            # Add user message to full history
            full_history.append({"role": "user", "content": user_message})
            
            # Create context for this turn based on retention settings
            turn_context = conversation.copy()
            
            # Add the new user message to the current turn context
            turn_context.append({"role": "user", "content": user_message})
            
            print("\nAssistant: ", end="", flush=True)
            
            # Stream the response
            full_response = ""
            
            # Directly use the client's stream_chat method without creating a new event loop
            async for chunk in client.stream_chat(
                messages=turn_context,
                template=template,
                options=options,
                keep_alive=keep_alive
            ):
                # Handle text content
                if "message" in chunk and "content" in chunk["message"]:
                    chunk_text = chunk["message"]["content"]
                    full_response += chunk_text
                    print(chunk_text, end="", flush=True)
            
            # Add assistant's response to full history
            full_history.append({"role": "assistant", "content": full_response})
            
            # Update the conversation context based on retention settings
            conversation = []
            if system_prompt:
                conversation = [{"role": "system", "content": system_prompt}]
                
            # Add previous messages based on settings
            for msg in full_history[1:]:  # Skip the system message
                role = msg.get("role", "")
                if role == "user" and include_user_messages:
                    conversation.append(msg)
                elif role == "assistant" and include_assistant_responses:
                    conversation.append(msg)
                    
        except KeyboardInterrupt:
            print("\nConversation interrupted by user.")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Continuing conversation...")
    
    # Print the full conversation history at the end
    print("\nFull conversation history:")
    for i, msg in enumerate(full_history):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if len(content) > 50:
            print(f"{i+1}. {role.capitalize()}: {content[:50]}...")
        else:
            print(f"{i+1}. {role.capitalize()}: {content}")
    
    return full_history

def interactive_chat_session(
    model: str,
    system_prompt: Optional[str] = "You are a helpful, friendly AI assistant.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True
) -> List[Dict[str, str]]:
    """
    Start an interactive chat session with an LLM that maintains conversation context.
    Uses a single event loop for the entire session.
    
    Args:
        model: The name of the LLM model to use (e.g. "llama2", "smollm2")
        system_prompt: System prompt to define assistant behavior (default: helpful assistant)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Create a single event loop for the entire session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the async function in this loop
        return loop.run_until_complete(
            async_interactive_chat_session(
                model=model,
                system_prompt=system_prompt,
                template=template,
                options=options,
                keep_alive=keep_alive,
                include_user_messages=include_user_messages,
                include_assistant_responses=include_assistant_responses
            )
        )
    finally:
        # Clean up the loop
        loop.close()

async def async_interactive_vlm_session(
    model: str,
    images_dir: str,
    system_prompt: Optional[str] = "You are a helpful vision assistant that can analyze images.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True,
    tools: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Asynchronous implementation of an interactive chat session with a VLM.
    
    Args:
        model: The name of the VLM model to use (e.g. "llava", "gemini-pro-vision")
        images_dir: Directory containing images to analyze
        system_prompt: System prompt to define assistant behavior (default: helpful vision assistant)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        tools: List of tool definitions to provide to the model (default: None)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Initialize the client - one client for the entire session
    client = OllamaVLMClient(model_name=model)
    
    # Initialize conversation with system message
    conversation = []
    if system_prompt:
        conversation = [{"role": "system", "content": system_prompt}]
    
    # Keep a complete history for returning at the end
    full_history = conversation.copy()
    
    print(f"\nStarting interactive VLM chat with model: {model}")
    print("-" * 50)
    if system_prompt:
        print(f"System prompt: {system_prompt[:100]}..." if len(system_prompt) > 100 else f"System prompt: {system_prompt}")
    print(f"Images directory: {images_dir}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'image:filename.jpg' to analyze a specific image from the images directory.")
    
    if not include_user_messages and not include_assistant_responses:
        print("Context retention: DISABLED (no conversation history will be sent to the model)")
    elif include_user_messages and not include_assistant_responses:
        print("Context retention: Only USER messages will be retained")
    elif not include_user_messages and include_assistant_responses:
        print("Context retention: Only ASSISTANT responses will be retained")
    else:
        print("Context retention: FULL (both user messages and assistant responses)")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            # Check if user wants to exit
            if user_input.lower() in ['exit', 'quit']:
                print("Ending conversation.")
                break
            
            # Check if this is an image analysis request
            current_image_path = None
            if user_input.startswith('image:'):
                # Extract image filename
                image_filename = user_input.split(':', 1)[1].strip()
                current_image_path = str(Path(images_dir) / image_filename)
                
                if not Path(current_image_path).exists():
                    print(f"Error: Image file not found: {current_image_path}")
                    continue
                
                # Ask for the prompt to analyze this image
                user_message = input("Enter prompt to analyze this image: ")
            else:
                # Regular text prompt without image
                user_message = user_input
                
            # Create user message object
            user_msg = {"role": "user", "content": user_message}
            if current_image_path:
                # For messages with images, add the image path
                user_msg["images"] = [current_image_path]
            
            # Add user message to full history
            full_history.append(user_msg)
            
            # Create context for this turn based on retention settings
            turn_context = conversation.copy()
            
            # Add the new user message to the current turn context
            turn_context.append(user_msg)
            
            print("\nAssistant: ", end="", flush=True)
            
            # Stream the response
            full_response = ""
            collected_tool_calls = []
            
            if current_image_path:
                # Using vision capabilities
                images = [current_image_path]
                
                # Process based on whether tools are provided
                stream_method = client.stream_complete_with_vision
                if tools:
                    print(f"Using {len(tools)} tools for this request")
                
                # Stream the VLM response
                async for chunk in stream_method(
                    prompt=user_message,
                    images=images,
                    system=system_prompt,
                    template=template,
                    tools=tools,
                    options=options,
                    keep_alive=keep_alive
                ):
                    # Handle text content
                    if "response" in chunk:
                        chunk_text = chunk["response"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    elif "message" in chunk and "content" in chunk["message"]:
                        chunk_text = chunk["message"]["content"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    
                    # Handle tool calls if present
                    if "message" in chunk and "tool_calls" in chunk["message"]:
                        tool_calls = chunk["message"]["tool_calls"]
                        
                        for tool_call in tool_calls:
                            # Check if tool call already processed
                            tool_call_id = tool_call.get("id", "")
                            existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                            
                            if tool_call_id not in existing_ids:
                                collected_tool_calls.append(tool_call)
                                function_info = tool_call.get("function", {})
                                function_name = function_info.get("name", "unknown")
                                function_args = function_info.get("arguments", "{}")
                                
                                # Pretty-print the tool call
                                print(f"\n\nTool Call: {function_name}")
                                try:
                                    # Try to parse and pretty-print JSON arguments
                                    args_obj = json.loads(function_args)
                                    print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                                except json.JSONDecodeError:
                                    # If not valid JSON, print as is
                                    print(f"Arguments: {function_args}")
            else:
                # Text-only interaction (no image)
                # For VLM client, we should use the same stream_complete_with_vision but without images
                # VLM client doesn't have stream_chat, so we use stream_complete_with_vision with empty images list
                async for chunk in client.stream_complete_with_vision(
                    prompt=user_message,
                    images=[],  # Empty images list for text-only interaction
                    system=system_prompt,
                    template=template,
                    tools=tools,
                    options=options,
                    keep_alive=keep_alive
                ):
                    # Handle text content
                    if "response" in chunk:
                        chunk_text = chunk["response"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    elif "message" in chunk and "content" in chunk["message"]:
                        chunk_text = chunk["message"]["content"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    
                    # Handle tool calls if present
                    if "message" in chunk and "tool_calls" in chunk["message"]:
                        tool_calls = chunk["message"]["tool_calls"]
                        
                        for tool_call in tool_calls:
                            # Check if tool call already processed
                            tool_call_id = tool_call.get("id", "")
                            existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                            
                            if tool_call_id not in existing_ids:
                                collected_tool_calls.append(tool_call)
                                function_info = tool_call.get("function", {})
                                function_name = function_info.get("name", "unknown")
                                function_args = function_info.get("arguments", "{}")
                                
                                # Pretty-print the tool call
                                print(f"\n\nTool Call: {function_name}")
                                try:
                                    # Try to parse and pretty-print JSON arguments
                                    args_obj = json.loads(function_args)
                                    print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                                except json.JSONDecodeError:
                                    # If not valid JSON, print as is
                                    print(f"Arguments: {function_args}")
            
            # Create assistant response object
            assistant_msg = {"role": "assistant", "content": full_response}
            if collected_tool_calls:
                assistant_msg["tool_calls"] = collected_tool_calls
            
            # Add assistant's response to full history
            full_history.append(assistant_msg)
            
            # Update the conversation context based on retention settings
            conversation = []
            if system_prompt:
                conversation = [{"role": "system", "content": system_prompt}]
                
            # Add previous messages based on settings
            for msg in full_history[1:]:  # Skip the system message
                role = msg.get("role", "")
                if role == "user" and include_user_messages:
                    conversation.append(msg)
                elif role == "assistant" and include_assistant_responses:
                    conversation.append(msg)
                    
        except KeyboardInterrupt:
            print("\nConversation interrupted by user.")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Continuing conversation...")
    
    # Print the full conversation history at the end
    print("\nFull conversation history:")
    for i, msg in enumerate(full_history):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        # Show if message had an image
        has_image = "images" in msg and msg["images"]
        image_indicator = " [with image]" if has_image else ""
        
        # Show if message had tool calls
        has_tools = "tool_calls" in msg and msg["tool_calls"]
        tools_indicator = f" [with {len(msg['tool_calls'])} tool calls]" if has_tools else ""
        
        # Print message summary
        indicators = image_indicator + tools_indicator
        if len(content) > 50:
            print(f"{i+1}. {role.capitalize()}{indicators}: {content[:50]}...")
        else:
            print(f"{i+1}. {role.capitalize()}{indicators}: {content}")
    
    return full_history

def interactive_vlm_session(
    model: str,
    images_dir: str,
    system_prompt: Optional[str] = "You are a helpful vision assistant that can analyze images.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True,
    tools: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Start an interactive chat session with a VLM that maintains conversation context.
    
    Args:
        model: The name of the VLM model to use (e.g. "llava", "gemini-pro-vision")
        images_dir: Directory containing images to analyze
        system_prompt: System prompt to define assistant behavior (default: helpful vision assistant)
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        tools: List of tool definitions to provide to the model (default: None)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Create a single event loop for the entire session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the async function in this loop
        return loop.run_until_complete(
            async_interactive_vlm_session(
                model=model,
                images_dir=images_dir,
                system_prompt=system_prompt,
                template=template,
                options=options,
                keep_alive=keep_alive,
                include_user_messages=include_user_messages,
                include_assistant_responses=include_assistant_responses,
                tools=tools
            )
        )
    finally:
        # Clean up the loop
        loop.close()

async def async_vlm_generate_multi_image(
    prompt: str, 
    image_paths: List[str], 
    model: str, 
    stream: bool = False, 
    sequence_aware_system: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a response from Ollama using a vision language model (VLM) with multiple images.
    
    Args:
        prompt: The text prompt to send to the model
        image_paths: List of paths to image files to analyze in sequence
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        stream: Whether to stream the response (default: False)
        sequence_aware_system: Whether to add image sequence awareness to system prompt (default: True)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system', '')
    template = kwargs.get('template')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')
    
    # If sequence_aware_system is True, append sequence information to system prompt
    if sequence_aware_system and image_paths and len(image_paths) > 1:
        sequence_info = f"\nIMPORTANT: You will be presented with {len(image_paths)} images in a specific sequence. " \
                         f"Process and analyze these images IN THE EXACT ORDER they are provided. " \
                         f"When referring to images, use 'first image', 'second image', etc. to maintain clarity."
        
        # Add the sequence info to the existing system prompt or create a new one
        if system:
            system = system + sequence_info
        else:
            system = f"You are a vision assistant analyzing multiple images in sequence.{sequence_info}"
    
    # If streaming is requested, collect all chunks into a single response
    if stream:
        full_response = {"response": ""}
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=image_paths,  # Pass the list of image paths directly
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                full_response["response"] += chunk["response"]
            elif "message" in chunk and "content" in chunk["message"]:
                full_response["response"] += chunk["message"]["content"]
                
            # Handle tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                if "tool_calls" not in full_response:
                    full_response["tool_calls"] = []
                
                for tool_call in chunk["message"]["tool_calls"]:
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in full_response.get("tool_calls", [])]
                    if tool_call_id not in existing_ids:
                        full_response.setdefault("tool_calls", []).append(tool_call)
                
        return full_response
    else:
        # Get a complete response at once
        response = await client.complete_with_vision(
            prompt=prompt,
            images=image_paths,  # Pass the list of image paths directly
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        )
        
        # Process the response to ensure consistent format
        if "message" in response and "content" in response["message"]:
            response["response"] = response["message"]["content"]
            
        return response

def vlm_generate_multi_image(
    prompt: str, 
    image_paths: List[str], 
    model: str, 
    stream: bool = False, 
    sequence_aware_system: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_vlm_generate_multi_image.
    
    Args:
        prompt: The text prompt to send to the model
        image_paths: List of paths to image files to analyze in sequence
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        stream: Whether to stream the response (default: False)
        sequence_aware_system: Whether to add image sequence awareness to system prompt (default: True)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    return asyncio.run(async_vlm_generate_multi_image(prompt, image_paths, model, stream, sequence_aware_system, **kwargs))

async def async_stream_vlm_multi_image(
    prompt: str, 
    image_paths: List[str], 
    model: str,
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    sequence_aware_system: bool = True,
    **kwargs
) -> None:
    """
    Generate a response from a VLM using text and multiple images and stream it in real-time.
    
    Args:
        prompt: The text prompt to send to the model
        image_paths: List of paths to image files to analyze in sequence
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        callback: Optional callback function to process content and tool calls
        sequence_aware_system: Whether to add image sequence awareness to system prompt (default: True)
        **kwargs: Additional parameters to pass to the Ollama API
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Extract parameters from kwargs
    system = kwargs.get('system', '')
    template = kwargs.get('template')
    options = kwargs.get('options')
    keep_alive = kwargs.get('keep_alive')
    tools = kwargs.get('tools')
    
    # If sequence_aware_system is True, append sequence information to system prompt
    if sequence_aware_system and image_paths and len(image_paths) > 1:
        sequence_info = f"\nIMPORTANT: You will be presented with {len(image_paths)} images in a specific sequence. " \
                         f"Process and analyze these images IN THE EXACT ORDER they are provided. " \
                         f"When referring to images, use 'first image', 'second image', etc. to maintain clarity."
        
        # Add the sequence info to the existing system prompt or create a new one
        if system:
            system = system + sequence_info
        else:
            system = f"You are a vision assistant analyzing multiple images in sequence.{sequence_info}"
    
    print("\nStreaming VLM response with multiple images in real-time:")
    print("-" * 50)
    print(f"Model: {model}")
    print(f"Number of images: {len(image_paths)}")
    if system:
        print(f"Using system prompt: {system[:100]}..." if len(system) > 100 else f"Using system prompt: {system}")
    if tools:
        print(f"Using {len(tools)} tools")
    print(f"Prompt: {prompt}")
    print("-" * 50)
    
    full_text = ""
    collected_tool_calls = []
    
    try:
        async for chunk in client.stream_complete_with_vision(
            prompt=prompt,
            images=image_paths,
            system=system,
            template=template,
            tools=tools,
            options=options,
            keep_alive=keep_alive
        ):
            # Handle text content - check both direct response and message.content
            if "response" in chunk:
                chunk_text = chunk["response"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            elif "message" in chunk and "content" in chunk["message"]:
                chunk_text = chunk["message"]["content"]
                full_text += chunk_text
                print(chunk_text, end="", flush=True)
            
            # Handle tool calls if present
            if "message" in chunk and "tool_calls" in chunk["message"]:
                tool_calls = chunk["message"]["tool_calls"]
                
                for tool_call in tool_calls:
                    # Check if we've already processed this tool call
                    tool_call_id = tool_call.get("id", "")
                    existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                    
                    if tool_call_id not in existing_ids:
                        collected_tool_calls.append(tool_call)
                        function_info = tool_call.get("function", {})
                        function_name = function_info.get("name", "unknown")
                        function_args = function_info.get("arguments", "{}")
                        
                        # Pretty-print the tool call
                        print(f"\n\nTool Call: {function_name}")
                        try:
                            # Try to parse and pretty-print JSON arguments
                            args_obj = json.loads(function_args)
                            print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                        except json.JSONDecodeError:
                            # If not valid JSON, print as is
                            print(f"Arguments: {function_args}")
        
        # If there's a callback, call it with the content and tool calls
        if callback and (full_text or collected_tool_calls):
            callback(full_text, collected_tool_calls)
        
        print("\n" + "-" * 50)
        if collected_tool_calls:
            print(f"Multi-image VLM streaming complete with {len(collected_tool_calls)} tool calls!")
        else:
            print("Multi-image VLM streaming complete!")
    except Exception as e:
        print(f"\nError during multi-image VLM streaming: {str(e)}")
        raise

def stream_vlm_multi_image(
    prompt: str, 
    image_paths: List[str], 
    model: str,
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    sequence_aware_system: bool = True,
    **kwargs
) -> None:
    """
    Synchronous wrapper for async_stream_vlm_multi_image.
    
    Args:
        prompt: The text prompt to send to the model
        image_paths: List of paths to image files to analyze in sequence
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        callback: Optional callback function to process content and tool calls
        sequence_aware_system: Whether to add image sequence awareness to system prompt (default: True)
        **kwargs: Additional parameters to pass to the Ollama API
    """
    asyncio.run(async_stream_vlm_multi_image(prompt, image_paths, model, callback, sequence_aware_system, **kwargs))

async def async_interactive_multi_image_vlm_session(
    model: str,
    images_dir: str,
    system_prompt: Optional[str] = "You are a helpful vision assistant that can analyze multiple images in sequence.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True,
    tools: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Asynchronous implementation of an interactive chat session with multi-image VLM support.
    
    Args:
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        images_dir: Directory containing images to analyze
        system_prompt: System prompt to define assistant behavior
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        tools: List of tool definitions to provide to the model (default: None)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Initialize the client
    client = OllamaVLMClient(model_name=model)
    
    # Initialize conversation with system message
    conversation = []
    if system_prompt:
        conversation = [{"role": "system", "content": system_prompt}]
    
    # Keep a complete history for returning at the end
    full_history = conversation.copy()
    
    print(f"\nStarting interactive multi-image VLM chat with model: {model}")
    print("-" * 70)
    if system_prompt:
        print(f"System prompt: {system_prompt[:100]}..." if len(system_prompt) > 100 else f"System prompt: {system_prompt}")
    print(f"Images directory: {images_dir}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Use the following commands to analyze images:")
    print("  'images: img1.jpg, img2.jpg' - Analyze multiple images in the specified sequence")
    print("  'image: img1.jpg' - Analyze a single image")
    
    if not include_user_messages and not include_assistant_responses:
        print("Context retention: DISABLED (no conversation history will be sent to the model)")
    elif include_user_messages and not include_assistant_responses:
        print("Context retention: Only USER messages will be retained")
    elif not include_user_messages and include_assistant_responses:
        print("Context retention: Only ASSISTANT responses will be retained")
    else:
        print("Context retention: FULL (both user messages and assistant responses)")
    print("-" * 70)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            # Check if user wants to exit
            if user_input.lower() in ['exit', 'quit']:
                print("Ending conversation.")
                break
            
            # Check if this is an image analysis request with multiple images
            current_image_paths = []
            
            if user_input.startswith('images:'):
                # Extract multiple image filenames
                image_filenames = [img.strip() for img in user_input.split(':', 1)[1].split(',')]
                current_image_paths = [str(Path(images_dir) / filename) for filename in image_filenames]
                
                # Verify images exist
                missing_images = [img for img in current_image_paths if not Path(img).exists()]
                if missing_images:
                    print(f"Error: The following image files were not found: {[Path(img).name for img in missing_images]}")
                    print(f"Please check the filenames and try again.")
                    continue
                
                # Ask for the prompt to analyze these images
                user_message = input("Enter prompt to analyze these images: ")
                
                # Add sequence awareness to system prompt for this turn if multiple images
                if len(current_image_paths) > 1:
                    sequence_info = f"\nIMPORTANT: You will be presented with {len(current_image_paths)} images in a specific sequence. " \
                                    f"Process and analyze these images IN THE EXACT ORDER they are provided. " \
                                    f"When referring to images, use 'first image', 'second image', etc. to maintain clarity."
                    
                    # Add temporary system message just for this turn
                    if system_prompt:
                        temp_system = system_prompt + sequence_info
                    else:
                        temp_system = f"You are a vision assistant analyzing multiple images in sequence.{sequence_info}"
                        
                    # Add temporary system message to beginning of this turn's context
                    system_for_this_turn = temp_system
                else:
                    system_for_this_turn = system_prompt
                
            elif user_input.startswith('image:'):
                # Handle single image case (for backward compatibility)
                image_filename = user_input.split(':', 1)[1].strip()
                image_path = str(Path(images_dir) / image_filename)
                
                if not Path(image_path).exists():
                    print(f"Error: Image file not found: {image_path}")
                    continue
                
                current_image_paths = [image_path]
                
                # Ask for the prompt to analyze this image
                user_message = input("Enter prompt to analyze this image: ")
                system_for_this_turn = system_prompt
                
            else:
                # Regular text prompt without image
                user_message = user_input
                system_for_this_turn = system_prompt
                
            # Create user message object
            user_msg = {"role": "user", "content": user_message}
            if current_image_paths:
                # For messages with images, add the image paths
                user_msg["images"] = current_image_paths
            
            # Add user message to full history
            full_history.append(user_msg)
            
            # Create context for this turn based on retention settings
            turn_context = []
            if system_for_this_turn:
                turn_context = [{"role": "system", "content": system_for_this_turn}]
            
            # Add previous messages based on retention settings
            if include_user_messages or include_assistant_responses:
                for msg in full_history:
                    role = msg.get("role", "")
                    if role == "system":
                        continue  # Skip system message, we already handled it
                    elif role == "user" and include_user_messages:
                        turn_context.append(msg)
                    elif role == "assistant" and include_assistant_responses:
                        turn_context.append(msg)
            
            # Add the new user message to the current turn context
            if user_msg not in turn_context:  # Avoid duplicating the message
                turn_context.append(user_msg)
            
            print("\nAssistant: ", end="", flush=True)
            
            # Stream the response
            full_response = ""
            collected_tool_calls = []
            
            if current_image_paths:
                # Using vision capabilities with images
                stream_method = client.stream_chat_with_vision
                
                # Stream the VLM response
                async for chunk in stream_method(
                    messages=turn_context,
                    images=current_image_paths,
                    system=None,  # System is already in the messages
                    template=template,
                    tools=tools,
                    options=options,
                    keep_alive=keep_alive
                ):
                    # Handle text content
                    if "response" in chunk:
                        chunk_text = chunk["response"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    elif "message" in chunk and "content" in chunk["message"]:
                        chunk_text = chunk["message"]["content"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    
                    # Handle tool calls if present
                    if "message" in chunk and "tool_calls" in chunk["message"]:
                        tool_calls = chunk["message"]["tool_calls"]
                        
                        for tool_call in tool_calls:
                            # Check if tool call already processed
                            tool_call_id = tool_call.get("id", "")
                            existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                            
                            if tool_call_id not in existing_ids:
                                collected_tool_calls.append(tool_call)
                                function_info = tool_call.get("function", {})
                                function_name = function_info.get("name", "unknown")
                                function_args = function_info.get("arguments", "{}")
                                
                                # Pretty-print the tool call
                                print(f"\n\nTool Call: {function_name}")
                                try:
                                    # Try to parse and pretty-print JSON arguments
                                    args_obj = json.loads(function_args)
                                    print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                                except json.JSONDecodeError:
                                    # If not valid JSON, print as is
                                    print(f"Arguments: {function_args}")
            else:
                # Text-only interaction (no image)
                # Process the messages as a chat using stream_chat
                # For VLM client, we're using stream_chat_with_vision with empty images list
                async for chunk in client.stream_chat_with_vision(
                    messages=turn_context,
                    images=[],  # Empty images list for text-only interaction
                    system=None,  # System already in messages
                    template=template,
                    tools=tools,
                    options=options,
                    keep_alive=keep_alive
                ):
                    # Handle text content
                    if "response" in chunk:
                        chunk_text = chunk["response"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    elif "message" in chunk and "content" in chunk["message"]:
                        chunk_text = chunk["message"]["content"]
                        full_response += chunk_text
                        print(chunk_text, end="", flush=True)
                    
                    # Handle tool calls if present
                    if "message" in chunk and "tool_calls" in chunk["message"]:
                        tool_calls = chunk["message"]["tool_calls"]
                        
                        for tool_call in tool_calls:
                            # Check if tool call already processed
                            tool_call_id = tool_call.get("id", "")
                            existing_ids = [tc.get("id", "") for tc in collected_tool_calls]
                            
                            if tool_call_id not in existing_ids:
                                collected_tool_calls.append(tool_call)
                                function_info = tool_call.get("function", {})
                                function_name = function_info.get("name", "unknown")
                                function_args = function_info.get("arguments", "{}")
                                
                                # Pretty-print the tool call
                                print(f"\n\nTool Call: {function_name}")
                                try:
                                    # Try to parse and pretty-print JSON arguments
                                    args_obj = json.loads(function_args)
                                    print(f"Arguments: {json.dumps(args_obj, indent=2)}")
                                except json.JSONDecodeError:
                                    # If not valid JSON, print as is
                                    print(f"Arguments: {function_args}")
            
            # Create assistant response object
            assistant_msg = {"role": "assistant", "content": full_response}
            if collected_tool_calls:
                assistant_msg["tool_calls"] = collected_tool_calls
            
            # Add assistant's response to full history
            full_history.append(assistant_msg)
                    
        except KeyboardInterrupt:
            print("\nConversation interrupted by user.")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Continuing conversation...")
    
    # Print the full conversation history at the end
    print("\nFull conversation history:")
    for i, msg in enumerate(full_history):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        # Show if message had images
        has_images = "images" in msg and msg["images"]
        image_indicator = f" [with {len(msg['images'])} images]" if has_images else ""
        
        # Show if message had tool calls
        has_tools = "tool_calls" in msg and msg["tool_calls"]
        tools_indicator = f" [with {len(msg['tool_calls'])} tool calls]" if has_tools else ""
        
        # Print message summary
        indicators = image_indicator + tools_indicator
        if len(content) > 50:
            print(f"{i+1}. {role.capitalize()}{indicators}: {content[:50]}...")
        else:
            print(f"{i+1}. {role.capitalize()}{indicators}: {content}")
    
    return full_history

def interactive_multi_image_vlm_session(
    model: str,
    images_dir: str,
    system_prompt: Optional[str] = "You are a helpful vision assistant that can analyze multiple images in sequence.",
    template: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
    include_user_messages: bool = True,
    include_assistant_responses: bool = True,
    tools: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Start an interactive chat session with a VLM that supports multiple images per message.
    
    Args:
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        images_dir: Directory containing images to analyze
        system_prompt: System prompt to define assistant behavior
        template: Custom prompt template (default: None)
        options: Additional parameters to pass to the Ollama API (default: None)
        keep_alive: Duration to keep the model loaded (default: None)
        include_user_messages: Whether to include previous user messages in context (default: True)
        include_assistant_responses: Whether to include previous assistant responses in context (default: True)
        tools: List of tool definitions to provide to the model (default: None)
        
    Returns:
        The complete conversation history when the session ends
    """
    # Create a single event loop for the entire session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Run the async function in this loop
        return loop.run_until_complete(
            async_interactive_multi_image_vlm_session(
                model=model,
                images_dir=images_dir,
                system_prompt=system_prompt,
                template=template,
                options=options,
                keep_alive=keep_alive,
                include_user_messages=include_user_messages,
                include_assistant_responses=include_assistant_responses,
                tools=tools
            )
        )
    finally:
        # Clean up the loop
        loop.close()

def analyze_images_in_sequence(
    image_dir: str,
    model: str,
    prompt: Optional[str] = None,
    system_prompt: Optional[str] = None,
    sort_method: str = "timestamp",  # "timestamp", "filename", or "numeric"
    reverse_order: bool = False,
    exclusion_pattern: Optional[str] = None,
    stream: bool = False,
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    max_images: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Analyze a sequence of images from a directory using a VLM.
    
    Args:
        image_dir: Directory containing images to analyze
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        prompt: The text prompt to send to the model (default: auto-generated based on sort_method)
        system_prompt: System prompt to define assistant behavior (default: auto-generated)
        sort_method: How to sort images - "timestamp", "filename", or "numeric" (default: "timestamp")
        reverse_order: Whether to reverse the sort order (default: False)
        exclusion_pattern: Regex pattern to exclude files (default: None)
        stream: Whether to stream the response (default: False)
        callback: Optional callback function for streaming (default: None)
        max_images: Maximum number of images to process (default: None - process all)
        **kwargs: Additional parameters to pass to the VLM
        
    Returns:
        The response from the VLM as a dictionary
    """
    import os
    import re
    
    # Find all image files in the directory
    image_files = []
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    try:
        for file in os.listdir(image_dir):
            file_path = os.path.join(image_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file_path)
                if ext.lower() in supported_extensions:
                    # Skip if it matches exclusion pattern
                    if exclusion_pattern and re.search(exclusion_pattern, file_path):
                        continue
                        
                    # Store relevant sorting key based on sort method
                    if sort_method == "timestamp":
                        sort_key = os.path.getmtime(file_path)
                    elif sort_method == "filename":
                        sort_key = file.lower()  # Case-insensitive sort
                    elif sort_method == "numeric":
                        # Try to extract numbers from the filename for natural sorting
                        numbers = re.findall(r'\d+', file)
                        # If numbers found, use the last number group for sorting
                        if numbers:
                            numeric_part = numbers[-1]
                            sort_key = file.replace(numeric_part, numeric_part.zfill(10))
                        else:
                            sort_key = file.lower()
                    else:
                        # Default to timestamp
                        sort_key = os.path.getmtime(file_path)
                    
                    image_files.append((file_path, sort_key))
        
        # Sort images by the chosen method
        image_files.sort(key=lambda x: x[1])
        
        # Apply reverse order if requested
        if reverse_order:
            image_files.reverse()
        
        # Limit number of images if max_images is specified
        if max_images and len(image_files) > max_images:
            image_files = image_files[:max_images]
        
        # Get list of image paths
        sorted_image_paths = [img[0] for img in image_files]
        
        if not sorted_image_paths:
            raise ValueError(f"No image files found in {image_dir}")
        
        # Generate default prompt if not provided
        if not prompt:
            time_term = "chronologically" if sort_method == "timestamp" else "sequentially"
            order_term = "reverse " if reverse_order else ""
            prompt = f"Analyze these images that are sorted {order_term}{time_term}. Describe what you see and any changes or progression across the sequence."
        
        # Generate default system prompt if not provided
        if not system_prompt:
            if sort_method == "timestamp":
                order_type = "CHRONOLOGICAL"
                if reverse_order:
                    order_description = f"REVERSE {order_type} ORDER (sorted by timestamp from newest to oldest)"
                else:
                    order_description = f"{order_type} ORDER (sorted by timestamp from oldest to newest)"
            else:
                order_type = "SEQUENTIAL"
                if reverse_order:
                    order_description = f"REVERSE {order_type} ORDER (sorted by filename in reverse)"
                else:
                    order_description = f"{order_type} ORDER (sorted by filename)"
            
            system_prompt = f"""You are an advanced vision assistant analyzing a sequence of {len(sorted_image_paths)} images.
IMPORTANT: These images are provided in {order_description}.
When referring to the images, use 'first image', 'second image', etc. through to 'image {len(sorted_image_paths)}'.
Analyze both individual images and the progression/changes across the sequence.
If timestamps or sequence indicators are visible in the images, note them and use them to enhance your analysis.
"""
        
        # Call the appropriate function based on streaming preference
        if stream:
            if callback:
                return stream_vlm_multi_image(
                    prompt=prompt,
                    image_paths=sorted_image_paths,
                    model=model,
                    system=system_prompt,
                    callback=callback,
                    sequence_aware_system=True,
                    **kwargs
                )
            else:
                # For streaming without callback, we still need to return something
                stream_vlm_multi_image(
                    prompt=prompt,
                    image_paths=sorted_image_paths,
                    model=model,
                    system=system_prompt,
                    sequence_aware_system=True,
                    **kwargs
                )
                return {"status": "streaming_complete", "image_count": len(sorted_image_paths)}
        else:
            # Non-streaming version returns the full response
            return vlm_generate_multi_image(
                prompt=prompt,
                image_paths=sorted_image_paths,
                model=model,
                system=system_prompt,
                sequence_aware_system=True,
                **kwargs
            )
            
    except Exception as e:
        # Provide detailed error information
        return {
            "error": str(e),
            "status": "failed",
            "image_count": len(image_files) if 'image_files' in locals() else 0
        }
        
async def async_vlm_analyze_screenshot_events(
    screenshot_events: List[ScreenshotEvent],
    user_prompt: str,
    model: str,
    prefer_annotated: bool = False,
    system_prompt: Optional[str] = None,
    stream: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a response from a vision language model analyzing a sequence of screenshot events.
    
    Args:
        screenshot_events: List of ScreenshotEvent objects containing screenshot metadata
        user_prompt: The text prompt to send to the model to analyze the screenshots
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        prefer_annotated: Whether to use annotated images when available (default: True)
        system_prompt: Custom system prompt to use (default: None)
        stream: Whether to stream the response (default: False)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    # Extract image paths from screenshot events
    image_paths = []
    descriptions = []
    
    # Generate event sequence information for each image
    for i, event in enumerate(screenshot_events):
        # Determine which image path to use (annotated or raw)
        if prefer_annotated and event.annotation_path:
            image_path = event.annotation_path
        elif event.screenshot_path:
            image_path = event.screenshot_path
        else:
            continue  # Skip events without valid image paths
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Warning: Screenshot file not found, skipping: {image_path}")
            continue
        
        print(f"Processing screenshot {i+1}: {image_path}")
            
        image_paths.append(image_path)
        
        # Extract event description
        if event.description:
            descriptions.append(f"Screenshot {i+1}: {event.description}")
            
            # Add context about mouse/keyboard interaction if available
            interaction_details = []
            if event.mouse_x is not None and event.mouse_y is not None:
                interaction_details.append(f"Mouse position: ({event.mouse_x}, {event.mouse_y})")
            if event.key_char:
                interaction_details.append(f"Key pressed: {event.key_char}")
            elif event.key_code:
                interaction_details.append(f"Special key pressed: {event.key_code}")
                
            if interaction_details:
                descriptions[-1] += f" [{' | '.join(interaction_details)}]"
    
    if not image_paths:
        return {"error": "No valid images found in the provided screenshot events"}
    
    # Create a sequence-aware system prompt if not provided
    if system_prompt is None:
        system_prompt = (
            f"You are analyzing a sequence of {len(image_paths)} screenshots captured during a user session. "
            f"These screenshots show steps of user interaction with an application. "
            f"Analyze them in sequence and provide insights based on the user's prompt."
        )
    
    # Add descriptions to user prompt if available
    enriched_prompt = user_prompt
    if descriptions:
        enriched_prompt = f"{user_prompt}\n\nContext about the screenshots:\n" + "\n".join(descriptions)
    
    # Call the multi-image VLM function
    return await async_vlm_generate_multi_image(
        prompt=enriched_prompt,
        image_paths=image_paths,
        model=model,
        stream=stream,
        sequence_aware_system=True,
        system=system_prompt,
        **kwargs
    )

def vlm_analyze_screenshot_events(
    screenshot_events: List[ScreenshotEvent],
    user_prompt: str,
    model: str,
    prefer_annotated: bool = False,
    system_prompt: Optional[str] = None,
    stream: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Synchronous wrapper for async_vlm_analyze_screenshot_events.
    
    Args:
        screenshot_events: List of ScreenshotEvent objects containing screenshot metadata
        user_prompt: The text prompt to send to the model to analyze the screenshots
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        prefer_annotated: Whether to use annotated images when available (default: True)
        system_prompt: Custom system prompt to use (default: None)
        stream: Whether to stream the response (default: False)
        **kwargs: Additional parameters to pass to the Ollama API
        
    Returns:
        The response from the Ollama API as a dictionary
    """
    return asyncio.run(async_vlm_analyze_screenshot_events(
        screenshot_events=screenshot_events,
        user_prompt=user_prompt,
        model=model,
        prefer_annotated=prefer_annotated,
        system_prompt=system_prompt,
        stream=stream,
        **kwargs
    ))

async def async_stream_vlm_analyze_screenshot_events(
    screenshot_events: List[ScreenshotEvent],
    user_prompt: str,
    model: str,
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    prefer_annotated: bool = False,
    system_prompt: Optional[str] = None,
    **kwargs
) -> None:
    """
    Stream a response from a vision language model analyzing a sequence of screenshot events.
    
    Args:
        screenshot_events: List of ScreenshotEvent objects containing screenshot metadata
        user_prompt: The text prompt to send to the model to analyze the screenshots
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        callback: Optional callback function to process content and tool calls
        prefer_annotated: Whether to use annotated images when available (default: True)
        system_prompt: Custom system prompt to use (default: None)
        **kwargs: Additional parameters to pass to the Ollama API
    """
    # Extract image paths from screenshot events
    image_paths = []
    descriptions = []
    
    # Generate event sequence information for each image
    for i, event in enumerate(screenshot_events):
        # Determine which image path to use (annotated or raw)
        if prefer_annotated and event.annotation_path:
            image_path = event.annotation_path
        elif event.screenshot_path:
            image_path = event.screenshot_path
        else:
            continue  # Skip events without valid image paths
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Warning: Screenshot file not found, skipping: {image_path}")
            continue
        
        print(f"Processing screenshot {i+1}: {image_path}")
            
        image_paths.append(image_path)
        
        # Extract event description
        if event.description:
            descriptions.append(f"Screenshot {i+1}: {event.description}")
            
            # Add context about mouse/keyboard interaction if available
            interaction_details = []
            if event.mouse_x is not None and event.mouse_y is not None:
                interaction_details.append(f"Mouse position: ({event.mouse_x}, {event.mouse_y})")
            if event.key_char:
                interaction_details.append(f"Key pressed: {event.key_char}")
            elif event.key_code:
                interaction_details.append(f"Special key pressed: {event.key_code}")
                
            if interaction_details:
                descriptions[-1] += f" [{' | '.join(interaction_details)}]"
    
    if not image_paths:
        if callback:
            callback("Error: No valid images found in the provided screenshot events", [])
        return
    
    # Create a sequence-aware system prompt if not provided
    if system_prompt is None:
        system_prompt = (
            f"You are analyzing a sequence of {len(image_paths)} screenshots captured during a user session. "
            f"These screenshots show steps of user interaction with an application. "
            f"Analyze them in sequence and provide insights based on the user's prompt."
        )
    
    # Add descriptions to user prompt if available
    enriched_prompt = user_prompt
    if descriptions:
        enriched_prompt = f"{user_prompt}\n\nContext about the screenshots:\n" + "\n".join(descriptions)
    
    # Call the multi-image streaming VLM function
    await async_stream_vlm_multi_image(
        prompt=enriched_prompt,
        image_paths=image_paths,
        model=model,
        callback=callback,
        sequence_aware_system=True,
        system=system_prompt,
        **kwargs
    )

def stream_vlm_analyze_screenshot_events(
    screenshot_events: List[ScreenshotEvent],
    user_prompt: str,
    model: str,
    callback: Optional[Callable[[str, List[Dict[str, Any]]], None]] = None,
    prefer_annotated: bool = False,
    system_prompt: Optional[str] = None,
    **kwargs
) -> None:
    """
    Synchronous wrapper for async_stream_vlm_analyze_screenshot_events.
    
    Args:
        screenshot_events: List of ScreenshotEvent objects containing screenshot metadata
        user_prompt: The text prompt to send to the model to analyze the screenshots
        model: The name of the VLM model to use (e.g. "llava", "granite3.2-vision")
        callback: Optional callback function to process content and tool calls
        prefer_annotated: Whether to use annotated images when available (default: True)
        system_prompt: Custom system prompt to use (default: None)
        **kwargs: Additional parameters to pass to the Ollama API
    """
    asyncio.run(async_stream_vlm_analyze_screenshot_events(
        screenshot_events=screenshot_events,
        user_prompt=user_prompt,
        model=model,
        callback=callback,
        prefer_annotated=prefer_annotated,
        system_prompt=system_prompt,
        **kwargs
    ))