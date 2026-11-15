// T-14 landmark markers: one circle per landmark, drawn above the radar image.
// Clicking a circle selects that landmark in the store; the selected one is drawn larger.
// Written by Zainab's session with Eduardo's OK (PR #49). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { ExpressionSpecification, GeoJSONSource, Map as MlMap } from 'maplibre-gl';
import type { Landmark } from '../types/manifest';

const SOURCE = 'landmarks';
const LAYER = 'landmark-circles';

/** Circle radius: bigger for the selected landmark. */
const radiusFor = (selectedId: string | null): ExpressionSpecification =>
  ['case', ['==', ['get', 'id'], selectedId ?? ''], 10, 6];

function toGeoJson(landmarks: Landmark[]) {
  return {
    type: 'FeatureCollection' as const,
    features: landmarks.map((l) => ({
      type: 'Feature' as const,
      geometry: { type: 'Point' as const, coordinates: [l.lon, l.lat] },
      properties: { id: l.id, name: l.name },
    })),
  };
}

/** Add the empty marker layer on top of everything added so far, and wire clicks. Call once, on 'load'. */
export function addLandmarkLayer(map: MlMap, onSelect: (id: string) => void): void {
  if (map.getSource(SOURCE)) return;
  map.addSource(SOURCE, { type: 'geojson', data: toGeoJson([]) });
  map.addLayer({
    id: LAYER,
    type: 'circle',
    source: SOURCE,
    paint: {
      'circle-radius': radiusFor(null),
      'circle-color': '#d29922',
      'circle-stroke-color': '#ffffff',
      'circle-stroke-width': 2,
    },
  });
  map.on('click', LAYER, (e) => {
    const id = e.features?.[0]?.properties?.id;
    if (typeof id === 'string') onSelect(id);
  });
  map.on('mouseenter', LAYER, () => (map.getCanvas().style.cursor = 'pointer'));
  map.on('mouseleave', LAYER, () => (map.getCanvas().style.cursor = ''));
}

/** Replace the markers, for example after a region change. */
export function setLandmarks(map: MlMap, landmarks: Landmark[]): void {
  (map.getSource(SOURCE) as GeoJSONSource | undefined)?.setData(toGeoJson(landmarks));
}

/** Draw the selected landmark larger. */
export function setSelectedLandmark(map: MlMap, selectedId: string | null): void {
  if (map.getLayer(LAYER)) map.setPaintProperty(LAYER, 'circle-radius', radiusFor(selectedId));
}
