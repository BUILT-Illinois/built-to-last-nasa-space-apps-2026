// Places the components on the page. Components never import each other; they share the store.
// Owner: Eduardo (app/src/App.tsx). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect } from 'react';
import LayerSwitcher from './components/layers/LayerSwitcher';
import Legend from './components/layers/Legend';
import MapView from './map/MapView';
import { DEFAULT_REGION_ID, useAppStore } from './state/store';

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
        <LayerSwitcher />
        <Legend />
      </aside>
      {/* Slots for later tasks: story (Monica), layers and time (Diego), landmarks, chart, sources (Zainab). */}
    </div>
  );
}
