# Ollama VLM and LLM Tool Calling

This module provides a streamlined interface for testing and using Vision Language Models (VLMs) and Language Models (LLMs) with tool calling capabilities via Ollama.

## Features

- Test VLMs with images and text prompts
- Test LLMs with text-only prompts
- Real-time streaming of model responses
- Tool calling support for both VLM and LLM models
- Handling of tool responses in conversations
- Customizable prompt templates and system prompts

## Requirements

- An Ollama server running locally or remotely
- A compatible VLM model (e.g., `granite3.2-vision`) or LLM model (e.g., `llama3.1`)

## Basic Usage

### VLM with Tool Support

```python
from ollama_helper import vlm_generate, get_weather_tool_definition, get_search_tool_definition

# Load a test image
image_path = "path/to/your/image.jpg"

# Get predefined tool definitions
weather_tool = get_weather_tool_definition()
search_tool = get_search_tool_definition()

# Generate a response with tool calling capabilities
response = vlm_generate(
    prompt="What's the weather like in this image? If you can identify the city, use tools to get more information.",
    image_path=image_path,
    model="granite3.2-vision",
    tools=[weather_tool, search_tool],
    system="You are a helpful assistant with vision capabilities."
)

# Process the response
print(response["response"])  # Text response

# Check if any tool calls were made
if "tool_calls" in response:
    for tool_call in response["tool_calls"]:
        function_name = tool_call.get("function", {}).get("name", "")
        arguments = tool_call.get("function", {}).get("arguments", "{}")
        print(f"Tool called: {function_name} with arguments: {arguments}")
```

### Streaming VLM with Tool Support

```python
from ollama_helper import stream_vlm_generate, get_weather_tool_definition

def callback(content, tool_calls):
    # This will be called with the final content and any tool calls
    print(f"Final content length: {len(content)}")
    print(f"Number of tool calls: {len(tool_calls)}")
    
    # Process tool calls
    for tool_call in tool_calls:
        function_name = tool_call.get("function", {}).get("name", "")
        # Make actual API calls based on the tool called
        
stream_vlm_generate(
    prompt="What city is shown in this image and what's the current weather like there?",
    image_path="path/to/your/image.jpg",
    model="granite3.2-vision",
    tools=[get_weather_tool_definition()],
    callback=callback,
    system="You are a helpful assistant with vision capabilities."
)
```

### LLM with Tool Support

```python
from ollama_helper import llm_generate, get_weather_tool_definition

response = llm_generate(
    prompt="What's the weather like in New York today?",
    model="llama3.1",
    tools=[get_weather_tool_definition()],
    system="You are a helpful assistant that can use tools to provide better answers."
)

print(response["response"])

if "tool_calls" in response:
    for tool_call in response["tool_calls"]:
        function_name = tool_call.get("function", {}).get("name", "")
        arguments = tool_call.get("function", {}).get("arguments", "{}")
        print(f"Tool called: {function_name} with arguments: {arguments}")
```

### Complete Conversation with Tool Responses

```python
import json
from ollama_helper import vlm_generate, vlm_chat_with_tool_response, get_weather_tool_definition

# Step 1: Initial prompt with image
weather_tool = get_weather_tool_definition()
initial_response = vlm_generate(
    prompt="What's the weather like in this image?",
    image_path="path/to/your/image.jpg",
    model="granite3.2-vision",
    tools=[weather_tool]
)

# Step 2: Process any tool calls
tool_responses = []
if "tool_calls" in initial_response:
    for tool_call in initial_response["tool_calls"]:
        function_name = tool_call.get("function", {}).get("name", "")
        
        if function_name == "get_weather":
            # In a real application, you would call a weather API here
            weather_data = {
                "temperature": 75,
                "condition": "sunny",
                "humidity": 50,
                "location": "New York"
            }
            
            # Add the tool response
            tool_responses.append({
                "tool_call_id": tool_call.get("id", ""),
                "content": json.dumps(weather_data)
            })

# Step 3: Get final response with tool results
if tool_responses:
    final_response = vlm_chat_with_tool_response(
        prompt="What's the weather like in this image?",
        image_path="path/to/your/image.jpg",
        model="granite3.2-vision",
        tool_responses=tool_responses,
        tools=[weather_tool]  # Keep tools available for follow-up questions
    )
    
    print("Final response with weather data:")
    print(final_response["response"])
```

## Available Tool Definitions

The module includes several predefined tool definitions:

### Weather Tool

```python
from ollama_helper import get_weather_tool_definition

weather_tool = get_weather_tool_definition()
```

### Web Search Tool

```python
from ollama_helper import get_search_tool_definition

search_tool = get_search_tool_definition()
```

### Object Identification Tool

```python
from ollama_helper import get_identify_object_tool_definition

identify_tool = get_identify_object_tool_definition()
```

## Creating Custom Tool Definitions

You can create custom tools by providing your own tool definition:

```python
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
```

## Advanced Usage

### Customizing Model Behavior

```python
from ollama_helper import vlm_generate

# Custom options
options = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_ctx": 8192
}

response = vlm_generate(
    prompt="What can you see in this image?",
    image_path="path/to/your/image.jpg",
    model="granite3.2-vision",
    tools=[get_weather_tool_definition()],
    options=options,
    system="You are a meticulous assistant that notices fine details in images."
)
```

### Custom Template for Conversation History

```python
from ollama_helper import llm_generate

# Custom template for specific model
template = """<|system|>
{{system}}
</s>
{{#each messages}}
<|{{role}}|>
{{content}}
</s>
{{/each}}
"""

response = llm_generate(
    prompt="Tell me about the weather in Paris",
    model="custom-model",
    tools=[get_weather_tool_definition()],
    template=template,
    system="You are a helpful assistant that provides accurate weather information."
)