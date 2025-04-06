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