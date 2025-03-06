# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: screen_capture.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'screen_capture.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14screen_capture.proto\x12\x14karna.screen_capture\"<\n\x0e\x43\x61ptureRequest\x12\x14\n\x0cproject_uuid\x18\x01 \x01(\t\x12\x14\n\x0c\x63ommand_uuid\x18\x02 \x01(\t\"A\n\x13\x43\x61ptureCacheRequest\x12\x14\n\x0cproject_uuid\x18\x01 \x01(\t\x12\x14\n\x0c\x63ommand_uuid\x18\x02 \x01(\t\"q\n\x14\x43\x61ptureUpdateRequest\x12\x14\n\x0cproject_uuid\x18\x01 \x01(\t\x12\x14\n\x0c\x63ommand_uuid\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x1c\n\x14screenshot_event_ids\x18\x04 \x03(\t\"\xa6\x02\n\x17ScreenCaptureRPCRequest\x12=\n\rstart_capture\x18\x01 \x01(\x0b\x32$.karna.screen_capture.CaptureRequestH\x00\x12<\n\x0cstop_capture\x18\x02 \x01(\x0b\x32$.karna.screen_capture.CaptureRequestH\x00\x12\x44\n\x0eupdate_capture\x18\x03 \x01(\x0b\x32*.karna.screen_capture.CaptureUpdateRequestH\x00\x12>\n\tget_cache\x18\x04 \x01(\x0b\x32).karna.screen_capture.CaptureCacheRequestH\x00\x42\x08\n\x06method\"\xe9\x02\n\x12RpcScreenshotEvent\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t\x12\x14\n\x0cproject_uuid\x18\x02 \x01(\t\x12\x14\n\x0c\x63ommand_uuid\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x17\n\x0fscreenshot_path\x18\x06 \x01(\t\x12\x1c\n\x0f\x61nnotation_path\x18\x07 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07mouse_x\x18\x08 \x01(\x05H\x01\x88\x01\x01\x12\x14\n\x07mouse_y\x18\t \x01(\x05H\x02\x88\x01\x01\x12\x15\n\x08key_char\x18\n \x01(\tH\x03\x88\x01\x01\x12\x15\n\x08key_code\x18\x0b \x01(\tH\x04\x88\x01\x01\x12\x16\n\x0eis_special_key\x18\x0c \x01(\x08\x42\x12\n\x10_annotation_pathB\n\n\x08_mouse_xB\n\n\x08_mouse_yB\x0b\n\t_key_charB\x0b\n\t_key_code\"\xa4\x01\n\rCaptureResult\x12\x14\n\x0cproject_uuid\x18\x01 \x01(\t\x12\x14\n\x0c\x63ommand_uuid\x18\x02 \x01(\t\x12\x11\n\tis_active\x18\x03 \x01(\x08\x12\x0f\n\x07message\x18\x04 \x01(\t\x12\x43\n\x11screenshot_events\x18\x05 \x03(\x0b\x32(.karna.screen_capture.RpcScreenshotEvent\"t\n\x18ScreenCaptureRPCResponse\x12?\n\x10\x63\x61pture_response\x18\x01 \x01(\x0b\x32#.karna.screen_capture.CaptureResultH\x00\x12\x0f\n\x05\x65rror\x18\x02 \x01(\tH\x00\x42\x06\n\x04typeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'screen_capture_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CAPTUREREQUEST']._serialized_start=46
  _globals['_CAPTUREREQUEST']._serialized_end=106
  _globals['_CAPTURECACHEREQUEST']._serialized_start=108
  _globals['_CAPTURECACHEREQUEST']._serialized_end=173
  _globals['_CAPTUREUPDATEREQUEST']._serialized_start=175
  _globals['_CAPTUREUPDATEREQUEST']._serialized_end=288
  _globals['_SCREENCAPTURERPCREQUEST']._serialized_start=291
  _globals['_SCREENCAPTURERPCREQUEST']._serialized_end=585
  _globals['_RPCSCREENSHOTEVENT']._serialized_start=588
  _globals['_RPCSCREENSHOTEVENT']._serialized_end=949
  _globals['_CAPTURERESULT']._serialized_start=952
  _globals['_CAPTURERESULT']._serialized_end=1116
  _globals['_SCREENCAPTURERPCRESPONSE']._serialized_start=1118
  _globals['_SCREENCAPTURERPCRESPONSE']._serialized_end=1234
# @@protoc_insertion_point(module_scope)
