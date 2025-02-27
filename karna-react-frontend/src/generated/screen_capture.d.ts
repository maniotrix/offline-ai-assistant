import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace karna. */
export namespace karna {

    /** Namespace screen_capture. */
    namespace screen_capture {

        /** Properties of a CaptureRequest. */
        interface ICaptureRequest {

            /** CaptureRequest projectUuid */
            projectUuid?: (string|null);

            /** CaptureRequest commandUuid */
            commandUuid?: (string|null);
        }

        /** Represents a CaptureRequest. */
        class CaptureRequest implements ICaptureRequest {

            /**
             * Constructs a new CaptureRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.ICaptureRequest);

            /** CaptureRequest projectUuid. */
            public projectUuid: string;

            /** CaptureRequest commandUuid. */
            public commandUuid: string;

            /**
             * Creates a new CaptureRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CaptureRequest instance
             */
            public static create(properties?: karna.screen_capture.ICaptureRequest): karna.screen_capture.CaptureRequest;

            /**
             * Encodes the specified CaptureRequest message. Does not implicitly {@link karna.screen_capture.CaptureRequest.verify|verify} messages.
             * @param message CaptureRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.ICaptureRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CaptureRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureRequest.verify|verify} messages.
             * @param message CaptureRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.ICaptureRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CaptureRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CaptureRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.CaptureRequest;

            /**
             * Decodes a CaptureRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CaptureRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.CaptureRequest;

            /**
             * Verifies a CaptureRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CaptureRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CaptureRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.CaptureRequest;

            /**
             * Creates a plain object from a CaptureRequest message. Also converts values to other types if specified.
             * @param message CaptureRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.CaptureRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CaptureRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CaptureRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a ScreenCaptureRPCRequest. */
        interface IScreenCaptureRPCRequest {

            /** ScreenCaptureRPCRequest startCapture */
            startCapture?: (karna.screen_capture.ICaptureRequest|null);

            /** ScreenCaptureRPCRequest stopCapture */
            stopCapture?: (karna.screen_capture.ICaptureRequest|null);
        }

        /** Represents a ScreenCaptureRPCRequest. */
        class ScreenCaptureRPCRequest implements IScreenCaptureRPCRequest {

            /**
             * Constructs a new ScreenCaptureRPCRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.IScreenCaptureRPCRequest);

            /** ScreenCaptureRPCRequest startCapture. */
            public startCapture?: (karna.screen_capture.ICaptureRequest|null);

            /** ScreenCaptureRPCRequest stopCapture. */
            public stopCapture?: (karna.screen_capture.ICaptureRequest|null);

            /** ScreenCaptureRPCRequest method. */
            public method?: ("startCapture"|"stopCapture");

            /**
             * Creates a new ScreenCaptureRPCRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns ScreenCaptureRPCRequest instance
             */
            public static create(properties?: karna.screen_capture.IScreenCaptureRPCRequest): karna.screen_capture.ScreenCaptureRPCRequest;

            /**
             * Encodes the specified ScreenCaptureRPCRequest message. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCRequest.verify|verify} messages.
             * @param message ScreenCaptureRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.IScreenCaptureRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ScreenCaptureRPCRequest message, length delimited. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCRequest.verify|verify} messages.
             * @param message ScreenCaptureRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.IScreenCaptureRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a ScreenCaptureRPCRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ScreenCaptureRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.ScreenCaptureRPCRequest;

            /**
             * Decodes a ScreenCaptureRPCRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ScreenCaptureRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.ScreenCaptureRPCRequest;

            /**
             * Verifies a ScreenCaptureRPCRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a ScreenCaptureRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ScreenCaptureRPCRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.ScreenCaptureRPCRequest;

            /**
             * Creates a plain object from a ScreenCaptureRPCRequest message. Also converts values to other types if specified.
             * @param message ScreenCaptureRPCRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.ScreenCaptureRPCRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this ScreenCaptureRPCRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for ScreenCaptureRPCRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a RpcScreenshotEvent. */
        interface IRpcScreenshotEvent {

