<!-- markdownlint-disable -->
## Layout Guide:
#### Description
The Chatgpt has 3 top-level clusters.
Header- Top
Left Sidebar- Left
Main Area - Right of Left Sidebar and below Header.

Header contains three required buttons:
    1. Show/Hide Left Sidebar button
    2. DropDown Model Selection Button
    3. Enable/Disable Temporary Chat Button

Main Area:
    1. A list of alternate user message and assistant messages with different background for each message
        1. All user messages are right aligned
        1. All assitant responses are left aligned and have copy buttton just below response. If not found, users can focus by mouse click or mouse hover over a assistant response to show these buttons.
    2. User Message Controls which contains input area, send button, and a button to attach files

Anti-bot Controls: The App also use cloudfare verification at any point of time during conversation, at this point the display screen with text like verify you are human.

#### Required UI Structure:
```
App layout-vertical
    header layout - horizontal type- container[] persistent- yes position-0
        container name-left_sidebar_controls layout - horizontal type- icon_button[] persistent- yes position- 0
            component type- icon_button tooltip- show/hide_left_side_bar position-0
            component type- icon_button tooltip - "new chat" position-1


        container type- dropdown name- model_selection persistent-yes layout-vertical position-1
            component type-dropdown_text_button default_text= "ChatGPT {model_name}" shows/hides_menu- yes position-0// assumes by default menu is hidden
            container name-model_selection_menu type-menu_container position-2 layout-vertical
                    list(component type- menu_text_button_item position-list_index
                        model_names- ["ChatGPT Plus", "ChatGPT", "GPT-4o"]) list_persistent- no

        component type-icon_text_button default_text= "Temporary" position-2
        component type- icon_button tooltip - "" position-3

    main_area layout-vertical persistent-yes type-container[] position-1
        container name-chat_list_area layout-vertical position-0 type- custom_objects.user_assistant_container[] list-dynamic
        container name-chat_controls_area layout-vertical position-1
            component type-text_input default_text-"Ask anything" position-0
            component type-double_click-icon button tooltip-"Upload files and more" position-1


    custom_objects
        user_container
            component type-text
        assistant_container
            container layout-vertical
                component type-text
                container layout-horizontal
                    component type- icon_button tooltip - "copy" position-0
        user_assistant_container
            container type-user_container position-0
            container type-assistant_container position-1
```

#### Task and related steps perormed by user in provided screenshots as single stitched file
Note: Screenshots may not be provided for some steps which does not involve user interaction with the app or using keyboard shortcut to interact with the app or screenshot is renundant to process.
Task - Send one or more messages and copy latest response of assistant
    Steps:
    1. close left side bar if open, screenshot index - 1, mouse coords- {}
    2. Choose model, screenshot index - 2, mouse coords- {}
    3. Activate temporary chat button, screenshot index - 3, mouse coords- {}
    4. Focus into the user message controls input area, screenshot index - 4, mouse coords- {}
    5. Paste latest clipboard content - using keyboard shortcut, screenshot index - None, keys - ctrl+v
    6. Send user message by pressing enter, screenshot index - None, keys - Enter
    7. Check every five seconds if send button icon restored to initial state before step 3, screenshot index - None
    8. focus inside user and assistant messages area, screenshot index - 5, mouse coords- {}
    9. Scroll to end of chat area, screenshot index - None, keys - End
    10. Locate and click the latest assistant reponse, screenshot index - None
    11. Locate copy button below assistant response, screenshot index - None
    12. Click copy button to copy assistant response to clipboard, screenshot index - 6, mouse coords- {}



        