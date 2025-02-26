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
        this.socket = new WebSocket(wsUrl);
        this.socket.binaryType = 'arraybuffer';
        
        this.socket.onopen = this.handleOpen.bind(this);
        this.socket.onmessage = this.handleMessage.bind(this);
        this.socket.onerror = this.handleError.bind(this);
        this.socket.onclose = this.handleClose.bind(this);
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
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.forEach(handler => handler(data));
        }
    }

    protected notifyError(error: Error): void {
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
    }

    protected removeHandler<T>(type: string, handler: MessageHandler<T>): void {
        const handlers = this.messageHandlers.get(type);
        if (handlers) {
            handlers.delete(handler);
            if (handlers.size === 0) {
                this.messageHandlers.delete(type);
            }
        }
    }

    onError(handler: ErrorHandler): () => void {
        this.errorHandlers.add(handler);
        return () => this.errorHandlers.delete(handler);
    }
}