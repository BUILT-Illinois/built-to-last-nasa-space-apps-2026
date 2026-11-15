// @vitest-environment jsdom
// The intro screen and tour against the real Mexico City manifest (T-18).
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, expect, it } from 'vitest';
import { useAppStore } from '../state/store';
import type { Manifest } from '../types/manifest';
import { getStory } from './story';
import StoryTour from './StoryTour';

const manifest = JSON.parse(
  // Tests run from app/; jsdom's import.meta.url is not a file URL.
  readFileSync(resolve(process.cwd(), 'public/data/mexico_city/manifest.json'), 'utf8'),
) as Manifest;
const story = getStory('mexico_city')!;
const frameDate = (layerId: string, i: number | null) =>
  i === null ? null : manifest.layers.find((l) => l.id === layerId)!.frames[i]!.date;

let container: HTMLDivElement;
let root: Root;
const initial = useAppStore.getState();

beforeEach(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  useAppStore.setState({ ...initial, regionId: 'mexico_city', manifest, activeLayerId: manifest.layers[0]!.id });
  container = document.createElement('div');
  document.body.append(container);
  root = createRoot(container);
  act(() => root.render(<StoryTour />));
});
afterEach(() => {
  act(() => root.unmount());
  container.remove();
});

const button = (label: string) => {
  const b = [...container.querySelectorAll('button')].find((x) => x.textContent === label);
  if (!b) throw new Error(`no button "${label}"`);
  return b;
};
const click = (label: string) => act(() => button(label).click());
const heading = () => container.querySelector('h2')?.textContent;

it('opens on the intro screen with both choices', () => {
  expect(container.querySelector('h1')?.textContent).toBe(story.intro.title);
  expect(button(story.intro.startLabel)).toBeTruthy();
  expect(button(story.intro.exploreLabel)).toBeTruthy();
  expect(useAppStore.getState().storyStep).toBeNull();
});

it('start applies step 1: layer, date, camera, landmark', () => {
  click(story.intro.startLabel);
  const s = useAppStore.getState();
  const first = story.steps[0]!;
  expect(s.storyStep).toBe(0);
  expect(heading()).toBe(first.title);
  expect(s.activeLayerId).toBe(first.set.layer);
  expect(frameDate(s.activeLayerId, s.dateIndex)).toBe(first.set.date);
  expect(s.cameraRequest).toMatchObject(first.camera);
  expect(s.selectedLandmarkId).toBe(first.set.landmark ?? null);
});

it('next and back walk the steps and set up the swipe a step names', () => {
  click(story.intro.startLabel);
  const swipeIndex = story.steps.findIndex((s) => s.set.compareLayer);
  for (let i = 0; i < swipeIndex; i++) click('Next');
  const s = useAppStore.getState();
  const step = story.steps[swipeIndex]!;
  expect(heading()).toBe(step.title);
  expect(s.compareLayerId).toBe(step.set.compareLayer);
  expect(frameDate(s.compareLayerId!, s.compareDateIndex)).toBe(step.set.compareDate);

  click('Back');
  expect(useAppStore.getState().storyStep).toBe(swipeIndex - 1);
  expect(useAppStore.getState().compareLayerId).toBe(story.steps[swipeIndex - 1]!.set.compareLayer ?? null);
});

it('the last step ends in free exploration', () => {
  click(story.intro.startLabel);
  for (let i = 1; i < story.steps.length; i++) click('Next');
  expect(container.textContent).toContain(`Step ${story.steps.length} of ${story.steps.length}`);
  click(story.intro.exploreLabel);
  expect(useAppStore.getState().storyStep).toBeNull();
  expect(container.querySelector('.story-card')).toBeNull();
});

it('"explore freely" on the intro skips the tour and leaves the view alone', () => {
  click(story.intro.exploreLabel);
  expect(useAppStore.getState().storyStep).toBeNull();
  expect(useAppStore.getState().cameraRequest).toBeNull();
  expect(container.querySelector('.story-intro')).toBeNull();
});

it('Escape exits the tour, and restarting from the store opens step 1', () => {
  click(story.intro.startLabel);
  click('Next');
  act(() => window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })));
  expect(useAppStore.getState().storyStep).toBeNull();
  act(() => useAppStore.getState().setStoryStep(0)); // what ReadingGuide's "Take the tour" does
  expect(heading()).toBe(story.steps[0]!.title);
});

it('the tour card carries the data badge (on phones it covers the map badge)', () => {
  click(story.intro.startLabel);
  expect(container.querySelector('.story-card .data-badge')?.textContent).toBe('Provisional data');
});

it('renders nothing for a region without a tour', () => {
  act(() => useAppStore.setState({ regionId: 'no_such_region' }));
  expect(container.innerHTML).toBe('');
});

it('folds a step card\'s sources so the card stays short over the swipe', () => {
  click(story.intro.startLabel);
  const details = container.querySelector('.story-card details.story-sources') as HTMLDetailsElement | null;
  expect(details).not.toBeNull();
  expect(details!.open).toBe(false);
  expect(details!.querySelector('summary')?.textContent).toMatch(/^Sources \(\d+\)$/);
  act(() => details!.querySelector('summary')!.click());
  expect(details!.open).toBe(true);
  expect(details!.querySelectorAll('a').length).toBeGreaterThan(0);
});
