# 📌 YOLO Bounding Box Editor – Frontend

This project provides an **interactive bounding box editor** for **YOLO-generated annotations**. The editor allows users to **view, edit, add, and remove bounding boxes on images** while supporting **class selection and zooming/panning**.

---

## 🚀 Tech Stack

The project is built using modern **React and TypeScript** with **state management and interactive UI**.

| Technology      | Purpose                                      |
|--------------- |--------------------------------------------- |
| **React**      | Core UI framework                           |
| **TypeScript** | Type safety for maintainability             |
| **Vite**       | Fast development server                     |
| **Zustand**    | Global state management for bounding boxes & UI |
| **React-Konva** | Canvas rendering for bounding box manipulation |
| **Material-UI (MUI)** | UI components and theming |
| **Tailwind CSS** | Responsive styling |
| **React-Draggable** | Movable toolbar |
| **ESLint & Prettier** | Code quality and formatting |

---

## 📂 Project Structure

```
bbox-editor/
├── public/
│   └── vite.svg                 # Default Vite logo
├── src/
│   ├── components/
│   │   ├── CanvasEditor/
│   │   │   ├── CanvasEditor.tsx # Main canvas rendering with Konva
│   │   │   └── CanvasEditor.css # Styling for canvas area
│   │   ├── ClassSelector/
│   │   │   └── ClassSelector.tsx # Sidebar for selecting bounding box classes
│   │   ├── Toolbar/
│   │   │   └── Toolbar.tsx       # Floating toolbar for Save/Cancel
│   ├── hooks/
│   │   └── useCanvasInit.ts      # Handles canvas setup
│   ├── stores/
│   │   └── annotationStore.ts    # Zustand store for managing bounding boxes
│   ├── types/
│   │   └── types.ts              # TypeScript interfaces for bounding boxes
│   ├── api/
│   │   └── api.ts                # API calls for fetching and saving data
│   │   └── websocket.ts          # WebSocket service for real-time communication
│   ├── App.tsx                   # Main application container
│   ├── main.tsx                  # React entry point
│   ├── index.css                  # Global styles (Tailwind)
├── .gitignore                     # Files to ignore in version control
├── package.json                    # Project dependencies and scripts
├── tsconfig.json                    # TypeScript configuration
├── vite.config.ts                   # Vite configuration for local server
```

---

## 🛠️ Features

### ✅ Bounding Box Editing
- View, resize, move, and delete bounding boxes.
- Add new bounding boxes by drawing on the image.

### ✅ Class Selection Panel
- **Collapsible sidebar** for class selection.
- Users can select **one or multiple classes**.
- "All Classes" toggle to show/hide all classes.

### ✅ Zoom & Pan
- **Konva-based image rendering** supports zooming and panning.

### ✅ Floating Toolbar
- **Draggable toolbar** for Save/Cancel actions.

### ✅ Mobile-Friendly
- **Responsive UI with Material-UI & Tailwind**.
- **Touch gestures for zoom/pan** support.

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/bbox-editor.git
cd bbox-editor
```

### 2️⃣ Install Dependencies
```sh
npm install
```

### 3️⃣ Start the Development Server
```sh
npm run dev
```
- The app runs at **`http://localhost:5173/`** by default.

### 4️⃣ Run the Backend (if needed)
Make sure your **Flask backend** is running at **`http://localhost:5000`**.

---

## 🛠️ Development Guidelines

### 🖊️ Coding Style
- Use **ESLint and Prettier** for consistent formatting.
- Follow **Material-UI & Tailwind best practices**.
- Keep **components modular**.

### 📂 File Naming Conventions
- Components: `PascalCase.tsx` (e.g., `CanvasEditor.tsx`).
- Hooks: `camelCase.ts` (e.g., `useCanvasInit.ts`).
- Zustand Stores: `camelCase.ts` (e.g., `annotationStore.ts`).

---

# Karna React Frontend - WebSocket Implementation

## Overview
The frontend implements a WebSocket client using Socket.IO to establish real-time communication with the backend. The implementation is encapsulated in the `WebSocketService` class.

## Architecture

### WebSocket Service
Located in `src/api/websocket.ts`, the WebSocketService provides:
- Connection management
- RPC-style message handling
- Status subscription
- Error handling

## Implementation Details

### Service Structure
```typescript
class WebSocketService {
    private socket: Socket | null;
    private messageHandlers: Map<string, (data: any) => void>;
    private rpcCallbacks: Map<string, (response: RPCResponse) => void>;
}
```

### Key Features

#### Connection Management
- Automatic reconnection with configurable attempts
- Connection state monitoring
- Clean disconnection handling

#### Message Types
```typescript
interface RPCResponse {
    type: 'command_response' | 'status_update' | 'error';
    data: any;
}

interface RPCRequest {
    method: string;
    params: any;
}
```

#### Status Subscription
```typescript
// Subscribe to status updates
websocketService.onStatusUpdate((status) => {
    // Handle status update
});

// Request current status
await websocketService.requestStatus();
```

#### Command Execution
```typescript
// Send a command
await websocketService.sendCommand("your command here");

// Listen for command responses
websocketService.onCommandResponse((response) => {
    // Handle command response
});
```

## Usage in Components

### Basic Setup
```typescript
import { websocketService } from '../api/websocket';

useEffect(() => {
    // Connect when component mounts
    websocketService.connect();

    return () => {
        // Cleanup on unmount
        websocketService.disconnect();
    };
}, []);
```

### Error Handling
- All WebSocket operations are Promise-based
- Errors are properly typed and propagated
- Connection errors trigger automatic reconnection

## Integration with Backend
- Connects to backend WebSocket endpoint at `ws://localhost:8000/ws`
- Uses Socket.IO for reliable bi-directional communication
- Implements the same message protocol as defined in the backend

## Best Practices
1. Use the singleton WebSocketService instance
2. Always handle connection errors
3. Clean up subscriptions on component unmount
4. Use TypeScript for type safety
5. Implement error boundaries for WebSocket-related errors

## 🎯 Future Enhancements
- ✅ **Undo/Redo support**.
- ✅ **Better keyboard shortcuts**.
- ✅ **Performance optimization for large datasets**.

🚀 **Now you're all set to use the Bounding Box Editor!** Let me know if you need **further improvements**. 🎉🔥
