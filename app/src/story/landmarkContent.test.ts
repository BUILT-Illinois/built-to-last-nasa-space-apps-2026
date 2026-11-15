// The hand-written cards in content/landmarks/ cite only sources that the card file lists or the
// region manifest already has. build_manifest.py validates the same thing in the pipeline.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { readdirSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { LandmarksFile, Manifest, Source } from '../types/manifest';

const repo = (rel: string) => new URL(`../../../${rel}`, import.meta.url);
const read = <T>(rel: string): T => JSON.parse(readFileSync(repo(rel), 'utf8')) as T;
type CardFile = LandmarksFile & { sources?: Source[] };

for (const file of readdirSync(repo('content/landmarks/')).filter((f) => f.endsWith('.json'))) {
  describe(`content/landmarks/${file}`, () => {
    const cards = read<CardFile>(`content/landmarks/${file}`);
    const manifest = read<Manifest>(`app/public/data/${cards.regionId}/manifest.json`);

    it('cites only sources it lists or the manifest has', () => {
      const known = new Set([...(cards.sources ?? []), ...manifest.sources].map((s) => s.id));
      const cited = cards.landmarks.flatMap((l) => l.sourceIds);
      expect(cited.filter((id) => !known.has(id))).toEqual([]);
    });

    it('gives every listed source an id, title, url and license', () => {
      for (const s of cards.sources ?? []) expect(s.id && s.title && s.url && s.license).toBeTruthy();
    });

    it('agrees with the manifest on any source both list', () => {
      for (const s of cards.sources ?? []) {
        const m = manifest.sources.find((x) => x.id === s.id);
        if (m) expect(s).toEqual(m);
      }
    });
  });
}
