import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel } from './base-channel';
import useScreenCaptureStore from '../../stores/screenCaptureStore';

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
                this.updateErrorState(new Error(response.error));
                return;
            }
            if (response.captureResponse) {
                console.log('Updating screen capture state with:', response.captureResponse);
                useScreenCaptureStore.getState().setCaptureResult(response.captureResponse);
            } else {
                console.log('No capture response in response:', response);
            }
        } catch (error) {
            console.error('Failed to parse screen capture message:', error);
            this.updateErrorState(error instanceof Error ? error : new Error(String(error)));
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
        useScreenCaptureStore.getState().setCapturing(true);
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
        useScreenCaptureStore.getState().setCapturing(false);
    }

    async updateCapture(projectUuid: string, commandUuid: string, updatedEvents: any[]): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Updating screen capture:', { projectUuid, commandUuid, eventCount: updatedEvents.length });
        
        // Create screenshot event objects for the protobuf message
        const screenshotEvents = updatedEvents.map(event => {
            return {
                eventId: event.eventId,
                projectUuid: event.projectUuid,
                commandUuid: event.commandUuid,
                timestamp: typeof event.timestamp === 'string' ? event.timestamp : new Date(event.timestamp).toISOString(),
                description: event.description,
                screenshotPath: event.screenshotPath,
                annotationPath: event.annotationPath,
                mouseX: event.mouseX,
                mouseY: event.mouseY,
                mouseEventToolTip: event.mouse_event_tool_tip || event.mouseEventToolTip,
                keyChar: event.keyChar,
                keyCode: event.keyCode,
                isSpecialKey: event.isSpecialKey
            };
        });

        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            updateCapture: {
                projectUuid,
                commandUuid,
                message: 'Update screenshots',
                screenshotEvents: screenshotEvents
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Update capture request sent with updated events');
    }

    async getCache(projectUuid: string, commandUuid: string): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Getting screen capture cache:', { projectUuid, commandUuid });
        const request = karna.screen_capture.ScreenCaptureRPCRequest.create({
            getCache: {
                projectUuid,
                commandUuid
            }
        });

        const buffer = karna.screen_capture.ScreenCaptureRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Get cache request sent');
        // The response will be handled by the handleMessage method
    }

    protected handleOpen(): void {
        super.handleOpen();
        console.log('ScreenCaptureChannel connected');
    }

    protected updateConnectionState(connected: boolean): void {
        useScreenCaptureStore.getState().setConnectionState(connected ? 'connected' : 'disconnected');
    }

    protected updateErrorState(error: Error): void {
        if (error) {
            console.error('Screen capture channel error:', error);
        }
        // Set error state in a different way since we don't have setError anymore
        useScreenCaptureStore.getState().setConnectionState('disconnected');
    }
}