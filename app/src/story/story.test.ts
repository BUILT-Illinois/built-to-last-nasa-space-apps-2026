// Checks every tour in content/story/ against its region's real data, and the step resolver.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { LandmarksFile, Manifest } from '../types/manifest';
import { getStory, resolveStep, storyRegionIds, type StoryStep } from './story';

const repoFile = (rel: string) => new URL(`../../../${rel}`, import.meta.url);
const readJson = <T>(rel: string): T => JSON.parse(readFileSync(repoFile(rel), 'utf8')) as T;

describe('tours in content/story/', () => {
  it('include Mexico City and the wider valley', () => {
    expect(storyRegionIds()).toEqual(expect.arrayContaining(['mexico_city', 'mexico_city_valley']));
  });

  for (const regionId of storyRegionIds()) {
    describe(regionId, () => {
      const story = getStory(regionId)!;
      const manifest = readJson<Manifest>(`app/public/data/${regionId}/manifest.json`);

      it('has unique step ids', () => {
        const ids = story.steps.map((s) => s.id);
        expect(new Set(ids).size).toBe(ids.length);
      });

      it('names only layers and dates that exist in the manifest', () => {
        const problems = story.steps.flatMap((s) => resolveStep(s, manifest).problems);
        expect(problems).toEqual([]);
      });

      it('names only published landmarks for the active region', () => {
        const file = `app/public/data/${regionId}/landmarks.json`;
        const known = new Set(readJson<LandmarksFile>(file).landmarks.map((l) => l.id));
        const missing = story.steps.map((s) => s.set.landmark).filter((id) => id !== undefined && !known.has(id));
        expect(missing).toEqual([]);
      });

      it('cites only sources the story or the manifest defines', () => {
        const known = new Set([...story.sources, ...manifest.sources].map((s) => s.id));
        const cited = [...story.intro.sourceIds, ...story.steps.flatMap((s) => s.sourceIds)];
        expect(cited.filter((id) => !known.has(id))).toEqual([]);
      });

      it('shows no flagged claims (they belong in pendingClaims)', () => {
        const shown = [story.intro.title, story.intro.tagline, ...story.intro.body, ...story.steps.flatMap((s) => [s.title, ...s.body])];
        expect(shown.filter((t) => /NEEDS SOURCE|TODO|CHECK \(/.test(t))).toEqual([]);
      });
    });
  }
});

describe('resolveStep', () => {
  const manifest = {
    layers: [
      { id: 'a', frames: [{ date: '2026-01-01' }, { date: '2026-02-01' }] },
      { id: 'b', frames: [{ date: '2026-02-01' }] },
    ],
    sources: [],
  } as unknown as Manifest;
  const step = (set: StoryStep['set']): StoryStep => ({
    id: 't',
    title: '',
    body: [],
    set,
    camera: { center: [0, 0], zoom: 5 },
    sourceIds: [],
  });

  it('turns dates into frame indexes and clears the swipe when none is named', () => {
    const { view, problems } = resolveStep(step({ layer: 'a', date: '2026-02-01' }), manifest);
    expect(problems).toEqual([]);
    expect(view).toMatchObject({
      activeLayerId: 'a',
      dateIndex: 1,
      compareLayerId: null,
      compareDateIndex: null,
      selectedLandmarkId: null,
    });
  });

  it('sets the swipe and the landmark', () => {
    const { view } = resolveStep(
      step({ layer: 'a', date: '2026-01-01', compareLayer: 'b', compareDate: '2026-02-01', landmark: 'x' }),
      manifest,
    );
    expect(view).toMatchObject({ compareLayerId: 'b', compareDateIndex: 0, selectedLandmarkId: 'x' });
  });

  it('reports a missing date or layer instead of guessing, and leaves that part of the view alone', () => {
    const { view, problems } = resolveStep(
      step({ layer: 'a', date: '2025-10-30', compareLayer: 'zzz', compareDate: '2026-02-01' }),
      manifest,
    );
    expect(problems).toHaveLength(2);
    expect(view).not.toHaveProperty('activeLayerId');
    expect(view).not.toHaveProperty('compareLayerId');
  });
});
