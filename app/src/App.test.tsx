// @vitest-environment jsdom
// Regression test: one region change must start exactly one load (PR #2 review, blocker).
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { flush, stubFetch, type PendingFetch } from './test/fetchMock';

vi.mock('./map/MapView', () => ({ default: () => null })); // no WebGL in tests

let calls: PendingFetch[];
beforeEach(() => {
  vi.resetModules();
  calls = stubFetch();
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
});
afterEach(() => vi.unstubAllGlobals());

it('loading region B from outside the App starts one manifest request, not two', async () => {
  const { default: App } = await import('./App');
  const { useAppStore } = await import('./state/store');
  const root = createRoot(document.createElement('div'));
  await act(async () => root.render(<App />));

  await act(async () => {
    void useAppStore.getState().loadRegion('b');
    await flush();
  });

  const bRequests = calls.filter((c) => c.url.endsWith('/data/b/manifest.json'));
  expect(bRequests).toHaveLength(1);
  act(() => root.unmount());
});
