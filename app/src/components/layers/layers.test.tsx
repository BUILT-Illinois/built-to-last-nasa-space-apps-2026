// @vitest-environment jsdom
// Tests for the layer switcher and legend (T-12). Fixtures: the sample manifest (Zainab) and the
// synthetic sinking manifest written by `pipeline/ingest_sinking.py --synthetic` (Elias, PR #24).
// Owner: Diego (app/src/components/layers/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import sampleJson from '../../../public/data/sample/manifest.json';
import sinkingJson from './fixtures/sinking-synthetic.manifest.json';
import { useAppStore } from '../../state/store';
import type { Layer, Manifest } from '../../types/manifest';
import LayerSwitcher from './LayerSwitcher';
import Legend from './Legend';

const sample = sampleJson as unknown as Manifest;
const sinkingLayer = (sinkingJson as unknown as Manifest).layers[0] as Layer;

/** The sample manifest plus the synthetic sinking layer, as the real bundle will look after T-33. */
const withSinking: Manifest = { ...sample, layers: [...sample.layers, sinkingLayer] };

/** The flood-priority layer exactly as pipeline/build_flood_priority.py (PR #20) writes it. */
const floodLayer = {
  id: 'flood_priority',
  title: 'Flood-prevention priority',
  kind: 'priority',
  product: 'GCOV+GUNW',
  polarization: null,
  units: 'index (0–1)',
  bounds: [-99.4, 19.1, -98.85, 19.65],
  colormap: { name: 'gray', min: 0, max: 1 },
  description: 'Screening index for where to investigate flood-prevention investment first.',
  caveats: ['This screening index does not predict flooding. It excludes drainage capacity, rainfall and exposure.'],
  frames: [
    { date: '2026-10-13', image: 'layers/flood_priority/2026-10-13.webp', granules: ['A', 'B'], track: 19, frame: 11, direction: 'ASCENDING' },
  ],
} as unknown as Layer;

const initialState = useAppStore.getState();
let container: HTMLDivElement;
let root: Root;
let consoleError: ReturnType<typeof vi.spyOn>;
let consoleWarn: ReturnType<typeof vi.spyOn>;

/** Put a manifest in the store the way loadRegion does, without any network. */
function load(manifest: Manifest, activeLayerId = manifest.layers[0]?.id ?? '') {
  act(() => useAppStore.setState({ manifest, activeLayerId, dateIndex: 0, loadStatus: 'ready' }));
}

function render(ui: React.ReactNode) {
  act(() => root.render(ui));
}

const text = () => container.textContent ?? '';
const radios = () => [...container.querySelectorAll<HTMLInputElement>('input[type="radio"]')];

beforeEach(() => {
  (globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean }).IS_REACT_ACT_ENVIRONMENT = true;
  useAppStore.setState(initialState, true);
  container = document.createElement('div');
  document.body.append(container);
  root = createRoot(container);
  consoleError = vi.spyOn(console, 'error').mockImplementation(() => {});
  consoleWarn = vi.spyOn(console, 'warn').mockImplementation(() => {});
});

afterEach(() => {
  act(() => root.unmount());
  container.remove();
  // Every test doubles as a "no console errors or warnings" check.
  expect(consoleError).not.toHaveBeenCalled();
  expect(consoleWarn).not.toHaveBeenCalled();
  vi.restoreAllMocks();
});

describe('LayerSwitcher', () => {
  it('renders nothing before a load starts, and a short text while loading', () => {
    render(<LayerSwitcher />);
    expect(text()).toBe('');
    act(() => useAppStore.setState({ loadStatus: 'loading' }));
    expect(text()).toBe('Loading layers…');
  });

  it('lists every layer in the manifest by title and marks the active one', () => {
    load(sample);
    render(<LayerSwitcher />);
    const labels = [...container.querySelectorAll('label')].map((l) => l.textContent);
    expect(labels).toEqual(sample.layers.map((l) => l.title));
    expect(radios().map((r) => r.checked)).toEqual([true, false, false]);
  });

  it('calls setLayer with the clicked layer id', () => {
    const setLayer = vi.fn();
    load(sample);
    act(() => useAppStore.setState({ setLayer }));
    render(<LayerSwitcher />);
    act(() => radios()[1]?.click());
    expect(setLayer).toHaveBeenCalledExactlyOnceWith('gcov_hv');
  });

  it('follows the store when the active layer changes', () => {
    load(sample);
    render(<LayerSwitcher />);
    act(() => radios()[2]?.click());
    expect(useAppStore.getState().activeLayerId).toBe('gcov_composite');
    expect(radios().map((r) => r.checked)).toEqual([false, false, true]);
  });

  it('has no ground-motion entry when the manifest has no sinking layer', () => {
    load(sample);
    render(<LayerSwitcher />);
    expect(radios().map((r) => r.value)).toEqual(['gcov_hh', 'gcov_hv', 'gcov_composite']);
  });

  it('lists the ground-motion layer by its manifest title when present', () => {
    load(withSinking);
    render(<LayerSwitcher />);
    expect(radios().map((r) => r.value)).toContain('sinking');
    expect(text()).toContain('Ground motion along the radar line of sight');
  });
});

