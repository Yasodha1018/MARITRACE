import create from 'zustand';

export const useStore = create((set) => ({
  incident: null,
  setIncident: (incident) => set({ incident }),
}));