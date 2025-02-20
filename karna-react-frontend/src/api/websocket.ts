import io from 'socket.io-client';

interface Status {
    vision: string;
    language: string;
    command: string;
}

interface RPCRequest {
    method: 'execute_command' | 'get_status';
    params: {
        command?: string;
        [key: string]: any;
    };
}

interface RPCResponse {
    type: 'command_response' | 'status_update' | 'error';
    data: Status | string | any;
}

interface SocketError {
    message?: string;
    code?: string;
}

class WebSocketService {
    private socket: SocketIOClient.Socket | null = null;
    private messageHandlers: Map<string, (data: any) => void> = new Map();
    private rpcCallbacks: Map<string, (response: RPCResponse) => void> = new Map();

    connect(): void {
        this.socket = io('ws://localhost:8000/ws', {
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 20000,
            transports: ['websocket']
        });
        
        this.socket.on('connect', () => {
            console.log('WebSocket Connected');
            this.requestStatus().catch(console.error);
        });

        this.socket.on('rpc_response', (response: RPCResponse) => {
            const handler = this.messageHandlers.get(response.type);
            if (handler) {
                handler(response.data);
            }
        });

        this.socket.on('error', (error: SocketError) => {
            console.error('WebSocket error:', error);
            this.messageHandlers.forEach(handler => 
                handler({ error: error.message || 'Unknown error occurred' })
            );
        });

        this.socket.on('disconnect', () => {
            console.log('WebSocket disconnected, attempting to reconnect...');
        });
    }

    async sendCommand(command: string): Promise<any> {
        if (!this.socket?.connected) {
            throw new Error('WebSocket is not connected');
        }
        
        return new Promise((resolve, reject) => {
            this.socket!.emit('rpc', {
                method: 'execute_command',
                params: { command }
            } as RPCRequest, (response: RPCResponse) => {
                if (response.type === 'error') {
                    reject(new Error(response.data));
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    async requestStatus(): Promise<void> {
        if (!this.socket?.connected) {
            throw new Error('WebSocket is not connected');
        }

        return new Promise((resolve, reject) => {
            this.socket!.emit('rpc', {
                method: 'get_status',
                params: {}
            } as RPCRequest, (response: RPCResponse) => {
                if (response.type === 'error') {
                    reject(new Error(response.data));
                } else {
                    const handler = this.messageHandlers.get('status_update');
                    if (handler) {
                        handler(response.data as Status);
                    }
                    resolve();
                }
            });
        });
    }

    onStatusUpdate(handler: (status: Status) => void): void {
        this.messageHandlers.set('status_update', handler);
    }

    onCommandResponse(handler: (response: any) => void): void {
        this.messageHandlers.set('command_response', handler);
    }

    disconnect(): void {
        this.socket?.disconnect();
    }
}

export const websocketService = new WebSocketService();