"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CaptureRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    project_uuid: builtins.str
    command_uuid: builtins.str
    def __init__(
        self,
        *,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "project_uuid", b"project_uuid"]) -> None: ...

global___CaptureRequest = CaptureRequest

@typing.final
class CaptureCacheRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    project_uuid: builtins.str
    command_uuid: builtins.str
    def __init__(
        self,
        *,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "project_uuid", b"project_uuid"]) -> None: ...

global___CaptureCacheRequest = CaptureCacheRequest

@typing.final
class CaptureUpdateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    SCREENSHOT_EVENTS_FIELD_NUMBER: builtins.int
    project_uuid: builtins.str
    command_uuid: builtins.str
    message: builtins.str
    @property
    def screenshot_events(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RpcScreenshotEvent]: ...
    def __init__(
        self,
        *,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
        message: builtins.str = ...,
        screenshot_events: collections.abc.Iterable[global___RpcScreenshotEvent] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "message", b"message", "project_uuid", b"project_uuid", "screenshot_events", b"screenshot_events"]) -> None: ...

global___CaptureUpdateRequest = CaptureUpdateRequest

@typing.final
class ScreenCaptureRPCRequest(google.protobuf.message.Message):
    """Request message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    START_CAPTURE_FIELD_NUMBER: builtins.int
    STOP_CAPTURE_FIELD_NUMBER: builtins.int
    UPDATE_CAPTURE_FIELD_NUMBER: builtins.int
    GET_CACHE_FIELD_NUMBER: builtins.int
    @property
    def start_capture(self) -> global___CaptureRequest: ...
    @property
    def stop_capture(self) -> global___CaptureRequest: ...
    @property
    def update_capture(self) -> global___CaptureUpdateRequest: ...
    @property
    def get_cache(self) -> global___CaptureCacheRequest: ...
    def __init__(
        self,
        *,
        start_capture: global___CaptureRequest | None = ...,
        stop_capture: global___CaptureRequest | None = ...,
        update_capture: global___CaptureUpdateRequest | None = ...,
        get_cache: global___CaptureCacheRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["get_cache", b"get_cache", "method", b"method", "start_capture", b"start_capture", "stop_capture", b"stop_capture", "update_capture", b"update_capture"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["get_cache", b"get_cache", "method", b"method", "start_capture", b"start_capture", "stop_capture", b"stop_capture", "update_capture", b"update_capture"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["method", b"method"]) -> typing.Literal["start_capture", "stop_capture", "update_capture", "get_cache"] | None: ...

global___ScreenCaptureRPCRequest = ScreenCaptureRPCRequest

@typing.final
class RpcScreenshotEvent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EVENT_ID_FIELD_NUMBER: builtins.int
    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    SCREENSHOT_PATH_FIELD_NUMBER: builtins.int
    ANNOTATION_PATH_FIELD_NUMBER: builtins.int
    MOUSE_X_FIELD_NUMBER: builtins.int
    MOUSE_Y_FIELD_NUMBER: builtins.int
    KEY_CHAR_FIELD_NUMBER: builtins.int
    KEY_CODE_FIELD_NUMBER: builtins.int
    IS_SPECIAL_KEY_FIELD_NUMBER: builtins.int
    MOUSE_EVENT_TOOL_TIP_FIELD_NUMBER: builtins.int
    event_id: builtins.str
    project_uuid: builtins.str
    command_uuid: builtins.str
    timestamp: builtins.str
    description: builtins.str
    screenshot_path: builtins.str
    annotation_path: builtins.str
    mouse_x: builtins.int
    mouse_y: builtins.int
    key_char: builtins.str
    key_code: builtins.str
    is_special_key: builtins.bool
    mouse_event_tool_tip: builtins.str
    """For mouse button information - defaults to "Left Button" for backward compatibility when mouseX/Y are present"""
    def __init__(
        self,
        *,
        event_id: builtins.str = ...,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
        timestamp: builtins.str = ...,
        description: builtins.str = ...,
        screenshot_path: builtins.str = ...,
        annotation_path: builtins.str | None = ...,
        mouse_x: builtins.int | None = ...,
        mouse_y: builtins.int | None = ...,
        key_char: builtins.str | None = ...,
        key_code: builtins.str | None = ...,
        is_special_key: builtins.bool = ...,
        mouse_event_tool_tip: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["_annotation_path", b"_annotation_path", "_key_char", b"_key_char", "_key_code", b"_key_code", "_mouse_event_tool_tip", b"_mouse_event_tool_tip", "_mouse_x", b"_mouse_x", "_mouse_y", b"_mouse_y", "annotation_path", b"annotation_path", "key_char", b"key_char", "key_code", b"key_code", "mouse_event_tool_tip", b"mouse_event_tool_tip", "mouse_x", b"mouse_x", "mouse_y", b"mouse_y"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["_annotation_path", b"_annotation_path", "_key_char", b"_key_char", "_key_code", b"_key_code", "_mouse_event_tool_tip", b"_mouse_event_tool_tip", "_mouse_x", b"_mouse_x", "_mouse_y", b"_mouse_y", "annotation_path", b"annotation_path", "command_uuid", b"command_uuid", "description", b"description", "event_id", b"event_id", "is_special_key", b"is_special_key", "key_char", b"key_char", "key_code", b"key_code", "mouse_event_tool_tip", b"mouse_event_tool_tip", "mouse_x", b"mouse_x", "mouse_y", b"mouse_y", "project_uuid", b"project_uuid", "screenshot_path", b"screenshot_path", "timestamp", b"timestamp"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_annotation_path", b"_annotation_path"]) -> typing.Literal["annotation_path"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_key_char", b"_key_char"]) -> typing.Literal["key_char"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_key_code", b"_key_code"]) -> typing.Literal["key_code"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_mouse_event_tool_tip", b"_mouse_event_tool_tip"]) -> typing.Literal["mouse_event_tool_tip"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_mouse_x", b"_mouse_x"]) -> typing.Literal["mouse_x"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing.Literal["_mouse_y", b"_mouse_y"]) -> typing.Literal["mouse_y"] | None: ...

global___RpcScreenshotEvent = RpcScreenshotEvent

@typing.final
class CaptureResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    IS_ACTIVE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    SCREENSHOT_EVENTS_FIELD_NUMBER: builtins.int
    project_uuid: builtins.str
    command_uuid: builtins.str
    is_active: builtins.bool
    message: builtins.str
    @property
    def screenshot_events(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RpcScreenshotEvent]: ...
    def __init__(
        self,
        *,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
        is_active: builtins.bool = ...,
        message: builtins.str = ...,
        screenshot_events: collections.abc.Iterable[global___RpcScreenshotEvent] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "is_active", b"is_active", "message", b"message", "project_uuid", b"project_uuid", "screenshot_events", b"screenshot_events"]) -> None: ...

global___CaptureResult = CaptureResult

@typing.final
class ScreenCaptureRPCResponse(google.protobuf.message.Message):
    """Response message types"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CAPTURE_RESPONSE_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    error: builtins.str
    @property
    def capture_response(self) -> global___CaptureResult: ...
    def __init__(
        self,
        *,
        capture_response: global___CaptureResult | None = ...,
        error: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["capture_response", b"capture_response", "error", b"error", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["capture_response", b"capture_response", "error", b"error", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["type", b"type"]) -> typing.Literal["capture_response", "error"] | None: ...

global___ScreenCaptureRPCResponse = ScreenCaptureRPCResponse
