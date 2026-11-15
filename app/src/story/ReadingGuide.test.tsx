// @vitest-environment jsdom
// T-23: the data badge, the explainer cards, and "Take the tour", against the real manifest.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { useAppStore } from '../state/store';
import type { Manifest } from '../types/manifest';
import ReadingGuide, { type ExplainersFile } from './ReadingGuide';

// Tests run from app/; jsdom's import.meta.url is not a file URL.
const fromApp = (rel: string) => readFileSync(resolve(process.cwd(), rel), 'utf8');
const manifest = JSON.parse(fromApp('public/data/mexico_city/manifest.json')) as Manifest;
const explainers = JSON.parse(fromApp('../content/explainers/cards.json')) as ExplainersFile;

let container: HTMLDivElement;
let root: Root;
const initial = useAppStore.getState();

beforeEach(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  useAppStore.setState({ ...initial, regionId: 'mexico_city', manifest });
  container = document.createElement('div');
  document.body.append(container);
  root = createRoot(container);
  act(() => root.render(<ReadingGuide />));
});
afterEach(() => {
  act(() => root.unmount());
  container.remove();
});

const button = (text: string) => {
  const b = [...container.querySelectorAll('button')].find((x) => x.textContent?.startsWith(text));
  if (!b) throw new Error(`no button "${text}"`);
  return b;
};

it('shows the data badge whenever data is loaded, with the label from the manifest', () => {
  expect(manifest.dataMaturity).toBe('PROVISIONAL');
  expect(container.querySelector('.data-badge')?.textContent).toContain('Provisional data');
});

it('labels a synthetic region as test data, never as provisional', () => {
  act(() => useAppStore.setState({ manifest: { ...manifest, dataMaturity: 'SYNTHETIC', synthetic: true } as Manifest }));
  expect(container.querySelector('.data-badge')?.textContent).toContain('Synthetic test data');
});

it('shows nothing before any data is loaded', () => {
  act(() => useAppStore.setState({ manifest: null }));
  expect(container.innerHTML).toBe('');
});

it('opens the explainer cards and closes on Escape', () => {
  act(() => button(explainers.title).click());
  const dialog = container.querySelector('[role="dialog"]');
  expect(dialog).not.toBeNull();
  const titles = [...dialog!.querySelectorAll('h2')].map((h) => h.textContent);
  expect(titles).toEqual(explainers.cards.map((c) => c.title));
  expect(dialog!.textContent).toContain('We infer:');
  act(() => window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })));
  expect(container.querySelector('[role="dialog"]')).toBeNull();
});

it('the badge opens the same explainer', () => {
  act(() => button('Provisional data').click());
  expect(container.querySelector('#explainer-provisional')).not.toBeNull();
});

it('"Take the tour" starts the tour and hides itself while it runs', () => {
  act(() => button('Take the tour').click());
  expect(useAppStore.getState().storyStep).toBe(0);
  expect([...container.querySelectorAll('button')].some((b) => b.textContent === 'Take the tour')).toBe(false);
});

describe('content/explainers/cards.json', () => {
  it('cites only sources it defines', () => {
    const known = new Set(explainers.sources.map((s) => s.id));
    const cited = [...explainers.badge.sourceIds, ...explainers.cards.flatMap((c) => c.sourceIds)];
    expect(cited.filter((id) => !known.has(id))).toEqual([]);
  });

  it('shows no flagged or unsourced placeholder text', () => {
    const shown = [explainers.title, explainers.badge.detail, ...explainers.cards.flatMap((c) => [c.title, ...c.body, c.weInfer ?? ''])];
    expect(shown.filter((t) => /NEEDS SOURCE|TODO|CHECK \(/.test(t))).toEqual([]);
  });

  it('keeps out the claims the memo says have no row', () => {
    const text = JSON.stringify(explainers).toLowerCase();
    for (const banned of ['through clouds', 'water looks dark', 'sunlight', '12 days']) expect(text).not.toContain(banned);
  });
});
