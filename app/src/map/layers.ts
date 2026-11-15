// Map layers that sit on top of the basemap style: optical imagery and the NISAR image.
// Layer order, bottom to top: basemap fills and lines, optical imagery, NISAR image, basemap labels.
// Owner: Eduardo (app/src/map/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { ImageSource, Map as MlMap } from 'maplibre-gl';
import type { BBox, Frame, Layer } from '../types/manifest';
import type { Basemap } from '../state/store';

/**
 * Keyless vector basemap: OpenFreeMap "positron" (light, quiet colors so the radar stands out).
 * OpenFreeMap is free with no key; map data is OpenStreetMap (ODbL). Attribution comes from the style.
 */
export const BASEMAP_STYLE = 'https://tiles.openfreemap.org/styles/positron';

/**
 * Optical imagery: EOxCloudless 2024 (Sentinel-2 cloud-free mosaic), keyless WMTS.
 * License for non-commercial use: CC BY-NC-SA 4.0, attribution visible on the map.
 */
const OPTICAL_TILES =
  'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2024_3857/default/g/{z}/{y}/{x}.jpg';
const OPTICAL_ATTRIBUTION =
  '<a href="https://cloudless.eox.at" target="_blank" rel="noopener">EOxCloudless 2024</a> by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2024)';

/** Image sources cannot carry attribution, so the base map's credits list NISAR directly. */
export const NISAR_ATTRIBUTION = 'NISAR data: NASA and ISRO, via the ASF DAAC (provisional)';

const OPTICAL_SOURCE = 'optical';
const OPTICAL_LAYER = 'optical-imagery';
const NISAR_SOURCE = 'nisar';
const NISAR_LAYER = 'nisar-image';

/** Id of the first label layer, so our rasters go under place names. Undefined = top of the stack. */
function firstSymbolLayerId(map: MlMap): string | undefined {
  return map.getStyle().layers.find((l) => l.type === 'symbol')?.id;
}

/** Image corners in the order MapLibre expects: top-left, top-right, bottom-right, bottom-left. */
export function boundsToCorners([w, s, e, n]: BBox): [[number, number], [number, number], [number, number], [number, number]] {
  return [
    [w, n],
    [e, n],
    [e, s],
    [w, s],
  ];
}

/** Add the optical imagery layer once (hidden). Call after the style has loaded. */
export function addOpticalLayer(map: MlMap): void {
  if (map.getSource(OPTICAL_SOURCE)) return;
  map.addSource(OPTICAL_SOURCE, {
    type: 'raster',
    tiles: [OPTICAL_TILES],
    tileSize: 256,
    maxzoom: 15,
    attribution: OPTICAL_ATTRIBUTION,
  });
  map.addLayer(
    { id: OPTICAL_LAYER, type: 'raster', source: OPTICAL_SOURCE, layout: { visibility: 'none' } },
    firstSymbolLayerId(map),
  );
}

/** Show the street map or the optical imagery under the radar image. */
export function setBasemap(map: MlMap, basemap: Basemap): void {
  if (!map.getLayer(OPTICAL_LAYER)) return;
  map.setLayoutProperty(OPTICAL_LAYER, 'visibility', basemap === 'satellite' ? 'visible' : 'none');
}

/**
 * Show one frame of one manifest layer, or nothing when `layer` or `frame` is undefined.
 * `baseUrl` is the region folder; frame image paths are relative to it.
 */
export function setNisarImage(
  map: MlMap,
  layer: Layer | undefined,
  frame: Frame | undefined,
  baseUrl: string,
  opacity: number,
): void {
  if (!layer || !frame) {
    if (map.getLayer(NISAR_LAYER)) map.removeLayer(NISAR_LAYER);
    if (map.getSource(NISAR_SOURCE)) map.removeSource(NISAR_SOURCE);
    return;
  }
  const url = new URL(frame.image, new URL(baseUrl, window.location.href)).href;
  const coordinates = boundsToCorners(layer.bounds);
  const source = map.getSource<ImageSource>(NISAR_SOURCE);
  if (source) {
    source.updateImage({ url, coordinates });
  } else {
    map.addSource(NISAR_SOURCE, { type: 'image', url, coordinates });
  }
  if (!map.getLayer(NISAR_LAYER)) {
    map.addLayer(
      {
        id: NISAR_LAYER,
        type: 'raster',
        source: NISAR_SOURCE,
        paint: { 'raster-fade-duration': 0, 'raster-opacity': opacity },
      },
      firstSymbolLayerId(map),
    );
  } else {
    map.setPaintProperty(NISAR_LAYER, 'raster-opacity', opacity);
  }
}
