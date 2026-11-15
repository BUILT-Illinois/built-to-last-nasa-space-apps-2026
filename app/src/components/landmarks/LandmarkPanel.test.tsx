// @vitest-environment jsdom
// Tests for the T-14 landmark panel, run against the real sample and mexico_city files and
// Monica's card text in content/landmarks/.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, expect, it } from 'vitest';
import { useAppStore } from '../../state/store';
import type { LandmarksFile, Manifest } from '../../types/manifest';
import LandmarkPanel from './LandmarkPanel';

const readData = <T,>(region: string, file: string): T =>
  JSON.parse(readFileSync(resolve(__dirname, `../../../public/data/${region}/${file}`), 'utf8'));

let container: HTMLDivElement;
let root: Root;

beforeEach(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  container = document.createElement('div');
  root = createRoot(container);
});
afterEach(() => act(() => root.unmount()));

/** Put a region's published data in the store, as loadRegion would, and render the panel. */
function show(region: string, landmarks = readData<LandmarksFile>(region, 'landmarks.json').landmarks) {
  useAppStore.setState({
    regionId: region,
    manifest: readData<Manifest>(region, 'manifest.json'),
    landmarks,
    selectedLandmarkId: null,
    cameraRequest: null,
    loadStatus: 'ready',
  });
  act(() => root.render(<LandmarkPanel />));
}

const names = () => [...container.querySelectorAll('.landmark-list button')].map((b) => b.textContent);
const click = (name: string) =>
  act(() => [...container.querySelectorAll<HTMLButtonElement>('.landmark-list button')].find((b) => b.textContent === name)!.click());

it('sample: lists both landmarks', () => {
  show('sample');
  expect(names()).toEqual(['Placeholder landmark A', 'Placeholder landmark B']);
});

it("mexico_city: lists Monica's 7 cards", () => {
  show('mexico_city');
  expect(names()).toEqual([
    'New Lake Chalco (Lago de Tláhuac-Xico)',
    'Tláhuac',
    'Nezahualcóyotl',
    'Benito Juárez International Airport',
    'Centro Histórico',
    'Ángel de la Independencia',
    'Chalco',
  ]);
});

it("mexico_city: the card shows Monica's text, not the pipeline placeholder", () => {
  show('mexico_city');
  click('Tláhuac');
  expect(container.querySelector('.landmark-radar')?.textContent).toContain('about 16.4 cm away from the satellite');
  expect(container.querySelector('.landmark-infer')?.textContent).toContain('still sinking quickly');
  expect(container.textContent).not.toContain('Monthly radar backscatter sampling point');
});

it('a region with no landmarks shows a clean empty state', () => {
  show('mexico_city', []);
  expect(container.textContent).toContain('No landmarks for this region yet.');
  expect(container.querySelector('.landmark-list')).toBeNull();
});

it('clicking a landmark selects it, flies to it, and keeps "radar shows" and "we infer" separate', () => {
  show('sample');
  click('Placeholder landmark A');

  const state = useAppStore.getState();
  expect(state.selectedLandmarkId).toBe('placeholder_a');
  expect(state.cameraRequest?.center).toEqual([-99.072, 19.436]);
  expect(container.querySelector('.landmark-radar')?.textContent).toContain('what the data shows here');
  expect(container.querySelector('.landmark-infer')?.textContent).toContain('worded as a hypothesis');
});

it('a selection made elsewhere (the map) opens the same card', () => {
  show('sample');
  act(() => useAppStore.getState().selectLandmark('placeholder_b'));
  expect(container.querySelector('.landmark-card h3')?.textContent).toBe('Placeholder landmark B');
});

it('before the first load starts (idle), shows loading, not the empty state', () => {
  useAppStore.setState({ landmarks: [], loadStatus: 'idle' });
  act(() => root.render(<LandmarkPanel />));
  expect(container.textContent).toContain('Loading landmarks');
  expect(container.textContent).not.toContain('No landmarks for this region yet.');
});

it('the Landmarks heading collapses and reopens the list', () => {
  show('sample');
  const toggle = container.querySelector<HTMLButtonElement>('.landmark-toggle')!;
  expect(toggle.textContent).toContain('Landmarks (2)');
  act(() => toggle.click());
  expect(container.querySelector('.landmark-list')).toBeNull();
  act(() => toggle.click());
  expect(names()).toHaveLength(2);
});
