import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace karna. */
export namespace karna {

    /** Namespace vision. */
    namespace vision {

        /** Properties of a GetResultsRequest. */
        interface IGetResultsRequest {

            /** GetResultsRequest projectUuid */
            projectUuid?: (string|null);

            /** GetResultsRequest commandUuid */
            commandUuid?: (string|null);

            /** GetResultsRequest screenshotEvents */
            screenshotEvents?: (karna.screen_capture.IRpcScreenshotEvent[]|null);
        }

        /** Represents a GetResultsRequest. */
        class GetResultsRequest implements IGetResultsRequest {

            /**
             * Constructs a new GetResultsRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IGetResultsRequest);

            /** GetResultsRequest projectUuid. */
            public projectUuid: string;

            /** GetResultsRequest commandUuid. */
            public commandUuid: string;

            /** GetResultsRequest screenshotEvents. */
            public screenshotEvents: karna.screen_capture.IRpcScreenshotEvent[];

            /**
             * Creates a new GetResultsRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns GetResultsRequest instance
             */
            public static create(properties?: karna.vision.IGetResultsRequest): karna.vision.GetResultsRequest;

            /**
             * Encodes the specified GetResultsRequest message. Does not implicitly {@link karna.vision.GetResultsRequest.verify|verify} messages.
             * @param message GetResultsRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IGetResultsRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified GetResultsRequest message, length delimited. Does not implicitly {@link karna.vision.GetResultsRequest.verify|verify} messages.
             * @param message GetResultsRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IGetResultsRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a GetResultsRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns GetResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.GetResultsRequest;

            /**
             * Decodes a GetResultsRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns GetResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.GetResultsRequest;

            /**
             * Verifies a GetResultsRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a GetResultsRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns GetResultsRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.GetResultsRequest;

            /**
             * Creates a plain object from a GetResultsRequest message. Also converts values to other types if specified.
             * @param message GetResultsRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.GetResultsRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this GetResultsRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for GetResultsRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of an UpdateResultsRequest. */
        interface IUpdateResultsRequest {

            /** UpdateResultsRequest results */
            results?: (karna.vision.IVisionDetectResultsList|null);
        }

        /** Represents an UpdateResultsRequest. */
        class UpdateResultsRequest implements IUpdateResultsRequest {

            /**
             * Constructs a new UpdateResultsRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IUpdateResultsRequest);

            /** UpdateResultsRequest results. */
            public results?: (karna.vision.IVisionDetectResultsList|null);

            /**
             * Creates a new UpdateResultsRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns UpdateResultsRequest instance
             */
            public static create(properties?: karna.vision.IUpdateResultsRequest): karna.vision.UpdateResultsRequest;

            /**
             * Encodes the specified UpdateResultsRequest message. Does not implicitly {@link karna.vision.UpdateResultsRequest.verify|verify} messages.
             * @param message UpdateResultsRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IUpdateResultsRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified UpdateResultsRequest message, length delimited. Does not implicitly {@link karna.vision.UpdateResultsRequest.verify|verify} messages.
             * @param message UpdateResultsRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IUpdateResultsRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes an UpdateResultsRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns UpdateResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.UpdateResultsRequest;

            /**
             * Decodes an UpdateResultsRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns UpdateResultsRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.UpdateResultsRequest;

            /**
             * Verifies an UpdateResultsRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates an UpdateResultsRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns UpdateResultsRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.UpdateResultsRequest;

            /**
             * Creates a plain object from an UpdateResultsRequest message. Also converts values to other types if specified.
             * @param message UpdateResultsRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.UpdateResultsRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this UpdateResultsRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for UpdateResultsRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a BoundingBox. */
        interface IBoundingBox {

            /** BoundingBox id */
            id?: (string|null);

            /** BoundingBox x */
            x?: (number|null);

            /** BoundingBox y */
            y?: (number|null);

            /** BoundingBox width */
            width?: (number|null);

            /** BoundingBox height */
            height?: (number|null);

            /** BoundingBox className */
            className?: (string|null);

            /** BoundingBox confidence */
            confidence?: (number|null);
        }

        /** Represents a BoundingBox. */
        class BoundingBox implements IBoundingBox {

            /**
             * Constructs a new BoundingBox.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IBoundingBox);

            /** BoundingBox id. */
            public id: string;

            /** BoundingBox x. */
            public x: number;

            /** BoundingBox y. */
            public y: number;

