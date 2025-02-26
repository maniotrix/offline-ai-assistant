import { karna } from '../generated/messages';
import { WS } from './constants';

type MessageHandler<T> = (data: T) => void;
type ErrorHandler = (error: Error) => void;

class WebSocketService {
    private socket: WebSocket | null = null;
    private messageHandlers: Map<string, Set<MessageHandler<any>>> = new Map();
    private errorHandlers: Set<ErrorHandler> = new Set();
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000;
    private pendingRequests: Map<string, { resolve: (value: any) => void, reject: (error: Error) => void }> = new Map();
    private isConnecting = false;

    connect(): void {
        if (this.isConnecting) {
            console.log('Connection attempt already in progress');
            return;
        }

        if (this.socket?.readyState === WebSocket.OPEN) {
            console.log('WebSocket already connected');
            return;
        }

        // Clean up existing socket if any
        this.disconnect();

        this.isConnecting = true;
        const baseUrl = WS.getBaseUrl();
        const wsUrl = `${baseUrl}${WS.COMMAND}`;
        this.socket = new WebSocket(wsUrl);
        this.socket.binaryType = 'arraybuffer';
        
        this.socket.onopen = () => {
            console.log('WebSocket Connected');
            this.reconnectAttempts = 0;
            this.isConnecting = false;
            this.requestStatus().catch(console.error);
        };

        this.socket.onmessage = (event) => {
            try {
                if (!(event.data instanceof ArrayBuffer)) {
                    throw new Error('Expected binary message');
                }
                const response = karna.RPCResponse.decode(new Uint8Array(event.data));
                
                if (response.error) {
                    this.notifyError(new Error(response.error));
                    return;
                }

                const type = response.type;
                if (!type) {
                    throw new Error('Missing response type');
                }

                const data = response[type];
                if (!data) {
                    throw new Error(`Missing data for type: ${type}`);
                }

                this.notifyHandlers(type, data);
            } catch (error) {
                console.error('Failed to parse WebSocket message:', error);
                this.notifyError(error instanceof Error ? error : new Error(String(error)));
            }
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.isConnecting = false;
            this.notifyError(new Error('WebSocket error occurred'));
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.isConnecting = false;
            
            // Reject all pending requests
            this.pendingRequests.forEach(({ reject }) => {
                reject(new Error('WebSocket disconnected'));
            });
            this.pendingRequests.clear();

            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                setTimeout(() => {
                    this.reconnectAttempts++;
                    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
                    this.connect();
                }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts)); // Exponential backoff
            }
        };
    }

    private notifyHandlers<T>(type: string, data: T): void {
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.forEach(handler => handler(data));
        }
    }

    private notifyError(error: Error): void {
        this.errorHandlers.forEach(handler => handler(error));
        // Also reject any pending requests
        this.pendingRequests.forEach(({ reject }) => reject(error));
        this.pendingRequests.clear();
    }

    async sendCommand(command: string, domain: string = 'default'): Promise<karna.ICommandResult> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }
        
        const request = karna.RPCRequest.create({
            executeCommand: {
                command,
                domain
            }
        });
        
        const buffer = karna.RPCRequest.encode(request).finish();
        this.socket.send(buffer);
        
        return new Promise<karna.ICommandResult>((resolve, reject) => {
            const requestId = Math.random().toString(36).substring(7);
            this.pendingRequests.set(requestId, { resolve, reject });

            const cleanup = () => {
                this.pendingRequests.delete(requestId);
                this.removeHandler('commandResponse', responseHandler);
                this.removeHandler('error', errorHandler);
            };

            const responseHandler = (response: karna.ICommandResult) => {
                cleanup();
                resolve(response);
            };

            const errorHandler = (error: Error) => {
                cleanup();
                reject(error);
            };
            
            this.addHandler('commandResponse', responseHandler);
            this.addHandler('error', errorHandler);

            // Timeout after 30 seconds
            setTimeout(() => {
                if (this.pendingRequests.has(requestId)) {
                    cleanup();
                    reject(new Error('Command timed out'));
                }
            }, 30000);
        });
    }

    async requestStatus(): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        const request = karna.RPCRequest.create({
            getStatus: {}
        });
        
        const buffer = karna.RPCRequest.encode(request).finish();
        this.socket.send(buffer);
    }

    private addHandler<T>(type: string, handler: MessageHandler<T>): void {
        let handlers = this.messageHandlers.get(type);
        if (!handlers) {
            handlers = new Set();
            this.messageHandlers.set(type, handlers);
        }
        handlers.add(handler);
    }

    private removeHandler<T>(type: string, handler: MessageHandler<T>): void {
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.delete(handler);
            if (handlers.size === 0) {
                this.messageHandlers.delete(type);
            }
        }
    }

    onStatusUpdate(handler: MessageHandler<karna.IStatus>): () => void {
        this.addHandler('statusUpdate', handler);
        return () => this.removeHandler('statusUpdate', handler);
    }

    onCommandResponse(handler: MessageHandler<karna.ICommandResult>): () => void {
        this.addHandler('commandResponse', handler);
        return () => this.removeHandler('commandResponse', handler);
    }

    onError(handler: ErrorHandler): () => void {
        this.errorHandlers.add(handler);
        return () => this.errorHandlers.delete(handler);
    }

    disconnect(): void {
        if (this.socket) {
            // Remove all event listeners before closing
            this.socket.onopen = null;
            this.socket.onmessage = null;
            this.socket.onerror = null;
            this.socket.onclose = null;
            
            if (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING) {
                this.socket.close();
            }
            this.socket = null;
        }
        
        this.isConnecting = false;
        // Clear all handlers and pending requests
        this.messageHandlers.clear();
        this.errorHandlers.clear();
        this.pendingRequests.clear();
    }
}

export const websocketService = new WebSocketService();