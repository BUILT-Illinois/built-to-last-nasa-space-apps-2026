// Keeps two maps on the same camera, for the swipe compare.
// Owner: Eduardo (app/src/map/). Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.
import type { Map as MlMap } from 'maplibre-gl';

/** Mirror camera moves between two maps. Returns a function that stops the syncing. */
export function syncMaps(a: MlMap, b: MlMap): () => void {
  let syncing = false;
  const follow = (from: MlMap, to: MlMap) => () => {
    if (syncing) return;
    syncing = true;
    to.jumpTo({
      center: from.getCenter(),
      zoom: from.getZoom(),
      bearing: from.getBearing(),
      pitch: from.getPitch(),
    });
    syncing = false;
  };
  const aToB = follow(a, b);
  const bToA = follow(b, a);
  a.on('move', aToB);
  b.on('move', bToA);
  aToB();
  return () => {
    a.off('move', aToB);
    b.off('move', bToA);
  };
}
