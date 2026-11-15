# AI usage log

Running record of where and how AI tools were used in this project. It is the source for the "Use of Super Intelligence (SI)" field on the project page. Owner: Zainab. Everyone adds a row when an AI tool produces something that ships.

Rules we follow (from the 2026 Project Submission Guide, summarized in `docs/challenge/README.md`):

- Every file an AI tool wrote or substantially drafted carries a notice in a header comment, or in a `_comment` or `generatedBy` field for JSON.
- AI-generated images and video need a visible watermark. We do not plan to generate any.
- AI-generated content never uses or modifies NASA logos, flags, or mission identifiers.
- The idea and the story are the team's decision. AI tools were used to check what the data supports and to plan and write code.

| Date | Who | Tool | Used for | Files |
|---|---|---|---|---|
| Nov 14 | Eduardo | Claude Code | Reading the 2026 guides and summarizing requirements | `docs/challenge/README.md` |
| Nov 14 | Eduardo | Claude Code | Catalog search script and region config; ran the search | `pipeline/search_granules.py`, `pipeline/config/regions.json`, `pipeline/reports/*` (the reports are script output from NASA's ASF catalog, not generated data) |
| Nov 14 | Eduardo | Claude Code | Drafting the plan, decision memo, data contract, and decisions log, including web lookups of NASA, JPL, and ASF pages for sourcing | `docs/PLAN.md`, `docs/DECISION_MEMO.md`, `docs/DATA_CONTRACT.md`, `docs/DECISIONS.md` |
| Nov 14 | Eduardo | Claude Code | Quick-look script for local NISAR files; ran it on the downloaded files and described what the pictures show (the pictures are renderings of NASA data, not generated imagery) | `pipeline/quicklook.py`, `data/quicklooks/*` (not in git) |
| Nov 14 | Eduardo | Claude Code | Coordination files from the team's protocol template | `coordination/*` |
| Nov 14 | Eduardo | Claude Code | T-02 app scaffold: Vite, React, TypeScript, MapLibre map, shared state store, data contract types and loader stubs, lint and build config | `app/*` (except `node_modules/`, `dist/`) |
| Nov 14 | Elias | Codex | T-03 ([PR #3](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/3), `60ef264`): drafted the authenticated NISAR crop fetcher and its offline smoke test. The PR also added their dependencies. | `pipeline/fetch_crops.py`, `pipeline/test_fetch_crops.py`, `pipeline/requirements.txt` (dependency updates) |
| Nov 14 | Elias | Codex | T-04 ([PR #4](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/4), `db39282`): drafted the workflow that runs lint, tests, and build checks on PRs and publishes the same app build from `main` to Azure Static Web Apps and Cloudflare Pages. | `.github/workflows/ci-deploy.yml` |
| Nov 14 | Elias | Codex | Drafted the monthly GCOV frequency-B batch runner and added restart handling. The script caches NASA/ISRO data locally for T-33. | `data/fetch_monthly_gcov.py` |
| Nov 14 | Elias | Codex | Added the primary Azure and fallback Cloudflare links and checked both endpoints. | `README.md` (Live URLs section) |
| Nov 14 | Elias | Codex | Drafting and testing the GCOV data build and reprojection | `pipeline/build_manifest.py`, `pipeline/test_build_manifest.py`, `pipeline/requirements.txt` |
| Nov 14 | Elias | Codex | T-33: extended the GCOV build and tests to accept monthly dates, then rendered and validated the 12 cached NISAR scenes. | `pipeline/build_manifest.py`, `pipeline/test_build_manifest.py`, `app/public/data/mexico_city/` (derived from NISAR data) |
| Nov 14 | Elias | Codex | Added HTTP read timeouts and retry tests, checked the April GCOV crop, and prepared the local overnight frequency-A reads. | `pipeline/fetch_crops.py`, `pipeline/test_fetch_crops.py`, `pipeline/requirements.txt`, local scripts under `data/` |
| Nov 14 | Elias | Codex | Implemented and tested Diego's hard child-process timeout and retry approach for NISAR window reads. | `pipeline/fetch_crops.py`, `pipeline/test_fetch_crops.py`, `data/fetch_monthly_gcov.py`, `data/fetch_landmark_windows.py` |
| Nov 14 | Elias | Codex | Made monthly GCOV selection and crop caching region-aware and tested a configured region offline. | `pipeline/config/regions.json`, `pipeline/fetch_crops.py`, `data/fetch_monthly_gcov.py`, `pipeline/build_manifest.py`, `pipeline/test_build_manifest.py` |
| Nov 14 | Elias | Codex | T-20: drafted and tested the typed managed Functions API, Azure deployment wiring, and static-only app regression test. | `api/`, `app/public/staticwebapp.config.json`, `app/src/lib/data.test.ts`, `.github/workflows/ci-deploy.yml` |
| Nov 14 | Elias | Codex | Drafted a small radar-themed favicon and linked it in the app. | `app/public/favicon.svg`, `app/public/favicon.ico`, `app/index.html` |
| Nov 14 | Diego | Claude Code | T-25: ran `pipeline/quicklook.py` on the local files, wrote throwaway scripts that checked the 29 GCOV browse previews and a second track, found the 2025-10-30 acquisition artifact behind D-13, checked Diego's own observations against the data, and drafted his findings and roadblocks (the pictures are renderings of NASA data, not generated imagery) | `coordination/claude_status_diego.md`; local, uncommitted scripts in `data/t25_work/` |
| Nov 14 | Diego | Claude Code | T-30: wrapper that runs `pipeline/fetch_crops.py` for every GUNW pair with retries and a log; lake check for the story (real dB per date and coherence per pair over OpenStreetMap lake outlines) and an open-water area count | local, uncommitted: `data/t30/run_t30.py`, `data/t30/lake_series.py`, `data/t30/water_area.py` |