            /** BoundingBox width. */
            public width: number;

            /** BoundingBox height. */
            public height: number;

            /** BoundingBox className. */
            public className: string;

            /** BoundingBox confidence. */
            public confidence: number;

            /**
             * Creates a new BoundingBox instance using the specified properties.
             * @param [properties] Properties to set
             * @returns BoundingBox instance
             */
            public static create(properties?: karna.vision.IBoundingBox): karna.vision.BoundingBox;

            /**
             * Encodes the specified BoundingBox message. Does not implicitly {@link karna.vision.BoundingBox.verify|verify} messages.
             * @param message BoundingBox message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IBoundingBox, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified BoundingBox message, length delimited. Does not implicitly {@link karna.vision.BoundingBox.verify|verify} messages.
             * @param message BoundingBox message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IBoundingBox, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a BoundingBox message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns BoundingBox
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.BoundingBox;

            /**
             * Decodes a BoundingBox message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns BoundingBox
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.BoundingBox;

            /**
             * Verifies a BoundingBox message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a BoundingBox message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns BoundingBox
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.BoundingBox;

            /**
             * Creates a plain object from a BoundingBox message. Also converts values to other types if specified.
             * @param message BoundingBox
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.BoundingBox, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this BoundingBox to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for BoundingBox
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a VisionDetectResultModel. */
        interface IVisionDetectResultModel {

            /** VisionDetectResultModel eventId */
            eventId?: (string|null);

            /** VisionDetectResultModel projectUuid */
            projectUuid?: (string|null);

            /** VisionDetectResultModel commandUuid */
            commandUuid?: (string|null);

            /** VisionDetectResultModel timestamp */
            timestamp?: (string|null);

            /** VisionDetectResultModel description */
            description?: (string|null);

            /** VisionDetectResultModel originalImagePath */
            originalImagePath?: (string|null);

            /** VisionDetectResultModel originalWidth */
            originalWidth?: (number|null);

            /** VisionDetectResultModel originalHeight */
            originalHeight?: (number|null);

            /** VisionDetectResultModel isCropped */
            isCropped?: (boolean|null);

            /** VisionDetectResultModel mergedUiIconBboxes */
            mergedUiIconBboxes?: (karna.vision.IBoundingBox[]|null);

            /** VisionDetectResultModel croppedImage */
            croppedImage?: (Uint8Array|null);

            /** VisionDetectResultModel croppedWidth */
            croppedWidth?: (number|null);

            /** VisionDetectResultModel croppedHeight */
            croppedHeight?: (number|null);
        }

        /** Represents a VisionDetectResultModel. */
        class VisionDetectResultModel implements IVisionDetectResultModel {

            /**
             * Constructs a new VisionDetectResultModel.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IVisionDetectResultModel);

            /** VisionDetectResultModel eventId. */
            public eventId: string;

            /** VisionDetectResultModel projectUuid. */
            public projectUuid: string;

            /** VisionDetectResultModel commandUuid. */
            public commandUuid: string;

            /** VisionDetectResultModel timestamp. */
            public timestamp: string;

            /** VisionDetectResultModel description. */
            public description: string;

            /** VisionDetectResultModel originalImagePath. */
            public originalImagePath: string;

            /** VisionDetectResultModel originalWidth. */
            public originalWidth: number;

            /** VisionDetectResultModel originalHeight. */
            public originalHeight: number;

            /** VisionDetectResultModel isCropped. */
            public isCropped: boolean;

            /** VisionDetectResultModel mergedUiIconBboxes. */
            public mergedUiIconBboxes: karna.vision.IBoundingBox[];

            /** VisionDetectResultModel croppedImage. */
            public croppedImage: Uint8Array;

            /** VisionDetectResultModel croppedWidth. */
            public croppedWidth: number;

            /** VisionDetectResultModel croppedHeight. */
            public croppedHeight: number;

            /**
             * Creates a new VisionDetectResultModel instance using the specified properties.
             * @param [properties] Properties to set
             * @returns VisionDetectResultModel instance
             */
            public static create(properties?: karna.vision.IVisionDetectResultModel): karna.vision.VisionDetectResultModel;

