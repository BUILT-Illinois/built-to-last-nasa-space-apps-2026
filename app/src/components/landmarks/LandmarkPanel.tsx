// T-14 landmark panel: a list of landmarks and a card for the selected one.
// Reads and writes only the shared store, so the map can stay in sync through selectedLandmarkId.
// Owner: Zainab (app/src/components/landmarks/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useMemo } from 'react';
import { useAppStore } from '../../state/store';
import type { Source } from '../../types/manifest';
import { cardsFor, withCardText } from './landmarkCards';
import './LandmarkPanel.css';

/** Zoom used when flying to a landmark. */
const LANDMARK_ZOOM = 13;

// One shared empty list: a new [] on every render would make the store selector loop forever.
const NO_SOURCES: Source[] = [];

export default function LandmarkPanel() {
  const regionId = useAppStore((s) => s.regionId);
  const published = useAppStore((s) => s.landmarks);
  const selectedId = useAppStore((s) => s.selectedLandmarkId);
  const loadStatus = useAppStore((s) => s.loadStatus);
  const manifestSources = useAppStore((s) => s.manifest?.sources ?? NO_SOURCES);
  const selectLandmark = useAppStore((s) => s.selectLandmark);
  const flyTo = useAppStore((s) => s.flyTo);

  // Monica's card text over the published landmarks; card sources first, then the manifest's.
  const cards = cardsFor(regionId);
  const landmarks = useMemo(() => withCardText(published, cards), [published, cards]);
  const sources = useMemo(() => [...(cards?.sources ?? []), ...manifestSources], [cards, manifestSources]);

  const selected = landmarks.find((l) => l.id === selectedId);

  if (loadStatus === 'loading' && landmarks.length === 0) {
    return <aside className="landmark-panel"><p>Loading landmarks…</p></aside>;
  }

  if (landmarks.length === 0) {
    return (
      <aside className="landmark-panel">
        <h2>Landmarks</h2>
        <p className="landmark-empty">No landmarks for this region yet.</p>
      </aside>
    );
  }

  return (
    <aside className="landmark-panel">
      <h2>Landmarks</h2>
      <ul className="landmark-list">
        {landmarks.map((l) => (
          <li key={l.id}>
            <button
              type="button"
              aria-pressed={l.id === selectedId}
              onClick={() => {
                if (l.id === selectedId) return selectLandmark(null);
                selectLandmark(l.id);
                flyTo([l.lon, l.lat], LANDMARK_ZOOM);
              }}
            >
              {l.name}
            </button>
          </li>
        ))}
      </ul>

      {selected && (
        <article className="landmark-card">
          <h3>{selected.name}</h3>
          <p>{selected.summary}</p>

          <section className="landmark-radar">
            <h4>What the radar shows</h4>
            <p>{selected.radarShows}</p>
          </section>

          <section className="landmark-infer">
            <h4>What we infer</h4>
            <p>{selected.weInfer}</p>
          </section>

          {(selected.drivers.human || selected.drivers.natural) && (
            <section>
              <h4>Possible drivers</h4>
              <ul>
                {selected.drivers.human && <li>Human: {selected.drivers.human}</li>}
                {selected.drivers.natural && <li>Natural: {selected.drivers.natural}</li>}
              </ul>
            </section>
          )}

          <section>
            <h4>Sources</h4>
            <ul>
              {selected.sourceIds.map((id) => {
                const source = sources.find((s) => s.id === id);
                return (
                  <li key={id}>
                    {source ? <a href={source.url} target="_blank" rel="noreferrer">{source.title}</a> : id}
                  </li>
                );
              })}
            </ul>
          </section>
        </article>
      )}
    </aside>
  );
}
