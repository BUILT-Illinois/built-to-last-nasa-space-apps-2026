# Status: Diego        Updated: Sat 5:45 PM CT        Branch: main (status only)
Plan version read: Sat 4:00 PM | Roadblock IDs E for Elias, F for Eduardo; RB-M01 option (a) accepted. (Plan v0.3: one go/no-go at Sun 1:00 AM.)

## Now / Next / Done
- Now:  T-11 `pipeline/render.py` (coached exercise), started late: T-25 ran about 2 h against 1.5 h.
- Next: T-12 layer switcher and legend against `app/public/data/sample/`.
- Done: T-25 findings, see the section "T-25 findings" at the bottom of this file. The story choice is the team's (GS); no decision is in `DECISIONS.md` yet.
- Done: Python 3.13 venv with `pipeline/requirements.txt` (no 3.12 on this laptop; all packages installed cleanly).

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

## T-25 findings (Sat 5:45 PM CT)

Observations by Diego; every number checked by his Claude session against the files. Everything is PROVISIONAL. "Radar shows" is what is in the pictures; "we infer" is a guess to be checked. Place names are approximate and not yet map-checked unless stated.

Inputs: the two local GCOV files (2025-10-30 BETA X05009 and 2026-11-06 P05036, track 19 / frame 11, so a release offset of about +1.4 dB in HV and +0.5 dB in HH comes from processing alone), the local GUNW pair (track 113, 2026-10-08 to 10-20), and the 29 public ASF browse PNGs of track 19 / frame 11 (one release, 240 m pixels, 8-bit and clipped at black, so they show shapes and timing, not dB).

Pictures (on Diego's laptop in `data/quicklooks/`, shared in the team chat): `change_2025-10-30_to_2026-11-06_HV_freqB.png`, `browse29_south_HV.png`, `browse29_northeast_HV.png`, `gcov_*_freqA_south_composite_*.png`, `gunw_2026-10-08_to_2026-10-20_P05023_los_cm_tilt_removed.png`.

| Candidate | Radar shows | We infer (provisional) | How sure |
|---|---|---|---|
| Seasonal and year-over-year surface change | (1) NE flat zone next to the airport (about -99.00 to -98.94, 19.45 to 19.52): HV -2.1 dB from 2025-10-30 to 2026-11-06 while the whole scene rose +1.4 dB, so about 3.5 dB darker than the rest. HH +0.8 dB (scene +0.5). In the 29 browse dates the 2025-10-30 frame is the lighter one; the zone stays dark after that. (2) South wetland area (about -99.00 to -98.96, 19.26 to 19.29): black in the 2025 radar picture; HH +2.4 dB, HV +4.1 dB by 2026. In the 29 browse dates it is darkest from about 2026-05-22 to 06-15 and clearly lighter from 2026-06-27 on, in both HH and HV. A 2026 Google satellite image shows green vegetation there. | (1) Less vegetation on the NE zone; a flood is possible but untested (open water would darken HH as well, and HH did not darken). (2) Open water shrank or plants covered it, with a step in late June. | Medium that something changed in both places (well above the release offset, sharp edges). Low on the causes. |
| Ground sinking | One 12-day pair: after removing the best-fit tilt, patches of 1 to 2 cm everywhere (std 1.05 cm). A blue patch over the north of the city is about the same strength as patches over the south-west mountains. Sign convention still unconfirmed. | Nothing from one pair. Worth checking whether the north-city patch persists in the 28-pair chain. | High that one pair cannot show it; matches RB-F02. |
| Soil moisture and farmland | Not looked at. | | |
| Urban growth at the edges | Not seen in the two dates. Bright dots at the west city edge are bright in both HH (+1.3 dB) and HV (-4.4 dB, brighter than forest at -8.6), so not plain vegetation; cause unknown (buildings at an angle to the radar, or slopes facing it). | | Low |
| Rainy-season street flooding | Not testable with these inputs. | | |

HH vs HV in general (2026, 80 m medians): HH is brightest over the city (-1.4 dB) and about 3 dB lower over the mountains. HV is similar over city (-7.8) and mountains (-8.6 to -9.8) and picks out the dark zones: NE flat zone -17.6, south wetland -13.8, airport -10.2. GUNW coherence: city 0.51, mountains 0.35 to 0.40, NE flat zone 0.21.

Open questions for the team: Is the NE darkening vegetation loss or water (needs real per-date numbers; remote reads work per Elias's T-01)? What is at the west-edge bright dots? Does the late-June step in the south line up with the rainy season (needs a cited source before the app says so)?
