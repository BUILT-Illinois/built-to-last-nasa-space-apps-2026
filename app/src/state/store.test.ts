// Regression tests for region loading (PR #2 review, blocker). Drafted with AI assistance
// (Claude Code), see docs/AI_USAGE.md.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { flush, manifestFor, stubFetch, type PendingFetch } from '../test/fetchMock';

let useAppStore: typeof import('./store').useAppStore;
let calls: PendingFetch[];

beforeEach(async () => {
  vi.resetModules(); // fresh store per test
  calls = stubFetch();
  ({ useAppStore } = await import('./store'));
});
afterEach(() => vi.unstubAllGlobals());

const manifestCall = (regionId: string, nth = 0) =>
  calls.filter((c) => c.url.endsWith(`/data/${regionId}/manifest.json`))[nth]!;
const landmarksCall = (regionId: string, nth = 0) =>
  calls.filter((c) => c.url.endsWith(`/data/${regionId}/landmarks.json`))[nth]!;

describe('loadRegion', () => {
  it('A then B then A: a slow first A response does not replace the latest A', async () => {
    const { loadRegion } = useAppStore.getState();
    const first = loadRegion('a');
    void loadRegion('b');
    const latest = loadRegion('a');

    // The latest A request answers first...
    await manifestCall('a', 1).json(manifestFor('a', 'latest'));
    await landmarksCall('a', 0).json({ schemaVersion: '0.1', regionId: 'a', landmarks: [] });
    await latest;
    // ...then the stale first A request answers.
    await manifestCall('a', 0).json(manifestFor('a', 'stale'));
    await flush();
    await landmarksCall('a', 1)?.json({ schemaVersion: '0.1', regionId: 'a', landmarks: [] });
    await first;

    expect(useAppStore.getState().manifest?.generatedAt).toBe('latest');
  });

  it('A loaded, then B fails: the store never reports B while showing A data', async () => {
    const { loadRegion } = useAppStore.getState();
    const a = loadRegion('a');
    await manifestCall('a').json(manifestFor('a', 'a'));
    await landmarksCall('a').json({ schemaVersion: '0.1', regionId: 'a', landmarks: [] });
    await a;

    const b = loadRegion('b');
    await manifestCall('b').fail(404);
    await b;

    const s = useAppStore.getState();
    expect(s.loadStatus).toBe('error');
    // Whatever region the store says is shown must match the data it holds.
    expect(s.manifest === null || s.manifest.region.id === s.regionId).toBe(true);
    // A stays on screen and the error names B.
    expect(s.regionId).toBe('a');
    expect(s.manifest?.region.id).toBe('a');
    expect(s.loadingRegionId).toBeNull();
    expect(s.loadError).toContain('"b"');
  });

  it('region and data change together: A stays until B has fully arrived', async () => {
    const { loadRegion } = useAppStore.getState();
    const a = loadRegion('a');
    await manifestCall('a').json(manifestFor('a', 'a'));
    await landmarksCall('a').json({ schemaVersion: '0.1', regionId: 'a', landmarks: [] });
    await a;

    const b = loadRegion('b');
    expect(useAppStore.getState()).toMatchObject({ regionId: 'a', loadingRegionId: 'b', loadStatus: 'loading' });
    await manifestCall('b').json(manifestFor('b', 'b'));
    expect(useAppStore.getState().regionId).toBe('a'); // landmarks for B still pending
    await landmarksCall('b').json({ schemaVersion: '0.1', regionId: 'b', landmarks: [] });
    await b;

    const s = useAppStore.getState();
    expect(s).toMatchObject({ regionId: 'b', loadingRegionId: null, loadStatus: 'ready', loadError: null });
    expect(s.manifest?.region.id).toBe('b');
  });

  it('a stale failure arriving late does not overwrite a newer success', async () => {
    const { loadRegion } = useAppStore.getState();
    const a = loadRegion('a');
    const b = loadRegion('b');
    await manifestCall('b').json(manifestFor('b', 'b'));
    await landmarksCall('b').json({ schemaVersion: '0.1', regionId: 'b', landmarks: [] });
    await b;
    await manifestCall('a').fail(500);
    await a;

    expect(useAppStore.getState()).toMatchObject({ regionId: 'b', loadStatus: 'ready', loadError: null });
  });
});
