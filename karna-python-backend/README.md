# Karna Python Backend - WebSocket Implementation

## Overview
The backend implements a WebSocket server using FastAPI's WebSocket support for real-time bidirectional communication with the frontend. The implementation is primarily handled by the `WebSocketManager` class.

## Architecture

### WebSocket Manager
Located in `api/websocket.py`, the WebSocketManager handles:
- Connection management
- Message broadcasting
- Command processing
- Status updates

### WebSocket Route
The WebSocket endpoint is defined in `api/routes.py` and is accessible at `/ws`.

## Features

### Connection Management
- Active connection tracking
- Proper connection acceptance and cleanup
- Automatic disconnection handling

### Message Handling
Supports two main RPC methods:
1. `execute_command`:
   - Processes user commands
   - Returns command execution results
   - Handles errors gracefully

2. `get_status`:
   - Returns current status of services:
     - Vision service status
     - Language service status
     - Command processor status

### Broadcasting
- Supports broadcasting messages to all connected clients
- Used for status updates and notifications

## Usage Example

```python
# Client-side connection
ws = await websocket.connect("ws://localhost:8000/ws")

# Execute command
await ws.send_json({
    "method": "execute_command",
    "params": {
        "command": "your_command_here"
    }
})

# Get status
await ws.send_json({
    "method": "get_status",
    "params": {}
})
```

## Error Handling
- All WebSocket operations are wrapped in try-except blocks
- Errors are properly formatted and sent back to clients
- Connection errors are handled gracefully

## Integration Points
- Integrates with Command Processor for command execution
- Connects with Vision and Language services for status monitoring
- Works alongside REST endpoints for hybrid communication

## Frontend Integration Guidelines

### Connection Setup
The frontend should use Socket.IO client to connect to the WebSocket server:

```typescript
import { io } from 'socket.io-client';

const socket = io('ws://localhost:8000/ws', {
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
    transports: ['websocket']
});

// Connection event handlers
socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
});

socket.on('error', (error) => {
    console.error('WebSocket error:', error);
});
```

### Message Structure
Messages sent to the server should follow this format:

```typescript
interface WebSocketMessage {
    method: 'execute_command' | 'get_status';
    params: {
        command?: string;
        [key: string]: any;
    };
}
```

### Handling Responses
Server responses follow this structure:

```typescript
interface WebSocketResponse {
    type: 'command_response' | 'status_update' | 'error';
    data: any;
}

// Example response handlers
socket.on('rpc_response', (response: WebSocketResponse) => {
    switch (response.type) {
        case 'command_response':
            handleCommandResponse(response.data);
            break;
        case 'status_update':
            handleStatusUpdate(response.data);
            break;
        case 'error':
            handleError(response.data);
            break;
    }
});
```

### Best Practices
1. Always implement reconnection logic
2. Handle connection errors gracefully
3. Implement proper cleanup on component unmount:
   ```typescript
   useEffect(() => {
       // Setup connection
       return () => {
           socket.disconnect();
       };
   }, []);
   ```
4. Use TypeScript interfaces for type safety
5. Implement proper error boundaries for WebSocket errors

### Example Component Integration

```typescript
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

function WebSocketComponent() {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [status, setStatus] = useState<any>(null);

    useEffect(() => {
        const newSocket = io('ws://localhost:8000/ws', {
            transports: ['websocket']
        });

        newSocket.on('connect', () => {
            console.log('Connected');
            // Request initial status
            newSocket.emit('rpc', {
                method: 'get_status',
                params: {}
            });
        });

        newSocket.on('rpc_response', (response) => {
            if (response.type === 'status_update') {
                setStatus(response.data);
            }
        });

        setSocket(newSocket);

        return () => {
            newSocket.disconnect();
        };
    }, []);

    const sendCommand = (command: string) => {
        if (socket) {
            socket.emit('rpc', {
                method: 'execute_command',
                params: { command }
            });
        }
    };

    return (
        <div>
            {/* Your component UI */}
        </div>
    );
}