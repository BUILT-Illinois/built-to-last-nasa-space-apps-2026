<!-- T-35, Eduardo. Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md. -->

# T-35: what sign the GUNW unwrapped phase has, and the incidence angle

Checked Sat Nov 14, 11:35 PM CT.

## Answer

**Positive unwrapped phase means the range grew between the two dates.** The ground moved away from the satellite, which for us means sinking. This matches the proof of concept, where the known sinking bowls come out positive.

How sure we are: **high, but not from the specification itself.** We could not get JPL D-102272. The answer rests on three checks below that agree with each other, plus our own data.

The app may say "sinking" in words, with two conditions:
- The number stays "along the radar's line of sight".
- Vertical figures are given only with the conversion stated.

## What was checked

| # | Where | What it says | What it shows |
|---|---|---|---|
| 1 | JPL D-102272, the L2 GUNW product specification | Listed as reference 7 in ISRO's *NISAR Data Product Format Document* v1.2.1, section 2: "L2_GUNW Rev C JPL D-102272 Feburary 7, 2024, Version 1.1.0". | **Not public.** A web search found no copy. ISRO's format document (333 pages, read in full text) describes the layers but never states the phase sign. |
| 2 | Our own GUNW file, product specification version 1.5.0, ISCE3 0.25.16 (`Datasets/NISAR_L2_PR_GUNW_032_113_D_079_..._P05023_N_F_J_001.h5`) | `unwrappedPhase` @description: "Unwrapped interferogram between HH layers", units radians. `identification/referenceZeroDopplerStartTime` is the earlier date (2026-10-08). On track 19, the remote file for Sep 7 to Sep 19, 2026 also has the earlier date as reference. | The file states no sign. It does show **reference = earlier date, secondary = later date**. |
| 3 | ISCE3, the NISAR processor: `cxx/isce3/signal/Crossmul.cpp` (develop branch) | The interferogram is `refSlcUpsampled * std::conj(secSlcUpsampled)`. The flattening term is commented "phase = (4*PI/wavelength)*(rangePixelSpacing)*(rngOffset)". | A range offset where the secondary point is farther away gives **positive** phase. So phase = +4π/λ × (secondary range − reference range). With the earlier date as reference, positive means the range increased, so the ground moved away from the satellite. |
| 4 | ARIA-tools README | "Negative phase differences indicate movement away from the sensor" (ARIA convention). "NISAR GUNW products natively use the opposite date order", and ARIA-tools "automatically flips the dates and mathematical signs for NISAR inputs." | If ARIA has to flip NISAR to reach "negative = away", then NISAR's native phase is positive = away. |
| 5 | MintPy `prep_nisar.py` | Loads the NISAR unwrapped phase unchanged, with no sign flip. MintPy's own convention is displacement = −λ/4π × phase, positive toward the satellite. | MintPy treats positive NISAR phase as range increase. Same answer. |
| 6 | Our data (`poc/mexico_city_sinking/`) | The airport, Nezahualcoyotl and Tlahuac come out positive. The western hills stay near 0. | Sinking where JPL puts it comes out positive. Same answer. |

Also checked, and silent on the sign: the ASF NISAR Data User Guide GUNW page (<https://nisar-docs.asf.alaska.edu/gunw/>).

## Incidence angle, for a rough vertical conversion

Read from the track 19 / frame 11 GUNW metadata cube `science/LSAR/GUNW/metadata/radarGrid/incidenceAngle`. Granule: Sep 7 to Sep 19, 2026, P05023, remote read of about 40 MB. Height layer: 2,000 m.

| Where | Incidence angle |
|---|---|
| Whole Mexico City box (-99.40 to -98.85 E, 19.10 to 19.65 N) | **36.7° to 40.7°**, mean 38.8° |
| Nezahualcoyotl / Tlahuac / Centro Historico | 38.1° / 38.2° / 38.7° |

ISRO's format document gives 42° as the "mid swath incidence angle used for ground range spacing" (section 8, RIFG, p. 135). The full frame on track 113 spans 28° to 52°. Neither is our box. Use the values above.

**Rough conversion:**
- Vertical ≈ line of sight / cos(38°) ≈ **1.27 × line of sight**.
- Example: Nezahualcoyotl 21.9 cm → about 28 cm vertical.
- This assumes the ground moves only straight down. Horizontal motion at the bowl edges breaks that assumption. Say so wherever a vertical number appears.
- Wavelength: 24.2 cm. The track 113 file's `centerFrequency` is 1,239,000,000 Hz, the same mode code (4000) as our track 19 crops.

## Open items for other people

1. **The data contract and the CSV disagree on the sign** (filed as RB-F03 in Eduardo's status file).
   - `docs/DATA_CONTRACT.md` says `los_displacement_cm`: "Negative means away from the satellite."
   - `poc/mexico_city_sinking/landmark_series_los_cm.csv` and `displacement_cumulative.npz` are **positive away**.
   - Whoever writes `landmarks.json` (Elias, T-33) must multiply by −1, or the contract must change (Elias's call, with a line in `DECISIONS.md`).
   - The manifest layer for ground motion must state which convention it uses.
2. **T-35's "done when" asks for a line in `DECISIONS.md`.** This task was told not to edit that file. Eduardo adds it, pointing here.
3. **To close the gap with the specification:** ask on the ASF or NISAR forum, or ask the organizers whether anyone has D-102272.
