// The one shared app state (docs/PLAN.md section 5). Components never import each other;
// each reads and writes this store, and the map reacts to it.
// Owner: Eduardo (app/src/state/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { create } from 'zustand';
import { loadLandmarks, loadManifest } from '../lib/data';
import type { Landmark, Layer, LngLat, Manifest } from '../types/manifest';

export type LoadStatus = 'idle' | 'loading' | 'ready' | 'error';

/** Where a story step asks the map to fly. Added for T-18 (Monica). */
export type CameraTarget = { center: LngLat; zoom: number };

export type AppState = {
  /**
   * Region whose data is in `manifest` and `landmarks`. It only changes together with that data,
   * so the two never disagree. Before the first load it is the default region with no data yet.
   */
  regionId: string;
  manifest: Manifest | null;
  landmarks: Landmark[];
  /** Region being loaded right now, or null. The current data stays on screen meanwhile. */
  loadingRegionId: string | null;
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
  /** Last camera a story step asked for; the map flies there when it changes. null = no request. */
  cameraTarget: CameraTarget | null;
  /** State of the most recent load request. */
  loadStatus: LoadStatus;
  /** Why the most recent load failed; the previous region's data is still shown. */
  loadError: string | null;
};

/** The part of the state a story step may set. Region and data change only through loadRegion. */
export type ViewState = Pick<
  AppState,
  | 'activeLayerId'
  | 'compareLayerId'
  | 'dateIndex'
  | 'compareDateIndex'
  | 'selectedLandmarkId'
  | 'storyStep'
  | 'cameraTarget'
>;

export type AppActions = {
  /**
   * The only way to change region. Loads manifest and landmarks, then swaps region and data in one
   * step and resets the view. Only the newest request may change the store: a response that
   * arrives after a newer request started is dropped, whether it succeeded or failed.
   */
  loadRegion: (regionId: string) => Promise<void>;
  setLayer: (layerId: string) => void;
  setCompare: (layerId: string | null, dateIndex?: number | null) => void;
  setDate: (dateIndex: number) => void;
  selectLandmark: (landmarkId: string | null) => void;
  setStoryStep: (step: number | null) => void;
  /** Apply a story step's `set` block (content/story/<region>.json). */
  applyPartial: (partial: Partial<ViewState>) => void;
};

/** Folder under public/data/ to load. "sample" until the pipeline writes a real region. */
export const DEFAULT_REGION_ID: string = import.meta.env.VITE_REGION_ID ?? 'sample';

/** Number of the newest loadRegion call. Responses from older calls are dropped. */
let latestRequest = 0;

export const useAppStore = create<AppState & AppActions>()((set) => ({
  regionId: DEFAULT_REGION_ID,
  manifest: null,
  landmarks: [],
  loadingRegionId: null,
  activeLayerId: '',
  compareLayerId: null,
  dateIndex: 0,
  compareDateIndex: null,
  selectedLandmarkId: null,
  storyStep: null,
  cameraTarget: null,
  loadStatus: 'idle',
  loadError: null,

  loadRegion: async (regionId) => {
    const request = ++latestRequest;
    const isStale = () => request !== latestRequest;
    set({ loadingRegionId: regionId, loadStatus: 'loading', loadError: null });
    try {
      const manifest = await loadManifest(regionId);
      // Landmarks are optional: the map works without them.
      const landmarks = await loadLandmarks(regionId)
        .then((f) => f.landmarks)
        .catch(() => [] as Landmark[]);
      if (isStale()) return;
      set({
        regionId,
        manifest,
        landmarks,
        loadingRegionId: null,
        activeLayerId: manifest.layers[0]?.id ?? '',
        compareLayerId: null,
        dateIndex: 0,
        compareDateIndex: null,
        selectedLandmarkId: null,
        loadStatus: 'ready',
      });
    } catch (err) {
      if (isStale()) return;
      // Keep the region and data already on screen; only report the failure.
      const reason = err instanceof Error ? err.message : String(err);
      set({ loadingRegionId: null, loadStatus: 'error', loadError: `Region "${regionId}": ${reason}` });
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
