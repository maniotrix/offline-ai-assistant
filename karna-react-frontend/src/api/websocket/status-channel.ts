import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel } from './base-channel';
import useStatusStore from '../../stores/statusStore';

export class StatusChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.STATUS);
    }

    protected handleMessage(event: MessageEvent): void {
        console.log('StatusChannel received message:', event);
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                console.error('Unexpected message type:', typeof event.data);
                throw new Error('Expected binary message');
            }

            const response = karna.status.StatusRPCResponse.decode(new Uint8Array(event.data));
            console.log('Decoded status response:', response);
            
            if (response.error) {
                this.updateErrorState(new Error(response.error));
                return;
            }
            if (response.statusUpdate) {
                console.log('Updating status state with:', response.statusUpdate);
                useStatusStore.getState().setStatus(response.statusUpdate);
            } else {
                console.log('No status update in response:', response);
            }
        } catch (error) {
            console.error('Failed to parse status message:', error);
            this.updateErrorState(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async requestStatus(): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        console.log('Requesting status update...');
        const request = karna.status.StatusRPCRequest.create({
            getStatus: {}
        });
        
        const buffer = karna.status.StatusRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Status request sent');
    }

    protected handleOpen(): void {
        super.handleOpen();
        // Request initial status when connection is established
        console.log('StatusChannel connected, requesting initial status');
        this.requestStatus().catch(error => {
            console.error('Failed to request initial status:', error);
            this.updateErrorState(error);
        });
    }

    protected updateConnectionState(connected: boolean): void {
        useStatusStore.getState().setConnected(connected);
    }

    protected updateErrorState(error: Error): void {
        useStatusStore.getState().setError(error);
    }
}