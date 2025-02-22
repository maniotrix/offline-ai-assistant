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

    karna.RPCRequest = (function() {

        /**
         * Properties of a RPCRequest.
         * @memberof karna
         * @interface IRPCRequest
         * @property {karna.ICommandRequest|null} [executeCommand] RPCRequest executeCommand
         * @property {karna.IStatusRequest|null} [getStatus] RPCRequest getStatus
         */

        /**
         * Constructs a new RPCRequest.
         * @memberof karna
         * @classdesc Represents a RPCRequest.
         * @implements IRPCRequest
         * @constructor
         * @param {karna.IRPCRequest=} [properties] Properties to set
         */
        function RPCRequest(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * RPCRequest executeCommand.
         * @member {karna.ICommandRequest|null|undefined} executeCommand
         * @memberof karna.RPCRequest
         * @instance
         */
        RPCRequest.prototype.executeCommand = null;

        /**
         * RPCRequest getStatus.
         * @member {karna.IStatusRequest|null|undefined} getStatus
         * @memberof karna.RPCRequest
         * @instance
         */
        RPCRequest.prototype.getStatus = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        /**
         * RPCRequest method.
         * @member {"executeCommand"|"getStatus"|undefined} method
         * @memberof karna.RPCRequest
         * @instance
         */
        Object.defineProperty(RPCRequest.prototype, "method", {
            get: $util.oneOfGetter($oneOfFields = ["executeCommand", "getStatus"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new RPCRequest instance using the specified properties.
         * @function create
         * @memberof karna.RPCRequest
         * @static
         * @param {karna.IRPCRequest=} [properties] Properties to set
         * @returns {karna.RPCRequest} RPCRequest instance
         */
        RPCRequest.create = function create(properties) {
            return new RPCRequest(properties);
        };

        /**
         * Encodes the specified RPCRequest message. Does not implicitly {@link karna.RPCRequest.verify|verify} messages.
         * @function encode
         * @memberof karna.RPCRequest
         * @static
         * @param {karna.IRPCRequest} message RPCRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        RPCRequest.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.executeCommand != null && Object.hasOwnProperty.call(message, "executeCommand"))
                $root.karna.CommandRequest.encode(message.executeCommand, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.getStatus != null && Object.hasOwnProperty.call(message, "getStatus"))
                $root.karna.StatusRequest.encode(message.getStatus, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified RPCRequest message, length delimited. Does not implicitly {@link karna.RPCRequest.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.RPCRequest
         * @static
         * @param {karna.IRPCRequest} message RPCRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        RPCRequest.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a RPCRequest message from the specified reader or buffer.
         * @function decode
         * @memberof karna.RPCRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.RPCRequest} RPCRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        RPCRequest.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.RPCRequest();
            while (reader.pos < end) {
                let tag = reader.uint32();
                switch (tag >>> 3) {
                case 1: {
                        message.executeCommand = $root.karna.CommandRequest.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.getStatus = $root.karna.StatusRequest.decode(reader, reader.uint32());
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
         * Decodes a RPCRequest message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.RPCRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.RPCRequest} RPCRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        RPCRequest.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a RPCRequest message.
         * @function verify
         * @memberof karna.RPCRequest
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        RPCRequest.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.executeCommand != null && message.hasOwnProperty("executeCommand")) {
                properties.method = 1;
                {
                    let error = $root.karna.CommandRequest.verify(message.executeCommand);
                    if (error)
                        return "executeCommand." + error;
                }
            }
            if (message.getStatus != null && message.hasOwnProperty("getStatus")) {
                if (properties.method === 1)
                    return "method: multiple values";
                properties.method = 1;
                {
                    let error = $root.karna.StatusRequest.verify(message.getStatus);
                    if (error)
                        return "getStatus." + error;
                }
            }
            return null;
        };

        /**
         * Creates a RPCRequest message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.RPCRequest
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.RPCRequest} RPCRequest
         */
        RPCRequest.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.RPCRequest)
                return object;
            let message = new $root.karna.RPCRequest();
            if (object.executeCommand != null) {
                if (typeof object.executeCommand !== "object")
                    throw TypeError(".karna.RPCRequest.executeCommand: object expected");
                message.executeCommand = $root.karna.CommandRequest.fromObject(object.executeCommand);
            }
            if (object.getStatus != null) {
                if (typeof object.getStatus !== "object")
                    throw TypeError(".karna.RPCRequest.getStatus: object expected");
                message.getStatus = $root.karna.StatusRequest.fromObject(object.getStatus);
            }
            return message;
        };

        /**
         * Creates a plain object from a RPCRequest message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.RPCRequest
         * @static
         * @param {karna.RPCRequest} message RPCRequest
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        RPCRequest.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (message.executeCommand != null && message.hasOwnProperty("executeCommand")) {
                object.executeCommand = $root.karna.CommandRequest.toObject(message.executeCommand, options);
                if (options.oneofs)
                    object.method = "executeCommand";
            }
            if (message.getStatus != null && message.hasOwnProperty("getStatus")) {
                object.getStatus = $root.karna.StatusRequest.toObject(message.getStatus, options);
                if (options.oneofs)
                    object.method = "getStatus";
            }
            return object;
        };

        /**
         * Converts this RPCRequest to JSON.
         * @function toJSON
         * @memberof karna.RPCRequest
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        RPCRequest.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for RPCRequest
         * @function getTypeUrl
         * @memberof karna.RPCRequest
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        RPCRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.RPCRequest";
        };

        return RPCRequest;
    })();

    karna.CommandRequest = (function() {

        /**
         * Properties of a CommandRequest.
         * @memberof karna
         * @interface ICommandRequest
         * @property {string|null} [command] CommandRequest command
         * @property {string|null} [domain] CommandRequest domain
         */

        /**
         * Constructs a new CommandRequest.
         * @memberof karna
         * @classdesc Represents a CommandRequest.
         * @implements ICommandRequest
         * @constructor
         * @param {karna.ICommandRequest=} [properties] Properties to set
         */
        function CommandRequest(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CommandRequest command.
         * @member {string} command
         * @memberof karna.CommandRequest
         * @instance
         */
        CommandRequest.prototype.command = "";

        /**
         * CommandRequest domain.
         * @member {string} domain
         * @memberof karna.CommandRequest
         * @instance
         */
        CommandRequest.prototype.domain = "";

        /**
         * Creates a new CommandRequest instance using the specified properties.
         * @function create
         * @memberof karna.CommandRequest
         * @static
         * @param {karna.ICommandRequest=} [properties] Properties to set
         * @returns {karna.CommandRequest} CommandRequest instance
         */
        CommandRequest.create = function create(properties) {
            return new CommandRequest(properties);
        };

        /**
         * Encodes the specified CommandRequest message. Does not implicitly {@link karna.CommandRequest.verify|verify} messages.
         * @function encode
         * @memberof karna.CommandRequest
         * @static
         * @param {karna.ICommandRequest} message CommandRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CommandRequest.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.command != null && Object.hasOwnProperty.call(message, "command"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.command);
            if (message.domain != null && Object.hasOwnProperty.call(message, "domain"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.domain);
            return writer;
        };

        /**
         * Encodes the specified CommandRequest message, length delimited. Does not implicitly {@link karna.CommandRequest.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.CommandRequest
         * @static
         * @param {karna.ICommandRequest} message CommandRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CommandRequest.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CommandRequest message from the specified reader or buffer.
         * @function decode
         * @memberof karna.CommandRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.CommandRequest} CommandRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CommandRequest.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.CommandRequest();
            while (reader.pos < end) {
                let tag = reader.uint32();
                switch (tag >>> 3) {
                case 1: {
                        message.command = reader.string();
                        break;
                    }
                case 2: {
                        message.domain = reader.string();
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
         * Decodes a CommandRequest message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.CommandRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.CommandRequest} CommandRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CommandRequest.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CommandRequest message.
         * @function verify
         * @memberof karna.CommandRequest
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CommandRequest.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.command != null && message.hasOwnProperty("command"))
                if (!$util.isString(message.command))
                    return "command: string expected";
            if (message.domain != null && message.hasOwnProperty("domain"))
                if (!$util.isString(message.domain))
                    return "domain: string expected";
            return null;
        };

        /**
         * Creates a CommandRequest message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.CommandRequest
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.CommandRequest} CommandRequest
         */
        CommandRequest.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.CommandRequest)
                return object;
            let message = new $root.karna.CommandRequest();
            if (object.command != null)
                message.command = String(object.command);
            if (object.domain != null)
                message.domain = String(object.domain);
            return message;
        };

        /**
         * Creates a plain object from a CommandRequest message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.CommandRequest
         * @static
         * @param {karna.CommandRequest} message CommandRequest
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CommandRequest.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.command = "";
                object.domain = "";
            }
            if (message.command != null && message.hasOwnProperty("command"))
                object.command = message.command;
            if (message.domain != null && message.hasOwnProperty("domain"))
                object.domain = message.domain;
            return object;
        };

        /**
         * Converts this CommandRequest to JSON.
         * @function toJSON
         * @memberof karna.CommandRequest
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CommandRequest.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CommandRequest
         * @function getTypeUrl
         * @memberof karna.CommandRequest
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CommandRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.CommandRequest";
        };

        return CommandRequest;
    })();

    karna.StatusRequest = (function() {

        /**
         * Properties of a StatusRequest.
         * @memberof karna
         * @interface IStatusRequest
         */

        /**
         * Constructs a new StatusRequest.
         * @memberof karna
         * @classdesc Represents a StatusRequest.
         * @implements IStatusRequest
         * @constructor
         * @param {karna.IStatusRequest=} [properties] Properties to set
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
         * @memberof karna.StatusRequest
         * @static
         * @param {karna.IStatusRequest=} [properties] Properties to set
         * @returns {karna.StatusRequest} StatusRequest instance
         */
        StatusRequest.create = function create(properties) {
            return new StatusRequest(properties);
        };

        /**
         * Encodes the specified StatusRequest message. Does not implicitly {@link karna.StatusRequest.verify|verify} messages.
         * @function encode
         * @memberof karna.StatusRequest
         * @static
         * @param {karna.IStatusRequest} message StatusRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        StatusRequest.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            return writer;
        };

        /**
         * Encodes the specified StatusRequest message, length delimited. Does not implicitly {@link karna.StatusRequest.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.StatusRequest
         * @static
         * @param {karna.IStatusRequest} message StatusRequest message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        StatusRequest.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a StatusRequest message from the specified reader or buffer.
         * @function decode
         * @memberof karna.StatusRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.StatusRequest} StatusRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        StatusRequest.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.StatusRequest();
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
         * @memberof karna.StatusRequest
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.StatusRequest} StatusRequest
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
         * @memberof karna.StatusRequest
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
         * @memberof karna.StatusRequest
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.StatusRequest} StatusRequest
         */
        StatusRequest.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.StatusRequest)
                return object;
            return new $root.karna.StatusRequest();
        };

        /**
         * Creates a plain object from a StatusRequest message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.StatusRequest
         * @static
         * @param {karna.StatusRequest} message StatusRequest
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        StatusRequest.toObject = function toObject() {
            return {};
        };

        /**
         * Converts this StatusRequest to JSON.
         * @function toJSON
         * @memberof karna.StatusRequest
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        StatusRequest.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for StatusRequest
         * @function getTypeUrl
         * @memberof karna.StatusRequest
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        StatusRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.StatusRequest";
        };

        return StatusRequest;
    })();

    karna.RPCResponse = (function() {

        /**
         * Properties of a RPCResponse.
         * @memberof karna
         * @interface IRPCResponse
         * @property {karna.ICommandResult|null} [commandResponse] RPCResponse commandResponse
         * @property {karna.IStatus|null} [statusUpdate] RPCResponse statusUpdate
         * @property {string|null} [error] RPCResponse error
         */

        /**
         * Constructs a new RPCResponse.
         * @memberof karna
         * @classdesc Represents a RPCResponse.
         * @implements IRPCResponse
         * @constructor
         * @param {karna.IRPCResponse=} [properties] Properties to set
         */
        function RPCResponse(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * RPCResponse commandResponse.
         * @member {karna.ICommandResult|null|undefined} commandResponse
         * @memberof karna.RPCResponse
         * @instance
         */
        RPCResponse.prototype.commandResponse = null;

        /**
         * RPCResponse statusUpdate.
         * @member {karna.IStatus|null|undefined} statusUpdate
         * @memberof karna.RPCResponse
         * @instance
         */
        RPCResponse.prototype.statusUpdate = null;

        /**
         * RPCResponse error.
         * @member {string|null|undefined} error
         * @memberof karna.RPCResponse
         * @instance
         */
        RPCResponse.prototype.error = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        /**
         * RPCResponse type.
         * @member {"commandResponse"|"statusUpdate"|"error"|undefined} type
         * @memberof karna.RPCResponse
         * @instance
         */
        Object.defineProperty(RPCResponse.prototype, "type", {
            get: $util.oneOfGetter($oneOfFields = ["commandResponse", "statusUpdate", "error"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new RPCResponse instance using the specified properties.
         * @function create
         * @memberof karna.RPCResponse
         * @static
         * @param {karna.IRPCResponse=} [properties] Properties to set
         * @returns {karna.RPCResponse} RPCResponse instance
         */
        RPCResponse.create = function create(properties) {
            return new RPCResponse(properties);
        };

        /**
         * Encodes the specified RPCResponse message. Does not implicitly {@link karna.RPCResponse.verify|verify} messages.
         * @function encode
         * @memberof karna.RPCResponse
         * @static
         * @param {karna.IRPCResponse} message RPCResponse message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        RPCResponse.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.commandResponse != null && Object.hasOwnProperty.call(message, "commandResponse"))
                $root.karna.CommandResult.encode(message.commandResponse, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.statusUpdate != null && Object.hasOwnProperty.call(message, "statusUpdate"))
                $root.karna.Status.encode(message.statusUpdate, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.error);
            return writer;
        };

        /**
         * Encodes the specified RPCResponse message, length delimited. Does not implicitly {@link karna.RPCResponse.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.RPCResponse
         * @static
         * @param {karna.IRPCResponse} message RPCResponse message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        RPCResponse.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a RPCResponse message from the specified reader or buffer.
         * @function decode
         * @memberof karna.RPCResponse
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.RPCResponse} RPCResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        RPCResponse.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.RPCResponse();
            while (reader.pos < end) {
                let tag = reader.uint32();
                switch (tag >>> 3) {
                case 1: {
                        message.commandResponse = $root.karna.CommandResult.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.statusUpdate = $root.karna.Status.decode(reader, reader.uint32());
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
         * Decodes a RPCResponse message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.RPCResponse
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.RPCResponse} RPCResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        RPCResponse.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a RPCResponse message.
         * @function verify
         * @memberof karna.RPCResponse
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        RPCResponse.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.commandResponse != null && message.hasOwnProperty("commandResponse")) {
                properties.type = 1;
                {
                    let error = $root.karna.CommandResult.verify(message.commandResponse);
                    if (error)
                        return "commandResponse." + error;
                }
            }
            if (message.statusUpdate != null && message.hasOwnProperty("statusUpdate")) {
                if (properties.type === 1)
                    return "type: multiple values";
                properties.type = 1;
                {
                    let error = $root.karna.Status.verify(message.statusUpdate);
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
         * Creates a RPCResponse message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.RPCResponse
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.RPCResponse} RPCResponse
         */
        RPCResponse.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.RPCResponse)
                return object;
            let message = new $root.karna.RPCResponse();
            if (object.commandResponse != null) {
                if (typeof object.commandResponse !== "object")
                    throw TypeError(".karna.RPCResponse.commandResponse: object expected");
                message.commandResponse = $root.karna.CommandResult.fromObject(object.commandResponse);
            }
            if (object.statusUpdate != null) {
                if (typeof object.statusUpdate !== "object")
                    throw TypeError(".karna.RPCResponse.statusUpdate: object expected");
                message.statusUpdate = $root.karna.Status.fromObject(object.statusUpdate);
            }
            if (object.error != null)
                message.error = String(object.error);
            return message;
        };

        /**
         * Creates a plain object from a RPCResponse message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.RPCResponse
         * @static
         * @param {karna.RPCResponse} message RPCResponse
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        RPCResponse.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (message.commandResponse != null && message.hasOwnProperty("commandResponse")) {
                object.commandResponse = $root.karna.CommandResult.toObject(message.commandResponse, options);
                if (options.oneofs)
                    object.type = "commandResponse";
            }
            if (message.statusUpdate != null && message.hasOwnProperty("statusUpdate")) {
                object.statusUpdate = $root.karna.Status.toObject(message.statusUpdate, options);
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
         * Converts this RPCResponse to JSON.
         * @function toJSON
         * @memberof karna.RPCResponse
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        RPCResponse.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for RPCResponse
         * @function getTypeUrl
         * @memberof karna.RPCResponse
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        RPCResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.RPCResponse";
        };

        return RPCResponse;
    })();

    karna.CommandResult = (function() {

        /**
         * Properties of a CommandResult.
         * @memberof karna
         * @interface ICommandResult
         * @property {string|null} [commandText] CommandResult commandText
         * @property {karna.TaskStatus|null} [status] CommandResult status
         * @property {string|null} [message] CommandResult message
         * @property {Array.<karna.IAction>|null} [actions] CommandResult actions
         */

        /**
         * Constructs a new CommandResult.
         * @memberof karna
         * @classdesc Represents a CommandResult.
         * @implements ICommandResult
         * @constructor
         * @param {karna.ICommandResult=} [properties] Properties to set
         */
        function CommandResult(properties) {
            this.actions = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CommandResult commandText.
         * @member {string} commandText
         * @memberof karna.CommandResult
         * @instance
         */
        CommandResult.prototype.commandText = "";

        /**
         * CommandResult status.
         * @member {karna.TaskStatus} status
         * @memberof karna.CommandResult
         * @instance
         */
        CommandResult.prototype.status = 0;

        /**
         * CommandResult message.
         * @member {string} message
         * @memberof karna.CommandResult
         * @instance
         */
        CommandResult.prototype.message = "";

        /**
         * CommandResult actions.
         * @member {Array.<karna.IAction>} actions
         * @memberof karna.CommandResult
         * @instance
         */
        CommandResult.prototype.actions = $util.emptyArray;

        /**
         * Creates a new CommandResult instance using the specified properties.
         * @function create
         * @memberof karna.CommandResult
         * @static
         * @param {karna.ICommandResult=} [properties] Properties to set
         * @returns {karna.CommandResult} CommandResult instance
         */
        CommandResult.create = function create(properties) {
            return new CommandResult(properties);
        };

        /**
         * Encodes the specified CommandResult message. Does not implicitly {@link karna.CommandResult.verify|verify} messages.
         * @function encode
         * @memberof karna.CommandResult
         * @static
         * @param {karna.ICommandResult} message CommandResult message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CommandResult.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.commandText != null && Object.hasOwnProperty.call(message, "commandText"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.commandText);
            if (message.status != null && Object.hasOwnProperty.call(message, "status"))
                writer.uint32(/* id 2, wireType 0 =*/16).int32(message.status);
            if (message.message != null && Object.hasOwnProperty.call(message, "message"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.message);
            if (message.actions != null && message.actions.length)
                for (let i = 0; i < message.actions.length; ++i)
                    $root.karna.Action.encode(message.actions[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CommandResult message, length delimited. Does not implicitly {@link karna.CommandResult.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.CommandResult
         * @static
         * @param {karna.ICommandResult} message CommandResult message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CommandResult.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CommandResult message from the specified reader or buffer.
         * @function decode
         * @memberof karna.CommandResult
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.CommandResult} CommandResult
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CommandResult.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.CommandResult();
            while (reader.pos < end) {
                let tag = reader.uint32();
                switch (tag >>> 3) {
                case 1: {
                        message.commandText = reader.string();
                        break;
                    }
                case 2: {
                        message.status = reader.int32();
                        break;
                    }
                case 3: {
                        message.message = reader.string();
                        break;
                    }
                case 4: {
                        if (!(message.actions && message.actions.length))
                            message.actions = [];
                        message.actions.push($root.karna.Action.decode(reader, reader.uint32()));
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
         * Decodes a CommandResult message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.CommandResult
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.CommandResult} CommandResult
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CommandResult.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CommandResult message.
         * @function verify
         * @memberof karna.CommandResult
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CommandResult.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.commandText != null && message.hasOwnProperty("commandText"))
                if (!$util.isString(message.commandText))
                    return "commandText: string expected";
            if (message.status != null && message.hasOwnProperty("status"))
                switch (message.status) {
                default:
                    return "status: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                    break;
                }
            if (message.message != null && message.hasOwnProperty("message"))
                if (!$util.isString(message.message))
                    return "message: string expected";
            if (message.actions != null && message.hasOwnProperty("actions")) {
                if (!Array.isArray(message.actions))
                    return "actions: array expected";
                for (let i = 0; i < message.actions.length; ++i) {
                    let error = $root.karna.Action.verify(message.actions[i]);
                    if (error)
                        return "actions." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CommandResult message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.CommandResult
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.CommandResult} CommandResult
         */
        CommandResult.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.CommandResult)
                return object;
            let message = new $root.karna.CommandResult();
            if (object.commandText != null)
                message.commandText = String(object.commandText);
            switch (object.status) {
            default:
                if (typeof object.status === "number") {
                    message.status = object.status;
                    break;
                }
                break;
            case "PENDING":
            case 0:
                message.status = 0;
                break;
            case "IN_PROGRESS":
            case 1:
                message.status = 1;
                break;
            case "COMPLETED":
            case 2:
                message.status = 2;
                break;
            case "FAILED":
            case 3:
                message.status = 3;
                break;
            }
            if (object.message != null)
                message.message = String(object.message);
            if (object.actions) {
                if (!Array.isArray(object.actions))
                    throw TypeError(".karna.CommandResult.actions: array expected");
                message.actions = [];
                for (let i = 0; i < object.actions.length; ++i) {
                    if (typeof object.actions[i] !== "object")
                        throw TypeError(".karna.CommandResult.actions: object expected");
                    message.actions[i] = $root.karna.Action.fromObject(object.actions[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CommandResult message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.CommandResult
         * @static
         * @param {karna.CommandResult} message CommandResult
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CommandResult.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.actions = [];
            if (options.defaults) {
                object.commandText = "";
                object.status = options.enums === String ? "PENDING" : 0;
                object.message = "";
            }
            if (message.commandText != null && message.hasOwnProperty("commandText"))
                object.commandText = message.commandText;
            if (message.status != null && message.hasOwnProperty("status"))
                object.status = options.enums === String ? $root.karna.TaskStatus[message.status] === undefined ? message.status : $root.karna.TaskStatus[message.status] : message.status;
            if (message.message != null && message.hasOwnProperty("message"))
                object.message = message.message;
            if (message.actions && message.actions.length) {
                object.actions = [];
                for (let j = 0; j < message.actions.length; ++j)
                    object.actions[j] = $root.karna.Action.toObject(message.actions[j], options);
            }
            return object;
        };

        /**
         * Converts this CommandResult to JSON.
         * @function toJSON
         * @memberof karna.CommandResult
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CommandResult.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CommandResult
         * @function getTypeUrl
         * @memberof karna.CommandResult
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CommandResult.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.CommandResult";
        };

        return CommandResult;
    })();

    karna.Status = (function() {

        /**
         * Properties of a Status.
         * @memberof karna
         * @interface IStatus
         * @property {string|null} [vision] Status vision
         * @property {string|null} [language] Status language
         * @property {string|null} [command] Status command
         */

        /**
         * Constructs a new Status.
         * @memberof karna
         * @classdesc Represents a Status.
         * @implements IStatus
         * @constructor
         * @param {karna.IStatus=} [properties] Properties to set
         */
        function Status(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Status vision.
         * @member {string} vision
         * @memberof karna.Status
         * @instance
         */
        Status.prototype.vision = "";

        /**
         * Status language.
         * @member {string} language
         * @memberof karna.Status
         * @instance
         */
        Status.prototype.language = "";

        /**
         * Status command.
         * @member {string} command
         * @memberof karna.Status
         * @instance
         */
        Status.prototype.command = "";

        /**
         * Creates a new Status instance using the specified properties.
         * @function create
         * @memberof karna.Status
         * @static
         * @param {karna.IStatus=} [properties] Properties to set
         * @returns {karna.Status} Status instance
         */
        Status.create = function create(properties) {
            return new Status(properties);
        };

        /**
         * Encodes the specified Status message. Does not implicitly {@link karna.Status.verify|verify} messages.
         * @function encode
         * @memberof karna.Status
         * @static
         * @param {karna.IStatus} message Status message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Status.encode = function encode(message, writer) {
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
         * Encodes the specified Status message, length delimited. Does not implicitly {@link karna.Status.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.Status
         * @static
         * @param {karna.IStatus} message Status message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Status.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Status message from the specified reader or buffer.
         * @function decode
         * @memberof karna.Status
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.Status} Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Status.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.Status();
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
         * Decodes a Status message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.Status
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.Status} Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Status.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Status message.
         * @function verify
         * @memberof karna.Status
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Status.verify = function verify(message) {
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
         * Creates a Status message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.Status
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.Status} Status
         */
        Status.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.Status)
                return object;
            let message = new $root.karna.Status();
            if (object.vision != null)
                message.vision = String(object.vision);
            if (object.language != null)
                message.language = String(object.language);
            if (object.command != null)
                message.command = String(object.command);
            return message;
        };

        /**
         * Creates a plain object from a Status message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.Status
         * @static
         * @param {karna.Status} message Status
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Status.toObject = function toObject(message, options) {
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
         * Converts this Status to JSON.
         * @function toJSON
         * @memberof karna.Status
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Status.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Status
         * @function getTypeUrl
         * @memberof karna.Status
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Status.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.Status";
        };

        return Status;
    })();

    karna.Action = (function() {

        /**
         * Properties of an Action.
         * @memberof karna
         * @interface IAction
         * @property {string|null} [type] Action type
         * @property {Object.<string,string>|null} [coordinates] Action coordinates
         * @property {string|null} [text] Action text
         */

        /**
         * Constructs a new Action.
         * @memberof karna
         * @classdesc Represents an Action.
         * @implements IAction
         * @constructor
         * @param {karna.IAction=} [properties] Properties to set
         */
        function Action(properties) {
            this.coordinates = {};
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Action type.
         * @member {string} type
         * @memberof karna.Action
         * @instance
         */
        Action.prototype.type = "";

        /**
         * Action coordinates.
         * @member {Object.<string,string>} coordinates
         * @memberof karna.Action
         * @instance
         */
        Action.prototype.coordinates = $util.emptyObject;

        /**
         * Action text.
         * @member {string|null|undefined} text
         * @memberof karna.Action
         * @instance
         */
        Action.prototype.text = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(Action.prototype, "_text", {
            get: $util.oneOfGetter($oneOfFields = ["text"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new Action instance using the specified properties.
         * @function create
         * @memberof karna.Action
         * @static
         * @param {karna.IAction=} [properties] Properties to set
         * @returns {karna.Action} Action instance
         */
        Action.create = function create(properties) {
            return new Action(properties);
        };

        /**
         * Encodes the specified Action message. Does not implicitly {@link karna.Action.verify|verify} messages.
         * @function encode
         * @memberof karna.Action
         * @static
         * @param {karna.IAction} message Action message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Action.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.type);
            if (message.coordinates != null && Object.hasOwnProperty.call(message, "coordinates"))
                for (let keys = Object.keys(message.coordinates), i = 0; i < keys.length; ++i)
                    writer.uint32(/* id 2, wireType 2 =*/18).fork().uint32(/* id 1, wireType 2 =*/10).string(keys[i]).uint32(/* id 2, wireType 2 =*/18).string(message.coordinates[keys[i]]).ldelim();
            if (message.text != null && Object.hasOwnProperty.call(message, "text"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.text);
            return writer;
        };

        /**
         * Encodes the specified Action message, length delimited. Does not implicitly {@link karna.Action.verify|verify} messages.
         * @function encodeDelimited
         * @memberof karna.Action
         * @static
         * @param {karna.IAction} message Action message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Action.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an Action message from the specified reader or buffer.
         * @function decode
         * @memberof karna.Action
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {karna.Action} Action
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Action.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.Action(), key, value;
            while (reader.pos < end) {
                let tag = reader.uint32();
                switch (tag >>> 3) {
                case 1: {
                        message.type = reader.string();
                        break;
                    }
                case 2: {
                        if (message.coordinates === $util.emptyObject)
                            message.coordinates = {};
                        let end2 = reader.uint32() + reader.pos;
                        key = "";
                        value = "";
                        while (reader.pos < end2) {
                            let tag2 = reader.uint32();
                            switch (tag2 >>> 3) {
                            case 1:
                                key = reader.string();
                                break;
                            case 2:
                                value = reader.string();
                                break;
                            default:
                                reader.skipType(tag2 & 7);
                                break;
                            }
                        }
                        message.coordinates[key] = value;
                        break;
                    }
                case 3: {
                        message.text = reader.string();
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
         * Decodes an Action message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof karna.Action
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {karna.Action} Action
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Action.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an Action message.
         * @function verify
         * @memberof karna.Action
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Action.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.type != null && message.hasOwnProperty("type"))
                if (!$util.isString(message.type))
                    return "type: string expected";
            if (message.coordinates != null && message.hasOwnProperty("coordinates")) {
                if (!$util.isObject(message.coordinates))
                    return "coordinates: object expected";
                let key = Object.keys(message.coordinates);
                for (let i = 0; i < key.length; ++i)
                    if (!$util.isString(message.coordinates[key[i]]))
                        return "coordinates: string{k:string} expected";
            }
            if (message.text != null && message.hasOwnProperty("text")) {
                properties._text = 1;
                if (!$util.isString(message.text))
                    return "text: string expected";
            }
            return null;
        };

        /**
         * Creates an Action message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof karna.Action
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {karna.Action} Action
         */
        Action.fromObject = function fromObject(object) {
            if (object instanceof $root.karna.Action)
                return object;
            let message = new $root.karna.Action();
            if (object.type != null)
                message.type = String(object.type);
            if (object.coordinates) {
                if (typeof object.coordinates !== "object")
                    throw TypeError(".karna.Action.coordinates: object expected");
                message.coordinates = {};
                for (let keys = Object.keys(object.coordinates), i = 0; i < keys.length; ++i)
                    message.coordinates[keys[i]] = String(object.coordinates[keys[i]]);
            }
            if (object.text != null)
                message.text = String(object.text);
            return message;
        };

        /**
         * Creates a plain object from an Action message. Also converts values to other types if specified.
         * @function toObject
         * @memberof karna.Action
         * @static
         * @param {karna.Action} message Action
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Action.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.objects || options.defaults)
                object.coordinates = {};
            if (options.defaults)
                object.type = "";
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = message.type;
            let keys2;
            if (message.coordinates && (keys2 = Object.keys(message.coordinates)).length) {
                object.coordinates = {};
                for (let j = 0; j < keys2.length; ++j)
                    object.coordinates[keys2[j]] = message.coordinates[keys2[j]];
            }
            if (message.text != null && message.hasOwnProperty("text")) {
                object.text = message.text;
                if (options.oneofs)
                    object._text = "text";
            }
            return object;
        };

        /**
         * Converts this Action to JSON.
         * @function toJSON
         * @memberof karna.Action
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Action.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Action
         * @function getTypeUrl
         * @memberof karna.Action
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Action.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/karna.Action";
        };

        return Action;
    })();

    /**
     * TaskStatus enum.
     * @name karna.TaskStatus
     * @enum {number}
     * @property {number} PENDING=0 PENDING value
     * @property {number} IN_PROGRESS=1 IN_PROGRESS value
     * @property {number} COMPLETED=2 COMPLETED value
     * @property {number} FAILED=3 FAILED value
     */
    karna.TaskStatus = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "PENDING"] = 0;
        values[valuesById[1] = "IN_PROGRESS"] = 1;
        values[valuesById[2] = "COMPLETED"] = 2;
        values[valuesById[3] = "FAILED"] = 3;
        return values;
    })();

    return karna;
})();

export { $root as default };
