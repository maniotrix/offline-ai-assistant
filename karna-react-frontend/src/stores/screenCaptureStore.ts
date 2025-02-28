import { create } from 'zustand';
import { karna } from '../generated/messages';

export interface ScreenCaptureState {
  // Connection state
  connected: boolean;
  error: Error | null;
  
  // Data state
  captureResult: karna.screen_capture.ICaptureResult | null;
  isCapturing: boolean;
  
  // Actions
  setConnected: (connected: boolean) => void;
  setError: (error: Error | null) => void;
  setCaptureResult: (result: karna.screen_capture.ICaptureResult) => void;
  setCapturing: (isCapturing: boolean) => void;
  reset: () => void;
}

const useScreenCaptureStore = create<ScreenCaptureState>((set) => ({
  // Initial state
  connected: false,
  error: null,
  captureResult: null,
  isCapturing: false,
  
  // Actions
  setConnected: (connected) => set({ connected }),
  setError: (error) => set({ error }),
  setCaptureResult: (captureResult) => set({ captureResult }),
  setCapturing: (isCapturing) => set({ isCapturing }),
  reset: () => set({
    connected: false,
    error: null,
    captureResult: null,
    isCapturing: false
  })
}));

export default useScreenCaptureStore;