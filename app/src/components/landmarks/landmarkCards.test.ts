// Tests for laying Monica's card text over the published landmarks (T-14).
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { expect, it } from 'vitest';
import type { Landmark } from '../../types/manifest';
import { withCardText } from './landmarkCards';

const published: Landmark = {
  id: 'a', name: 'Published', lon: 1, lat: 2, summary: 'p', radarShows: 'p', weInfer: 'p',
  drivers: { human: 'pub', natural: null }, sourceIds: ['nisar-gcov'], series: { hh_db: [] },
};
const file = (card: object) => ({ schemaVersion: '0.1', regionId: 'r', landmarks: [{ id: 'a', ...card }] });

it('card text replaces the published text; position and series stay', () => {
  const l = withCardText([published], file({ name: 'Card', radarShows: 'card radar', lon: 99 }))[0]!;
  expect(l.name).toBe('Card');
  expect(l.radarShows).toBe('card radar');
  expect(l.lon).toBe(1);
  expect(l.series).toEqual({ hh_db: [] });
});

it('a field the card leaves out keeps the published value', () => {
  const l = withCardText([published], file({ name: 'Card' }))[0]!;
  expect(l.drivers).toEqual({ human: 'pub', natural: null });
  expect(l.sourceIds).toEqual(['nisar-gcov']);
});

it('no card file leaves the landmarks unchanged', () => {
  expect(withCardText([published], undefined)).toEqual([published]);
});
