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
class GetResultsRequest(google.protobuf.message.Message):
    """Request to get vision detection results"""

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

global___GetResultsRequest = GetResultsRequest

@typing.final
class UpdateResultsRequest(google.protobuf.message.Message):
    """Request to update vision detection results"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULTS_FIELD_NUMBER: builtins.int
    @property
    def results(self) -> global___VisionDetectResultsList: ...
    def __init__(
        self,
        *,
        results: global___VisionDetectResultsList | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["results", b"results"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["results", b"results"]) -> None: ...

global___UpdateResultsRequest = UpdateResultsRequest

@typing.final
class BoundingBox(google.protobuf.message.Message):
    """Bounding box for UI elements"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    WIDTH_FIELD_NUMBER: builtins.int
    HEIGHT_FIELD_NUMBER: builtins.int
    CLASS_NAME_FIELD_NUMBER: builtins.int
    CONFIDENCE_FIELD_NUMBER: builtins.int
    id: builtins.str
    x: builtins.int
    y: builtins.int
    width: builtins.int
    height: builtins.int
    class_name: builtins.str
    confidence: builtins.float
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        x: builtins.int = ...,
        y: builtins.int = ...,
        width: builtins.int = ...,
        height: builtins.int = ...,
        class_name: builtins.str = ...,
        confidence: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["class_name", b"class_name", "confidence", b"confidence", "height", b"height", "id", b"id", "width", b"width", "x", b"x", "y", b"y"]) -> None: ...

global___BoundingBox = BoundingBox

@typing.final
class VisionDetectResultModel(google.protobuf.message.Message):
    """Vision detection result model"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EVENT_ID_FIELD_NUMBER: builtins.int
    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    ORIGINAL_IMAGE_PATH_FIELD_NUMBER: builtins.int
    ORIGINAL_WIDTH_FIELD_NUMBER: builtins.int
    ORIGINAL_HEIGHT_FIELD_NUMBER: builtins.int
    IS_CROPPED_FIELD_NUMBER: builtins.int
    MERGED_UI_ICON_BBOXES_FIELD_NUMBER: builtins.int
    CROPPED_IMAGE_FIELD_NUMBER: builtins.int
    CROPPED_WIDTH_FIELD_NUMBER: builtins.int
    CROPPED_HEIGHT_FIELD_NUMBER: builtins.int
    event_id: builtins.str
    project_uuid: builtins.str
    command_uuid: builtins.str
    timestamp: builtins.str
    """ISO format timestamp"""
    description: builtins.str
    original_image_path: builtins.str
    original_width: builtins.int
    original_height: builtins.int
    is_cropped: builtins.bool
    cropped_image: builtins.bytes
    """Optional binary image data for websocket transfer"""
    cropped_width: builtins.int
    cropped_height: builtins.int
    @property
    def merged_ui_icon_bboxes(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BoundingBox]: ...
    def __init__(
        self,
        *,
        event_id: builtins.str = ...,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
        timestamp: builtins.str = ...,
        description: builtins.str = ...,
        original_image_path: builtins.str = ...,
        original_width: builtins.int = ...,
        original_height: builtins.int = ...,
        is_cropped: builtins.bool = ...,
        merged_ui_icon_bboxes: collections.abc.Iterable[global___BoundingBox] | None = ...,
        cropped_image: builtins.bytes = ...,
        cropped_width: builtins.int = ...,
        cropped_height: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "cropped_height", b"cropped_height", "cropped_image", b"cropped_image", "cropped_width", b"cropped_width", "description", b"description", "event_id", b"event_id", "is_cropped", b"is_cropped", "merged_ui_icon_bboxes", b"merged_ui_icon_bboxes", "original_height", b"original_height", "original_image_path", b"original_image_path", "original_width", b"original_width", "project_uuid", b"project_uuid", "timestamp", b"timestamp"]) -> None: ...

global___VisionDetectResultModel = VisionDetectResultModel

@typing.final
class VisionDetectResultsList(google.protobuf.message.Message):
    """Vision detection results list"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROJECT_UUID_FIELD_NUMBER: builtins.int
    COMMAND_UUID_FIELD_NUMBER: builtins.int
    RESULTS_FIELD_NUMBER: builtins.int
    project_uuid: builtins.str
    command_uuid: builtins.str
    @property
    def results(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___VisionDetectResultModel]: ...
    def __init__(
        self,
        *,
        project_uuid: builtins.str = ...,
        command_uuid: builtins.str = ...,
        results: collections.abc.Iterable[global___VisionDetectResultModel] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["command_uuid", b"command_uuid", "project_uuid", b"project_uuid", "results", b"results"]) -> None: ...

global___VisionDetectResultsList = VisionDetectResultsList

@typing.final
class VisionDetectStatus(google.protobuf.message.Message):
    """Status of the vision detection service"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STATUS_FIELD_NUMBER: builtins.int
    SCREENSHOT_EVENTS_COUNT_FIELD_NUMBER: builtins.int
    HAS_RESULTS_FIELD_NUMBER: builtins.int
    RESULTS_COUNT_FIELD_NUMBER: builtins.int
    IS_PROCESSING_FIELD_NUMBER: builtins.int
    LAST_PROCESSED_FIELD_NUMBER: builtins.int
    LAST_ERROR_FIELD_NUMBER: builtins.int
    status: builtins.str
    screenshot_events_count: builtins.int
    has_results: builtins.bool
    results_count: builtins.int
    is_processing: builtins.bool
    last_processed: builtins.str
    last_error: builtins.str
    def __init__(
        self,
        *,
        status: builtins.str = ...,
        screenshot_events_count: builtins.int = ...,
        has_results: builtins.bool = ...,
        results_count: builtins.int = ...,
        is_processing: builtins.bool = ...,
        last_processed: builtins.str = ...,
        last_error: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["has_results", b"has_results", "is_processing", b"is_processing", "last_error", b"last_error", "last_processed", b"last_processed", "results_count", b"results_count", "screenshot_events_count", b"screenshot_events_count", "status", b"status"]) -> None: ...

global___VisionDetectStatus = VisionDetectStatus

@typing.final
class VisionDetectRPCRequest(google.protobuf.message.Message):
    """RPC request for vision detection"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GET_RESULTS_REQUEST_FIELD_NUMBER: builtins.int
    UPDATE_RESULTS_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def get_results_request(self) -> global___GetResultsRequest: ...
    @property
    def update_results_request(self) -> global___UpdateResultsRequest: ...
    def __init__(
        self,
        *,
        get_results_request: global___GetResultsRequest | None = ...,
        update_results_request: global___UpdateResultsRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["get_results_request", b"get_results_request", "method", b"method", "update_results_request", b"update_results_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["get_results_request", b"get_results_request", "method", b"method", "update_results_request", b"update_results_request"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["method", b"method"]) -> typing.Literal["get_results_request", "update_results_request"] | None: ...

global___VisionDetectRPCRequest = VisionDetectRPCRequest

@typing.final
class VisionDetectRPCResponse(google.protobuf.message.Message):
    """RPC response for vision detection"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULTS_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    error: builtins.str
    @property
    def results(self) -> global___VisionDetectResultsList: ...
    @property
    def status(self) -> global___VisionDetectStatus: ...
    def __init__(
        self,
        *,
        results: global___VisionDetectResultsList | None = ...,
        status: global___VisionDetectStatus | None = ...,
        error: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["response", b"response", "results", b"results", "status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["error", b"error", "response", b"response", "results", b"results", "status", b"status"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["response", b"response"]) -> typing.Literal["results", "status"] | None: ...

global___VisionDetectRPCResponse = VisionDetectRPCResponse
