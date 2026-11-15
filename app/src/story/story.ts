// Guided tour data (T-18): types, loading content/story/<region>.json, and turning a step into store state.
// Owner: Monica (app/src/story/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { ViewState } from '../state/store';
import type { IsoDate, LngLat, Manifest } from '../types/manifest';

/** Where a step moves the map. The tour passes it to the store's flyTo. */
export type StoryCamera = { center: LngLat; zoom: number };

/**
 * What a step shows. Each step names its whole view, so Back and Next give the same picture
 * whichever way you arrive. Dates are written as dates, not frame numbers, so the story keeps
 * working when the pipeline adds or drops frames (as D-13 did).
 */
export type StorySet = {
  layer: string;
  date: IsoDate;
  /** Right side of the swipe. Leave out for no swipe. */
  compareLayer?: string;
  compareDate?: IsoDate;
  /** Landmark to open. Leave out for none. */
  landmark?: string;
};

export type StoryStep = {
  id: string;
  title: string;
  /** Paragraphs. Only claims with a row in docs/DECISION_MEMO.md belong here. */
  body: string[];
  set: StorySet;
  camera: StoryCamera;
  sourceIds: string[];
  /** Claims waiting for a source row or a data check. Never shown in the app. */
  pendingClaims?: string[];
};

export type StorySource = { id: string; title: string; url: string };

export type StoryFile = {
  schemaVersion: string;
  regionId: string;
  intro: {
    title: string;
    tagline: string;
    body: string[];
    startLabel: string;
    exploreLabel: string;
    sourceIds: string[];
  };
  steps: StoryStep[];
  sources: StorySource[];
};

// Every story in content/story/, keyed by region id. Adding content/story/caracas.json is enough
// to give that region a tour.
const files = import.meta.glob<StoryFile>('../../../content/story/*.json', { eager: true, import: 'default' });
const stories = new Map<string, StoryFile>(Object.values(files).map((s) => [s.regionId, s]));

/** The tour for a region, or undefined if it has none. */
export function getStory(regionId: string): StoryFile | undefined {
  return stories.get(regionId);
}

/** All region ids that have a tour. */
export function storyRegionIds(): string[] {
  return [...stories.keys()];
}

export type ResolvedStep = {
  view: Partial<ViewState>;
  /** Anything the step names that the manifest does not have. Empty when the step is valid. */
  problems: string[];
};

/** Turn a step into store state against the loaded manifest. Unknown layers or dates are reported, not guessed. */
export function resolveStep(step: StoryStep, manifest: Manifest): ResolvedStep {
  const problems: string[] = [];
  const frameIndex = (layerId: string, date: IsoDate): number | null => {
    const layer = manifest.layers.find((l) => l.id === layerId);
    if (!layer) {
      problems.push(`step "${step.id}": no layer "${layerId}" in the manifest`);
      return null;
    }
    const i = layer.frames.findIndex((f) => f.date === date);
    if (i < 0) problems.push(`step "${step.id}": layer "${layerId}" has no frame dated ${date}`);
    return i < 0 ? null : i;
  };

  const { layer, date, compareLayer, compareDate, landmark } = step.set;
  const view: Partial<ViewState> = {
    selectedLandmarkId: landmark ?? null,
  };

  const dateIndex = frameIndex(layer, date);
  if (dateIndex !== null) {
    view.activeLayerId = layer;
    view.dateIndex = dateIndex;
  }

  if (compareLayer === undefined) {
    view.compareLayerId = null;
    view.compareDateIndex = null;
  } else if (compareDate === undefined) {
    problems.push(`step "${step.id}": compareLayer is set but compareDate is missing`);
  } else {
    const compareIndex = frameIndex(compareLayer, compareDate);
    if (compareIndex !== null) {
      view.compareLayerId = compareLayer;
      view.compareDateIndex = compareIndex;
    }
  }

  return { view, problems };
}

/** Look up source ids in the story's own list first, then the manifest's. Unknown ids are skipped. */
export function findSources(story: StoryFile, manifest: Manifest | null, ids: string[]): StorySource[] {
  return ids.flatMap((id) => {
    const s = story.sources.find((x) => x.id === id) ?? manifest?.sources.find((x) => x.id === id);
    return s ? [{ id: s.id, title: s.title, url: s.url }] : [];
  });
}
