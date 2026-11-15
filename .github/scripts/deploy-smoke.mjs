/* Drafted with AI assistance (Codex). See docs/AI_USAGE.md. */
import { pathToFileURL } from 'node:url';

const checks = [
  { path: '/', status: 200 },
  { path: '/data/sample/manifest.json', status: 200, json: true },
  { path: '/api/health', status: 200, json: true },
  { path: '/api/regions', status: 200, json: true,
    verify: (body) => Array.isArray(body) &&
      ['sample', 'mexico_city'].every((id) => body.some((region) => region?.id === id)) },
  ...['/api/regions/sample', '/api/regions/sample/manifest'].map((path) => ({
    path, status: 200, json: true,
    verify: (body) => body?.region?.id === 'sample' && body.synthetic === true &&
      body.dataMaturity === 'SYNTHETIC',
  })),
  { path: '/api/regions/sample/landmarks', status: 200, json: true,
    verify: (body) => body?.regionId === 'sample' && Array.isArray(body.landmarks) },
  { path: '/api/regions/mexico_city/manifest', status: 200, json: true },
  { path: '/api/regions/deploy-smoke-unknown/manifest', status: 404, json: true },
];

export async function smokeCheck(site, origin) {
  if (site !== 'Azure' && site !== 'Cloudflare') throw new Error('Expected site Azure or Cloudflare');
  return (await Promise.all(checks.map(async ({ path, status, json, verify }) => {
    // Use the origin only. Never log response bodies, headers, or fetch errors.
    const url = new URL(path, new URL(origin).origin);
    const failure = (reason) => `${site} ${url.href} — ${reason}`;
    try {
      const response = await fetch(url, {
        redirect: 'manual',
        signal: AbortSignal.timeout(10_000),
      });
      try {
        if (response.status !== status) {
          return failure(`expected HTTP ${status}, got ${response.status}`);
        }
        if (json) {
          const mime = response.headers.get('content-type')?.split(';')[0].trim().toLowerCase();
          if (mime !== 'application/json' && !mime?.endsWith('+json')) {
            return failure('expected a JSON Content-Type');
          }
          let body;
          try {
            body = await response.json();
          } catch {
            return failure('could not read a valid JSON response');
          }
          if (verify && !verify(body)) return failure('JSON did not match the expected data');
        }
      } finally {
        if (response.body && !response.bodyUsed) await response.body.cancel();
      }
    } catch {
      return failure('request failed or timed out');
    }
  }))).filter(Boolean);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [, , site, origin] = process.argv;
  const failures = await smokeCheck(site, origin);
  for (const failure of failures) console.error(failure);
  if (failures.length) process.exitCode = 1;
  else console.log(`${site}: all ${checks.length} smoke checks passed`);
}
