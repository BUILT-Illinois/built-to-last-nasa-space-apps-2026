# app/

Web map for the NISAR data. Vite + React + TypeScript + MapLibre GL JS. Scaffold from T-02, drafted with AI assistance (Claude Code), see `docs/AI_USAGE.md`.

## Commands

Node 20 or newer. Run from `app/`.

| Command | What it does |
|---|---|
| `npm install` | Install dependencies (once, and after `package.json` changes) |
| `npm run dev` | Dev server at http://localhost:5173 |
| `npm run build` | Type-check, then build to `dist/` |
| `npm run preview` | Serve the built `dist/` locally |
| `npm run lint` | ESLint |
| `npm run typecheck` | TypeScript only |

Run `npm run lint` and `npm run build` before opening a PR. Nobody merges a red build.

## Where things go

See `docs/PLAN.md` section 5 for owners.

```text
src/App.tsx           places components on the page (Eduardo)
src/state/store.ts    the one shared state; components talk only through it (Eduardo)
src/map/              MapLibre map (Eduardo)
src/types/manifest.ts types for docs/DATA_CONTRACT.md (Elias)
src/lib/data.ts       loads manifest.json and landmarks.json (Elias)
src/story/            walkthrough and explainers (Monica)
src/styles/           styles (Monica)
src/components/       layers/ and time/ (Diego); landmarks/, chart/, sources/ (Zainab)
public/data/sample/   hand-written sample data (Zainab, T-08)
```

Components never import each other. Read and write the store:

```ts
import { useAppStore } from '../../state/store';
const dateIndex = useAppStore((s) => s.dateIndex);
const setDate = useAppStore((s) => s.setDate);
```

What the map reacts to (all in `src/state/store.ts`):

| State or action | What the map does |
|---|---|
| `activeLayerId`, `dateIndex` (`setLayer`, `setDate`) | Shows that layer's frame on the left side, or the whole map when not comparing |
| `compareLayerId`, `compareDateIndex` (`setCompare`, `setCompareDate`) | Turns on the swipe and shows that frame on the right. `setCompare(null)` turns it off. Use the same layer id with another date to compare two dates. `compareDateIndex: null` means "same index as `dateIndex`". |
| `basemap` (`setBasemap('streets' \| 'satellite')`) | Street map or optical satellite imagery under the radar |
| `layerOpacity` (`setLayerOpacity(0..1)`) | Radar image opacity |
| `flyTo(center, zoom)` | Flies the camera there (story steps, landmark clicks) |

Selectors for components: `selectActiveLayer`, `selectActiveFrame`, `selectCompareLayer`, `selectCompareFrame`.

**Try it before the UI exists.** In `npm run dev`, the store is on `window.appStore`. In the browser console:

```js
appStore.getState().manifest.layers.map((l) => l.id)   // layer ids
appStore.getState().setCompare('gcov_hh', 1)           // swipe: date 0 on the left, date 1 on the right
appStore.getState().setBasemap('satellite')
appStore.getState().flyTo([-99.072, 19.436], 13)
```

## Data

The app loads `/data/<region>/manifest.json`. The region is `sample` unless `VITE_REGION_ID` is set in `app/.env.local` (see `.env.example`). If the manifest is missing, the map still shows and a warning is logged in the browser console. Frame images are placed by the layer's `bounds` and must be in Web Mercator (data contract).

## Map sources (no API keys)

| Layer | Source | License and credit |
|---|---|---|
| Street basemap | OpenFreeMap "positron" style, OpenStreetMap data | Free, no key. Credit "OpenFreeMap © OpenMapTiles Data from OpenStreetMap" (from the style) |
| Satellite imagery | EOxCloudless 2024 (Sentinel-2 cloud-free mosaic) by EOX IT Services GmbH | CC BY-NC-SA 4.0 for non-commercial use; credit must stay visible on the map |
| Radar | NISAR, from our pipeline | Credit "NISAR data: NASA and ISRO, via the ASF DAAC (provisional)" |

The credits show in the map's bottom-right corner.

## Notes

- MapLibre's worker is loaded from an explicit URL (`src/map/MapView.tsx`). Without it, tiles never load after Vite bundles the library. The deployed host must serve `.mjs` files as JavaScript.
- The swipe uses two stacked maps that share one camera; the top one is clipped to the right of the divider. Both load the basemap, so tile traffic doubles while the app is open.
