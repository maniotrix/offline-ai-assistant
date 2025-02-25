import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace karna. */
export namespace karna {

    /** Namespace command. */
    namespace command {

        /** Properties of a CommandRequest. */
        interface ICommandRequest {

            /** CommandRequest command */
            command?: (string|null);

            /** CommandRequest domain */
            domain?: (string|null);
        }

        /** Represents a CommandRequest. */
        class CommandRequest implements ICommandRequest {

            /**
             * Constructs a new CommandRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.command.ICommandRequest);

            /** CommandRequest command. */
            public command: string;

            /** CommandRequest domain. */
            public domain: string;

            /**
             * Creates a new CommandRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CommandRequest instance
             */
            public static create(properties?: karna.command.ICommandRequest): karna.command.CommandRequest;

            /**
             * Encodes the specified CommandRequest message. Does not implicitly {@link karna.command.CommandRequest.verify|verify} messages.
             * @param message CommandRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.command.ICommandRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CommandRequest message, length delimited. Does not implicitly {@link karna.command.CommandRequest.verify|verify} messages.
             * @param message CommandRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.command.ICommandRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CommandRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CommandRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.command.CommandRequest;

            /**
             * Decodes a CommandRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CommandRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.command.CommandRequest;

            /**
             * Verifies a CommandRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CommandRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CommandRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.command.CommandRequest;

            /**
             * Creates a plain object from a CommandRequest message. Also converts values to other types if specified.
             * @param message CommandRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.command.CommandRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CommandRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CommandRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a CommandRPCRequest. */
        interface ICommandRPCRequest {

            /** CommandRPCRequest executeCommand */
            executeCommand?: (karna.command.ICommandRequest|null);
        }

        /** Represents a CommandRPCRequest. */
        class CommandRPCRequest implements ICommandRPCRequest {

            /**
             * Constructs a new CommandRPCRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.command.ICommandRPCRequest);

            /** CommandRPCRequest executeCommand. */
            public executeCommand?: (karna.command.ICommandRequest|null);

            /** CommandRPCRequest method. */
            public method?: "executeCommand";

            /**
             * Creates a new CommandRPCRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CommandRPCRequest instance
             */
            public static create(properties?: karna.command.ICommandRPCRequest): karna.command.CommandRPCRequest;

            /**
             * Encodes the specified CommandRPCRequest message. Does not implicitly {@link karna.command.CommandRPCRequest.verify|verify} messages.
             * @param message CommandRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.command.ICommandRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CommandRPCRequest message, length delimited. Does not implicitly {@link karna.command.CommandRPCRequest.verify|verify} messages.
             * @param message CommandRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.command.ICommandRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CommandRPCRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CommandRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.command.CommandRPCRequest;

            /**
             * Decodes a CommandRPCRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CommandRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.command.CommandRPCRequest;

            /**
             * Verifies a CommandRPCRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CommandRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CommandRPCRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.command.CommandRPCRequest;

            /**
             * Creates a plain object from a CommandRPCRequest message. Also converts values to other types if specified.
             * @param message CommandRPCRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.command.CommandRPCRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CommandRPCRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CommandRPCRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a CommandAction. */
        interface ICommandAction {

            /** CommandAction type */
            type?: (string|null);

            /** CommandAction coordinates */
            coordinates?: ({ [k: string]: string }|null);

            /** CommandAction text */
            text?: (string|null);
        }

        /** Represents a CommandAction. */
        class CommandAction implements ICommandAction {

            /**
             * Constructs a new CommandAction.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.command.ICommandAction);

            /** CommandAction type. */
            public type: string;

            /** CommandAction coordinates. */
            public coordinates: { [k: string]: string };

            /** CommandAction text. */
            public text?: (string|null);

            /**
             * Creates a new CommandAction instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CommandAction instance
             */
            public static create(properties?: karna.command.ICommandAction): karna.command.CommandAction;

            /**
             * Encodes the specified CommandAction message. Does not implicitly {@link karna.command.CommandAction.verify|verify} messages.
             * @param message CommandAction message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.command.ICommandAction, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CommandAction message, length delimited. Does not implicitly {@link karna.command.CommandAction.verify|verify} messages.
             * @param message CommandAction message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.command.ICommandAction, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CommandAction message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CommandAction
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.command.CommandAction;

            /**
             * Decodes a CommandAction message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CommandAction
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.command.CommandAction;

            /**
             * Verifies a CommandAction message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CommandAction message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CommandAction
             */
            public static fromObject(object: { [k: string]: any }): karna.command.CommandAction;

