# Status: Elias        Updated: Sat 3:48 PM CT        Branch: elias/backend
Plan version read: Sat 3:10 PM CT, plan v0.2 approved and in force

## Now / Next / Done
- Now: [PR #1](https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026/pull/1) is open to `main` for Zainab's T-08 fixture handoff. `git check-ignore` confirmed that public manifests, landmark data, WebP, and GeoJSON are stageable and that raw files, interim crops, and the local identity file are ignored.
- Next: T-01 for G1 at Sat 4:30 PM CT (5:00 PM if the probe is unfinished). Catalog inputs selected for both products on track 19 / frame 11, PROVISIONAL P05023. Run an Earthdata login check when Elias confirms `_netrc` is ready, then run the probe reads.
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
