class WebSocketService {
    private ws: WebSocket | null = null;
    private messageHandlers: Map<string, (data: any) => void> = new Map();

    connect() {
        this.ws = new WebSocket('ws://localhost:8000/ws');
        
        this.ws.onopen = () => {
            console.log('WebSocket Connected');
            this.requestStatus();
        };

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            const handler = this.messageHandlers.get(message.type);
            if (handler) {
                handler(message.data);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            // Attempt to reconnect after 5 seconds
            setTimeout(() => this.connect(), 5000);
        };
    }

    sendCommand(command: string) {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'command',
                command
            }));
        }
    }

    requestStatus() {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'status_request'
            }));
        }
    }

    onStatusUpdate(handler: (status: any) => void) {
        this.messageHandlers.set('status_update', handler);
    }

    onCommandResponse(handler: (response: any) => void) {
        this.messageHandlers.set('command_response', handler);
    }

    disconnect() {
        this.ws?.close();
    }
}

export const websocketService = new WebSocketService();