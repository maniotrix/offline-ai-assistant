import { create } from 'zustand';
import { karna } from '../generated/messages';

interface VisionDetectState {
    connected: boolean;
    error: Error | null;
    results: karna.vision.IVisionDetectResultsList | null;
    status: karna.vision.IVisionDetectStatus | null;
    isProcessing: boolean;
    setConnected: (connected: boolean) => void;
    setError: (error: Error | null) => void;
    setResults: (results: karna.vision.IVisionDetectResultsList) => void;
    setStatus: (status: karna.vision.IVisionDetectStatus) => void;
    setProcessing: (isProcessing: boolean) => void;
    reset: () => void;
}

const useVisionDetectStore = create<VisionDetectState>((set) => ({
    connected: false,
    error: null,
    results: null,
    status: null,
    isProcessing: false,
    setConnected: (connected) => set({ connected }),
    setError: (error) => set({ error }),
    setResults: (results) => set({ results }),
    setStatus: (status) => set({ status }),
    setProcessing: (isProcessing) => set({ isProcessing }),
    reset: () => set({
        connected: false,
        error: null,
        results: null,
        status: null,
        isProcessing: false,
    }),
}));

export default useVisionDetectStore; 