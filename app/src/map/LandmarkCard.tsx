// Map landmark info card. Drafted with AI assistance (Codex), see docs/AI_USAGE.md.
import { useEffect, useRef } from 'react';
import { useAppStore } from '../state/store';
import { cardsFor, withCardText } from '../components/landmarks/landmarkCards';
import './landmarkCard.css';

export default function LandmarkCard({ onClose }: { onClose: () => void }) {
  const regionId = useAppStore((s) => s.regionId);
  const landmarks = useAppStore((s) => s.landmarks);
  const selectedId = useAppStore((s) => s.selectedLandmarkId);
  const manifest = useAppStore((s) => s.manifest);
  const storyStep = useAppStore((s) => s.storyStep);
  const closeRef = useRef<HTMLButtonElement>(null);
  const published = landmarks.find((landmark) => landmark.id === selectedId);
  const cards = cardsFor(regionId);
  const selected = published && storyStep === null ? withCardText([published], cards)[0] : undefined;
  const visibleId = selected?.id;

  useEffect(() => {
    if (visibleId) closeRef.current?.focus();
  }, [visibleId]);

  if (!selected) return null;
  const sources = selected.sourceIds.flatMap((id) => {
    const source = cards?.sources?.find((s) => s.id === id) ?? manifest?.sources.find((s) => s.id === id);
    return source ? [source] : [];
  });
  const { human, natural } = selected.drivers;

  return (
    <article
      className="map-landmark-card"
      aria-labelledby="map-landmark-card-title"
      onKeyDown={(event) => {
        if (event.key === 'Escape') {
          event.stopPropagation();
          onClose();
        }
      }}
    >
      <header>
        <h2 id="map-landmark-card-title">{selected.name}</h2>
        <button ref={closeRef} type="button" aria-label="Close landmark card" onClick={onClose}>×</button>
      </header>
      <p>{selected.summary}</p>
      <h3>What the radar shows</h3>
      <p>{selected.radarShows}</p>
      <h3>What we infer</h3>
      <p>{selected.weInfer}</p>
      {(human || natural) && (
        <>
          <h3>Possible drivers</h3>
          <ul>
            {human && <li>Human: {human}</li>}
            {natural && <li>Natural: {natural}</li>}
          </ul>
        </>
      )}
      {sources.length > 0 && (
        <>
          <h3>Sources</h3>
          <ul>
            {sources.map((source) => (
              <li key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title}</a></li>
            ))}
          </ul>
        </>
      )}
    </article>
  );
}
