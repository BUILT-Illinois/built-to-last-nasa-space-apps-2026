// The map. T-02 scaffold: a keyless basemap centered on the region.
// T-09 adds image layers from the manifest, layer and date switching from state, swipe compare,
// and the final basemap choice with attribution recorded in docs/SOURCES.md.
// Owner: Eduardo (app/src/map/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect, useRef } from 'react';
import * as maplibregl from 'maplibre-gl';
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
import { useAppStore } from '../state/store';
import type { LngLat } from '../types/manifest';

// MapLibre finds its worker relative to its own module URL, which breaks once Vite pre-bundles
// or bundles it ("Worker failed to load" and no tiles). Point it at the worker file explicitly.
maplibregl.setWorkerUrl(maplibreWorkerUrl);

/** Keyless vector basemap (OpenFreeMap, OpenStreetMap data). Placeholder until T-09 decides. */
const BASEMAP_STYLE = 'https://tiles.openfreemap.org/styles/liberty';

/** Mexico City (center of the bbox in pipeline/config/regions.json). Used until a manifest loads. */
const FALLBACK_CENTER: LngLat = [-99.13, 19.4];
const FALLBACK_ZOOM = 10;

export default function MapView() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const region = useAppStore((s) => s.manifest?.region);
  const cameraTarget = useAppStore((s) => s.cameraTarget);

  useEffect(() => {
    if (!containerRef.current) return;
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: BASEMAP_STYLE,
      center: FALLBACK_CENTER,
      zoom: FALLBACK_ZOOM,
      attributionControl: { compact: false },
    });
    map.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), 'top-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');
    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Move to the region's camera once its manifest is loaded.
  useEffect(() => {
    if (region && mapRef.current) {
      mapRef.current.jumpTo({ center: region.center, zoom: region.zoom });
    }
  }, [region]);

  // Fly to the camera a story step asks for (T-18). Declared after the region jump so it wins
  // when both change together. Jumps instead of flying for people who ask for reduced motion.
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !cameraTarget) return;
    const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
    if (reduceMotion) map.jumpTo(cameraTarget);
    else map.flyTo({ ...cameraTarget, duration: 1600 });
  }, [cameraTarget]);

  return <div ref={containerRef} className="map" aria-label="Map of the study region" />;
}
