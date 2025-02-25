import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace karna. */
export namespace karna {

    /** Namespace status. */
    namespace status {

        /** Properties of a StatusRequest. */
        interface IStatusRequest {
        }

        /** Represents a StatusRequest. */
        class StatusRequest implements IStatusRequest {

            /**
             * Constructs a new StatusRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.status.IStatusRequest);

            /**
             * Creates a new StatusRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns StatusRequest instance
             */
            public static create(properties?: karna.status.IStatusRequest): karna.status.StatusRequest;

            /**
             * Encodes the specified StatusRequest message. Does not implicitly {@link karna.status.StatusRequest.verify|verify} messages.
             * @param message StatusRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.status.IStatusRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified StatusRequest message, length delimited. Does not implicitly {@link karna.status.StatusRequest.verify|verify} messages.
             * @param message StatusRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.status.IStatusRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a StatusRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns StatusRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.status.StatusRequest;

            /**
             * Decodes a StatusRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns StatusRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.status.StatusRequest;

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
            public static fromObject(object: { [k: string]: any }): karna.status.StatusRequest;

            /**
             * Creates a plain object from a StatusRequest message. Also converts values to other types if specified.
             * @param message StatusRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.status.StatusRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

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

        /** Properties of a StatusRPCRequest. */
        interface IStatusRPCRequest {

            /** StatusRPCRequest getStatus */
            getStatus?: (karna.status.IStatusRequest|null);
        }

        /** Represents a StatusRPCRequest. */
        class StatusRPCRequest implements IStatusRPCRequest {

            /**
             * Constructs a new StatusRPCRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.status.IStatusRPCRequest);

            /** StatusRPCRequest getStatus. */
            public getStatus?: (karna.status.IStatusRequest|null);

            /** StatusRPCRequest method. */
            public method?: "getStatus";

            /**
             * Creates a new StatusRPCRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns StatusRPCRequest instance
             */
            public static create(properties?: karna.status.IStatusRPCRequest): karna.status.StatusRPCRequest;

            /**
             * Encodes the specified StatusRPCRequest message. Does not implicitly {@link karna.status.StatusRPCRequest.verify|verify} messages.
             * @param message StatusRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.status.IStatusRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified StatusRPCRequest message, length delimited. Does not implicitly {@link karna.status.StatusRPCRequest.verify|verify} messages.
             * @param message StatusRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.status.IStatusRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a StatusRPCRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns StatusRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.status.StatusRPCRequest;

            /**
             * Decodes a StatusRPCRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns StatusRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.status.StatusRPCRequest;

            /**
             * Verifies a StatusRPCRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a StatusRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns StatusRPCRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.status.StatusRPCRequest;

            /**
             * Creates a plain object from a StatusRPCRequest message. Also converts values to other types if specified.
             * @param message StatusRPCRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.status.StatusRPCRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this StatusRPCRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for StatusRPCRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a StatusResult. */
        interface IStatusResult {

            /** StatusResult vision */
            vision?: (string|null);

            /** StatusResult language */
            language?: (string|null);

            /** StatusResult command */
            command?: (string|null);
        }

        /** Represents a StatusResult. */
        class StatusResult implements IStatusResult {

            /**
             * Constructs a new StatusResult.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.status.IStatusResult);

            /** StatusResult vision. */
            public vision: string;

            /** StatusResult language. */
            public language: string;

            /** StatusResult command. */
            public command: string;

            /**
             * Creates a new StatusResult instance using the specified properties.
             * @param [properties] Properties to set
             * @returns StatusResult instance
             */
            public static create(properties?: karna.status.IStatusResult): karna.status.StatusResult;

            /**
             * Encodes the specified StatusResult message. Does not implicitly {@link karna.status.StatusResult.verify|verify} messages.
             * @param message StatusResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.status.IStatusResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified StatusResult message, length delimited. Does not implicitly {@link karna.status.StatusResult.verify|verify} messages.
             * @param message StatusResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.status.IStatusResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a StatusResult message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns StatusResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.status.StatusResult;

            /**
             * Decodes a StatusResult message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns StatusResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.status.StatusResult;

            /**
             * Verifies a StatusResult message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a StatusResult message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns StatusResult
             */
            public static fromObject(object: { [k: string]: any }): karna.status.StatusResult;

            /**
             * Creates a plain object from a StatusResult message. Also converts values to other types if specified.
             * @param message StatusResult
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.status.StatusResult, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this StatusResult to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for StatusResult
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a StatusRPCResponse. */
        interface IStatusRPCResponse {

            /** StatusRPCResponse statusUpdate */
            statusUpdate?: (karna.status.IStatusResult|null);

            /** StatusRPCResponse error */
            error?: (string|null);
        }

        /** Represents a StatusRPCResponse. */
        class StatusRPCResponse implements IStatusRPCResponse {

            /**
             * Constructs a new StatusRPCResponse.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.status.IStatusRPCResponse);

            /** StatusRPCResponse statusUpdate. */
            public statusUpdate?: (karna.status.IStatusResult|null);

            /** StatusRPCResponse error. */
            public error?: (string|null);

            /** StatusRPCResponse type. */
            public type?: ("statusUpdate"|"error");

            /**
             * Creates a new StatusRPCResponse instance using the specified properties.
             * @param [properties] Properties to set
             * @returns StatusRPCResponse instance
             */
            public static create(properties?: karna.status.IStatusRPCResponse): karna.status.StatusRPCResponse;

            /**
             * Encodes the specified StatusRPCResponse message. Does not implicitly {@link karna.status.StatusRPCResponse.verify|verify} messages.
             * @param message StatusRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.status.IStatusRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified StatusRPCResponse message, length delimited. Does not implicitly {@link karna.status.StatusRPCResponse.verify|verify} messages.
             * @param message StatusRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.status.IStatusRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a StatusRPCResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns StatusRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.status.StatusRPCResponse;

            /**
             * Decodes a StatusRPCResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns StatusRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.status.StatusRPCResponse;

            /**
             * Verifies a StatusRPCResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a StatusRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns StatusRPCResponse
             */
            public static fromObject(object: { [k: string]: any }): karna.status.StatusRPCResponse;

            /**
             * Creates a plain object from a StatusRPCResponse message. Also converts values to other types if specified.
             * @param message StatusRPCResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.status.StatusRPCResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this StatusRPCResponse to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for StatusRPCResponse
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }
    }
}
