// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { readFileSync, readdirSync, existsSync } = require('node:fs');
const { join } = require('node:path');
const { test } = require('node:test');
const { HttpRequest } = require('@azure/functions');
const { health, regions, manifest, landmarks, mexicoCityLandmarks } = require('../dist/api/src/index.js');

const dataRoot = join(__dirname, '../../app/public/data');
const readJson = (path) => JSON.parse(readFileSync(path, 'utf8'));
const published = readdirSync(dataRoot).filter((id) => existsSync(join(dataRoot, id, 'manifest.json')));
const request = (id, file) => new HttpRequest({
  method: 'GET',
  url: `http://localhost/api/regions/${encodeURIComponent(id)}/${file}`,
  params: { id },
});

test('health reports the build commit', () => {
  const result = health();
  assert.equal(result.status, 200);
  assert.deepEqual(result.jsonBody, {
    ok: true,
    version: process.env.GITHUB_SHA ??
      require('node:child_process').execFileSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(),
  });
});

test('regions lists exactly the published static datasets and their summary fields', () => {
  const result = regions();
  assert.equal(result.status, 200);
  assert.ok(published.includes('mexico_city'));
  assert.ok(published.includes('sample'));
  assert.deepEqual(result.jsonBody.toSorted((a, b) => a.id.localeCompare(b.id)),
    published.toSorted((a, b) => a.localeCompare(b)).map((id) => {
      const { name, bbox } = readJson(join(dataRoot, id, 'manifest.json')).region;
      return { id, name, bbox };
    }));
});

test('Pages serves the bundled region list and synthetic sample routes as JSON', async () => {
  const { onRequestGet } = await import('../../functions/api/[[route]].js');
  const requestRoute = (route) => onRequestGet({ params: { route } });
  const sampleManifest = readJson(join(dataRoot, 'sample', 'manifest.json'));
  const sampleLandmarks = readJson(join(dataRoot, 'sample', 'landmarks.json'));
  for (const [route, expected] of [
    [['regions'], regions().jsonBody],
    [['regions', 'sample'], sampleManifest],
    [['regions', 'sample', 'manifest'], sampleManifest],
    [['regions', 'sample', 'landmarks'], sampleLandmarks],
  ]) {
    const result = requestRoute(route);
    assert.equal(result.status, 200);
    assert.match(result.headers.get('content-type'), /^application\/json(?:;|$)/);
    assert.deepEqual(await result.json(), expected);
  }
  const missing = requestRoute(['regions', 'missing', 'manifest']);
  assert.equal(missing.status, 404);
  assert.deepEqual(await missing.json(), { success: false, message: 'Region not found' });
});

test('manifest and landmarks return the same JSON as the static site', () => {
  for (const id of published) {
    for (const [file, handler] of Object.entries({ manifest, landmarks })) {
      assert.deepEqual(handler(request(id, file)), {
        status: 200,
        jsonBody: readJson(join(dataRoot, id, `${file}.json`)),
      });
    }
  }
});

test('the wider valley serves the same GCOV acquisitions as the city', () => {
  const city = manifest(request('mexico_city', 'manifest')).jsonBody;
  const valley = manifest(request('mexico_city_valley', 'manifest')).jsonBody;
  assert.deepEqual(valley.region.bbox, [-99.60, 19.00, -98.60, 19.90]);
  const gcov = ({ layers }) => layers.filter(({ product }) => product === 'GCOV')
    .map(({ id, frames }) => ({ id, frames }));
  assert.deepEqual(gcov(valley), gcov(city));
  assert.ok(gcov(valley).every(({ frames }) => frames.length === 11));
  assert.equal(valley.dataMaturity, 'PROVISIONAL');
  const sinking = valley.layers.find(({ id }) => id === 'sinking');
  assert.equal(sinking.awaySign, 'positive');
  assert.equal(sinking.units, 'cm/yr');
  assert.deepEqual(sinking.bounds, valley.region.bbox);
  assert.equal(sinking.frames[0].granules.length, 27);
  assert.match(sinking.caveats.join(' '), /likely noise, pending review/);
  const valleyLandmarks = landmarks(request('mexico_city_valley', 'landmarks')).jsonBody.landmarks;
  const cityLandmarks = landmarks(request('mexico_city', 'landmarks')).jsonBody.landmarks;
  assert.deepEqual(valleyLandmarks.map(({ id }) => id), cityLandmarks.map(({ id }) => id));
});

test('/api/landmarks serves the Mexico City monthly landmark series', () => {
  const result = mexicoCityLandmarks();
  assert.deepEqual(result, landmarks(request('mexico_city', 'landmarks')));
  const entries = result.jsonBody.landmarks;
  assert.equal(entries.length, 7);
  const lake = entries.find(({ id }) => id === 'new_lake_chalco');
  assert.equal(lake.series.hh_db.length, 11);
  assert.equal(lake.series.hv_db.length, 11);
  assert.equal(lake.series.water_months.provisional, true);
  assert.equal(lake.series.water_months.valid_months, 11);
});

test('published region manifests and radar series exclude the D-17 dates', () => {
  const excluded = new Set(['2025-12-05', '2026-04-16']);
  for (const { id } of regions().jsonBody) {
    const { status, jsonBody } = manifest(request(id, 'manifest'));
    assert.equal(status, 200);
    for (const layer of jsonBody.layers) {
      for (const { date } of layer.frames) {
        assert.ok(!excluded.has(date), `${id}/${layer.id} serves D-17 excluded frame ${date}`);
      }
    }
    for (const landmark of landmarks(request(id, 'landmarks')).jsonBody.landmarks) {
      for (const { date } of [...(landmark.series.hh_db ?? []), ...(landmark.series.hv_db ?? [])]) {
        assert.ok(!excluded.has(date), `${id}/${landmark.id} serves D-17 excluded radar date ${date}`);
      }
    }
  }
});

test('unknown IDs return the contract 404 for both region file routes', () => {
  for (const [file, handler] of Object.entries({ manifest, landmarks })) {
    for (const id of ['missing', '__proto__', '../mexico_city']) {
      assert.deepEqual(handler(request(id, file)), {
        status: 404,
        jsonBody: { success: false, message: 'Region not found' },
      });
    }
  }
});
