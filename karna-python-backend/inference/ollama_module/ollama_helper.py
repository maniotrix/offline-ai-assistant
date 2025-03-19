# type: ignore
import asyncio
import json
from typing import Dict, Any, Union, List, Optional, Callable
import base64
from pathlib import Path

# Use proper relative imports
from llm_client import OllamaLLMClient
from vlm_client import OllamaVLMClient

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
                # Stream chat using the existing context
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

if __name__ == "__main__":
    # Test functions for LLM
    def test_regular_generation():
        """Test regular (non-streaming) LLM generation"""
        test_prompt = "Explain how to make a cup of coffee in three steps."
        test_model = "smollm2"
        
        print(f"Testing regular LLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        try:
            response = llm_generate(prompt=test_prompt, model=test_model)
            print("\nResponse:")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def test_streaming_generation():
        """Test streaming LLM generation (collected response)"""
        test_prompt = "Write a short poem about artificial intelligence."
        test_model = "smollm2"
        
        print(f"\nTesting streaming LLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        try:
            response = llm_generate(prompt=test_prompt, model=test_model, stream=True)
            print("\nStreamed Response (collected):")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def test_real_time_streaming(use_system_prompt=True):
        """Test real-time streaming where chunks are displayed as they arrive"""
        test_prompt = "Tell me a short story about a robot learning to feel emotions."
        test_model = "smollm2"
        
        print(f"\nTesting real-time streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        # Define system prompt if enabled
        system_prompt = None
        if use_system_prompt:
            system_prompt = "You are a creative storyteller from India, specialized in emotional narratives about robots and AI."
            print(f"Using system prompt: {system_prompt}")
        
        try:
            stream_llm_generate(prompt=test_prompt, model=test_model, system=system_prompt)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test functions for VLM
    def test_regular_vlm_generation():
        """Test regular (non-streaming) VLM generation"""
        test_prompt = "What can you see in this image?"
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting regular VLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        try:
            response = vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model)
            print("\nVLM Response:")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def test_streaming_vlm_generation():
        """Test streaming VLM generation (collected response)"""
        test_prompt = "Describe this image in detail."
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting streaming VLM generation with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        try:
            response = vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model, stream=True)
            print("\nStreamed VLM Response (collected):")
            print(response.get("response", "No response found"))
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def test_real_time_vlm_streaming(use_system_prompt=True):
        """Test real-time VLM streaming where chunks are displayed as they arrive"""
        test_prompt = "Find the bounding box coordinates of the open requests and output as a json object"
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting real-time VLM streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        # Define system prompt if enabled
        system_prompt = None
        if use_system_prompt:
            system_prompt = """You are a good webpage screenshot reader. 
            You will be given a screenshot of a webpage and you properly analyse the image before answering the user's question."""
            print(f"Using system prompt: {system_prompt}")
        
        try:
            stream_vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model, system=system_prompt)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test functions for continuous chat streaming
    def test_continuous_chat_streaming():
        """Test continuous chat streaming with conversation history using runtime user input"""
        test_model = "smollm2"
        system_prompt = "You are a helpful, friendly AI assistant."
        
        print("\nContext Retention Options:")
        print("1. Full context retention (default)")
        print("2. Only retain user messages")
        print("3. Only retain assistant responses")
        print("4. No context retention (stateless)")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            include_user = True
            include_assistant = True
            
            if choice == 2:
                include_assistant = False
            elif choice == 3:
                include_user = False
            elif choice == 4:
                include_user = False
                include_assistant = False
                
            # Call interactive chat with selected options
            interactive_chat_session(
                model=test_model,
                system_prompt=system_prompt,
                include_user_messages=include_user,
                include_assistant_responses=include_assistant
            )
        except ValueError:
            print("Invalid choice. Using default (full context retention).")
            interactive_chat_session(
                model=test_model,
                system_prompt=system_prompt
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test function for continuous VLM chat streaming
    def test_continuous_vlm_chat():
        """Test continuous chat streaming with a VLM using runtime user input and images"""
        test_model = "granite3.2-vision:latest"  # Set to an appropriate VLM model available in your Ollama instance
        system_prompt = "You are a helpful vision assistant that can analyze images."
        
        # Get images directory from user
        default_images_dir = str(Path(__file__).parent)
        images_dir = input(f"\nEnter directory with images (default: {default_images_dir}): ") or default_images_dir
        
        print("\nContext Retention Options:")
        print("1. Full context retention (default)")
        print("2. Only retain user messages")
        print("3. Only retain assistant responses")
        print("4. No context retention (stateless)")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            include_user = True
            include_assistant = True
            
            if choice == 2:
                include_assistant = False
            elif choice == 3:
                include_user = False
            elif choice == 4:
                include_user = False
                include_assistant = False
            
            # Check if user wants to use tools
            use_tools = input("\nDo you want to use vision tools? (y/n, default: n): ").lower().startswith('y')
            
            tools = None
            if use_tools:
                tools = [
                    get_weather_tool_definition(),
                    get_search_tool_definition(),
                    get_identify_object_tool_definition()
                ]
                print(f"Enabled {len(tools)} vision tools")
                
            # Call interactive VLM chat with selected options
            interactive_vlm_session(
                model=test_model,
                images_dir=images_dir,
                system_prompt=system_prompt,
                include_user_messages=include_user,
                include_assistant_responses=include_assistant,
                tools=tools
            )
        except ValueError:
            print("Invalid choice. Using default (full context retention).")
            interactive_vlm_session(
                model=test_model,
                images_dir=images_dir,
                system_prompt=system_prompt
            )
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Run the test functions
    if __name__ == "__main__":
        # LLM tests
        #test_regular_generation()
        #test_streaming_generation()
        #test_real_time_streaming(use_system_prompt=True)
        # test_continuous_chat_streaming()
        
        # VLM tests
        #test_regular_vlm_generation()
        #test_streaming_vlm_generation()
        #test_real_time_vlm_streaming()
        test_continuous_vlm_chat()  # Run the VLM continuous chat test
