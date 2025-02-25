from domain.task import TaskContext, TaskStatus
from generated.command_pb2 import (
    CommandAction,
    CommandResult as ProtoCommandResult,
    CommandExecutionStatus
)
from domain.action import Action

@staticmethod
def task_status_to_proto(status: TaskStatus) -> CommandExecutionStatus.ValueType:
    """Convert domain TaskStatus to protobuf CommandExecutionStatus value"""
    return {
        TaskStatus.PENDING: CommandExecutionStatus.PENDING,
        TaskStatus.IN_PROGRESS: CommandExecutionStatus.IN_PROGRESS,
        TaskStatus.COMPLETED: CommandExecutionStatus.COMPLETED,
        TaskStatus.FAILED: CommandExecutionStatus.FAILED
    }.get(status, CommandExecutionStatus.FAILED)
    
@staticmethod
def action_to_proto(self, action: Action) -> CommandAction:
        """Convert domain Action to protobuf Action"""
        proto_action = CommandAction()
        proto_action.type = action.type
        if action.coordinates:
            proto_action.coordinates["x"] = str(action.coordinates.x)
            proto_action.coordinates["y"] = str(action.coordinates.y)
        if action.text:
            proto_action.text = action.text
        return proto_action

@staticmethod
def create_command_result(context: TaskContext) -> ProtoCommandResult:
    """Create protobuf CommandResult from TaskContext"""
    result = ProtoCommandResult()
    result.command_text = str(context.command) if context.command else ""
    result.status = CommandExecutionStatus.Value(task_status_to_proto(context.status))
    result.message = context.message or ""
    
    if hasattr(context, 'actions') and context.actions:
            for action in context.actions:
                proto_action = result.actions.add()
                proto_action.CopyFrom(action_to_proto(action))
    
    return result
    