// Places the components on the page. Components never import each other; they share the store.
// Owner: Eduardo (app/src/App.tsx). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect } from 'react';
import MapView from './map/MapView';
import { useAppStore } from './state/store';

export default function App() {
  const regionId = useAppStore((s) => s.regionId);
  const loadRegion = useAppStore((s) => s.loadRegion);
  const loadError = useAppStore((s) => s.loadError);

  useEffect(() => {
    void loadRegion(regionId);
  }, [regionId, loadRegion]);

  useEffect(() => {
    // The map still works without data (for example before the T-08 sample lands), so only warn.
    if (loadError) console.warn(`[data] ${loadError}`);
  }, [loadError]);

  return (
    <div className="app">
      <MapView />
      {/* Slots for later tasks: story (Monica), layers and time (Diego), landmarks, chart, sources (Zainab). */}
    </div>
  );
}
