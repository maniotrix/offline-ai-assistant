import create from "zustand";
import { BoundingBox } from "../types/types";

interface AnnotationStore {
  annotations: BoundingBox[];
  selectedAnnotationId: string | null;
  selectedClasses: Set<string>;
  isSidebarOpen: boolean;
  history: BoundingBox[][]; // Stores past states for undo
  redoStack: BoundingBox[][]; // Stores redoable states
  setAnnotations: (annotations: BoundingBox[]) => void;
  pushToHistory: () => void;
  setSelectedAnnotationId: (id: string | null) => void;
  toggleSelectedClass: (className: string) => void;
  setSelectedClasses: (classes: Set<string>) => void;
  toggleSidebar: () => void;
}

const useAnnotationStore = create<AnnotationStore>((set) => ({
  annotations: [],
  selectedAnnotationId: null,
  selectedClasses: new Set(),
  isSidebarOpen: true,
  history: [],
  redoStack: [],

  setAnnotations: (newAnnotations) =>
    set(() => ({
      annotations: newAnnotations,
    })),

  // ✅ Function to manually push current state into history
  pushToHistory: () =>
    set((state) => ({
      history: [...state.history, state.annotations],
      redoStack: [], // Clear redoStack on new history update
    })),

  setSelectedAnnotationId: (id) => set({ selectedAnnotationId: id }),

  toggleSelectedClass: (className) =>
    set((state) => {
      const updatedClasses = new Set(state.selectedClasses);
      if (updatedClasses.has(className)) {
        updatedClasses.delete(className);
      } else {
        updatedClasses.add(className);
      }
      return { selectedClasses: updatedClasses };
    }),

  setSelectedClasses: (classes) => set({ selectedClasses: classes }),

  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
}));

export default useAnnotationStore;
