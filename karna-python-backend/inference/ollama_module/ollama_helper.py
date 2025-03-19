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
            
    def test_real_time_streaming():
        """Test real-time streaming where chunks are displayed as they arrive"""
        test_prompt = "Tell me a short story about a robot learning to feel emotions."
        test_model = "smollm2"
        
        print(f"\nTesting real-time streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        
        try:
            stream_llm_generate(prompt=test_prompt, model=test_model)
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
            
    def test_real_time_vlm_streaming():
        """Test real-time VLM streaming where chunks are displayed as they arrive"""
        test_prompt = "briefly Describe the image in 300 words"
        # Use absolute path to ensure the file is found
        test_image = str(Path(__file__).parent / "test.png")
        test_model = "granite3.2-vision:latest"
        
        print(f"\nTesting real-time VLM streaming with model: {test_model}")
        print(f"Prompt: {test_prompt}")
        print(f"Image: {test_image}")
        
        try:
            stream_vlm_generate(prompt=test_prompt, image_path=test_image, model=test_model)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Run the test functions
    if __name__ == "__main__":
        # LLM tests
        #test_regular_generation()
        #test_streaming_generation()
        test_real_time_streaming()
        
        # VLM tests
        #test_regular_vlm_generation()
        #test_streaming_vlm_generation()
        #test_real_time_vlm_streaming()
