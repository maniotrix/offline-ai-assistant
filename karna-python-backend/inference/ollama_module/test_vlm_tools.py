import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Callable

# Import the helper functions from ollama_helper
from ollama_helper.vlm.vlm_helper import (
    vlm_generate,
    stream_vlm_generate,
    vlm_chat_with_tool_response
)

from ollama_helper.llm.llm_helper import (
    get_weather_tool_definition,
    get_search_tool_definition,
    get_identify_object_tool_definition
)

# Helper to process tool calls from callback
def process_tool_calls(content: str, tool_calls: List[Dict[str, Any]]) -> None:
    """Process tool calls in the callback."""
    if tool_calls:
        for tool_call in tool_calls:
            # In a real application, you would implement actual API calls here
            function_info = tool_call.get("function", {})
            function_name = function_info.get("name", "unknown")
            
            print(f"\nProcessing tool call: {function_name}")
            # You would make the actual API call here and get real data

async def test_vlm_with_tools():
    """Test VLM with tool calling capabilities."""
    
    # Check if test image exists
    test_image = str(Path(__file__).parent / "test.png")
    if not Path(test_image).exists():
        print(f"Warning: Test image not found at {test_image}")
        print("Creating a simple test file as a placeholder...")
        # Create a simple placeholder file for testing if needed
        with open(test_image, "w") as f:
            f.write("Test image placeholder")
    
    # Define the model to use (needs to support tool calling and vision)
    model = "granite3.2-vision"  # Replace with your actual model name
    
    # Get predefined tool definitions
    weather_tool = get_weather_tool_definition()
    search_tool = get_search_tool_definition()
    identify_tool = get_identify_object_tool_definition()
    
    # Custom system prompt
    system_prompt = "You are a helpful assistant with vision capabilities. When you see an image, analyze it carefully and use tools when needed to provide better answers."
    
    # Test 1: Basic non-streaming usage with tools
    print("\n" + "="*50)
    print("Test 1: Basic VLM generation with tools")
    print("="*50)
    
    prompt1 = "What can you see in this image? If you see any landmarks or objects you need more information about, use the appropriate tools."
    
    try:
        response = vlm_generate(
            prompt=prompt1,
            image_path=test_image,
            model=model,
            tools=[weather_tool, search_tool, identify_tool],
            system=system_prompt
        )
        
        print("\nResponse:")
        print("-"*50)
        if "response" in response:
            print(response["response"])
        
        if "tool_calls" in response:
            tool_calls = response["tool_calls"]
            print(f"\nTool Calls ({len(tool_calls)}):")
            for i, tool_call in enumerate(tool_calls):
                function_info = tool_call.get("function", {})
                function_name = function_info.get("name", "unknown")
                function_args = function_info.get("arguments", "{}")
                print(f"\n{i+1}. {function_name}")
                try:
                    args_obj = json.loads(function_args)
                    print(f"   Arguments: {json.dumps(args_obj, indent=2)}")
                except json.JSONDecodeError:
                    print(f"   Arguments: {function_args}")
    except Exception as e:
        print(f"Error in Test 1: {str(e)}")
    
    # Test 2: Real-time streaming with tools
    print("\n" + "="*50)
    print("Test 2: VLM Streaming with tools")
    print("="*50)
    
    prompt2 = "What's the weather like in the location shown in this image? Use the weather tool to check current conditions."
    
    try:
        stream_vlm_generate(
            prompt=prompt2,
            image_path=test_image,
            model=model,
            tools=[weather_tool],
            callback=process_tool_calls,
            system=system_prompt
        )
    except Exception as e:
        print(f"Error in Test 2: {str(e)}")
    
    # Test 3: Tool response handling
    print("\n" + "="*50)
    print("Test 3: VLM with tool response handling")
    print("="*50)
    
    prompt3 = "What's the weather like in this image? Please analyze the scene and suggest if I need an umbrella."
    
    try:
        # First, get the initial response with potential tool calls
        initial_response = vlm_generate(
            prompt=prompt3,
            image_path=test_image,
            model=model,
            tools=[weather_tool],
            system=system_prompt
        )
        
        # Check if there are any tool calls
        tool_calls = initial_response.get("tool_calls", [])
        
        if tool_calls:
            # Mock tool response data - in a real app, you would call actual services
            mock_weather_data = {
                "location": "New York, NY",
                "temperature": 75,
                "condition": "Partly Cloudy",
                "precipitation": 20,
                "humidity": 65
            }
            
            # Format the tool responses
            tool_responses = []
            for tool_call in tool_calls:
                function_info = tool_call.get("function", {})
                function_name = function_info.get("name", "unknown")
                
                # Prepare tool response based on the function called
                if function_name == "get_weather":
                    tool_responses.append({
                        "tool_call_id": tool_call.get("id", ""),
                        "content": json.dumps(mock_weather_data)
                    })
            
            if tool_responses:
                # Get final response with the tool results integrated
                final_response = vlm_chat_with_tool_response(
                    prompt=prompt3,
                    image_path=test_image,
                    model=model,
                    tool_responses=tool_responses,
                    tools=[weather_tool],  # Keep tools available for further calls
                    system=system_prompt
                )
                
                print("\nFinal Response with Tool Results:")
                print("-"*50)
                if "response" in final_response:
                    print(final_response["response"])
            else:
                print("No tool responses to process")
        else:
            print("No tool calls were made")
    except Exception as e:
        print(f"Error in Test 3: {str(e)}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_vlm_with_tools()) 