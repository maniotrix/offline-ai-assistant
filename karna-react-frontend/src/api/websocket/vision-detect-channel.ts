import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel } from './base-channel';
import useVisionDetectStore from '../../stores/visionDetectStore';

export class VisionDetectChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.VISION_DETECT);
    }

    protected handleMessage(event: MessageEvent): void {
        console.log('VisionDetectChannel received message:', event);
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                console.error('Unexpected message type:', typeof event.data);
                throw new Error('Expected binary message');
            }

            const response = karna.vision.VisionDetectRPCResponse.decode(new Uint8Array(event.data));
            console.log('Decoded vision detect response:', response);
            
            if (response.error) {
                this.updateErrorState(new Error(response.error));
                return;
            }

            if (response.response) {
                if (response.response === 'results' && response.results) {
                    console.log('Updating vision detect results:', response.results);
                    useVisionDetectStore.getState().setResults(response.results);
                }
                
                if (response.response === 'status' && response.status) {
                    console.log('Updating vision detect status:', response.status);
                    useVisionDetectStore.getState().setStatus(response.status);
                    useVisionDetectStore.getState().setProcessing(response.status.isProcessing ?? false);
                }
            }
        } catch (error) {
            console.error('Failed to parse vision detect message:', error);
            this.updateErrorState(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async getResults(
        projectUuid: string, 
        commandUuid: string, 
        screenshotEvents?: karna.screen_capture.IRpcScreenshotEvent[]
    ): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Getting vision detect results:', { projectUuid, commandUuid, screenshotEvents });
        const request = karna.vision.VisionDetectRPCRequest.create({
            getResultsRequest: {
                projectUuid,
                commandUuid,
                screenshotEvents: screenshotEvents || []
            }
        });

        const buffer = karna.vision.VisionDetectRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Get results request sent');
    }

    async updateResults(results: karna.vision.IVisionDetectResultsList): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Updating vision detect results:', results);
        const request = karna.vision.VisionDetectRPCRequest.create({
            updateResultsRequest: {
                results
            }
        });

        const buffer = karna.vision.VisionDetectRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Update results request sent');
    }

    protected handleOpen(): void {
        super.handleOpen();
        console.log('VisionDetectChannel connected');
    }

    protected updateConnectionState(connected: boolean): void {
        useVisionDetectStore.getState().setConnected(connected);
    }

    protected updateErrorState(error: Error): void {
        useVisionDetectStore.getState().setError(error);
    }
} 