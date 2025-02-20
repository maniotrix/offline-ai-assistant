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

### 📌 API Guidelines
- `GET /api/get_image_data` → Fetch image & bounding boxes.
- `POST /api/save_bboxes` → Save updated bounding box data.

---

## 🎯 Future Enhancements
- ✅ **Undo/Redo support**.
- ✅ **Better keyboard shortcuts**.
- ✅ **Performance optimization for large datasets**.

🚀 **Now you're all set to use the Bounding Box Editor!** Let me know if you need **further improvements**. 🎉🔥
