from enum import Enum

class CommandKeys(Enum):
    """
    Enum class for command keys used in the application.
    
    Attributes:
        USER_COMMAND (str): Key for user command.
        TASK_DOMAIN_ID (str): Key for task domain ID.
        IS_IN_CACHE (str): Key for checking if the command is in cache.
        UUID (str): Key for unique ID.
    """
    USER_COMMAND = 'user-command'
    TASK_DOMAIN_ID = 'task-domain-id'
    IS_IN_CACHE = "is-in-cache"
    UUID = 'unique-id'
    # Add more keys as needed
    # Example: NEW_KEY = 'new-key'
