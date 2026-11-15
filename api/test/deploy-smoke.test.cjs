// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
const assert = require('node:assert/strict');
const { createServer } = require('node:http');
const { test } = require('node:test');

test('smoke checks cover each host and report failures without logging bodies', async (t) => {
  const { smokeCheck } = await import('../../.github/scripts/deploy-smoke.mjs');
  const sample = '/api/regions/sample';
  const list = '/api/regions';
  const unknown = '/api/regions/deploy-smoke-unknown/manifest';
  const manifest = '/api/regions/mexico_city/manifest';
  const paths = [];
  let broken = false;
  const server = createServer((req, res) => {
    paths.push(req.url);
    if (req.url === '/') return res.writeHead(broken ? 503 : 200).end();
    if (req.url === sample && broken) {
      return res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end('<private>');
    }
    if (req.url === sample + '/manifest' && broken) {
      return res.writeHead(200, { 'content-type': 'application/json' }).end('<private>');
    }
    const bodies = {
      [list]: broken ? [{ id: 'mexico_city' }] : [{ id: 'mexico_city' }, { id: 'sample' }],
      [sample]: { region: { id: 'sample' }, synthetic: true, dataMaturity: 'SYNTHETIC' },
      [sample + '/landmarks']: { regionId: 'sample', landmarks: [] },
    };
    res.writeHead(req.url === unknown ? 404 : 200, { 'content-type': 'application/json' })
      .end(JSON.stringify(bodies[req.url === sample + '/manifest' ? sample : req.url] ?? {}));
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const origin = `http://127.0.0.1:${server.address().port}`;

  for (const site of ['Azure', 'Cloudflare']) {
    broken = false;
    assert.deepEqual(await smokeCheck(site, origin), []);
    assert.deepEqual(paths.splice(0).sort(), [
      '/', '/data/sample/manifest.json', '/api/health', list, sample, sample + '/manifest',
      sample + '/landmarks', manifest, unknown,
    ].sort());
    broken = true;
    assert.deepEqual(await smokeCheck(site, origin), [
      `${site} ${origin}/ — expected HTTP 200, got 503`,
      `${site} ${origin}${list} — JSON did not match the expected data`,
      `${site} ${origin}${sample} — expected a JSON Content-Type`,
      `${site} ${origin}${sample}/manifest — could not read a valid JSON response`,
    ]);
    paths.length = 0;
  }
});
