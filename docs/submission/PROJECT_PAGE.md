Draft for Monica to polish. Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md.

# Project page: all 8 form fields

Team **B[U]ILT to Last**, NASA Space Apps 2026 Chicago, challenge **Dancing with the SARs**.

Notes for Monica before pasting:

- `docs/challenge/README.md` lists no character or word limits for these fields. Check the live form for limits when you paste.
- Every number below has a row in `docs/submission/CLAIMS.md`. If you change a number, change it there too, and add nothing that is not in the memo's "Numbers we may quote" table.
- Text marked **[IF SHIPPED]** describes work not confirmed live at the last status update (Sun 6:45 AM): the ground-motion (sinking) layer, layer switcher and legend were being merged to the live site; the 7 landmark points are in `landmarks.json`, but landmark cards on the map are not confirmed; the flood-priority map is **not shipped** (it appears only as "planned next"). Open the live site at G5 (10:30 AM). Keep an [IF SHIPPED] sentence only if the feature is live; otherwise delete it.
- Wording rules: "recognize and measure", never the p-word or the f-word (except "not a forecast"). Every ground-motion number says "line of sight". The data is always PROVISIONAL.

---

## 1. Project Name

`[PROJECT NAME — team agrees (T-17). PLAN.md T-17 notes Monica leans "Project Lago".]`

Tagline: **Mexico City is sinking, and NISAR measured a year of it.**

## 2. High-Level Project Summary

Mexico City is sinking, and NISAR measured a year of it. We built an open-source, interactive web map that helps governments, international organizations and residents recognize and measure a slow hazard that is hard to see from the street. We added up 27 consecutive NISAR radar interferograms (26 spanning 12 days, one 24 days; GUNW, PROVISIONAL data, CRID P05023) from Nov 11, 2025 to Oct 13, 2026. Two sinking bowls appear: one in the north-east (the airport and Nezahualcóyotl) and one in the south-east (Tláhuac and Chalco). At Nezahualcóyotl the ground moved about 21.9 cm away from the satellite along the radar line of sight in that time, about 2 cm per month. About 3.2 million people (WorldPop 2020) live on ground that moves faster than 10 cm per year along the line of sight. The live app lets anyone swipe between NISAR HH and HV radar images from November 2025 and October 2026. [IF SHIPPED: It adds the year of ground motion as a map layer, with a legend in centimeters along the line of sight.] [IF SHIPPED: Landmark cards keep what the radar shows apart from what we infer.]

## 3. Link to Project Demo

[DEMO LINK — Monica adds]

(7-slide deck, public, no login, English. Outline: `docs/submission/DECK_OUTLINE.md`.)

## 4. Link to Final Project

- Live app (Azure): https://yellow-desert-02401091e.4.azurestaticapps.net
- Backup (Cloudflare Pages): https://built-to-last-6or.pages.dev
- Source code (MIT license): https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026

`[Check at G5 in a private window: both URLs open, and the repo is public (T-54).]`

## 5. Detailed Project Description

### The problem

Mexico City is built on an old lakebed, and it is sinking. NASA/JPL reports that in the 1990s and 2000s parts of the metropolitan area were sinking by "around 14 inches (35 centimeters) per year", and that the Angel of Independence has had 14 steps added to its base as the land around it sank. JPL names three causes: groundwater pumping, the weight of urban development, and compaction of the ancient lakebed. Sinking like this is slow and hard to see from the street. To manage it, cities need to recognize where it happens and measure how fast.

### Why NISAR

NISAR is "a joint mission developed by NASA and the Indian Space Research Organisation (ISRO)"; NASA's JPL "provided the satellite's L-band SAR and antenna reflector". A synthetic aperture radar "sends out a pulse of energy" and "records the amount of that energy reflected back after it interacts with Earth", and it can collect data "night or day, regardless of weather conditions". L-band has a wavelength of about 23 cm, and NISAR's L-band radar is "unhindered by clouds or vegetation that impede optical sensors and higher-frequency radars". NISAR passes over the same spot every 12 days. Comparing two passes (an interferogram) shows how far the ground moved toward or away from the satellite.

### What we built

An interactive, open-source web map of the Valley of Mexico, live on Azure:

