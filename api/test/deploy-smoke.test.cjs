// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { test } = require('node:test');

test('smoke checks cover each host and report failures without logging bodies', async (t) => {
  const { smokeCheck } = await import('../../.github/scripts/deploy-smoke.mjs');
  const sample = '/data/sample/manifest.json';
  const unknown = '/api/regions/deploy-smoke-unknown/manifest';
  const manifest = '/api/regions/mexico_city/manifest';
  const paths = [];
  let broken = false;
  const server = createServer((req, res) => {
    paths.push(req.url);
    if (req.url === '/') return res.writeHead(broken ? 503 : 200).end();
    if (req.url === sample && broken) {
      return res.writeHead(200, { 'content-type': 'application/json' }).end('<private>');
    }
    if (req.url === unknown && broken) {
      return res.writeHead(404, { 'content-type': 'text/html' }).end('<private>');
    }
    res.writeHead(req.url === unknown ? 404 : 200, { 'content-type': 'application/json' }).end('{}');
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const origin = `http://127.0.0.1:${server.address().port}`;

  assert.deepEqual(await smokeCheck('Azure', origin), []);
  assert.deepEqual(paths.splice(0).sort(), ['/', sample, '/api/health', '/api/regions', manifest, unknown].sort());
  assert.deepEqual(await smokeCheck('Cloudflare', origin), []);
  assert.deepEqual(paths.sort(), ['/', sample]);

  broken = true;
  assert.deepEqual(await smokeCheck('Azure', origin), [
    `Azure ${origin}/ — expected HTTP 200, got 503`,
    `Azure ${origin}${sample} — could not read a valid JSON response`,
    `Azure ${origin}${unknown} — expected a JSON Content-Type`,
  ]);
});