            /** RpcScreenshotEvent projectUuid */
            projectUuid?: (string|null);

            /** RpcScreenshotEvent commandUuid */
            commandUuid?: (string|null);

            /** RpcScreenshotEvent timestamp */
            timestamp?: (string|null);

            /** RpcScreenshotEvent description */
            description?: (string|null);

            /** RpcScreenshotEvent screenshotPath */
            screenshotPath?: (string|null);

            /** RpcScreenshotEvent annotationPath */
            annotationPath?: (string|null);

            /** RpcScreenshotEvent mouseX */
            mouseX?: (number|null);

            /** RpcScreenshotEvent mouseY */
            mouseY?: (number|null);

            /** RpcScreenshotEvent keyChar */
            keyChar?: (string|null);

            /** RpcScreenshotEvent keyCode */
            keyCode?: (string|null);

            /** RpcScreenshotEvent isSpecialKey */
            isSpecialKey?: (boolean|null);
        }

        /** Represents a RpcScreenshotEvent. */
        class RpcScreenshotEvent implements IRpcScreenshotEvent {

            /**
             * Constructs a new RpcScreenshotEvent.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.IRpcScreenshotEvent);

            /** RpcScreenshotEvent projectUuid. */
            public projectUuid: string;

            /** RpcScreenshotEvent commandUuid. */
            public commandUuid: string;

            /** RpcScreenshotEvent timestamp. */
            public timestamp: string;

            /** RpcScreenshotEvent description. */
            public description: string;

            /** RpcScreenshotEvent screenshotPath. */
            public screenshotPath: string;

            /** RpcScreenshotEvent annotationPath. */
            public annotationPath?: (string|null);

            /** RpcScreenshotEvent mouseX. */
            public mouseX?: (number|null);

            /** RpcScreenshotEvent mouseY. */
            public mouseY?: (number|null);

            /** RpcScreenshotEvent keyChar. */
            public keyChar?: (string|null);

            /** RpcScreenshotEvent keyCode. */
            public keyCode?: (string|null);

            /** RpcScreenshotEvent isSpecialKey. */
            public isSpecialKey: boolean;

            /**
             * Creates a new RpcScreenshotEvent instance using the specified properties.
             * @param [properties] Properties to set
             * @returns RpcScreenshotEvent instance
             */
            public static create(properties?: karna.screen_capture.IRpcScreenshotEvent): karna.screen_capture.RpcScreenshotEvent;

            /**
             * Encodes the specified RpcScreenshotEvent message. Does not implicitly {@link karna.screen_capture.RpcScreenshotEvent.verify|verify} messages.
             * @param message RpcScreenshotEvent message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.IRpcScreenshotEvent, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified RpcScreenshotEvent message, length delimited. Does not implicitly {@link karna.screen_capture.RpcScreenshotEvent.verify|verify} messages.
             * @param message RpcScreenshotEvent message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.IRpcScreenshotEvent, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a RpcScreenshotEvent message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns RpcScreenshotEvent
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.RpcScreenshotEvent;

            /**
             * Decodes a RpcScreenshotEvent message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns RpcScreenshotEvent
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.RpcScreenshotEvent;

            /**
             * Verifies a RpcScreenshotEvent message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a RpcScreenshotEvent message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns RpcScreenshotEvent
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.RpcScreenshotEvent;

            /**
             * Creates a plain object from a RpcScreenshotEvent message. Also converts values to other types if specified.
             * @param message RpcScreenshotEvent
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.RpcScreenshotEvent, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this RpcScreenshotEvent to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for RpcScreenshotEvent
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a CaptureResult. */
        interface ICaptureResult {

            /** CaptureResult projectUuid */
            projectUuid?: (string|null);

            /** CaptureResult commandUuid */
            commandUuid?: (string|null);

            /** CaptureResult isActive */
            isActive?: (boolean|null);

            /** CaptureResult message */
            message?: (string|null);

