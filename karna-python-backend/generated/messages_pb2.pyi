"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _TaskStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _TaskStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TaskStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PENDING: _TaskStatus.ValueType  # 0
    IN_PROGRESS: _TaskStatus.ValueType  # 1
    COMPLETED: _TaskStatus.ValueType  # 2
    FAILED: _TaskStatus.ValueType  # 3

class TaskStatus(_TaskStatus, metaclass=_TaskStatusEnumTypeWrapper): ...

PENDING: TaskStatus.ValueType  # 0
IN_PROGRESS: TaskStatus.ValueType  # 1
COMPLETED: TaskStatus.ValueType  # 2
FAILED: TaskStatus.ValueType  # 3
global___TaskStatus = TaskStatus

@typing.final
class RPCRequest(google.protobuf.message.Message):
    """Request message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EXECUTE_COMMAND_FIELD_NUMBER: builtins.int
    GET_STATUS_FIELD_NUMBER: builtins.int
    @property
    def execute_command(self) -> global___CommandRequest: ...
    @property
    def get_status(self) -> global___StatusRequest: ...
    def __init__(
        self,
        *,
        execute_command: global___CommandRequest | None = ...,
        get_status: global___StatusRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["execute_command", b"execute_command", "get_status", b"get_status", "method", b"method"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["execute_command", b"execute_command", "get_status", b"get_status", "method", b"method"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["method", b"method"]) -> typing.Literal["execute_command", "get_status"] | None: ...

global___RPCRequest = RPCRequest

@typing.final
class CommandRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMAND_FIELD_NUMBER: builtins.int
    DOMAIN_FIELD_NUMBER: builtins.int
    command: builtins.str
    domain: builtins.str
    def __init__(
        self,
        *,
        command: builtins.str = ...,
        domain: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command", b"command", "domain", b"domain"]) -> None: ...

global___CommandRequest = CommandRequest

@typing.final
class StatusRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StatusRequest = StatusRequest

@typing.final
class RPCResponse(google.protobuf.message.Message):
    """Response message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMAND_RESPONSE_FIELD_NUMBER: builtins.int
    STATUS_UPDATE_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    error: builtins.str
    @property
    def command_response(self) -> global___CommandResult: ...
    @property
    def status_update(self) -> global___Status: ...
    def __init__(
        self,
        *,
        command_response: global___CommandResult | None = ...,
        status_update: global___Status | None = ...,
        error: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["command_response", b"command_response", "error", b"error", "status_update", b"status_update", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["command_response", b"command_response", "error", b"error", "status_update", b"status_update", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["type", b"type"]) -> typing.Literal["command_response", "status_update", "error"] | None: ...

global___RPCResponse = RPCResponse

@typing.final
class CommandResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMAND_TEXT_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    ACTIONS_FIELD_NUMBER: builtins.int
    command_text: builtins.str
    status: global___TaskStatus.ValueType
    message: builtins.str
    @property
    def actions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Action]: ...
    def __init__(
        self,
        *,
        command_text: builtins.str = ...,
        status: global___TaskStatus.ValueType = ...,
        message: builtins.str = ...,
        actions: collections.abc.Iterable[global___Action] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["actions", b"actions", "command_text", b"command_text", "message", b"message", "status", b"status"]) -> None: ...

global___CommandResult = CommandResult

@typing.final
class Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VISION_FIELD_NUMBER: builtins.int
    LANGUAGE_FIELD_NUMBER: builtins.int
    COMMAND_FIELD_NUMBER: builtins.int
    vision: builtins.str
    language: builtins.str
    command: builtins.str
    def __init__(
        self,
        *,
        vision: builtins.str = ...,
        language: builtins.str = ...,
        command: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command", b"command", "language", b"language", "vision", b"vision"]) -> None: ...

global___Status = Status

@typing.final
class Action(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class CoordinatesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    TYPE_FIELD_NUMBER: builtins.int
    COORDINATES_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    type: builtins.str
    text: builtins.str
    @property
    def coordinates(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        type: builtins.str = ...,
        coordinates: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        text: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["_text", b"_text", "text", b"text"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["_text", b"_text", "coordinates", b"coordinates", "text", b"text", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["_text", b"_text"]) -> typing.Literal["text"] | None: ...

global___Action = Action
