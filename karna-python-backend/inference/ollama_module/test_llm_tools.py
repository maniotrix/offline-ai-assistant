import asyncio
import json
import os
from typing import Dict, List, Any

# Import the helper functions from ollama_helper
from ollama_helper.llm.llm_helper import (
    llm_generate,
    stream_llm_generate,
    get_weather_tool_definition,
    get_search_tool_definition
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

async def test_llm_with_tools():
    """Test LLM with tool calling capabilities."""
    
    # Define the model to use (needs to support tool calling, e.g., llama3.1)
    model = "llama3.1"  # Replace with your actual model name
    
    # Get predefined tool definitions
    weather_tool = get_weather_tool_definition()
    search_tool = get_search_tool_definition()
    
    # Define custom tool for calculator
    calculator_tool = {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate (e.g., '2 + 2', '5 * 10')"
                    }
                },
                "required": ["expression"]
            }
        }
    }
    
    # Custom system prompt
    system_prompt = "You are a helpful assistant that can use tools to provide better answers."
    
    # Test 1: Basic non-streaming usage with tools
    print("\n" + "="*50)
    print("Test 1: Basic LLM generation with tools")
    print("="*50)
    
    prompt1 = "What's the weather like in New York today?"
    
    try:
        response = llm_generate(
            prompt=prompt1,
            model=model,
            tools=[weather_tool],
            system=system_prompt,
            options={"temperature": 0.7, "top_p": 0.8}
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
    
    # Test 2: Real-time streaming with calculator tool
    print("\n" + "="*50)
    print("Test 2: LLM Streaming with calculator tool")
    print("="*50)
    
    prompt2 = "Calculate the result of (15 * 27) + 42"
    
    try:
        stream_llm_generate(
            prompt=prompt2,
            model=model,
            tools=[calculator_tool],
            system=system_prompt,
            callback=process_tool_calls
        )
    except Exception as e:
        print(f"Error in Test 2: {str(e)}")
    
    # Test 3: Multiple tools
    print("\n" + "="*50)
    print("Test 3: LLM with multiple tool options")
    print("="*50)
    
    prompt3 = "Can you tell me the capital of France and what the weather is like there today?"
    
    try:
        # Test with multiple tools
        response = llm_generate(
            prompt=prompt3,
            model=model,
            tools=[weather_tool, search_tool],
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
        print(f"Error in Test 3: {str(e)}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_llm_with_tools()) 