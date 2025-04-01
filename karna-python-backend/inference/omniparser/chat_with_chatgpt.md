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
    // if we have info of a visual clue, no need to know about its text version or name
    // the state of screen can be also determined by just comparing and finding visual clues like icons or texts on screen , hence identifying visual changes jsut like human vision
    // need to better conceptualise this wait thing
    // clicking at any random point at any point and pressing end is not very visual way of doing it, its mostly traditional botting
        so when copy icon is there on screen for latest response, why are we clciking and pressing end unneccesarily?
        we should directly look for copy icon, and we keep track of copy icons programmatically?, no not visual way how humans do?
        need better approach, which is more visually aligned than hardcoding stuff
        // do we need to capture even when user is not triggering any events?
        // we should also capture the omniparser type and related patch for focusing in chat area, and find similar or related patches at runtime
        introduce this as fallback step rather than main step for copying new response