describe('Legend', () => {
  it('renders nothing without a manifest, or when the active layer is not in it', () => {
    render(<Legend />);
    expect(text()).toBe('');
    load(sample, 'sinking');
    expect(text()).toBe('');
  });

  it('shows title, units, min, max, description, caveats and the data-maturity note', () => {
    load({ ...sample, dataMaturity: 'PROVISIONAL', synthetic: false });
    render(<Legend />);
    expect(container.querySelector('h2')?.textContent).toBe('Radar brightness, HH, dB');
    expect(container.querySelector('.legend__range')?.textContent).toBe('-250');
    expect(text()).not.toMatch(/[≤≥]/); // brightness limits are not capped values
    expect(container.querySelector('.legend__ramp')).not.toBeNull();
    expect(text()).toContain('PROVISIONAL data');
    expect(text()).not.toContain('Synthetic test data');
    expect(text()).toContain('Generated test pattern, not NISAR data.');
    expect(text()).toContain('Synthetic placeholder images, not NISAR data.');
    expect(text()).toContain('Source: NISAR GCOV (NASA/ISRO).');
  });

  it('shows a synthetic note when the manifest says synthetic', () => {
    load(sample);
    render(<Legend />);
    expect(text()).toContain('SYNTHETIC data');
    expect(text()).toContain('Synthetic test data');
  });

  it('does not credit NISAR as the source when the manifest is synthetic', () => {
    // The sample manifest lists a NISAR GCOV source even though its images are generated.
    expect(sample.synthetic).toBe(true);
    expect(sample.sources.some((s) => s.title.includes('NISAR'))).toBe(true);
    load(sample);
    render(<Legend />);
    expect(text()).toContain('Generated test pattern, not NISAR data.');
    expect(text()).toContain('Source: generated test data, not NISAR.');
    expect(text()).not.toContain('Source: NISAR');
    expect(text()).not.toContain('NASA/ISRO');
  });

  it('rounds long real-data limits and shows no ramp for a colormap without one', () => {
    const first = sample.layers[0] as Layer;
    load({ ...sample, layers: [{ ...first, colormap: { name: 'rgb', min: -12.965582618713379, max: 4.076268119812003 } }] });
    render(<Legend />);
    expect(container.querySelector('.legend__range')?.textContent).toBe('-134.1');
    expect(container.querySelector('.legend__ramp')).toBeNull();
  });

  it('labels ground motion as line of sight, with sign, reference area and source', () => {
    load({ ...withSinking, synthetic: false }, 'sinking');
    render(<Legend />);
    expect(container.querySelector('h2')?.textContent).toBe('Radar line-of-sight rate, cm/yr');
    // Rates beyond the range are capped by the pipeline, so the ends read "or beyond".
    const ends = [...container.querySelectorAll('.legend__range span')].map((el) => el.textContent);
    expect(ends).toEqual(['≤ -30', '≥ +30']);
    expect(text()).toContain('Positive (red) = moving away from the satellite');
    // The same statement in the caveats is not repeated.
    expect(text()).not.toContain('Positive means away from the satellite.');
    expect(text()).toContain('No conversion to vertical motion.');
    expect(text()).toContain('Reference area: Generated test area.');
    expect(text()).toContain('Period: 2025-11-11 to 2026-10-13.');
    expect(text()).toContain('Source: NISAR GUNW (NASA/ISRO).');
    expect(text()).not.toMatch(/sinking|subsid/i);
  });

  it('says nothing about the sign when the manifest does not give it, and counts granules', () => {
    const frame = sinkingLayer.frames[0]!;
    const layer: Layer = {
      ...sinkingLayer,
      losLabel: undefined,
      awaySign: undefined,
      frames: [{ ...frame, granules: ['G1', 'G2', 'G3'] }],
    };
    load({ ...sample, synthetic: false, layers: [layer] });
    render(<Legend />);
    expect(container.querySelector('h2')?.textContent).toBe('Line-of-sight movement, cm/yr');
    expect(text()).not.toContain('= moving away');
    expect(text()).toContain('Positive means away from the satellite.'); // manifest caveat, shown as written
    expect(text()).toContain('Source: NISAR GUNW (NASA/ISRO), 3 granules.');
  });

  it('shows the last frame, like the map, when the date index is past the end', () => {
    const frame = sinkingLayer.frames[0]!;
    const layer: Layer = {
      ...sinkingLayer,
      frames: [
        { ...frame, since: '2025-11-11', date: '2026-04-22' },
        { ...frame, since: '2025-11-11', date: '2026-10-13' },
      ],
    };
    load({ ...sample, layers: [layer] });
    render(<Legend />);
    expect(text()).toContain('Period: 2025-11-11 to 2026-04-22.');
    act(() => useAppStore.setState({ dateIndex: 99 }));
    expect(text()).toContain('Period: 2025-11-11 to 2026-10-13.');
    expect(text()).not.toContain('2026-04-22');
  });

  it('drops only the exact sign sentence, and keeps a longer caveat that mentions the satellite', () => {
    const longer =
      'Motion away from the satellite can be vertical, horizontal or both; one viewing direction cannot tell them apart.';
    const caveats = ['  Positive means away from the satellite. ', longer];
    load({ ...sample, layers: [{ ...sinkingLayer, caveats }] });
    render(<Legend />);
    const items = [...container.querySelectorAll('.legend__caveats li')].map((li) => li.textContent);
    expect(items).toEqual([longer]);
    expect(text()).toContain('Positive (red) = moving away from the satellite');
  });

  it('draws the los-blue-white-red color bar from blue through white to red', () => {
    load(withSinking, 'sinking');
    render(<Legend />);
    expect(sinkingLayer.colormap.name).toBe('los-blue-white-red');
    const ramp = container.querySelector<HTMLElement>('.legend__ramp');
    // jsdom may rewrite hex colors as rgb(), so accept either spelling, in order.
    expect(ramp?.style.background).toMatch(
      /(#2166ac|rgb\(33, 102, 172\)).*(#ffffff|rgb\(255, 255, 255\)).*(#b2182b|rgb\(178, 24, 43\))/i,
    );
  });

  it('shows the reference area exactly as the manifest gives it', () => {
    // Wording from poc/mexico_city_sinking/provenance.json ("referenceArea", Eduardo).
    const referenceArea =
      'Western hills near Santa Fe, assumed stable (not yet a literature-named outcrop); its median is zero on every date';
    load({ ...sample, layers: [{ ...sinkingLayer, referenceArea }] });
    render(<Legend />);
    expect(text()).toContain(`Reference area: ${referenceArea}.`);
  });

  it('prints one full stop when the reference area already ends in one', () => {
    load({ ...sample, layers: [{ ...sinkingLayer, referenceArea: 'Western hills near Santa Fe.' }] });
    render(<Legend />);
    expect(text()).toContain('Reference area: Western hills near Santa Fe. ');
    expect(text()).not.toContain('..');
  });

  it('shows a repeated caveat twice without a React key warning', () => {
    const caveats = ['No conversion to vertical motion.', 'No conversion to vertical motion.'];
    load({ ...sample, layers: [{ ...sinkingLayer, caveats }] });
    render(<Legend />);
    expect(container.querySelectorAll('.legend__caveats li')).toHaveLength(2);
    // afterEach fails the test if React logged a duplicate-key error.
  });

  it('labels the flood-priority layer as a screening aid, not a forecast', () => {
    load({ ...sample, dataMaturity: 'PROVISIONAL', layers: [...sample.layers, floodLayer] }, 'flood_priority');
    render(<Legend />);
    expect(text()).toContain('Screening aid built on PROVISIONAL data. Not a flood forecast.');
    expect(container.querySelector('.legend__range')?.textContent).toBe('01');
  });
});
