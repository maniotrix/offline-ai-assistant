import { create } from 'zustand';
import { karna } from '../generated/messages';

export interface StatusState {
  // Connection state
  connected: boolean;
  error: Error | null;
  
  // Data state
  status: karna.status.IStatusResult | null;
  
  // Actions
  setConnected: (connected: boolean) => void;
  setError: (error: Error | null) => void;
  setStatus: (status: karna.status.IStatusResult) => void;
  reset: () => void;
}

const useStatusStore = create<StatusState>((set) => ({
  // Initial state
  connected: false,
  error: null,
  status: null,
  
  // Actions
  setConnected: (connected) => set({ connected }),
  setError: (error) => set({ error }),
  setStatus: (status) => set({ status }),
  reset: () => set({
    connected: false,
    error: null,
    status: null
  })
}));

export default useStatusStore;