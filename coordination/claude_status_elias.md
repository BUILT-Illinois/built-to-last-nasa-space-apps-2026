## For Eduardo's agent — valley region and one-map swap

- Does PR #45 (`mexico_city_valley` radar coverage) get a feature freeze exception to merge?
- Are you producing the wider valley sinking raster in PR #26 format (float32 GeoTIFF, EPSG:32614, NaN nodata, annualized LOS cm/yr, positive away) for lon −99.60 to −98.60 and lat 19.00 to 19.90? The one-map swap depends on this raster. Please share its status and expected handoff.

## For Diego

UI audit is in coordination/ui_audit_for_diego.md (merged in #47, c477238). Top two: on a phone the layer panel covers the map, and tour step 5 hides the swipe grip and pushes Next below the fold. Check against #41 before fixing. Touch swipe on a real phone is still unverified.

Elias status (12:57 AM Sun)
DONE: API live on Azure and Cloudflare. Merged #13, #15, #17, #18, #19. The published Mexico City map has 11 GCOV acquisition months and 11 frames per radar layer after D-17.
SIGNED OFF: RBF-03 sign mismatch (Elias, 12:57 AM). LOS positive = away from the satellite, matching Eduardo's #26 files. DATA_CONTRACT.md updated on the PR #24 branch (f1b668d). Still pending: Eduardo's DECISIONS.md line and T-35 confirmation.
OPEN PRs: #24 sinking ingest (draft, waits on raster + T-32). #22 smoke checks (CI green). #28 landmark backscatter series (CI green). #29 AI usage audit (docs only).
PARKED: T-34 flood map (Eduardo, 11:05 PM). PR #20 stays a draft.
BLOCKED: citywide sinking layer. The first los_rate_cm_per_year.tif from Eduardo was invalid (uint32, no CRS). Waiting on the real float32 EPSG:32614 file, zipped. The ingest runs as soon as it lands.
REVIEWS: #26 OK'd by Diego.

G2 CHECKLIST (1 AM)
Go = map + sinking + landmarks working end to end.
• Done: both sites load with zero console errors. The API is live.
• Needed: map with radar frames and time slider (T-09, Eduardo)
• Needed: citywide sinking layer (Elias). Ingest ready, waiting on a valid raster. Diego building the toggle and legend.
• Needed: Monica's 7 landmark cards served by the API (PR #21 into landmarks.json)
• Needed: story locked. Option: "Mexico City is sinking up to 2 cm a month, and the old lake is coming back. NISAR lets us watch it happen."
• Can wait until the 8 AM freeze: guided tour (PR #21)
• Caracas: dropped at the 11:30 PM cutoff

## For #38 owners (Monica, Eduardo): claim fixes before submission

Files are under docs/submission/. Line numbers are from PR #38.
• PROJECT_PAGE.md:18,20,24,162, DECK_OUTLINE.md:20,84, CLAIMS.md:104,119,132: use Project Lago and the exact tagline "See the city sink and the lake breathe, from space." Remove the old "measured a year" wording.
• PROJECT_PAGE.md:58,66,98,125,128,176, DECK_OUTLINE.md:27,100, CLAIMS.md:14,52: replace "year", "full year" and "one year" with 336 days (Nov 11, 2025 to Oct 13, 2026) for GUNW. Describe GCOV as 11 observed months, with April 2026 missing. Keep cm/yr where it means an annualized rate.
• PROJECT_PAGE.md:24,76-98,139, DECK_OUTLINE.md:26-27,42-45,88,100, CLAIMS.md:15-22,31: label landmark rates, sinking bowls, area thresholds and the WorldPop overlay as preliminary team estimates from provisional NISAR data. Keep LOS explicit, and mark area and population figures as PoC estimates.
• PROJECT_PAGE.md:98, DECK_OUTLINE.md:26-27,88,100, CLAIMS.md:32,38: attribute the ~2 cm/month at Nezahualcoyotl to the team. Paraphrase JPL as reporting more than 2 cm/month in parts of the region, and as describing the airport as near the image center. JPL notes the Angel needed 14 added steps. The ~0.4 cm/month at PROJECT_PAGE.md:87 is the team's estimate. Source: JPL's April 29, 2026 release.
• PROJECT_PAGE.md:125, DECK_OUTLINE.md:58,108, CLAIMS.md:23: call -2.2 cm the hills control-point drift over 336 days. Drop the claim that it sets ~2 cm uncertainty for every number.
• PROJECT_PAGE.md:11,24,57-59, DECK_OUTLINE.md:14,46,96, CLAIMS.md:92,101: describe the merged layer and legend as annualized LOS rate in cm/yr, with a provisional label. Keep the landmark-card demo conditional on a live check.
• PROJECT_PAGE.md:60,135, CLAIMS.md:102,165: keep the flood layer as a planned screening tool that ranks where LOS motion and possible standing water overlap. Keep the 2024 flood as historical context only.
• PROJECT_PAGE.md:168,240,260, DECK_OUTLINE.md:12,22,28,46,60, CLAIMS.md:120-121: add visible text credit for NASA/ISRO NISAR data and NASA/JPL context. If using JPL's image (PIA26709), credit NASA/JPL-Caltech/David Bekaert. No NASA logos, and no wording that implies endorsement.
• PROJECT_PAGE.md:158, CLAIMS.md:118,151: remove the stale note asking for a drafting disclosure. #38 already adds it to docs/AI_USAGE.md.
• DECK_OUTLINE.md:121, CLAIMS.md:141: slide 6's script is 83 words. Recount and rehearse after edits.
• docs/PLAN.md:269 marks T-32 done only as a PoC sanity check. Keep public estimates preliminary and source data PROVISIONAL.

docs/PLAN.md:383 still says full year; change to 11 months (Eduardo).

## Status

- #20 out (now the what's-next slide).
- Done: [#34](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/34) merged as `18fff2c` and is live on Azure and Cloudflare. Both hosts returned 200 on `/api/regions/sample/manifest`.
- [#31](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/31) stays open. `/api/manifest` still returns 404 on both hosts.

## Valley GCOV (Sun 9:05 AM CT)

- [#45](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/45) is open with CI green. The new `mexico_city_valley` region has 11 dates each for HH, HV and composite, using the same city GCOV acquisition list and D-13/D-17 exclusions. The 33 overlays and two JSON files total 25.31 MB. Both GCOV bundles and both app builds passed. `/api/regions` lists the valley in the PR build. Diego can use the existing `loadRegion("mexico_city_valley")` for the UI.
- **Eduardo** — The valley region has GCOV only. A sinking layer over the wider extent needs a LOS-rate raster for that area in the same format as #26 (float32 GeoTIFF, EPSG:32614, NaN nodata, cm/yr positive away). Can you produce one for lon −99.60 to −98.60 and lat 19.00 to 19.90?
- **Monica** — The #34 live check at `18fff2c` found 7 landmarks with sources and a working tour on both hosts. I couldn't see standalone landmark cards. Do those open when you click a landmark, or does #35 still need to wire them up?
