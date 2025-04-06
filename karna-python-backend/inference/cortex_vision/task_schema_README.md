# Task Schema Module

## Overview

The `task_schema.py` module provides a robust framework for defining, planning, and executing automated UI tasks using computer vision. This module enables programmatic interaction with web applications by simulating human-like mouse movements and keyboard inputs based on visual recognition of UI elements.

## Core Components

### Schema Classes

#### Task Definition

- `Task`: The top-level container for a complete automation task
  - Manages a sequence of steps to be executed
  - Handles serialization and deserialization of task definitions
  - Provides utility methods to filter steps by type

- `Step`: Base class for all task step types
  - Contains core properties like step_id, description, action_type, and action
  - Uses Pydantic for validation and serialization

- Step Types:
  - `MouseStep`: Actions involving mouse interactions (clicks)
  - `KeyboardActionStep`: Keyboard input actions (typing, shortcuts)
  - `WaitStep`: Conditional waiting for UI elements to appear
  - `StepWithTarget`: Abstract base class for steps with UI element targets

#### Target Definition

- `Target`: Defines a target UI element to interact with
  - Contains a type (from ScreenObjectType) and optional value (text or image path)

- `ScreenObjectType`: Enum defining types of UI elements
  - `BOX_YOLO_CONTENT_OCR`: Elements detected via YOLO and OCR
  - `BOX_OCR_CONTENT_OCR`: Elements detected via OCR only
  - `BOX_YOLO_CONTENT_YOLO`: Elements detected via YOLO only
  - `NONE`: No specific target (e.g., for center-of-screen actions)

- `Attention`: Enum defining focus points for interaction
  - Values: TOP, BOTTOM, LEFT, RIGHT, CENTER

- `ActionType`: Enum for step action categories
  - Values: MOUSE_ACTION, KEYBOARD_ACTION, WAIT

### Execution Classes

- `TaskPlanner`: Manages the task definition and planning
  - Wrapper for a task schema to use with execution

- `TaskExecutor`: Executes tasks by performing the defined steps
  - Takes screenshots of the application
  - Processes them with Omniparser for element detection
  - Matches target elements using visual pattern matching
  - Performs specified actions at the correct screen locations
  - Logs execution for later analysis

- `TaskLog`: Records execution history and results
  - Tracks steps, screenshots, matches, and outcomes
  - Provides visualization for debugging

- `Clipboard`: Manages clipboard content for copy/paste operations
  - Handles both text and file content

## Key Features

- **Computer Vision-based Element Detection**: Locates UI elements through visual pattern matching using Omniparser
- **Human-like Interaction**: Simulates natural mouse movements with random micro-adjustments, hesitations, and corrections
- **Multi-step Execution Flow**: Handles sequences of interdependent actions with conditional waiting
- **Task Logging and Visualization**: Records step outcomes for debugging with visual representations
- **Robust Error Handling**: Manages timeouts and handling of missing elements

## Usage

```python
# 1. Define a task with steps
task = Task(
    task="Login to application",
    description="Automate login process",
    app_name="MyApp",
    app_type="web",
    app_url="https://example.com/login",
    steps=[
        # Wait for login form
        WaitStep(
            step_id=1,
            description="Wait for login form",
            action="wait",
            attention=Attention.CENTER,
            target=Target(
                type=ScreenObjectType.BOX_YOLO_CONTENT_OCR,
                value="patches/login_form.png"
            )
        ),
        # Click username field
        MouseStep(
            step_id=2,
            description="Click username field",
            action="click",
            attention=Attention.CENTER,
            target=Target(
                type=ScreenObjectType.BOX_YOLO_CONTENT_OCR,
                value="patches/username_field.png"
            )
        ),
        # Type username via clipboard
        KeyboardActionStep(
            step_id=3,
            description="Enter username",
            action="paste",
            attention=Attention.CENTER
        )
    ]
)

# 2. Create task planner and executor
planner = TaskPlanner(task)
executor = TaskExecutor(planner)

# 3. Set clipboard content for paste operations
executor.set_clipboard("test@example.com")

# 4. Prepare and execute the task
executor.prepare_for_task()
executor.execute_task()

# 5. View execution logs
executor.task_log.visualize_task_log()
```

## Technical Details

### Pattern Matching

The module uses a `VerticalPatchMatcher` to find UI elements by matching image patterns:
- Takes a target image (patch) and compares it to elements detected by Omniparser
- Calculates similarity scores to identify the best matching element
- Returns match information including bounding box coordinates for interaction

### Human-like Interaction

Mouse movements use a custom tween function that introduces:
- Natural acceleration and deceleration curves
- Random micro-adjustments to movement paths
- Occasional hesitations
- Realistic overshooting and correction behavior

### Viewport Management

Tasks are executed within a defined viewport region:
- Default viewport is configured as a region of the screen
- Custom viewports can be set via `set_viewport()`
- Screenshots and coordinate calculations are viewport-relative

## Dependencies

