// The one shared app state (docs/PLAN.md section 5). Components never import each other;
// each reads and writes this store, and the map reacts to it.
// Owner: Eduardo (app/src/state/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { create } from 'zustand';
import { loadLandmarks, loadManifest } from '../lib/data';
import type { Landmark, Layer, Manifest } from '../types/manifest';

export type LoadStatus = 'idle' | 'loading' | 'ready' | 'error';

export type AppState = {
  regionId: string;
  manifest: Manifest | null;
  landmarks: Landmark[];
  /** Layer shown (left side of the swipe). Empty string until a manifest is loaded. */
  activeLayerId: string;
  /** Right side of the swipe; null = no swipe. */
  compareLayerId: string | null;
  /** Index into the active layer's frames. */
  dateIndex: number;
  compareDateIndex: number | null;
  selectedLandmarkId: string | null;
  /** null = free exploration. */
  storyStep: number | null;
  loadStatus: LoadStatus;
  loadError: string | null;
};

export type AppActions = {
  /** Load manifest and landmarks for a region and reset the view state. */
  loadRegion: (regionId: string) => Promise<void>;
  setLayer: (layerId: string) => void;
  setCompare: (layerId: string | null, dateIndex?: number | null) => void;
  setDate: (dateIndex: number) => void;
  selectLandmark: (landmarkId: string | null) => void;
  setStoryStep: (step: number | null) => void;
  /** Apply a story step's `set` block (content/story/<region>.json). */
  applyPartial: (partial: Partial<AppState>) => void;
};

/** Folder under public/data/ to load. "sample" until the pipeline writes a real region. */
export const DEFAULT_REGION_ID: string = import.meta.env.VITE_REGION_ID ?? 'sample';

export const useAppStore = create<AppState & AppActions>()((set, get) => ({
  regionId: DEFAULT_REGION_ID,
  manifest: null,
  landmarks: [],
  activeLayerId: '',
  compareLayerId: null,
  dateIndex: 0,
  compareDateIndex: null,
  selectedLandmarkId: null,
  storyStep: null,
  loadStatus: 'idle',
  loadError: null,

  loadRegion: async (regionId) => {
    set({ regionId, loadStatus: 'loading', loadError: null });
    try {
      const manifest = await loadManifest(regionId);
      // Landmarks are optional: the map works without them.
      const landmarks = await loadLandmarks(regionId)
        .then((f) => f.landmarks)
        .catch(() => [] as Landmark[]);
      if (get().regionId !== regionId) return; // a newer load started meanwhile
      set({
        manifest,
        landmarks,
        activeLayerId: manifest.layers[0]?.id ?? '',
        compareLayerId: null,
        dateIndex: 0,
        compareDateIndex: null,
        selectedLandmarkId: null,
        loadStatus: 'ready',
      });
    } catch (err) {
      if (get().regionId !== regionId) return;
      set({ loadStatus: 'error', loadError: err instanceof Error ? err.message : String(err) });
    }
  },

  setLayer: (layerId) => set({ activeLayerId: layerId, dateIndex: 0 }),
  setCompare: (layerId, dateIndex = null) =>
    set({ compareLayerId: layerId, compareDateIndex: layerId === null ? null : dateIndex }),
  setDate: (dateIndex) => set({ dateIndex }),
  selectLandmark: (landmarkId) => set({ selectedLandmarkId: landmarkId }),
  setStoryStep: (step) => set({ storyStep: step }),
  applyPartial: (partial) => set(partial),
}));

/** The active layer, or undefined if no manifest is loaded. */
export const selectActiveLayer = (s: AppState): Layer | undefined =>
  s.manifest?.layers.find((l) => l.id === s.activeLayerId);