            /**
             * Encodes the specified VisionDetectResultModel message. Does not implicitly {@link karna.vision.VisionDetectResultModel.verify|verify} messages.
             * @param message VisionDetectResultModel message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IVisionDetectResultModel, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified VisionDetectResultModel message, length delimited. Does not implicitly {@link karna.vision.VisionDetectResultModel.verify|verify} messages.
             * @param message VisionDetectResultModel message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IVisionDetectResultModel, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a VisionDetectResultModel message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns VisionDetectResultModel
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.VisionDetectResultModel;

            /**
             * Decodes a VisionDetectResultModel message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns VisionDetectResultModel
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.VisionDetectResultModel;

            /**
             * Verifies a VisionDetectResultModel message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a VisionDetectResultModel message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns VisionDetectResultModel
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.VisionDetectResultModel;

            /**
             * Creates a plain object from a VisionDetectResultModel message. Also converts values to other types if specified.
             * @param message VisionDetectResultModel
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.VisionDetectResultModel, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this VisionDetectResultModel to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for VisionDetectResultModel
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a VisionDetectResultsList. */
        interface IVisionDetectResultsList {

            /** VisionDetectResultsList projectUuid */
            projectUuid?: (string|null);

            /** VisionDetectResultsList commandUuid */
            commandUuid?: (string|null);

            /** VisionDetectResultsList results */
            results?: (karna.vision.IVisionDetectResultModel[]|null);
        }

        /** Represents a VisionDetectResultsList. */
        class VisionDetectResultsList implements IVisionDetectResultsList {

            /**
             * Constructs a new VisionDetectResultsList.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IVisionDetectResultsList);

            /** VisionDetectResultsList projectUuid. */
            public projectUuid: string;

            /** VisionDetectResultsList commandUuid. */
            public commandUuid: string;

            /** VisionDetectResultsList results. */
            public results: karna.vision.IVisionDetectResultModel[];

            /**
             * Creates a new VisionDetectResultsList instance using the specified properties.
             * @param [properties] Properties to set
             * @returns VisionDetectResultsList instance
             */
            public static create(properties?: karna.vision.IVisionDetectResultsList): karna.vision.VisionDetectResultsList;

            /**
             * Encodes the specified VisionDetectResultsList message. Does not implicitly {@link karna.vision.VisionDetectResultsList.verify|verify} messages.
             * @param message VisionDetectResultsList message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IVisionDetectResultsList, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified VisionDetectResultsList message, length delimited. Does not implicitly {@link karna.vision.VisionDetectResultsList.verify|verify} messages.
             * @param message VisionDetectResultsList message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IVisionDetectResultsList, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a VisionDetectResultsList message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns VisionDetectResultsList
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.VisionDetectResultsList;

            /**
             * Decodes a VisionDetectResultsList message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns VisionDetectResultsList
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.VisionDetectResultsList;

            /**
             * Verifies a VisionDetectResultsList message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a VisionDetectResultsList message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns VisionDetectResultsList
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.VisionDetectResultsList;

            /**
             * Creates a plain object from a VisionDetectResultsList message. Also converts values to other types if specified.
             * @param message VisionDetectResultsList
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.VisionDetectResultsList, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this VisionDetectResultsList to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for VisionDetectResultsList
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a VisionDetectStatus. */
        interface IVisionDetectStatus {

            /** VisionDetectStatus status */
            status?: (string|null);

            /** VisionDetectStatus screenshotEventsCount */
            screenshotEventsCount?: (number|null);

            /** VisionDetectStatus hasResults */
            hasResults?: (boolean|null);

            /** VisionDetectStatus resultsCount */
            resultsCount?: (number|null);

            /** VisionDetectStatus isProcessing */
            isProcessing?: (boolean|null);

            /** VisionDetectStatus lastProcessed */
            lastProcessed?: (string|null);

            /** VisionDetectStatus lastError */
            lastError?: (string|null);
        }

        /** Represents a VisionDetectStatus. */
        class VisionDetectStatus implements IVisionDetectStatus {

            /**
             * Constructs a new VisionDetectStatus.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IVisionDetectStatus);

            /** VisionDetectStatus status. */
            public status: string;

            /** VisionDetectStatus screenshotEventsCount. */
            public screenshotEventsCount: number;

            /** VisionDetectStatus hasResults. */
            public hasResults: boolean;

            /** VisionDetectStatus resultsCount. */
            public resultsCount: number;

            /** VisionDetectStatus isProcessing. */
            public isProcessing: boolean;

            /** VisionDetectStatus lastProcessed. */
            public lastProcessed: string;

            /** VisionDetectStatus lastError. */
            public lastError: string;

