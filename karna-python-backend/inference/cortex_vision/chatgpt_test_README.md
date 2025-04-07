# ChatGPT Web Interface Automation

## Overview

The `chatgpt_test.py` module provides a simple testing framework and command-line interface that enables interacting with ChatGPT's web interface programmatically through Python. It demonstrates how the `task_schema.py` framework can be used to automate browser interactions with AI systems, effectively turning a web-based ChatGPT interface into a programmable Vision-Language Model (VLM) API.

## Features

- **CLI Interface**: Interactive command-line interface for ChatGPT conversations
- **Image Upload Support**: Can upload images to ChatGPT, utilizing its VLM capabilities
- **Automated Browser Control**: Uses computer vision to locate and interact with UI elements
- **Response Capturing**: Automatically extracts ChatGPT's responses to the clipboard
- **Performance Measurement**: Tracks and displays response time metrics
- **Task Visualization**: Ability to visualize task execution steps with `show_tasks_viz`
- **Auto-Switching**: Automatically switches application focus after each response

## Scope Note: Selective Use of Vision Components - A Pragmatic Approach

It's important to understand that while Karna's `cortex_vision` module offers a rich suite of components designed to mimic human visual processing, this specific `chatgpt_test.py` example deliberately employs a focused subset. This is **not** skipping necessary work, but rather applying **appropriate, pragmatic scoping** for the task at hand.

**1. Task-Specific Minimalism:**
*   The core task—automating the ChatGPT web UI—follows a relatively linear and predictable sequence: find input -> paste -> click send -> wait -> find copy -> click copy -> read clipboard.
*   This specific flow primarily requires robust element localization and reliable action execution, not necessarily a deep, dynamic understanding of the entire visual scene at every moment.

**2. Sufficient Components Utilized:**
*   **`TaskExecutor` / `TaskSchema`:** Essential for defining the interaction sequence and orchestrating browser actions.
*   **`VerticalPatchMatcher` (used internally by `TaskExecutor`):** This is the key vision component leveraged here. It provides visually robust localization of critical UI elements (input field, buttons) using pre-defined image patches. This handles minor UI shifts better than brittle selectors and represents the core philosophy of visually grounded interaction.

**3. Justified Omission of Advanced Components (for *this* test):**
*   **`AttentionController`:** Dynamically modeling visual attention is overkill for finding a few specific, known elements in a relatively static layout. The `TaskSchema` itself provides enough attentional guidance (e.g., target location hints) for the `VerticalPatchMatcher`.
*   **`DynamicAreaDetector` / `ImageDiffCreator`:** While potentially useful for confirming response generation, simpler methods like `WaitStep` combined with patch matching for the 'Copy' button are sufficient and computationally cheaper for this script's goal.
*   **`Clustering`, other advanced detectors:** Unnecessary for locating the specific, predefined UI controls needed for this interaction.

**4. Performance Considerations:**
*   Integrating the full suite of vision components (attention, change detection) into every step would introduce significant computational overhead, slowing down this specific automation task unnecessarily.

**In Conclusion:** This script effectively demonstrates the core value proposition—automating UI interactions using `TaskSchema` and visually robust element finding (`VerticalPatchMatcher`)—without the performance cost or complexity of deploying the *entire* `cortex_vision` suite. The more advanced components remain available for integration into tasks that genuinely require their sophisticated capabilities, such as navigating highly dynamic interfaces or performing deeper scene analysis.

## Using Generated Task Schema

The module uses the task schema files created by the `TaskSchemaGenerator`:

1. **Loading Generated Schema**:
   - Automatically finds and loads JSON files ending with `_memory_generated.json` from the memory directory
   - Uses the corresponding patches directory for UI element matching
   - Integrates with the schema structure produced by the `TaskSchemaGenerator`

2. **Directory Structure**:
   ```
   generated_task_schema_sample_chatgpt/
   ├── chat_with_chatgpt_steps_train_memory_generated.json
   └── patches/
       ├── patch_step1.png
       ├── patch_step3.png
       └── ...
   ```

3. **Schema to Execution Pipeline**:
   ```
   TaskSchemaGenerator → Generated JSON + Patches → TaskPlanner → TaskExecutor → Browser Automation
   ```

## Technical Implementation

### Architecture

The implementation consists of several interconnected components:

1. **Task Definition**: Generated from training JSON files using `TaskSchemaGenerator`
2. **Task Executor**: The `TaskExecutor` class from `task_schema.py` handles browser automation
3. **Computer Vision**: Uses `VerticalPatchMatcher` and `Omniparser` to locate UI elements
4. **Clipboard Integration**: Uses `clipboard_utils.py` for data transfer between application and ChatGPT
5. **Output Control**: Advanced output suppression using context managers and stream redirection

### Process Flow

1. **Initialization**:
   - Loads the generated task schema from `*_memory_generated.json`
   - Creates a TaskPlanner with the patches directory path
   - Suppresses verbose logging output
   - Configures the CLI interface

2. **Conversation Loop**:
   - User enters a question or prompt through the command-line
   - Text is transferred to the clipboard
   - (Optional) Images from a specified directory can be included with VLM mode

3. **Web Automation Steps**:
   - Executes each step defined in the task schema
   - Uses visual pattern matching to locate UI elements
   - Performs clicks, pastes, and waits as defined in the schema
   - Captures the response through clipboard operations

4. **Response Processing**:
   - Captures response from clipboard using `get_clipboard_text()`
   - Displays formatted output in the terminal with ANSI color formatting
   - Records and displays timing information
   - Automatically switches application focus back using Alt+Tab
   - Prepares for next interaction

