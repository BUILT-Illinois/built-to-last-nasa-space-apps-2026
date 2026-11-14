// Test helper: a fetch stub whose responses the test releases one by one, in any order,
// so tests can replay slow and out-of-order network responses.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { vi } from 'vitest';

export type PendingFetch = {
  url: string;
  /** Answer with JSON (HTTP 200, application/json). */
  json: (body: unknown) => Promise<void>;
  /** Answer with an HTTP error status. */
  fail: (status?: number) => Promise<void>;
};

/** Let pending promise callbacks run. */
export const flush = () => new Promise((r) => setTimeout(r, 0));

/** Replace global fetch. Every call is recorded in the returned array until the test answers it. */
export function stubFetch(): PendingFetch[] {
  const calls: PendingFetch[] = [];
  vi.stubGlobal('fetch', (input: RequestInfo | URL) => {
    const url = String(input);
    return new Promise<Response>((resolve) => {
      calls.push({
        url,
        json: async (body) => {
          resolve(new Response(JSON.stringify(body), { headers: { 'content-type': 'application/json' } }));
          await flush();
        },
        fail: async (status = 404) => {
          resolve(new Response('not found', { status, headers: { 'content-type': 'text/plain' } }));
          await flush();
        },
      });
    });
  });
  return calls;
}

/** A minimal manifest for a region; `tag` marks which response the store ended up with. */
export function manifestFor(regionId: string, tag: string) {
  return {
    schemaVersion: '0.1',
    generatedAt: tag,
    generatedBy: 'test',
    region: { id: regionId, name: regionId, bbox: [-99.4, 19.1, -98.85, 19.65], center: [-99.13, 19.4], zoom: 10 },
    dataMaturity: 'PROVISIONAL',
    layers: [],
    vectors: [],
    sources: [],
  };
}
