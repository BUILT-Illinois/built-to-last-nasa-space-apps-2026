<!-- T-19 working notes. Owner: Monica. Structure drafted with AI assistance (Claude Code); card text is Monica's. See docs/AI_USAGE.md. -->

# Landmark card text (T-19)

`mexico_city.json` holds the hand-written card text (docs/DATA_CONTRACT.md, "landmarks.json"). The pipeline copies it into `app/public/data/mexico_city/landmarks.json` and adds the `series` values, so `series` stays `{}` here. Eduardo reviews the science before merge.

Rules for the text:
- `radarShows` is what the data shows, with no interpretation. `weInfer` is a hypothesis, worded as one.
- Every factual claim needs a row in the "Numbers we may quote" table in `docs/DECISION_MEMO.md`. If the row is missing, the claim waits here instead of going in the card.
- `sourceIds` must be ids in the manifest `sources` list.

Cards (Sat Nov 14, ~10:45 PM): New Lake Chalco, Tláhuac, Nezahualcóyotl, the airport, Centro Histórico, Ángel de la Independencia, Chalco. The list may still change with Eduardo's answer about matching his ground-motion chart points.

## Before merge

### 1. Numbers (all cards): pending Eduardo's review
Every `radarShows` ends with "pending Eduardo's review". Remove that only after he signs off.

| Card | Line-of-sight movement, Nov 2025–Oct 2026 | Ranking claim in the text |
|---|---|---|
| nezahualcoyotl | about 22 cm | "the most of any place we measured" |
| tlahuac_ground_motion | about 16 cm | "the second-fastest" |
| new_lake_chalco | no cm figure (points to the Tláhuac card); HV +1.2 dB rainy vs dry, city center +0.4 dB | "among the fastest-moving areas we measured" |
| aicm | about 15 cm | |
| centro_historico | about 9 cm | |
| chalco_2024_flood | about 8 cm | |
| angel_independencia | about 4 cm | |

- **D-08:** "relative to a reference area" must name the area once Eduardo confirms it.
- **"Sinking" wording:** the data is movement along the radar's line of sight, not vertical sinking (DATA_CONTRACT rule). Summaries say "moving"; "sinking" appears only in `weInfer`.

### 2. Source ids to add to the memo table and the manifest `sources`
Requested from Eduardo (memo rows) and Elias (manifest `sources`).

| id | Status |
|---|---|
| `nisar-gunw` | Not in the manifest yet; should come with the T-33 ground-motion layer (Elias) |
| `earthdata-sar` | Memo row exists; not in the manifest `sources` |
| `jpl-2026-mexico-city` | Memo rows exist; not in the manifest `sources` |
| `unam-2007-chalco` | **No memo row.** Ortiz Zamora & Ortega Guerrero (2007), UNAM |
| `iahs-2020` | **No memo row** |
| `ap-2024-chalco` | **No memo row.** Confirm the AP numbers on the AP page first |

### 3. Claims that need a source before they are final
- **Lake, `drivers.human`:** "The lake exists because of people." Cites `unam-2007-chalco`, which needs its memo row.
- **Tláhuac, `weInfer`:** "the same process that created the nearby lake". Needs `unam-2007-chalco`.
- **Chalco, `drivers.human`:** "Unchecked urban growth and failing infrastructure." Check that AP 2024 supports this.
- **Ángel, `drivers.natural`:** "Lakebed sediment, thinner here than in the east" was marked "needs a source, or delete". Set to `null` for now; the line is held below.

## Held text (no field in the contract yet)

These go into the cards once the contract gets a `context` field (agree it with Zainab and Elias) and each source has its memo row.

**new_lake_chalco: context** (source `unam-2007-chalco`, no memo row yet)
> This lake didn't exist 40 years ago. Pumping groundwater from wells here, starting in 1984, made the clay underground compress and the land sink. By 1991, water had filled the hollow, forming a new lake about 12 meters below the original ground. A 2007 study warned it could keep growing toward nearby neighborhoods.

**tlahuac_ground_motion: personal** (second sentence: `unam-2007-chalco`, no memo row yet)
> My family is from Santa Cecilia, a neighborhood in central Tláhuac. A 2007 study named nearby San José among the areas at risk of flooding from the growing lake.

**nezahualcoyotl: context** (source `iahs-2020`, no memo row yet)
> A 2020 study found the fastest sinking in the eastern part of the city, and that lower-income residents bear a proportionally greater share of the cost.

**centro_historico: context** (source `jpl-2026-mexico-city`, memo row exists)
> NASA/JPL names groundwater pumping, the weight of development, and compaction of the ancient lakebed as the causes of Mexico City's sinking.

**angel_independencia: context** (source `jpl-2026-mexico-city`, memo row exists)
> According to NASA/JPL, the Ángel has had 14 steps added to its base as the land around it sank.

**angel_independencia: drivers.natural** (needs a source, or delete)
> Lakebed sediment, thinner here than in the east.

**chalco_2024_flood: context** (source `ap-2024-chalco`, no memo row yet; confirm numbers on the AP page)
> In August 2024, sewage-mixed flooding lasted over a month in Chalco. According to Chalco's government, more than 2,000 homes and over 7,000 residents were affected. (Our data starts in 2025 and does not show this flood.)

## Coordinates (lat, lon): all approximate, check against the map and Eduardo's chart points
new_lake_chalco 19.27, -98.97 · tlahuac_ground_motion 19.28, -99.00 · nezahualcoyotl 19.40, -99.02 · aicm 19.44, -99.07 · centro_historico 19.43, -99.13 · angel_independencia 19.43, -99.17 · chalco_2024_flood 19.26, -98.90
