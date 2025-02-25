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

    karna.command = (function() {

        /**
         * Namespace command.
         * @memberof karna
         * @namespace
         */
        const command = {};

        command.CommandRequest = (function() {

            /**
             * Properties of a CommandRequest.
             * @memberof karna.command
             * @interface ICommandRequest
             * @property {string|null} [command] CommandRequest command
             * @property {string|null} [domain] CommandRequest domain
             */

            /**
             * Constructs a new CommandRequest.
             * @memberof karna.command
             * @classdesc Represents a CommandRequest.
             * @implements ICommandRequest
             * @constructor
             * @param {karna.command.ICommandRequest=} [properties] Properties to set
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
             * @memberof karna.command.CommandRequest
             * @instance
             */
            CommandRequest.prototype.command = "";

            /**
             * CommandRequest domain.
             * @member {string} domain
             * @memberof karna.command.CommandRequest
             * @instance
             */
            CommandRequest.prototype.domain = "";

            /**
             * Creates a new CommandRequest instance using the specified properties.
             * @function create
             * @memberof karna.command.CommandRequest
             * @static
             * @param {karna.command.ICommandRequest=} [properties] Properties to set
             * @returns {karna.command.CommandRequest} CommandRequest instance
             */
            CommandRequest.create = function create(properties) {
                return new CommandRequest(properties);
            };

            /**
             * Encodes the specified CommandRequest message. Does not implicitly {@link karna.command.CommandRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.command.CommandRequest
             * @static
             * @param {karna.command.ICommandRequest} message CommandRequest message or plain object to encode
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
             * Encodes the specified CommandRequest message, length delimited. Does not implicitly {@link karna.command.CommandRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.command.CommandRequest
             * @static
             * @param {karna.command.ICommandRequest} message CommandRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CommandRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.command.CommandRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.command.CommandRequest} CommandRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.command.CommandRequest();
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
             * @memberof karna.command.CommandRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.command.CommandRequest} CommandRequest
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
             * @memberof karna.command.CommandRequest
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
             * @memberof karna.command.CommandRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.command.CommandRequest} CommandRequest
             */
            CommandRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.command.CommandRequest)
                    return object;
                let message = new $root.karna.command.CommandRequest();
                if (object.command != null)
                    message.command = String(object.command);
                if (object.domain != null)
                    message.domain = String(object.domain);
                return message;
            };

            /**
             * Creates a plain object from a CommandRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.command.CommandRequest
             * @static
             * @param {karna.command.CommandRequest} message CommandRequest
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
             * @memberof karna.command.CommandRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CommandRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CommandRequest
             * @function getTypeUrl
             * @memberof karna.command.CommandRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CommandRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.command.CommandRequest";
            };

            return CommandRequest;
        })();

        command.CommandRPCRequest = (function() {

            /**
             * Properties of a CommandRPCRequest.
             * @memberof karna.command
             * @interface ICommandRPCRequest
             * @property {karna.command.ICommandRequest|null} [executeCommand] CommandRPCRequest executeCommand
             */

            /**
             * Constructs a new CommandRPCRequest.
             * @memberof karna.command
             * @classdesc Represents a CommandRPCRequest.
             * @implements ICommandRPCRequest
             * @constructor
             * @param {karna.command.ICommandRPCRequest=} [properties] Properties to set
             */
            function CommandRPCRequest(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CommandRPCRequest executeCommand.
             * @member {karna.command.ICommandRequest|null|undefined} executeCommand
             * @memberof karna.command.CommandRPCRequest
             * @instance
             */
            CommandRPCRequest.prototype.executeCommand = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * CommandRPCRequest method.
             * @member {"executeCommand"|undefined} method
             * @memberof karna.command.CommandRPCRequest
             * @instance
             */
            Object.defineProperty(CommandRPCRequest.prototype, "method", {
                get: $util.oneOfGetter($oneOfFields = ["executeCommand"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new CommandRPCRequest instance using the specified properties.
             * @function create
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {karna.command.ICommandRPCRequest=} [properties] Properties to set
             * @returns {karna.command.CommandRPCRequest} CommandRPCRequest instance
             */
            CommandRPCRequest.create = function create(properties) {
                return new CommandRPCRequest(properties);
            };

            /**
             * Encodes the specified CommandRPCRequest message. Does not implicitly {@link karna.command.CommandRPCRequest.verify|verify} messages.
             * @function encode
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {karna.command.ICommandRPCRequest} message CommandRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandRPCRequest.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.executeCommand != null && Object.hasOwnProperty.call(message, "executeCommand"))
                    $root.karna.command.CommandRequest.encode(message.executeCommand, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified CommandRPCRequest message, length delimited. Does not implicitly {@link karna.command.CommandRPCRequest.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {karna.command.ICommandRPCRequest} message CommandRPCRequest message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandRPCRequest.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CommandRPCRequest message from the specified reader or buffer.
             * @function decode
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.command.CommandRPCRequest} CommandRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandRPCRequest.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.command.CommandRPCRequest();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.executeCommand = $root.karna.command.CommandRequest.decode(reader, reader.uint32());
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
             * Decodes a CommandRPCRequest message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.command.CommandRPCRequest} CommandRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandRPCRequest.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CommandRPCRequest message.
             * @function verify
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CommandRPCRequest.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.executeCommand != null && message.hasOwnProperty("executeCommand")) {
                    properties.method = 1;
                    {
                        let error = $root.karna.command.CommandRequest.verify(message.executeCommand);
                        if (error)
                            return "executeCommand." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a CommandRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.command.CommandRPCRequest} CommandRPCRequest
             */
            CommandRPCRequest.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.command.CommandRPCRequest)
                    return object;
                let message = new $root.karna.command.CommandRPCRequest();
                if (object.executeCommand != null) {
                    if (typeof object.executeCommand !== "object")
                        throw TypeError(".karna.command.CommandRPCRequest.executeCommand: object expected");
                    message.executeCommand = $root.karna.command.CommandRequest.fromObject(object.executeCommand);
                }
                return message;
            };

            /**
             * Creates a plain object from a CommandRPCRequest message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {karna.command.CommandRPCRequest} message CommandRPCRequest
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CommandRPCRequest.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.executeCommand != null && message.hasOwnProperty("executeCommand")) {
                    object.executeCommand = $root.karna.command.CommandRequest.toObject(message.executeCommand, options);
                    if (options.oneofs)
                        object.method = "executeCommand";
                }
                return object;
            };

            /**
             * Converts this CommandRPCRequest to JSON.
             * @function toJSON
             * @memberof karna.command.CommandRPCRequest
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CommandRPCRequest.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CommandRPCRequest
             * @function getTypeUrl
             * @memberof karna.command.CommandRPCRequest
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CommandRPCRequest.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.command.CommandRPCRequest";
            };

            return CommandRPCRequest;
        })();

        command.CommandAction = (function() {

            /**
             * Properties of a CommandAction.
             * @memberof karna.command
             * @interface ICommandAction
             * @property {string|null} [type] CommandAction type
             * @property {Object.<string,string>|null} [coordinates] CommandAction coordinates
             * @property {string|null} [text] CommandAction text
             */

            /**
             * Constructs a new CommandAction.
             * @memberof karna.command
             * @classdesc Represents a CommandAction.
             * @implements ICommandAction
             * @constructor
             * @param {karna.command.ICommandAction=} [properties] Properties to set
             */
            function CommandAction(properties) {
                this.coordinates = {};
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CommandAction type.
             * @member {string} type
             * @memberof karna.command.CommandAction
             * @instance
             */
            CommandAction.prototype.type = "";

            /**
             * CommandAction coordinates.
             * @member {Object.<string,string>} coordinates
             * @memberof karna.command.CommandAction
             * @instance
             */
            CommandAction.prototype.coordinates = $util.emptyObject;

            /**
             * CommandAction text.
             * @member {string|null|undefined} text
             * @memberof karna.command.CommandAction
             * @instance
             */
            CommandAction.prototype.text = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            // Virtual OneOf for proto3 optional field
            Object.defineProperty(CommandAction.prototype, "_text", {
                get: $util.oneOfGetter($oneOfFields = ["text"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new CommandAction instance using the specified properties.
             * @function create
             * @memberof karna.command.CommandAction
             * @static
             * @param {karna.command.ICommandAction=} [properties] Properties to set
             * @returns {karna.command.CommandAction} CommandAction instance
             */
            CommandAction.create = function create(properties) {
                return new CommandAction(properties);
            };

            /**
             * Encodes the specified CommandAction message. Does not implicitly {@link karna.command.CommandAction.verify|verify} messages.
             * @function encode
             * @memberof karna.command.CommandAction
             * @static
             * @param {karna.command.ICommandAction} message CommandAction message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandAction.encode = function encode(message, writer) {
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
             * Encodes the specified CommandAction message, length delimited. Does not implicitly {@link karna.command.CommandAction.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.command.CommandAction
             * @static
             * @param {karna.command.ICommandAction} message CommandAction message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandAction.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CommandAction message from the specified reader or buffer.
             * @function decode
             * @memberof karna.command.CommandAction
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.command.CommandAction} CommandAction
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandAction.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.command.CommandAction(), key, value;
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
             * Decodes a CommandAction message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.command.CommandAction
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.command.CommandAction} CommandAction
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandAction.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CommandAction message.
             * @function verify
             * @memberof karna.command.CommandAction
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CommandAction.verify = function verify(message) {
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
             * Creates a CommandAction message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.command.CommandAction
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.command.CommandAction} CommandAction
             */
            CommandAction.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.command.CommandAction)
                    return object;
                let message = new $root.karna.command.CommandAction();
                if (object.type != null)
                    message.type = String(object.type);
                if (object.coordinates) {
                    if (typeof object.coordinates !== "object")
                        throw TypeError(".karna.command.CommandAction.coordinates: object expected");
                    message.coordinates = {};
                    for (let keys = Object.keys(object.coordinates), i = 0; i < keys.length; ++i)
                        message.coordinates[keys[i]] = String(object.coordinates[keys[i]]);
                }
                if (object.text != null)
                    message.text = String(object.text);
                return message;
            };

            /**
             * Creates a plain object from a CommandAction message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.command.CommandAction
             * @static
             * @param {karna.command.CommandAction} message CommandAction
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CommandAction.toObject = function toObject(message, options) {
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
             * Converts this CommandAction to JSON.
             * @function toJSON
             * @memberof karna.command.CommandAction
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CommandAction.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CommandAction
             * @function getTypeUrl
             * @memberof karna.command.CommandAction
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CommandAction.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.command.CommandAction";
            };

            return CommandAction;
        })();

        /**
         * CommandExecutionStatus enum.
         * @name karna.command.CommandExecutionStatus
         * @enum {number}
         * @property {number} PENDING=0 PENDING value
         * @property {number} IN_PROGRESS=1 IN_PROGRESS value
         * @property {number} COMPLETED=2 COMPLETED value
         * @property {number} FAILED=3 FAILED value
         */
        command.CommandExecutionStatus = (function() {
            const valuesById = {}, values = Object.create(valuesById);
            values[valuesById[0] = "PENDING"] = 0;
            values[valuesById[1] = "IN_PROGRESS"] = 1;
            values[valuesById[2] = "COMPLETED"] = 2;
            values[valuesById[3] = "FAILED"] = 3;
            return values;
        })();

        command.CommandResult = (function() {

            /**
             * Properties of a CommandResult.
             * @memberof karna.command
             * @interface ICommandResult
             * @property {string|null} [commandText] CommandResult commandText
             * @property {karna.command.CommandExecutionStatus|null} [status] CommandResult status
             * @property {string|null} [message] CommandResult message
             * @property {Array.<karna.command.ICommandAction>|null} [actions] CommandResult actions
             */

            /**
             * Constructs a new CommandResult.
             * @memberof karna.command
             * @classdesc Represents a CommandResult.
             * @implements ICommandResult
             * @constructor
             * @param {karna.command.ICommandResult=} [properties] Properties to set
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
             * @memberof karna.command.CommandResult
             * @instance
             */
            CommandResult.prototype.commandText = "";

            /**
             * CommandResult status.
             * @member {karna.command.CommandExecutionStatus} status
             * @memberof karna.command.CommandResult
             * @instance
             */
            CommandResult.prototype.status = 0;

            /**
             * CommandResult message.
             * @member {string} message
             * @memberof karna.command.CommandResult
             * @instance
             */
            CommandResult.prototype.message = "";

            /**
             * CommandResult actions.
             * @member {Array.<karna.command.ICommandAction>} actions
             * @memberof karna.command.CommandResult
             * @instance
             */
            CommandResult.prototype.actions = $util.emptyArray;

            /**
             * Creates a new CommandResult instance using the specified properties.
             * @function create
             * @memberof karna.command.CommandResult
             * @static
             * @param {karna.command.ICommandResult=} [properties] Properties to set
             * @returns {karna.command.CommandResult} CommandResult instance
             */
            CommandResult.create = function create(properties) {
                return new CommandResult(properties);
            };

            /**
             * Encodes the specified CommandResult message. Does not implicitly {@link karna.command.CommandResult.verify|verify} messages.
             * @function encode
             * @memberof karna.command.CommandResult
             * @static
             * @param {karna.command.ICommandResult} message CommandResult message or plain object to encode
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
                        $root.karna.command.CommandAction.encode(message.actions[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
                return writer;
            };

            /**
             * Encodes the specified CommandResult message, length delimited. Does not implicitly {@link karna.command.CommandResult.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.command.CommandResult
             * @static
             * @param {karna.command.ICommandResult} message CommandResult message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandResult.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CommandResult message from the specified reader or buffer.
             * @function decode
             * @memberof karna.command.CommandResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.command.CommandResult} CommandResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandResult.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.command.CommandResult();
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
                            message.actions.push($root.karna.command.CommandAction.decode(reader, reader.uint32()));
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
             * @memberof karna.command.CommandResult
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.command.CommandResult} CommandResult
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
             * @memberof karna.command.CommandResult
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
                        let error = $root.karna.command.CommandAction.verify(message.actions[i]);
                        if (error)
                            return "actions." + error;
                    }
                }
                return null;
            };

            /**
             * Creates a CommandResult message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.command.CommandResult
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.command.CommandResult} CommandResult
             */
            CommandResult.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.command.CommandResult)
                    return object;
                let message = new $root.karna.command.CommandResult();
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
                        throw TypeError(".karna.command.CommandResult.actions: array expected");
                    message.actions = [];
                    for (let i = 0; i < object.actions.length; ++i) {
                        if (typeof object.actions[i] !== "object")
                            throw TypeError(".karna.command.CommandResult.actions: object expected");
                        message.actions[i] = $root.karna.command.CommandAction.fromObject(object.actions[i]);
                    }
                }
                return message;
            };

            /**
             * Creates a plain object from a CommandResult message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.command.CommandResult
             * @static
             * @param {karna.command.CommandResult} message CommandResult
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
                    object.status = options.enums === String ? $root.karna.command.CommandExecutionStatus[message.status] === undefined ? message.status : $root.karna.command.CommandExecutionStatus[message.status] : message.status;
                if (message.message != null && message.hasOwnProperty("message"))
                    object.message = message.message;
                if (message.actions && message.actions.length) {
                    object.actions = [];
                    for (let j = 0; j < message.actions.length; ++j)
                        object.actions[j] = $root.karna.command.CommandAction.toObject(message.actions[j], options);
                }
                return object;
            };

            /**
             * Converts this CommandResult to JSON.
             * @function toJSON
             * @memberof karna.command.CommandResult
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CommandResult.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CommandResult
             * @function getTypeUrl
             * @memberof karna.command.CommandResult
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CommandResult.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.command.CommandResult";
            };

            return CommandResult;
        })();

        command.CommandRPCResponse = (function() {

            /**
             * Properties of a CommandRPCResponse.
             * @memberof karna.command
             * @interface ICommandRPCResponse
             * @property {karna.command.ICommandResult|null} [commandResponse] CommandRPCResponse commandResponse
             * @property {string|null} [error] CommandRPCResponse error
             */

            /**
             * Constructs a new CommandRPCResponse.
             * @memberof karna.command
             * @classdesc Represents a CommandRPCResponse.
             * @implements ICommandRPCResponse
             * @constructor
             * @param {karna.command.ICommandRPCResponse=} [properties] Properties to set
             */
            function CommandRPCResponse(properties) {
                if (properties)
                    for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                        if (properties[keys[i]] != null)
                            this[keys[i]] = properties[keys[i]];
            }

            /**
             * CommandRPCResponse commandResponse.
             * @member {karna.command.ICommandResult|null|undefined} commandResponse
             * @memberof karna.command.CommandRPCResponse
             * @instance
             */
            CommandRPCResponse.prototype.commandResponse = null;

            /**
             * CommandRPCResponse error.
             * @member {string|null|undefined} error
             * @memberof karna.command.CommandRPCResponse
             * @instance
             */
            CommandRPCResponse.prototype.error = null;

            // OneOf field names bound to virtual getters and setters
            let $oneOfFields;

            /**
             * CommandRPCResponse type.
             * @member {"commandResponse"|"error"|undefined} type
             * @memberof karna.command.CommandRPCResponse
             * @instance
             */
            Object.defineProperty(CommandRPCResponse.prototype, "type", {
                get: $util.oneOfGetter($oneOfFields = ["commandResponse", "error"]),
                set: $util.oneOfSetter($oneOfFields)
            });

            /**
             * Creates a new CommandRPCResponse instance using the specified properties.
             * @function create
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {karna.command.ICommandRPCResponse=} [properties] Properties to set
             * @returns {karna.command.CommandRPCResponse} CommandRPCResponse instance
             */
            CommandRPCResponse.create = function create(properties) {
                return new CommandRPCResponse(properties);
            };

            /**
             * Encodes the specified CommandRPCResponse message. Does not implicitly {@link karna.command.CommandRPCResponse.verify|verify} messages.
             * @function encode
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {karna.command.ICommandRPCResponse} message CommandRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandRPCResponse.encode = function encode(message, writer) {
                if (!writer)
                    writer = $Writer.create();
                if (message.commandResponse != null && Object.hasOwnProperty.call(message, "commandResponse"))
                    $root.karna.command.CommandResult.encode(message.commandResponse, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
                if (message.error != null && Object.hasOwnProperty.call(message, "error"))
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.error);
                return writer;
            };

            /**
             * Encodes the specified CommandRPCResponse message, length delimited. Does not implicitly {@link karna.command.CommandRPCResponse.verify|verify} messages.
             * @function encodeDelimited
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {karna.command.ICommandRPCResponse} message CommandRPCResponse message or plain object to encode
             * @param {$protobuf.Writer} [writer] Writer to encode to
             * @returns {$protobuf.Writer} Writer
             */
            CommandRPCResponse.encodeDelimited = function encodeDelimited(message, writer) {
                return this.encode(message, writer).ldelim();
            };

            /**
             * Decodes a CommandRPCResponse message from the specified reader or buffer.
             * @function decode
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @param {number} [length] Message length if known beforehand
             * @returns {karna.command.CommandRPCResponse} CommandRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandRPCResponse.decode = function decode(reader, length) {
                if (!(reader instanceof $Reader))
                    reader = $Reader.create(reader);
                let end = length === undefined ? reader.len : reader.pos + length, message = new $root.karna.command.CommandRPCResponse();
                while (reader.pos < end) {
                    let tag = reader.uint32();
                    switch (tag >>> 3) {
                    case 1: {
                            message.commandResponse = $root.karna.command.CommandResult.decode(reader, reader.uint32());
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
             * Decodes a CommandRPCResponse message from the specified reader or buffer, length delimited.
             * @function decodeDelimited
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
             * @returns {karna.command.CommandRPCResponse} CommandRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            CommandRPCResponse.decodeDelimited = function decodeDelimited(reader) {
                if (!(reader instanceof $Reader))
                    reader = new $Reader(reader);
                return this.decode(reader, reader.uint32());
            };

            /**
             * Verifies a CommandRPCResponse message.
             * @function verify
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {Object.<string,*>} message Plain object to verify
             * @returns {string|null} `null` if valid, otherwise the reason why it is not
             */
            CommandRPCResponse.verify = function verify(message) {
                if (typeof message !== "object" || message === null)
                    return "object expected";
                let properties = {};
                if (message.commandResponse != null && message.hasOwnProperty("commandResponse")) {
                    properties.type = 1;
                    {
                        let error = $root.karna.command.CommandResult.verify(message.commandResponse);
                        if (error)
                            return "commandResponse." + error;
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
             * Creates a CommandRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @function fromObject
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {Object.<string,*>} object Plain object
             * @returns {karna.command.CommandRPCResponse} CommandRPCResponse
             */
            CommandRPCResponse.fromObject = function fromObject(object) {
                if (object instanceof $root.karna.command.CommandRPCResponse)
                    return object;
                let message = new $root.karna.command.CommandRPCResponse();
                if (object.commandResponse != null) {
                    if (typeof object.commandResponse !== "object")
                        throw TypeError(".karna.command.CommandRPCResponse.commandResponse: object expected");
                    message.commandResponse = $root.karna.command.CommandResult.fromObject(object.commandResponse);
                }
                if (object.error != null)
                    message.error = String(object.error);
                return message;
            };

            /**
             * Creates a plain object from a CommandRPCResponse message. Also converts values to other types if specified.
             * @function toObject
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {karna.command.CommandRPCResponse} message CommandRPCResponse
             * @param {$protobuf.IConversionOptions} [options] Conversion options
             * @returns {Object.<string,*>} Plain object
             */
            CommandRPCResponse.toObject = function toObject(message, options) {
                if (!options)
                    options = {};
                let object = {};
                if (message.commandResponse != null && message.hasOwnProperty("commandResponse")) {
                    object.commandResponse = $root.karna.command.CommandResult.toObject(message.commandResponse, options);
                    if (options.oneofs)
                        object.type = "commandResponse";
                }
                if (message.error != null && message.hasOwnProperty("error")) {
                    object.error = message.error;
                    if (options.oneofs)
                        object.type = "error";
                }
                return object;
            };

            /**
             * Converts this CommandRPCResponse to JSON.
             * @function toJSON
             * @memberof karna.command.CommandRPCResponse
             * @instance
             * @returns {Object.<string,*>} JSON object
             */
            CommandRPCResponse.prototype.toJSON = function toJSON() {
                return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
            };

            /**
             * Gets the default type url for CommandRPCResponse
             * @function getTypeUrl
             * @memberof karna.command.CommandRPCResponse
             * @static
             * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns {string} The default type url
             */
            CommandRPCResponse.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
                if (typeUrlPrefix === undefined) {
                    typeUrlPrefix = "type.googleapis.com";
                }
                return typeUrlPrefix + "/karna.command.CommandRPCResponse";
            };

            return CommandRPCResponse;
        })();

        return command;
    })();

    return karna;
})();

export { $root as default };
