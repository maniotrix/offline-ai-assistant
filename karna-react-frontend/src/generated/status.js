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

    karna.status = (function() {

        /**
         * Namespace status.
         * @memberof karna
         * @namespace
         */
        const status = {};

        status.StatusRequest = (function() {

            /**
             * Properties of a StatusRequest.
             * @memberof karna.status
             * @interface IStatusRequest
             */

            /**
             * Constructs a new StatusRequest.
             * @memberof karna.status
             * @classdesc Represents a StatusRequest.
             * @implements IStatusRequest
             * @constructor
             * @param {karna.status.IStatusRequest=} [properties] Properties to set
             */
            function StatusRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * Creates a new StatusRequest instance using the specified properties.
             * @function create
             * @memberof karna.status.StatusRequest
             * @static
             * @param {karna.status.IStatusRequest=} [properties] Properties to set
             * @returns {karna.status.StatusRequest} StatusRequest instance
             */
            StatusRequest.create = function create(properties) {
                return new StatusRequest(properties);
            };

            /**
             * Encodes the specified StatusRequest message. Does not implicitly {@link karna.status.StatusRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.status.StatusRequest
             * @static
             * @param {karna.status.IStatusRequest} message StatusRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                return writer;
            };

            /**
             * Encodes the specified StatusRequest message, length delimited. Does not implicitly {@link karna.status.StatusRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.status.StatusRequest
             * @static
             * @param {karna.status.IStatusRequest} message StatusRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a StatusRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.status.StatusRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.status.StatusRequest} StatusRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.status.StatusRequest();
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
             * Decodes a StatusRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.status.StatusRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.status.StatusRequest} StatusRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a StatusRequest message.
             * @function verify
             * @memberof karna.status.StatusRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            StatusRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                return null;
            };

            /**
             * Creates a StatusRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.status.StatusRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.status.StatusRequest} StatusRequest
             */
            StatusRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.status.StatusRequest)
                    return object;
                return new $root.karna.status.StatusRequest();
            };

            /**
             * Creates a plain object from a StatusRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.status.StatusRequest
             * @static
             * @param {karna.status.StatusRequest} message StatusRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            StatusRequest.toObject = function toObject() {
                return {};
            };

            /**
             * Converts this StatusRequest to JSON.
             * @function toJSON
             * @memberof karna.status.StatusRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            StatusRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for StatusRequest
             * @function getTypeUrl
             * @memberof karna.status.StatusRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            StatusRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.status.StatusRequest";
            };

            return StatusRequest;
        })();

        status.StatusRPCRequest = (function() {

            /**
             * Properties of a StatusRPCRequest.
             * @memberof karna.status
             * @interface IStatusRPCRequest
             * @property {karna.status.IStatusRequest|null} [getStatus] StatusRPCRequest getStatus
             */

            /**
             * Constructs a new StatusRPCRequest.
             * @memberof karna.status
             * @classdesc Represents a StatusRPCRequest.
             * @implements IStatusRPCRequest
             * @constructor
             * @param {karna.status.IStatusRPCRequest=} [properties] Properties to set
             */
            function StatusRPCRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * StatusRPCRequest getStatus.
             * @member {karna.status.IStatusRequest|null|undefined} getStatus
             * @memberof karna.status.StatusRPCRequest
             * @instance
             */
            StatusRPCRequest.prototype.getStatus = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * StatusRPCRequest method.
             * @member {"getStatus"|undefined} method
             * @memberof karna.status.StatusRPCRequest
             * @instance
             */
            Object.defineProperty(StatusRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["getStatus"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new StatusRPCRequest instance using the specified properties.
             * @function create
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {karna.status.IStatusRPCRequest=} [properties] Properties to set
             * @returns {karna.status.StatusRPCRequest} StatusRPCRequest instance
             */
            StatusRPCRequest.create = function create(properties) {
                return new StatusRPCRequest(properties);
            };

            /**
             * Encodes the specified StatusRPCRequest message. Does not implicitly {@link karna.status.StatusRPCRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {karna.status.IStatusRPCRequest} message StatusRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRPCRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.getStatus != null && Object.hasOwnProperty.call(message, "getStatus"))
                    $root.karna.status.StatusRequest.encode(message.getStatus, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified StatusRPCRequest message, length delimited. Does not implicitly {@link karna.status.StatusRPCRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {karna.status.IStatusRPCRequest} message StatusRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRPCRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a StatusRPCRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.status.StatusRPCRequest} StatusRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRPCRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.status.StatusRPCRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.getStatus = $root.karna.status.StatusRequest.decode(reader, reader.uint32());
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
             * Decodes a StatusRPCRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.status.StatusRPCRequest} StatusRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRPCRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a StatusRPCRequest message.
             * @function verify
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            StatusRPCRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.getStatus != null && message.hasOwnProperty("getStatus")) {
                    properties.method = 1;
                    {
                        let error = $root.karna.status.StatusRequest.verify(message.getStatus);
                        if (error)
                            return "getStatus." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a StatusRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.status.StatusRPCRequest} StatusRPCRequest
             */
            StatusRPCRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.status.StatusRPCRequest)
                    return object;
                let message = new $root.karna.status.StatusRPCRequest();
                if (object.getStatus != null) {
                    if (typeof object.getStatus !== "object")
                        throw TypeError(".karna.status.StatusRPCRequest.getStatus: object expected");
                    message.getStatus = $root.karna.status.StatusRequest.fromObject(object.getStatus);
                }
                return message;
            };

            /**
             * Creates a plain object from a StatusRPCRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {karna.status.StatusRPCRequest} message StatusRPCRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            StatusRPCRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.getStatus != null && message.hasOwnProperty("getStatus")) {
                    object.getStatus = $root.karna.status.StatusRequest.toObject(message.getStatus, options);
                    if (options.oneofs)
                        object.method = "getStatus";
                }
                return object;
            };

            /**
             * Converts this StatusRPCRequest to JSON.
             * @function toJSON
             * @memberof karna.status.StatusRPCRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            StatusRPCRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for StatusRPCRequest
             * @function getTypeUrl
             * @memberof karna.status.StatusRPCRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            StatusRPCRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.status.StatusRPCRequest";
            };

            return StatusRPCRequest;
        })();

        status.StatusResult = (function() {

            /**
             * Properties of a StatusResult.
             * @memberof karna.status
             * @interface IStatusResult
             * @property {string|null} [vision] StatusResult vision
             * @property {string|null} [language] StatusResult language
             * @property {string|null} [command] StatusResult command
             */

            /**
             * Constructs a new StatusResult.
             * @memberof karna.status
             * @classdesc Represents a StatusResult.
             * @implements IStatusResult
             * @constructor
             * @param {karna.status.IStatusResult=} [properties] Properties to set
             */
            function StatusResult(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * StatusResult vision.
             * @member {string} vision
             * @memberof karna.status.StatusResult
             * @instance
             */
            StatusResult.prototype.vision = "";

            /**
             * StatusResult language.
             * @member {string} language
             * @memberof karna.status.StatusResult
             * @instance
             */
            StatusResult.prototype.language = "";

            /**
             * StatusResult command.
             * @member {string} command
             * @memberof karna.status.StatusResult
             * @instance
             */
            StatusResult.prototype.command = "";

            /**
             * Creates a new StatusResult instance using the specified properties.
             * @function create
             * @memberof karna.status.StatusResult
             * @static
             * @param {karna.status.IStatusResult=} [properties] Properties to set
             * @returns {karna.status.StatusResult} StatusResult instance
             */
            StatusResult.create = function create(properties) {
                return new StatusResult(properties);
            };

            /**
             * Encodes the specified StatusResult message. Does not implicitly {@link karna.status.StatusResult.verify|verify} messages.
             * @function encode
             * @memberof karna.status.StatusResult
             * @static
             * @param {karna.status.IStatusResult} message StatusResult message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusResult.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.vision != null && Object.hasOwnProperty.call(message, "vision"))
                    writer.uint32(/* id 1, wireType 2 =*/10).string(message.vision);
                if (message.language != null && Object.hasOwnProperty.call(message, "language"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.language);
                if (message.command != null && Object.hasOwnProperty.call(message, "command"))
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.command);
                return writer;
            };

            /**
             * Encodes the specified StatusResult message, length delimited. Does not implicitly {@link karna.status.StatusResult.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.status.StatusResult
             * @static
             * @param {karna.status.IStatusResult} message StatusResult message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusResult.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a StatusResult message from the specified reader or buffer.
             * @function decode
             * @memberof karna.status.StatusResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.status.StatusResult} StatusResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusResult.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.status.StatusResult();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.vision = reader.string();
                            break;
                        }
                    case 2: {
                            message.language = reader.string();
                            break;
                        }
                    case 3: {
                            message.command = reader.string();
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
             * Decodes a StatusResult message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.status.StatusResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.status.StatusResult} StatusResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusResult.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a StatusResult message.
             * @function verify
             * @memberof karna.status.StatusResult
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            StatusResult.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                if (message.vision != null && message.hasOwnProperty("vision"))
                    if (!$util.isString(message.vision))
                        return "vision: string expected";
                if (message.language != null && message.hasOwnProperty("language"))
                    if (!$util.isString(message.language))
                        return "language: string expected";
                if (message.command != null && message.hasOwnProperty("command"))
                    if (!$util.isString(message.command))
                        return "command: string expected";
                return null;
            };

            /**
             * Creates a StatusResult message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.status.StatusResult
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.status.StatusResult} StatusResult
             */
            StatusResult.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.status.StatusResult)
                    return object;
                let message = new $root.karna.status.StatusResult();
                if (object.vision != null)
                    message.vision = String(object.vision);
                if (object.language != null)
                    message.language = String(object.language);
                if (object.command != null)
                    message.command = String(object.command);
                return message;
            };

            /**
             * Creates a plain object from a StatusResult message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.status.StatusResult
             * @static
             * @param {karna.status.StatusResult} message StatusResult
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            StatusResult.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (options.defaults) {
                    object.vision = "";
                    object.language = "";
                    object.command = "";
                }
                if (message.vision != null && message.hasOwnProperty("vision"))
                    object.vision = message.vision;
                if (message.language != null && message.hasOwnProperty("language"))
                    object.language = message.language;
                if (message.command != null && message.hasOwnProperty("command"))
                    object.command = message.command;
                return object;
            };

            /**
             * Converts this StatusResult to JSON.
             * @function toJSON
             * @memberof karna.status.StatusResult
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            StatusResult.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for StatusResult
             * @function getTypeUrl
             * @memberof karna.status.StatusResult
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            StatusResult.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.status.StatusResult";
            };

            return StatusResult;
        })();

        status.StatusRPCResponse = (function() {

            /**
             * Properties of a StatusRPCResponse.
             * @memberof karna.status
             * @interface IStatusRPCResponse
             * @property {karna.status.IStatusResult|null} [statusUpdate] StatusRPCResponse statusUpdate
             * @property {string|null} [error] StatusRPCResponse error
             */

            /**
             * Constructs a new StatusRPCResponse.
             * @memberof karna.status
             * @classdesc Represents a StatusRPCResponse.
             * @implements IStatusRPCResponse
             * @constructor
             * @param {karna.status.IStatusRPCResponse=} [properties] Properties to set
             */
            function StatusRPCResponse(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * StatusRPCResponse statusUpdate.
             * @member {karna.status.IStatusResult|null|undefined} statusUpdate
             * @memberof karna.status.StatusRPCResponse
             * @instance
             */
            StatusRPCResponse.prototype.statusUpdate = null;

            /**
             * StatusRPCResponse error.
             * @member {string|null|undefined} error
             * @memberof karna.status.StatusRPCResponse
             * @instance
             */
            StatusRPCResponse.prototype.error = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * StatusRPCResponse type.
             * @member {"statusUpdate"|"error"|undefined} type
             * @memberof karna.status.StatusRPCResponse
             * @instance
             */
            Object.defineProperty(StatusRPCResponse.prototype, "type", {
                get: $util.oneOfGetter($oneOfFields = ["statusUpdate", "error"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new StatusRPCResponse instance using the specified properties.
             * @function create
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {karna.status.IStatusRPCResponse=} [properties] Properties to set
             * @returns {karna.status.StatusRPCResponse} StatusRPCResponse instance
             */
            StatusRPCResponse.create = function create(properties) {
                return new StatusRPCResponse(properties);
            };

            /**
             * Encodes the specified StatusRPCResponse message. Does not implicitly {@link karna.status.StatusRPCResponse.verify|verify} messages.
             * @function encode
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {karna.status.IStatusRPCResponse} message StatusRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRPCResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.statusUpdate != null && Object.hasOwnProperty.call(message, "statusUpdate"))
                    $root.karna.status.StatusResult.encode(message.statusUpdate, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.error);
                return writer;
            };

            /**
             * Encodes the specified StatusRPCResponse message, length delimited. Does not implicitly {@link karna.status.StatusRPCResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {karna.status.IStatusRPCResponse} message StatusRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            StatusRPCResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a StatusRPCResponse message from the specified reader or buffer.
             * @function decode
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.status.StatusRPCResponse} StatusRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRPCResponse.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.status.StatusRPCResponse();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.statusUpdate = $root.karna.status.StatusResult.decode(reader, reader.uint32());
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
             * Decodes a StatusRPCResponse message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.status.StatusRPCResponse} StatusRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            StatusRPCResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a StatusRPCResponse message.
             * @function verify
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            StatusRPCResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.statusUpdate != null && message.hasOwnProperty("statusUpdate")) {
                    properties.type = 1;
                    {
                        let error = $root.karna.status.StatusResult.verify(message.statusUpdate);
                        if (error)
                            return "statusUpdate." + error;
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
             * Creates a StatusRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.status.StatusRPCResponse} StatusRPCResponse
             */
            StatusRPCResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.status.StatusRPCResponse)
                    return object;
                let message = new $root.karna.status.StatusRPCResponse();
                if (object.statusUpdate != null) {
                    if (typeof object.statusUpdate !== "object")
                        throw TypeError(".karna.status.StatusRPCResponse.statusUpdate: object expected");
                    message.statusUpdate = $root.karna.status.StatusResult.fromObject(object.statusUpdate);
                }
                if (object.error != null)
                    message.error = String(object.error);
                return message;
            };

            /**
             * Creates a plain object from a StatusRPCResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {karna.status.StatusRPCResponse} message StatusRPCResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            StatusRPCResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.statusUpdate != null && message.hasOwnProperty("statusUpdate")) {
                    object.statusUpdate = $root.karna.status.StatusResult.toObject(message.statusUpdate, options);
                    if (options.oneofs)
                        object.type = "statusUpdate";
                }
                if (message.error != null && message.hasOwnProperty("error")) {
                    object.error = message.error;
                    if (options.oneofs)
                        object.type = "error";
                }
                return object;
            };

            /**
             * Converts this StatusRPCResponse to JSON.
             * @function toJSON
             * @memberof karna.status.StatusRPCResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            StatusRPCResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for StatusRPCResponse
             * @function getTypeUrl
             * @memberof karna.status.StatusRPCResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            StatusRPCResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.status.StatusRPCResponse";
            };

            return StatusRPCResponse;
        })();

        return status;
    })();

    return karna;
})();

export { $root as default };
