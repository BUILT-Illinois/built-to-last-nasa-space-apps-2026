# Status: Elias        Updated: Sat 3:48 PM CT        Branch: elias/backend
Plan version read: Sat 3:10 PM CT, plan v0.2 approved and in force

Schedule update from Elias relaying Eduardo: G2 go/no-go moved from Sat 9:30 PM to Sun 1:00 AM CT. The checked-in plan still lists 9:30 PM. No revised G3 time or Tier 1 live deadline was provided.

## Now / Next / Done
- Now: [PR #1](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/1) is open to `main` for Zainab's T-08 fixture handoff. `git check-ignore` confirmed that public manifests, landmark data, WebP, and GeoJSON are stageable and that raw files, interim crops, and the local identity file are ignored.
- Next: Present T-01 evidence at G1, Sat 4:30 PM CT. Continue with T-03 after the probe handoff.
- Done: T-01 Earthdata login succeeded and both track 19 / frame 11 PROVISIONAL P05023 windows were read over HTTPS. GCOV frequency B HH/HV: 31.9 s, 14.16 MB, 28 range requests. GUNW unwrapped phase: 21.0 s, 9.74 MB, 20 range requests. Both crops are 761 × 723 cells. Time includes opening the HDF5 and reading the grid; MB is HTTP file response payload. No whole granules downloaded. Crops and quicklook PNGs are in `data/interim/t01_{gcov,gunw}.{npz,png}`.
- Done: Created the ignored Python 3.12.15 virtual environment. Installed and import-checked the probe dependencies, including earthaccess and rasterio.
- Done: Local identity and Codex instructions set up. T-04 deploy checklist prepared (due Sat 6:00 PM CT). Azure setup waits for Elias to confirm an active subscription.

## Roadblocks (append-only; mark resolved, never delete)
<!-- Copy this block for each roadblock. IDs are RB-<initial><nn>, for example RB-E01.
### RB-E01  [BLOCKER | DEGRADED | FYI]  OPEN   Needed by: Sat 6:00 PM
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
| file | product | collection | date | track/frame | GB | checksum | derived outputs |
|---|---|---|---|---|---|---|---|