            /** CaptureResult screenshotEvents */
            screenshotEvents?: (karna.screen_capture.IRpcScreenshotEvent[]|null);
        }

        /** Represents a CaptureResult. */
        class CaptureResult implements ICaptureResult {

            /**
             * Constructs a new CaptureResult.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.ICaptureResult);

            /** CaptureResult projectUuid. */
            public projectUuid: string;

            /** CaptureResult commandUuid. */
            public commandUuid: string;

            /** CaptureResult isActive. */
            public isActive: boolean;

            /** CaptureResult message. */
            public message: string;

            /** CaptureResult screenshotEvents. */
            public screenshotEvents: karna.screen_capture.IRpcScreenshotEvent[];

            /**
             * Creates a new CaptureResult instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CaptureResult instance
             */
            public static create(properties?: karna.screen_capture.ICaptureResult): karna.screen_capture.CaptureResult;

            /**
             * Encodes the specified CaptureResult message. Does not implicitly {@link karna.screen_capture.CaptureResult.verify|verify} messages.
             * @param message CaptureResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.ICaptureResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CaptureResult message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureResult.verify|verify} messages.
             * @param message CaptureResult message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.ICaptureResult, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CaptureResult message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CaptureResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.CaptureResult;

            /**
             * Decodes a CaptureResult message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CaptureResult
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.CaptureResult;

            /**
             * Verifies a CaptureResult message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CaptureResult message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CaptureResult
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.CaptureResult;

            /**
             * Creates a plain object from a CaptureResult message. Also converts values to other types if specified.
             * @param message CaptureResult
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.CaptureResult, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CaptureResult to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CaptureResult
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a ScreenCaptureRPCResponse. */
        interface IScreenCaptureRPCResponse {

            /** ScreenCaptureRPCResponse captureResponse */
            captureResponse?: (karna.screen_capture.ICaptureResult|null);

            /** ScreenCaptureRPCResponse error */
            error?: (string|null);
        }

        /** Represents a ScreenCaptureRPCResponse. */
        class ScreenCaptureRPCResponse implements IScreenCaptureRPCResponse {

            /**
             * Constructs a new ScreenCaptureRPCResponse.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.IScreenCaptureRPCResponse);

            /** ScreenCaptureRPCResponse captureResponse. */
            public captureResponse?: (karna.screen_capture.ICaptureResult|null);

            /** ScreenCaptureRPCResponse error. */
            public error?: (string|null);

            /** ScreenCaptureRPCResponse type. */
            public type?: ("captureResponse"|"error");

            /**
             * Creates a new ScreenCaptureRPCResponse instance using the specified properties.
             * @param [properties] Properties to set
             * @returns ScreenCaptureRPCResponse instance
             */
            public static create(properties?: karna.screen_capture.IScreenCaptureRPCResponse): karna.screen_capture.ScreenCaptureRPCResponse;

            /**
             * Encodes the specified ScreenCaptureRPCResponse message. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCResponse.verify|verify} messages.
             * @param message ScreenCaptureRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.IScreenCaptureRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified ScreenCaptureRPCResponse message, length delimited. Does not implicitly {@link karna.screen_capture.ScreenCaptureRPCResponse.verify|verify} messages.
             * @param message ScreenCaptureRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.IScreenCaptureRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a ScreenCaptureRPCResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns ScreenCaptureRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.ScreenCaptureRPCResponse;

            /**
             * Decodes a ScreenCaptureRPCResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns ScreenCaptureRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.ScreenCaptureRPCResponse;

            /**
             * Verifies a ScreenCaptureRPCResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a ScreenCaptureRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns ScreenCaptureRPCResponse
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.ScreenCaptureRPCResponse;

            /**
             * Creates a plain object from a ScreenCaptureRPCResponse message. Also converts values to other types if specified.
             * @param message ScreenCaptureRPCResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.ScreenCaptureRPCResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this ScreenCaptureRPCResponse to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for ScreenCaptureRPCResponse
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }
    }
}
