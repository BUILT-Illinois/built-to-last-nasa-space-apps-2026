<!-- Paste-ready text for the 8 fields of the Space Apps project form. Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md. Every number traces to docs/submission/CLAIMS.md. Copy the text under each "Field" heading into the matching form field. -->

# Project Lago: paste-ready project page

Paste the text under each heading into the form field of the same name, without the headings themselves.

---

## Field 1. Project Name

Project Lago

---

## Field 2. High-Level Project Summary

Project Lago: see the ground beneath your city move. Mexico City is built on an ancient lakebed, and it is sinking. We added up a year of radar data from the NASA–ISRO NISAR satellite (27 consecutive interferograms, Nov 11, 2025 to Oct 13, 2026; PROVISIONAL data) and built an open-source, interactive web map of the Valley of Mexico. Radar shows two sinking bowls: the north-east (the airport and Nezahualcóyotl) and the south-east (Tláhuac and Chalco). At Nezahualcóyotl the ground moved about 21.9 cm away from the satellite along the radar line of sight in 336 days; at Tláhuac, about 16.4 cm. About 3.2 million people (WorldPop 2020) live in our analysis area on ground moving faster than 10 cm per year along the line of sight. In Tláhuac, where one of us has family, the land sank so far that a new lake formed: water first pooled in 1988, and by 1991 it was a small lake. The live app offers a six-step guided tour, radar images in HH and HV, a year of ground motion and seven landmark cards, so residents, students and decision-makers can recognize and measure a hazard that is hard to see from the street.

---

## Field 3. Link to Project Demo

https://www.canva.com/design/DAHa_1SYPbU/8QPJ37FToTvRL4GDHSWKzA/view

---

## Field 4. Link to Final Project

https://yellow-desert-02401091e.4.azurestaticapps.net

