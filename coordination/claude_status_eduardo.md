# Status: Eduardo        Updated: Sun 8:30 AM CT        Branch: main (status only)
Plan version read: Sun 7:45 AM, plan v0.5 plus D-19 and the 7:45 AM CHANGELOG line (9:00 AM cutoff, approved cuts)

## Now / Next / Done
- **Decision (Sun 8:25 AM, Eduardo): merge order before the 9:00 AM cutoff is #35 first, then Diego's UI PR.** Done for #35: it failed the Python tests because `pipeline/build_manifest.py` wrote only `nisar-gcov` into the manifest `sources[]` while Monica's cards cite six sources. #40 fixes it (`merge_sources()`, plus a unit test; Elias, FYI, your file), merged 8:15 AM. #35 (intro, six-step tour, reading guide, provisional badge, card text) merged 8:25 AM after the full gate; live on Azure with 0 console errors, the ground-motion layer and legend intact, 7 landmarks, no sideways scroll at 390 px. **Diego: `App.tsx` now also places `<StoryTour />` and the reading guide. Merge `main` into your UI branch before asking for review, and keep both the tour and the layer controls on the page.**
- **Diego, please send me the 27 valley-wide GUNW crops now** (the zip you prepared for me; `data/interim/valley_wide/`, box lon -99.60 to -98.60, lat 19.00 to 19.90), by USB or LocalSend. Only the GUNW pairs, not the GCOV. I rerun `poc/mexico_city_sinking/` on them to show the sinking against its surroundings, then Elias re-ingests the sinking layer with the larger bounds. Target: merged and checked live by 8:45. This comes before your UI PR only because it takes you 2 minutes.
- Now:  1:1 with Monica on the project page and deck (#38, her call). Reviewing and merging PRs before the 9:00 AM cutoff: Diego's UI proof of concept first, then #35 (tour and cards), then #20 if it's live by 8:30.
- Next: G5 link check at 10:30 AM; submission at 12:00 PM.
- Done (overnight, with Claude Code; every merge passed CI and was checked on the live Azure URL with 0 console errors):
  - #24 sinking layer (main merged in; description fixed to positive = away)
  - #30 layer switcher and legend (re-reviewed: items 1 to 4 and nits 8 to 10 fixed)
  - #37 placement in `App.tsx`
  - #36 removed the 3 `gcov_19_*` debug landmarks (7 left)
  - #32 Diego's AI-usage rows
  - #39 `.gitignore` for going public
  - Repo made public; the secrets scan of all branches and history is clean
  - Draft #38 opened for Monica (project page, deck outline, claim table; fact-checked)
  - Earlier: #25, #26, #27; D-19; plan v0.5

## Morning briefing, Sun Nov 15, 7:45 AM (everyone: read this first)

**Cutoff for additions moved: 9:00 AM** (was 8:00). After 9:00, only text changes and bug fixes. G5 link check is still at 10:30, submission at 12:00, and the hard local deadline at 1:30 PM (no edits after it).

### Where we are (7:35 AM)

- **Live site:** https://yellow-desert-02401091e.4.azurestaticapps.net (fallback: https://built-to-last-6or.pages.dev).
  - On the site now: the radar layers (HH, HV, composite) and the **ground-motion layer**, which shows both sinking bowls.
  - Also live: the **layer switcher and legend** (cm/yr, line of sight, "positive = away from the satellite", PROVISIONAL badge) and **exactly 7 landmarks** in the data.
- **Merged overnight:** #24 (Elias, sinking layer), #30 (Diego, switcher and legend), #37 (placement on the page), #36 (debug points removed), #32 (Diego's AI-usage rows), #39 (.gitignore).
  - Every merge passed CI.
  - After each merge we checked the live site: no console errors.
- **The repo is public.** No secrets are in the code or its history.
- **Still missing from Tier 1:**
  - landmark cards on the map (#35 / T-14)
  - the polarization explainer (T-23)
  - the sources page (T-24)
  - the flood-priority map (#20)

### Elias

- **Flood-priority map (#20):** it stays in only if it's rebased on `main`, passes CI and is working on the live site **by 8:30**. That leaves time to check it before the 9:00 cutoff.
- If it won't make 8:30, stop. It becomes the "what's next" slide.
- After that, finish or close #34 and #31, and run the smoke tests on both hosts.
- FYI: #36 removed the three `gcov_19_*` points from `landmark_series.py`. If #20 needs them, keep them in that pipeline, not in the published landmarks.

### Monica

- **Quick OK for Diego:** his UI touches `app/src/styles/base.css` (your file).
- **First, #35 (tour and landmark cards).** It is the biggest Tier 1 gap.
  - `App.tsx` now places the layer controls, so merge `main` into #35 first.
  - Then mark it ready for review, by **8:30** at the latest.
- **Submission drafts (#38):** your call. Eduardo will meet with you 1:1 to walk through the project.
  - Every number in the drafts is traced in `docs/submission/CLAIMS.md`. Please don't add numbers that aren't in it.
- **Deck in Canva:** 7 slides max. The pitch script in `DECK_OUTLINE.md` runs 3:45.
- **Still to fill in:** the project name, the demo link, Diego's and Zainab's last names (you have them on Slack), and the personal connection (only with the member's consent).

### Diego

- **First: ship your UI proof of concept (`diego/ui-poc`).** The team chose it because the current UI is lacking. Have the PR ready for review **by 8:30**, so it merges and gets checked live before 9:00.
  - Start a fresh branch from `main`, then `git cherry-pick b9feea7`. That brings only the UI commit. The rest of `diego/ui-poc` is older copies of #24 and #30, which would conflict.
  - Resolve the commit onto the current `Legend.tsx` and `LayerSwitcher.tsx` from #30. Keep every review fix from items 1–4 and nits 8–10, and keep their tests passing.
  - **Approvals:** Eduardo approves the `App.tsx` change. Monica, `base.css` is your file, so please give Diego a quick OK.
  - **Font:** the Archivo font loads from Google Fonts. Either self-host it, or add a row to `docs/SOURCES.md` and keep a system-font fallback in case the venue's web filter blocks it.
  - **`ViewOptions`:** its swipe-compare control is what makes the swipe and dates reachable on the page. Make sure it works on the Mexico City data, comparing Nov 2025 against Oct 2026.
  - **Checks before asking for review:**
    - lint, tests and the `mexico_city` build pass
    - 0 console errors
    - the ground-motion layer shows both bowls, with the legend's line-of-sight and "positive = away" text intact
    - no sideways scroll at 390 px, with the bottom sheet usable on a phone
- **Then:** a phone walkthrough of the live site, a bug list, and the deck screenshots (default view, ground-motion layer with legend, HH swipe Nov vs Oct, phone view).
- **After 9:00:** fixes only. Review items 5 and 6 from #30 can go in as fixes if they're small.

### Zainab

- **Project page:** fill in the References and Use of SI fields, from `docs/AI_USAGE.md` and `docs/SOURCES.md`.
- **Sources (T-24):**
  - `SOURCES.md` line 32 still says the basemap is TBD. It's OpenFreeMap with OpenMapTiles and OpenStreetMap data.
  - If a sources page in the app can't land by 9:00, link `docs/SOURCES.md` from the project page instead.
- **Landmark panel (T-14):** coordinate with Monica on #35 so you don't both build cards.

### Cuts (approved by Eduardo, 7:45 AM)

1. **Flood-priority map:** it becomes a "what's next" slide unless it's live by 8:30.
2. **Time slider (T-13):** cut. The swipe compare in Diego's UI (`ViewOptions`) covers comparing dates.
3. **Not cut:** Diego's UI proof of concept ships before 9:00 (see Diego).
4. **After 9:00 AM:** text and bug fixes only, no new features.
5. Already cut in plan v0.5 and still cut: Venezuela, Tier 3, the borough layer (T-21), T-16.

## Roadblocks (append-only; mark resolved, never delete)
### RB-F01 (was RB-E01)  [FYI]  RESOLVED Sat 6:25 PM   Needed by: Sat 4:30 PM
What I was trying to do: check whether the downloaded files can be used together in the app.
What happened (exact error or evidence): the two GCOV files are different processing releases (`compositeReleaseId` X05009 = BETA for 2025-10-30, P05036 for 2026-11-06). The HV difference between them has a scene-wide median of +1.36 dB, which is probably processing and not the ground. A third file is truncated: `h5py` reports `truncated file: eof = 104904968, stored_eof = 6983516160`.
What I already tried: confirmed in the catalog CSV that a PROVISIONAL (P05023) version of the 2025-10-30 scene exists.
Impact on the plan (task IDs, timeline, tiers): T-10 must use two GCOV dates of one release. T-25 conclusions from the current pair are about patterns, not numbers.
Options (2 or 3, with cost in hours): (a) read both dates from the PROVISIONAL collection remotely once T-01 works, 0 extra hours; (b) download the PROVISIONAL 2025-10-30 file, 7 GB, about 26 min; (c) keep the mixed pair and say so in the app.
My recommendation: (a), with (b) as the G1 fallback.
Update Sat 3:10 PM: the truncated file was deleted on Eduardo's instruction. Fallback (b) is pre-approved.
Resolved Sat 6:25 PM: G1 passed, so option (a) is in use. T-10 reads PROVISIONAL (P05023) scenes remotely and the fallback downloads are cancelled.

### RB-F02 (was RB-E02)  [FYI]  OPEN   Needed by: Sat 5:30 PM
What I was trying to do: see whether ground sinking shows in the one GUNW pair we have (track 113, 2026-10-08 to 2026-10-20).
What happened (exact error or evidence): raw line-of-sight change over the box spans -4.3 to +2.9 cm (2nd to 98th percentile) as a smooth tilt. After removing a best-fit plane the spread is still about 1 cm (standard deviation 0.96 to 1.01 cm), with blobs over the mountains as large as those over the city.
What I already tried: masking coherence below 0.4, subtracting the ionosphere layer, removing a plane.
Impact on the plan (task IDs, timeline, tiers): T-30 to T-34. Ground motion cannot be shown from one or a few pairs. It needs the chain of pairs and gate G3.
Options (2 or 3, with cost in hours): (a) keep it as Tier 2 behind G1 and G3; (b) drop it and make surface change the whole story.
My recommendation: the team decides at GS (5:30 PM) after T-25.
Update Sat 4:00 PM: G3 is merged into G2 at Sun 1:00 AM (plan v0.3, D-12). Renamed from RB-E01 and RB-E02 because Elias uses E.
Resolved Sat 11:30 PM: the 27-pair chain reproduces the sinking (`poc/mexico_city_sinking/README.md`). Ground motion is Tier 1 in plan v0.5 (D-16).

### RB-F03  [DEGRADED]  RESOLVED Sun 6:55 AM   Needed by: Sun 12:45 AM (before landmarks.json gets numbers)
What I was trying to do: hand the line-of-sight numbers to the landmark cards and the sinking layer.
What happened (exact error or evidence): `docs/DATA_CONTRACT.md` says `los_displacement_cm` "Negative means away from the satellite". Our files (`poc/mexico_city_sinking/landmark_series_los_cm.csv`, `displacement_cumulative.npz`, `los_rate_cm_per_year.tif`) are positive = away, and T-35 (`docs/T35_SIGN_CHECK.md`, PR #27) confirms NISAR's native phase is positive = away.
What I already tried: documented the sign in `provenance.json` (PR #26) and in the memo rows (PR #27).
Impact on the plan (task IDs, timeline, tiers): T-19 cards, T-15 chart, T-33 layer, T-34 flood map. A wrong sign shows sinking as uplift.
Options (2 or 3, with cost in hours): (a) change the contract to positive = away, one line by Elias plus a DECISIONS.md entry (0.1 h); (b) keep the contract and multiply by -1 when writing landmarks.json and the layer (0.1 h, easy to forget in one place).
My recommendation: (a). Elias, please confirm; I add the decision line.
Update Sun 1:45 AM: Elias signed off (a) at 12:57 AM and changed `docs/DATA_CONTRACT.md` to positive = away on the PR #24 branch (f1b668d). D-19 records the sign itself. Closes when #24 merges.

Resolved Sun 6:55 AM: #24 merged with `docs/DATA_CONTRACT.md` at positive = away (D-19).

### RB-F04  [BLOCKER]  RESOLVED Sun 6:55 AM   Needed by: now (G2 was Sun 1:00 AM)
What I was trying to do: hand Elias the citywide line-of-sight rate raster for the T-33 ground-motion layer.
What happened (exact error or evidence): Elias reports (status, 12:57 AM) that the first `los_rate_cm_per_year.tif` I sent was invalid: uint32 and no CRS. His ingest in #24 is ready and waits on a float32 EPSG:32614 file, zipped. Not re-checked on my side yet.
What I already tried: nothing yet since his report.
Impact on the plan (task IDs, timeline, tiers): T-33 ground-motion layer (Tier 1, G2), T-34 flood map (uses the same rates), Diego's #30 (based on #24).
Options (2 or 3, with cost in hours): (a) re-export the GeoTIFF from `displacement_cumulative.npz` as float32 with the EPSG:32614 grid of the crops, check it with `gdalinfo`, zip and send over LocalSend (0.25 h, needs a Python env with numpy and rasterio); (b) send Elias the npz plus the grid transform and he writes the GeoTIFF (0.25 h of his time).
My recommendation: (a).

Resolved Sun 6:55 AM: #24 merged with the corrected float32 EPSG:32614 raster; the live layer shows both bowls.

## Reviews of other people's roadblocks
- RB-D01: AGREE with (a). Eduardo decided at 6:20 PM to drop Oct 30, 2025 from every layer and frame (D-13, plan v0.4). The memo and plan lines are corrected. Option (c), real dB values for Oct 30 against Nov 11, is still welcome if Elias has 15 minutes, but nothing waits on it.
- RB-D02: T-11 is cancelled (plan v0.4); the plan never assigned anyone to write its starter and tests. AGREE with (c): T-12 starts when PR #6 merges.
- RB-M01: AGREE with (a), done at 4:00 PM: T-06 claims 1 to 7 are rows in the decision memo table. (b) the HV definition and dark/bright guidance are still needed before T-23.

## Local data (so nobody downloads the same file twice)
All in `Datasets/` at the repo root on Eduardo's laptop (git-ignored).

| file | product | collection | date | track/frame | GB | checksum (md5) | derived outputs |
|---|---|---|---|---|---|---|---|
| NISAR_L2_PR_GCOV_004_019_A_011_4005_DHDH_A_20251030T120539_20251030T120613_X05009_N_F_J_001.h5 | GCOV | NISAR_L2_GCOV_BETA_V1 | 2025-10-30 | 19 / 11 asc | 6.99 | cd3eddc69f6a98f027cf37357b98bc8d | `data/quicklooks/gcov_2025-10-30_*`, `change_*` |
| NISAR_L2_PR_GCOV_035_019_A_011_4005_DHDH_A_20261106T120539_20261106T120613_P05036_N_F_J_001 (2).h5 | GCOV | NISAR_L2_GCOV_V1 | 2026-11-06 | 19 / 11 asc | 6.98 | 8c1d5537d8b546352b474035f0254ea4 | `data/quicklooks/gcov_2026-11-06_*`, `change_*` |
| NISAR_L2_PR_GUNW_032_113_D_079_033_4000_SH_20261008T011329_20261008T011403_20261020T011329_20261020T011403_P05023_N_F_J_001.h5 | GUNW | NISAR_L2_GUNW_PROVISIONAL_V1 | 2026-10-08 to 2026-10-20 | 113 / 79 desc | 2.35 | d020136a804f5888dc8af99152584820 | `data/quicklooks/gunw_2026-10-08_*` |