- **Pydantic**: Schema validation
- **PIL/Pillow**: Image processing
- **PyAutoGUI**: Mouse/keyboard control
- **NumPy**: Array operations
- **Matplotlib**: Visualization
- **ChromeRobot**: Browser automation
- **Omniparser**: Computer vision for UI element detection

## Notes

- The system requires screen capture capabilities and UI control permissions
- For reliable operation, ensure target images closely match what will appear on screen
- Human-like interaction parameters can be tuned in the `human_like_tween` function

# Task Schema Generator

## Overview

The `TaskSchemaGenerator` is a tool that generates fully-specified task schema JSON files from simplified training JSONs. This makes it easier to create automation scripts for web applications by extracting UI elements from screenshots and mapping them to appropriate target elements in the task steps.

## How It Works

1. **Screenshot Events**: The system first processes a series of screenshots collected during user interaction with an application.
2. **OmniParser**: Each screenshot is analyzed using OmniParser to detect UI elements (buttons, input fields, icons, etc.).
3. **Patch Extraction**: Visual patches are extracted for each detected UI element and saved as image files.
4. **Target Mapping**: Step descriptions in the training JSON are mapped to appropriate UI elements using content and visual matching.
5. **Schema Generation**: A fully-specified task schema is generated with proper action types, targets, and other required fields.

## Usage

### Step 1: Record User Interaction

Use the `ScreenCaptureService` to record user interaction with an application. This will create a series of screenshots and export them as a JSON file.

### Step 2: Create a Training JSON

Create a simplified training JSON with step descriptions. For example:

```json
{
    "task": "Send message and copy latest response",
    "description": "This task is to send a message to the chatgpt and copy the latest response",
    "app_name": "chatgpt",
    "app_type": "web",
    "default_attention": "bottom",
    "app_url": "https://chatgpt.com/?temporary-chat=true",
    "steps": [
        {   "step_id": 1,
            "description": "Click on the chatgpt input box"
        },
        {   "step_id": 2,
            "description": "Paste the message to the chatgpt input box"
        },
        {   "step_id": 3,
            "description": "Send the message to the chatgpt",
            "keyboard_shortcut": "enter"
        },
        // Additional steps...
    ]
}
```

### Step 3: Generate the Task Schema

Use the `TaskSchemaGenerator` to process the training JSON and screenshot events:

```python
from inference.cortex_vision.task_schema_generator import TaskSchemaGenerator

# Create generator instance with output directory
generator = TaskSchemaGenerator(output_dir="generated_task_output")

# Generate task schema
output_file = generator.generate_task_schema(
    training_json_path="chat_with_chatgpt_steps_train.json",
    screenshot_events_json="screenshot_events_export.json"
)

print(f"Generated task schema: {output_file}")
```

### Step 4: Use the Generated Schema

The generated task schema can now be used with `TaskExecutor` to automate the application interaction:

```python
from inference.cortex_vision.task_schema import load_task_schema_from_json, TaskPlanner
from inference.cortex_vision.task_schema import TaskExecutor

# Load the generated task schema
task_schema = load_task_schema_from_json(output_file)
task_planner = TaskPlanner(task_schema)

# Create and execute the task
task_executor = TaskExecutor(task_planner)
task_executor.execute_task()
```

## Command Line Usage

You can also use the `TaskSchemaGenerator` from the command line:

```bash
python task_schema_generator_test.py example
```

Or to run unit tests:

```bash
python task_schema_generator_test.py
```

## Generated Files

The generator creates the following output:

1. **Task Schema JSON**: A fully-specified task schema file.
2. **Patches Directory**: Contains extracted image patches for all UI elements.

## Step Types and Action Types

The generator automatically infers the appropriate step types and action types based on step descriptions:

| Description Contains | Action Type | Action | Target Type |
|---------------------|-------------|--------|------------|
| "click" | MOUSE_ACTION | "click" | Based on content |
| "paste" | KEYBOARD_ACTION | "paste" | None |
| "scroll" or "end" | KEYBOARD_ACTION | "end" | None |
| "wait" | WAIT | "none" | Based on referenced step |

## Target Mapping Rules

The generator uses the following rules to map step descriptions to targets:

- "input box" descriptions -> Input fields (type BOX_YOLO_CONTENT_OCR)
- "copy icon" descriptions -> Copy buttons (type BOX_YOLO_CONTENT_YOLO)
- "send" descriptions -> Send buttons (type BOX_YOLO_CONTENT_YOLO)
- Center clicks -> No specific target (type NONE)

## Advanced Features

### Import Targets from Other Steps

You can reference targets from previous steps using the `import_target_from_step` field:

```json
{
    "step_id": 4,
    "description": "Wait for the chatgpt to respond",
    "action_type": "wait",
    "action": "none",
    "import_target_from_step": 3,
    "attention": "center"
}
```

### Custom Output Directory

Specify a custom output directory when creating the generator:

```python
generator = TaskSchemaGenerator(output_dir="my_custom_output_directory")
```

If not specified, a directory named `generated_{training_file_name}_{timestamp}` will be created. 