            /**
             * Creates a plain object from a CommandAction message. Also converts values to other types if specified.
             * @param message CommandAction
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.command.CommandAction, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CommandAction to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CommandAction
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** CommandExecutionStatus enum. */
        enum CommandExecutionStatus {
            PENDING = 0,
            IN_PROGRESS = 1,
            COMPLETED = 2,
            FAILED = 3
        }

        /** Properties of a CommandResult. */
        interface ICommandResult {

            /** CommandResult commandText */
            commandText?: (string|null);

            /** CommandResult status */
            status?: (karna.command.CommandExecutionStatus|null);

            /** CommandResult message */
            message?: (string|null);

            /** CommandResult actions */
            actions?: (karna.command.ICommandAction[]|null);
        }

        /** Represents a CommandResult. */
        class CommandResult implements ICommandResult {

            /**
             * Constructs a new CommandResult.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.command.ICommandResult);

            /** CommandResult commandText. */
            public commandText: string;

            /** CommandResult status. */
            public status: karna.command.CommandExecutionStatus;

            /** CommandResult message. */
            public message: string;

            /** CommandResult actions. */
            public actions: karna.command.ICommandAction[];

            /**
             * Creates a new CommandResult instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CommandResult instance
             */
            public static create(properties?: karna.command.ICommandResult): karna.command.CommandResult;

            /**
             * Encodes the specified CommandResult message. Does not implicitly {@link karna.command.CommandResult.verify|verify} messages.
             * @param message CommandResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.command.ICommandResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CommandResult message, length delimited. Does not implicitly {@link karna.command.CommandResult.verify|verify} messages.
             * @param message CommandResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.command.ICommandResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CommandResult message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CommandResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.command.CommandResult;

            /**
             * Decodes a CommandResult message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CommandResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.command.CommandResult;

            /**
             * Verifies a CommandResult message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CommandResult message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CommandResult
             */
            public static fromObject(object: { [k: string]: any }): karna.command.CommandResult;

            /**
             * Creates a plain object from a CommandResult message. Also converts values to other types if specified.
             * @param message CommandResult
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.command.CommandResult, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CommandResult to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CommandResult
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a CommandRPCResponse. */
        interface ICommandRPCResponse {

            /** CommandRPCResponse commandResponse */
            commandResponse?: (karna.command.ICommandResult|null);

            /** CommandRPCResponse error */
            error?: (string|null);
        }

        /** Represents a CommandRPCResponse. */
        class CommandRPCResponse implements ICommandRPCResponse {

            /**
             * Constructs a new CommandRPCResponse.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.command.ICommandRPCResponse);

            /** CommandRPCResponse commandResponse. */
            public commandResponse?: (karna.command.ICommandResult|null);

            /** CommandRPCResponse error. */
            public error?: (string|null);

            /** CommandRPCResponse type. */
            public type?: ("commandResponse"|"error");

            /**
             * Creates a new CommandRPCResponse instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CommandRPCResponse instance
             */
            public static create(properties?: karna.command.ICommandRPCResponse): karna.command.CommandRPCResponse;

            /**
             * Encodes the specified CommandRPCResponse message. Does not implicitly {@link karna.command.CommandRPCResponse.verify|verify} messages.
             * @param message CommandRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.command.ICommandRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CommandRPCResponse message, length delimited. Does not implicitly {@link karna.command.CommandRPCResponse.verify|verify} messages.
             * @param message CommandRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.command.ICommandRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CommandRPCResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CommandRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.command.CommandRPCResponse;

            /**
             * Decodes a CommandRPCResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CommandRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.command.CommandRPCResponse;

            /**
             * Verifies a CommandRPCResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CommandRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CommandRPCResponse
             */
            public static fromObject(object: { [k: string]: any }): karna.command.CommandRPCResponse;

            /**
             * Creates a plain object from a CommandRPCResponse message. Also converts values to other types if specified.
             * @param message CommandRPCResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.command.CommandRPCResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CommandRPCResponse to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CommandRPCResponse
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }
    }
}
