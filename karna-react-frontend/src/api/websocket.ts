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
    private socket: WebSocket | null = null;
    private messageHandlers: Map<string, (data: any) => void> = new Map();
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000;

    connect(): void {
        this.socket = new WebSocket('ws://localhost:8000/ws');
        
        this.socket.onopen = () => {
            console.log('WebSocket Connected');
            this.reconnectAttempts = 0;
            this.requestStatus().catch(console.error);
        };

        this.socket.onmessage = (event) => {
            try {
                const response: RPCResponse = JSON.parse(event.data);
                const handler = this.messageHandlers.get(response.type);
                if (handler) {
                    handler(response.data);
                }
            } catch (error) {
                console.error('Failed to parse WebSocket message:', error);
            }
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.messageHandlers.forEach(handler => 
                handler({ error: 'WebSocket error occurred' })
            );
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                setTimeout(() => {
                    this.reconnectAttempts++;
                    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
                    this.connect();
                }, this.reconnectDelay);
            }
        };
    }

    async sendCommand(command: string): Promise<any> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }
        
        const request: RPCRequest = {
            method: 'execute_command',
            params: { command }
        };
        
        this.socket.send(JSON.stringify(request));
        
        return new Promise((resolve, reject) => {
            const handler = (response: any) => {
                if (response.error) {
                    reject(new Error(response.error));
                } else {
                    resolve(response);
                }
            };
            this.messageHandlers.set('command_response', handler);
        });
    }

    async requestStatus(): Promise<void> {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket is not connected');
        }

        const request: RPCRequest = {
            method: 'get_status',
            params: {}
        };
        
        this.socket.send(JSON.stringify(request));
    }

    onStatusUpdate(handler: (status: Status) => void): void {
        this.messageHandlers.set('status_update', handler);
    }

    onCommandResponse(handler: (response: any) => void): void {
        this.messageHandlers.set('command_response', handler);
    }

    disconnect(): void {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}

export const websocketService = new WebSocketService();