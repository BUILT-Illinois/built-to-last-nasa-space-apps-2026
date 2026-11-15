<!-- T-19 working notes. Owner: Monica. Structure drafted with AI assistance (Claude Code); card text is Monica's. See docs/AI_USAGE.md. -->

# Landmark card text (T-19)

`mexico_city.json` holds the hand-written card text (docs/DATA_CONTRACT.md, "landmarks.json"). The pipeline copies it into `app/public/data/mexico_city/landmarks.json` and adds the `series` values, so `series` stays `{}` here. Eduardo reviews the science before merge.

Rules for the text:
- `radarShows` is what the data shows, with no interpretation. `weInfer` is a hypothesis, worded as one.
- Every factual claim needs a row in the "Numbers we may quote" table in `docs/DECISION_MEMO.md`. If the row is missing, or the memo lists the claim under "keep them out of visible text", the claim waits here instead of going in the card.
- `sourceIds` must be ids in the manifest `sources` list.
- D-19: "sinking" is fine in words as long as every number stays labeled "line of sight".

Cards (Sun Nov 15): New Lake Chalco, Tláhuac, Nezahualcóyotl, the airport, Centro Histórico, Ángel de la Independencia, Chalco.

## Valley ground-motion rates

Annualized line-of-sight rates from 336 days of provisional GUNW observations (Nov 11, 2025 to Oct 13, 2026), relative to the western hills. Positive means away from the satellite.

| Card | Rate (cm/yr) |
|---|---:|
| Nezahualcóyotl | +24.2 |
| Tláhuac | +17.9 |
| Benito Juárez International Airport | +16.5 |
| Centro Histórico | +9.0 |
| Chalco | +8.4 |
| Ángel de la Independencia | +5.1 |
| New Lake Chalco | No reported rate |

## Still open

### Source ids not yet in the manifest `sources`
All seven ids now have memo rows. Elias adds them to the manifest: `nisar-gunw` (with the T-33 ground-motion layer), `earthdata-sar`, `jpl-2026-mexico-city`, `unam-2007-chalco`, `iahs-2020`, `ap-2024-chalco`.

### Held from the lake card (memo: "keep them out of visible text")
- "The ground around this lake is among the fastest-moving areas we measured." Waiting on the lake point being sampled.
- "The lake surface itself changes with the seasons far more than the city: in the rainy season (Jul–Oct 2026) its HV signal is about 1.2 dB higher than in the dry season (Jan–Apr), vs. about 0.4 dB for the city center." Waiting on review of Diego's lake check.
- weInfer: "The rainy-season change is consistent with more water and plant growth on and around the lake." Goes back with the HV sentence.
- drivers.natural "The rains are natural." stays on the card, but only makes sense with the HV sentence.

### Held from the Ángel card
- drivers.natural: "Lakebed sediment, thinner here than in the east." Needs a source, or delete.

## Held text (no field in the contract yet)

These go into the cards once the contract gets a `context` field (agree it with Zainab and Elias). Corrected against the memo rows on Sun Nov 15.

**new_lake_chalco: context** (`unam-2007-chalco`)
> Lake Chalco covered this plain for thousands of years, until it was drained in the early 20th century. Groundwater pumping, intensive since the early 1960s and from a system of 14 wells since 1984, compacted the clay and the ground sank, by up to 40 cm a year at the center of the plain. Water began to pool in the hollow in 1988, and by 1991 the pools had joined into a small lake. By 2006 its surface was 12 meters below the original ground. A 2007 study projected it would keep growing, increasing the flood risk to Tláhuac and Valle de Chalco.

What changed from the first draft: pumping did not "begin" in 1984 (memo); the 12 m is a 2006 figure, not 1991; "warned" is now "projected", because it is a 2007 projection we have not checked.

**tlahuac_ground_motion: personal** (`unam-2007-chalco`)
> My family is from Santa Cecilia, a neighborhood in central Tláhuac. A 2007 study projected that the growing lake could reach San José, a Tláhuac neighborhood next to the lake.

What changed: "nearby San José" is removed. The memo says the source for Santa Cecilia being next to San José has not been read.

**nezahualcoyotl: context** (`iahs-2020`)
> A 2020 study found the fastest sinking in the eastern part of the city, and that lower-income residents bear a proportionally greater share of the cost.

**centro_historico: context** (`jpl-2026-mexico-city`)
> NASA/JPL names groundwater pumping, the weight of development, and compaction of the ancient lakebed as the causes of Mexico City's sinking.

**angel_independencia: context** (`jpl-2026-mexico-city`)
> According to NASA/JPL, the Ángel has had 14 steps added to its base as the land around it sank.

**chalco_2024_flood: context** (`ap-2024-chalco`, context only: do not tie it to the lake, sinking or our data)
> In 2024, floodwater mixed with sewage stayed in homes in Chalco for over a month. According to Chalco's government, more than 2,000 homes and over 7,000 residents were affected. (Our data starts in 2025 and does not show this flood.)

What changed: "August" is removed. The AP row does not give the month the flood started.

## Coordinates (lat, lon): approximate, sent to Elias (all inside the frame)
new_lake_chalco 19.27, -98.97 · tlahuac_ground_motion 19.28, -99.00 · nezahualcoyotl 19.40, -99.02 · aicm 19.44, -99.07 · centro_historico 19.43, -99.13 · angel_independencia 19.43, -99.17 · chalco_2024_flood 19.26, -98.90
