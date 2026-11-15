// Places the components on the page. Components never import each other; they share the store.
// Owner: Eduardo (app/src/App.tsx). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect } from 'react';
import LayerSwitcher from './components/layers/LayerSwitcher';
import Legend from './components/layers/Legend';
import ViewOptions from './components/layers/ViewOptions';
import MapView from './map/MapView';
import { DEFAULT_REGION_ID, useAppStore } from './state/store';
import ReadingGuide from './story/ReadingGuide';
import StoryTour from './story/StoryTour';

export default function App() {
  const loadError = useAppStore((s) => s.loadError);

  // Load the starting region once. After that, only loadRegion changes region; this component
  // does not react to regionId, so a region change never starts a second load.
  // (In development, React StrictMode runs this twice; the store drops the older request.)
  useEffect(() => {
    void useAppStore.getState().loadRegion(DEFAULT_REGION_ID);
  }, []);

  useEffect(() => {
    // The map still works without data (for example before the T-08 sample lands), so only warn.
    if (loadError) console.warn(`[data] ${loadError}`);
  }, [loadError]);

  return (
    <div className="app">
      <MapView />
      <aside className="layer-controls">
        <header className="panel__header">
          <h1 className="panel__title">NISAR over Mexico City</h1>
          <p className="panel__byline">Team B[U]ILT to Last, NASA Space Apps 2026</p>
        </header>
        <LayerSwitcher />
        <ViewOptions />
        <Legend />
      </aside>
      <ReadingGuide />
      <StoryTour />
      {/* Slots for later tasks: layers and time (Diego), landmarks, chart, sources (Zainab). */}
    </div>
  );
}