            /**
             * Creates a new VisionDetectStatus instance using the specified properties.
             * @param [properties] Properties to set
             * @returns VisionDetectStatus instance
             */
            public static create(properties?: karna.vision.IVisionDetectStatus): karna.vision.VisionDetectStatus;

            /**
             * Encodes the specified VisionDetectStatus message. Does not implicitly {@link karna.vision.VisionDetectStatus.verify|verify} messages.
             * @param message VisionDetectStatus message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IVisionDetectStatus, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified VisionDetectStatus message, length delimited. Does not implicitly {@link karna.vision.VisionDetectStatus.verify|verify} messages.
             * @param message VisionDetectStatus message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IVisionDetectStatus, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a VisionDetectStatus message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns VisionDetectStatus
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.VisionDetectStatus;

            /**
             * Decodes a VisionDetectStatus message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns VisionDetectStatus
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.VisionDetectStatus;

            /**
             * Verifies a VisionDetectStatus message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a VisionDetectStatus message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns VisionDetectStatus
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.VisionDetectStatus;

            /**
             * Creates a plain object from a VisionDetectStatus message. Also converts values to other types if specified.
             * @param message VisionDetectStatus
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.VisionDetectStatus, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this VisionDetectStatus to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for VisionDetectStatus
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a VisionDetectRPCRequest. */
        interface IVisionDetectRPCRequest {

            /** VisionDetectRPCRequest getResultsRequest */
            getResultsRequest?: (karna.vision.IGetResultsRequest|null);

            /** VisionDetectRPCRequest updateResultsRequest */
            updateResultsRequest?: (karna.vision.IUpdateResultsRequest|null);
        }

        /** Represents a VisionDetectRPCRequest. */
        class VisionDetectRPCRequest implements IVisionDetectRPCRequest {

            /**
             * Constructs a new VisionDetectRPCRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IVisionDetectRPCRequest);

            /** VisionDetectRPCRequest getResultsRequest. */
            public getResultsRequest?: (karna.vision.IGetResultsRequest|null);

            /** VisionDetectRPCRequest updateResultsRequest. */
            public updateResultsRequest?: (karna.vision.IUpdateResultsRequest|null);

            /** VisionDetectRPCRequest method. */
            public method?: ("getResultsRequest"|"updateResultsRequest");

            /**
             * Creates a new VisionDetectRPCRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns VisionDetectRPCRequest instance
             */
            public static create(properties?: karna.vision.IVisionDetectRPCRequest): karna.vision.VisionDetectRPCRequest;

            /**
             * Encodes the specified VisionDetectRPCRequest message. Does not implicitly {@link karna.vision.VisionDetectRPCRequest.verify|verify} messages.
             * @param message VisionDetectRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IVisionDetectRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified VisionDetectRPCRequest message, length delimited. Does not implicitly {@link karna.vision.VisionDetectRPCRequest.verify|verify} messages.
             * @param message VisionDetectRPCRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IVisionDetectRPCRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a VisionDetectRPCRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns VisionDetectRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.VisionDetectRPCRequest;

            /**
             * Decodes a VisionDetectRPCRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns VisionDetectRPCRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.VisionDetectRPCRequest;

            /**
             * Verifies a VisionDetectRPCRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a VisionDetectRPCRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns VisionDetectRPCRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.VisionDetectRPCRequest;

            /**
             * Creates a plain object from a VisionDetectRPCRequest message. Also converts values to other types if specified.
             * @param message VisionDetectRPCRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.VisionDetectRPCRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this VisionDetectRPCRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for VisionDetectRPCRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a VisionDetectRPCResponse. */
        interface IVisionDetectRPCResponse {

            /** VisionDetectRPCResponse results */
            results?: (karna.vision.IVisionDetectResultsList|null);

            /** VisionDetectRPCResponse status */
            status?: (karna.vision.IVisionDetectStatus|null);

            /** VisionDetectRPCResponse error */
            error?: (string|null);
        }

        /** Represents a VisionDetectRPCResponse. */
        class VisionDetectRPCResponse implements IVisionDetectRPCResponse {

            /**
             * Constructs a new VisionDetectRPCResponse.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.vision.IVisionDetectRPCResponse);

            /** VisionDetectRPCResponse results. */
            public results?: (karna.vision.IVisionDetectResultsList|null);

            /** VisionDetectRPCResponse status. */
            public status?: (karna.vision.IVisionDetectStatus|null);

