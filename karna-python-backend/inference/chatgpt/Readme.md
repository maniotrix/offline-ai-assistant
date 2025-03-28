#### how to check if an assistant reponse is available and copy to clip board
1. On start of conversation, we capture the image of and location of send button
2. After sending message, after each 5 seconds, we keep checking if the image restored to same image captured on step 1.
3.After that trigger a click event to focus in the conversation area/list.
4. Then we triggere keyboard end key event
5. At this step we again, take a screenshot of the screen, and try to find the last/latest
   response.
   find the feedback options, copy icons etc. below assitant reponse
   while loop: hover mouse over each icon, starting from left icon
            at this point, take screenshot and capture mouse coords
            use ocr to see if icon has copy tooltip
            if yes, trigger left click to copy to clipboard


# lets use attentation mechanism which decides which cluster to focus by vision agent and keep its attention on
# browsers/chatgpt supports only file per paste event from clipoard at a time