(If the form allows more than one link or a note: backup copy https://built-to-last-6or.pages.dev; source code, MIT license, https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026)

---

## Field 5. Detailed Project Description

**What it does**

Project Lago is an interactive, open-source map of the Valley of Mexico built from NISAR radar data. Visitors can follow a six-step guided tour or explore freely:

- Switch between four layers: radar brightness in HH, in HV, an HH/HV color composite, and a year of ground motion along the radar line of sight.
- Pick any two dates and swipe between them, by mouse, touch or keyboard.
- Choose a street or a satellite basemap and set the radar's opacity.
- Open seven landmark cards (Nezahualcóyotl, the airport, Centro Histórico, the Ángel de la Independencia, Tláhuac, Chalco and the new Lake Chalco). Each card separates what the radar shows from what we infer, names human and natural drivers, and lists its sources.
- Open "How to read this map" for short explainers on HH and HV, on what the radar shows versus what we infer, and on provisional data.

A provisional-data badge is on screen whenever data is shown. The site works on a phone and needs no login.

**The problem**

Mexico City is built on an old lakebed, and it is sinking. NASA/JPL reports that in the 1990s and 2000s parts of the metropolitan area sank by "around 14 inches (35 centimeters) per year", and that the Angel of Independence has had 14 steps added to its base as the land around it sank. JPL names three causes: groundwater pumping, the weight of urban development, and compaction of the ancient lakebed. Sinking like this is slow and hard to see from the street. To manage it, cities first need to recognize where it happens and measure how fast.

**Why NISAR**

NISAR is a joint mission of NASA and the Indian Space Research Organisation (ISRO). Its L-band synthetic aperture radar sends out pulses and records the energy reflected back, night or day, regardless of weather, and the long L-band wavelength (about 24 cm) is unhindered by clouds. Comparing two passes over the same place (an interferogram) shows how far the ground moved toward or away from the satellite. Our pairs are 12 days apart.

**How it works**

1. **Read only what we need.** Our Python pipeline reads just the Mexico City window from the cloud-hosted NISAR files over HTTPS with an Earthdata login (`earthaccess`, `h5py`), so it does not need to download whole granules.
2. **Radar images (GCOV).** The pipeline converts HH and HV to decibels, reprojects them to Web Mercator and writes small images plus a `manifest.json` that records every granule name. The web app loads only these static files.
3. **A year of ground motion (GUNW).** We add up 27 consecutive interferograms (26 spanning 12 days, one spanning 24 days), from Nov 11, 2025 to Oct 13, 2026:
   - every pair is set to zero over the same reference area in the western hills (-99.27 to -99.22 E, 19.33 to 19.38 N), which we assume is stable;
   - the ionosphere layer provided with each pair is subtracted;
   - patches that the unwrapping split off are re-attached by the whole number of cycles that best matches the neighbouring pairs;
   - a pixel missing at most 4 of the 27 pairs is filled from its own average rate (87% of pixels needed no filling, 12% were filled, 1% are dropped);
   - adding consecutive pairs cancels the atmosphere of every date in between; the first and last dates' atmosphere remains, which is one reason for our uncertainty of about 2 cm.
4. **Sign.** Positive means the ground moved away from the satellite, which here means sinking. The product specification is not public, so we checked the NISAR processing software (ISCE3), ARIA-tools and MintPy, and the known sinking zones come out positive in our data.
5. **Hosting.** Azure Static Web Apps serves the app, and managed Azure Functions serve a typed API with the same data. A backup copy runs on Cloudflare Pages. GitHub Actions tests every change and deploys it.

**What the data shows**

Radar shows, along the line of sight, Nov 11, 2025 to Oct 13, 2026 (PROVISIONAL data, CRID P05023; positive = away from the satellite; place locations approximate):

| Place | Moved away from the satellite in 336 days | Per month |
|---|---|---|
| Nezahualcóyotl | about 21.9 cm | about 2.0 cm |
| Tláhuac | about 16.4 cm | about 1.5 cm |
| Airport area (AICM) | about 15.3 cm | about 1.4 cm |
| Centro Histórico | about 9.2 cm | about 0.8 cm |
| Chalco | about 7.6 cm | about 0.7 cm |
| Ángel de la Independencia | about 4.3 cm | about 0.4 cm |
| Iztapalapa | about 3.3 cm | about 0.3 cm |

Inside our Mexico City analysis box (-99.40 to -98.85 E, 19.10 to 19.65 N), along the line of sight:

- 1% of the area moves faster than 24 cm per year (99th percentile).
- About 338 km² moves faster than 10 cm per year, and about 105 km² faster than 20 cm per year.
- About 3.2 million people live on ground moving faster than 10 cm per year. This is a preliminary exposure estimate: WorldPop 2020 population counts (1 km cells) laid over our rate map.

Two sinking bowls appear. The north-east bowl covers the airport, Nezahualcóyotl and the old Texcoco lakebed; the south-east bowl covers Tláhuac, Chalco and the Xochimilco lakebed. The western hills and the Sierra de Guadalupe barely move.

**Checked against what was published.** JPL's April 2026 NISAR image of Mexico City shows the deformation centered near Benito Juárez International Airport ("The structure near the center of the image is Benito Juarez International Airport"), which matches our north-east bowl. JPL reports preliminary NISAR data (Oct 25, 2025 to Jan 17, 2026) showing parts of the region "subsiding by more than half an inch (more than 2 centimeters) per month". We get about 2.0 cm per month at Nezahualcóyotl along the line of sight over the full year. The time windows differ, and we do not know which track JPL used.

**The lake that came back**

Lake Chalco covered its plain "for several thousand years, until the early 20th century, when it was drained" (UNAM 2007, our translation). As groundwater pumping made the ground sink, water collected again in the hollow, "como consecuencia del bombeo" (as a consequence of pumping): five small pools in 1988, a lake of about 100 ha by 1991. In 2006 the lake surface sat 12 m below the original ground level. Today new Lake Chalco (Lago de Tláhuac-Xico) is one of our landmarks. Our teammate Monica's family is from Santa Cecilia, in Tláhuac, where radar shows the ground moved about 16.4 cm along the line of sight in 336 days.

**Why it matters: Chalco, 2024**

In September 2024 AP reported from Chalco, "a low-income suburb southeast of Mexico City", where floodwaters stayed in homes "for over a month". We give this as context only: we do not link this flood to sinking or to our data, and NISAR data starts in 2025.

**Honest limits**

- PROVISIONAL data (CRID P05023): ASF says these products are calibrated and validated at a limited set of sites.
- Line of sight, not vertical. One track cannot separate up-down from sideways motion. If the motion were purely vertical, it would be roughly 1.27 times the line-of-sight number.
- About 2 cm uncertainty on any single number: a control point in the hills, which should not move, ended the year at -2.2 cm.
- Dates left out: Oct 30, 2025 from every layer (measurement errors we found ourselves); Dec 5, 2025 and Apr 16, 2026 from the radar-image frames (scene-wide artifacts). The two later dates stay in the interferogram chain.
- Pixels are 80 m averages, so single buildings are not resolved; we quote percentiles, never the maximum. Rates beyond ±50 cm per year and a 6 km band at the swath edge are masked as artifacts.
- We are not first: NASA/JPL published NISAR sinking over Mexico City in April 2026. Our contribution is an open, interactive tool, a full year of data and place-by-place numbers.

**What we hope to achieve, and what comes next**

The goal is to help residents, students, decision-makers and international organizations recognize and measure slow ground sinking with free, open data and an open tool. Every number we quote is traced to its source in the repo (`docs/submission/CLAIMS.md`). Next: each new NISAR pass extends the record with the same pipeline; new regions mostly by configuration; combining the ascending track we use (19) with the descending track over the city (113) to help separate vertical from sideways motion; a Spanish version for residents; and a flood-priority screening map where sinking ground and standing water coincide (planned, not a forecast).

**Tools and languages**

- Languages: TypeScript, Python.
- Web app: React, Vite, MapLibre GL JS, Zustand, Vitest, ESLint.
- Pipeline: asf_search, earthaccess, h5py, NumPy, pyproj, Pillow, rasterio, matplotlib, pytest.
- Hosting and tools: Azure Static Web Apps and Azure Functions, Cloudflare Pages, GitHub and GitHub Actions, VS Code, Canva (slides).

**Team B[U]ILT to Last:** Eduardo Aranda (team lead), Elias Ghanayem, Monica Venancio, Diego Arias, Zainab Salau.

---

## Field 6. Use of Super Intelligence (SI)

Yes. We used AI coding assistants throughout and logged each use in `docs/AI_USAGE.md` in the repo.

- **Claude Code (Anthropic):** planning and the decision log; reading and summarizing the challenge guides and sources; the NISAR catalog search and quick-look scripts; the web app scaffold, map screen, layer controls, legend, landmark panel, guided tour and tests; the year-of-ground-motion proof of concept (chaining the 27 interferograms) and its checks; the sample dataset and manifest validator; README, sources list and drafts of this page and the slide outline.
- **Codex (OpenAI):** the authenticated NISAR crop fetcher, the CI and deploy workflow, the radar-image data build and reprojection, the ground-motion ingest, the typed Azure Functions API, landmark sampling, and the site's favicon.
- **GitHub Copilot:** automated review comments on some pull requests.

The idea, the story, the landmarks, the dates we dropped and every go/no-go decision were the team's. AI tools were used to check what the data supports, to find and read sources, and to plan and write code; the team reviewed what shipped.

How we mark AI use: every file an AI tool wrote or substantially drafted carries a notice in a header comment or a `_comment` field. The only AI-drafted image is the site's small favicon, disclosed here. The radar layers, figures and screenshots are renderings of NASA data, not generated imagery. No AI-generated content uses or modifies NASA logos, flags or mission identifiers.

---

## Field 7. NASA Data

**NISAR (NASA and ISRO), distributed by the Alaska Satellite Facility DAAC. All products PROVISIONAL, CRID P05023; track 19, frame 11, ascending.**

- **NISAR L2 GUNW** (geocoded unwrapped interferograms, HH), collection `NISAR_L2_GUNW_PROVISIONAL_V1`: the year of ground motion, from 27 consecutive pairs (26 of 12 days, one of 24 days), Nov 11, 2025 to Oct 13, 2026.
- **NISAR L2 GCOV** (radar backscatter, HH and HV), collection `NISAR_L2_GCOV_PROVISIONAL_V1`: the radar images on the map, 11 dates from Nov 11, 2025 to Oct 13, 2026.
- Reference area for ground motion: western hills, -99.27 to -99.22 E, 19.33 to 19.38 N. Sign: positive = away from the satellite. Line of sight, not vertical.
- Every granule name is recorded in the app's `manifest.json` and in `poc/mexico_city_sinking/provenance.json` in the repo.

GUNW granules (27):
NISAR_L2_PR_GUNW_005_019_A_011_006_4000_SH_20251111T120539_20251111T120614_20251123T120540_20251123T120614_P05023_N_F_J_001
NISAR_L2_PR_GUNW_006_019_A_011_007_4000_SH_20251123T120540_20251123T120614_20251205T120540_20251205T120615_P05023_N_F_J_001
NISAR_L2_PR_GUNW_007_019_A_011_008_4000_SH_20251205T120540_20251205T120615_20251217T120541_20251217T120615_P05023_N_F_J_001
NISAR_L2_PR_GUNW_008_019_A_011_009_4000_SH_20251217T120541_20251217T120615_20251229T120541_20251229T120616_P05023_N_F_J_001
NISAR_L2_PR_GUNW_009_019_A_011_010_4000_SH_20251229T120541_20251229T120616_20260110T120542_20260110T120616_P05023_N_F_J_001
NISAR_L2_PR_GUNW_010_019_A_011_011_4000_SH_20260110T120542_20260110T120616_20260122T120542_20260122T120617_P05023_N_F_J_001
NISAR_L2_PR_GUNW_011_019_A_011_012_4000_SH_20260122T120542_20260122T120617_20260203T120543_20260203T120618_P05023_N_F_J_001
NISAR_L2_PR_GUNW_012_019_A_011_013_4000_SH_20260203T120543_20260203T120618_20260215T120544_20260215T120618_P05023_N_F_J_001
NISAR_L2_PR_GUNW_013_019_A_011_014_4000_SH_20260215T120544_20260215T120618_20260227T120544_20260227T120618_P05023_N_F_J_001
NISAR_L2_PR_GUNW_014_019_A_011_015_4000_SH_20260227T120544_20260227T120618_20260311T120544_20260311T120619_P05023_N_F_J_001
NISAR_L2_PR_GUNW_015_019_A_011_016_4000_SH_20260311T120544_20260311T120619_20260323T120544_20260323T120619_P05023_N_F_J_001
NISAR_L2_PR_GUNW_016_019_A_011_017_4000_SH_20260323T120544_20260323T120619_20260404T120545_20260404T120619_P05023_N_F_J_001
NISAR_L2_PR_GUNW_017_019_A_011_018_4000_SH_20260404T120545_20260404T120619_20260416T120544_20260416T120619_P05023_N_F_J_001
NISAR_L2_PR_GUNW_018_019_A_011_019_4000_SH_20260416T120544_20260416T120619_20260428T120544_20260428T120619_P05023_N_F_J_001
NISAR_L2_PR_GUNW_019_019_A_011_020_4000_SH_20260428T120544_20260428T120619_20260510T120543_20260510T120618_P05023_N_F_J_001
NISAR_L2_PR_GUNW_020_019_A_011_021_4000_SH_20260510T120543_20260510T120618_20260522T120543_20260522T120617_P05023_N_F_J_001
NISAR_L2_PR_GUNW_021_019_A_011_022_4000_SH_20260522T120543_20260522T120617_20260603T120542_20260603T120617_P05023_N_F_J_001
NISAR_L2_PR_GUNW_022_019_A_011_023_4000_SH_20260603T120542_20260603T120617_20260615T120541_20260615T120616_P05023_N_F_J_001
NISAR_L2_PR_GUNW_023_019_A_011_024_4000_SH_20260615T120541_20260615T120616_20260627T120541_20260627T120615_P05023_N_F_J_001
NISAR_L2_PR_GUNW_024_019_A_011_025_4000_SH_20260627T120541_20260627T120615_20260709T120540_20260709T120615_P05023_N_F_J_001
NISAR_L2_PR_GUNW_025_019_A_011_026_4000_SH_20260709T120540_20260709T120615_20260721T120539_20260721T120614_P05023_N_F_J_001
NISAR_L2_PR_GUNW_026_019_A_011_028_4000_SH_20260721T120539_20260721T120614_20260814T120538_20260814T120613_P05023_N_F_J_001
NISAR_L2_PR_GUNW_028_019_A_011_029_4000_SH_20260814T120538_20260814T120613_20260826T120538_20260826T120612_P05023_N_F_J_001
NISAR_L2_PR_GUNW_029_019_A_011_030_4000_SH_20260826T120538_20260826T120612_20260907T120538_20260907T120612_P05023_N_F_J_001
NISAR_L2_PR_GUNW_030_019_A_011_031_4000_SH_20260907T120538_20260907T120612_20260919T120538_20260919T120612_P05023_F_F_J_001
NISAR_L2_PR_GUNW_031_019_A_011_032_4000_SH_20260919T120538_20260919T120612_20261001T120538_20261001T120612_P05023_N_F_J_001
NISAR_L2_PR_GUNW_032_019_A_011_033_4000_SH_20261001T120538_20261001T120612_20261013T120538_20261013T120612_P05023_N_F_J_001

GCOV granules (11):
NISAR_L2_PR_GCOV_005_019_A_011_4005_DHDH_A_20251111T120539_20251111T120614_P05023_N_F_J_001
NISAR_L2_PR_GCOV_008_019_A_011_4005_DHDH_A_20251217T120541_20251217T120615_P05023_N_F_J_001
NISAR_L2_PR_GCOV_010_019_A_011_4005_DHDH_A_20260110T120542_20260110T120616_P05023_N_F_J_001
NISAR_L2_PR_GCOV_013_019_A_011_4005_DHDH_A_20260215T120544_20260215T120618_P05023_N_F_J_001
NISAR_L2_PR_GCOV_015_019_A_011_4005_DHDH_A_20260311T120544_20260311T120619_P05023_N_F_J_001
NISAR_L2_PR_GCOV_020_019_A_011_4005_DHDH_A_20260510T120543_20260510T120618_P05023_N_F_J_001
NISAR_L2_PR_GCOV_023_019_A_011_4005_DHDH_A_20260615T120541_20260615T120616_P05023_N_F_J_001
NISAR_L2_PR_GCOV_025_019_A_011_4005_DHDH_A_20260709T120540_20260709T120615_P05023_N_F_J_001
NISAR_L2_PR_GCOV_028_019_A_011_4005_DHDH_A_20260814T120538_20260814T120613_P05023_N_F_J_001
NISAR_L2_PR_GCOV_031_019_A_011_4005_DHDH_A_20260919T120538_20260919T120612_P05023_F_F_J_001
NISAR_L2_PR_GCOV_033_019_A_011_4005_DHDH_A_20261013T120538_20261013T120612_P05023_N_F_J_001

NASA resources we used:
- NASA Earthdata, "Synthetic Aperture Radar (SAR)": https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar
- NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026: https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/
- NASA Earthdata Search: https://search.earthdata.nasa.gov/search
- ASF Vertex: https://search.asf.alaska.edu/
- NISAR Data User Guide (ASF): https://nisar-docs.asf.alaska.edu/
- ASF, NISAR PROVISIONAL known issues: https://nisar-docs.asf.alaska.edu/provisional-known-issues/

---

## Field 8. Space Agency Partner Data and Other References

**Space agency partner: ISRO.** NISAR is a joint NASA–ISRO mission; all NISAR data above is joint NASA–ISRO data. We also read ISRO's NISAR Data Product Format Document (v1.2.1) for the sign check.

**Other data**
- WorldPop 2020, Mexico, 1 km, UN-adjusted population counts, CC BY 4.0: https://www.worldpop.org/
- Street basemap: OpenFreeMap "positron" style with OpenMapTiles and OpenStreetMap data (© OpenStreetMap contributors, ODbL): https://openfreemap.org/
- Satellite basemap: EOxCloudless 2024 by EOX IT Services GmbH (contains modified Copernicus Sentinel data 2024), CC BY-NC-SA 4.0: https://cloudless.eox.at

**Text sources**
- NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026: https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/
- NASA Earthdata, "Synthetic Aperture Radar (SAR)": https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar
- Ortiz Zamora, D. C., and Ortega Guerrero, M. A. (2007), "Origen y evolución de un nuevo lago en la planicie de Chalco...", Investigaciones Geográficas (UNAM) no. 64, pp. 26–42: https://scielo.org.mx/pdf/igeo/n64/n64a3.pdf
- Fernández-Torres, E., et al. (2020), "Land Subsidence risk maps and InSAR based angular distortion structural vulnerability assessment: an example in Mexico City", Proc. IAHS 382, 583–587: https://piahs.copernicus.org/articles/382/583/2020/
- AP, "Residents of Mexico City suburb are anxious after living over a month in black sewage water", Sep 13, 2024: https://apnews.com/article/mexico-flooding-chalco-climate-8ecc2eb4d9fabd5219fe6850de5addf6
- Chaussard, E., et al. (2021), "Over a Century of Sinking in Mexico City: No Hope for Significant Elevation and Storage Capacity Recovery", JGR Solid Earth, doi:10.1029/2020JB020648 (background reading; no number quoted)
- Sign-convention checks: ISCE3 (Crossmul), ARIA-tools README, MintPy prep_nisar.py.

**Images**
- Slide 2: NASA/JPL-Caltech / David Bekaert, NISAR subsidence image of Mexico City (from the JPL article above).
- Slide 3: scattering diagram from NASA Earthdata, "Synthetic Aperture Radar (SAR)".
- Slide decorations: Canva template and Canva library graphics.

**Code libraries (open source):** MapLibre GL JS, React, Zustand, Vite, Vitest, TypeScript, ESLint; asf_search, earthaccess, h5py, NumPy, pyproj, Pillow, rasterio, matplotlib, pytest.

**Tools and services:** Claude Code (Anthropic), Codex (OpenAI), GitHub Copilot; GitHub and GitHub Actions; Azure Static Web Apps and Azure Functions; Cloudflare Pages; VS Code; Canva.

Our own code is MIT-licensed: https://github.com/BUILT-Illinois/built-to-last-nasa-space-apps-2026. NASA/ISRO data, basemaps and quoted text remain under their own terms.
