import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel } from './base-channel';
import useCommandStore from '../../stores/commandStore';

export class CommandChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.COMMAND);
    }

    protected handleMessage(event: MessageEvent): void {
        console.log('CommandChannel received message:', event);
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                console.error('Unexpected message type:', typeof event.data);
                throw new Error('Expected binary message');
            }

            const response = karna.command.CommandRPCResponse.decode(new Uint8Array(event.data));
            console.log('Decoded command response:', response);
            
            if (response.error) {
                this.updateErrorState(new Error(response.error));
                return;
            }
            if (response.commandResponse) {
                console.log('Updating command state with:', response.commandResponse);
                useCommandStore.getState().setCommandResponse(response.commandResponse);
                
                // Resolve any pending requests
                this.pendingRequests.forEach(({ resolve }, requestId) => {
                    resolve(response.commandResponse);
                    this.pendingRequests.delete(requestId);
                    
                    // Update the pending commands in the store
                    useCommandStore.getState().removePendingCommand(requestId);
                });
            } else {
                console.log('No command response in response:', response);
            }
        } catch (error) {
            console.error('Failed to parse command message:', error);
            this.updateErrorState(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async sendCommand(command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }
        
        console.log('Sending command:', { command, domain });
        const request = karna.command.CommandRPCRequest.create({
            executeCommand: {
                command,
                domain
            }
        });
        
        const buffer = karna.command.CommandRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        console.log('Command request sent');
        
        return new Promise<karna.command.ICommandResult>((resolve, reject) => {
            const requestId = Math.random().toString(36).substring(7);
            this.pendingRequests.set(requestId, { resolve, reject });
            
            // Update the pending commands in the store
            useCommandStore.getState().addPendingCommand(requestId);

            // Set a timeout to avoid hanging indefinitely
            setTimeout(() => {
                if (this.pendingRequests.has(requestId)) {
                    this.pendingRequests.delete(requestId);
                    useCommandStore.getState().removePendingCommand(requestId);
                    reject(new Error('Command timed out'));
                }
            }, 30000);
        });
    }

    protected handleOpen(): void {
        super.handleOpen();
        console.log('CommandChannel connected');
    }

    protected updateConnectionState(connected: boolean): void {
        useCommandStore.getState().setConnected(connected);
    }

    protected updateErrorState(error: Error): void {
        useCommandStore.getState().setError(error);
    }
}