# Status: Eduardo        Updated: Sun 1:45 AM CT        Branch: main (status only); no feature PRs of mine open
Plan version read: Sun 12:59 AM, plan v0.5 plus D-19 (T-35 sign convention)

## Now / Next / Done
- G2 (Sun 1:00 AM): not met yet on the live URL. Present: map with radar layers and swipe (#25 merged). Missing: ground-motion layer (#24, draft, waits on my raster, RB-F04), flood-priority map (#20, draft), landmark cards on the map (T-14, T-19), and the layer controls on the page (#30, after #24). Go/no-go call pending, my decision.
- Now:  RB-F04, a valid line-of-sight rate GeoTIFF for Elias (float32, EPSG:32614, zipped), so #24 can run.
- Next: place Diego's `LayerSwitcher` and `Legend` in `app/src/App.tsx` once #30 lands (Diego is sending the placement lines). Answer open questions: Diego (are the two 2026-03-23 pairs masked in T-31; drop 2025-10-30 by date in T-31; "sign INFERRED" text in the PoC is stale after D-19; New Lake Chalco missing from the landmark CSV; `matplotlib` missing from `pipeline/requirements.txt`) and Zainab (is T-16 still hers). Repo public by Sun 9:00 AM (T-54). PR #2 should-fix items only if time allows.
- Reviews: PR #30 (Diego, T-12) reviewed Sun about 1:20 AM, 10 inline comments; Diego fixed items 1 to 4 and nits 8 to 10 at c843581. Items 5 and 6 go in a follow-up. Not re-reviewed yet.
- Done: #25 T-09 map screen merged 12:27 AM; #26 sinking proof of concept merged 12:44 AM; #27 memo sources and T-35 sign check merged 12:58 AM; D-19 recorded 12:55 AM (sign convention, line-of-sight to vertical about 1.27x). Plan v0.5 pushed (D-16 to D-18); T-31 and T-32 via `poc/mexico_city_sinking/` (27 pairs, Nezahualcoyotl 21.9 cm line of sight over 336 days, about 3.2 million people on ground moving >10 cm/yr); rate GeoTIFF and provenance for Elias (PR #26); T-35 sign check (PR #27: positive phase = away from the satellite, high confidence, not from the spec itself; incidence 36.7 to 40.7 degrees); Venezuela work dropped and moved out of the repo; T-02 merged; Azure deploy secret set; plan v0.2 to v0.4.

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

### RB-F03  [DEGRADED]  OPEN   Needed by: Sun 12:45 AM (before landmarks.json gets numbers)
What I was trying to do: hand the line-of-sight numbers to the landmark cards and the sinking layer.
What happened (exact error or evidence): `docs/DATA_CONTRACT.md` says `los_displacement_cm` "Negative means away from the satellite". Our files (`poc/mexico_city_sinking/landmark_series_los_cm.csv`, `displacement_cumulative.npz`, `los_rate_cm_per_year.tif`) are positive = away, and T-35 (`docs/T35_SIGN_CHECK.md`, PR #27) confirms NISAR's native phase is positive = away.
What I already tried: documented the sign in `provenance.json` (PR #26) and in the memo rows (PR #27).
Impact on the plan (task IDs, timeline, tiers): T-19 cards, T-15 chart, T-33 layer, T-34 flood map. A wrong sign shows sinking as uplift.
Options (2 or 3, with cost in hours): (a) change the contract to positive = away, one line by Elias plus a DECISIONS.md entry (0.1 h); (b) keep the contract and multiply by -1 when writing landmarks.json and the layer (0.1 h, easy to forget in one place).
My recommendation: (a). Elias, please confirm; I add the decision line.
Update Sun 1:45 AM: Elias signed off (a) at 12:57 AM and changed `docs/DATA_CONTRACT.md` to positive = away on the PR #24 branch (f1b668d). D-19 records the sign itself. Closes when #24 merges.

### RB-F04  [BLOCKER]  OPEN   Needed by: now (G2 was Sun 1:00 AM)
What I was trying to do: hand Elias the citywide line-of-sight rate raster for the T-33 ground-motion layer.
What happened (exact error or evidence): Elias reports (status, 12:57 AM) that the first `los_rate_cm_per_year.tif` I sent was invalid: uint32 and no CRS. His ingest in #24 is ready and waits on a float32 EPSG:32614 file, zipped. Not re-checked on my side yet.
What I already tried: nothing yet since his report.
Impact on the plan (task IDs, timeline, tiers): T-33 ground-motion layer (Tier 1, G2), T-34 flood map (uses the same rates), Diego's #30 (based on #24).
Options (2 or 3, with cost in hours): (a) re-export the GeoTIFF from `displacement_cumulative.npz` as float32 with the EPSG:32614 grid of the crops, check it with `gdalinfo`, zip and send over LocalSend (0.25 h, needs a Python env with numpy and rasterio); (b) send Elias the npz plus the grid transform and he writes the GeoTIFF (0.25 h of his time).
My recommendation: (a).

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
