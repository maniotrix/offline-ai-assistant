# Ollama Module for Karna

This module provides a clean, modern interface to the Ollama API for both text-only language models (LLMs) and vision language models (VLMs), with full support for tool calling capabilities.

## Overview

The Ollama module offers a streamlined way to interact with Ollama-hosted models, focusing on:

- Simple, consistent interfaces for both LLMs and VLMs
- Full support for tool calling in modern models
- Real-time streaming of responses
- Conversation history management
- Customizable parameters and templates

## Key Components

- **Base Client**: Foundation class that handles low-level communication with Ollama server
- **LLM Client**: Specialized client for text-only language models
- **VLM Client**: Specialized client for vision language models
- **Helper Functions**: High-level convenience functions for common operations
- **Utility Functions**: Shared utilities for image processing, parameter management, etc.
- **Tool Definitions**: Pre-defined tools like weather, search, and object identification

## Usage

This module exclusively uses the chat API endpoint from Ollama for all requests, providing a consistent interface for both streaming and non-streaming interactions.

See the detailed documentation in:
- `README_VLM_TOOLS.md` - For VLM and LLM tool calling capabilities
- Test files - For practical examples of usage

## Getting Started

```python
from ollama_helper import llm_generate, vlm_generate

# Text-only example
text_response = llm_generate(
    prompt="Explain quantum computing in simple terms",
    model="llama3.1"
)

# Vision example
vision_response = vlm_generate(
    prompt="What's in this image?",
    image_path="path/to/image.jpg",
    model="granite3.2-vision"
)

print(text_response["response"])
print(vision_response["response"])
```

## Tool Calling Example

```python
from ollama_helper import llm_generate, get_weather_tool_definition

response = llm_generate(
    prompt="What's the weather like in Paris?",
    model="llama3.1",
    tools=[get_weather_tool_definition()]
)

# Check for tool calls
if "tool_calls" in response:
    for tool_call in response["tool_calls"]:
        print(f"Tool called: {tool_call.get('function', {}).get('name')}")
```

## Requirements

- Python 3.7+
- An Ollama server (local or remote)
- Compatible Ollama models 