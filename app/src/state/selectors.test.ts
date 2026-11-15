// Tests for the T-09 map selectors and view actions. Drafted with AI assistance (Claude Code),
// see docs/AI_USAGE.md.
import { beforeEach, describe, expect, it } from 'vitest';
import type { Layer, Manifest } from '../types/manifest';
import { selectActiveFrame, selectCompareFrame, selectCompareLayer, useAppStore } from './store';

const layer = (id: string, dates: string[]): Layer => ({
  id,
  title: id,
  kind: 'backscatter',
  product: 'GCOV',
  polarization: 'HH',
  units: 'dB',
  bounds: [-99.4, 19.1, -98.85, 19.65],
  colormap: { name: 'gray', min: -25, max: 0 },
  description: '',
  caveats: [],
  frames: dates.map((date) => ({ date, image: `layers/${id}/${date}.webp`, granules: [], track: 19, frame: 11, direction: 'ASCENDING' })),
});

const manifest = {
  layers: [layer('hh', ['2025-11-11', '2026-04-16', '2026-10-13']), layer('hv', ['2025-11-11'])],
} as unknown as Manifest;

beforeEach(() => {
  useAppStore.setState({ manifest, activeLayerId: 'hh', dateIndex: 0, compareLayerId: null, compareDateIndex: null });
});

describe('map selectors', () => {
  it('no compare layer means no swipe', () => {
    expect(selectCompareLayer(useAppStore.getState())).toBeUndefined();
    expect(selectCompareFrame(useAppStore.getState())).toBeUndefined();
  });

  it('compares two dates of the same layer', () => {
    useAppStore.getState().setCompare('hh', 2);
    const s = useAppStore.getState();
    expect(selectActiveFrame(s)?.date).toBe('2025-11-11');
    expect(selectCompareFrame(s)?.date).toBe('2026-10-13');
  });

  it('compare date defaults to the active date, clamped to the layer', () => {
    useAppStore.getState().setDate(2);
    useAppStore.getState().setCompare('hv');
    // hv has one frame, so index 2 clamps to its last frame instead of breaking the map
    expect(selectCompareFrame(useAppStore.getState())?.date).toBe('2025-11-11');
  });

  it('setCompare(null) turns the swipe off', () => {
    useAppStore.getState().setCompare('hh', 1);
    useAppStore.getState().setCompare(null);
    expect(useAppStore.getState()).toMatchObject({ compareLayerId: null, compareDateIndex: null });
  });

  it('opacity is kept between 0 and 1, and flyTo always issues a new request', () => {
    useAppStore.getState().setLayerOpacity(3);
    expect(useAppStore.getState().layerOpacity).toBe(1);
    useAppStore.getState().flyTo([-99.07, 19.43], 13);
    const first = useAppStore.getState().cameraRequest?.seq;
    useAppStore.getState().flyTo([-99.07, 19.43], 13);
    expect(useAppStore.getState().cameraRequest?.seq).toBe((first ?? 0) + 1);
  });
});
