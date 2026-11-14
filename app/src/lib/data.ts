// Loads a region's static data files (docs/DATA_CONTRACT.md). Same-origin static files only;
// the app must work with the API switched off.
// Owner: Elias (app/src/lib/). Stub written in T-02 by Eduardo's session; Elias may replace it.
// Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { LandmarksFile, Manifest } from '../types/manifest';

/** Base URL of a region's data folder, e.g. "/data/sample/". Manifest image paths are relative to it. */
export function regionBaseUrl(regionId: string): string {
  return `${import.meta.env.BASE_URL}data/${encodeURIComponent(regionId)}/`;
}

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load ${url} (HTTP ${res.status})`);
  const type = res.headers.get('content-type') ?? '';
  // Vite's dev server answers missing files with index.html, so check before parsing.
  if (!type.includes('json')) throw new Error(`Could not load ${url} (not JSON: ${type || 'no type'})`);
  return (await res.json()) as T;
}

/** Fetch manifest.json for a region. Throws if it is missing or not JSON. */
export function loadManifest(regionId: string): Promise<Manifest> {
  return fetchJson<Manifest>(`${regionBaseUrl(regionId)}manifest.json`);
}

/** Fetch landmarks.json for a region. Throws if it is missing or not JSON. */
export function loadLandmarks(regionId: string): Promise<LandmarksFile> {
  return fetchJson<LandmarksFile>(`${regionBaseUrl(regionId)}landmarks.json`);
}
