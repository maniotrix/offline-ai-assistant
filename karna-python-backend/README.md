# Karna Python Backend

## Overview
The Karna Python Backend is a real-time assistant that powers the offline AI assistant. It provides a robust WebSocket server implementation using FastAPI for bidirectional communication with the frontend, along with computer vision, natural language processing, and automation capabilities.

## Architecture

### Core Components

#### WebSocket System
Located in `api/websockets/`, the WebSocket system consists of:

- **WebSocketManager** - Main singleton that manages all WebSocket connections
- **Specialized Channel Handlers**:
  - `CommandWebSocketHandler` - Processes user commands
  - `StatusWebSocketHandler` - Provides system status updates
  - `ScreenCaptureWebSocketHandler` - Handles screen capture operations
  - `VisionDetectWebSocketHandler` - Manages vision detection messages

#### Services
The backend implements several key services in the `services/` directory:

- **Screen Capture Service** - Captures screen content for analysis
- **Vision Detect Service** - Detects UI elements and visual features
- **Task Execution Service** - Executes various automation tasks
- **Status Service** - Reports on system health and component status

#### Inference Modules
Located in `inference/`, these modules handle AI model inference:

- **Cortex Vision** - Advanced computer vision capabilities
- **Ollama Module** - Integration with Ollama for language models
- **YOLO** - Object detection for UI elements

#### Robot Automation
Located in `robot/`, these modules handle system automation:

- **Base Robot** - Core automation functionality
- **Chrome Robot** - Chrome-specific automation
- **Windows Robot** - Windows-specific automation
- **Robot Manager** - Coordinates different robot implementations

## WebSocket API

### Endpoints
The WebSocket API exposes several specialized endpoints:

- **Command Channel**: `/ws/command`
  - For sending commands and receiving results

- **Status Channel**: `/ws/status`
  - For receiving system status updates

- **Screen Capture Channel**: `/ws/screen_capture`
  - For screen capture operations

- **Vision Detect Channel**: `/ws/vision_detect`
  - For vision detection operations

### Message Protocol
Messages use Protocol Buffers for efficient, type-safe serialization.

### Connection Management
- Active connections are tracked per channel
- Proper connection acceptance and cleanup
- Automatic disconnection handling with observer pattern

## REST API Endpoints

- **Health Check**: `GET /health`
  - Basic health check endpoint

- **Generate System Bounding Boxes**: `POST /generate-system-bboxes`
  - Creates system bounding box definitions for automation

- **Active Clients**: `GET /ws/clients`
  - Returns count of active WebSocket clients per channel

## Core Modules

### Command Processing
The command module processes user inputs and converts them to actionable instructions.

### Action Prediction
Uses language models to predict intended actions from user commands.

### Action Execution
Executes predicted actions through the robot automation system.

### Vision Agent
Provides visual understanding of the screen content.

## Frontend Integration Guidelines

### Connection Setup
Connect to specific WebSocket channels based on functionality needed:

```typescript
const socket = new WebSocket('ws://localhost:8000/ws/command');

socket.onopen = () => {
  console.log('Connected to command channel');
};

socket.onclose = () => {
  console.log('Disconnected from command channel');
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

### Sending Messages
Messages should be serialized as Protocol Buffers before sending:

```typescript
// Using protobuf.js or similar library
const message = CommandMessage.create({
  command: 'open chrome'
});

const binary = CommandMessage.encode(message).finish();
socket.send(binary);
```

### Receiving Messages
Responses will be binary Protocol Buffer messages:

```typescript
socket.onmessage = (event) => {
  // Decode the binary message using the appropriate protobuf definition
  const response = CommandResponse.decode(new Uint8Array(event.data));
  handleResponse(response);
};
```

### Multiple Channel Management
For applications requiring multiple channels:

```typescript
class WebSocketChannels {
  commandChannel: WebSocket;
  statusChannel: WebSocket;
  screenCaptureChannel: WebSocket;
  
  constructor() {
    this.commandChannel = new WebSocket('ws://localhost:8000/ws/command');
    this.statusChannel = new WebSocket('ws://localhost:8000/ws/status');
    this.screenCaptureChannel = new WebSocket('ws://localhost:8000/ws/screen_capture');
    
    // Setup handlers for each channel
    this.setupHandlers();
  }
  
  setupHandlers() {
    // Setup connection handlers for each channel
  }
}
```

### Best Practices
1. Implement reconnection logic for WebSocket channels
2. Handle connection errors gracefully
3. Clean up connections when components unmount
4. Use typed interfaces for message handling
5. Handle binary Protocol Buffer messages properly
