# Status: Diego        Updated: Sat 10:55 PM CT        Branch: main (status only)
Plan version read: Sat 6:25 PM | Plan v0.4: G1 passed, GS default (surface change), Oct 30, 2025 dropped (D-13), T-11 cancelled (D-15).

## Now / Next / Done
- Now:  Lake check done (numbers in the new "Lake check results" section); writing it up with Monica. Data-quality FYI in RB-D04.
- Next: T-12 layer switcher and legend against the real `app/public/data/mexico_city/manifest.json`. Not started; Tier 1, so at risk for the 1:00 AM go/no-go. Then T-13 time slider (Elias's 12 monthly frames, no 2025-10-30 frame).
- FYI Eduardo (T-31): `displacement.py` is not on main yet. A top-level glob of `data/interim/mexico_city_gunw_*.npz` skips `excluded_D13/`, but `rglob` or `**` would pick up the 2025-10-30 pair, and a re-fetch of 2025-10-30 lands back in `data/interim/`. Recommend T-31 also drops 2025-10-30 by date. PLAN T-31 row still says "Runs on the 28 crops"; under D-13 it is 27. (Elias asked; answered in Slack.)
- FYI Elias (root config): the earthaccess login created an untracked `.dodsrc` in the repo root on my second laptop. Not committed; consider adding `.dodsrc` to `.gitignore`.
- Done: T-30. 28 of 28 GUNW pairs fetched on my second laptop, no failures (one timeout on 2026-04-28, retry succeeded); 7:03 to 7:30 PM, median 47 s per pair. The T-31 set is the 27 pairs from 2025-11-11 to 2026-10-01 in `data/interim/` (142 MB, all 761 x 723, phase 100% finite, median coherence 0.56 to 0.75); the 2025-10-30 pair is in `data/interim/excluded_D13/` (D-13). FYI Eduardo (T-31): there is no 2026-08-02 acquisition, so the pair starting 2026-07-21 spans 24 days, not 12. Files reach Eduardo by USB or local share; tell me which. Hand-off: DM sent to Eduardo with the file notes; waiting on his choice of USB or local share. Quick-look pictures of all 27 pairs (coherence and phase): `data/interim/views/` on my second laptop (script `data/t30/view_gunw.py`).
- Done: T-25 findings (section at the bottom); RB-D01 accepted as D-13. T-11 cancelled (D-15).
- Done: Python 3.13 venv with `pipeline/requirements.txt` plus `earthaccess` and `scipy` (no 3.12 on this laptop; all packages installed cleanly). Second laptop: Python 3.12 venv, same requirements plus earthaccess.

## Roadblocks (append-only; mark resolved, never delete)
<!-- Copy this block for each roadblock. IDs are RB-<initial><nn>, for example RB-D01.
### RB-D01  [BLOCKER | DEGRADED | FYI]  OPEN   Needed by: Sat 6:00 PM
What I was trying to do:
What happened (exact error or evidence):
What I already tried:
Impact on the plan (task IDs, timeline, tiers):
Options (2 or 3, with cost in hours):
My recommendation:
-->

### RB-D01  [FYI]  RESOLVED Sat 6:25 PM (option a accepted, D-13, plan v0.4)   Needed by: before T-10 picks its dates and before any NE-zone claim goes in the app or slides
What I was trying to do: T-25, find the cause of the NE-zone HV darkening (the flat zone north-east of the airport) so the team could use it in the story.
What happened (exact error or evidence): The darkening is most likely an artifact of the track 19 GCOV acquisition of 2025-10-30, not a ground change.
(1) In the 29 ASF browse PNGs (track 19, one release P05023), the NE zone is mean gray 112 in HV on 2025-10-30 and 12 to 36 on all 28 later GCOV dates (browse previews, not GUNW pairs); HH shows no step.
(2) On 2025-10-30 every dark pixel in the whole valley is lifted, most in HV: the darkest 4% of pixels +72 gray against their typical value, then +55, +33, +16, +6, and +4 in the brightest. A normal date (2026-03-11) shows no such pattern. That is the signature of a higher noise floor in that acquisition. It is in both the BETA (X05009) and PROVISIONAL (P05023) processing of the same acquisition.
(3) The other track (113, descending) shows no drop in the NE zone between 2025-10-25 and 2025-11-06 (BETA browse 82 then 91), and its 2025-11-06 PROVISIONAL value (29.5) already equals the later dates (29.6, 30.4).
ASF's PROVISIONAL known-issues page (updated Jul 30, 2026) does not list this; closest item: "low-level ripples ... in areas with dark backgrounds".
What I already tried: second track, comparison against control areas, brightness-binned test across all dates. Scripts and numbers: `data/t25_work/` on Diego's laptop (local).
Impact on the plan (task IDs, timeline, tiers): PLAN section 1 and the decision memo say "the dark lakebed zone north-east of the airport is clearly darker in HV in 2026"; that comparison uses the 2025-10-30 file, so it is most likely this artifact. T-10 (date choice) and T-13 / T-33 (time slider frames): a 2025-10-30 frame would show a fake change in dark areas. Without that date, the NE zone changes by under 1 dB from Nov 2025 to Oct 2026.
Options (2 or 3, with cost in hours): (a) drop 2025-10-30 from all HV layers and frames, start at 2025-11-11 (0 h); (b) keep it with a visible "acquisition artifact" note (0.25 h, confusing); (c) check real dB values for 2025-10-30 vs 2025-11-11 with remote reads (0.25 h, Elias).
My recommendation: (a), plus (c) if someone has 15 minutes, and Eduardo corrects the memo line.

### RB-D02  [DEGRADED]  PARTLY RESOLVED Sat 6:25 PM: T-11 cancelled (D-15); T-12 still waits on PR #6   Needed by: Sat 6:45 PM (after dinner)
What I was trying to do: start T-11 and T-12.
What happened (exact error or evidence): at 6:06 PM on main there is no `pipeline/render.py`, no `pipeline/tests/` (T-11 says "against given tests"), and no `app/public/data/sample/` (Zainab's status: T-08 done, PR open, not merged yet).
What I already tried: `git pull --rebase origin main` at 6:06 PM; `ls` of all three paths.
Impact on the plan (task IDs, timeline, tiers): T-11 and T-12 cannot start as written; T-10 depends on T-11.
Options (2 or 3, with cost in hours): (a) whoever wrote the exercise (Eduardo or Zainab) pushes the `render.py` skeleton and tests (0.25 h); (b) I write the stubs and tests myself from PLAN section 7 (0.5 h, and then it is not a "given tests" exercise); (c) merge Zainab's T-08 PR so T-12 can start.
My recommendation: (a) and (c) after dinner; I do T-30 in the meantime.
Update Sat 9:00 PM: T-11 cancelled (D-15). The sample data (PR #6) is still not on main, so I am starting T-12 against the real `app/public/data/mexico_city/manifest.json`, which follows the same contract.

### RB-D03  [FYI]  RESOLVED Sat 8:48 PM by PR #15; hang covered by PR #18 (hard child-process deadline + retry)   Needed by: before the next unattended fetch (Elias's overnight GCOV job, PLAN section 10)
What I was trying to do: fetch 28 GCOV window crops with `pipeline/fetch_crops.py` (`fetch_crop`) for the lake check, unattended.
What happened (exact error or evidence): `fetch_crop` hung 4 times: the HTTPS connection was dropped by the server and the process sat at zero CPU, waiting forever (no timeout, no retry). Restarted once by hand at 7:38 PM, then a watchdog restarted it 3 times (log on my second laptop: `data/interim/lake_watchdog_log.txt`). No data lost. Separately, T-30 saw one `FSTimeoutError` on 2026-04-28 (retry succeeded).
What I already tried: restarting; the script skips finished crops, so restarts are safe.
Impact on the plan (task IDs, timeline, tiers): any unattended fetch with `fetch_crops.py` (Elias's overnight frequencyA job, T-33 monthly frames) can stall silently.
Options (2 or 3, with cost in hours): (a) add a read timeout to the fsspec HTTPS session and a retry in `fetch_crop` (0.25 h, Elias); (b) run fetches under a watchdog that restarts stalled runs (0.25 h, local); (c) leave as is and check jobs by hand.
My recommendation: (a). DM to Elias sent separately.
Update Sat 10:50 PM: Elias agreed the 30 s HTTP timeout from PR #15 probably would not catch this hang (it raises no error). PR #18 runs each read in a child process that is killed at a deadline and retried, adds a GCOV exists check and tmp cleanup, and credits my approach. The helper session tested the kill-and-retry wrapper on a fake hang and a normal fetch, with no downloads.

### RB-D04  [FYI]  OPEN   Needed by: before T-31 picks its pairs, before T-13 / T-33 pick frames, and before the story uses 2025-12-05, 2026-04-16 or 2026-03-23
What I was trying to do: lake check on the 28 GCOV crops (dB per zone) and the 27 GUNW pairs (coherence per zone), plus a radar-dark water area by date.
What happened (exact error or evidence):
(1) GCOV 2025-12-05 and 2026-04-16: HH drops 2 to 3 dB in the Tlahuac-Xico zone, Bosque de Tlahuac and the NE flat zone, then recovers on the next date; the city-centre control does not drop (`data/interim/lakes_gcov_series.csv`). The radar-dark area below -14 dB HH around the lakes jumps to 7.2 and 9.2 km2 on those dates (2.2 to 3.2 km2 on the dates around them), with dark pixels spreading over land (`data/interim/water_masks_strip.png`). Same date in separate places, so most likely an acquisition-wide effect (processing, or weather at acquisition time), not a ground change.
(2) GUNW: both pairs that use the 2026-03-23 acquisition (reference dates 2026-03-11 and 2026-03-23) show a straight diagonal band of near-zero coherence across the whole crop (`data/interim/views/overview_coherence.png`). It explains the NE-zone coherence drop in those two pairs (median 0.25, 36 to 40% usable, against about 0.5 in other pairs). Cause unknown.
What I already tried: compared against two control zones, checked the neighbouring dates, looked at all 27 pairs side by side.
Impact on the plan (task IDs, timeline, tiers): T-31 (two pairs with the band), T-13 / T-33 frames (2025-12-05 and 2026-04-16 would show a fake darkening of natural areas), and any lake or water numbers in the story.
Options (2 or 3, with cost in hours): (a) leave 2025-12-05 and 2026-04-16 out of GCOV frames and water trends, and mask or drop the two 2026-03-23 pairs in T-31 (0 h); (b) check ASF known issues and the metadata of those three acquisitions (0.25 h); (c) keep them with a visible note (0 h, confusing).
My recommendation: (a) now, (b) if someone has 15 minutes.

## Reviews of other people's roadblocks
<!-- - RB-X01: AGREE / DISAGREE / ALTERNATIVE / NEED MORE INFO. One or two lines. -->

## Local data (so nobody downloads the same file twice)
All in `C:\Users\diego\Downloads\nasa data\` (outside the repo). Same files as Eduardo's; md5 checked Sat 3:43 PM. The 2026-11-06 file here has no "(2)" in its name but is the complete 6.98 GB copy, not the truncated one.

| file | product | collection | date | track/frame | GB | checksum | derived outputs |
|---|---|---|---|---|---|---|---|
| NISAR_L2_PR_GCOV_004_019_A_011_4005_DHDH_A_20251030T120539_20251030T120613_X05009_N_F_J_001.h5 | GCOV | NISAR_L2_GCOV_BETA_V1 | 2025-10-30 | 19 / 11 asc | 6.99 | cd3eddc69f6a98f027cf37357b98bc8d | `data/quicklooks/` |
| NISAR_L2_PR_GCOV_035_019_A_011_4005_DHDH_A_20261106T120539_20261106T120613_P05036_N_F_J_001.h5 | GCOV | NISAR_L2_GCOV_V1 | 2026-11-06 | 19 / 11 asc | 6.98 | 8c1d5537d8b546352b474035f0254ea4 | `data/quicklooks/` |
| NISAR_L2_PR_GUNW_032_113_D_079_033_4000_SH_20261008T011329_20261008T011403_20261020T011329_20261020T011403_P05023_N_F_J_001.h5 | GUNW | NISAR_L2_GUNW_PROVISIONAL_V1 | 2026-10-08 to 2026-10-20 | 113 / 79 desc | 2.35 | d020136a804f5888dc8af99152584820 | `data/quicklooks/` |
| 58 ASF browse PNGs, `*_NATIVE_B_HHHH.png` and `*_NATIVE_B_HVHV.png`, all 29 dates | GCOV browse | NISAR_L2_GCOV_PROVISIONAL_V1 (P05023) | 2025-10-30 to 2026-10-13 | 19 / 11 asc | 0.05 | n/a (no login, public) | `data/browse/`, `data/quicklooks/browse29_*.png` |
| 12 ASF browse PNGs (native HH/HV) + 2 BETA color browse PNGs | GCOV browse | PROVISIONAL P05023 and BETA X05009 | 2025-10-25 to 2026-01-05 (6 dates) | 113 / 79 desc | 0.01 | n/a (no login, public) | `data/browse_t113/`, `data/quicklooks/t113_northeast_HV_oct25_to_jan05.png` |
| `mexico_city_gunw_<reference date>.npz` x 27 (T-30 done; the 2025-10-30 pair is in `excluded_D13/`), on my second laptop in `data/interim/` | GUNW window crops (unwrappedPhase, coherenceMagnitude, connectedComponents, ionospherePhaseScreen) | NISAR_L2_GUNW_PROVISIONAL_V1 (P05023) | 2025-11-11 to 2026-10-01 (reference dates); the 2025-10-30 pair is in `excluded_D13/` | 19 / 11 asc | 0.142 on disk | n/a | for T-31 (Eduardo); move by USB or local share when he needs them |
| `mexico_city_gcov_<date>.npz` x 28 (lake check), on my second laptop in `data/interim/` | GCOV frequencyB window crops (HHHH, HVHV) via `pipeline/fetch_crops.py` | NISAR_L2_GCOV_PROVISIONAL_V1 (P05023) | 2025-11-11 to 2026-10-13 | 19 / 11 asc | 0.087 on disk | n/a | `data/interim/lakes_gcov_series.csv`, `lakes_gunw_pairs.csv` |
| Derived lake and water outputs, on my second laptop in `data/interim/` | `lakes_gcov_series.csv`, `lakes_gunw_pairs.csv`, `lake_series_out.txt`, `water_area_by_date.csv`, `water_masks_strip.png`, `views/*.png` (27 pair pictures plus 2 overviews) | from the GCOV and GUNW crops above | 2025-11-11 to 2026-10-13 | 19 / 11 asc | <0.05 | n/a | scripts: `data/t30/lake_series.py`, `water_area.py`, `view_gunw.py` (local, git-ignored) |

## Lake check results (Sat 10:50 PM CT). PROVISIONAL P05023, one release, track 19; "radar shows", not "we infer"

GCOV, mean of linear power in dB, 28 dates (`lakes_gcov_series.csv`):
- Every zone is brighter in Jul-Oct than in Jan-Apr 2026. HH: Tlahuac-Xico +1.5 dB, Bosque de Tlahuac +1.1, city-centre control +1.0, NE control +2.0. HV: Tlahuac-Xico +1.2, Bosque +0.9, city +0.4, NE +2.0. The lake change is inside the controls' range (the NE natural area rises more), so the radar does not show a lake-specific change over the year; natural areas in general brighten. The timing matches the rainy season (needs a cited source before the app says so).
- Nov 2025 to Sep/Oct 2026 (same season): Tlahuac-Xico HH +0.8, HV +1.1; city HH +0.5, HV -0.1. The earlier "lakes much brighter, HV +5 dB" picture mixed releases and used 2025-10-30, so it is not supported.
- The OSM Tlahuac-Xico zone is about -10 dB HH and -18.7 dB HV: not as dark as calm open water (see the outline note below).

GUNW coherence, median / usable % (`lakes_gunw_pairs.csv`):
- City centre: about 0.7 / 99.8% in every pair (good for T-31).
- Tlahuac-Xico zone: 0.24 to 0.27 / 27 to 38% in the Jun-Jul and late Sep-Oct pairs; displacement around the lakes will be patchy.

Radar-dark water area (`water_area.py`; box lon -99.07 to -98.94, lat 19.24 to 19.30, 90.8 km2, 80 m pixels, 3x3 smoothed HH, same cut-offs for all dates):
- Below -14 dB, leaving out 2025-12-05 and 2026-04-16 (RB-D04): 2.3 to 3.2 km2 Nov to Mar, 1.2 to 2.8 km2 Apr to Jun, 1.4 to 2.4 km2 Jul to Oct.
- The darkest 1% only reaches about -14 to -17 dB, and nothing is below -18 dB outside the two odd dates, so there is little calm open water in radar terms (wind, floating plants or shallow water brighten it).
- With fixed cut-offs, the rainy-season brightening of the whole scene (controls +1 to +2 dB) lowers the count even if the water stays the same. So: "less radar-dark area in Jul-Oct", not "the lake shrank".
- On every normal date the dark area sits on the Tlahuac-Xico lake. The OSM outline (lat about 19.254 to 19.263) covers only its southern edge; the dark area reaches roughly 19.29. That likely explains the -10 dB zone mean. The Bosque de Tlahuac lake is not detected at 80 m. Compare with Elias's water-persistence count in draft PR #20 (New Lake Chalco water in 7 of 12 months).

## T-25 findings (Sat 5:45 PM CT, corrected 6:10 PM)

**Correction, 6:10 PM:** finding (1) below, the NE-zone HV darkening, is most likely a data artifact of the 2025-10-30 acquisition, not a ground change. Evidence in RB-D01. Additions from Claude's analysis of the 29 GCOV browse previews (for Diego to review) are listed after the table.

**Where each finding comes from. None of it uses the 28 GUNW pairs; those are fetched in T-30.**

| Source | What it is |
|---|---|
| Local GCOV files | 2 full GCOV files, track 19: 2025-10-30 (BETA X05009) and 2026-11-06 (P05036). Real dB values. |
| Local GUNW pair | 1 GUNW pair, track 113 (descending), 2026-10-08 to 10-20. Not part of the 28-pair track 19 chain. |
| Previews | ASF browse PNGs, one per GCOV date: 29 dates on track 19 (2025-10-30 to 2026-10-13) and 6 on track 113 (2025-10-25 to 2026-01-05). 8-bit pictures: shapes and timing, approximate dB only. |

| Finding | Source | Status |
|---|---|---|
| HH vs HV basics (city, mountains, dark zones) | Local GCOV files | Stands |
| NE zone darker in HV, 2025 to 2026 | Local GCOV files, then previews | Most likely a 2025-10-30 artifact (RB-D01) |
| Noise-floor diagnosis of 2025-10-30 | Previews (track 19 and track 113) | Our diagnosis, not documented by ASF |
| South wetland brighter, 2025 to 2026 | Local GCOV files | Not confirmed by the previews |
| South wetland late-June 2026 step | Previews (29 dates) | Stands |
| Southern farm belt brighter in Jul-Oct (Claude's analysis) | Previews (29 dates) | Stands, cause open |
| NE seasonal water patches (Claude's analysis) | Previews (29 dates) | Low confidence |
| West-edge bright dots, bright in HH and HV | Local GCOV files | Stands, cause unknown |
| No sinking visible in one pair (1 to 2 cm patches everywhere) | Local GUNW pair (track 113) | Stands; the 28 track 19 pairs (T-30) are the real test |

Observations by Diego; every number checked by his Claude session against the files. Everything is PROVISIONAL. "Radar shows" is what is in the pictures; "we infer" is a guess to be checked. Place names are approximate and not yet map-checked unless stated.

Inputs: the two local GCOV files (2025-10-30 BETA X05009 and 2026-11-06 P05036, track 19 / frame 11, so a release offset of about +1.4 dB in HV and +0.5 dB in HH comes from processing alone), the local GUNW pair (track 113, 2026-10-08 to 10-20), and the 29 public ASF browse PNGs of track 19 / frame 11 (one release, 240 m pixels, 8-bit and clipped at black, so they show shapes and timing, not dB).

Pictures (on Diego's laptop in `data/quicklooks/`, shared in the team chat): `browse29_year_and_season_4panel.png`, `t113_northeast_HV_oct25_to_jan05.png`, `change_2025-10-30_to_2026-11-06_HV_freqB.png`, `browse29_south_HV.png`, `browse29_northeast_HV.png`, `gcov_*_freqA_south_composite_*.png`, `gunw_2026-10-08_to_2026-10-20_P05023_los_cm_tilt_removed.png`.

| Candidate | Radar shows | We infer (provisional) | How sure |
|---|---|---|---|
| Seasonal and year-over-year surface change | (1) NE flat zone next to the airport (about -99.00 to -98.94, 19.45 to 19.52): HV -2.1 dB from 2025-10-30 to 2026-11-06 while the whole scene rose +1.4 dB, so about 3.5 dB darker than the rest. HH +0.8 dB (scene +0.5). In the 29 browse dates the 2025-10-30 frame is the lighter one; the zone stays dark after that. (2) South wetland area (about -99.00 to -98.96, 19.26 to 19.29): black in the 2025 radar picture; HH +2.4 dB, HV +4.1 dB by 2026. In the 29 browse dates it is darkest from about 2026-05-22 to 06-15 and clearly lighter from 2026-06-27 on, in both HH and HV. A 2026 Google satellite image shows green vegetation there. | (1) **CORRECTED: most likely a 2025-10-30 acquisition artifact (RB-D01), not less vegetation.** Original guess: less vegetation; a flood is possible but untested (open water would darken HH as well, and HH did not darken). (2) Open water shrank or plants covered it, with a step in late June. | (1) Low: likely artifact. (2) The 2025-to-2026 brightening is NOT confirmed by same-release browse data (about 0 dB); the late-June 2026 step stands (medium). |
| Ground sinking | One 12-day pair: after removing the best-fit tilt, patches of 1 to 2 cm everywhere (std 1.05 cm). A blue patch over the north of the city is about the same strength as patches over the south-west mountains. Sign convention still unconfirmed. | Nothing from one pair. Worth checking whether the north-city patch persists in the 28-pair chain. | High that one pair cannot show it; matches RB-F02. |
| Soil moisture and farmland | (Claude's analysis, Diego to review) The farm and hill belt along the southern edge of the box (lat about 19.10 to 19.17) is brighter in Jul-Oct 2026 than in Jan-Apr 2026 by +3 to +9 dB in both HH and HV, the strongest seasonal change in the valley; largest patch about 55 km2 near -98.915, 19.13. | Crops growing and/or wetter soil in the rainy months (rainy-season months need a cited source). | Medium that the seasonal brightening is real (one release, 29 dates); low on the cause. |
| Urban growth at the edges | Not seen in the two dates. Bright dots at the west city edge are bright in both HH (+1.3 dB) and HV (-4.4 dB, brighter than forest at -8.6), so not plain vegetation; cause unknown (buildings at an angle to the radar, or slopes facing it). | | Low |
| Rainy-season street flooding | Not testable with these inputs. | | |

HH vs HV in general (2026, 80 m medians): HH is brightest over the city (-1.4 dB) and about 3 dB lower over the mountains. HV is similar over city (-7.8) and mountains (-8.6 to -9.8) and picks out the dark zones: NE flat zone -17.6, south wetland -13.8, airport -10.2. GUNW coherence: city 0.51, mountains 0.35 to 0.40, NE flat zone 0.21.

Also from Claude's analysis (low confidence): in Jul-Oct vs Jan-Apr 2026, 15 of 17 small patches that get darker in both HH and HV (the open-water signature) are in the NE zone, 0.2 to 1.3 km2 each. Those pixels sit near the noise floor, so treat as a hint of seasonal standing water only.

Open questions for the team: Should 2025-10-30 be dropped from HV layers (RB-D01)? What is in the southern farm belt on a map, and is it farmland? What is at the west-edge bright dots? Does the late-June step in the south line up with the rainy season (needs a cited source before the app says so)?
