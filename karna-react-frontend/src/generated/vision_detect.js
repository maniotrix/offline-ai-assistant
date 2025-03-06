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

        vision.ProcessRequest = (function() {

            /**
             * Properties of a ProcessRequest.
             * @memberof karna.vision
             * @interface IProcessRequest
             * @property {boolean|null} [shouldCrop] ProcessRequest shouldCrop
             */

            /**
             * Constructs a new ProcessRequest.
             * @memberof karna.vision
             * @classdesc Represents a ProcessRequest.
             * @implements IProcessRequest
             * @constructor
             * @param {karna.vision.IProcessRequest=} [properties] Properties to set
             */
            function ProcessRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ProcessRequest shouldCrop.
             * @member {boolean} shouldCrop
             * @memberof karna.vision.ProcessRequest
             * @instance
             */
            ProcessRequest.prototype.shouldCrop = false;

            /**
             * Creates a new ProcessRequest instance using the specified properties.
             * @function create
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {karna.vision.IProcessRequest=} [properties] Properties to set
             * @returns {karna.vision.ProcessRequest} ProcessRequest instance
             */
            ProcessRequest.create = function create(properties) {
                return new ProcessRequest(properties);
            };

            /**
             * Encodes the specified ProcessRequest message. Does not implicitly {@link karna.vision.ProcessRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {karna.vision.IProcessRequest} message ProcessRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ProcessRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.shouldCrop != null && Object.hasOwnProperty.call(message, "shouldCrop"))
                    writer.uint32(/* id 1, wireType 0 =*/8).bool(message.shouldCrop);
                return writer;
            };

            /**
             * Encodes the specified ProcessRequest message, length delimited. Does not implicitly {@link karna.vision.ProcessRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {karna.vision.IProcessRequest} message ProcessRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ProcessRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a ProcessRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.ProcessRequest} ProcessRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ProcessRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.ProcessRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.shouldCrop = reader.bool();
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
             * Decodes a ProcessRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.ProcessRequest} ProcessRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ProcessRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a ProcessRequest message.
             * @function verify
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ProcessRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.shouldCrop != null && message.hasOwnProperty("shouldCrop"))
                    if (typeof message.shouldCrop !== "boolean")
                        return "shouldCrop: boolean expected";
                return null;
            };

            /**
             * Creates a ProcessRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.ProcessRequest} ProcessRequest
             */
            ProcessRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.ProcessRequest)
                    return object;
                let message = new $root.karna.vision.ProcessRequest();
                if (object.shouldCrop != null)
                    message.shouldCrop = Boolean(object.shouldCrop);
                return message;
            };

            /**
             * Creates a plain object from a ProcessRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {karna.vision.ProcessRequest} message ProcessRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ProcessRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults)
                    object.shouldCrop = false;
                if (message.shouldCrop != null && message.hasOwnProperty("shouldCrop"))
                    object.shouldCrop = message.shouldCrop;
                return object;
            };

            /**
             * Converts this ProcessRequest to JSON.
             * @function toJSON
             * @memberof karna.vision.ProcessRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ProcessRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ProcessRequest
             * @function getTypeUrl
             * @memberof karna.vision.ProcessRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ProcessRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.ProcessRequest";
            };

            return ProcessRequest;
        })();

        vision.GetResultsRequest = (function() {

            /**
             * Properties of a GetResultsRequest.
             * @memberof karna.vision
             * @interface IGetResultsRequest
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
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

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
                return new $root.karna.vision.GetResultsRequest();
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
            GetResultsRequest.toObject = function toObject() {
                return {};
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

        vision.ExportRequest = (function() {

            /**
             * Properties of an ExportRequest.
             * @memberof karna.vision
             * @interface IExportRequest
             * @property {string|null} [outputDir] ExportRequest outputDir
             */

            /**
             * Constructs a new ExportRequest.
             * @memberof karna.vision
             * @classdesc Represents an ExportRequest.
             * @implements IExportRequest
             * @constructor
             * @param {karna.vision.IExportRequest=} [properties] Properties to set
             */
            function ExportRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * ExportRequest outputDir.
             * @member {string} outputDir
             * @memberof karna.vision.ExportRequest
             * @instance
             */
            ExportRequest.prototype.outputDir = "";

            /**
             * Creates a new ExportRequest instance using the specified properties.
             * @function create
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {karna.vision.IExportRequest=} [properties] Properties to set
             * @returns {karna.vision.ExportRequest} ExportRequest instance
             */
            ExportRequest.create = function create(properties) {
                return new ExportRequest(properties);
            };

            /**
             * Encodes the specified ExportRequest message. Does not implicitly {@link karna.vision.ExportRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {karna.vision.IExportRequest} message ExportRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ExportRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.outputDir != null && Object.hasOwnProperty.call(message, "outputDir"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.outputDir);
                return writer;
            };

            /**
             * Encodes the specified ExportRequest message, length delimited. Does not implicitly {@link karna.vision.ExportRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {karna.vision.IExportRequest} message ExportRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            ExportRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes an ExportRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.vision.ExportRequest} ExportRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ExportRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.vision.ExportRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.outputDir = reader.string();
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
             * Decodes an ExportRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.vision.ExportRequest} ExportRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            ExportRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies an ExportRequest message.
             * @function verify
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            ExportRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.outputDir != null && message.hasOwnProperty("outputDir"))
                    if (!$util.isString(message.outputDir))
                        return "outputDir: string expected";
                return null;
            };

            /**
             * Creates an ExportRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.vision.ExportRequest} ExportRequest
             */
            ExportRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.vision.ExportRequest)
                    return object;
                let message = new $root.karna.vision.ExportRequest();
                if (object.outputDir != null)
                    message.outputDir = String(object.outputDir);
                return message;
            };

            /**
             * Creates a plain object from an ExportRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {karna.vision.ExportRequest} message ExportRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            ExportRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults)
                    object.outputDir = "";
                if (message.outputDir != null && message.hasOwnProperty("outputDir"))
                    object.outputDir = message.outputDir;
                return object;
            };

            /**
             * Converts this ExportRequest to JSON.
             * @function toJSON
             * @memberof karna.vision.ExportRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            ExportRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for ExportRequest
             * @function getTypeUrl
             * @memberof karna.vision.ExportRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            ExportRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.vision.ExportRequest";
            };

            return ExportRequest;
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
             * @property {karna.vision.IProcessRequest|null} [processRequest] VisionDetectRPCRequest processRequest
             * @property {karna.vision.IGetResultsRequest|null} [getResultsRequest] VisionDetectRPCRequest getResultsRequest
             * @property {karna.vision.IExportRequest|null} [exportRequest] VisionDetectRPCRequest exportRequest
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
             * VisionDetectRPCRequest processRequest.
             * @member {karna.vision.IProcessRequest|null|undefined} processRequest
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            VisionDetectRPCRequest.prototype.processRequest = null;

            /**
             * VisionDetectRPCRequest getResultsRequest.
             * @member {karna.vision.IGetResultsRequest|null|undefined} getResultsRequest
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            VisionDetectRPCRequest.prototype.getResultsRequest = null;

            /**
             * VisionDetectRPCRequest exportRequest.
             * @member {karna.vision.IExportRequest|null|undefined} exportRequest
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            VisionDetectRPCRequest.prototype.exportRequest = null;

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
             * @member {"processRequest"|"getResultsRequest"|"exportRequest"|"updateResultsRequest"|undefined} method
             * @memberof karna.vision.VisionDetectRPCRequest
             * @instance
             */
            Object.defineProperty(VisionDetectRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["processRequest", "getResultsRequest", "exportRequest", "updateResultsRequest"]),
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
                if (message.processRequest != null && Object.hasOwnProperty.call(message, "processRequest"))
                    $root.karna.vision.ProcessRequest.encode(message.processRequest, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.getResultsRequest != null && Object.hasOwnProperty.call(message, "getResultsRequest"))
                    $root.karna.vision.GetResultsRequest.encode(message.getResultsRequest, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
                if (message.exportRequest != null && Object.hasOwnProperty.call(message, "exportRequest"))
                    $root.karna.vision.ExportRequest.encode(message.exportRequest, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
                if (message.updateResultsRequest != null && Object.hasOwnProperty.call(message, "updateResultsRequest"))
                    $root.karna.vision.UpdateResultsRequest.encode(message.updateResultsRequest, writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
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
                            message.processRequest = $root.karna.vision.ProcessRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 2: {
                            message.getResultsRequest = $root.karna.vision.GetResultsRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 3: {
                            message.exportRequest = $root.karna.vision.ExportRequest.decode(reader, reader.uint32());
                            break;
                        }
                    case 4: {
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
                if (message.processRequest != null && message.hasOwnProperty("processRequest")) {
                    properties.method = 1;
                    {
                        let error = $root.karna.vision.ProcessRequest.verify(message.processRequest);
                        if (error)
                            return "processRequest." + error;
                    }
                }
                if (message.getResultsRequest != null && message.hasOwnProperty("getResultsRequest")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.vision.GetResultsRequest.verify(message.getResultsRequest);
                        if (error)
                            return "getResultsRequest." + error;
                    }
                }
                if (message.exportRequest != null && message.hasOwnProperty("exportRequest")) {
                    if (properties.method === 1)
                        return "method: multiple values";
                    properties.method = 1;
                    {
                        let error = $root.karna.vision.ExportRequest.verify(message.exportRequest);
                        if (error)
                            return "exportRequest." + error;
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
                if (object.processRequest != null) {
                    if (typeof object.processRequest !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCRequest.processRequest: object expected");
                    message.processRequest = $root.karna.vision.ProcessRequest.fromObject(object.processRequest);
                }
                if (object.getResultsRequest != null) {
                    if (typeof object.getResultsRequest !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCRequest.getResultsRequest: object expected");
                    message.getResultsRequest = $root.karna.vision.GetResultsRequest.fromObject(object.getResultsRequest);
                }
                if (object.exportRequest != null) {
                    if (typeof object.exportRequest !== "object")
                        throw TypeError(".karna.vision.VisionDetectRPCRequest.exportRequest: object expected");
                    message.exportRequest = $root.karna.vision.ExportRequest.fromObject(object.exportRequest);
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
                if (message.processRequest != null && message.hasOwnProperty("processRequest")) {
                    object.processRequest = $root.karna.vision.ProcessRequest.toObject(message.processRequest, options);
                    if (options.oneofs)
                        object.method = "processRequest";
                }
                if (message.getResultsRequest != null && message.hasOwnProperty("getResultsRequest")) {
                    object.getResultsRequest = $root.karna.vision.GetResultsRequest.toObject(message.getResultsRequest, options);
                    if (options.oneofs)
                        object.method = "getResultsRequest";
                }
                if (message.exportRequest != null && message.hasOwnProperty("exportRequest")) {
                    object.exportRequest = $root.karna.vision.ExportRequest.toObject(message.exportRequest, options);
                    if (options.oneofs)
                        object.method = "exportRequest";
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
             * @property {string|null} [exportPath] VisionDetectRPCResponse exportPath
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
             * VisionDetectRPCResponse exportPath.
             * @member {string|null|undefined} exportPath
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            VisionDetectRPCResponse.prototype.exportPath = null;

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
             * @member {"results"|"status"|"exportPath"|undefined} response
             * @memberof karna.vision.VisionDetectRPCResponse
             * @instance
             */
            Object.defineProperty(VisionDetectRPCResponse.prototype, "response", {
                get: $util.oneOfGetter($oneOfFields = ["results", "status", "exportPath"]),
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
                if (message.exportPath != null && Object.hasOwnProperty.call(message, "exportPath"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.exportPath);
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 4, wireType 2 =*/34).string(message.error);
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
                            message.exportPath = reader.string();
                            break;
                        }
                    case 4: {
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
                if (message.exportPath != null && message.hasOwnProperty("exportPath")) {
                    if (properties.response === 1)
                        return "response: multiple values";
                    properties.response = 1;
                    if (!$util.isString(message.exportPath))
                        return "exportPath: string expected";
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
                if (object.exportPath != null)
                    message.exportPath = String(object.exportPath);
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
                if (message.exportPath != null && message.hasOwnProperty("exportPath")) {
                    object.exportPath = message.exportPath;
                    if (options.oneofs)
                        object.response = "exportPath";
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

    return karna;
})();

export { $root as default };
