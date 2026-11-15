// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { test } = require('node:test');

test('deploy smoke checks accept Pages routes and report invalid responses without logging bodies', async (t) => {
  const { smokeCheck } = await import('../../.github/scripts/deploy-smoke.mjs');
  const { onRequestGet } = await import('../../functions/api/[[route]].js');
  const sample = readFileSync(join(__dirname, '../../app/public/data/sample/manifest.json'));
  let broken = false;
  const server = createServer(async (req, res) => {
    const url = new URL(req.url, 'http://localhost');
    if (url.pathname === '/') return res.writeHead(broken ? 503 : 200).end();
    if (url.pathname === '/data/sample/manifest.json') {
      return res.writeHead(200, { 'content-type': 'application/json' }).end(broken ? '<private>' : sample);
    }
    if (broken && url.pathname === '/api/regions/deploy-smoke-unknown/manifest') {
      return res.writeHead(404, { 'content-type': 'text/html' }).end('<private>');
    }

    const response = onRequestGet({ params: { route: url.pathname.split('/').slice(2) } });
    res.writeHead(response.status, Object.fromEntries(response.headers)).end(await response.text());
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const origin = `http://127.0.0.1:${server.address().port}`;

  assert.deepEqual(await smokeCheck('Cloudflare', origin), []);
  broken = true;
  assert.deepEqual(await smokeCheck('Cloudflare', origin), [
    `Cloudflare ${origin}/ — expected HTTP 200, got 503`,
    `Cloudflare ${origin}/api/regions/deploy-smoke-unknown/manifest — expected a JSON Content-Type`,
    `Cloudflare ${origin}/data/sample/manifest.json — could not read a valid JSON response`,
  ]);
});
