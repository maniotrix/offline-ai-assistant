import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel, MessageHandler } from './base-channel';

export class ScreenCaptureChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.SCREEN_CAPTURE);
    }

    protected handleMessage(event: MessageEvent): void {
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                throw new Error('Expected binary message');
            }

            const response = karna.screen_capture.ScreenCaptureRPCResponse.decode(new Uint8Array(event.data));
            if (response.error) {
                this.notifyError(new Error(response.error));
                return;
            }
            if (response.captureResponse) {
                this.notifyHandlers('captureResponse', response.captureResponse);
            }
        } catch (error) {
            console.error('Failed to parse screen capture message:', error);
            this.notifyError(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async startCapture(projectUuid: string, commandUuid: string): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            startCapture: {
                projectUuid,
                commandUuid
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
    }

    async stopCapture(projectUuid: string, commandUuid: string): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            stopCapture: {
                projectUuid,
                commandUuid
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
    }

    onCaptureResponse(handler: MessageHandler<karna.screen_capture.ICaptureResult>): () => void {
        this.addHandler('captureResponse', handler);
        return () => this.removeHandler('captureResponse', handler);
    }
}