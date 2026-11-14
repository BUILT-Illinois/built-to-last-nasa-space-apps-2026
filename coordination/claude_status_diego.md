# Status: Diego        Updated: Sat 3:45 PM CT        Branch: main (status only)
Plan version read: Sat 3:10 PM | Plan v0.2 approved by Eduardo and in force.

## Now / Next / Done
- Now:  T-25 data exploration. Whole-valley 80 m quicklooks done on my laptop (same 3 files as Eduardo, md5 match). Next: 10 m zooms, then the 29-date ASF browse PNGs (no login, about 190 MB). Findings at the 4:30 PM standup.
- Next: T-11 `render.py`, then T-12 layer switcher against sample data.
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
