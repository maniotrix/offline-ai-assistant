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

