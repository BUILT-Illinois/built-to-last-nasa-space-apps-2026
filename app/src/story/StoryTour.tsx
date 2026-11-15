// Intro screen and guided walkthrough (T-18), driven by content/story/<region>.json.
// Reads and writes only the shared store; the map reacts to it. Owner: Monica (app/src/story/).
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect, useRef, useState } from 'react';
import { useAppStore } from '../state/store';
import ProvisionalBadge from './ProvisionalBadge';
import { findSources, getStory, resolveStep, type StorySource } from './story';
import '../styles/story.css';

function SourceLinks({ sources }: { sources: StorySource[] }) {
  return (
    <>
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
    </>
  );
}

/**
 * The sources line. On a tour step it starts folded ("Sources (3)"), so the card stays short
 * enough not to hide the swipe it asks people to compare; one tap opens it.
 */
function Sources({ sources, folded = false }: { sources: StorySource[]; folded?: boolean }) {
  if (sources.length === 0) return null;
  if (folded) {
    return (
      <details className="story-sources">
        <summary>Sources ({sources.length})</summary>
        <SourceLinks sources={sources} />
      </details>
    );
  }
  return (
    <p className="story-sources">
      Sources: <SourceLinks sources={sources} />
    </p>
  );
}

export default function StoryTour() {
  const regionId = useAppStore((s) => s.regionId);
  const manifest = useAppStore((s) => s.manifest);
  const storyStep = useAppStore((s) => s.storyStep);
  const story = getStory(regionId);
  const [introOpen, setIntroOpen] = useState(true);
  const headingRef = useRef<HTMLHeadingElement>(null);
  const startRef = useRef<HTMLButtonElement>(null);

  const step = story && storyStep !== null ? story.steps[storyStep] : undefined;

  // Apply the current step once the manifest is loaded (the visitor may press Start before it is).
  useEffect(() => {
    if (!step || !manifest) return;
    const { view, problems } = resolveStep(step, manifest);
    for (const p of problems) console.warn(`[story] ${p}`);
    const store = useAppStore.getState();
    store.applyPartial(view);
    store.flyTo(step.camera.center, step.camera.zoom);
  }, [step, manifest]);

  // Keyboard and screen-reader users land on the new content.
  useEffect(() => {
    if (step) headingRef.current?.focus();
  }, [step]);
  useEffect(() => {
    if (introOpen) startRef.current?.focus();
  }, [introOpen]);

  const exploreFreely = () => {
    setIntroOpen(false);
    useAppStore.getState().setStoryStep(null);
  };
  const goTo = (i: number) => {
    setIntroOpen(false);
    useAppStore.getState().setStoryStep(i);
  };

  // Escape leaves the intro or the tour.
  useEffect(() => {
    if (!introOpen && !step) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return;
      setIntroOpen(false);
      useAppStore.getState().setStoryStep(null);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [introOpen, step]);

  if (!story || story.steps.length === 0) return null;

  if (introOpen) {
    const { intro } = story;
    return (
      <div className="story-backdrop">
        <section className="story-intro" role="dialog" aria-modal="true" aria-labelledby="story-intro-title">
          <h1 id="story-intro-title">{intro.title}</h1>
          <p className="story-tagline">{intro.tagline}</p>
          {intro.body.map((p) => (
            <p key={p}>{p}</p>
          ))}
          <div className="story-actions">
            <button ref={startRef} type="button" className="story-btn story-btn-primary" onClick={() => goTo(0)}>
              {intro.startLabel}
            </button>
            <button type="button" className="story-btn" onClick={exploreFreely}>
              {intro.exploreLabel}
            </button>
          </div>
          <Sources sources={findSources(story, manifest, intro.sourceIds)} />
        </section>
      </div>
    );
  }

  // Outside the tour, ReadingGuide shows the "Take the tour" button.
  if (!step || storyStep === null) return null;

  const isLast = storyStep === story.steps.length - 1;
  return (
    <section className="story-card" aria-labelledby="story-step-title">
      <div className="story-card-head">
        <p className="story-count" aria-live="polite">
          Step {storyStep + 1} of {story.steps.length}
        </p>
        {/* On phones this card covers the map's badge, so it carries its own. */}
        <ProvisionalBadge />
        <button type="button" className="story-exit" onClick={exploreFreely}>
          Exit tour
        </button>
      </div>
      <h2 id="story-step-title" ref={headingRef} tabIndex={-1}>
        {step.title}
      </h2>
      {step.body.map((p) => (
        <p key={p}>{p}</p>
      ))}
      <Sources sources={findSources(story, manifest, step.sourceIds)} folded />
      <div className="story-actions">
        <button type="button" className="story-btn" onClick={() => goTo(storyStep - 1)} disabled={storyStep === 0}>
          Back
        </button>
        {isLast ? (
          <button type="button" className="story-btn story-btn-primary" onClick={exploreFreely}>
            {story.intro.exploreLabel}
          </button>
        ) : (
          <button type="button" className="story-btn story-btn-primary" onClick={() => goTo(storyStep + 1)}>
            Next
          </button>
        )}
      </div>
    </section>
  );
}
