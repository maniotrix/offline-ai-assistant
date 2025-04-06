# ChatGPT Web Interface Automation

## Overview

The `chatgpt_test.py` module provides a powerful testing framework and command-line interface that enables interacting with ChatGPT's web interface programmatically through Python. It demonstrates how the `task_schema.py` framework can be used to automate browser interactions with AI systems, effectively turning a web-based ChatGPT interface into a programmable Vision-Language Model (VLM) API.

## Features

- **CLI Interface**: Interactive command-line interface for ChatGPT conversations
- **Image Upload Support**: Can upload images to ChatGPT, utilizing its VLM capabilities
- **Automated Browser Control**: Uses computer vision to locate and interact with UI elements
- **Response Capturing**: Automatically extracts ChatGPT's responses to the clipboard
- **Performance Measurement**: Tracks and displays response time metrics

## Technical Implementation

### Architecture

The implementation consists of several interconnected components:

1. **Task Definition**: The `chat_with_chatgpt.json` file defines the UI automation steps
2. **Task Executor**: The `TaskExecutor` class from `task_schema.py` handles browser automation
3. **Computer Vision**: Uses `VerticalPatchMatcher` and `Omniparser` to locate UI elements
4. **Clipboard Integration**: Uses `clipboard_utils.py` for data transfer between application and ChatGPT

### Process Flow

1. **Initialization**:
   - Loads the task schema from `chat_with_chatgpt.json`
   - Creates a TaskPlanner and TaskExecutor
   - Suppresses verbose logging output
   - Configures the CLI interface

2. **Conversation Loop**:
   - User enters a question or prompt through the command-line
   - Text is transferred to the clipboard
   - (Optional) Images from a specified directory can be included

3. **Web Automation Steps**:
   - Step 1: Click on ChatGPT input box (locates using image matching)
   - Step 2: Paste the user's question (from clipboard)
   - Step 3: Send the message (clicks enter or submit button)
   - Step 4: Wait for ChatGPT to respond (detects UI changes)
   - Step 5: Click at center of screen (to ensure focus)
   - Step 6: Scroll to end (to see complete response)
   - Step 7: Click copy button (to extract the response)

4. **Response Processing**:
   - Captures response from clipboard
   - Displays formatted output in the terminal
   - Records timing information
   - Prepares for next interaction

### Technical Details

#### Computer Vision Integration

The system uses a sophisticated computer vision pipeline to identify UI elements:

- **Pattern Matching**: Image-based pattern matching to locate buttons and input fields
- **Element Identification**: Uses reference images (`10_AAsk_anything.png`, `38_Up_or_down.png`, `44_Copy.png`) to identify interactive elements
- **Attention Mechanisms**: Implements screen area focus strategies (top, bottom, center) for more efficient element detection

#### Clipboard Management

The system uses clipboard as the primary data transfer mechanism:

- **Text Transfer**: Uses `pyperclip` for cross-platform clipboard text operations
- **File Transfer**: Uses PowerShell scripts (`copy_files_to_clipboard.ps1`) for clipboard file operations on Windows
- **Response Extraction**: Captures ChatGPT's response by programmatically clicking the "copy" button and reading clipboard contents

#### Output Suppression

The module implements sophisticated output control mechanisms:

- **Context Manager**: Uses a custom `suppress_output` context manager to temporarily redirect stdout/stderr
- **ANSI Formatting**: Implements colorized terminal output for better user experience
- **Selective Logging**: Suppresses all but critical log messages to maintain a clean interface

## Practical Applications

### Use as a VLM

This approach turns ChatGPT's web interface into a programmable VLM by:

1. **Enabling Image Analysis**: You can upload images to ChatGPT for analysis, description, or OCR
2. **Maintaining Conversation Context**: The browser session maintains context between interactions
3. **Bypassing API Limitations**: Access to features that might not be available in the official API
4. **Cost Efficiency**: Utilizing existing ChatGPT subscriptions rather than paying for API calls

### Integration Possibilities

This framework can be extended to:

- **Batch Processing**: Automate multiple queries with different images
- **Data Collection**: Create datasets of AI responses to specific inputs
- **Multimodal Applications**: Build applications that leverage ChatGPT's vision capabilities
- **Testing Framework**: Compare responses across different inputs or versions

## Technical Insights

### Behind the Scenes

The system works through several key innovations:

1. **Declarative Automation**: The task schema describes "what" to do, not "how" to do it
2. **Visual Element Recognition**: Instead of relying on CSS selectors or XPaths which can change, the system recognizes UI elements visually
3. **Human-Like Interaction**: The mouse movements and interactions simulate human behavior to prevent detection as automation
4. **Error Resilience**: The wait steps ensure the system adapts to variable network conditions and response times

### Limitations and Considerations

- **Browser Dependencies**: Requires Chrome browser with specific configuration
- **Visual Changes**: UI updates to ChatGPT may require updating the reference images
- **Performance Overhead**: Vision-based detection is more resource-intensive than traditional web automation
- **Platform Specificity**: Some operations (particularly file clipboard operations) are Windows-specific

## Usage Example

Running the script provides an interactive interface:

```
$ python task_schema_test.py

╔═══════════════════════════════════════════════════════════╗
║                   KARNA CHATGPT INTERFACE                  ║
╚═══════════════════════════════════════════════════════════╝

• Type 'exit' or 'quit' to end the conversation

╭─────────────────────────────────────────────────────────────╮
│ Enter your question: What is the capital of France?
╰─────────────────────────────────────────────────────────────╯

Asking and Waiting for ChatGPT...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ CONVERSATION #1 - 2023-04-06 08:20:15 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🙋 YOU ASKED:
What is the capital of France?

🤖 CHATGPT RESPONSE (took 2.34s):
The capital of France is Paris.
─────────────────────────────────────────────────────────────
```

## Developer Notes

To use ChatGPT as a Vision-Language Model:

1. Set `use_as_vlm = True` at line 79
2. Set `directory_path` to point to your images folder
3. The first question will upload both your text and images

## Conclusion

This module demonstrates how traditional web UI automation can be transformed into a sophisticated AI integration tool through computer vision and careful orchestration of browser interactions. By treating web interfaces as APIs, it opens up new possibilities for programmatic interaction with systems that may not provide official API access or where the web interface offers unique capabilities.

The approach showcased here represents a bridge between conventional UI automation and modern AI systems, enabling developers to combine the strengths of both paradigms. 