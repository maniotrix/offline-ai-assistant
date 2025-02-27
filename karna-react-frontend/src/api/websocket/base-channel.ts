import { WS } from '../constants';

export type MessageHandler<T> = (data: T) => void;
export type ErrorHandler = (error: Error) => void;

export abstract class BaseWebSocketChannel {
    protected socket: WebSocket | null = null;
    protected messageHandlers: Map<string, Set<MessageHandler<any>>> = new Map();
    protected errorHandlers: Set<ErrorHandler> = new Set();
    protected reconnectAttempts = 0;
    protected maxReconnectAttempts = 5;
    protected reconnectDelay = 1000;
    protected isConnecting = false;
    protected pendingRequests: Map<string, { resolve: (value: any) => void, reject: (error: Error) => void }> = new Map();

    constructor(protected readonly endpoint: string) {}

    protected abstract handleMessage(event: MessageEvent): void;

    connect(): void {
        if (this.isConnecting || this.socket?.readyState === WebSocket.OPEN) {
            return;
        }

        this.disconnect();
        this.isConnecting = true;

        const baseUrl = WS.getBaseUrl();
        const wsUrl = `${baseUrl}${this.endpoint}`;
        console.log(`Connecting to WebSocket at ${wsUrl}`);
        
        this.socket = new WebSocket(wsUrl);
        this.socket.binaryType = 'arraybuffer';
        
        this.socket.onopen = (event) => {
            console.log('WebSocket.onopen called:', event);
            this.handleOpen();
        };
        this.socket.onmessage = (event) => {
            console.log('WebSocket.onmessage called:', event);
            this.handleMessage(event);
        };
        this.socket.onerror = (event) => {
            console.log('WebSocket.onerror called:', event);
            this.handleError(event);
        };
        this.socket.onclose = (event) => {
            console.log('WebSocket.onclose called:', event);
            this.handleClose();
        };
    }

    disconnect(): void {
        if (this.socket) {
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
        this.clearHandlers();
    }

    protected clearHandlers(): void {
        this.messageHandlers.clear();
        this.errorHandlers.clear();
        this.pendingRequests.clear();
    }

    protected handleOpen(): void {
        console.log('WebSocket Connected');
        this.reconnectAttempts = 0;
        this.isConnecting = false;
    }

    protected handleError(event: Event): void {
        console.error('WebSocket error:', event);
        this.isConnecting = false;
        this.notifyError(new Error('WebSocket error occurred'));
    }

    protected handleClose(): void {
        console.log('WebSocket disconnected');
        this.isConnecting = false;
        
        this.pendingRequests.forEach(({ reject }) => {
            reject(new Error('WebSocket disconnected'));
        });
        this.pendingRequests.clear();

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                this.reconnectAttempts++;
                console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
                this.connect();
            }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
        }
    }

    protected notifyHandlers<T>(type: string, data: T): void {
        console.log(`Notifying handlers for type ${type}:`, this.messageHandlers.get(type)?.size || 0, 'handlers');
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.forEach(handler => {
                console.log('Calling handler with data:', data);
                handler(data);
            });
        }
    }

    protected notifyError(error: Error): void {
        console.error('Notifying error handlers:', error);
        this.errorHandlers.forEach(handler => handler(error));
        this.pendingRequests.forEach(({ reject }) => reject(error));
        this.pendingRequests.clear();
    }

    protected addHandler<T>(type: string, handler: MessageHandler<T>): void {
        let handlers = this.messageHandlers.get(type);
        if (!handlers) {
            handlers = new Set();
            this.messageHandlers.set(type, handlers);
        }
        handlers.add(handler);
        console.log(`Added handler for type ${type}, now have ${handlers.size} handlers`);
    }

    protected removeHandler<T>(type: string, handler: MessageHandler<T>): void {
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.delete(handler);
            if (handlers.size === 0) {
                this.messageHandlers.delete(type);
            }
            console.log(`Removed handler for type ${type}, now have ${handlers.size} handlers`);
        }
    }

    onError(handler: ErrorHandler): () => void {
        this.errorHandlers.add(handler);
        return () => this.errorHandlers.delete(handler);
    }
}