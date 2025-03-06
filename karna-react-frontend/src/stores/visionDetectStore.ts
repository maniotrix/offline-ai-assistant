import { create } from 'zustand';
import { karna } from '../generated/messages';
import { BoundingBox } from '../types/types';

// Extended interface that includes all fields from VisionDetectResultModel plus state management fields
interface ImageAnnotationState extends karna.vision.IVisionDetectResultModel {
  // Fields from VisionDetectResultModel are already included via extension:
  // eventId, projectUuid, commandUuid, timestamp, description,
  // originalImagePath, originalWidth, originalHeight, isCropped,
  // mergedUiIconBboxes, croppedImage, croppedWidth, croppedHeight

  // Additional fields for state management
  annotations: BoundingBox[]; // Converted from mergedUiIconBboxes for easier manipulation
  selectedAnnotationId: string | null;
  history: BoundingBox[][]; // Stores past states for undo
  redoStack: BoundingBox[][]; // Stores redoable states
}

interface VisionDetectState {
    // Connection and processing state
    connected: boolean;
    error: Error | null;
    results: karna.vision.IVisionDetectResultsList | null;
    status: karna.vision.IVisionDetectStatus | null;
    isProcessing: boolean;
    
    // Multi-image annotation state
    images: Record<string, ImageAnnotationState>;
    currentImageId: string | null;
    selectedClasses: Set<string>;
    isSidebarOpen: boolean;
    
    // Connection and processing actions
    setConnected: (connected: boolean) => void;
    setError: (error: Error | null) => void;
    setResults: (results: karna.vision.IVisionDetectResultsList) => void;
    setStatus: (status: karna.vision.IVisionDetectStatus) => void;
    setProcessing: (isProcessing: boolean) => void;
    reset: () => void;
    
    // Multi-image annotation actions
    addImage: (resultModel: karna.vision.IVisionDetectResultModel, annotations?: BoundingBox[]) => void;
    removeImage: (imageId: string) => void;
    setCurrentImage: (imageId: string | null) => void;
    
    // Per-image annotation actions
    setAnnotations: (imageId: string, annotations: BoundingBox[]) => void;
    pushToHistory: (imageId: string) => void;
    setSelectedAnnotationId: (imageId: string, id: string | null) => void;
    
    // Global annotation actions
    toggleSelectedClass: (className: string) => void;
    setSelectedClasses: (classes: Set<string>) => void;
    toggleSidebar: () => void;
    
    // Undo/redo actions
    undo: (imageId: string) => void;
    redo: (imageId: string) => void;

    // Process vision detect results
    processVisionDetectResults: () => void;
}

