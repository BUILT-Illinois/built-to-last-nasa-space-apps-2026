// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { readFileSync, readdirSync, existsSync } = require('node:fs');
const { join } = require('node:path');
const { test } = require('node:test');
const { HttpRequest } = require('@azure/functions');
const { health, regions, manifest, landmarks, hotspots } = require('../dist/api/src/index.js');

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
  assert.deepEqual(result.jsonBody.toSorted((a, b) => a.id.localeCompare(b.id)),
    published.toSorted((a, b) => a.localeCompare(b)).map((id) => {
      const { name, bbox } = readJson(join(dataRoot, id, 'manifest.json')).region;
      return { id, name, bbox };
    }));
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

test('hotspots returns the published file or a JSON 404 for an unpublished region layer', () => {
  for (const id of published) {
    const region = join(dataRoot, id);
    const hasPriority = readJson(join(region, 'manifest.json')).layers.some(({ kind }) => kind === 'priority');
    assert.deepEqual(hotspots(request(id, 'hotspots')), hasPriority
      ? { status: 200, jsonBody: readJson(join(region, 'hotspots.json')) }
      : { status: 404, jsonBody: { success: false, message: 'Region not found' } });
  }
});

test('unknown IDs return the contract 404 for all region file routes', () => {
  for (const [file, handler] of Object.entries({ manifest, landmarks, hotspots })) {
    for (const id of ['missing', '__proto__', '../mexico_city']) {
      assert.deepEqual(handler(request(id, file)), {
        status: 404,
        jsonBody: { success: false, message: 'Region not found' },
      });
    }
  }
});