- **Real NISAR radar images** (GCOV, PROVISIONAL) in HH, in HV, and as an HH/HV color composite, for 11 dates from Nov 11, 2025 to Oct 13, 2026, all from track 19 / frame 11, so the viewing geometry is the same on every date.
- **Swipe compare** between two dates, by mouse, touch or keyboard.
- **A street basemap and a satellite basemap**, with credits on the map.
- [IF SHIPPED: **A provisional-data label** on every radar layer. (The manifest carries "Provisional NISAR data. Interpret with caution." on each layer; check that the legend shows it.)]
- [IF SHIPPED: **A ground-motion layer**: the year total along the radar line of sight, Nov 11, 2025 to Oct 13, 2026, with a legend in centimeters.]
- [IF SHIPPED: **Landmark cards** for seven places (new Lake Chalco, Tláhuac, Nezahualcóyotl, the airport, Centro Histórico, the Angel of Independence and Chalco). Each card keeps "what the radar shows" apart from "what we infer".]
- *Planned next: a flood-priority map that ranks places where line-of-sight sinking and standing water coincide, as a screening aid on PROVISIONAL data, not a forecast.* (Not shipped as of Sun 6:45 AM.)

### How it works

1. **Read only what we need.** NISAR files are large. Our Python pipeline reads just the Mexico City window from the cloud-hosted NISAR files over HTTPS with an Earthdata login (`earthaccess`, `h5py`), so it does not need to download whole granules.
2. **Radar images (GCOV).** The pipeline converts HH and HV to decibels, reprojects them to Web Mercator, and writes small images plus a `manifest.json` that records every granule name. The web app loads only these static files, so it needs no login and no API to run.
3. **A year of ground motion (GUNW).** Our proof of concept (`poc/mexico_city_sinking/`) adds up 27 consecutive interferograms (26 spanning 12 days, one spanning 24 days, Jul 21 to Aug 14, 2026):
   - **One shared zero.** We subtract the median of the same reference area in the western hills (-99.27 to -99.22 E, 19.33 to 19.38 N) from every pair.
   - **No tilt removal on single pairs.** The bowls cover much of the box, so removing a fitted tilt would remove the sinking itself.
   - **Ionosphere correction.** The ionosphere layer is subtracted from each pair.
   - **Unwrapping patches** are re-attached by the whole number of cycles that best matches the neighbouring pairs.
   - **Gap filling.** A pixel missing at most 4 of 27 pairs is filled from its own average rate. 87% of pixels needed no filling, 12% were filled, and 1% (water, steep forest) are dropped.
   - **Adding consecutive pairs cancels most atmospheric noise**, because each date's atmosphere enters once with a plus and once with a minus.
4. **Sign.** Positive means the ground moved away from the satellite, which here means sinking (D-19). We could not get the product specification (JPL D-102272), which is not public. Four independent checks agree: the ISCE3 processor code, ARIA-tools, MintPy, and our own bowls coming out positive.
5. **Hosting.** Azure Static Web Apps serves the app, and managed Azure Functions serve a typed API with the same data for other clients. A backup copy runs on Cloudflare Pages.

### What the data shows

Radar shows, along the line of sight, Nov 11, 2025 to Oct 13, 2026 (PROVISIONAL data, CRID P05023; positive = away from the satellite; place locations approximate):

| Place | Moved away from the satellite, line of sight | Per month, line of sight |
|---|---|---|
| Nezahualcóyotl | about 21.9 cm | about 2.0 cm |
| Tláhuac | about 16.4 cm | about 1.5 cm |
| Airport area (AICM) | about 15.3 cm | about 1.4 cm |
| Centro Histórico | about 9.2 cm | about 0.8 cm |
| Chalco | about 7.6 cm | about 0.7 cm |
| Angel of Independence | about 4.3 cm | about 0.4 cm |
| Iztapalapa | about 3.3 cm | about 0.3 cm |

Across the whole map, along the line of sight:

- 1% of the valid area moves faster than 24 cm per year (99th percentile).
- About 338 km² moves faster than 10 cm per year, and about 105 km² faster than 20 cm per year.
- About 3.2 million people live on the ground that moves faster than 10 cm per year (WorldPop 2020 population counts laid over our rate map).