const useVisionDetectStore = create<VisionDetectState>((set, get) => ({
    // Initial connection and processing state
    connected: false,
    error: null,
    results: null,
    status: null,
    isProcessing: false,
    
    // Initial multi-image annotation state
    images: {},
    currentImageId: null,
    selectedClasses: new Set(),
    isSidebarOpen: true,
    
    // Connection and processing actions
    setConnected: (connected) => set({ connected }),
    setError: (error) => set({ error }),
    setResults: (results) => {
        set({ results });
        // Process the results automatically when they are set
        setTimeout(() => get().processVisionDetectResults(), 0);
    },
    setStatus: (status) => set({ status }),
    setProcessing: (isProcessing) => set({ isProcessing }),
    reset: () => set({
        connected: false,
        error: null,
        results: null,
        status: null,
        isProcessing: false,
    }),
    
    // Multi-image annotation actions
    addImage: (resultModel, annotations = []) => {
        // Ensure eventId is a string
        if (!resultModel.eventId || typeof resultModel.eventId !== 'string') {
            console.error('Cannot add image: eventId is missing or not a string');
            return;
        }
        
        const imageId = resultModel.eventId;
        
        set((state) => ({
            images: {
                ...state.images,
                [imageId]: {
                    // Include all fields from the result model
                    ...resultModel,
                    
                    // Add state management fields
                    annotations,
                    selectedAnnotationId: null,
                    history: [],
                    redoStack: []
                }
            },
            currentImageId: state.currentImageId || imageId // Set as current if none selected
        }));
    },
    
    removeImage: (imageId) => set((state) => {
        const { [imageId]: _, ...remainingImages } = state.images;
        const newCurrentImageId = state.currentImageId === imageId
            ? Object.keys(remainingImages)[0] || null
            : state.currentImageId;
            
        return {
            images: remainingImages,
            currentImageId: newCurrentImageId
        };
    }),
    
    setCurrentImage: (imageId) => set({ currentImageId: imageId }),
    
    // Per-image annotation actions
    setAnnotations: (imageId, annotations) => set((state) => {
        if (!state.images[imageId]) return state;
        
        return {
            images: {
                ...state.images,
                [imageId]: {
                    ...state.images[imageId],
                    annotations,
                    // Also update the mergedUiIconBboxes to keep in sync with proto model
                    mergedUiIconBboxes: annotations.map(ann => ({
                        id: ann.id,
                        x: ann.x,
                        y: ann.y,
                        width: ann.width,
                        height: ann.height,
                        className: ann.class
                    }))
                }
            }
        };
    }),
    
    pushToHistory: (imageId) => set((state) => {
        if (!state.images[imageId]) return state;
        
        const imageState = state.images[imageId];
        
        return {
            images: {
                ...state.images,
                [imageId]: {
                    ...imageState,
                    history: [...imageState.history, [...imageState.annotations]],
                    redoStack: [] // Clear redoStack on new history update
                }
            }
        };
    }),
    
    setSelectedAnnotationId: (imageId, id) => set((state) => {
        if (!state.images[imageId]) return state;
        
        return {
            images: {
                ...state.images,
                [imageId]: {
                    ...state.images[imageId],
                    selectedAnnotationId: id
                }
            }
        };
    }),
    
    // Global annotation actions
    toggleSelectedClass: (className) => set((state) => {
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
    
    // Undo/redo actions
    undo: (imageId) => set((state) => {
        if (!state.images[imageId]) return state;
        
        const imageState = state.images[imageId];
        if (imageState.history.length === 0) return state;
        
        // Get the last state from history
        const prevAnnotations = imageState.history[imageState.history.length - 1];
        
        return {
            images: {
                ...state.images,
                [imageId]: {
                    ...imageState,
                    annotations: [...prevAnnotations],
                    // Also update the mergedUiIconBboxes to keep in sync with proto model
                    mergedUiIconBboxes: prevAnnotations.map(ann => ({
                        id: ann.id,
                        x: ann.x,
                        y: ann.y,
                        width: ann.width,
                        height: ann.height,
                        className: ann.class
                    })),
                    history: imageState.history.slice(0, -1),
                    redoStack: [[...imageState.annotations], ...imageState.redoStack]
                }
            }
        };
    }),
    
    redo: (imageId) => set((state) => {
        if (!state.images[imageId]) return state;
        
        const imageState = state.images[imageId];
        if (imageState.redoStack.length === 0) return state;
        
        // Get the next state from redoStack
        const nextAnnotations = imageState.redoStack[0];
        
        return {
            images: {
                ...state.images,
                [imageId]: {
                    ...imageState,
                    annotations: [...nextAnnotations],
                    // Also update the mergedUiIconBboxes to keep in sync with proto model
                    mergedUiIconBboxes: nextAnnotations.map(ann => ({
                        id: ann.id,
                        x: ann.x,
                        y: ann.y,
                        width: ann.width,
                        height: ann.height,
                        className: ann.class
                    })),
                    history: [...imageState.history, [...imageState.annotations]],
                    redoStack: imageState.redoStack.slice(1)
                }
            }
        };
    }),

    // Process vision detect results
    processVisionDetectResults: () => {
        const { results } = get();
        if (!results || !results.results || !results.results.length) return;

        // Process each result and add it to the images state
        results.results.forEach(result => {
            // Skip results without eventId
            if (!result || !result.eventId || typeof result.eventId !== 'string') {
                console.warn('Skipping result without valid eventId');
                return;
            }

            // Convert proto bounding boxes to our BoundingBox type
            const annotations: BoundingBox[] = (result.mergedUiIconBboxes || [])
                .filter(bbox => bbox && bbox.id && typeof bbox.id === 'string') // Ensure id is a string
                .map(bbox => ({
                    id: bbox.id as string, // Type assertion since we filtered
                    x: bbox.x || 0,
                    y: bbox.y || 0,
                    width: bbox.width || 0,
                    height: bbox.height || 0,
                    class: bbox.className || 'unknown'
                }));

            // Add or update the image in the store
            const state = get();
            const imageId = result.eventId;
            const existingImage = state.images[imageId];
            
            if (existingImage) {
                // Update existing image
                state.setAnnotations(imageId, annotations);
            } else {
                // Add new image with the full result model
                state.addImage(result, annotations);
            }
        });

        // Set the first image as current if none is selected
        const state = get();
        if (!state.currentImageId && Object.keys(state.images).length > 0) {
            state.setCurrentImage(Object.keys(state.images)[0]);
        }

        // Extract all unique classes and add them to selectedClasses if empty
        if (state.selectedClasses.size === 0) {
            const allClasses = new Set<string>();
            Object.values(state.images).forEach(image => {
                image.annotations.forEach(annotation => {
                    if (annotation.class) {
                        allClasses.add(annotation.class);
                    }
                });
            });
            
            if (allClasses.size > 0) {
                state.setSelectedClasses(allClasses);
            }
        }
    }
}));

// Helper functions to make working with the current image easier
export const getCurrentImageState = () => {
    const state = useVisionDetectStore.getState();
    const { currentImageId, images } = state;
    
    if (!currentImageId || !images[currentImageId]) {
        return null;
    }
    
    return images[currentImageId];
};

export const getCurrentAnnotations = () => {
    const currentImage = getCurrentImageState();
    return currentImage ? currentImage.annotations : [];
};

export const getCurrentSelectedAnnotationId = () => {
    const currentImage = getCurrentImageState();
    return currentImage ? currentImage.selectedAnnotationId : null;
};

// Helper to create an object URL from binary image data
export const getImageUrl = (imageId: string) => {
    const state = useVisionDetectStore.getState();
    const image = state.images[imageId];
    
    if (!image || !image.croppedImage || image.croppedImage.length === 0) {
        return null;
    }
    
    // Create URL from binary data
    const blob = new Blob([image.croppedImage], { type: 'image/png' });
    return URL.createObjectURL(blob);
};

export default useVisionDetectStore;