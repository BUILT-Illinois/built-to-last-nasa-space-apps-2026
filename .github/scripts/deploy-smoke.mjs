/* Drafted with AI assistance (Codex). See docs/AI_USAGE.md. */
import { pathToFileURL } from 'node:url';

const staticChecks = [
  { path: '/', status: 200 },
  { path: '/data/sample/manifest.json', status: 200, json: true },
];
const checksBySite = new Map([
  ['Azure', [
    ...staticChecks,
    { path: '/api/health', status: 200, json: true },
    { path: '/api/regions', status: 200, json: true },
    { path: '/api/regions/mexico_city/manifest', status: 200, json: true },
    { path: '/api/regions/deploy-smoke-unknown/manifest', status: 404, json: true },
  ]],
  ['Cloudflare', staticChecks],
]);

export async function smokeCheck(site, origin) {
  const checks = checksBySite.get(site);
  if (!checks) throw new Error('Expected site Azure or Cloudflare');
  return (await Promise.all(checks.map(async ({ path, status, json }) => {
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
          try {
            await response.json();
          } catch {
            return failure('could not read a valid JSON response');
          }
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
  else console.log(`${site}: all ${checksBySite.get(site).length} smoke checks passed`);
}