Two sinking bowls appear. The north-east bowl covers the airport, Nezahualcóyotl and the old Texcoco lakebed. The south-east bowl covers Tláhuac, Chalco and the Xochimilco lakebed. The western hills and the Sierra de Guadalupe barely move.

**Checked against what was published.** JPL's April 2026 NISAR image puts "Benito Juarez International Airport near the center of the mapped deformation field", which matches our north-east bowl. JPL reports preliminary NISAR data (Oct 25, 2025 to Jan 17, 2026) showing parts of the region "subsiding by more than half an inch (more than 2 centimeters) per month". We get about 2.0 cm per month at Nezahualcóyotl over the full year, and about 4 cm per month at the fastest 0.1% of pixels in the first 72 days, both along the line of sight. A Sentinel-1 study (Fernández-Torres et al., 2020) also found that "the highest velocities are located on the eastern sector of the city".

### Physical drivers (what we infer, not what the radar shows)

- JPL names groundwater pumping, the weight of urban development, and compaction of the ancient lakebed as the causes.
- Both bowls sit on old lakebeds (Texcoco in the north-east, Xochimilco and Chalco in the south-east). A 2007 UNAM study of the Chalco plain reports that where the lakebed clay is thickest (300 m), pumping compacts the clay and the ground had sunk by up to about 40 cm per year.
- The IAHS 2020 Sentinel-1 study (Fernández-Torres et al.) reports that "the lower income inhabitants share a proportionally greater economic cost due to land subsidence and associated shallow faulting."

### The lake that came back

Lake Chalco covered its plain "for several thousand years, until the early 20th century, when it was drained" (UNAM 2007; our translation of "por varios miles de años hasta principios del siglo XX, cuando fue drenado"). A system of 14 wells has pumped groundwater from the Chalco plain since 1984, and intensive pumping in the sub-basin started in the early 1960s. As the ground sank, water collected again in the hollow, "como consecuencia del bombeo" (as a consequence of pumping): five pools of up to about 1 ha in 1988, a small lake of about 100 ha by 1991, and a little over 1,000 ha at the time of the study. In 2006 the lake surface sat 12 m below the original ground level. Today new Lake Chalco (Lago de Tláhuac-Xico) is one of our landmarks.

### Why it matters: Chalco, 2024

In September 2024 AP reported from Chalco, "a low-income suburb southeast of Mexico City", where floodwaters stayed in homes "for over a month". "According to Chalco's government, more than 2,000 homes and over 7,000 residents have been affected." Residents blamed "a combination of unchecked growth and failing infrastructure". We give this as context only. We do not link this flood to the lake, to sinking, or to our data, and NISAR data starts in 2025.

