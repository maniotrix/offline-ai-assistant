"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class StatusRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StatusRequest = StatusRequest

@typing.final
class StatusRPCRequest(google.protobuf.message.Message):
    """Request message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GET_STATUS_FIELD_NUMBER: builtins.int
    @property
    def get_status(self) -> global___StatusRequest: ...
    def __init__(
        self,
        *,
        get_status: global___StatusRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["get_status", b"get_status", "method", b"method"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["get_status", b"get_status", "method", b"method"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["method", b"method"]) -> typing.Literal["get_status"] | None: ...

global___StatusRPCRequest = StatusRPCRequest

@typing.final
class StatusResult(google.protobuf.message.Message):
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

global___StatusResult = StatusResult

@typing.final
class StatusRPCResponse(google.protobuf.message.Message):
    """Response message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STATUS_UPDATE_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    error: builtins.str
    @property
    def status_update(self) -> global___StatusResult: ...
    def __init__(
        self,
        *,
        status_update: global___StatusResult | None = ...,
        error: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["error", b"error", "status_update", b"status_update", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["error", b"error", "status_update", b"status_update", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["type", b"type"]) -> typing.Literal["status_update", "error"] | None: ...

global___StatusRPCResponse = StatusRPCResponse
