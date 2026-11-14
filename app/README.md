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

## Data

The app loads `/data/<region>/manifest.json`. The region is `sample` unless `VITE_REGION_ID` is set in `app/.env.local` (see `.env.example`). If the manifest is missing, the map still shows and a warning is logged in the browser console.

## Notes

- No API keys in the front end. The basemap is keyless (OpenFreeMap); T-09 confirms the final choice and records attribution in `docs/SOURCES.md`.
- MapLibre's worker is loaded from an explicit URL (`src/map/MapView.tsx`). Without it, tiles never load after Vite bundles the library. The deployed host must serve `.mjs` files as JavaScript.
