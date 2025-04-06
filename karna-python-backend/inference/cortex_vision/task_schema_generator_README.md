# Task Schema Generator

## Overview

The `TaskSchemaGenerator` is a tool that generates fully-specified task schema JSON files from simplified training JSONs. This makes it easier to create automation scripts for web applications by extracting UI elements from screenshots and mapping them to appropriate steps in the task sequence.

## How It Works

1. **Training File & Screenshot Events**: The system processes a simplified training JSON and matches it with screenshot events collected during user interaction.
2. **Two-Phase Processing**: Non-wait steps are processed first, matching them sequentially with screenshot events. Then, wait steps are processed with targets copied from referenced steps.
3. **OmniParser**: Screenshots are analyzed using OmniParser to detect UI elements (buttons, input fields, icons, etc.).
4. **Patch Extraction**: For mouse events, visual patches are extracted for the UI element at the clicked coordinates.
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
        {   "step_id": 4,
            "description": "Wait for the chatgpt to respond",
            "action_type": "wait",
            "action": "none",
            "import_target_from_step": 3
        },
        // Additional steps...
    ]
}
```

> **Important**: The number of non-wait steps in the training JSON must match the number of screenshot events.

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
python task_schema_generator.py training_json_path screenshot_events_json [--output-dir PATH] [--output-file PATH]
```

Example:
```bash
python task_schema_generator.py chat_with_chatgpt_steps_train.json screenshot_events_export.json --output-dir generated_output
```

## Generated Files

The generator creates the following output:

1. **Task Schema JSON**: A fully-specified task schema file.
2. **Patches Directory**: Contains extracted image patches for all UI elements at mouse click coordinates.

## Processing Logic

The generator processes steps in the following order:

1. **Step Categorization**: Steps are categorized into wait steps and non-wait steps.
2. **Validation**: Ensures the number of screenshot events matches the number of non-wait steps.
3. **Sequential Processing**: 
   - Non-wait steps are processed first, matched sequentially with screenshot events.
   - Wait steps are processed last, with targets copied from referenced steps.
4. **Recombination**: All steps are recombined in the original order based on step_id.

## Action Type Determination

Action types are determined based on the screenshot events:

| Event Contains | Action Type | Action | Target |
|----------------|-------------|--------|--------|
| Mouse coordinates | MOUSE_ACTION | "click" | Extracted from UI element at coordinates |
| Key press | KEYBOARD_ACTION | "paste" or "end" | None |
| Wait step in training | WAIT | "none" | Copied from referenced step |

## Target Extraction

For mouse events, the generator:
1. Finds the UI element containing the clicked coordinates
2. Extracts a visual patch of that element
3. Saves it with a clean filename (no special characters or double dots)
4. References it in the step's target field

## Advanced Features

### Output Directory Management

The output directory is automatically cleaned at initialization to ensure fresh results:

```python
# Will delete the directory if it exists before generating new output
generator = TaskSchemaGenerator(output_dir="my_custom_output_directory")
```

If not specified, a directory named `generated_{training_file_name}_{timestamp}` will be created.

### Wait Step Target References

Wait steps can reference targets from previously processed steps using the `import_target_from_step` field:

```json
{
    "step_id": 4,
    "description": "Wait for the chatgpt to respond",
    "action_type": "wait",
    "action": "none",
    "import_target_from_step": 3
}
```

This copies the target from step 3 to step 4, ensuring the wait step knows what UI element to watch for.

### Custom Processing

The generator allows for specifying action_type and action in the training JSON to override automatic determination:

```json
{
    "step_id": 3,
    "description": "Send the message",
    "action_type": "mouse_action",  // Override automatic determination
    "action": "click"               // Override automatic determination
}
``` 