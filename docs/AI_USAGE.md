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
| Nov 14 | Elias | Codex | T-20: drafted and tested the typed managed Functions API, Azure deployment wiring, and static-only app regression test. | `api/`, `app/public/staticwebapp.config.json`, `app/src/lib/data.test.ts`, `.github/workflows/ci-deploy.yml` |
