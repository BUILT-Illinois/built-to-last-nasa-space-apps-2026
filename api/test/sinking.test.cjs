// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { test } = require('node:test');
const { HttpRequest } = require('@azure/functions');

test('the manifest route serves the synthetic LOS rate and its provenance unchanged', () => {
  const sinking = {
    id: 'sinking',
    kind: 'displacement',
    product: 'GUNW',
    units: 'cm/yr',
    bounds: [-99.40, 19.10, -98.85, 19.65],
    colormap: { name: 'los-blue-white-red', min: -30, max: 30 },
    losLabel: 'Radar line-of-sight rate',
    awaySign: 'positive',
    referenceArea: 'Generated test area',
    frames: [{
      since: '2025-11-11',
      date: '2026-10-13',
      image: 'layers/sinking/test.png',
      granules: [],
    }],
  };
  const fixture = {
    region: { id: 'mexico_city' },
    dataMaturity: 'SYNTHETIC',
    synthetic: true,
    layers: [sinking],
  };
  // Swap the bundled JSON in this test process only; leave live data and the packaged bundle intact.
  const bundle = require.resolve('../dist/bundle.json');
  require.cache[bundle] = { exports: { regions: [{ manifest: fixture }] } };
  const { manifest } = require('../dist/api/src/index.js');
  const result = manifest(new HttpRequest({
    method: 'GET',
    url: 'http://localhost/api/regions/mexico_city/manifest',
    params: { id: 'mexico_city' },
  }));
  assert.deepEqual(result, { status: 200, jsonBody: fixture });
});
