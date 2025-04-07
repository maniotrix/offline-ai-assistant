# 🧠 Project Karna: Offline AI Assistant

> ⚠️ **Development Status**  
>> This project is under **active development** and is currently in an **experimental phase**. 
>> 
>>> Its current implementation is **tightly bound to the developer’s local system configuration**, with limited portability across environments.
>
> It is open-sourced for **transparency, exploration, and early feedback** — not yet intended for **production use or active collaboration**. 
>
> 🧠 Experienced developers are welcome to clone, explore, and run at their own risk.

An intelligent, human-in-the-loop ,vision-based offline AI assistant capable of understanding and automating tasks on a user's computer through screen capture and analysis.

## 🚀 Project Overview

Project Karna is an offline AI assistant that automates tasks on your computer by analyzing screen contents and executing actions. The system captures screenshots, processes visual information, understands context, and performs actions on your behalf.

#### Read More:
* **[Karna Vision-Based UI Agent: Current Capabilities and Next Steps](karna_cortex_current_status.md)** 

### Core Features

- **📷 Screen Capture & Analysis**: Captures and processes screen content in real-time
- **🤖 Intelligent Automation**: Executes actions based on visual understanding of UI elements
- **🔒 Privacy-Focused**: Works offline for enhanced privacy and security
- **📱 Cross-Device**: Knowledge and configurations can be transferred between devices
- **🧠 Continuous Learning**: Improves through user feedback and interactions

## 🛠️ Repository Structure

> ⚡️ This project has been built with significant help from AI coding agents like GitHub Copilot and Cursor — as part of an ongoing experiment in their real-world capabilities.  
> System architecture, strategy, and even parts of the design process have been developed through interactive collaboration with these agents, under human direction.

```
offline-ai-assistant/
├── karna-python-backend/        # Python backend for AI processing and automation
│   ├── api/                     # API endpoints and handlers
│   ├── asyncs/                  # Asynchronous task processing
│   ├── base/                    # Base classes and interfaces
│   ├── config/                  # Configuration settings
│   ├── data/                    # Data storage and processing
│   ├── database/                # Database models and connections
│   ├── domain/                  # Domain-specific logic
│   ├── generated/               # Generated protobuf code
│   ├── inference/               # AI model inference
│   ├── migrations/              # Database migrations
│   ├── models/                  # ML models and definitions
│   ├── modules/                 # Core application modules
│   ├── robot/                   # Automation control
│   ├── scripts/                 # Utility scripts
│   ├── services/                # Application services
│   ├── tests/                   # Test suite
│   ├── utils/                   # Utility functions
│   └── main.py                  # Application entry point
├── karna-react-frontend/        # React frontend application
│   ├── src/
│   │   ├── api/                 # API clients and WebSocket interface
│   │   ├── components/          # React components
│   │   │   ├── Editor/          # Bounding box editor components
│   │   │   └── Home/            # Homepage and screen capture components
│   │   ├── generated/           # Generated protobuf code
│   │   ├── stores/              # State management with Zustand
│   │   ├── types/               # TypeScript type definitions
│   │   └── utils/               # Utility functions
├── data/                        # Shared data resources
│   ├── chatgpt/                 # ChatGPT integration data
│   ├── logs/                    # Application logs
│   └── youtube.com/             # Demo data for YouTube
├── proto/                       # Protocol buffer definitions
├── scripts/                     # Shared utility scripts
│   └── generate_proto.py        # Protobuf code generation
├── shared/                      # Shared modules between frontend and backend
└── requirements.txt             # Python dependencies
```

## 🧹 Architecture

The system follows a modular architecture for flexibility and maintainability:

### Backend Components

1. **Screen Capture Module**
   - Captures screenshots using platform-specific APIs (DirectX, Metal, X11)
   - Provides privacy features to exclude sensitive areas

2. **Vision Processing Module**
   - Uses YOLO for UI element detection
   - Employs OCR for text extraction
   - Analyzes screen layout and content

3. **Action Execution Module**
   - Simulates user actions (mouse clicks, keyboard input)
   - Supports web browser automation

4. **WebSocket Service**
   - Enables real-time communication between frontend and backend
   - Manages command execution and status updates

### Frontend Components

1. **Home Interface**
   - Controls screen capture sessions
   - Displays captured screenshots and analysis results

2. **Bounding Box Editor**
   - Allows viewing and editing of detected UI elements
   - Supports class selection and annotation

3. **WebSocket Integration**
   - Communicates with backend in real-time
   - Handles command responses and status updates

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ for backend
- Node.js 16+ for frontend
- Windows, macOS, or Linux operating system

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/offline-ai-assistant.git
cd offline-ai-assistant

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
cd karna-python-backend
python main.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd karna-react-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be accessible at `http://localhost:5173`

## 🔄 Communication Flow

1. The frontend captures user interactions and sends commands via WebSocket
2. The backend processes these commands and captures the screen when requested
3. Vision models analyze the captured screens to detect UI elements
4. The backend executes actions based on the analysis and user instructions
5. Results and status updates are sent back to the frontend in real-time

## 🧪 Development

### Protocol Buffers

The project uses Protocol Buffers for efficient data serialization between frontend and backend:

```bash
# Generate Protocol Buffer code for both Python and TypeScript
python scripts/generate_proto.py
```

### Testing

```bash
# Run backend tests
cd karna-python-backend
pytest

# Run frontend tests
cd karna-react-frontend
npm test
```

## 📝 Future Enhancements

- Improve WebSocket connection management and scalability
- Enhance screen capture UI with real-time network viewing
- Implement GPS-based proximity authentication
- Develop specialized agents for different domains/websites
- Better separation of concerns in screen capture service
- Implement more robust error handling and recovery

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project.

## 📄 License

This project is licensed under the [MIT License](./LICENSE).  
It is provided “as-is” without warranty or guarantee of any kind.

## 🤖 AI-Assisted Development Acknowledgment

We gratefully acknowledge the use of **GitHub Copilot**, **Cursor**, and other coding agents throughout this project — as part of an ongoing experiment in their real-world capabilities.

- 🧱 **99% of the frontend code** was scaffolded or directly written with the help of AI coding agents.  
- ⚙️ **~80% of the backend code** was generated via AI assistance, including protobuf schemas, model scaffolds, and automation logic.  
- 📝 **100% of the documentation** (including this README and subcomponent , md files) was written with the assistance of AI Coding/Writing agents.

> System architecture, strategy, and even parts of the design process have been developed through interactive collaboration with these agents — under the direction of a human developer.

This project demonstrates how a human–AI feedback loop can produce complex, modular, and intelligent systems with minimal boilerplate burden and accelerated iteration speed.


