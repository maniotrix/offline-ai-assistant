from robot.utils import open_chrome_maximized_then_navigate


def test_open_chrome_and_navigate_to_google():
    """
    Test that we can open Chrome and navigate to Google.
    This is a direct test of the function used in the main block.
    """
    # Test the same functionality as in the __main__ block
    open_chrome_maximized_then_navigate("https://www.google.com")

