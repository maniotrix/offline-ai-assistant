import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace karna. */
export namespace karna {

    /** Properties of a RPCRequest. */
    interface IRPCRequest {

        /** RPCRequest executeCommand */
        executeCommand?: (karna.ICommandRequest|null);

        /** RPCRequest getStatus */
        getStatus?: (karna.IStatusRequest|null);
    }

    /** Represents a RPCRequest. */
    class RPCRequest implements IRPCRequest {

        /**
         * Constructs a new RPCRequest.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.IRPCRequest);

        /** RPCRequest executeCommand. */
        public executeCommand?: (karna.ICommandRequest|null);

        /** RPCRequest getStatus. */
        public getStatus?: (karna.IStatusRequest|null);

        /** RPCRequest method. */
        public method?: ("executeCommand"|"getStatus");

        /**
         * Creates a new RPCRequest instance using the specified properties.
         * @param [properties] Properties to set
         * @returns RPCRequest instance
         */
        public static create(properties?: karna.IRPCRequest): karna.RPCRequest;

        /**
         * Encodes the specified RPCRequest message. Does not implicitly {@link karna.RPCRequest.verify|verify} messages.
         * @param message RPCRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.IRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified RPCRequest message, length delimited. Does not implicitly {@link karna.RPCRequest.verify|verify} messages.
         * @param message RPCRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.IRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a RPCRequest message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns RPCRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.RPCRequest;

        /**
         * Decodes a RPCRequest message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns RPCRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.RPCRequest;

        /**
         * Verifies a RPCRequest message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a RPCRequest message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns RPCRequest
         */
        public static fromObject(object: { [k: string]: any }): karna.RPCRequest;

        /**
         * Creates a plain object from a RPCRequest message. Also converts values to other types if specified.
         * @param message RPCRequest
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.RPCRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this RPCRequest to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for RPCRequest
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

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
        constructor(properties?: karna.ICommandRequest);

        /** CommandRequest command. */
        public command: string;

        /** CommandRequest domain. */
        public domain: string;

        /**
         * Creates a new CommandRequest instance using the specified properties.
         * @param [properties] Properties to set
         * @returns CommandRequest instance
         */
        public static create(properties?: karna.ICommandRequest): karna.CommandRequest;

        /**
         * Encodes the specified CommandRequest message. Does not implicitly {@link karna.CommandRequest.verify|verify} messages.
         * @param message CommandRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.ICommandRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified CommandRequest message, length delimited. Does not implicitly {@link karna.CommandRequest.verify|verify} messages.
         * @param message CommandRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.ICommandRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a CommandRequest message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns CommandRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.CommandRequest;

        /**
         * Decodes a CommandRequest message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns CommandRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.CommandRequest;

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
        public static fromObject(object: { [k: string]: any }): karna.CommandRequest;

        /**
         * Creates a plain object from a CommandRequest message. Also converts values to other types if specified.
         * @param message CommandRequest
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.CommandRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

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

    /** Properties of a StatusRequest. */
    interface IStatusRequest {
    }

    /** Represents a StatusRequest. */
    class StatusRequest implements IStatusRequest {

        /**
         * Constructs a new StatusRequest.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.IStatusRequest);

        /**
         * Creates a new StatusRequest instance using the specified properties.
         * @param [properties] Properties to set
         * @returns StatusRequest instance
         */
        public static create(properties?: karna.IStatusRequest): karna.StatusRequest;

        /**
         * Encodes the specified StatusRequest message. Does not implicitly {@link karna.StatusRequest.verify|verify} messages.
         * @param message StatusRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.IStatusRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified StatusRequest message, length delimited. Does not implicitly {@link karna.StatusRequest.verify|verify} messages.
         * @param message StatusRequest message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.IStatusRequest, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a StatusRequest message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns StatusRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.StatusRequest;

        /**
         * Decodes a StatusRequest message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns StatusRequest
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.StatusRequest;

        /**
         * Verifies a StatusRequest message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a StatusRequest message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns StatusRequest
         */
        public static fromObject(object: { [k: string]: any }): karna.StatusRequest;

        /**
         * Creates a plain object from a StatusRequest message. Also converts values to other types if specified.
         * @param message StatusRequest
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.StatusRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this StatusRequest to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for StatusRequest
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a RPCResponse. */
    interface IRPCResponse {

        /** RPCResponse commandResponse */
        commandResponse?: (karna.ICommandResult|null);

        /** RPCResponse statusUpdate */
        statusUpdate?: (karna.IStatus|null);

        /** RPCResponse error */
        error?: (string|null);
    }

    /** Represents a RPCResponse. */
    class RPCResponse implements IRPCResponse {

        /**
         * Constructs a new RPCResponse.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.IRPCResponse);

        /** RPCResponse commandResponse. */
        public commandResponse?: (karna.ICommandResult|null);

        /** RPCResponse statusUpdate. */
        public statusUpdate?: (karna.IStatus|null);

        /** RPCResponse error. */
        public error?: (string|null);

        /** RPCResponse type. */
        public type?: ("commandResponse"|"statusUpdate"|"error");

        /**
         * Creates a new RPCResponse instance using the specified properties.
         * @param [properties] Properties to set
         * @returns RPCResponse instance
         */
        public static create(properties?: karna.IRPCResponse): karna.RPCResponse;

