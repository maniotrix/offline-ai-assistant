import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel, MessageHandler } from './base-channel';

export class StatusChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.STATUS);
    }

    protected handleMessage(event: MessageEvent): void {
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                throw new Error('Expected binary message');
            }

            const response = karna.status.StatusRPCResponse.decode(new Uint8Array(event.data));
            if (response.error) {
                this.notifyError(new Error(response.error));
                return;
            }
            if (response.statusUpdate) {
                this.notifyHandlers('statusUpdate', response.statusUpdate);
            }
        } catch (error) {
            console.error('Failed to parse status message:', error);
            this.notifyError(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async requestStatus(): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        const request = karna.status.StatusRPCRequest.create({
            getStatus: {}
        });
        
        const buffer = karna.status.StatusRPCRequest.encode(request).finish();
        this.socket.send(buffer);
    }

    onStatusUpdate(handler: MessageHandler<karna.status.IStatusResult>): () => void {
        this.addHandler('statusUpdate', handler);
        return () => this.removeHandler('statusUpdate', handler);
    }

    protected handleOpen(): void {
        super.handleOpen();
        // Request initial status when connection is established
        this.requestStatus().catch(console.error);
    }
}