### Technical Details

#### VLM Mode Configuration

The system provides a dedicated VLM (Vision-Language Model) mode:

```python
# Enable VLM mode
use_as_vlm = True
directory_path = os.path.join(current_dir, "test_chatgpt_upload_dir")

# First question will upload both text and images
if question_count == 1 and use_as_vlm:
    task_executor.set_clipboard(user_question, directory_path)
```

- **Single-Shot Use**: By default, VLM operations work for the first question only
- **Directory Control**: Images are loaded from a configurable directory path
- **Automatic Upload**: Images are automatically transferred to ChatGPT with the first query

#### Task Visualization

The system can visualize task execution for debugging and demonstration:

```python
# Enable task visualization
show_tasks_viz = True

# After first question, visualize the task execution
if question_count == 1 and show_tasks_viz:
    task_executor.task_log.visualize_task_log()
    break
```

- **Visual Analysis**: Creates a visual representation of each step execution
- **Development Aid**: Helps understand and debug task execution flow
- **Session Limiting**: Can automatically exit after first query for demonstration purposes

#### Output Suppression System

The module implements a comprehensive output control system:

```python
# Context manager for output suppression
@contextlib.contextmanager
def suppress_output():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# Selective use in code
with suppress_output():
    task_executor.execute_task()
```

- **Granular Control**: Suppresses output only for specific operations
- **Stream Capture**: Uses StringIO to capture and discard unwanted output
- **Clean Interface**: Maintains a professional CLI experience without technical noise

#### Computer Vision Integration

The system uses a sophisticated computer vision pipeline to identify UI elements:

- **Pattern Matching**: Image-based pattern matching to locate buttons and input fields
- **Element Identification**: Uses patch images from the generated task schema
- **Attention Mechanisms**: Implements screen area focus strategies (top, bottom, center) for more efficient element detection

#### Clipboard Management

The system uses clipboard as the primary data transfer mechanism:

- **Text Transfer**: Uses `pyperclip` for cross-platform clipboard text operations
- **File Transfer**: Uses PowerShell scripts for clipboard file operations on Windows
- **Response Extraction**: Captures ChatGPT's response by programmatically clicking the "copy" button and reading clipboard contents

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
- **Testing Framework**: Compare responses across different versions

## Technical Insights

### Behind the Scenes

The system works through several key innovations:

1. **Declarative Automation**: The task schema describes "what" to do, not "how" to do it
2. **Visual Element Recognition**: Instead of relying on CSS selectors or XPaths which can change, the system recognizes UI elements visually
3. **Human-Like Interaction**: The mouse movements and interactions simulate human behavior to prevent detection as automation
4. **Error Resilience**: The wait steps ensure the system adapts to variable network conditions and response times
5. **App Switching**: Automatically returns focus to the terminal after interaction via Alt+Tab

### Limitations and Considerations

- **Browser Dependencies**: Requires Chrome browser with specific configuration
- **Visual Changes**: UI updates to ChatGPT may require regenerating the task schema with TaskSchemaGenerator
- **Theme Sensitivity:** The visual recognition relies on patch matching. Accuracy may decrease significantly if the task schema was generated (trained) on one UI theme (e.g., light mode) and executed on a different theme (e.g., dark mode). For best results, regenerate the task schema using screenshots from the target theme if issues occur. Tested and chatted perefectly for more than 1 hour on light theme without any issues.
- **Error Handling:** The script assumes a smooth interaction flow. It does not currently handle unexpected interruptions like CAPTCHA checks (e.g., "Cloudflare verify you are human"), network errors prompting a retry, or other conversational UI pop-ups/errors that might appear on the ChatGPT website. Such events will likely cause the automation to fail. Future versions aim to incorporate more robust error handling and performance optimizations.
- **Performance Overhead**: Vision-based detection is more resource-intensive than traditional web automation
- **Platform Specificity**: Some operations (particularly file clipboard operations) are Windows-specific

## Usage Example

Running the script provides an interactive interface:

```
$ python chatgpt_test.py

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

1. Edit these variables in the code:
   ```python
   use_as_vlm = True  # Enable VLM mode
   show_tasks_viz = True  # Enable task visualization (optional)
   directory_path = "path/to/your/images"  # Set your image directory
   ```

2. The first question will upload both your text and images
3. Subsequent questions will only use text unless you modify the code
4. Set `show_tasks_viz = False` to continue conversation after the first query

## Configuration Options

The following configuration options can be adjusted in the code:

| Variable | Default | Description |
|----------|---------|-------------|
| `use_as_vlm` | `True` | Enables image upload for first question |
| `show_tasks_viz` | `True` | Visualizes task execution and exits after first question |
| `directory_path` | `test_chatgpt_upload_dir` | Directory containing images to upload |
| `memory_dir` | `generated_task_schema_sample_chatgpt` | Directory for task schema files |

## Creating Your Own Task Schema

To create your own task schema for automating ChatGPT or other web interfaces:

1. Use `TaskSchemaGenerator` to create a task schema from training JSON and screenshot events
2. Store the generated files in a directory structure as described above
3. Update the `memory_dir` path in the code to point to your generated schema
4. Run the script to use your custom automation

## Conclusion

This module demonstrates how traditional web UI automation can be transformed into a sophisticated AI integration tool through computer vision and careful orchestration of browser interactions. By treating web interfaces as APIs, it opens up new possibilities for programmatic interaction with systems that may not provide official API access or where the web interface offers unique capabilities.

The approach showcased here represents a bridge between conventional UI automation and modern AI systems, enabling developers to combine the strengths of both paradigms. 