<!-- T-19 working notes. Owner: Monica. Structure drafted with AI assistance (Claude Code); card text is Monica's. See docs/AI_USAGE.md. -->

# Landmark card text (T-19)

`mexico_city.json` holds the hand-written card text (docs/DATA_CONTRACT.md, "landmarks.json"). The pipeline copies it into `app/public/data/mexico_city/landmarks.json` and adds the `series` values, so `series` stays `{}` here. Eduardo reviews the science before merge.

Rules for the text:
- `radarShows` is what the data shows, with no interpretation. `weInfer` is a hypothesis, worded as one.
- Every factual claim needs a row in the "Numbers we may quote" table in `docs/DECISION_MEMO.md`. If the row is missing, write `[NEEDS SOURCE ROW: ...]` instead of the claim.
- `sourceIds` must be ids in the manifest `sources` list. Only `nisar-gcov` exists today; ids for the JPL article and the Lake Chalco sources still need to be added.

## Open items before merge

The list may change, depending on Eduardo's answer about matching his ground-motion chart points.

| id | lat, lon | Check |
|---|---|---|
| new_lake_chalco | 19.27, -98.97 | Check against the map and Eduardo's chart points |
| bosque_tlahuac_lake | **missing** (`null`) | Needs coordinates from Monica's notes. The file does not pass the contract until this is filled |
| santa_cecilia_tlahuac | 19.28, -99.00 | Check against the map. **Same point as `tlahuac_ground_motion`**, so the two markers overlap |
| tlahuac_ground_motion | 19.28, -99.00 | Check against the map and Eduardo's chart points; separate it from Santa Cecilia, or merge the two cards |
| nezahualcoyotl | 19.40, -99.02 | Check against the map and Eduardo's chart points. "Fastest" needs T-32 or a source row |
| aicm | 19.44, -99.07 | Check against the map and Eduardo's chart points |
| angel_independencia | 19.43, -99.17 | Check against the map. The "14 steps added" claim already has a JPL row in the memo |
| chalco_2024_flood | 19.26, -98.90 | Check against the map. The AP 2024 numbers need a memo row, after the AP page is confirmed |
