# 📌 Karna React Frontend

A modern React application for the Project Karna Offline AI Assistant. This frontend provides interactive image annotation features, screen capture capabilities, and real-time communication with the backend.

---

## 🚀 Tech Stack

The project is built using modern web technologies for optimal performance and user experience.

| Technology      | Purpose                                      |
|--------------- |--------------------------------------------- |
| **React**      | Core UI framework                           |
| **TypeScript** | Type safety for maintainability             |
| **Vite**       | Fast development server                     |
| **Zustand**    | Global state management                     |
| **React-Konva** | Canvas rendering for bounding box manipulation |
| **Material-UI (MUI)** | UI components and theming |
| **Tailwind CSS** | Responsive styling |
| **React-Draggable** | Movable toolbar |
| **Socket.IO** | Real-time communication with backend |
| **React Router** | Application routing |
| **ESLint & Prettier** | Code quality and formatting |

---

## 📂 Project Structure

```
karna-react-frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── websocket/
│   │   ├── api.ts                 # API client for HTTP requests
│   │   ├── constants.ts           # API constants and endpoints
│   │   └── websocket.ts           # WebSocket service implementation
│   ├── components/
│   │   ├── Editor/
│   │   │   ├── BboxEditor.tsx     # Main bounding box editor component
│   │   │   ├── CanvasEditor/      # Canvas rendering with Konva
│   │   │   ├── ClassSelector/     # Sidebar for selecting bounding box classes
│   │   │   ├── Header/            # Editor header components
│   │   │   └── Toolbar/           # Floating toolbar for editor actions
│   │   └── Home/
│   │       ├── Homepage.tsx       # Main homepage component
│   │       ├── Homepage.css       # Homepage styling
│   │       ├── ScreenCaptureButton.tsx  # Button for capturing screen
│   │       └── ScreenCaptureSlideshow.tsx  # Component for displaying captured screens
│   ├── generated/                 # Generated code (e.g., protobuf)
│   ├── stores/
│   │   ├── commandStore.ts        # Store for command management
│   │   ├── screenCaptureStore.ts  # Store for screen capture state
│   │   ├── statusStore.ts         # Store for application status
│   │   └── visionDetectStore.ts   # Store for vision detection results
│   ├── types/                     # TypeScript interfaces and type definitions
│   ├── utils/                     # Utility functions
│   ├── App.tsx                    # Main application container
│   ├── main.tsx                   # React entry point
│   └── index.css                  # Global styles (Tailwind)
├── .gitignore                     # Files to ignore in version control
├── package.json                   # Project dependencies and scripts
├── tsconfig.json                  # TypeScript configuration
├── vite.config.ts                 # Vite configuration for local server
└── tailwind.config.js             # Tailwind CSS configuration
```

---

## 🛠️ Features

### ✅ Bounding Box Editor
- View, resize, move, and delete bounding boxes on images
- Add new bounding boxes by drawing on the image
- Class selection with color coding
- Zoom & pan functionality

### ✅ Screen Capture
- Capture and process screens for AI analysis
- Visual display of captured screens with slideshow functionality
- Real-time feedback on captured screens

### ✅ WebSocket Integration
- Real-time communication with backend systems
- Status updates and command execution
- RPC-style message handling

### ✅ Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch gesture support

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/offline-ai-assistant.git
cd offline-ai-assistant/karna-react-frontend
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

### 4️⃣ Build for Production
```sh
npm run build
```
- The production build will be in the `dist` directory.

---

## 📡 WebSocket Implementation

### WebSocket Service
Located in `src/api/websocket.ts`, the WebSocketService provides:
- Connection management with automatic reconnection
- RPC-style message handling
- Status subscription
- Error handling

### Message Types
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

### Usage in Components
```typescript
import { websocketService } from '../api/websocket';

// Connect when component mounts
useEffect(() => {
    websocketService.connect();
    return () => websocketService.disconnect();
}, []);

// Send commands
await websocketService.sendCommand("your_command", params);

// Subscribe to status updates
websocketService.onStatusUpdate((status) => {
    // Handle status update
});
```

---

## 🖊️ Development Guidelines

### Coding Style
- Use ESLint and Prettier for consistent formatting
- Follow Material-UI & Tailwind best practices
- Keep components modular and focused

### State Management
- Use Zustand for global state
- Keep stores organized by domain (e.g., screenCaptureStore, statusStore)
- Minimize prop drilling through proper store design

### Component Structure
- Place components in logical folders by feature
- Use TypeScript interfaces for props and state
- Implement error boundaries where appropriate

---

## 🎯 Future Enhancements
- Full keyboard shortcuts support
- Additional annotation tools
- Performance optimization for large datasets
- Enhanced real-time collaboration features

---

🚀 **Now you're ready to work with the Karna React Frontend!** 🎉