[Team member's family connection — only with their consent]

### Which polarizations show the change

- **Ground motion is measured in HH.** The GUNW interferograms over Mexico City are HH only.
- **The radar images use HH and HV.** Over Mexico City NISAR collects HH and HV; there is no VV. Per NASA Earthdata, double-bounce scattering is most sensitive to HH, and volume scattering (for example forest canopy) to cross-polarized HV. The app has a layer for each, plus an HH/HV color composite, so users can compare them.

### Honest limits

- **PROVISIONAL data, CRID P05023.** ASF says PROVISIONAL products are calibrated and validated at a limited set of sites.
- **Line of sight, not vertical.** One track cannot separate up-down from sideways motion. If the motion were purely vertical, vertical sinking would be roughly 1.27 times the line-of-sight number (dividing by cos 38°). Horizontal motion at the edges of the bowls breaks that assumption.
- **About 2 cm uncertainty** on any single number: our control point in the hills drifts by about -2.2 cm over the year.
- **Excluded dates.** We dropped the Oct 30, 2025 acquisition from every layer because of measurement errors we observed ourselves (D-13; it is not on ASF's known-issues list). We also left Dec 5, 2025 and Apr 16, 2026 out of the radar-image frames and water counts (D-17).
- **80 m pixels** are averages; single buildings are not resolved. We quote percentiles, never the maximum, because a few isolated pixels show impossible rates from unwrapping errors.
- **We are not first.** NASA/JPL published NISAR sinking over Mexico City in April 2026. Our contribution is an open, interactive tool, a full year of data, and place-by-place numbers.

### Future applications of NISAR

- **Keep measuring.** NISAR keeps passing every 12 days, so the record grows with each pass and the same pipeline can extend it.
- **Any region.** A new region is one entry in `pipeline/config/regions.json` plus a content file, with no code changes.
- **Help separate vertical from sideways motion** by combining the ascending track we use (19) with the descending track that also covers the city (113).
- **Screening for flood priority** where sinking ground and standing water coincide (planned; see "What we built").

### Benefits and goals

The goal is to help governments, international organizations and residents recognize and measure slow ground sinking with free, open data and an open tool. Anyone can open the map with no login and look at the radar images [IF SHIPPED: and see where the ground moves fastest]. Every number we quote is traced to its source in the repo.

### Tools and languages

- **Languages:** TypeScript, Python.
- **Web app:** React, Vite, MapLibre GL JS, Zustand, Vitest, ESLint.
- **Pipeline:** asf_search, earthaccess, h5py, NumPy, pyproj, Pillow, rasterio, pytest; matplotlib for the proof-of-concept figure.
- **Hosting and tools:** Azure Static Web Apps with managed Azure Functions; Cloudflare Pages (backup); GitHub; VS Code. AI tools are listed in field 6.

### Team

Eduardo Aranda (team lead), Elias Ghanayem, Monica Venancio, Diego [last name], Zainab [last name].

## 6. Use of Super Intelligence (SI)

We used AI coding assistants throughout and logged every use in `docs/AI_USAGE.md` in the repo.

**Tools**

- **Claude Code (Anthropic).** Eduardo: summarizing the 2026 submission and judging guides; drafting the plan, decision memo, data contract and decisions log, including web lookups of NASA, JPL and ASF pages for sourcing; the NISAR catalog search script and region config; a quick-look script for local NISAR files; the app scaffold and the map screen (radar layers, date switching, swipe, basemaps, tests); the year-of-sinking proof of concept (chaining the 27 GUNW pairs, date exclusion, provenance file, GeoTIFF export, figure, landmark CSV); source rows for the memo from reads of each source; the check of the GUNW sign convention and incidence angle. Zainab: the sample dataset, the manifest validator and its tests, the README section text, the sources list and the MIT license text. This project page and the slide outline were also drafted with Claude Code. `[Team: this use is not yet logged in docs/AI_USAGE.md; add a row before submitting so field 6 and the log agree.]`
- **Codex (OpenAI).** Elias: the authenticated NISAR crop fetcher and its tests; the CI and deploy workflow to Azure Static Web Apps and Cloudflare Pages, with post-deploy checks; the GCOV data build and reprojection; the monthly GCOV batch runner, read timeouts and retries; the typed Azure Functions API; landmark sampling and water-month counts; applying the date exclusions; a small radar-themed favicon; audits of the AI usage log.
- **GitHub Copilot** left automated review comments on several pull requests.

**What the team decided, not the AI.** The story ("Mexico City is sinking, and NISAR measured a year of it"), the landmarks, the dates we dropped, and every go/no-go call were the team's decisions. The dates were dropped after Diego's checks of the acquisitions. AI tools were used to check what the data supports, to find and read sources, and to plan and write code.

**Disclosure rules we follow**

- Every file an AI tool wrote or substantially drafted carries a notice in a header comment, or in a `_comment` or `generatedBy` field for JSON.
- Apart from the small favicon drafted by Codex, we generated no images or video with AI. The radar layers, figures and screenshots are renderings of NASA data (with the credited basemaps), not generated imagery. `[Team: decide whether the Codex-drafted favicon needs a visible AI watermark or a note on the page; flagged in CLAIMS.md.]`
- AI-generated content never uses or modifies NASA logos, flags or mission identifiers.

## 7. NASA Data

**NISAR (NASA and ISRO), distributed by the ASF DAAC. All products are PROVISIONAL, CRID P05023.**

| Product | Collection | Used for |
|---|---|---|
| NISAR L2 GUNW (geocoded unwrapped interferograms, HH) | `NISAR_L2_GUNW_PROVISIONAL_V1` (CRID P05023) | The year of ground motion: 27 consecutive pairs (26 of 12 days, one of 24 days) |
| NISAR L2 GCOV (radar backscatter, HH and HV) | `NISAR_L2_GCOV_PROVISIONAL_V1` (CRID P05023) | The radar images on the map: HH, HV and the HH/HV composite, 11 dates |

- **Track 19, frame 11, ascending**, for every layer.
- **Dates:** Nov 11, 2025 to Oct 13, 2026.
- **Excluded:** Oct 30, 2025, from every layer, because of measurement errors we observed ourselves (D-13). Dec 5, 2025 and Apr 16, 2026, from the radar-image frames and water counts (D-17).
- **Reference area** for ground motion: western hills, -99.27 to -99.22 E, 19.33 to 19.38 N.
- **Sign:** positive = away from the satellite (D-19). Line of sight, not vertical.

<details>
<summary>All 27 GUNW granules used for ground motion (from poc/mexico_city_sinking/provenance.json)</summary>

1. NISAR_L2_PR_GUNW_005_019_A_011_006_4000_SH_20251111T120539_20251111T120614_20251123T120540_20251123T120614_P05023_N_F_J_001
2. NISAR_L2_PR_GUNW_006_019_A_011_007_4000_SH_20251123T120540_20251123T120614_20251205T120540_20251205T120615_P05023_N_F_J_001
3. NISAR_L2_PR_GUNW_007_019_A_011_008_4000_SH_20251205T120540_20251205T120615_20251217T120541_20251217T120615_P05023_N_F_J_001
4. NISAR_L2_PR_GUNW_008_019_A_011_009_4000_SH_20251217T120541_20251217T120615_20251229T120541_20251229T120616_P05023_N_F_J_001
5. NISAR_L2_PR_GUNW_009_019_A_011_010_4000_SH_20251229T120541_20251229T120616_20260110T120542_20260110T120616_P05023_N_F_J_001
6. NISAR_L2_PR_GUNW_010_019_A_011_011_4000_SH_20260110T120542_20260110T120616_20260122T120542_20260122T120617_P05023_N_F_J_001
7. NISAR_L2_PR_GUNW_011_019_A_011_012_4000_SH_20260122T120542_20260122T120617_20260203T120543_20260203T120618_P05023_N_F_J_001
8. NISAR_L2_PR_GUNW_012_019_A_011_013_4000_SH_20260203T120543_20260203T120618_20260215T120544_20260215T120618_P05023_N_F_J_001
9. NISAR_L2_PR_GUNW_013_019_A_011_014_4000_SH_20260215T120544_20260215T120618_20260227T120544_20260227T120618_P05023_N_F_J_001
10. NISAR_L2_PR_GUNW_014_019_A_011_015_4000_SH_20260227T120544_20260227T120618_20260311T120544_20260311T120619_P05023_N_F_J_001
11. NISAR_L2_PR_GUNW_015_019_A_011_016_4000_SH_20260311T120544_20260311T120619_20260323T120544_20260323T120619_P05023_N_F_J_001
12. NISAR_L2_PR_GUNW_016_019_A_011_017_4000_SH_20260323T120544_20260323T120619_20260404T120545_20260404T120619_P05023_N_F_J_001
13. NISAR_L2_PR_GUNW_017_019_A_011_018_4000_SH_20260404T120545_20260404T120619_20260416T120544_20260416T120619_P05023_N_F_J_001
14. NISAR_L2_PR_GUNW_018_019_A_011_019_4000_SH_20260416T120544_20260416T120619_20260428T120544_20260428T120619_P05023_N_F_J_001
15. NISAR_L2_PR_GUNW_019_019_A_011_020_4000_SH_20260428T120544_20260428T120619_20260510T120543_20260510T120618_P05023_N_F_J_001
16. NISAR_L2_PR_GUNW_020_019_A_011_021_4000_SH_20260510T120543_20260510T120618_20260522T120543_20260522T120617_P05023_N_F_J_001
17. NISAR_L2_PR_GUNW_021_019_A_011_022_4000_SH_20260522T120543_20260522T120617_20260603T120542_20260603T120617_P05023_N_F_J_001
18. NISAR_L2_PR_GUNW_022_019_A_011_023_4000_SH_20260603T120542_20260603T120617_20260615T120541_20260615T120616_P05023_N_F_J_001
19. NISAR_L2_PR_GUNW_023_019_A_011_024_4000_SH_20260615T120541_20260615T120616_20260627T120541_20260627T120615_P05023_N_F_J_001
20. NISAR_L2_PR_GUNW_024_019_A_011_025_4000_SH_20260627T120541_20260627T120615_20260709T120540_20260709T120615_P05023_N_F_J_001
21. NISAR_L2_PR_GUNW_025_019_A_011_026_4000_SH_20260709T120540_20260709T120615_20260721T120539_20260721T120614_P05023_N_F_J_001
22. NISAR_L2_PR_GUNW_026_019_A_011_028_4000_SH_20260721T120539_20260721T120614_20260814T120538_20260814T120613_P05023_N_F_J_001
23. NISAR_L2_PR_GUNW_028_019_A_011_029_4000_SH_20260814T120538_20260814T120613_20260826T120538_20260826T120612_P05023_N_F_J_001
24. NISAR_L2_PR_GUNW_029_019_A_011_030_4000_SH_20260826T120538_20260826T120612_20260907T120538_20260907T120612_P05023_N_F_J_001
25. NISAR_L2_PR_GUNW_030_019_A_011_031_4000_SH_20260907T120538_20260907T120612_20260919T120538_20260919T120612_P05023_F_F_J_001
26. NISAR_L2_PR_GUNW_031_019_A_011_032_4000_SH_20260919T120538_20260919T120612_20261001T120538_20261001T120612_P05023_N_F_J_001
27. NISAR_L2_PR_GUNW_032_019_A_011_033_4000_SH_20261001T120538_20261001T120612_20261013T120538_20261013T120612_P05023_N_F_J_001

</details>

<details>
<summary>All 11 GCOV granules shown on the map (from app/public/data/mexico_city/manifest.json; the same granules feed HH, HV and the composite)</summary>

1. NISAR_L2_PR_GCOV_005_019_A_011_4005_DHDH_A_20251111T120539_20251111T120614_P05023_N_F_J_001
2. NISAR_L2_PR_GCOV_008_019_A_011_4005_DHDH_A_20251217T120541_20251217T120615_P05023_N_F_J_001
3. NISAR_L2_PR_GCOV_010_019_A_011_4005_DHDH_A_20260110T120542_20260110T120616_P05023_N_F_J_001
4. NISAR_L2_PR_GCOV_013_019_A_011_4005_DHDH_A_20260215T120544_20260215T120618_P05023_N_F_J_001
5. NISAR_L2_PR_GCOV_015_019_A_011_4005_DHDH_A_20260311T120544_20260311T120619_P05023_N_F_J_001
6. NISAR_L2_PR_GCOV_020_019_A_011_4005_DHDH_A_20260510T120543_20260510T120618_P05023_N_F_J_001
7. NISAR_L2_PR_GCOV_023_019_A_011_4005_DHDH_A_20260615T120541_20260615T120616_P05023_N_F_J_001
8. NISAR_L2_PR_GCOV_025_019_A_011_4005_DHDH_A_20260709T120540_20260709T120615_P05023_N_F_J_001
9. NISAR_L2_PR_GCOV_028_019_A_011_4005_DHDH_A_20260814T120538_20260814T120613_P05023_N_F_J_001
10. NISAR_L2_PR_GCOV_031_019_A_011_4005_DHDH_A_20260919T120538_20260919T120612_P05023_F_F_J_001
11. NISAR_L2_PR_GCOV_033_019_A_011_4005_DHDH_A_20261013T120538_20261013T120612_P05023_N_F_J_001

`[If the live manifest changes before submission, re-copy this list from app/public/data/mexico_city/manifest.json.]`

</details>

**NASA resources we used**

- NASA Earthdata, "Synthetic Aperture Radar (SAR)": https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar
- NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026: https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/
- NASA Earthdata Search: https://search.earthdata.nasa.gov/search
- ASF Vertex: https://search.asf.alaska.edu/
- NISAR Data User Guide (ASF): https://nisar-docs.asf.alaska.edu/ (GUNW page: https://nisar-docs.asf.alaska.edu/gunw/; earthaccess page: https://nisar-docs.asf.alaska.edu/earthaccess/)
- ASF, NISAR "PROVISIONAL known issues" (updated Jul 30, 2026): https://nisar-docs.asf.alaska.edu/provisional-known-issues/

## 8. Space Agency Partner Data and Other References

**Space agency partner**

- **ISRO.** NISAR is a joint NASA–ISRO mission; all NISAR data above is joint NASA–ISRO data. We also read ISRO's *NISAR Data Product Format Document* v1.2.1 for the sign check (`docs/T35_SIGN_CHECK.md`).

**Other data**

- WorldPop 2020, Mexico, 1 km, UN-adjusted population counts (`mex_ppp_2020_1km_Aggregated_UNadj.tif`), CC BY 4.0: https://www.worldpop.org/
- Street basemap: OpenFreeMap "positron" style, OpenStreetMap data. Credit: "OpenFreeMap © OpenMapTiles Data from OpenStreetMap". https://tiles.openfreemap.org/styles/positron
- Satellite basemap: EOxCloudless 2024 (Sentinel-2 cloud-free mosaic) by EOX IT Services GmbH, CC BY-NC-SA 4.0: https://cloudless.eox.at

**Text sources**

- NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026: https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/
- NASA Earthdata, "Synthetic Aperture Radar (SAR)": https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar
- Ortiz Zamora, D. C., and Ortega Guerrero, M. A. (2007), "Origen y evolución de un nuevo lago en la planicie de Chalco: implicaciones de peligro por subsidencia e inundación de áreas urbanas en Valle de Chalco (Estado de México) y Tláhuac (Distrito Federal)", *Investigaciones Geográficas* (UNAM) no. 64, pp. 26–42: https://scielo.org.mx/pdf/igeo/n64/n64a3.pdf
- Fernández-Torres, E., Cabral-Cano, E., Solano-Rojas, D., Havazli, E., and Salazar-Tlaczani, L. (2020), "Land Subsidence risk maps and InSAR based angular distortion structural vulnerability assessment: an example in Mexico City", *Proc. IAHS* 382, 583: https://piahs.copernicus.org/articles/382/583/2020/
- AP, "Residents of Mexico City suburb are anxious after living over a month in black sewage water", Sep 13, 2024: https://apnews.com/article/mexico-flooding-chalco-climate-8ecc2eb4d9fabd5219fe6850de5addf6 (AP-credited copy we checked the text against: https://kvia.com/news/2024/09/13/residents-of-mexico-city-suburb-are-anxious-after-living-over-a-month-in-black-sewage-water/)
- Chaussard, E., et al. (2021), "Over a century of sinking in Mexico City", JGR Solid Earth, doi:10.1029/2020JB020648: https://doi.org/10.1029/2020JB020648
- ASF, NISAR "PROVISIONAL known issues": https://nisar-docs.asf.alaska.edu/provisional-known-issues/
- Sign-convention checks (`docs/T35_SIGN_CHECK.md`): ISCE3 (`cxx/isce3/signal/Crossmul.cpp`), ARIA-tools README, MintPy `prep_nisar.py`.

**Learning resources**

- NISAR Data User Guide: https://nisar-docs.asf.alaska.edu/
- Intro to Remote Sensing: https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/remote-sensing
- NASA ARSET trainings: https://appliedsciences.nasa.gov/get-involved/training
- NISAR StoryMaps: https://nisar.jpl.nasa.gov/applications/arcgis-storymaps/
- NISAR Applications White Papers: https://nisar.jpl.nasa.gov/applications/societal-benefit/
- UAVSAR Postcards: https://uavsar.jpl.nasa.gov/education/postcards.html
- CSA SAR Python and QGIS tutorial: https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial

**Code libraries (open source)**

- Web app: MapLibre GL JS, React, Zustand, Vite, Vitest, TypeScript, ESLint.
- Pipeline: asf_search, earthaccess, h5py, NumPy, pyproj, Pillow, rasterio, pytest, matplotlib.

**Tools and services**

- Claude Code (Anthropic) and Codex (OpenAI), AI coding assistants; GitHub Copilot review comments (see field 6 and `docs/AI_USAGE.md`).
- GitHub (code and reviews), Azure Static Web Apps and Azure Functions (hosting and API), Cloudflare Pages (backup hosting), VS Code (editor).

Our own code is MIT-licensed: https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026
