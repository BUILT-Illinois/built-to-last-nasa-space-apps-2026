// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { test } = require('node:test');
const bundle = require('../dist/bundle.json');

test('Pages API serves the bundled data and a JSON 404 for unknown regions', async () => {
  const { onRequestGet } = await import('../../functions/api/[[route]].js');
  const get = (...route) => onRequestGet({ params: { route } });
  const mexicoCity = bundle.regions.find(({ manifest }) => manifest.region.id === 'mexico_city');

  const health = get('health');
  assert.equal(health.status, 200);
  assert.deepEqual(await health.json(), { ok: true, version: bundle.version });

  const regions = get('regions');
  assert.equal(regions.status, 200);
  assert.deepEqual(await regions.json(), bundle.regions.map(({ manifest: { region: { id, name, bbox } } }) =>
    ({ id, name, bbox })));

  for (const route of [['manifest'], ['regions', 'mexico_city', 'manifest']]) {
    const response = get(...route);
    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), mexicoCity.manifest);
  }
  const landmarks = get('regions', 'mexico_city', 'landmarks');
  assert.equal(landmarks.status, 200);
  assert.deepEqual(await landmarks.json(), mexicoCity.landmarks);

  const missing = get('regions', 'deploy-smoke-unknown', 'manifest');
  assert.equal(missing.status, 404);
  assert.deepEqual(await missing.json(), { success: false, message: 'Region not found' });
});
