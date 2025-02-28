import { create } from 'zustand';
import { karna } from '../generated/messages';

export interface CommandState {
  // Connection state
  connected: boolean;
  error: Error | null;
  
  // Data state
  commandResponse: karna.command.ICommandResult | null;
  pendingCommands: Map<string, boolean>;
  
  // Actions
  setConnected: (connected: boolean) => void;
  setError: (error: Error | null) => void;
  setCommandResponse: (response: karna.command.ICommandResult) => void;
  addPendingCommand: (id: string) => void;
  removePendingCommand: (id: string) => void;
  reset: () => void;
}

const useCommandStore = create<CommandState>((set) => ({
  // Initial state
  connected: false,
  error: null,
  commandResponse: null,
  pendingCommands: new Map<string, boolean>(),
  
  // Actions
  setConnected: (connected) => set({ connected }),
  setError: (error) => set({ error }),
  setCommandResponse: (response) => set({ commandResponse: response }),
  addPendingCommand: (id) => set((state) => {
    const pendingCommands = new Map(state.pendingCommands);
    pendingCommands.set(id, true);
    return { pendingCommands };
  }),
  removePendingCommand: (id) => set((state) => {
    const pendingCommands = new Map(state.pendingCommands);
    pendingCommands.delete(id);
    return { pendingCommands };
  }),
  reset: () => set({
    connected: false,
    error: null,
    commandResponse: null,
    pendingCommands: new Map<string, boolean>()
  })
}));

export default useCommandStore;