# Status: Eduardo        Updated: Sat 6:25 PM CT        Branch: eduardo/map-screen (T-09)
Plan version read: Sat 6:25 PM, plan v0.4

## Now / Next / Done
- Now:  T-09 map screen (built and tested locally; PR after rebasing on main). FYI Elias: repo secret AZURE_STATIC_WEB_APPS_API_TOKEN is set (Sat 5:52 PM) for PR #4. CLOUDFLARE_API_TOKEN is not set.
- Next: follow-up PR for the PR #2 should-fix items (runtime validation, displacement `since`, Node 24 engines, minimatch audit, AI notices); landmark markers on the map for T-14
- Done: T-02 merged (PR #2, with the region-loading race fix and regression tests); Azure deploy secret set; plan v0.3 (D-12) pushed; RB-M01 claims added to the memo; T-02 pushed; plan v0.2 approved and pushed; Phase 0 to 3 planning; catalog check (`pipeline/reports/`); first look at local files (`data/quicklooks/`, `pipeline/quicklook.py`)

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
