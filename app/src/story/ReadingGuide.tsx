// "How to read this map" (T-23): the data badge, which is always on screen over the map, and the
// explainer cards from content/explainers/cards.json (polarization, radar shows vs. we infer,
// provisional data). Also holds the "Take the tour" button once the tour is closed.
// Reads and writes only the shared store. Owner: Monica (app/src/story/).
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect, useRef, useState } from 'react';
import { useAppStore } from '../state/store';
import ProvisionalBadge from './ProvisionalBadge';
import '../styles/story.css';

type Source = { id: string; title: string; url: string };
type ExplainerCard = { id: string; title: string; body: string[]; weInfer?: string; sourceIds: string[] };
export type ExplainersFile = {
  schemaVersion: string;
  title: string;
  badge: { detail: string; sourceIds: string[] };
  cards: ExplainerCard[];
  sources: Source[];
};

// Loaded like the story files (tsconfig has no resolveJsonModule).
const files = import.meta.glob<ExplainersFile>('../../../content/explainers/cards.json', {
  eager: true,
  import: 'default',
});
const explainers = Object.values(files)[0]!;

function SourceLine({ ids }: { ids: string[] }) {
  const sources = ids.flatMap((id) => explainers.sources.filter((s) => s.id === id));
  if (sources.length === 0) return null;
  return (
    <p className="story-sources">
      Sources:{' '}
      {sources.map((s, i) => (
        <span key={s.id}>
          {i > 0 && '; '}
          {s.url ? (
            <a href={s.url} target="_blank" rel="noreferrer">
              {s.title}
            </a>
          ) : (
            s.title
          )}
        </span>
      ))}
    </p>
  );
}

export default function ReadingGuide() {
  const hasData = useAppStore((s) => s.manifest !== null);
  const inTour = useAppStore((s) => s.storyStep !== null);
  const [open, setOpen] = useState<string | null>(null); // id of the card to scroll to, or null
  const headingRef = useRef<HTMLHeadingElement>(null);
  const openerRef = useRef<HTMLElement | null>(null);

  const show = (cardId: string) => {
    openerRef.current = document.activeElement as HTMLElement | null;
    setOpen(cardId);
  };
  const close = () => {
    setOpen(null);
    openerRef.current?.focus();
  };

  useEffect(() => {
    if (open === null) return;
    headingRef.current?.focus();
    document.getElementById(`explainer-${open}`)?.scrollIntoView?.({ block: 'nearest' });
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(null);
        openerRef.current?.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open]);

  if (!hasData) return null;

  return (
    <>
      <div className="reading-guide">
        <ProvisionalBadge onClick={() => show('provisional')} title={explainers.badge.detail} />
        <button type="button" className="story-btn reading-guide__btn" onClick={() => show('polarization')}>
          {explainers.title}
        </button>
        {!inTour && (
          <button
            type="button"
            className="story-btn reading-guide__btn"
            onClick={() => useAppStore.getState().setStoryStep(0)}
          >
            Take the tour
          </button>
        )}
      </div>

      {open !== null && (
        <div className="story-backdrop" onClick={close}>
          <section
            className="story-intro explainer"
            role="dialog"
            aria-modal="true"
            aria-labelledby="explainer-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="story-card-head">
              <h1 id="explainer-title" ref={headingRef} tabIndex={-1}>
                {explainers.title}
              </h1>
              <button type="button" className="story-exit" onClick={close}>
                Close
              </button>
            </div>
            {explainers.cards.map((c) => (
              <article key={c.id} id={`explainer-${c.id}`} className="explainer-card">
                <h2>{c.title}</h2>
                {c.body.map((p) => (
                  <p key={p}>{p}</p>
                ))}
                {c.weInfer && (
                  <p>
                    <em>We infer:</em> {c.weInfer}
                  </p>
                )}
                <SourceLine ids={c.sourceIds} />
              </article>
            ))}
          </section>
        </div>
      )}
    </>
  );
}
