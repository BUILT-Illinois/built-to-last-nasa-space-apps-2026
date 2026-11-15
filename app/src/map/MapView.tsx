// The map screen (T-09): basemap or optical imagery, the NISAR image for the active layer and date,
// and a swipe compare against a second layer or date. It only reads the shared store.
// Two stacked maps share one camera; the top one shows the compare image and is clipped to the
// right of the divider.
// Owner: Eduardo (app/src/map/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
import {
  selectActiveFrame,
  selectActiveLayer,
  selectCompareFrame,
  selectCompareLayer,
  useAppStore,
} from '../state/store';
import { regionBaseUrl } from '../lib/data';
import type { Frame, Layer, LngLat } from '../types/manifest';
import { BASEMAP_STYLE, NISAR_ATTRIBUTION, addOpticalLayer, setBasemap, setNisarImage } from './layers';
import { syncMaps } from './syncMaps';
import { cardsFor, withCardText } from '../components/landmarks/landmarkCards';
import LandmarkCard from './LandmarkCard';
import SwipeHandle from './SwipeHandle';
import './map.css';

// MapLibre finds its worker relative to its own module URL, which breaks once Vite pre-bundles
// or bundles it ("Worker failed to load" and no tiles). Point it at the worker file explicitly.
maplibregl.setWorkerUrl(maplibreWorkerUrl);

/** Mexico City (center of the bbox in pipeline/config/regions.json). Used until a manifest loads. */
const FALLBACK_CENTER: LngLat = [-99.13, 19.4];
const FALLBACK_ZOOM = 10;

type Maps = { base: maplibregl.Map; compare: maplibregl.Map };

/** Title and date of one side of the swipe; `when` is empty if there is no frame. */
function sideLabel(layer: Layer | undefined, frame: Frame | undefined): { title: string; when: string } {
  if (!layer) return { title: 'No layer', when: '' };
  if (!frame) return { title: layer.title, when: '' };
  return { title: layer.title, when: frame.since ? `${frame.since} to ${frame.date}` : frame.date };
}

const labelText = ({ title, when }: { title: string; when: string }) => (when ? `${title}, ${when}` : title);

function SideLabel({ side, label }: { side: 'left' | 'right'; label: { title: string; when: string } }) {
  return (
    <div className={`swipe-label swipe-label--${side}`}>
      <div>{label.title}</div>
      {label.when && <div className="swipe-label__date">{label.when}</div>}
    </div>
  );
}