            /** VisionDetectRPCResponse error. */
            public error: string;

            /** VisionDetectRPCResponse response. */
            public response?: ("results"|"status");

            /**
             * Creates a new VisionDetectRPCResponse instance using the specified properties.
             * @param [properties] Properties to set
             * @returns VisionDetectRPCResponse instance
             */
            public static create(properties?: karna.vision.IVisionDetectRPCResponse): karna.vision.VisionDetectRPCResponse;

            /**
             * Encodes the specified VisionDetectRPCResponse message. Does not implicitly {@link karna.vision.VisionDetectRPCResponse.verify|verify} messages.
             * @param message VisionDetectRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.vision.IVisionDetectRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified VisionDetectRPCResponse message, length delimited. Does not implicitly {@link karna.vision.VisionDetectRPCResponse.verify|verify} messages.
             * @param message VisionDetectRPCResponse message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.vision.IVisionDetectRPCResponse, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a VisionDetectRPCResponse message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns VisionDetectRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.vision.VisionDetectRPCResponse;

            /**
             * Decodes a VisionDetectRPCResponse message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns VisionDetectRPCResponse
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.vision.VisionDetectRPCResponse;

            /**
             * Verifies a VisionDetectRPCResponse message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a VisionDetectRPCResponse message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns VisionDetectRPCResponse
             */
            public static fromObject(object: { [k: string]: any }): karna.vision.VisionDetectRPCResponse;

            /**
             * Creates a plain object from a VisionDetectRPCResponse message. Also converts values to other types if specified.
             * @param message VisionDetectRPCResponse
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.vision.VisionDetectRPCResponse, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this VisionDetectRPCResponse to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for VisionDetectRPCResponse
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }
    }

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

        /** Properties of a CaptureCacheRequest. */
        interface ICaptureCacheRequest {

            /** CaptureCacheRequest projectUuid */
            projectUuid?: (string|null);

            /** CaptureCacheRequest commandUuid */
            commandUuid?: (string|null);
        }

        /** Represents a CaptureCacheRequest. */
        class CaptureCacheRequest implements ICaptureCacheRequest {

            /**
             * Constructs a new CaptureCacheRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.ICaptureCacheRequest);

            /** CaptureCacheRequest projectUuid. */
            public projectUuid: string;

            /** CaptureCacheRequest commandUuid. */
            public commandUuid: string;

            /**
             * Creates a new CaptureCacheRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CaptureCacheRequest instance
             */
            public static create(properties?: karna.screen_capture.ICaptureCacheRequest): karna.screen_capture.CaptureCacheRequest;

            /**
             * Encodes the specified CaptureCacheRequest message. Does not implicitly {@link karna.screen_capture.CaptureCacheRequest.verify|verify} messages.
             * @param message CaptureCacheRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.ICaptureCacheRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CaptureCacheRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureCacheRequest.verify|verify} messages.
             * @param message CaptureCacheRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.ICaptureCacheRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CaptureCacheRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CaptureCacheRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.CaptureCacheRequest;

            /**
             * Decodes a CaptureCacheRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CaptureCacheRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.CaptureCacheRequest;

            /**
             * Verifies a CaptureCacheRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CaptureCacheRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CaptureCacheRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.CaptureCacheRequest;

            /**
             * Creates a plain object from a CaptureCacheRequest message. Also converts values to other types if specified.
             * @param message CaptureCacheRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.CaptureCacheRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CaptureCacheRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CaptureCacheRequest
             * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
             * @returns The default type url
             */
            public static getTypeUrl(typeUrlPrefix?: string): string;
        }

        /** Properties of a CaptureUpdateRequest. */
        interface ICaptureUpdateRequest {

            /** CaptureUpdateRequest projectUuid */
            projectUuid?: (string|null);

            /** CaptureUpdateRequest commandUuid */
            commandUuid?: (string|null);

            /** CaptureUpdateRequest message */
            message?: (string|null);

            /** CaptureUpdateRequest screenshotEventIds */
            screenshotEventIds?: (string[]|null);
        }

        /** Represents a CaptureUpdateRequest. */
        class CaptureUpdateRequest implements ICaptureUpdateRequest {

            /**
             * Constructs a new CaptureUpdateRequest.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.ICaptureUpdateRequest);

            /** CaptureUpdateRequest projectUuid. */
            public projectUuid: string;

