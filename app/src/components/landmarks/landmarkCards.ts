// Monica's hand-written card text (content/landmarks/<region>.json, T-19), bundled at build time
// the same way the story files are, so it works on the static site without the API.
// Owner: Zainab (app/src/components/landmarks/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { Landmark, LandmarksFile, Source } from '../../types/manifest';

/** A hand-written card may leave fields out; those keep the published value. */
type Card = Partial<Landmark> & { id: string };
type CardFile = Omit<LandmarksFile, 'landmarks'> & { landmarks: Card[]; sources?: Source[] };

const files = import.meta.glob<CardFile>('../../../../content/landmarks/*.json', { eager: true, import: 'default' });

// The wider valley map shows the same 7 landmarks as Mexico City, so it uses the same card text
// (the tour does the same in story.ts). Without this, the valley showed the older copied text.
const CARD_ALIASES: Record<string, string> = { mexico_city_valley: 'mexico_city' };

/** The card file for a region, or undefined if Monica has not written one. */
export function cardsFor(regionId: string): CardFile | undefined {
  const own = Object.values(files).find((f) => f.regionId === regionId);
  if (own) return own;
  const alias = CARD_ALIASES[regionId];
  return alias ? Object.values(files).find((f) => f.regionId === alias) : undefined;
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
    // A field the card leaves out keeps the published value, so a partial card never blanks one.
    return {
      ...l,
      name: card.name ?? l.name,
      summary: card.summary ?? l.summary,
      radarShows: card.radarShows ?? l.radarShows,
      weInfer: card.weInfer ?? l.weInfer,
      drivers: card.drivers ?? l.drivers,
      sourceIds: card.sourceIds ?? l.sourceIds,
    };
  });
}
