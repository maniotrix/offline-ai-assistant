from enum import Enum

class CommandKeys(Enum):
    """
    Enum class for command keys used in the application.
    
    Attributes:
        USER_COMMAND (str): Key for user command.
        TASK_DOMAIN_ID (str): Key for task domain ID.
        NEW_KEY (str): Description of what the new key is used for.
    """
    USER_COMMAND = 'user-command'
    TASK_DOMAIN_ID = 'task-domain-id'
    # Add more keys as needed
    # Example: NEW_KEY = 'new-key'
