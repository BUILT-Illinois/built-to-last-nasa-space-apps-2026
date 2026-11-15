<!-- Drafted with AI assistance (Codex); see docs/AI_USAGE.md. -->
# T-20 managed API

Azure Static Web Apps Free hosts these anonymous, read-only HTTP functions under
`/api` with Node.js 22. No separate Azure resource or data service is needed.
The API packages the manifest and landmark JSON from `app/public/data/` at build
time. Only published regions are listed. The static files and images still ship
in `app/dist`, and the web app uses those files directly.

From `api/`, using Node.js 22:

```sh
npm ci
npm run build
npm test
```

To exercise the HTTP routes locally, install Azure Functions Core Tools v4 and
run `func start` from `api/` with `FUNCTIONS_WORKER_RUNTIME=node`. The default
local URL is `http://localhost:7071`. On Azure the same routes are on the app's
origin. Cloudflare Pages serves the same routes from the shared data bundle:

- `GET /api/health` returns the Git SHA included at build time.
- `GET /api/regions` lists published region IDs, names, and bounding boxes.
- `GET /api/regions/sample` and `GET /api/regions/sample/manifest` return the synthetic sample manifest.
- `GET /api/regions/sample/landmarks` returns the sample landmarks.
- `GET /api/regions/mexico_city/manifest` returns the published manifest.
- `GET /api/regions/mexico_city/landmarks` returns the published landmarks file.
- An unknown region ID on any region file route returns a JSON 404.

For the static-only build, set `VITE_REGION_ID=mexico_city`, run
`npm run build` from `app/`, and serve `app/dist` with any static server.
Do not start Functions for this check. The map reads from `/data/mexico_city/`.
The CI deploys the same static artifact to Azure and to the static fallback host.
