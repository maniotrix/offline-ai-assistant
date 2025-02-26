import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel, MessageHandler } from './base-channel';

export class CommandChannel extends BaseWebSocketChannel {
    constructor() {
        super(WS.COMMAND);
    }

    protected handleMessage(event: MessageEvent): void {
        try {
            if (!(event.data instanceof ArrayBuffer)) {
                throw new Error('Expected binary message');
            }

            const response = karna.command.CommandRPCResponse.decode(new Uint8Array(event.data));
            if (response.error) {
                this.notifyError(new Error(response.error));
                return;
            }
            if (response.commandResponse) {
                this.notifyHandlers('commandResponse', response.commandResponse);
            }
        } catch (error) {
            console.error('Failed to parse command message:', error);
            this.notifyError(error instanceof Error ? error : new Error(String(error)));
        }
    }

    async sendCommand(command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }
        
        const request = karna.command.CommandRPCRequest.create({
            executeCommand: {
                command,
                domain
            }
        });
        
        const buffer = karna.command.CommandRPCRequest.encode(request).finish();
        this.socket.send(buffer);
        
        return new Promise<karna.command.ICommandResult>((resolve, reject) => {
            const requestId = Math.random().toString(36).substring(7);
            this.pendingRequests.set(requestId, { resolve, reject });

            const cleanup = () => {
                this.pendingRequests.delete(requestId);
                this.removeHandler('commandResponse', responseHandler);
                this.removeHandler('error', errorHandler);
            };

            const responseHandler = (response: karna.command.ICommandResult) => {
                cleanup();
                resolve(response);
            };

            const errorHandler = (error: Error) => {
                cleanup();
                reject(error);
            };
            
            this.addHandler('commandResponse', responseHandler);
            this.addHandler('error', errorHandler);

            setTimeout(() => {
                if (this.pendingRequests.has(requestId)) {
                    cleanup();
                    reject(new Error('Command timed out'));
                }
            }, 30000);
        });
    }

    onCommandResponse(handler: MessageHandler<karna.command.ICommandResult>): () => void {
        this.addHandler('commandResponse', handler);
        return () => this.removeHandler('commandResponse', handler);
    }
}