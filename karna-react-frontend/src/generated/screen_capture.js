/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
import * as $protobuf from "protobufjs/minimal";

// Common aliases
const $Reader = $protobuf.Reader, $Writer = $protobuf.Writer, $util = $protobuf.util;

// Exported root namespace
const $root = $protobuf.roots["default"] || ($protobuf.roots["default"] = {});

export const karna = $root.karna = (() => {

    /**
     * Namespace karna.
     * @exports karna
     * @namespace
     */
    const karna = {};

    karna.screen_capture = (function() {

        /**
         * Namespace screen_capture.
         * @memberof karna
         * @namespace
         */
        const screen_capture = {};

        screen_capture.CaptureRequest = (function() {

            /**
             * Properties of a CaptureRequest.
             * @memberof karna.screen_capture
             * @interface ICaptureRequest
             * @property {string|null} [projectUuid] CaptureRequest projectUuid
             * @property {string|null} [commandUuid] CaptureRequest commandUuid
             */

            /**
             * Constructs a new CaptureRequest.
             * @memberof karna.screen_capture
             * @classdesc Represents a CaptureRequest.
             * @implements ICaptureRequest
             * @constructor
             * @param {karna.screen_capture.ICaptureRequest=} [properties] Properties to set
             */
            function CaptureRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CaptureRequest projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.CaptureRequest
             * @instance
             */
            CaptureRequest.prototype.projectUuid = "";

            /**
             * CaptureRequest commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.CaptureRequest
             * @instance
             */
            CaptureRequest.prototype.commandUuid = "";

            /**
             * Creates a new CaptureRequest instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {karna.screen_capture.ICaptureRequest=} [properties] Properties to set
             * @returns {karna.screen_capture.CaptureRequest} CaptureRequest instance
             */
            CaptureRequest.create = function create(properties) {
                return new CaptureRequest(properties);
            };

            /**
             * Encodes the specified CaptureRequest message. Does not implicitly {@link karna.screen_capture.CaptureRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {karna.screen_capture.ICaptureRequest} message CaptureRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                return writer;
            };

            /**
             * Encodes the specified CaptureRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {karna.screen_capture.ICaptureRequest} message CaptureRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CaptureRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.CaptureRequest} CaptureRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.CaptureRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.projectUuid = reader.string();
                            break;
                        }
                    case 2: {
                            message.commandUuid = reader.string();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a CaptureRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.CaptureRequest} CaptureRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CaptureRequest message.
             * @function verify
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CaptureRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                return null;
            };

            /**
             * Creates a CaptureRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.CaptureRequest} CaptureRequest
             */
            CaptureRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.CaptureRequest)
                    return object;
                let message = new $root.karna.screen_capture.CaptureRequest();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                return message;
            };

            /**
             * Creates a plain object from a CaptureRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {karna.screen_capture.CaptureRequest} message CaptureRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CaptureRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                return object;
            };

            /**
             * Converts this CaptureRequest to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.CaptureRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CaptureRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CaptureRequest
             * @function getTypeUrl
             * @memberof karna.screen_capture.CaptureRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CaptureRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.CaptureRequest";
            };

            return CaptureRequest;
        })();

        screen_capture.CaptureUpdateRequest = (function() {

            /**
             * Properties of a CaptureUpdateRequest.
             * @memberof karna.screen_capture
             * @interface ICaptureUpdateRequest
             * @property {string|null} [projectUuid] CaptureUpdateRequest projectUuid
             * @property {string|null} [commandUuid] CaptureUpdateRequest commandUuid
             * @property {string|null} [message] CaptureUpdateRequest message
             * @property {Array.<string>|null} [screenshotEventIds] CaptureUpdateRequest screenshotEventIds
             */

            /**
             * Constructs a new CaptureUpdateRequest.
             * @memberof karna.screen_capture
             * @classdesc Represents a CaptureUpdateRequest.
             * @implements ICaptureUpdateRequest
             * @constructor
             * @param {karna.screen_capture.ICaptureUpdateRequest=} [properties] Properties to set
             */
            function CaptureUpdateRequest(properties) {
                this.screenshotEventIds = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CaptureUpdateRequest projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             */
            CaptureUpdateRequest.prototype.projectUuid = "";

            /**
             * CaptureUpdateRequest commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             */
            CaptureUpdateRequest.prototype.commandUuid = "";

            /**
             * CaptureUpdateRequest message.
             * @member {string} message
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             */
            CaptureUpdateRequest.prototype.message = "";

            /**
             * CaptureUpdateRequest screenshotEventIds.
             * @member {Array.<string>} screenshotEventIds
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             */
            CaptureUpdateRequest.prototype.screenshotEventIds = $util.emptyArray;

            /**
             * Creates a new CaptureUpdateRequest instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {karna.screen_capture.ICaptureUpdateRequest=} [properties] Properties to set
             * @returns {karna.screen_capture.CaptureUpdateRequest} CaptureUpdateRequest instance
             */
            CaptureUpdateRequest.create = function create(properties) {
                return new CaptureUpdateRequest(properties);
            };

            /**
             * Encodes the specified CaptureUpdateRequest message. Does not implicitly {@link karna.screen_capture.CaptureUpdateRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {karna.screen_capture.ICaptureUpdateRequest} message CaptureUpdateRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureUpdateRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                if (message.message != null && Object.hasOwnProperty.call(message, "message"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.message);
                if (message.screenshotEventIds != null && message.screenshotEventIds.length)
                    for (let i = 0; i < message.screenshotEventIds.length; ++i)
                        writer.uint32(/* id 4, wireType 2 =*/34).string(message.screenshotEventIds[i]);
                return writer;
            };

            /**
             * Encodes the specified CaptureUpdateRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureUpdateRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {karna.screen_capture.ICaptureUpdateRequest} message CaptureUpdateRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureUpdateRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CaptureUpdateRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.CaptureUpdateRequest} CaptureUpdateRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureUpdateRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.CaptureUpdateRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.projectUuid = reader.string();
                            break;
                        }
                    case 2: {
                            message.commandUuid = reader.string();
                            break;
                        }
                    case 3: {
                            message.message = reader.string();
                            break;
                        }
                    case 4: {
                            if (!(message.screenshotEventIds && message.screenshotEventIds.length))
                                message.screenshotEventIds = [];
                            message.screenshotEventIds.push(reader.string());
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a CaptureUpdateRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.CaptureUpdateRequest} CaptureUpdateRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureUpdateRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CaptureUpdateRequest message.
             * @function verify
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CaptureUpdateRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                if (message.message != null && message.hasOwnProperty("message"))
                    if (!$util.isString(message.message))
                        return "message: string expected";
                if (message.screenshotEventIds != null && message.hasOwnProperty("screenshotEventIds")) {
                    if (!Array.isArray(message.screenshotEventIds))
                        return "screenshotEventIds: array expected";
                    for (let i = 0; i < message.screenshotEventIds.length; ++i)
                        if (!$util.isString(message.screenshotEventIds[i]))
                            return "screenshotEventIds: string[] expected";
                }
                return null;
            };

            /**
             * Creates a CaptureUpdateRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.CaptureUpdateRequest} CaptureUpdateRequest
             */
            CaptureUpdateRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.CaptureUpdateRequest)
                    return object;
                let message = new $root.karna.screen_capture.CaptureUpdateRequest();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.message != null)
                    message.message = String(object.message);
                if (object.screenshotEventIds) {
                    if (!Array.isArray(object.screenshotEventIds))
                        throw TypeError(".karna.screen_capture.CaptureUpdateRequest.screenshotEventIds: array expected");
                    message.screenshotEventIds = [];
                    for (let i = 0; i < object.screenshotEventIds.length; ++i)
                        message.screenshotEventIds[i] = String(object.screenshotEventIds[i]);
                }
                return message;
            };

            /**
             * Creates a plain object from a CaptureUpdateRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {karna.screen_capture.CaptureUpdateRequest} message CaptureUpdateRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CaptureUpdateRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.screenshotEventIds = [];
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                    object.message = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.message != null && message.hasOwnProperty("message"))
                    object.message = message.message;
                if (message.screenshotEventIds && message.screenshotEventIds.length) {
                    object.screenshotEventIds = [];
                    for (let j = 0; j < message.screenshotEventIds.length; ++j)
                        object.screenshotEventIds[j] = message.screenshotEventIds[j];
                }
                return object;
            };

            /**
             * Converts this CaptureUpdateRequest to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CaptureUpdateRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CaptureUpdateRequest
             * @function getTypeUrl
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CaptureUpdateRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.CaptureUpdateRequest";
            };

            return CaptureUpdateRequest;
        })();

        screen_capture.CaptureUpdateResponse = (function() {

            /**
             * Properties of a CaptureUpdateResponse.
             * @memberof karna.screen_capture
             * @interface ICaptureUpdateResponse
             * @property {string|null} [projectUuid] CaptureUpdateResponse projectUuid
             * @property {string|null} [commandUuid] CaptureUpdateResponse commandUuid
             * @property {string|null} [message] CaptureUpdateResponse message
             * @property {Array.<karna.screen_capture.IRpcScreenshotEvent>|null} [screenshotEvents] CaptureUpdateResponse screenshotEvents
             */

            /**
             * Constructs a new CaptureUpdateResponse.
             * @memberof karna.screen_capture
             * @classdesc Represents a CaptureUpdateResponse.
             * @implements ICaptureUpdateResponse
             * @constructor
             * @param {karna.screen_capture.ICaptureUpdateResponse=} [properties] Properties to set
             */
            function CaptureUpdateResponse(properties) {
                this.screenshotEvents = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CaptureUpdateResponse projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @instance
             */
            CaptureUpdateResponse.prototype.projectUuid = "";

            /**
             * CaptureUpdateResponse commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @instance
             */
            CaptureUpdateResponse.prototype.commandUuid = "";

            /**
             * CaptureUpdateResponse message.
             * @member {string} message
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @instance
             */
            CaptureUpdateResponse.prototype.message = "";

            /**
             * CaptureUpdateResponse screenshotEvents.
             * @member {Array.<karna.screen_capture.IRpcScreenshotEvent>} screenshotEvents
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @instance
             */
            CaptureUpdateResponse.prototype.screenshotEvents = $util.emptyArray;

            /**
             * Creates a new CaptureUpdateResponse instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {karna.screen_capture.ICaptureUpdateResponse=} [properties] Properties to set
             * @returns {karna.screen_capture.CaptureUpdateResponse} CaptureUpdateResponse instance
             */
            CaptureUpdateResponse.create = function create(properties) {
                return new CaptureUpdateResponse(properties);
            };

            /**
             * Encodes the specified CaptureUpdateResponse message. Does not implicitly {@link karna.screen_capture.CaptureUpdateResponse.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {karna.screen_capture.ICaptureUpdateResponse} message CaptureUpdateResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureUpdateResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                if (message.message != null && Object.hasOwnProperty.call(message, "message"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.message);
                if (message.screenshotEvents != null && message.screenshotEvents.length)
                    for (let i = 0; i < message.screenshotEvents.length; ++i)
                        $root.karna.screen_capture.RpcScreenshotEvent.encode(message.screenshotEvents[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified CaptureUpdateResponse message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureUpdateResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {karna.screen_capture.ICaptureUpdateResponse} message CaptureUpdateResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureUpdateResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CaptureUpdateResponse message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.CaptureUpdateResponse} CaptureUpdateResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureUpdateResponse.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.CaptureUpdateResponse();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.projectUuid = reader.string();
                            break;
                        }
                    case 2: {
                            message.commandUuid = reader.string();
                            break;
                        }
                    case 3: {
                            message.message = reader.string();
                            break;
                        }
                    case 4: {
                            if (!(message.screenshotEvents && message.screenshotEvents.length))
                                message.screenshotEvents = [];
                            message.screenshotEvents.push($root.karna.screen_capture.RpcScreenshotEvent.decode(reader, reader.uint32()));
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a CaptureUpdateResponse message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.CaptureUpdateResponse} CaptureUpdateResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureUpdateResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CaptureUpdateResponse message.
             * @function verify
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CaptureUpdateResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                if (message.message != null && message.hasOwnProperty("message"))
                    if (!$util.isString(message.message))
                        return "message: string expected";
                if (message.screenshotEvents != null && message.hasOwnProperty("screenshotEvents")) {
                    if (!Array.isArray(message.screenshotEvents))
                        return "screenshotEvents: array expected";
                    for (let i = 0; i < message.screenshotEvents.length; ++i) {
                        let error = $root.karna.screen_capture.RpcScreenshotEvent.verify(message.screenshotEvents[i]);
                        if (error)
                            return "screenshotEvents." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a CaptureUpdateResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.CaptureUpdateResponse} CaptureUpdateResponse
             */
            CaptureUpdateResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.CaptureUpdateResponse)
                    return object;
                let message = new $root.karna.screen_capture.CaptureUpdateResponse();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.message != null)
                    message.message = String(object.message);
                if (object.screenshotEvents) {
                    if (!Array.isArray(object.screenshotEvents))
                        throw TypeError(".karna.screen_capture.CaptureUpdateResponse.screenshotEvents: array expected");
                    message.screenshotEvents = [];
                    for (let i = 0; i < object.screenshotEvents.length; ++i) {
                        if (typeof object.screenshotEvents[i] !== "object")
                            throw TypeError(".karna.screen_capture.CaptureUpdateResponse.screenshotEvents: object expected");
                        message.screenshotEvents[i] = $root.karna.screen_capture.RpcScreenshotEvent.fromObject(object.screenshotEvents[i]);
                    }
                }
                return message;
            };

            /**
             * Creates a plain object from a CaptureUpdateResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {karna.screen_capture.CaptureUpdateResponse} message CaptureUpdateResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CaptureUpdateResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.screenshotEvents = [];
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                    object.message = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.message != null && message.hasOwnProperty("message"))
                    object.message = message.message;
                if (message.screenshotEvents && message.screenshotEvents.length) {
                    object.screenshotEvents = [];
                    for (let j = 0; j < message.screenshotEvents.length; ++j)
                        object.screenshotEvents[j] = $root.karna.screen_capture.RpcScreenshotEvent.toObject(message.screenshotEvents[j], options);
                }
                return object;
            };

            /**
             * Converts this CaptureUpdateResponse to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CaptureUpdateResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CaptureUpdateResponse
             * @function getTypeUrl
             * @memberof karna.screen_capture.CaptureUpdateResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CaptureUpdateResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.CaptureUpdateResponse";
            };

            return CaptureUpdateResponse;
        })();

        screen_capture.ScreenCaptureRPCRequest = (function() {

            /**
             * Properties of a ScreenCaptureRPCRequest.
             * @memberof karna.screen_capture
             * @interface IScreenCaptureRPCRequest
             * @property {karna.screen_capture.ICaptureRequest|null} [startCapture] ScreenCaptureRPCRequest startCapture
             * @property {karna.screen_capture.ICaptureRequest|null} [stopCapture] ScreenCaptureRPCRequest stopCapture
             * @property {karna.screen_capture.ICaptureUpdateRequest|null} [updateCapture] ScreenCaptureRPCRequest updateCapture
             */

            /**
             * Constructs a new ScreenCaptureRPCRequest.
             * @memberof karna.screen_capture
             * @classdesc Represents a ScreenCaptureRPCRequest.
             * @implements IScreenCaptureRPCRequest
             * @constructor
             * @param {karna.screen_capture.IScreenCaptureRPCRequest=} [properties] Properties to set
             */
            function ScreenCaptureRPCRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ScreenCaptureRPCRequest startCapture.
             * @member {karna.screen_capture.ICaptureRequest|null|undefined} startCapture
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            ScreenCaptureRPCRequest.prototype.startCapture = null;

            /**
             * ScreenCaptureRPCRequest stopCapture.
             * @member {karna.screen_capture.ICaptureRequest|null|undefined} stopCapture
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            ScreenCaptureRPCRequest.prototype.stopCapture = null;

            /**
             * ScreenCaptureRPCRequest updateCapture.
             * @member {karna.screen_capture.ICaptureUpdateRequest|null|undefined} updateCapture
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            ScreenCaptureRPCRequest.prototype.updateCapture = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * ScreenCaptureRPCRequest method.
             * @member {"startCapture"|"stopCapture"|"updateCapture"|undefined} method
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            Object.defineProperty(ScreenCaptureRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["startCapture", "stopCapture", "updateCapture"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new ScreenCaptureRPCRequest instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCRequest=} [properties] Properties to set
             * @returns {karna.screen_capture.ScreenCaptureRPCRequest} ScreenCaptureRPCRequest instance
             */
            ScreenCaptureRPCRequest.create = function create(properties) {
                return new ScreenCaptureRPCRequest(properties);
            };

            /**
             * Encodes the specified ScreenCaptureRPCRequest message. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCRequest} message ScreenCaptureRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ScreenCaptureRPCRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.startCapture != null && Object.hasOwnProperty.call(message, "startCapture"))
                    $root.karna.screen_capture.CaptureRequest.encode(message.startCapture, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.stopCapture != null && Object.hasOwnProperty.call(message, "stopCapture"))
                    $root.karna.screen_capture.CaptureRequest.encode(message.stopCapture, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
                if (message.updateCapture != null && Object.hasOwnProperty.call(message, "updateCapture"))
                    $root.karna.screen_capture.CaptureUpdateRequest.encode(message.updateCapture, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified ScreenCaptureRPCRequest message, length delimited. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCRequest} message ScreenCaptureRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ScreenCaptureRPCRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a ScreenCaptureRPCRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.ScreenCaptureRPCRequest} ScreenCaptureRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ScreenCaptureRPCRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.ScreenCaptureRPCRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.startCapture = $root.karna.screen_capture.CaptureRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 2: {
                            message.stopCapture = $root.karna.screen_capture.CaptureRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 3: {
                            message.updateCapture = $root.karna.screen_capture.CaptureUpdateRequest.decode(reader, reader.uint32());
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a ScreenCaptureRPCRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.ScreenCaptureRPCRequest} ScreenCaptureRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ScreenCaptureRPCRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ScreenCaptureRPCRequest message.
             * @function verify
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ScreenCaptureRPCRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.startCapture != null && message.hasOwnProperty("startCapture")) {
                    properties.method = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureRequest.verify(message.startCapture);
                        if (error)
                            return "startCapture." + error;
                    }
                }
                if (message.stopCapture != null && message.hasOwnProperty("stopCapture")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureRequest.verify(message.stopCapture);
                        if (error)
                            return "stopCapture." + error;
                    }
                }
                if (message.updateCapture != null && message.hasOwnProperty("updateCapture")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureUpdateRequest.verify(message.updateCapture);
                        if (error)
                            return "updateCapture." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a ScreenCaptureRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.ScreenCaptureRPCRequest} ScreenCaptureRPCRequest
             */
            ScreenCaptureRPCRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.ScreenCaptureRPCRequest)
                    return object;
                let message = new $root.karna.screen_capture.ScreenCaptureRPCRequest();
                if (object.startCapture != null) {
                    if (typeof object.startCapture !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCRequest.startCapture: object expected");
                    message.startCapture = $root.karna.screen_capture.CaptureRequest.fromObject(object.startCapture);
                }
                if (object.stopCapture != null) {
                    if (typeof object.stopCapture !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCRequest.stopCapture: object expected");
                    message.stopCapture = $root.karna.screen_capture.CaptureRequest.fromObject(object.stopCapture);
                }
                if (object.updateCapture != null) {
                    if (typeof object.updateCapture !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCRequest.updateCapture: object expected");
                    message.updateCapture = $root.karna.screen_capture.CaptureUpdateRequest.fromObject(object.updateCapture);
                }
                return message;
            };

            /**
             * Creates a plain object from a ScreenCaptureRPCRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {karna.screen_capture.ScreenCaptureRPCRequest} message ScreenCaptureRPCRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ScreenCaptureRPCRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.startCapture != null && message.hasOwnProperty("startCapture")) {
                    object.startCapture = $root.karna.screen_capture.CaptureRequest.toObject(message.startCapture, options);
                    if (options.oneofs)
                        object.method = "startCapture";
                }
                if (message.stopCapture != null && message.hasOwnProperty("stopCapture")) {
                    object.stopCapture = $root.karna.screen_capture.CaptureRequest.toObject(message.stopCapture, options);
                    if (options.oneofs)
                        object.method = "stopCapture";
                }
                if (message.updateCapture != null && message.hasOwnProperty("updateCapture")) {
                    object.updateCapture = $root.karna.screen_capture.CaptureUpdateRequest.toObject(message.updateCapture, options);
                    if (options.oneofs)
                        object.method = "updateCapture";
                }
                return object;
            };

            /**
             * Converts this ScreenCaptureRPCRequest to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ScreenCaptureRPCRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ScreenCaptureRPCRequest
             * @function getTypeUrl
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ScreenCaptureRPCRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.ScreenCaptureRPCRequest";
            };

            return ScreenCaptureRPCRequest;
        })();

        screen_capture.RpcScreenshotEvent = (function() {

            /**
             * Properties of a RpcScreenshotEvent.
             * @memberof karna.screen_capture
             * @interface IRpcScreenshotEvent
             * @property {string|null} [eventId] RpcScreenshotEvent eventId
             * @property {string|null} [projectUuid] RpcScreenshotEvent projectUuid
             * @property {string|null} [commandUuid] RpcScreenshotEvent commandUuid
             * @property {string|null} [timestamp] RpcScreenshotEvent timestamp
             * @property {string|null} [description] RpcScreenshotEvent description
             * @property {string|null} [screenshotPath] RpcScreenshotEvent screenshotPath
             * @property {string|null} [annotationPath] RpcScreenshotEvent annotationPath
             * @property {number|null} [mouseX] RpcScreenshotEvent mouseX
             * @property {number|null} [mouseY] RpcScreenshotEvent mouseY
             * @property {string|null} [keyChar] RpcScreenshotEvent keyChar
             * @property {string|null} [keyCode] RpcScreenshotEvent keyCode
             * @property {boolean|null} [isSpecialKey] RpcScreenshotEvent isSpecialKey
             */

            /**
             * Constructs a new RpcScreenshotEvent.
             * @memberof karna.screen_capture
             * @classdesc Represents a RpcScreenshotEvent.
             * @implements IRpcScreenshotEvent
             * @constructor
             * @param {karna.screen_capture.IRpcScreenshotEvent=} [properties] Properties to set
             */
            function RpcScreenshotEvent(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * RpcScreenshotEvent eventId.
             * @member {string} eventId
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.eventId = "";

            /**
             * RpcScreenshotEvent projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.projectUuid = "";

            /**
             * RpcScreenshotEvent commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.commandUuid = "";

            /**
             * RpcScreenshotEvent timestamp.
             * @member {string} timestamp
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.timestamp = "";

            /**
             * RpcScreenshotEvent description.
             * @member {string} description
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.description = "";

            /**
             * RpcScreenshotEvent screenshotPath.
             * @member {string} screenshotPath
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.screenshotPath = "";

            /**
             * RpcScreenshotEvent annotationPath.
             * @member {string|null|undefined} annotationPath
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.annotationPath = null;

            /**
             * RpcScreenshotEvent mouseX.
             * @member {number|null|undefined} mouseX
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.mouseX = null;

            /**
             * RpcScreenshotEvent mouseY.
             * @member {number|null|undefined} mouseY
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.mouseY = null;

            /**
             * RpcScreenshotEvent keyChar.
             * @member {string|null|undefined} keyChar
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.keyChar = null;

            /**
             * RpcScreenshotEvent keyCode.
             * @member {string|null|undefined} keyCode
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.keyCode = null;

            /**
             * RpcScreenshotEvent isSpecialKey.
             * @member {boolean} isSpecialKey
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.isSpecialKey = false;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_annotationPath", {
                get: $util.oneOfGetter($oneOfFields = ["annotationPath"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_mouseX", {
                get: $util.oneOfGetter($oneOfFields = ["mouseX"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_mouseY", {
                get: $util.oneOfGetter($oneOfFields = ["mouseY"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_keyChar", {
                get: $util.oneOfGetter($oneOfFields = ["keyChar"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_keyCode", {
                get: $util.oneOfGetter($oneOfFields = ["keyCode"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new RpcScreenshotEvent instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {karna.screen_capture.IRpcScreenshotEvent=} [properties] Properties to set
             * @returns {karna.screen_capture.RpcScreenshotEvent} RpcScreenshotEvent instance
             */
            RpcScreenshotEvent.create = function create(properties) {
                return new RpcScreenshotEvent(properties);
            };

            /**
             * Encodes the specified RpcScreenshotEvent message. Does not implicitly {@link karna.screen_capture.RpcScreenshotEvent.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {karna.screen_capture.IRpcScreenshotEvent} message RpcScreenshotEvent message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            RpcScreenshotEvent.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.eventId != null && Object.hasOwnProperty.call(message, "eventId"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.eventId);
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.commandUuid);
                if (message.timestamp != null && Object.hasOwnProperty.call(message, "timestamp"))
                    writer.uint32(/* id 4, wireType 2 =*/34).string(message.timestamp);
                if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                    writer.uint32(/* id 5, wireType 2 =*/42).string(message.description);
                if (message.screenshotPath != null && Object.hasOwnProperty.call(message, "screenshotPath"))
                    writer.uint32(/* id 6, wireType 2 =*/50).string(message.screenshotPath);
                if (message.annotationPath != null && Object.hasOwnProperty.call(message, "annotationPath"))
                    writer.uint32(/* id 7, wireType 2 =*/58).string(message.annotationPath);
                if (message.mouseX != null && Object.hasOwnProperty.call(message, "mouseX"))
                    writer.uint32(/* id 8, wireType 0 =*/64).int32(message.mouseX);
                if (message.mouseY != null && Object.hasOwnProperty.call(message, "mouseY"))
                    writer.uint32(/* id 9, wireType 0 =*/72).int32(message.mouseY);
                if (message.keyChar != null && Object.hasOwnProperty.call(message, "keyChar"))
                    writer.uint32(/* id 10, wireType 2 =*/82).string(message.keyChar);
                if (message.keyCode != null && Object.hasOwnProperty.call(message, "keyCode"))
                    writer.uint32(/* id 11, wireType 2 =*/90).string(message.keyCode);
                if (message.isSpecialKey != null && Object.hasOwnProperty.call(message, "isSpecialKey"))
                    writer.uint32(/* id 12, wireType 0 =*/96).bool(message.isSpecialKey);
                return writer;
            };

            /**
             * Encodes the specified RpcScreenshotEvent message, length delimited. Does not implicitly {@link karna.screen_capture.RpcScreenshotEvent.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {karna.screen_capture.IRpcScreenshotEvent} message RpcScreenshotEvent message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            RpcScreenshotEvent.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a RpcScreenshotEvent message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.RpcScreenshotEvent} RpcScreenshotEvent
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            RpcScreenshotEvent.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.RpcScreenshotEvent();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.eventId = reader.string();
                            break;
                        }
                    case 2: {
                            message.projectUuid = reader.string();
                            break;
                        }
                    case 3: {
                            message.commandUuid = reader.string();
                            break;
                        }
                    case 4: {
                            message.timestamp = reader.string();
                            break;
                        }
                    case 5: {
                            message.description = reader.string();
                            break;
                        }
                    case 6: {
                            message.screenshotPath = reader.string();
                            break;
                        }
                    case 7: {
                            message.annotationPath = reader.string();
                            break;
                        }
                    case 8: {
                            message.mouseX = reader.int32();
                            break;
                        }
                    case 9: {
                            message.mouseY = reader.int32();
                            break;
                        }
                    case 10: {
                            message.keyChar = reader.string();
                            break;
                        }
                    case 11: {
                            message.keyCode = reader.string();
                            break;
                        }
                    case 12: {
                            message.isSpecialKey = reader.bool();
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a RpcScreenshotEvent message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.RpcScreenshotEvent} RpcScreenshotEvent
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            RpcScreenshotEvent.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a RpcScreenshotEvent message.
             * @function verify
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            RpcScreenshotEvent.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.eventId != null && message.hasOwnProperty("eventId"))
                    if (!$util.isString(message.eventId))
                        return "eventId: string expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                    if (!$util.isString(message.timestamp))
                        return "timestamp: string expected";
                if (message.description != null && message.hasOwnProperty("description"))
                    if (!$util.isString(message.description))
                        return "description: string expected";
                if (message.screenshotPath != null && message.hasOwnProperty("screenshotPath"))
                    if (!$util.isString(message.screenshotPath))
                        return "screenshotPath: string expected";
                if (message.annotationPath != null && message.hasOwnProperty("annotationPath")) {
                    properties._annotationPath = 1;
                    if (!$util.isString(message.annotationPath))
                        return "annotationPath: string expected";
                }
                if (message.mouseX != null && message.hasOwnProperty("mouseX")) {
                    properties._mouseX = 1;
                    if (!$util.isInteger(message.mouseX))
                        return "mouseX: integer expected";
                }
                if (message.mouseY != null && message.hasOwnProperty("mouseY")) {
                    properties._mouseY = 1;
                    if (!$util.isInteger(message.mouseY))
                        return "mouseY: integer expected";
                }
                if (message.keyChar != null && message.hasOwnProperty("keyChar")) {
                    properties._keyChar = 1;
                    if (!$util.isString(message.keyChar))
                        return "keyChar: string expected";
                }
                if (message.keyCode != null && message.hasOwnProperty("keyCode")) {
                    properties._keyCode = 1;
                    if (!$util.isString(message.keyCode))
                        return "keyCode: string expected";
                }
                if (message.isSpecialKey != null && message.hasOwnProperty("isSpecialKey"))
                    if (typeof message.isSpecialKey !== "boolean")
                        return "isSpecialKey: boolean expected";
                return null;
            };

            /**
             * Creates a RpcScreenshotEvent message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.RpcScreenshotEvent} RpcScreenshotEvent
             */
            RpcScreenshotEvent.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.RpcScreenshotEvent)
                    return object;
                let message = new $root.karna.screen_capture.RpcScreenshotEvent();
                if (object.eventId != null)
                    message.eventId = String(object.eventId);
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.timestamp != null)
                    message.timestamp = String(object.timestamp);
                if (object.description != null)
                    message.description = String(object.description);
                if (object.screenshotPath != null)
                    message.screenshotPath = String(object.screenshotPath);
                if (object.annotationPath != null)
                    message.annotationPath = String(object.annotationPath);
                if (object.mouseX != null)
                    message.mouseX = object.mouseX | 0;
                if (object.mouseY != null)
                    message.mouseY = object.mouseY | 0;
                if (object.keyChar != null)
                    message.keyChar = String(object.keyChar);
                if (object.keyCode != null)
                    message.keyCode = String(object.keyCode);
                if (object.isSpecialKey != null)
                    message.isSpecialKey = Boolean(object.isSpecialKey);
                return message;
            };

            /**
             * Creates a plain object from a RpcScreenshotEvent message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {karna.screen_capture.RpcScreenshotEvent} message RpcScreenshotEvent
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            RpcScreenshotEvent.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults) {
                    object.eventId = "";
                    object.projectUuid = "";
                    object.commandUuid = "";
                    object.timestamp = "";
                    object.description = "";
                    object.screenshotPath = "";
                    object.isSpecialKey = false;
                }
                if (message.eventId != null && message.hasOwnProperty("eventId"))
                    object.eventId = message.eventId;
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                    object.timestamp = message.timestamp;
                if (message.description != null && message.hasOwnProperty("description"))
                    object.description = message.description;
                if (message.screenshotPath != null && message.hasOwnProperty("screenshotPath"))
                    object.screenshotPath = message.screenshotPath;
                if (message.annotationPath != null && message.hasOwnProperty("annotationPath")) {
                    object.annotationPath = message.annotationPath;
                    if (options.oneofs)
                        object._annotationPath = "annotationPath";
                }
                if (message.mouseX != null && message.hasOwnProperty("mouseX")) {
                    object.mouseX = message.mouseX;
                    if (options.oneofs)
                        object._mouseX = "mouseX";
                }
                if (message.mouseY != null && message.hasOwnProperty("mouseY")) {
                    object.mouseY = message.mouseY;
                    if (options.oneofs)
                        object._mouseY = "mouseY";
                }
                if (message.keyChar != null && message.hasOwnProperty("keyChar")) {
                    object.keyChar = message.keyChar;
                    if (options.oneofs)
                        object._keyChar = "keyChar";
                }
                if (message.keyCode != null && message.hasOwnProperty("keyCode")) {
                    object.keyCode = message.keyCode;
                    if (options.oneofs)
                        object._keyCode = "keyCode";
                }
                if (message.isSpecialKey != null && message.hasOwnProperty("isSpecialKey"))
                    object.isSpecialKey = message.isSpecialKey;
                return object;
            };

            /**
             * Converts this RpcScreenshotEvent to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            RpcScreenshotEvent.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for RpcScreenshotEvent
             * @function getTypeUrl
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            RpcScreenshotEvent.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.RpcScreenshotEvent";
            };

            return RpcScreenshotEvent;
        })();

        screen_capture.CaptureResult = (function() {

            /**
             * Properties of a CaptureResult.
             * @memberof karna.screen_capture
             * @interface ICaptureResult
             * @property {string|null} [projectUuid] CaptureResult projectUuid
             * @property {string|null} [commandUuid] CaptureResult commandUuid
             * @property {boolean|null} [isActive] CaptureResult isActive
             * @property {string|null} [message] CaptureResult message
             * @property {Array.<karna.screen_capture.IRpcScreenshotEvent>|null} [screenshotEvents] CaptureResult screenshotEvents
             */

            /**
             * Constructs a new CaptureResult.
             * @memberof karna.screen_capture
             * @classdesc Represents a CaptureResult.
             * @implements ICaptureResult
             * @constructor
             * @param {karna.screen_capture.ICaptureResult=} [properties] Properties to set
             */
            function CaptureResult(properties) {
                this.screenshotEvents = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CaptureResult projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             */
            CaptureResult.prototype.projectUuid = "";

            /**
             * CaptureResult commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             */
            CaptureResult.prototype.commandUuid = "";

            /**
             * CaptureResult isActive.
             * @member {boolean} isActive
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             */
            CaptureResult.prototype.isActive = false;

            /**
             * CaptureResult message.
             * @member {string} message
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             */
            CaptureResult.prototype.message = "";

            /**
             * CaptureResult screenshotEvents.
             * @member {Array.<karna.screen_capture.IRpcScreenshotEvent>} screenshotEvents
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             */
            CaptureResult.prototype.screenshotEvents = $util.emptyArray;

            /**
             * Creates a new CaptureResult instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {karna.screen_capture.ICaptureResult=} [properties] Properties to set
             * @returns {karna.screen_capture.CaptureResult} CaptureResult instance
             */
            CaptureResult.create = function create(properties) {
                return new CaptureResult(properties);
            };

            /**
             * Encodes the specified CaptureResult message. Does not implicitly {@link karna.screen_capture.CaptureResult.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {karna.screen_capture.ICaptureResult} message CaptureResult message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureResult.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                if (message.isActive != null && Object.hasOwnProperty.call(message, "isActive"))
                    writer.uint32(/* id 3, wireType 0 =*/24).bool(message.isActive);
                if (message.message != null && Object.hasOwnProperty.call(message, "message"))
                    writer.uint32(/* id 4, wireType 2 =*/34).string(message.message);
                if (message.screenshotEvents != null && message.screenshotEvents.length)
                    for (let i = 0; i < message.screenshotEvents.length; ++i)
                        $root.karna.screen_capture.RpcScreenshotEvent.encode(message.screenshotEvents[i], writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified CaptureResult message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureResult.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {karna.screen_capture.ICaptureResult} message CaptureResult message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureResult.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CaptureResult message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.CaptureResult} CaptureResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureResult.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.CaptureResult();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.projectUuid = reader.string();
                            break;
                        }
                    case 2: {
                            message.commandUuid = reader.string();
                            break;
                        }
                    case 3: {
                            message.isActive = reader.bool();
                            break;
                        }
                    case 4: {
                            message.message = reader.string();
                            break;
                        }
                    case 5: {
                            if (!(message.screenshotEvents && message.screenshotEvents.length))
                                message.screenshotEvents = [];
                            message.screenshotEvents.push($root.karna.screen_capture.RpcScreenshotEvent.decode(reader, reader.uint32()));
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a CaptureResult message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.CaptureResult} CaptureResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureResult.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CaptureResult message.
             * @function verify
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CaptureResult.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                if (message.isActive != null && message.hasOwnProperty("isActive"))
                    if (typeof message.isActive !== "boolean")
                        return "isActive: boolean expected";
                if (message.message != null && message.hasOwnProperty("message"))
                    if (!$util.isString(message.message))
                        return "message: string expected";
                if (message.screenshotEvents != null && message.hasOwnProperty("screenshotEvents")) {
                    if (!Array.isArray(message.screenshotEvents))
                        return "screenshotEvents: array expected";
                    for (let i = 0; i < message.screenshotEvents.length; ++i) {
                        let error = $root.karna.screen_capture.RpcScreenshotEvent.verify(message.screenshotEvents[i]);
                        if (error)
                            return "screenshotEvents." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a CaptureResult message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.CaptureResult} CaptureResult
             */
            CaptureResult.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.CaptureResult)
                    return object;
                let message = new $root.karna.screen_capture.CaptureResult();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.isActive != null)
                    message.isActive = Boolean(object.isActive);
                if (object.message != null)
                    message.message = String(object.message);
                if (object.screenshotEvents) {
                    if (!Array.isArray(object.screenshotEvents))
                        throw TypeError(".karna.screen_capture.CaptureResult.screenshotEvents: array expected");
                    message.screenshotEvents = [];
                    for (let i = 0; i < object.screenshotEvents.length; ++i) {
                        if (typeof object.screenshotEvents[i] !== "object")
                            throw TypeError(".karna.screen_capture.CaptureResult.screenshotEvents: object expected");
                        message.screenshotEvents[i] = $root.karna.screen_capture.RpcScreenshotEvent.fromObject(object.screenshotEvents[i]);
                    }
                }
                return message;
            };

            /**
             * Creates a plain object from a CaptureResult message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {karna.screen_capture.CaptureResult} message CaptureResult
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CaptureResult.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.screenshotEvents = [];
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                    object.isActive = false;
                    object.message = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.isActive != null && message.hasOwnProperty("isActive"))
                    object.isActive = message.isActive;
                if (message.message != null && message.hasOwnProperty("message"))
                    object.message = message.message;
                if (message.screenshotEvents && message.screenshotEvents.length) {
                    object.screenshotEvents = [];
                    for (let j = 0; j < message.screenshotEvents.length; ++j)
                        object.screenshotEvents[j] = $root.karna.screen_capture.RpcScreenshotEvent.toObject(message.screenshotEvents[j], options);
                }
                return object;
            };

            /**
             * Converts this CaptureResult to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.CaptureResult
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CaptureResult.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CaptureResult
             * @function getTypeUrl
             * @memberof karna.screen_capture.CaptureResult
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CaptureResult.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.CaptureResult";
            };

            return CaptureResult;
        })();

        screen_capture.ScreenCaptureRPCResponse = (function() {

            /**
             * Properties of a ScreenCaptureRPCResponse.
             * @memberof karna.screen_capture
             * @interface IScreenCaptureRPCResponse
             * @property {karna.screen_capture.ICaptureResult|null} [captureResponse] ScreenCaptureRPCResponse captureResponse
             * @property {string|null} [error] ScreenCaptureRPCResponse error
             * @property {karna.screen_capture.ICaptureUpdateResponse|null} [updateCaptureResponse] ScreenCaptureRPCResponse updateCaptureResponse
             */

            /**
             * Constructs a new ScreenCaptureRPCResponse.
             * @memberof karna.screen_capture
             * @classdesc Represents a ScreenCaptureRPCResponse.
             * @implements IScreenCaptureRPCResponse
             * @constructor
             * @param {karna.screen_capture.IScreenCaptureRPCResponse=} [properties] Properties to set
             */
            function ScreenCaptureRPCResponse(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ScreenCaptureRPCResponse captureResponse.
             * @member {karna.screen_capture.ICaptureResult|null|undefined} captureResponse
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             */
            ScreenCaptureRPCResponse.prototype.captureResponse = null;

            /**
             * ScreenCaptureRPCResponse error.
             * @member {string|null|undefined} error
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             */
            ScreenCaptureRPCResponse.prototype.error = null;

            /**
             * ScreenCaptureRPCResponse updateCaptureResponse.
             * @member {karna.screen_capture.ICaptureUpdateResponse|null|undefined} updateCaptureResponse
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             */
            ScreenCaptureRPCResponse.prototype.updateCaptureResponse = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * ScreenCaptureRPCResponse type.
             * @member {"captureResponse"|"error"|"updateCaptureResponse"|undefined} type
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             */
            Object.defineProperty(ScreenCaptureRPCResponse.prototype, "type", {
                get: $util.oneOfGetter($oneOfFields = ["captureResponse", "error", "updateCaptureResponse"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new ScreenCaptureRPCResponse instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCResponse=} [properties] Properties to set
             * @returns {karna.screen_capture.ScreenCaptureRPCResponse} ScreenCaptureRPCResponse instance
             */
            ScreenCaptureRPCResponse.create = function create(properties) {
                return new ScreenCaptureRPCResponse(properties);
            };

            /**
             * Encodes the specified ScreenCaptureRPCResponse message. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCResponse.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCResponse} message ScreenCaptureRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ScreenCaptureRPCResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.captureResponse != null && Object.hasOwnProperty.call(message, "captureResponse"))
                    $root.karna.screen_capture.CaptureResult.encode(message.captureResponse, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.error);
                if (message.updateCaptureResponse != null && Object.hasOwnProperty.call(message, "updateCaptureResponse"))
                    $root.karna.screen_capture.CaptureUpdateResponse.encode(message.updateCaptureResponse, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified ScreenCaptureRPCResponse message, length delimited. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {karna.screen_capture.IScreenCaptureRPCResponse} message ScreenCaptureRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ScreenCaptureRPCResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a ScreenCaptureRPCResponse message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.ScreenCaptureRPCResponse} ScreenCaptureRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ScreenCaptureRPCResponse.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.ScreenCaptureRPCResponse();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.captureResponse = $root.karna.screen_capture.CaptureResult.decode(reader, reader.uint32());
                            break;
                        }
                    case 2: {
                            message.error = reader.string();
                            break;
                        }
                    case 3: {
                            message.updateCaptureResponse = $root.karna.screen_capture.CaptureUpdateResponse.decode(reader, reader.uint32());
                            break;
                        }
                    default:
                        reader.skipType(tag & 7);
                        break;
                    }
                }
                return message;
            };

            /**
             * Decodes a ScreenCaptureRPCResponse message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.ScreenCaptureRPCResponse} ScreenCaptureRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ScreenCaptureRPCResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ScreenCaptureRPCResponse message.
             * @function verify
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ScreenCaptureRPCResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.captureResponse != null && message.hasOwnProperty("captureResponse")) {
                    properties.type = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureResult.verify(message.captureResponse);
                        if (error)
                            return "captureResponse." + error;
                    }
                }
                if (message.error != null && message.hasOwnProperty("error")) {
                    if (properties.type === 1)
                        return "type: multiple values";
                    properties.type = 1;
                    if (!$util.isString(message.error))
                        return "error: string expected";
                }
                if (message.updateCaptureResponse != null && message.hasOwnProperty("updateCaptureResponse")) {
                    if (properties.type === 1)
                        return "type: multiple values";
                    properties.type = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureUpdateResponse.verify(message.updateCaptureResponse);
                        if (error)
                            return "updateCaptureResponse." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a ScreenCaptureRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.ScreenCaptureRPCResponse} ScreenCaptureRPCResponse
             */
            ScreenCaptureRPCResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.ScreenCaptureRPCResponse)
                    return object;
                let message = new $root.karna.screen_capture.ScreenCaptureRPCResponse();
                if (object.captureResponse != null) {
                    if (typeof object.captureResponse !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCResponse.captureResponse: object expected");
                    message.captureResponse = $root.karna.screen_capture.CaptureResult.fromObject(object.captureResponse);
                }
                if (object.error != null)
                    message.error = String(object.error);
                if (object.updateCaptureResponse != null) {
                    if (typeof object.updateCaptureResponse !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCResponse.updateCaptureResponse: object expected");
                    message.updateCaptureResponse = $root.karna.screen_capture.CaptureUpdateResponse.fromObject(object.updateCaptureResponse);
                }
                return message;
            };

            /**
             * Creates a plain object from a ScreenCaptureRPCResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {karna.screen_capture.ScreenCaptureRPCResponse} message ScreenCaptureRPCResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ScreenCaptureRPCResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.captureResponse != null && message.hasOwnProperty("captureResponse")) {
                    object.captureResponse = $root.karna.screen_capture.CaptureResult.toObject(message.captureResponse, options);
                    if (options.oneofs)
                        object.type = "captureResponse";
                }
                if (message.error != null && message.hasOwnProperty("error")) {
                    object.error = message.error;
                    if (options.oneofs)
                        object.type = "error";
                }
                if (message.updateCaptureResponse != null && message.hasOwnProperty("updateCaptureResponse")) {
                    object.updateCaptureResponse = $root.karna.screen_capture.CaptureUpdateResponse.toObject(message.updateCaptureResponse, options);
                    if (options.oneofs)
                        object.type = "updateCaptureResponse";
                }
                return object;
            };

            /**
             * Converts this ScreenCaptureRPCResponse to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ScreenCaptureRPCResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ScreenCaptureRPCResponse
             * @function getTypeUrl
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ScreenCaptureRPCResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.ScreenCaptureRPCResponse";
            };

            return ScreenCaptureRPCResponse;
        })();

        return screen_capture;
    })();

    return karna;
})();

export { $root as default };
