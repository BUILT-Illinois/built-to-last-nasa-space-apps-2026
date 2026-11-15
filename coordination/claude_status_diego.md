# Status: Diego        Updated: Sat 7:05 PM CT        Branch: main (status only)
Plan version read: Sat 6:25 PM | Plan v0.4: G1 passed, GS default (surface change), Oct 30, 2025 dropped (D-13), T-11 cancelled (D-15).

## Now / Next / Done
- Now:  T-30 running unattended on my second laptop (`C:\Users\dsola\...`, Python 3.12 venv, my own Earthdata login), started 7:03 PM (that laptop's clock), expected done about 7:30 PM. It uses Elias's `pipeline/fetch_crops.py` from main (PR #9, bf3b65d: 4 GUNW layers, skips existing files) through a local, uncommitted wrapper that adds 3 tries per pair and a log (`data/interim/t30_log.txt`). At 7:06 PM: 4 of 28 pairs done (2025-10-30 to 2025-12-05), 45 to 56 s each, all 761 x 723, phase 100% finite, median coherence 0.67 to 0.73, about 5.5 MB each on disk; no failures. Pair 2025-10-30 is fetched but not used (D-13). Final count and failures after the talk.
- Next: T-12 layer switcher and legend once Zainab's sample data (PR #6) is on main; then T-13 time slider (no Oct 30, 2025 frame).
- Done: T-25 findings (section at the bottom); RB-D01 accepted as D-13. T-11 cancelled (D-15).
- Done: Python 3.13 venv with `pipeline/requirements.txt` plus `earthaccess` and `scipy` (no 3.12 on this laptop; all packages installed cleanly).

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
| `mexico_city_gunw_<reference date>.npz` x 28 (T-30, in progress), on my second laptop in `data/interim/` | GUNW window crops (unwrappedPhase, coherenceMagnitude, connectedComponents, ionospherePhaseScreen) | NISAR_L2_GUNW_PROVISIONAL_V1 (P05023) | 2025-10-30 to 2026-10-01 (reference dates) | 19 / 11 asc | about 0.15 on disk (about 1 GB transferred) | n/a | for T-31 (Eduardo); move by USB or local share when he needs them |

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
