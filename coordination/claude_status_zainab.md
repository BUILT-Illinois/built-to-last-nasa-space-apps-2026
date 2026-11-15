# Status: Zainab        Updated: Sat 10:48 PM CT        Branch: zainab-sample-data (PR #6), then zainab-docs (PR #11)
Plan version read: Sat 6:25 PM | Plan v0.4. G1 passed, GS default story (surface change in GCOV), Oct 30, 2025 dropped (D-13)

## Now / Next / Done
- Now:  Second-round review fixes on PR #6 and PR #11.
  - PR #6: sample is labelled synthetic (`dataMaturity: "SYNTHETIC"`, `"synthetic": true`, empty `granules`, "generated test pattern" descriptions). Validator allows empty granules only when `synthetic` is true. 57 tests pass.
  - PR #11: README says Node 24, separates the local test sample from the live dataset, explains static site vs. Azure API, updates the Earthdata link.
- Next: T-14 landmark panel in `app/src/components/landmarks/`. Builds on `app/src/lib/data.ts`, loads the live region's `landmarks.json` (not only the sample), and shows a clean empty state until Monica's landmarks land. Then T-24 sources page (live by Sun 1:00 AM).
- Done:
  - T-08: sample data + validator (PR #6), first review round addressed (no crashes on bad input, matches `manifest.ts`, `"vectors": []`).
  - T-07: README, MIT LICENSE, `docs/SOURCES.md` (PR #11), live URLs added, no region names.
- Open question for Eduardo: is T-16 (`sample_at_points()`) still mine?

## Roadblocks (append-only; mark resolved, never delete)
<!-- Copy this block for each roadblock. IDs are RB-<initial><nn>, for example RB-Z01.
### RB-Z01  [BLOCKER | DEGRADED | FYI]  OPEN   Needed by: Sat 6:00 PM
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
| (none, no NISAR files on this laptop) | | | | | | | |