            /** CaptureUpdateRequest commandUuid. */
            public commandUuid: string;

            /** CaptureUpdateRequest message. */
            public message: string;

            /** CaptureUpdateRequest screenshotEventIds. */
            public screenshotEventIds: string[];

            /**
             * Creates a new CaptureUpdateRequest instance using the specified properties.
             * @param [properties] Properties to set
             * @returns CaptureUpdateRequest instance
             */
            public static create(properties?: karna.screen_capture.ICaptureUpdateRequest): karna.screen_capture.CaptureUpdateRequest;

            /**
             * Encodes the specified CaptureUpdateRequest message. Does not implicitly {@link karna.screen_capture.CaptureUpdateRequest.verify|verify} messages.
             * @param message CaptureUpdateRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encode(message: karna.screen_capture.ICaptureUpdateRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Encodes the specified CaptureUpdateRequest message, length delimited. Does not implicitly {@link karna.screen_capture.CaptureUpdateRequest.verify|verify} messages.
             * @param message CaptureUpdateRequest message or plain object to encode
             * @param [writer] Writer to encode to
             * @returns Writer
             */
            public static encodeDelimited(message: karna.screen_capture.ICaptureUpdateRequest, writer?: $protobuf.Writer): $protobuf.Writer;

            /**
             * Decodes a CaptureUpdateRequest message from the specified reader or buffer.
             * @param reader Reader or buffer to decode from
             * @param [length] Message length if known beforehand
             * @returns CaptureUpdateRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): karna.screen_capture.CaptureUpdateRequest;

            /**
             * Decodes a CaptureUpdateRequest message from the specified reader or buffer, length delimited.
             * @param reader Reader or buffer to decode from
             * @returns CaptureUpdateRequest
             * @throws {Error} If the payload is not a reader or valid buffer
             * @throws {$protobuf.util.ProtocolError} If required fields are missing
             */
            public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): karna.screen_capture.CaptureUpdateRequest;

            /**
             * Verifies a CaptureUpdateRequest message.
             * @param message Plain object to verify
             * @returns `null` if valid, otherwise the reason why it is not
             */
            public static verify(message: { [k: string]: any }): (string|null);

            /**
             * Creates a CaptureUpdateRequest message from a plain object. Also converts values to their respective internal types.
             * @param object Plain object
             * @returns CaptureUpdateRequest
             */
            public static fromObject(object: { [k: string]: any }): karna.screen_capture.CaptureUpdateRequest;

            /**
             * Creates a plain object from a CaptureUpdateRequest message. Also converts values to other types if specified.
             * @param message CaptureUpdateRequest
             * @param [options] Conversion options
             * @returns Plain object
             */
            public static toObject(message: karna.screen_capture.CaptureUpdateRequest, options?: $protobuf.IConversionOptions): { [k: string]: any };

            /**
             * Converts this CaptureUpdateRequest to JSON.
             * @returns JSON object
             */
            public toJSON(): { [k: string]: any };

            /**
             * Gets the default type url for CaptureUpdateRequest
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

            /** ScreenCaptureRPCRequest updateCapture */
            updateCapture?: (karna.screen_capture.ICaptureUpdateRequest|null);

            /** ScreenCaptureRPCRequest getCache */
            getCache?: (karna.screen_capture.ICaptureCacheRequest|null);
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

            /** ScreenCaptureRPCRequest updateCapture. */
            public updateCapture?: (karna.screen_capture.ICaptureUpdateRequest|null);

            /** ScreenCaptureRPCRequest getCache. */
            public getCache?: (karna.screen_capture.ICaptureCacheRequest|null);

            /** ScreenCaptureRPCRequest method. */
            public method?: ("startCapture"|"stopCapture"|"updateCapture"|"getCache");

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

            /** RpcScreenshotEvent eventId */
            eventId?: (string|null);

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

            /** RpcScreenshotEvent mouseEventToolTip */
            mouseEventToolTip?: (string|null);
        }

        /** Represents a RpcScreenshotEvent. */
        class RpcScreenshotEvent implements IRpcScreenshotEvent {

            /**
             * Constructs a new RpcScreenshotEvent.
             * @param [properties] Properties to set
             */
            constructor(properties?: karna.screen_capture.IRpcScreenshotEvent);

            /** RpcScreenshotEvent eventId. */
            public eventId: string;

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

            /** RpcScreenshotEvent mouseEventToolTip. */
            public mouseEventToolTip?: (string|null);

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
