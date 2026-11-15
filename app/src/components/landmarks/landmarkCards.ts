// Monica's hand-written card text (content/landmarks/<region>.json, T-19), bundled at build time
// the same way the story files are, so it works on the static site without the API.
// Owner: Zainab (app/src/components/landmarks/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { Landmark, LandmarksFile, Source } from '../../types/manifest';

type CardFile = LandmarksFile & { sources?: Source[] };

const files = import.meta.glob<CardFile>('../../../../content/landmarks/*.json', { eager: true, import: 'default' });

/** The card file for a region, or undefined if Monica has not written one. */
export function cardsFor(regionId: string): CardFile | undefined {
  return Object.values(files).find((f) => f.regionId === regionId);
}

/**
 * Published landmarks with the card text laid over them, matched by id.
 * Text comes from the card; position and series stay from the published file.
 */
export function withCardText(landmarks: Landmark[], cards: CardFile | undefined): Landmark[] {
  if (!cards) return landmarks;
  return landmarks.map((l) => {
    const card = cards.landmarks.find((c) => c.id === l.id);
    if (!card) return l;
    const { name, summary, radarShows, weInfer, drivers, sourceIds } = card;
    return { ...l, name, summary, radarShows, weInfer, drivers, sourceIds };
  });
}
