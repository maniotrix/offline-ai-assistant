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

    karna.vision = (function() {

        /**
         * Namespace vision.
         * @memberof karna
         * @namespace
         */
        const vision = {};

        vision.GetResultsRequest = (function() {

            /**
             * Properties of a GetResultsRequest.
             * @memberof karna.vision
             * @interface IGetResultsRequest
             * @property {string|null} [projectUuid] GetResultsRequest projectUuid
             * @property {string|null} [commandUuid] GetResultsRequest commandUuid
             * @property {Array.<karna.screen_capture.IRpcScreenshotEvent>|null} [screenshotEvents] GetResultsRequest screenshotEvents
             */

            /**
             * Constructs a new GetResultsRequest.
             * @memberof karna.vision
             * @classdesc Represents a GetResultsRequest.
             * @implements IGetResultsRequest
             * @constructor
             * @param {karna.vision.IGetResultsRequest=} [properties] Properties to set
             */
            function GetResultsRequest(properties) {
                this.screenshotEvents = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * GetResultsRequest projectUuid.
             * @member {string} projectUuid
             * @memberof karna.vision.GetResultsRequest
             * @instance
             */
            GetResultsRequest.prototype.projectUuid = "";

            /**
             * GetResultsRequest commandUuid.
             * @member {string} commandUuid
             * @memberof karna.vision.GetResultsRequest
             * @instance
             */
            GetResultsRequest.prototype.commandUuid = "";

            /**
             * GetResultsRequest screenshotEvents.
             * @member {Array.<karna.screen_capture.IRpcScreenshotEvent>} screenshotEvents
             * @memberof karna.vision.GetResultsRequest
             * @instance
             */
            GetResultsRequest.prototype.screenshotEvents = $util.emptyArray;

            /**
             * Creates a new GetResultsRequest instance using the specified properties.
             * @function create
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {karna.vision.IGetResultsRequest=} [properties] Properties to set
             * @returns {karna.vision.GetResultsRequest} GetResultsRequest instance
             */
            GetResultsRequest.create = function create(properties) {
                return new GetResultsRequest(properties);
            };

            /**
             * Encodes the specified GetResultsRequest message. Does not implicitly {@link karna.vision.GetResultsRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {karna.vision.IGetResultsRequest} message GetResultsRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            GetResultsRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                if (message.screenshotEvents != null && message.screenshotEvents.length)
                    for (let i = 0; i < message.screenshotEvents.length; ++i)
                        $root.karna.screen_capture.RpcScreenshotEvent.encode(message.screenshotEvents[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified GetResultsRequest message, length delimited. Does not implicitly {@link karna.vision.GetResultsRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {karna.vision.IGetResultsRequest} message GetResultsRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            GetResultsRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a GetResultsRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.GetResultsRequest} GetResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            GetResultsRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.GetResultsRequest();
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
             * Decodes a GetResultsRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.GetResultsRequest} GetResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            GetResultsRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a GetResultsRequest message.
             * @function verify
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            GetResultsRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
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
             * Creates a GetResultsRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.GetResultsRequest} GetResultsRequest
             */
            GetResultsRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.GetResultsRequest)
                    return object;
                let message = new $root.karna.vision.GetResultsRequest();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.screenshotEvents) {
                    if (!Array.isArray(object.screenshotEvents))
                        throw TypeError(".karna.vision.GetResultsRequest.screenshotEvents: array expected");
                    message.screenshotEvents = [];
                    for (let i = 0; i < object.screenshotEvents.length; ++i) {
                        if (typeof object.screenshotEvents[i] !== "object")
                            throw TypeError(".karna.vision.GetResultsRequest.screenshotEvents: object expected");
                        message.screenshotEvents[i] = $root.karna.screen_capture.RpcScreenshotEvent.fromObject(object.screenshotEvents[i]);
                    }
                }
                return message;
            };

            /**
             * Creates a plain object from a GetResultsRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {karna.vision.GetResultsRequest} message GetResultsRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            GetResultsRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.screenshotEvents = [];
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.screenshotEvents && message.screenshotEvents.length) {
                    object.screenshotEvents = [];
                    for (let j = 0; j < message.screenshotEvents.length; ++j)
                        object.screenshotEvents[j] = $root.karna.screen_capture.RpcScreenshotEvent.toObject(message.screenshotEvents[j], options);
                }
                return object;
            };

            /**
             * Converts this GetResultsRequest to JSON.
             * @function toJSON
             * @memberof karna.vision.GetResultsRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            GetResultsRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for GetResultsRequest
             * @function getTypeUrl
             * @memberof karna.vision.GetResultsRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            GetResultsRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.GetResultsRequest";
            };

            return GetResultsRequest;
        })();

        vision.UpdateResultsRequest = (function() {

            /**
             * Properties of an UpdateResultsRequest.
             * @memberof karna.vision
             * @interface IUpdateResultsRequest
             * @property {karna.vision.IVisionDetectResultsList|null} [results] UpdateResultsRequest results
             */

            /**
             * Constructs a new UpdateResultsRequest.
             * @memberof karna.vision
             * @classdesc Represents an UpdateResultsRequest.
             * @implements IUpdateResultsRequest
             * @constructor
             * @param {karna.vision.IUpdateResultsRequest=} [properties] Properties to set
             */
            function UpdateResultsRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * UpdateResultsRequest results.
             * @member {karna.vision.IVisionDetectResultsList|null|undefined} results
             * @memberof karna.vision.UpdateResultsRequest
             * @instance
             */
            UpdateResultsRequest.prototype.results = null;

            /**
             * Creates a new UpdateResultsRequest instance using the specified properties.
             * @function create
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {karna.vision.IUpdateResultsRequest=} [properties] Properties to set
             * @returns {karna.vision.UpdateResultsRequest} UpdateResultsRequest instance
             */
            UpdateResultsRequest.create = function create(properties) {
                return new UpdateResultsRequest(properties);
            };

            /**
             * Encodes the specified UpdateResultsRequest message. Does not implicitly {@link karna.vision.UpdateResultsRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {karna.vision.IUpdateResultsRequest} message UpdateResultsRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            UpdateResultsRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.results != null && Object.hasOwnProperty.call(message, "results"))
                    $root.karna.vision.VisionDetectResultsList.encode(message.results, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified UpdateResultsRequest message, length delimited. Does not implicitly {@link karna.vision.UpdateResultsRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {karna.vision.IUpdateResultsRequest} message UpdateResultsRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            UpdateResultsRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes an UpdateResultsRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.UpdateResultsRequest} UpdateResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            UpdateResultsRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.UpdateResultsRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.results = $root.karna.vision.VisionDetectResultsList.decode(reader, reader.uint32());
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
             * Decodes an UpdateResultsRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.UpdateResultsRequest} UpdateResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            UpdateResultsRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies an UpdateResultsRequest message.
             * @function verify
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            UpdateResultsRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.results != null && message.hasOwnProperty("results")) {
                    let error = $root.karna.vision.VisionDetectResultsList.verify(message.results);
                    if (error)
                        return "results." + error;
                }
                return null;
            };

            /**
             * Creates an UpdateResultsRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.UpdateResultsRequest} UpdateResultsRequest
             */
            UpdateResultsRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.UpdateResultsRequest)
                    return object;
                let message = new $root.karna.vision.UpdateResultsRequest();
                if (object.results != null) {
                    if (typeof object.results !== "object")
                        throw TypeError(".karna.vision.UpdateResultsRequest.results: object expected");
                    message.results = $root.karna.vision.VisionDetectResultsList.fromObject(object.results);
                }
                return message;
            };

            /**
             * Creates a plain object from an UpdateResultsRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {karna.vision.UpdateResultsRequest} message UpdateResultsRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            UpdateResultsRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults)
                    object.results = null;
                if (message.results != null && message.hasOwnProperty("results"))
                    object.results = $root.karna.vision.VisionDetectResultsList.toObject(message.results, options);
                return object;
            };

            /**
             * Converts this UpdateResultsRequest to JSON.
             * @function toJSON
             * @memberof karna.vision.UpdateResultsRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            UpdateResultsRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for UpdateResultsRequest
             * @function getTypeUrl
             * @memberof karna.vision.UpdateResultsRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            UpdateResultsRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.UpdateResultsRequest";
            };

            return UpdateResultsRequest;
        })();

        vision.BoundingBox = (function() {

            /**
             * Properties of a BoundingBox.
             * @memberof karna.vision
             * @interface IBoundingBox
             * @property {string|null} [id] BoundingBox id
             * @property {number|null} [x] BoundingBox x
             * @property {number|null} [y] BoundingBox y
             * @property {number|null} [width] BoundingBox width
             * @property {number|null} [height] BoundingBox height
             * @property {string|null} [className] BoundingBox className
             * @property {number|null} [confidence] BoundingBox confidence
             */

            /**
             * Constructs a new BoundingBox.
             * @memberof karna.vision
             * @classdesc Represents a BoundingBox.
             * @implements IBoundingBox
             * @constructor
             * @param {karna.vision.IBoundingBox=} [properties] Properties to set
             */
            function BoundingBox(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * BoundingBox id.
             * @member {string} id
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.id = "";

            /**
             * BoundingBox x.
             * @member {number} x
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.x = 0;

            /**
             * BoundingBox y.
             * @member {number} y
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.y = 0;

            /**
             * BoundingBox width.
             * @member {number} width
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.width = 0;

            /**
             * BoundingBox height.
             * @member {number} height
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.height = 0;

            /**
             * BoundingBox className.
             * @member {string} className
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.className = "";

            /**
             * BoundingBox confidence.
             * @member {number} confidence
             * @memberof karna.vision.BoundingBox
             * @instance
             */
            BoundingBox.prototype.confidence = 0;

            /**
             * Creates a new BoundingBox instance using the specified properties.
             * @function create
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {karna.vision.IBoundingBox=} [properties] Properties to set
             * @returns {karna.vision.BoundingBox} BoundingBox instance
             */
            BoundingBox.create = function create(properties) {
                return new BoundingBox(properties);
            };

            /**
             * Encodes the specified BoundingBox message. Does not implicitly {@link karna.vision.BoundingBox.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {karna.vision.IBoundingBox} message BoundingBox message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            BoundingBox.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
                if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                    writer.uint32(/* id 2, wireType 0 =*/16).int32(message.x);
                if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                    writer.uint32(/* id 3, wireType 0 =*/24).int32(message.y);
                if (message.width != null && Object.hasOwnProperty.call(message, "width"))
                    writer.uint32(/* id 4, wireType 0 =*/32).int32(message.width);
                if (message.height != null && Object.hasOwnProperty.call(message, "height"))
                    writer.uint32(/* id 5, wireType 0 =*/40).int32(message.height);
                if (message.className != null && Object.hasOwnProperty.call(message, "className"))
                    writer.uint32(/* id 6, wireType 2 =*/50).string(message.className);
                if (message.confidence != null && Object.hasOwnProperty.call(message, "confidence"))
                    writer.uint32(/* id 7, wireType 5 =*/61).float(message.confidence);
                return writer;
            };

            /**
             * Encodes the specified BoundingBox message, length delimited. Does not implicitly {@link karna.vision.BoundingBox.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {karna.vision.IBoundingBox} message BoundingBox message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            BoundingBox.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a BoundingBox message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.BoundingBox} BoundingBox
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            BoundingBox.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.BoundingBox();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.id = reader.string();
                            break;
                        }
                    case 2: {
                            message.x = reader.int32();
                            break;
                        }
                    case 3: {
                            message.y = reader.int32();
                            break;
                        }
                    case 4: {
                            message.width = reader.int32();
                            break;
                        }
                    case 5: {
                            message.height = reader.int32();
                            break;
                        }
                    case 6: {
                            message.className = reader.string();
                            break;
                        }
                    case 7: {
                            message.confidence = reader.float();
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
             * Decodes a BoundingBox message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.BoundingBox} BoundingBox
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            BoundingBox.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a BoundingBox message.
             * @function verify
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            BoundingBox.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.id != null && message.hasOwnProperty("id"))
                    if (!$util.isString(message.id))
                        return "id: string expected";
                if (message.x != null && message.hasOwnProperty("x"))
                    if (!$util.isInteger(message.x))
                        return "x: integer expected";
                if (message.y != null && message.hasOwnProperty("y"))
                    if (!$util.isInteger(message.y))
                        return "y: integer expected";
                if (message.width != null && message.hasOwnProperty("width"))
                    if (!$util.isInteger(message.width))
                        return "width: integer expected";
                if (message.height != null && message.hasOwnProperty("height"))
                    if (!$util.isInteger(message.height))
                        return "height: integer expected";
                if (message.className != null && message.hasOwnProperty("className"))
                    if (!$util.isString(message.className))
                        return "className: string expected";
                if (message.confidence != null && message.hasOwnProperty("confidence"))
                    if (typeof message.confidence !== "number")
                        return "confidence: number expected";
                return null;
            };

            /**
             * Creates a BoundingBox message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.BoundingBox} BoundingBox
             */
            BoundingBox.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.BoundingBox)
                    return object;
                let message = new $root.karna.vision.BoundingBox();
                if (object.id != null)
                    message.id = String(object.id);
                if (object.x != null)
                    message.x = object.x | 0;
                if (object.y != null)
                    message.y = object.y | 0;
                if (object.width != null)
                    message.width = object.width | 0;
                if (object.height != null)
                    message.height = object.height | 0;
                if (object.className != null)
                    message.className = String(object.className);
                if (object.confidence != null)
                    message.confidence = Number(object.confidence);
                return message;
            };

            /**
             * Creates a plain object from a BoundingBox message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {karna.vision.BoundingBox} message BoundingBox
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            BoundingBox.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults) {
                    object.id = "";
                    object.x = 0;
                    object.y = 0;
                    object.width = 0;
                    object.height = 0;
                    object.className = "";
                    object.confidence = 0;
                }
                if (message.id != null && message.hasOwnProperty("id"))
                    object.id = message.id;
                if (message.x != null && message.hasOwnProperty("x"))
                    object.x = message.x;
                if (message.y != null && message.hasOwnProperty("y"))
                    object.y = message.y;
                if (message.width != null && message.hasOwnProperty("width"))
                    object.width = message.width;
                if (message.height != null && message.hasOwnProperty("height"))
                    object.height = message.height;
                if (message.className != null && message.hasOwnProperty("className"))
                    object.className = message.className;
                if (message.confidence != null && message.hasOwnProperty("confidence"))
                    object.confidence = options.json && !isFinite(message.confidence) ? String(message.confidence) : message.confidence;
                return object;
            };

            /**
             * Converts this BoundingBox to JSON.
             * @function toJSON
             * @memberof karna.vision.BoundingBox
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            BoundingBox.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for BoundingBox
             * @function getTypeUrl
             * @memberof karna.vision.BoundingBox
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            BoundingBox.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.BoundingBox";
            };

            return BoundingBox;
        })();

        vision.VisionDetectResultModel = (function() {

            /**
             * Properties of a VisionDetectResultModel.
             * @memberof karna.vision
             * @interface IVisionDetectResultModel
             * @property {string|null} [eventId] VisionDetectResultModel eventId
             * @property {string|null} [projectUuid] VisionDetectResultModel projectUuid
             * @property {string|null} [commandUuid] VisionDetectResultModel commandUuid
             * @property {string|null} [timestamp] VisionDetectResultModel timestamp
             * @property {string|null} [description] VisionDetectResultModel description
             * @property {string|null} [originalImagePath] VisionDetectResultModel originalImagePath
             * @property {number|null} [originalWidth] VisionDetectResultModel originalWidth
             * @property {number|null} [originalHeight] VisionDetectResultModel originalHeight
             * @property {boolean|null} [isCropped] VisionDetectResultModel isCropped
             * @property {Array.<karna.vision.IBoundingBox>|null} [mergedUiIconBboxes] VisionDetectResultModel mergedUiIconBboxes
             * @property {Uint8Array|null} [croppedImage] VisionDetectResultModel croppedImage
             * @property {number|null} [croppedWidth] VisionDetectResultModel croppedWidth
             * @property {number|null} [croppedHeight] VisionDetectResultModel croppedHeight
             */

            /**
             * Constructs a new VisionDetectResultModel.
             * @memberof karna.vision
             * @classdesc Represents a VisionDetectResultModel.
             * @implements IVisionDetectResultModel
             * @constructor
             * @param {karna.vision.IVisionDetectResultModel=} [properties] Properties to set
             */
            function VisionDetectResultModel(properties) {
                this.mergedUiIconBboxes = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * VisionDetectResultModel eventId.
             * @member {string} eventId
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.eventId = "";

            /**
             * VisionDetectResultModel projectUuid.
             * @member {string} projectUuid
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.projectUuid = "";

            /**
             * VisionDetectResultModel commandUuid.
             * @member {string} commandUuid
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.commandUuid = "";

            /**
             * VisionDetectResultModel timestamp.
             * @member {string} timestamp
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.timestamp = "";

            /**
             * VisionDetectResultModel description.
             * @member {string} description
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.description = "";

            /**
             * VisionDetectResultModel originalImagePath.
             * @member {string} originalImagePath
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.originalImagePath = "";

            /**
             * VisionDetectResultModel originalWidth.
             * @member {number} originalWidth
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.originalWidth = 0;

            /**
             * VisionDetectResultModel originalHeight.
             * @member {number} originalHeight
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.originalHeight = 0;

            /**
             * VisionDetectResultModel isCropped.
             * @member {boolean} isCropped
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.isCropped = false;

            /**
             * VisionDetectResultModel mergedUiIconBboxes.
             * @member {Array.<karna.vision.IBoundingBox>} mergedUiIconBboxes
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.mergedUiIconBboxes = $util.emptyArray;

            /**
             * VisionDetectResultModel croppedImage.
             * @member {Uint8Array} croppedImage
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.croppedImage = $util.newBuffer([]);

            /**
             * VisionDetectResultModel croppedWidth.
             * @member {number} croppedWidth
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.croppedWidth = 0;

            /**
             * VisionDetectResultModel croppedHeight.
             * @member {number} croppedHeight
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             */
            VisionDetectResultModel.prototype.croppedHeight = 0;

            /**
             * Creates a new VisionDetectResultModel instance using the specified properties.
             * @function create
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {karna.vision.IVisionDetectResultModel=} [properties] Properties to set
             * @returns {karna.vision.VisionDetectResultModel} VisionDetectResultModel instance
             */
            VisionDetectResultModel.create = function create(properties) {
                return new VisionDetectResultModel(properties);
            };

            /**
             * Encodes the specified VisionDetectResultModel message. Does not implicitly {@link karna.vision.VisionDetectResultModel.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {karna.vision.IVisionDetectResultModel} message VisionDetectResultModel message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectResultModel.encode = function encode(message, writer) {
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
                if (message.originalImagePath != null && Object.hasOwnProperty.call(message, "originalImagePath"))
                    writer.uint32(/* id 6, wireType 2 =*/50).string(message.originalImagePath);
                if (message.originalWidth != null && Object.hasOwnProperty.call(message, "originalWidth"))
                    writer.uint32(/* id 7, wireType 0 =*/56).int32(message.originalWidth);
                if (message.originalHeight != null && Object.hasOwnProperty.call(message, "originalHeight"))
                    writer.uint32(/* id 8, wireType 0 =*/64).int32(message.originalHeight);
                if (message.isCropped != null && Object.hasOwnProperty.call(message, "isCropped"))
                    writer.uint32(/* id 9, wireType 0 =*/72).bool(message.isCropped);
                if (message.mergedUiIconBboxes != null && message.mergedUiIconBboxes.length)
                    for (let i = 0; i < message.mergedUiIconBboxes.length; ++i)
                        $root.karna.vision.BoundingBox.encode(message.mergedUiIconBboxes[i], writer.uint32(/* id 10, wireType 2 =*/82).fork()).ldelim();
                if (message.croppedImage != null && Object.hasOwnProperty.call(message, "croppedImage"))
                    writer.uint32(/* id 11, wireType 2 =*/90).bytes(message.croppedImage);
                if (message.croppedWidth != null && Object.hasOwnProperty.call(message, "croppedWidth"))
                    writer.uint32(/* id 12, wireType 0 =*/96).int32(message.croppedWidth);
                if (message.croppedHeight != null && Object.hasOwnProperty.call(message, "croppedHeight"))
                    writer.uint32(/* id 13, wireType 0 =*/104).int32(message.croppedHeight);
                return writer;
            };

            /**
             * Encodes the specified VisionDetectResultModel message, length delimited. Does not implicitly {@link karna.vision.VisionDetectResultModel.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {karna.vision.IVisionDetectResultModel} message VisionDetectResultModel message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectResultModel.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a VisionDetectResultModel message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.VisionDetectResultModel} VisionDetectResultModel
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectResultModel.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.VisionDetectResultModel();
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
                            message.originalImagePath = reader.string();
                            break;
                        }
                    case 7: {
                            message.originalWidth = reader.int32();
                            break;
                        }
                    case 8: {
                            message.originalHeight = reader.int32();
                            break;
                        }
                    case 9: {
                            message.isCropped = reader.bool();
                            break;
                        }
                    case 10: {
                            if (!(message.mergedUiIconBboxes && message.mergedUiIconBboxes.length))
                                message.mergedUiIconBboxes = [];
                            message.mergedUiIconBboxes.push($root.karna.vision.BoundingBox.decode(reader, reader.uint32()));
                            break;
                        }
                    case 11: {
                            message.croppedImage = reader.bytes();
                            break;
                        }
                    case 12: {
                            message.croppedWidth = reader.int32();
                            break;
                        }
                    case 13: {
                            message.croppedHeight = reader.int32();
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
             * Decodes a VisionDetectResultModel message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.VisionDetectResultModel} VisionDetectResultModel
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectResultModel.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a VisionDetectResultModel message.
             * @function verify
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            VisionDetectResultModel.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
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
                if (message.originalImagePath != null && message.hasOwnProperty("originalImagePath"))
                    if (!$util.isString(message.originalImagePath))
                        return "originalImagePath: string expected";
                if (message.originalWidth != null && message.hasOwnProperty("originalWidth"))
                    if (!$util.isInteger(message.originalWidth))
                        return "originalWidth: integer expected";
                if (message.originalHeight != null && message.hasOwnProperty("originalHeight"))
                    if (!$util.isInteger(message.originalHeight))
                        return "originalHeight: integer expected";
                if (message.isCropped != null && message.hasOwnProperty("isCropped"))
                    if (typeof message.isCropped !== "boolean")
                        return "isCropped: boolean expected";
                if (message.mergedUiIconBboxes != null && message.hasOwnProperty("mergedUiIconBboxes")) {
                    if (!Array.isArray(message.mergedUiIconBboxes))
                        return "mergedUiIconBboxes: array expected";
                    for (let i = 0; i < message.mergedUiIconBboxes.length; ++i) {
                        let error = $root.karna.vision.BoundingBox.verify(message.mergedUiIconBboxes[i]);
                        if (error)
                            return "mergedUiIconBboxes." + error;
                    }
                }
                if (message.croppedImage != null && message.hasOwnProperty("croppedImage"))
                    if (!(message.croppedImage && typeof message.croppedImage.length === "number" || $util.isString(message.croppedImage)))
                        return "croppedImage: buffer expected";
                if (message.croppedWidth != null && message.hasOwnProperty("croppedWidth"))
                    if (!$util.isInteger(message.croppedWidth))
                        return "croppedWidth: integer expected";
                if (message.croppedHeight != null && message.hasOwnProperty("croppedHeight"))
                    if (!$util.isInteger(message.croppedHeight))
                        return "croppedHeight: integer expected";
                return null;
            };

            /**
             * Creates a VisionDetectResultModel message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.VisionDetectResultModel} VisionDetectResultModel
             */
            VisionDetectResultModel.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.VisionDetectResultModel)
                    return object;
                let message = new $root.karna.vision.VisionDetectResultModel();
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
                if (object.originalImagePath != null)
                    message.originalImagePath = String(object.originalImagePath);
                if (object.originalWidth != null)
                    message.originalWidth = object.originalWidth | 0;
                if (object.originalHeight != null)
                    message.originalHeight = object.originalHeight | 0;
                if (object.isCropped != null)
                    message.isCropped = Boolean(object.isCropped);
                if (object.mergedUiIconBboxes) {
                    if (!Array.isArray(object.mergedUiIconBboxes))
                        throw TypeError(".karna.vision.VisionDetectResultModel.mergedUiIconBboxes: array expected");
                    message.mergedUiIconBboxes = [];
                    for (let i = 0; i < object.mergedUiIconBboxes.length; ++i) {
                        if (typeof object.mergedUiIconBboxes[i] !== "object")
                            throw TypeError(".karna.vision.VisionDetectResultModel.mergedUiIconBboxes: object expected");
                        message.mergedUiIconBboxes[i] = $root.karna.vision.BoundingBox.fromObject(object.mergedUiIconBboxes[i]);
                    }
                }
                if (object.croppedImage != null)
                    if (typeof object.croppedImage === "string")
                        $util.base64.decode(object.croppedImage, message.croppedImage = $util.newBuffer($util.base64.length(object.croppedImage)), 0);
                    else if (object.croppedImage.length >= 0)
                        message.croppedImage = object.croppedImage;
                if (object.croppedWidth != null)
                    message.croppedWidth = object.croppedWidth | 0;
                if (object.croppedHeight != null)
                    message.croppedHeight = object.croppedHeight | 0;
                return message;
            };

            /**
             * Creates a plain object from a VisionDetectResultModel message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {karna.vision.VisionDetectResultModel} message VisionDetectResultModel
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            VisionDetectResultModel.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.mergedUiIconBboxes = [];
                if (options.defaults) {
                    object.eventId = "";
                    object.projectUuid = "";
                    object.commandUuid = "";
                    object.timestamp = "";
                    object.description = "";
                    object.originalImagePath = "";
                    object.originalWidth = 0;
                    object.originalHeight = 0;
                    object.isCropped = false;
                    if (options.bytes === String)
                        object.croppedImage = "";
                    else {
                        object.croppedImage = [];
                        if (options.bytes !== Array)
                            object.croppedImage = $util.newBuffer(object.croppedImage);
                    }
                    object.croppedWidth = 0;
                    object.croppedHeight = 0;
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
                if (message.originalImagePath != null && message.hasOwnProperty("originalImagePath"))
                    object.originalImagePath = message.originalImagePath;
                if (message.originalWidth != null && message.hasOwnProperty("originalWidth"))
                    object.originalWidth = message.originalWidth;
                if (message.originalHeight != null && message.hasOwnProperty("originalHeight"))
                    object.originalHeight = message.originalHeight;
                if (message.isCropped != null && message.hasOwnProperty("isCropped"))
                    object.isCropped = message.isCropped;
                if (message.mergedUiIconBboxes && message.mergedUiIconBboxes.length) {
                    object.mergedUiIconBboxes = [];
                    for (let j = 0; j < message.mergedUiIconBboxes.length; ++j)
                        object.mergedUiIconBboxes[j] = $root.karna.vision.BoundingBox.toObject(message.mergedUiIconBboxes[j], options);
                }
                if (message.croppedImage != null && message.hasOwnProperty("croppedImage"))
                    object.croppedImage = options.bytes === String ? $util.base64.encode(message.croppedImage, 0, message.croppedImage.length) : options.bytes === Array ? Array.prototype.slice.call(message.croppedImage) : message.croppedImage;
                if (message.croppedWidth != null && message.hasOwnProperty("croppedWidth"))
                    object.croppedWidth = message.croppedWidth;
                if (message.croppedHeight != null && message.hasOwnProperty("croppedHeight"))
                    object.croppedHeight = message.croppedHeight;
                return object;
            };

            /**
             * Converts this VisionDetectResultModel to JSON.
             * @function toJSON
             * @memberof karna.vision.VisionDetectResultModel
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            VisionDetectResultModel.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for VisionDetectResultModel
             * @function getTypeUrl
             * @memberof karna.vision.VisionDetectResultModel
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            VisionDetectResultModel.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.VisionDetectResultModel";
            };

            return VisionDetectResultModel;
        })();

        vision.VisionDetectResultsList = (function() {

            /**
             * Properties of a VisionDetectResultsList.
             * @memberof karna.vision
             * @interface IVisionDetectResultsList
             * @property {string|null} [projectUuid] VisionDetectResultsList projectUuid
             * @property {string|null} [commandUuid] VisionDetectResultsList commandUuid
             * @property {Array.<karna.vision.IVisionDetectResultModel>|null} [results] VisionDetectResultsList results
             */

            /**
             * Constructs a new VisionDetectResultsList.
             * @memberof karna.vision
             * @classdesc Represents a VisionDetectResultsList.
             * @implements IVisionDetectResultsList
             * @constructor
             * @param {karna.vision.IVisionDetectResultsList=} [properties] Properties to set
             */
            function VisionDetectResultsList(properties) {
                this.results = [];
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * VisionDetectResultsList projectUuid.
             * @member {string} projectUuid
             * @memberof karna.vision.VisionDetectResultsList
             * @instance
             */
            VisionDetectResultsList.prototype.projectUuid = "";

            /**
             * VisionDetectResultsList commandUuid.
             * @member {string} commandUuid
             * @memberof karna.vision.VisionDetectResultsList
             * @instance
             */
            VisionDetectResultsList.prototype.commandUuid = "";

            /**
             * VisionDetectResultsList results.
             * @member {Array.<karna.vision.IVisionDetectResultModel>} results
             * @memberof karna.vision.VisionDetectResultsList
             * @instance
             */
            VisionDetectResultsList.prototype.results = $util.emptyArray;

            /**
             * Creates a new VisionDetectResultsList instance using the specified properties.
             * @function create
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {karna.vision.IVisionDetectResultsList=} [properties] Properties to set
             * @returns {karna.vision.VisionDetectResultsList} VisionDetectResultsList instance
             */
            VisionDetectResultsList.create = function create(properties) {
                return new VisionDetectResultsList(properties);
            };

            /**
             * Encodes the specified VisionDetectResultsList message. Does not implicitly {@link karna.vision.VisionDetectResultsList.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {karna.vision.IVisionDetectResultsList} message VisionDetectResultsList message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectResultsList.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                if (message.results != null && message.results.length)
                    for (let i = 0; i < message.results.length; ++i)
                        $root.karna.vision.VisionDetectResultModel.encode(message.results[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified VisionDetectResultsList message, length delimited. Does not implicitly {@link karna.vision.VisionDetectResultsList.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {karna.vision.IVisionDetectResultsList} message VisionDetectResultsList message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectResultsList.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a VisionDetectResultsList message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.VisionDetectResultsList} VisionDetectResultsList
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectResultsList.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.VisionDetectResultsList();
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
                            if (!(message.results && message.results.length))
                                message.results = [];
                            message.results.push($root.karna.vision.VisionDetectResultModel.decode(reader, reader.uint32()));
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
             * Decodes a VisionDetectResultsList message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.VisionDetectResultsList} VisionDetectResultsList
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectResultsList.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a VisionDetectResultsList message.
             * @function verify
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            VisionDetectResultsList.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    if (!$util.isString(message.projectUuid))
                        return "projectUuid: string expected";
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    if (!$util.isString(message.commandUuid))
                        return "commandUuid: string expected";
                if (message.results != null && message.hasOwnProperty("results")) {
                    if (!Array.isArray(message.results))
                        return "results: array expected";
                    for (let i = 0; i < message.results.length; ++i) {
                        let error = $root.karna.vision.VisionDetectResultModel.verify(message.results[i]);
                        if (error)
                            return "results." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a VisionDetectResultsList message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.VisionDetectResultsList} VisionDetectResultsList
             */
            VisionDetectResultsList.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.VisionDetectResultsList)
                    return object;
                let message = new $root.karna.vision.VisionDetectResultsList();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                if (object.results) {
                    if (!Array.isArray(object.results))
                        throw TypeError(".karna.vision.VisionDetectResultsList.results: array expected");
                    message.results = [];
                    for (let i = 0; i < object.results.length; ++i) {
                        if (typeof object.results[i] !== "object")
                            throw TypeError(".karna.vision.VisionDetectResultsList.results: object expected");
                        message.results[i] = $root.karna.vision.VisionDetectResultModel.fromObject(object.results[i]);
                    }
                }
                return message;
            };

            /**
             * Creates a plain object from a VisionDetectResultsList message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {karna.vision.VisionDetectResultsList} message VisionDetectResultsList
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            VisionDetectResultsList.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.arrays || options.defaults)
                    object.results = [];
                if (options.defaults) {
                    object.projectUuid = "";
                    object.commandUuid = "";
                }
                if (message.projectUuid != null && message.hasOwnProperty("projectUuid"))
                    object.projectUuid = message.projectUuid;
                if (message.commandUuid != null && message.hasOwnProperty("commandUuid"))
                    object.commandUuid = message.commandUuid;
                if (message.results && message.results.length) {
                    object.results = [];
                    for (let j = 0; j < message.results.length; ++j)
                        object.results[j] = $root.karna.vision.VisionDetectResultModel.toObject(message.results[j], options);
                }
                return object;
            };

            /**
             * Converts this VisionDetectResultsList to JSON.
             * @function toJSON
             * @memberof karna.vision.VisionDetectResultsList
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            VisionDetectResultsList.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for VisionDetectResultsList
             * @function getTypeUrl
             * @memberof karna.vision.VisionDetectResultsList
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            VisionDetectResultsList.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.VisionDetectResultsList";
            };

            return VisionDetectResultsList;
        })();

        vision.VisionDetectStatus = (function() {

            /**
             * Properties of a VisionDetectStatus.
             * @memberof karna.vision
             * @interface IVisionDetectStatus
             * @property {string|null} [status] VisionDetectStatus status
             * @property {number|null} [screenshotEventsCount] VisionDetectStatus screenshotEventsCount
             * @property {boolean|null} [hasResults] VisionDetectStatus hasResults
             * @property {number|null} [resultsCount] VisionDetectStatus resultsCount
             * @property {boolean|null} [isProcessing] VisionDetectStatus isProcessing
             * @property {string|null} [lastProcessed] VisionDetectStatus lastProcessed
             * @property {string|null} [lastError] VisionDetectStatus lastError
             */

            /**
             * Constructs a new VisionDetectStatus.
             * @memberof karna.vision
             * @classdesc Represents a VisionDetectStatus.
             * @implements IVisionDetectStatus
             * @constructor
             * @param {karna.vision.IVisionDetectStatus=} [properties] Properties to set
             */
            function VisionDetectStatus(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * VisionDetectStatus status.
             * @member {string} status
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.status = "";

            /**
             * VisionDetectStatus screenshotEventsCount.
             * @member {number} screenshotEventsCount
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.screenshotEventsCount = 0;

            /**
             * VisionDetectStatus hasResults.
             * @member {boolean} hasResults
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.hasResults = false;

            /**
             * VisionDetectStatus resultsCount.
             * @member {number} resultsCount
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.resultsCount = 0;

            /**
             * VisionDetectStatus isProcessing.
             * @member {boolean} isProcessing
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.isProcessing = false;

            /**
             * VisionDetectStatus lastProcessed.
             * @member {string} lastProcessed
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.lastProcessed = "";

            /**
             * VisionDetectStatus lastError.
             * @member {string} lastError
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             */
            VisionDetectStatus.prototype.lastError = "";

            /**
             * Creates a new VisionDetectStatus instance using the specified properties.
             * @function create
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {karna.vision.IVisionDetectStatus=} [properties] Properties to set
             * @returns {karna.vision.VisionDetectStatus} VisionDetectStatus instance
             */
            VisionDetectStatus.create = function create(properties) {
                return new VisionDetectStatus(properties);
            };

            /**
             * Encodes the specified VisionDetectStatus message. Does not implicitly {@link karna.vision.VisionDetectStatus.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {karna.vision.IVisionDetectStatus} message VisionDetectStatus message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectStatus.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.status);
                if (message.screenshotEventsCount != null && Object.hasOwnProperty.call(message, "screenshotEventsCount"))
                    writer.uint32(/* id 2, wireType 0 =*/16).int32(message.screenshotEventsCount);
                if (message.hasResults != null && Object.hasOwnProperty.call(message, "hasResults"))
                    writer.uint32(/* id 3, wireType 0 =*/24).bool(message.hasResults);
                if (message.resultsCount != null && Object.hasOwnProperty.call(message, "resultsCount"))
                    writer.uint32(/* id 4, wireType 0 =*/32).int32(message.resultsCount);
                if (message.isProcessing != null && Object.hasOwnProperty.call(message, "isProcessing"))
                    writer.uint32(/* id 5, wireType 0 =*/40).bool(message.isProcessing);
                if (message.lastProcessed != null && Object.hasOwnProperty.call(message, "lastProcessed"))
                    writer.uint32(/* id 6, wireType 2 =*/50).string(message.lastProcessed);
                if (message.lastError != null && Object.hasOwnProperty.call(message, "lastError"))
                    writer.uint32(/* id 7, wireType 2 =*/58).string(message.lastError);
                return writer;
            };

            /**
             * Encodes the specified VisionDetectStatus message, length delimited. Does not implicitly {@link karna.vision.VisionDetectStatus.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {karna.vision.IVisionDetectStatus} message VisionDetectStatus message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectStatus.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a VisionDetectStatus message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.VisionDetectStatus} VisionDetectStatus
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectStatus.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.VisionDetectStatus();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.status = reader.string();
                            break;
                        }
                    case 2: {
                            message.screenshotEventsCount = reader.int32();
                            break;
                        }
                    case 3: {
                            message.hasResults = reader.bool();
                            break;
                        }
                    case 4: {
                            message.resultsCount = reader.int32();
                            break;
                        }
                    case 5: {
                            message.isProcessing = reader.bool();
                            break;
                        }
                    case 6: {
                            message.lastProcessed = reader.string();
                            break;
                        }
                    case 7: {
                            message.lastError = reader.string();
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
             * Decodes a VisionDetectStatus message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.VisionDetectStatus} VisionDetectStatus
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectStatus.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a VisionDetectStatus message.
             * @function verify
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            VisionDetectStatus.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.status != null && message.hasOwnProperty("status"))
                    if (!$util.isString(message.status))
                        return "status: string expected";
                if (message.screenshotEventsCount != null && message.hasOwnProperty("screenshotEventsCount"))
                    if (!$util.isInteger(message.screenshotEventsCount))
                        return "screenshotEventsCount: integer expected";
                if (message.hasResults != null && message.hasOwnProperty("hasResults"))
                    if (typeof message.hasResults !== "boolean")
                        return "hasResults: boolean expected";
                if (message.resultsCount != null && message.hasOwnProperty("resultsCount"))
                    if (!$util.isInteger(message.resultsCount))
                        return "resultsCount: integer expected";
                if (message.isProcessing != null && message.hasOwnProperty("isProcessing"))
                    if (typeof message.isProcessing !== "boolean")
                        return "isProcessing: boolean expected";
                if (message.lastProcessed != null && message.hasOwnProperty("lastProcessed"))
                    if (!$util.isString(message.lastProcessed))
                        return "lastProcessed: string expected";
                if (message.lastError != null && message.hasOwnProperty("lastError"))
                    if (!$util.isString(message.lastError))
                        return "lastError: string expected";
                return null;
            };

            /**
             * Creates a VisionDetectStatus message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.VisionDetectStatus} VisionDetectStatus
             */
            VisionDetectStatus.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.VisionDetectStatus)
                    return object;
                let message = new $root.karna.vision.VisionDetectStatus();
                if (object.status != null)
                    message.status = String(object.status);
                if (object.screenshotEventsCount != null)
                    message.screenshotEventsCount = object.screenshotEventsCount | 0;
                if (object.hasResults != null)
                    message.hasResults = Boolean(object.hasResults);
                if (object.resultsCount != null)
                    message.resultsCount = object.resultsCount | 0;
                if (object.isProcessing != null)
                    message.isProcessing = Boolean(object.isProcessing);
                if (object.lastProcessed != null)
                    message.lastProcessed = String(object.lastProcessed);
                if (object.lastError != null)
                    message.lastError = String(object.lastError);
                return message;
            };

            /**
             * Creates a plain object from a VisionDetectStatus message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {karna.vision.VisionDetectStatus} message VisionDetectStatus
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            VisionDetectStatus.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults) {
                    object.status = "";
                    object.screenshotEventsCount = 0;
                    object.hasResults = false;
                    object.resultsCount = 0;
                    object.isProcessing = false;
                    object.lastProcessed = "";
                    object.lastError = "";
                }
                if (message.status != null && message.hasOwnProperty("status"))
                    object.status = message.status;
                if (message.screenshotEventsCount != null && message.hasOwnProperty("screenshotEventsCount"))
                    object.screenshotEventsCount = message.screenshotEventsCount;
                if (message.hasResults != null && message.hasOwnProperty("hasResults"))
                    object.hasResults = message.hasResults;
                if (message.resultsCount != null && message.hasOwnProperty("resultsCount"))
                    object.resultsCount = message.resultsCount;
                if (message.isProcessing != null && message.hasOwnProperty("isProcessing"))
                    object.isProcessing = message.isProcessing;
                if (message.lastProcessed != null && message.hasOwnProperty("lastProcessed"))
                    object.lastProcessed = message.lastProcessed;
                if (message.lastError != null && message.hasOwnProperty("lastError"))
                    object.lastError = message.lastError;
                return object;
            };

            /**
             * Converts this VisionDetectStatus to JSON.
             * @function toJSON
             * @memberof karna.vision.VisionDetectStatus
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            VisionDetectStatus.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for VisionDetectStatus
             * @function getTypeUrl
             * @memberof karna.vision.VisionDetectStatus
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            VisionDetectStatus.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.VisionDetectStatus";
            };

            return VisionDetectStatus;
        })();

        vision.VisionDetectRPCRequest = (function() {

            /**
             * Properties of a VisionDetectRPCRequest.
             * @memberof karna.vision
             * @interface IVisionDetectRPCRequest
             * @property {karna.vision.IGetResultsRequest|null} [getResultsRequest] VisionDetectRPCRequest getResultsRequest
             * @property {karna.vision.IUpdateResultsRequest|null} [updateResultsRequest] VisionDetectRPCRequest updateResultsRequest
             */

            /**
             * Constructs a new VisionDetectRPCRequest.
             * @memberof karna.vision
             * @classdesc Represents a VisionDetectRPCRequest.
             * @implements IVisionDetectRPCRequest
             * @constructor
             * @param {karna.vision.IVisionDetectRPCRequest=} [properties] Properties to set
             */
            function VisionDetectRPCRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * VisionDetectRPCRequest getResultsRequest.
             * @member {karna.vision.IGetResultsRequest|null|undefined} getResultsRequest
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            VisionDetectRPCRequest.prototype.getResultsRequest = null;

            /**
             * VisionDetectRPCRequest updateResultsRequest.
             * @member {karna.vision.IUpdateResultsRequest|null|undefined} updateResultsRequest
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            VisionDetectRPCRequest.prototype.updateResultsRequest = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * VisionDetectRPCRequest method.
             * @member {"getResultsRequest"|"updateResultsRequest"|undefined} method
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            Object.defineProperty(VisionDetectRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["getResultsRequest", "updateResultsRequest"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new VisionDetectRPCRequest instance using the specified properties.
             * @function create
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {karna.vision.IVisionDetectRPCRequest=} [properties] Properties to set
             * @returns {karna.vision.VisionDetectRPCRequest} VisionDetectRPCRequest instance
             */
            VisionDetectRPCRequest.create = function create(properties) {
                return new VisionDetectRPCRequest(properties);
            };

            /**
             * Encodes the specified VisionDetectRPCRequest message. Does not implicitly {@link karna.vision.VisionDetectRPCRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {karna.vision.IVisionDetectRPCRequest} message VisionDetectRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectRPCRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.getResultsRequest != null && Object.hasOwnProperty.call(message, "getResultsRequest"))
                    $root.karna.vision.GetResultsRequest.encode(message.getResultsRequest, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.updateResultsRequest != null && Object.hasOwnProperty.call(message, "updateResultsRequest"))
                    $root.karna.vision.UpdateResultsRequest.encode(message.updateResultsRequest, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified VisionDetectRPCRequest message, length delimited. Does not implicitly {@link karna.vision.VisionDetectRPCRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {karna.vision.IVisionDetectRPCRequest} message VisionDetectRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectRPCRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a VisionDetectRPCRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.VisionDetectRPCRequest} VisionDetectRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectRPCRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.VisionDetectRPCRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.getResultsRequest = $root.karna.vision.GetResultsRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 2: {
                            message.updateResultsRequest = $root.karna.vision.UpdateResultsRequest.decode(reader, reader.uint32());
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
             * Decodes a VisionDetectRPCRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.VisionDetectRPCRequest} VisionDetectRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectRPCRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a VisionDetectRPCRequest message.
             * @function verify
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            VisionDetectRPCRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.getResultsRequest != null && message.hasOwnProperty("getResultsRequest")) {
                    properties.method = 1;
                    {
                        let error = $root.karna.vision.GetResultsRequest.verify(message.getResultsRequest);
                        if (error)
                            return "getResultsRequest." + error;
                    }
                }
                if (message.updateResultsRequest != null && message.hasOwnProperty("updateResultsRequest")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.vision.UpdateResultsRequest.verify(message.updateResultsRequest);
                        if (error)
                            return "updateResultsRequest." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a VisionDetectRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.VisionDetectRPCRequest} VisionDetectRPCRequest
             */
            VisionDetectRPCRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.VisionDetectRPCRequest)
                    return object;
                let message = new $root.karna.vision.VisionDetectRPCRequest();
                if (object.getResultsRequest != null) {
                    if (typeof object.getResultsRequest !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCRequest.getResultsRequest: object expected");
                    message.getResultsRequest = $root.karna.vision.GetResultsRequest.fromObject(object.getResultsRequest);
                }
                if (object.updateResultsRequest != null) {
                    if (typeof object.updateResultsRequest !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCRequest.updateResultsRequest: object expected");
                    message.updateResultsRequest = $root.karna.vision.UpdateResultsRequest.fromObject(object.updateResultsRequest);
                }
                return message;
            };

            /**
             * Creates a plain object from a VisionDetectRPCRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {karna.vision.VisionDetectRPCRequest} message VisionDetectRPCRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            VisionDetectRPCRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.getResultsRequest != null && message.hasOwnProperty("getResultsRequest")) {
                    object.getResultsRequest = $root.karna.vision.GetResultsRequest.toObject(message.getResultsRequest, options);
                    if (options.oneofs)
                        object.method = "getResultsRequest";
                }
                if (message.updateResultsRequest != null && message.hasOwnProperty("updateResultsRequest")) {
                    object.updateResultsRequest = $root.karna.vision.UpdateResultsRequest.toObject(message.updateResultsRequest, options);
                    if (options.oneofs)
                        object.method = "updateResultsRequest";
                }
                return object;
            };

            /**
             * Converts this VisionDetectRPCRequest to JSON.
             * @function toJSON
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            VisionDetectRPCRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for VisionDetectRPCRequest
             * @function getTypeUrl
             * @memberof karna.vision.VisionDetectRPCRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            VisionDetectRPCRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.VisionDetectRPCRequest";
            };

            return VisionDetectRPCRequest;
        })();

        vision.VisionDetectRPCResponse = (function() {

            /**
             * Properties of a VisionDetectRPCResponse.
             * @memberof karna.vision
             * @interface IVisionDetectRPCResponse
             * @property {karna.vision.IVisionDetectResultsList|null} [results] VisionDetectRPCResponse results
             * @property {karna.vision.IVisionDetectStatus|null} [status] VisionDetectRPCResponse status
             * @property {string|null} [error] VisionDetectRPCResponse error
             */

            /**
             * Constructs a new VisionDetectRPCResponse.
             * @memberof karna.vision
             * @classdesc Represents a VisionDetectRPCResponse.
             * @implements IVisionDetectRPCResponse
             * @constructor
             * @param {karna.vision.IVisionDetectRPCResponse=} [properties] Properties to set
             */
            function VisionDetectRPCResponse(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * VisionDetectRPCResponse results.
             * @member {karna.vision.IVisionDetectResultsList|null|undefined} results
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            VisionDetectRPCResponse.prototype.results = null;

            /**
             * VisionDetectRPCResponse status.
             * @member {karna.vision.IVisionDetectStatus|null|undefined} status
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            VisionDetectRPCResponse.prototype.status = null;

            /**
             * VisionDetectRPCResponse error.
             * @member {string} error
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            VisionDetectRPCResponse.prototype.error = "";

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * VisionDetectRPCResponse response.
             * @member {"results"|"status"|undefined} response
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            Object.defineProperty(VisionDetectRPCResponse.prototype, "response", {
                get: $util.oneOfGetter($oneOfFields = ["results", "status"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new VisionDetectRPCResponse instance using the specified properties.
             * @function create
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {karna.vision.IVisionDetectRPCResponse=} [properties] Properties to set
             * @returns {karna.vision.VisionDetectRPCResponse} VisionDetectRPCResponse instance
             */
            VisionDetectRPCResponse.create = function create(properties) {
                return new VisionDetectRPCResponse(properties);
            };

            /**
             * Encodes the specified VisionDetectRPCResponse message. Does not implicitly {@link karna.vision.VisionDetectRPCResponse.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {karna.vision.IVisionDetectRPCResponse} message VisionDetectRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectRPCResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.results != null && Object.hasOwnProperty.call(message, "results"))
                    $root.karna.vision.VisionDetectResultsList.encode(message.results, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                    $root.karna.vision.VisionDetectStatus.encode(message.status, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.error);
                return writer;
            };

            /**
             * Encodes the specified VisionDetectRPCResponse message, length delimited. Does not implicitly {@link karna.vision.VisionDetectRPCResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {karna.vision.IVisionDetectRPCResponse} message VisionDetectRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            VisionDetectRPCResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a VisionDetectRPCResponse message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.VisionDetectRPCResponse} VisionDetectRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectRPCResponse.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.VisionDetectRPCResponse();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.results = $root.karna.vision.VisionDetectResultsList.decode(reader, reader.uint32());
                            break;
                        }
                    case 2: {
                            message.status = $root.karna.vision.VisionDetectStatus.decode(reader, reader.uint32());
                            break;
                        }
                    case 3: {
                            message.error = reader.string();
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
             * Decodes a VisionDetectRPCResponse message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.VisionDetectRPCResponse} VisionDetectRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            VisionDetectRPCResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a VisionDetectRPCResponse message.
             * @function verify
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            VisionDetectRPCResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.results != null && message.hasOwnProperty("results")) {
                    properties.response = 1;
                    {
                        let error = $root.karna.vision.VisionDetectResultsList.verify(message.results);
                        if (error)
                            return "results." + error;
                    }
                }
                if (message.status != null && message.hasOwnProperty("status")) {
                    if (properties.response === 1)
                        return "response: multiple values";
                    properties.response = 1;
                    {
                        let error = $root.karna.vision.VisionDetectStatus.verify(message.status);
                        if (error)
                            return "status." + error;
                    }
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    if (!$util.isString(message.error))
                        return "error: string expected";
                return null;
            };

            /**
             * Creates a VisionDetectRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.VisionDetectRPCResponse} VisionDetectRPCResponse
             */
            VisionDetectRPCResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.VisionDetectRPCResponse)
                    return object;
                let message = new $root.karna.vision.VisionDetectRPCResponse();
                if (object.results != null) {
                    if (typeof object.results !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCResponse.results: object expected");
                    message.results = $root.karna.vision.VisionDetectResultsList.fromObject(object.results);
                }
                if (object.status != null) {
                    if (typeof object.status !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCResponse.status: object expected");
                    message.status = $root.karna.vision.VisionDetectStatus.fromObject(object.status);
                }
                if (object.error != null)
                    message.error = String(object.error);
                return message;
            };

            /**
             * Creates a plain object from a VisionDetectRPCResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {karna.vision.VisionDetectRPCResponse} message VisionDetectRPCResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            VisionDetectRPCResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults)
                    object.error = "";
                if (message.results != null && message.hasOwnProperty("results")) {
                    object.results = $root.karna.vision.VisionDetectResultsList.toObject(message.results, options);
                    if (options.oneofs)
                        object.response = "results";
                }
                if (message.status != null && message.hasOwnProperty("status")) {
                    object.status = $root.karna.vision.VisionDetectStatus.toObject(message.status, options);
                    if (options.oneofs)
                        object.response = "status";
                }
                if (message.error != null && message.hasOwnProperty("error"))
                    object.error = message.error;
                return object;
            };

            /**
             * Converts this VisionDetectRPCResponse to JSON.
             * @function toJSON
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            VisionDetectRPCResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for VisionDetectRPCResponse
             * @function getTypeUrl
             * @memberof karna.vision.VisionDetectRPCResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            VisionDetectRPCResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.VisionDetectRPCResponse";
            };

            return VisionDetectRPCResponse;
        })();

        return vision;
    })();

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

        screen_capture.CaptureCacheRequest = (function() {

            /**
             * Properties of a CaptureCacheRequest.
             * @memberof karna.screen_capture
             * @interface ICaptureCacheRequest
             * @property {string|null} [projectUuid] CaptureCacheRequest projectUuid
             * @property {string|null} [commandUuid] CaptureCacheRequest commandUuid
             */

            /**
             * Constructs a new CaptureCacheRequest.
             * @memberof karna.screen_capture
             * @classdesc Represents a CaptureCacheRequest.
             * @implements ICaptureCacheRequest
             * @constructor
             * @param {karna.screen_capture.ICaptureCacheRequest=} [properties] Properties to set
             */
            function CaptureCacheRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CaptureCacheRequest projectUuid.
             * @member {string} projectUuid
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @instance
             */
            CaptureCacheRequest.prototype.projectUuid = "";

            /**
             * CaptureCacheRequest commandUuid.
             * @member {string} commandUuid
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @instance
             */
            CaptureCacheRequest.prototype.commandUuid = "";

            /**
             * Creates a new CaptureCacheRequest instance using the specified properties.
             * @function create
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {karna.screen_capture.ICaptureCacheRequest=} [properties] Properties to set
             * @returns {karna.screen_capture.CaptureCacheRequest} CaptureCacheRequest instance
             */
            CaptureCacheRequest.create = function create(properties) {
                return new CaptureCacheRequest(properties);
            };

            /**
             * Encodes the specified CaptureCacheRequest message. Does not implicitly {@link karna.screen_capture.CaptureCacheRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {karna.screen_capture.ICaptureCacheRequest} message CaptureCacheRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureCacheRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.projectUuid != null && Object.hasOwnProperty.call(message, "projectUuid"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.projectUuid);
                if (message.commandUuid != null && Object.hasOwnProperty.call(message, "commandUuid"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.commandUuid);
                return writer;
            };

            /**
             * Encodes the specified CaptureCacheRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureCacheRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {karna.screen_capture.ICaptureCacheRequest} message CaptureCacheRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CaptureCacheRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CaptureCacheRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.screen_capture.CaptureCacheRequest} CaptureCacheRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureCacheRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.screen_capture.CaptureCacheRequest();
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
             * Decodes a CaptureCacheRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.screen_capture.CaptureCacheRequest} CaptureCacheRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CaptureCacheRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CaptureCacheRequest message.
             * @function verify
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CaptureCacheRequest.verify = function verify(message) {
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
             * Creates a CaptureCacheRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.screen_capture.CaptureCacheRequest} CaptureCacheRequest
             */
            CaptureCacheRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.screen_capture.CaptureCacheRequest)
                    return object;
                let message = new $root.karna.screen_capture.CaptureCacheRequest();
                if (object.projectUuid != null)
                    message.projectUuid = String(object.projectUuid);
                if (object.commandUuid != null)
                    message.commandUuid = String(object.commandUuid);
                return message;
            };

            /**
             * Creates a plain object from a CaptureCacheRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {karna.screen_capture.CaptureCacheRequest} message CaptureCacheRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CaptureCacheRequest.toObject = function toObject(message, options) {
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
             * Converts this CaptureCacheRequest to JSON.
             * @function toJSON
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CaptureCacheRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CaptureCacheRequest
             * @function getTypeUrl
             * @memberof karna.screen_capture.CaptureCacheRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CaptureCacheRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.screen_capture.CaptureCacheRequest";
            };

            return CaptureCacheRequest;
        })();

        screen_capture.CaptureUpdateRequest = (function() {

            /**
             * Properties of a CaptureUpdateRequest.
             * @memberof karna.screen_capture
             * @interface ICaptureUpdateRequest
             * @property {string|null} [projectUuid] CaptureUpdateRequest projectUuid
             * @property {string|null} [commandUuid] CaptureUpdateRequest commandUuid
             * @property {string|null} [message] CaptureUpdateRequest message
             * @property {Array.<karna.screen_capture.IRpcScreenshotEvent>|null} [screenshotEvents] CaptureUpdateRequest screenshotEvents
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
                this.screenshotEvents = [];
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
             * CaptureUpdateRequest screenshotEvents.
             * @member {Array.<karna.screen_capture.IRpcScreenshotEvent>} screenshotEvents
             * @memberof karna.screen_capture.CaptureUpdateRequest
             * @instance
             */
            CaptureUpdateRequest.prototype.screenshotEvents = $util.emptyArray;

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
                if (message.screenshotEvents != null && message.screenshotEvents.length)
                    for (let i = 0; i < message.screenshotEvents.length; ++i)
                        $root.karna.screen_capture.RpcScreenshotEvent.encode(message.screenshotEvents[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
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
                if (object.screenshotEvents) {
                    if (!Array.isArray(object.screenshotEvents))
                        throw TypeError(".karna.screen_capture.CaptureUpdateRequest.screenshotEvents: array expected");
                    message.screenshotEvents = [];
                    for (let i = 0; i < object.screenshotEvents.length; ++i) {
                        if (typeof object.screenshotEvents[i] !== "object")
                            throw TypeError(".karna.screen_capture.CaptureUpdateRequest.screenshotEvents: object expected");
                        message.screenshotEvents[i] = $root.karna.screen_capture.RpcScreenshotEvent.fromObject(object.screenshotEvents[i]);
                    }
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

        screen_capture.ScreenCaptureRPCRequest = (function() {

            /**
             * Properties of a ScreenCaptureRPCRequest.
             * @memberof karna.screen_capture
             * @interface IScreenCaptureRPCRequest
             * @property {karna.screen_capture.ICaptureRequest|null} [startCapture] ScreenCaptureRPCRequest startCapture
             * @property {karna.screen_capture.ICaptureRequest|null} [stopCapture] ScreenCaptureRPCRequest stopCapture
             * @property {karna.screen_capture.ICaptureUpdateRequest|null} [updateCapture] ScreenCaptureRPCRequest updateCapture
             * @property {karna.screen_capture.ICaptureCacheRequest|null} [getCache] ScreenCaptureRPCRequest getCache
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

            /**
             * ScreenCaptureRPCRequest getCache.
             * @member {karna.screen_capture.ICaptureCacheRequest|null|undefined} getCache
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            ScreenCaptureRPCRequest.prototype.getCache = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * ScreenCaptureRPCRequest method.
             * @member {"startCapture"|"stopCapture"|"updateCapture"|"getCache"|undefined} method
             * @memberof karna.screen_capture.ScreenCaptureRPCRequest
             * @instance
             */
            Object.defineProperty(ScreenCaptureRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["startCapture", "stopCapture", "updateCapture", "getCache"]),
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
                if (message.getCache != null && Object.hasOwnProperty.call(message, "getCache"))
                    $root.karna.screen_capture.CaptureCacheRequest.encode(message.getCache, writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
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
                    case 4: {
                            message.getCache = $root.karna.screen_capture.CaptureCacheRequest.decode(reader, reader.uint32());
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
                if (message.getCache != null && message.hasOwnProperty("getCache")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.screen_capture.CaptureCacheRequest.verify(message.getCache);
                        if (error)
                            return "getCache." + error;
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
                if (object.getCache != null) {
                    if (typeof object.getCache !== "object")
                        throw TypeError(".karna.screen_capture.ScreenCaptureRPCRequest.getCache: object expected");
                    message.getCache = $root.karna.screen_capture.CaptureCacheRequest.fromObject(object.getCache);
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
                if (message.getCache != null && message.hasOwnProperty("getCache")) {
                    object.getCache = $root.karna.screen_capture.CaptureCacheRequest.toObject(message.getCache, options);
                    if (options.oneofs)
                        object.method = "getCache";
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
             * @property {string|null} [mouseEventToolTip] RpcScreenshotEvent mouseEventToolTip
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

            /**
             * RpcScreenshotEvent mouseEventToolTip.
             * @member {string|null|undefined} mouseEventToolTip
             * @memberof karna.screen_capture.RpcScreenshotEvent
             * @instance
             */
            RpcScreenshotEvent.prototype.mouseEventToolTip = null;

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

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(RpcScreenshotEvent.prototype, "_mouseEventToolTip", {
                get: $util.oneOfGetter($oneOfFields = ["mouseEventToolTip"]),
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
                if (message.mouseEventToolTip != null && Object.hasOwnProperty.call(message, "mouseEventToolTip"))
                    writer.uint32(/* id 13, wireType 2 =*/106).string(message.mouseEventToolTip);
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
                    case 13: {
                            message.mouseEventToolTip = reader.string();
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
                if (message.mouseEventToolTip != null && message.hasOwnProperty("mouseEventToolTip")) {
                    properties._mouseEventToolTip = 1;
                    if (!$util.isString(message.mouseEventToolTip))
                        return "mouseEventToolTip: string expected";
                }
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
                if (object.mouseEventToolTip != null)
                    message.mouseEventToolTip = String(object.mouseEventToolTip);
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
                if (message.mouseEventToolTip != null && message.hasOwnProperty("mouseEventToolTip")) {
                    object.mouseEventToolTip = message.mouseEventToolTip;
                    if (options.oneofs)
                        object._mouseEventToolTip = "mouseEventToolTip";
                }
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

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * ScreenCaptureRPCResponse type.
             * @member {"captureResponse"|"error"|undefined} type
             * @memberof karna.screen_capture.ScreenCaptureRPCResponse
             * @instance
             */
            Object.defineProperty(ScreenCaptureRPCResponse.prototype, "type", {
                get: $util.oneOfGetter($oneOfFields = ["captureResponse", "error"]),
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
