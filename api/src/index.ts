// Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
import { app, type HttpRequest, type HttpResponseInit } from '@azure/functions';
import type { HotspotsFile, LandmarksFile, Manifest, Region } from '../../app/src/types/manifest.js' with { 'resolution-mode': 'import' };

type RegionSummary = Pick<Region, 'id' | 'name' | 'bbox'>;
type Health = { ok: true; version: string };
type ApiError = { success: false; message: string };
type Dataset = { manifest: Manifest; landmarks: LandmarksFile; hotspots?: HotspotsFile };
type Bundle = { version: string; regions: Dataset[] };

const bundle = require('../../bundle.json') as Bundle;
const datasets = new Map(bundle.regions.map((dataset) => [dataset.manifest.region.id, dataset]));

function ok(payload: Health | RegionSummary[] | Manifest | LandmarksFile | HotspotsFile): HttpResponseInit {
  return { status: 200, jsonBody: payload };
}

function notFound(): HttpResponseInit {
  const error: ApiError = { success: false, message: 'Region not found' };
  return { status: 404, jsonBody: error };
}

export function health(): HttpResponseInit {
  return ok({ ok: true, version: bundle.version });
}

export function regions(): HttpResponseInit {
  return ok(bundle.regions.map(({ manifest: { region: { id, name, bbox } } }) => ({ id, name, bbox })));
}

function regionFile(request: HttpRequest, key: keyof Dataset): HttpResponseInit {
  const payload = datasets.get(request.params.id)?.[key];
  return payload ? ok(payload) : notFound();
}

export function manifest(request: HttpRequest): HttpResponseInit {
  return regionFile(request, 'manifest');
}

export function landmarks(request: HttpRequest): HttpResponseInit {
  return regionFile(request, 'landmarks');
}

export function hotspots(request: HttpRequest): HttpResponseInit {
  return regionFile(request, 'hotspots');
}

app.http('hotspots', {
  route: 'regions/{id}/hotspots', methods: ['GET'], authLevel: 'anonymous', handler: hotspots,
});

app.http('health', { route: 'health', methods: ['GET'], authLevel: 'anonymous', handler: health });
app.http('regions', { route: 'regions', methods: ['GET'], authLevel: 'anonymous', handler: regions });
app.http('manifest', {
  route: 'regions/{id}/manifest', methods: ['GET'], authLevel: 'anonymous', handler: manifest,
});
app.http('landmarks', {
  route: 'regions/{id}/landmarks', methods: ['GET'], authLevel: 'anonymous', handler: landmarks,
});
