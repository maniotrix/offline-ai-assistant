import { karna } from '../../generated/messages';
import { WS } from '../constants';
import { BaseWebSocketChannel, MessageHandler } from './base-channel';

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
                this.notifyError(new Error(response.error));
                return;
            }
            if (response.commandResponse) {
                console.log('Notifying handlers with command response:', response.commandResponse);
                this.notifyHandlers('commandResponse', response.commandResponse);
            } else {
                console.log('No command response in response:', response);
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
        console.log('Adding command response handler');
        this.addHandler('commandResponse', handler);
        return () => {
            console.log('Removing command response handler');
            this.removeHandler('commandResponse', handler);
        };
    }

    protected handleOpen(): void {
        super.handleOpen();
        console.log('CommandChannel connected');
    }
}