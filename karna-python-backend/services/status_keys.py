from enum import Enum

class StatusKeys(Enum):
    """
    Enum class for status keys used in the application.
    
    Attributes:
        OPERATION (str): Key for operation type
        STATUS (str): Key for status state
        MESSAGE (str): Key for status message
        PROGRESS (str): Key for progress value
        RESULT (str): Key for result data
        ACTIONS_EXECUTED (str): Key for executed actions
    """
    OPERATION = 'operation'
    STATUS = 'status'
    MESSAGE = 'message'
    PROGRESS = 'progress'
    RESULT = 'result'
    ACTIONS_EXECUTED = 'actions_executed'

class StatusStates(Enum):
    """
    Enum class for possible status states.
    """
    IDLE = 'idle'
    RUNNING = 'running'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    ERROR = 'error'

class OperationTypes(Enum):
    """
    Enum class for operation types.
    """
    COMMAND_EXECUTION = 'command_execution'