        /**
         * Encodes the specified RPCResponse message. Does not implicitly {@link karna.RPCResponse.verify|verify} messages.
         * @param message RPCResponse message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.IRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified RPCResponse message, length delimited. Does not implicitly {@link karna.RPCResponse.verify|verify} messages.
         * @param message RPCResponse message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.IRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a RPCResponse message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns RPCResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.RPCResponse;

        /**
         * Decodes a RPCResponse message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns RPCResponse
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.RPCResponse;

        /**
         * Verifies a RPCResponse message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a RPCResponse message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns RPCResponse
         */
        public static fromObject(object: { [k: string]: any }): karna.RPCResponse;

        /**
         * Creates a plain object from a RPCResponse message. Also converts values to other types if specified.
         * @param message RPCResponse
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.RPCResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this RPCResponse to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for RPCResponse
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a CommandResult. */
    interface ICommandResult {

        /** CommandResult commandText */
        commandText?: (string|null);

        /** CommandResult status */
        status?: (karna.TaskStatus|null);

        /** CommandResult message */
        message?: (string|null);

        /** CommandResult actions */
        actions?: (karna.IAction[]|null);
    }

    /** Represents a CommandResult. */
    class CommandResult implements ICommandResult {

        /**
         * Constructs a new CommandResult.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.ICommandResult);

        /** CommandResult commandText. */
        public commandText: string;

        /** CommandResult status. */
        public status: karna.TaskStatus;

        /** CommandResult message. */
        public message: string;

        /** CommandResult actions. */
        public actions: karna.IAction[];

        /**
         * Creates a new CommandResult instance using the specified properties.
         * @param [properties] Properties to set
         * @returns CommandResult instance
         */
        public static create(properties?: karna.ICommandResult): karna.CommandResult;

        /**
         * Encodes the specified CommandResult message. Does not implicitly {@link karna.CommandResult.verify|verify} messages.
         * @param message CommandResult message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.ICommandResult, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified CommandResult message, length delimited. Does not implicitly {@link karna.CommandResult.verify|verify} messages.
         * @param message CommandResult message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.ICommandResult, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a CommandResult message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns CommandResult
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.CommandResult;

        /**
         * Decodes a CommandResult message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns CommandResult
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.CommandResult;

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
        public static fromObject(object: { [k: string]: any }): karna.CommandResult;

        /**
         * Creates a plain object from a CommandResult message. Also converts values to other types if specified.
         * @param message CommandResult
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.CommandResult, options?: $protobuf.IConversionOptions): { [k: string]: any };

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

    /** Properties of a Status. */
    interface IStatus {

        /** Status vision */
        vision?: (string|null);

        /** Status language */
        language?: (string|null);

        /** Status command */
        command?: (string|null);
    }

    /** Represents a Status. */
    class Status implements IStatus {

        /**
         * Constructs a new Status.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.IStatus);

        /** Status vision. */
        public vision: string;

        /** Status language. */
        public language: string;

        /** Status command. */
        public command: string;

        /**
         * Creates a new Status instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Status instance
         */
        public static create(properties?: karna.IStatus): karna.Status;

        /**
         * Encodes the specified Status message. Does not implicitly {@link karna.Status.verify|verify} messages.
         * @param message Status message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.IStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Status message, length delimited. Does not implicitly {@link karna.Status.verify|verify} messages.
         * @param message Status message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.IStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Status message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.Status;

        /**
         * Decodes a Status message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Status
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.Status;

        /**
         * Verifies a Status message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Status message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Status
         */
        public static fromObject(object: { [k: string]: any }): karna.Status;

        /**
         * Creates a plain object from a Status message. Also converts values to other types if specified.
         * @param message Status
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.Status, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Status to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Status
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an Action. */
    interface IAction {

        /** Action type */
        type?: (string|null);

        /** Action coordinates */
        coordinates?: ({ [k: string]: string }|null);

        /** Action text */
        text?: (string|null);
    }

    /** Represents an Action. */
    class Action implements IAction {

        /**
         * Constructs a new Action.
         * @param [properties] Properties to set
         */
        constructor(properties?: karna.IAction);

        /** Action type. */
        public type: string;

        /** Action coordinates. */
        public coordinates: { [k: string]: string };

        /** Action text. */
        public text?: (string|null);

        /**
         * Creates a new Action instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Action instance
         */
        public static create(properties?: karna.IAction): karna.Action;

        /**
         * Encodes the specified Action message. Does not implicitly {@link karna.Action.verify|verify} messages.
         * @param message Action message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: karna.IAction, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Action message, length delimited. Does not implicitly {@link karna.Action.verify|verify} messages.
         * @param message Action message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: karna.IAction, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an Action message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Action
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.Action;

        /**
         * Decodes an Action message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Action
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.Action;

        /**
         * Verifies an Action message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an Action message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Action
         */
        public static fromObject(object: { [k: string]: any }): karna.Action;

        /**
         * Creates a plain object from an Action message. Also converts values to other types if specified.
         * @param message Action
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: karna.Action, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Action to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Action
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** TaskStatus enum. */
    enum TaskStatus {
        PENDING = 0,
        IN_PROGRESS = 1,
        COMPLETED = 2,
        FAILED = 3
    }
}
