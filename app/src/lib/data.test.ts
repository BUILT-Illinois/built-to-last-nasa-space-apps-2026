// @vitest-environment jsdom
// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createElement, act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, expect, it, vi } from 'vitest';

vi.mock('../map/MapView', () => ({ default: () => null })); // WebGL is outside this test.

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
  vi.resetModules();
});

it('starts with the published Mexico City region using static files and no API', async () => {
  vi.stubEnv('VITE_REGION_ID', 'mexico_city');
  vi.stubGlobal('IS_REACT_ACT_ENVIRONMENT', true);
  const manifestPath = '/data/mexico_city/manifest.json';
  const landmarksPath = '/data/mexico_city/landmarks.json';
  const fetchStatic = vi.fn(async (path: string) => {
    if (path !== manifestPath && path !== landmarksPath) return new Response(null, { status: 404 });
    return new Response(readFileSync(resolve('public', `.${path}`), 'utf8'), {
      headers: { 'Content-Type': 'application/json' },
    });
  });
  vi.stubGlobal('fetch', fetchStatic);

  const { default: App } = await import('../App');
  const { useAppStore } = await import('../state/store');
  const root = createRoot(document.createElement('div'));
  try {
    await act(async () => root.render(createElement(App)));
    expect(fetchStatic.mock.calls).toEqual([[manifestPath], [landmarksPath]]);
    const state = useAppStore.getState();
    expect(state.loadError).toBeNull();
    expect(state.manifest?.region.id).toBe('mexico_city');
    expect(state.manifest?.layers.length).toBeGreaterThan(0);
    expect(state.landmarks).toEqual(JSON.parse(
      readFileSync(resolve('public', `.${landmarksPath}`), 'utf8'),
    ).landmarks);
  } finally {
    act(() => root.unmount());
  }
});
