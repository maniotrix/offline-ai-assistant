import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel, MessageHandler } from './base-channel';

export class ScreenCaptureChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.SCREEN_CAPTURE);
    }

    protected handleMessage(event: MessageEvent): void {
        console.log('ScreenCaptureChannel received message:', event);
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                console.error('Unexpected message type:', typeof event.data);
                throw new Error('Expected binary message');
            }

            const response = karna.screen_capture.ScreenCaptureRPCResponse.decode(new Uint8Array(event.data));
            console.log('Decoded screen capture response:', response);
            
            if (response.error) {
                this.notifyError(new Error(response.error));
                return;
            }
            if (response.captureResponse) {
                console.log('Notifying handlers with capture response:', response.captureResponse);
                this.notifyHandlers('captureResponse', response.captureResponse);
            } else {
                console.log('No capture response in response:', response);
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

        console.log('Starting screen capture:', { projectUuid, commandUuid });
        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            startCapture: {
                projectUuid,
                commandUuid
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Start capture request sent');
    }

    async stopCapture(projectUuid: string, commandUuid: string): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Stopping screen capture:', { projectUuid, commandUuid });
        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            stopCapture: {
                projectUuid,
                commandUuid
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Stop capture request sent');
    }

    onCaptureResponse(handler: MessageHandler<karna.screen_capture.ICaptureResult>): () => void {
        console.log('Adding capture response handler');
        this.addHandler('captureResponse', handler);
        return () => {
            console.log('Removing capture response handler');
            this.removeHandler('captureResponse', handler);
        };
    }

    protected handleOpen(): void {
        super.handleOpen();
        console.log('ScreenCaptureChannel connected');
    }
}