export default function MapView() {
  const baseRef = useRef<HTMLDivElement>(null);
  const compareRef = useRef<HTMLDivElement>(null);
  const mapsRef = useRef<Maps | null>(null);
  const landmarkPins = useRef<{ button: HTMLButtonElement; id: string }[]>([]);
  const [ready, setReady] = useState({ base: false, compare: false });
  const [swipe, setSwipe] = useState(0.5);

  const region = useAppStore((s) => s.manifest?.region);
  const regionId = useAppStore((s) => s.regionId);
  const landmarks = useAppStore((s) => s.landmarks);
  const selectedLandmarkId = useAppStore((s) => s.selectedLandmarkId);
  const selectLandmark = useAppStore((s) => s.selectLandmark);
  const storyStep = useAppStore((s) => s.storyStep);
  const basemap = useAppStore((s) => s.basemap);
  const opacity = useAppStore((s) => s.layerOpacity);
  const cameraRequest = useAppStore((s) => s.cameraRequest);
  const activeLayer = useAppStore(selectActiveLayer);
  const activeFrame = useAppStore(selectActiveFrame);
  const compareLayer = useAppStore(selectCompareLayer);
  const compareFrame = useAppStore(selectCompareFrame);
  const comparing = compareLayer !== undefined;

  // Create both maps once.
  useEffect(() => {
    if (!baseRef.current || !compareRef.current) return;
    const common = { style: BASEMAP_STYLE, center: FALLBACK_CENTER, zoom: FALLBACK_ZOOM };
    const base = new maplibregl.Map({
      ...common,
      container: baseRef.current,
      // compact is left unset so MapLibre collapses the credits on narrow screens.
      attributionControl: { customAttribution: NISAR_ATTRIBUTION },
    });
    const compare = new maplibregl.Map({
      ...common,
      container: compareRef.current,
      attributionControl: false, // the base map's credits sit above both maps
    });
    base.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), 'top-right');
    base.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');
    base.on('load', () => {
      addOpticalLayer(base);
      setReady((r) => ({ ...r, base: true }));
    });
    compare.on('load', () => {
      addOpticalLayer(compare);
      setReady((r) => ({ ...r, compare: true }));
    });
    const unsync = syncMaps(base, compare);
    mapsRef.current = { base, compare };
    return () => {
      unsync();
      base.remove();
      compare.remove();
      mapsRef.current = null;
    };
  }, []);

  // Move to the region's camera once its manifest is loaded.
  useEffect(() => {
    if (region) mapsRef.current?.base.jumpTo({ center: region.center, zoom: region.zoom });
  }, [region]);

  // Story steps and landmark clicks ask the map to fly somewhere.
  useEffect(() => {
    if (cameraRequest) {
      mapsRef.current?.base.flyTo({ center: cameraRequest.center, zoom: cameraRequest.zoom });
    }
  }, [cameraRequest]);

  // Street map or optical imagery under the radar.
  useEffect(() => {
    const maps = mapsRef.current;
    if (!maps) return;
    if (ready.base) setBasemap(maps.base, basemap);
    if (ready.compare) setBasemap(maps.compare, basemap);
  }, [basemap, ready]);

  // The active layer and date on the base map.
  useEffect(() => {
    const map = mapsRef.current?.base;
    if (map && ready.base) setNisarImage(map, activeLayer, activeFrame, regionBaseUrl(regionId), opacity);
  }, [activeLayer, activeFrame, regionId, opacity, ready.base]);

  // The compare layer and date on the top map.
  useEffect(() => {
    const map = mapsRef.current?.compare;
    if (map && ready.compare) {
      setNisarImage(map, compareLayer, compareFrame, regionBaseUrl(regionId), opacity);
    }
  }, [compareLayer, compareFrame, regionId, opacity, ready.compare]);

  useEffect(() => {
    const map = mapsRef.current?.base;
    if (!map || !ready.base || storyStep !== null) return;
    const pins = withCardText(landmarks, cardsFor(regionId)).map((landmark) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'map-landmark-pin';
      button.setAttribute('aria-label', landmark.name);
      const marker = new maplibregl.Marker({ element: button })
        .setLngLat([landmark.lon, landmark.lat])
        .addTo(map);
      button.onclick = () => selectLandmark(landmark.id);
      return { marker, button, id: landmark.id };
    });
    landmarkPins.current = pins;
    return () => {
      pins.forEach(({ marker }) => marker.remove());
      landmarkPins.current = [];
    };
  }, [landmarks, ready.base, regionId, selectLandmark, storyStep]);

  useEffect(() => {
    landmarkPins.current.forEach(({ button, id }) => {
      button.setAttribute('aria-expanded', String(id === selectedLandmarkId));
    });
  }, [landmarks, ready.base, regionId, selectedLandmarkId, storyStep]);

  function closeLandmark() {
    selectLandmark(null);
    landmarkPins.current.find(({ id }) => id === selectedLandmarkId)?.button.focus();
  }

  const leftLabel = sideLabel(activeLayer, activeFrame);
  const rightLabel = sideLabel(compareLayer, compareFrame);

  return (
    <div className="map-screen">
      <div ref={baseRef} className="map" aria-label={`Map: ${labelText(leftLabel)}`} />
      <div
        ref={compareRef}
        className="map map--compare"
        aria-hidden={!comparing}
        aria-label={comparing ? `Compare map: ${labelText(rightLabel)}` : undefined}
        style={{
          clipPath: `inset(0 0 0 ${swipe * 100}%)`,
          visibility: comparing ? 'visible' : 'hidden',
        }}
      />
      <LandmarkCard onClose={closeLandmark} />
      {comparing && (
        <>
          <SwipeHandle
            position={swipe}
            onChange={setSwipe}
            leftLabel={labelText(leftLabel)}
            rightLabel={labelText(rightLabel)}
          />
          <SideLabel side="left" label={leftLabel} />
          <SideLabel side="right" label={rightLabel} />
        </>
      )}
    </div>
  );
}
