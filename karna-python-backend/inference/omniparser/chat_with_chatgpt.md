    {
    "task": "Send message and copy latest response",
    "description": "This task is to send a message to the chatgpt and copy the latest response",
    "app_name": "chatgpt",
    "app_type": "web",
    "app_url": "https://chatgpt.com/?temporary-chat=true",
    "steps": [
        {
            "action_type": "mouse_action",
            "action": "click",
            "target_type": "ocr"
        },
        {
            "action_type": "keyboard_action",
            "action": "paste"
        },
        {
            "action_type": "mouse_action",
            "action": "click",
            "target_type": "icon"
        },
        {
            "action_type": "wait"
        },
        {
            "action_type": "mouse_action",
            "action": "click",
            "target_type": "none"
        },
        {
            "action_type": "keyboard_action",
            "action": "end"
        },
        {
            "action_type": "mouse_action",
            "action": "click",
            "target_type": "icon",
            "is_target_repeated": true,
            "target_repeated_layout_type": "vertical",
            "is_target_repeated_layout_index_fixed": true,
            "target_repeated_layout_index": -1
        }
    ]
    }
    // no of steps with mouse action should be equal to mouse events in json imported screenshot events
    // for validation step, we need to check if the image patch required in next step is present on the screen
    // target is not present in steps, calculated at runtime
    // keyboard actions do not have target type
    // Target object type should be only defined in json file,if the step is taking any action on the screen.
    Here just like clicks and key press, wait is also an event.
