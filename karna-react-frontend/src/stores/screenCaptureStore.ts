import { create } from 'zustand';
import { karna } from '../generated/messages';

export interface ScreenCaptureState {
  // Connection state
  connectionState: 'connected' | 'connecting' | 'disconnected';
  dataState: 'loading' | 'ready' | 'error';
  
  // Data state
  captureResult: karna.screen_capture.ICaptureResult | null;
  isCapturing: boolean;
  
  // Actions
  setConnectionState: (state: 'connected' | 'connecting' | 'disconnected') => void;
  setCaptureResult: (result: karna.screen_capture.ICaptureResult | null) => void;
  setCapturing: (isCapturing: boolean) => void;
  setScreenshotEvents: (events: karna.screen_capture.IRpcScreenshotEvent[]) => void;
  reset: () => void;
}

const useScreenCaptureStore = create<ScreenCaptureState>((set) => ({
  // Initial state
  connectionState: 'disconnected',
  dataState: 'loading',
  captureResult: null,
  isCapturing: false,
  
  // Actions
  setConnectionState: (connectionState) => set({ connectionState }),
  setCaptureResult: (captureResult) => set({ captureResult, dataState: 'ready' }),
  setCapturing: (isCapturing) => set({ isCapturing }),
  setScreenshotEvents: (events) => set((state) => ({
    captureResult: state.captureResult ? {
      ...state.captureResult,
      screenshotEvents: events
    } : null
  })),
  reset: () => set({
    connectionState: 'disconnected',
    dataState: 'loading',
    captureResult: null,
    isCapturing: false
  })
}));

export default useScreenCaptureStore;