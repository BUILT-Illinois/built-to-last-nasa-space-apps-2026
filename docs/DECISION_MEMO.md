# Decision memo: what we build over Mexico City

Status: **the story is open. The team analyses the data and decides by Sat Nov 14, 5:30 PM CT (gate GS).** Updated 2:45 PM with a first look at the files in `Datasets/`. Updated 3:55 PM: gates G2 and G3 merged into one go/no-go at Sun 1:00 AM (plan v0.3). **Updated 6:25 PM (plan v0.4): GS passed with no decision recorded, so the default (option A, surface change in GCOV) applies until the team records one. The Oct 30, 2025 acquisition is excluded (D-13); the correction is marked below.**

The Submission Guide says AI should not be used to come up with the idea of how to solve the challenge. This memo therefore only reports what the data can and cannot support. The choice is the team's.

## Where to find the information

| What | Where | Needs |
|---|---|---|
| Every NISAR file over Mexico City: dates, tracks, polarizations, sizes | [pipeline/reports/summary_mexico_city.md](../pipeline/reports/summary_mexico_city.md) and [granules_mexico_city.csv](../pipeline/reports/granules_mexico_city.csv) (open the CSV in Excel). Re-run with `python pipeline/search_granules.py`. | Nothing |
| Pictures of our own downloaded files, cropped to the city | `data/quicklooks/` on Eduardo's laptop (git-ignored). Made by `pipeline/quicklook.py`. | The files in `Datasets/` |
| A browse picture of any granule, no login | ASF Vertex, <https://search.asf.alaska.edu/>: dataset NISAR, draw a box on Mexico City, filter path 19 and frame 11, click a result. The `url` column of the CSV has each file's address; the browse PNG sits next to it. | Nothing |
| What the products are and their known problems | NISAR Data User Guide, <https://nisar-docs.asf.alaska.edu/>, especially the GCOV and GUNW pages and "PROVISIONAL known issues" | Nothing |
| What NASA already published about this city | The JPL article in the table at the bottom | Nothing |
| The rules and judging criteria | [challenge/README.md](challenge/README.md) | Nothing |

To make your own pictures (the virtual environment `.venv` is already set up on Eduardo's laptop):

```text
.venv\Scripts\activate
python pipeline/quicklook.py gcov   "Datasets\<gcov file>.h5"
python pipeline/quicklook.py gcov   "Datasets\<gcov file>.h5" --frequency A --bbox -99.12 19.38 -98.95 19.52 --suffix _airport
python pipeline/quicklook.py change "Datasets\<earlier gcov>.h5" "Datasets\<later gcov>.h5"
python pipeline/quicklook.py gunw   "Datasets\<gunw file>.h5"
```

`--frequency A` gives 10 m pixels and should be used with a small `--bbox` (west south east north). In the color composite, red is HH, green is HV, blue is HH minus HV. In the change pictures, red means brighter on the later date and blue means darker.

Questions worth answering during the analysis (T-25): Which places change the most between the two GCOV dates, and is the change in HH, HV, or both? What is at those places on a normal map? Does the change survive when both files are from the same release? Which of these would a non-expert care about?

## What the first look at our own files shows

Three complete files (16 GB) and one broken one that has since been deleted.

| File | What it is | Note |
|---|---|---|
| GCOV, track 19 / frame 11, Oct 30, 2025, release X05009 | BETA (pre-calibration) | A PROVISIONAL version of the same scene exists in the catalog |
| GCOV, track 19 / frame 11, Nov 6, 2026, release P05036, file name ends in "(2)" | From the `NISAR_L2_GCOV_V1` collection, newer than PROVISIONAL | Check how ASF labels this collection before describing it |
| Same name without "(2)", 105 MB | Truncated download, would not open | Deleted Nov 14, 3:09 PM |
| GUNW, track 113 / frame 79 (descending), Oct 8 to Oct 20, 2026, release P05023 | PROVISIONAL | A different track from the two GCOV files |

- **Corrected at 6:25 PM. The first reading of surface change was wrong for one place and unconfirmed for the other.** We first read the two local files (Oct 30, 2025 and Nov 6, 2026) as showing the flat zone north-east of the airport darker in HV and the southern wetland brighter. Diego's check of all 29 browse dates (his RB-D01) shows the Oct 30, 2025 acquisition has measurement errors: on that date only, every dark area in the valley is lifted, most in HV, and track 113 shows no such drop over the same weeks. ASF's known-issues page does not list this, so we describe it as our own observation. In same-release data without that date, the north-east zone changes by under 1 dB and the southern wetland shows about 0 dB year over year. **What still stands:** a step in the southern wetland in late June 2026, visible in both HH and HV (medium confidence on the change, low on the cause), and a seasonal brightening of the farm belt on the southern edge of the box (+3 to +9 dB in Jul to Oct against Jan to Apr 2026; from an AI-assisted pass over the 29 dates that Diego has not reviewed yet). Place names are read off coordinates and must be checked on a map. Any rainy-season statement needs a cited source.
- **Ground sinking is not visible in one GUNW pair.** The raw 12-day picture is a smooth tilt of several centimeters across the valley. After removing the tilt, blobs of about 1 cm remain everywhere, including over the mountains where nothing should be sinking. The motion we expect in 12 days is about that size, so one pair cannot separate signal from noise. Showing sinking needs many pairs added together, which means either remote reads working (gate G1) or 32 to 65 GB of downloads.
- **The file layout matches the documentation**, so cropping and picture-making take seconds per file.

## What the catalog shows

Evidence: [pipeline/reports/summary_mexico_city.md](../pipeline/reports/summary_mexico_city.md) and [granules_mexico_city.csv](../pipeline/reports/granules_mexico_city.csv), produced by `python pipeline/search_granules.py` at 19:32 UTC on Nov 14.

- Two tracks cover 100% of our Mexico City box: **track 19 / frame 11 (ascending)** and track 113 / frame 79 (descending). Three other track/frame combinations touch 0 to 2% of the box and are ignored.
- On track 19 / frame 11 the PROVISIONAL collection holds **29 GCOV dates** (Oct 30, 2025 to Oct 13, 2026, every 12 days with one 24-day step in August) and **28 GUNW pairs that form one unbroken chain** over the same 348 days. Since plan v0.4 the Oct 30, 2025 acquisition is excluded (D-13), which leaves 28 GCOV dates and 27 chained pairs from Nov 11, 2025 to Oct 13, 2026 (336 days).
- The January to June 2026 gap we expected is not there. The older acquisitions have been reprocessed into PROVISIONAL (same processing ID, P05023), so we do not need to mix BETA and PROVISIONAL.
- Polarizations over Mexico City are **HH and HV only**. There is no VV. GUNW is HH only.
- File sizes: GCOV about 7.1 GB each, GUNW about 2.3 GB, SME2 soil moisture about 0.12 GB. At venue Wi-Fi (60 Mbps, assuming 60% real throughput) that is about 26 minutes per GCOV file and 9 minutes per GUNW file.
- SME2 soil moisture exists as PROVISIONAL here (29 dates), but ASF says it is "not yet fully calibrated".

## What each candidate story can and cannot carry

| Story | Verdict | Why |
|---|---|---|
| Ground sinking | **Supported by the catalog. Not yet shown by us.** | Unbroken one-year GUNW chain. NASA/JPL published this signal from NISAR on Apr 29, 2026, from data taken between Oct 25, 2025 and Jan 17, 2026 (wording in the table at the bottom), so we have something to check a map against. Our one local pair shows mostly noise, as expected for 12 days. |
| Seasonal surface change (water, wetlands, vegetation, dry vs. rainy season) | **Supported. Easiest to ship.** | 29 GCOV dates in HH and HV on one track with identical geometry. |
| Soil moisture and farmland | Possible, optional | Small files, but not fully calibrated. Only as a clearly labeled extra. |
| Urban growth at the edges | **Not supported** | One year of data is too short to show growth convincingly. |
| Rainy-season street flooding | **Not supported as a claim** | A 12-day revisit will mostly miss floods that last hours or days, and we have no verified 2026 flood date. We can show open-water change in lakes and wetlands, nothing more. |

## The choice in front of the team

Two stories are supported by the data, and they can be combined.

| Option | What the app says | Cost and risk |
|---|---|---|
| A. Surface change (GCOV) | How the valley's water, wetlands, vegetation, and built-up land look to radar in HH and HV, between seasons and one year apart | Lowest. It is Tier 1 as planned. Needs two to twelve GCOV windows of one release. |
| B. Ground sinking (GUNW) | Where and how fast the ground moves as the old lakebed compacts | Highest. Needs the 28-pair chain, careful processing, and gate G2. NASA has already published the finding, so our contribution would be the interactive tool and the longer time span. |
| A + B. "A city built on a lake" | Both views tied to a handful of landmarks | A is Tier 1, B is Tier 2 behind G2. If B fails, the app is still complete. |

Whatever is chosen, the app keeps what the radar shows separate from what we infer about causes.

## Tiers

| Tier | Content | Ships when |
|---|---|---|
| **1, must ship** | Web map of Mexico City with NISAR GCOV layers (HH, HV, and an HH/HV color composite) for one dry-season and one rainy-season date, a swipe slider between them, 5 to 7 landmark cards (what radar shows, what we infer, human vs. natural driver, sources), a polarization explainer, a "provisional data" label, a sources page. Static files, deployed on Azure, sample data bundled. | Core live by the **Sat 9:30 PM** checkpoint, complete by **Sun 1:00 AM** (G2) |
| **2, if Tier 1 is complete at G2 (Sun 1:00 AM) and the team chose option B** | Ground-motion layer: cumulative line-of-sight movement Oct 2025 to Oct 2026 from the 28 GUNW pairs, with a time-series chart per landmark. GCOV time slider with about monthly frames. | Sanity-checked by **Sun 1:00 AM** (G2), in the app by Sun 8:00 AM |
| **3, only if Tier 2 is in by Sun 7:30 AM** | In order: soil-moisture layer, a second Mexican region through config, Spanish/English toggle, click-anywhere point query through the API, an Azure AI plain-language helper, a data-quality flag. | Probably none. That is fine. |

## Gates

| Gate | Time (CT) | Question | If no |
|---|---|---|---|
| G1 | Sat 4:30 PM | Can we read just the Mexico City window out of a cloud-hosted GCOV file and a GUNW file without downloading whole files? | Switch to full downloads: 2 GCOV files (14 GB, about 55 min) for Tier 1. For Tier 2, 7 dry-season plus 7 rainy-season GUNW pairs (32 GB, about 2 h, on Eduardo's laptop in the evening as soon as G1 fails, shared over LocalSend on a direct Ethernet link). Eduardo approved both sets in advance on Nov 14, 3:05 PM. |
| GS | Sat 5:30 PM | Has the team chosen the story from the data? | Default: option A. Option B stays possible behind G2. |
| Checkpoint | Sat 9:30 PM | Progress report, not a gate: is the core of Tier 1 live on the public URL with real NISAR data? | Nothing is cut. Problems go into the next block. |
| G2 | Sun 1:00 AM | (a) Is all of Tier 1 live, including the polarization explainer, provisional label, sources page, and landmark text? (b) Does our ground-motion map pass the sanity check (sinking where the JPL image shows it, reference area stable, fastest rate in the range JPL and the literature report)? Replaces the old G2 (9:30 PM) and G3 (11:30 PM). | (a) No: no Tier 2; everyone finishes Tier 1, and the JPL result is cited as context only. (b) No: cut the layer, or show only the months that pass, labeled as such; the headline becomes seasonal surface change. |
| G4 | Sun 8:00 AM | Feature freeze. Is main deployed and working? | Roll back to the last good deploy. Bug fixes only from here. |
| G5 | Sun 10:30 AM | Do all submission links open in a private window, and is every form field drafted? | Stop all code. Everyone on the submission. |

## Numbers we may quote, and where they come from

| Claim | Source |
|---|---|
| Preliminary NISAR data from Oct 25, 2025 to Jan 17, 2026 (dry season) show parts of the region "subsiding by more than half an inch (more than 2 centimeters) per month"; the image caption says "up to a few centimeters per month". **Quote JPL's words. Do not convert the units ourselves: half an inch is 1.27 cm, so the article's two figures do not match, and we should not pick one silently.** | NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026: <https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/> |
| In the 1990s and 2000s parts of the metropolitan area were sinking by "around 14 inches (35 centimeters) per year" | Same JPL article |
| The Angel of Independence has had 14 steps added to its base as the land around it sank | Same JPL article |
| Groundwater pumping, the weight of urban development, and compaction of the ancient lakebed are the stated causes | Same JPL article |
| Subsidence rates reach up to 50 cm per year and are almost fully irreversible | Chaussard et al. (2021), JGR Solid Earth, doi:10.1029/2020JB020648. **Read the abstract ourselves before quoting.** |
| Double bounce is most sensitive to HH; volume scattering (for example forest canopy) to cross-polarized HV or VH; rough surface scattering to VV | NASA Earthdata, "What is SAR": <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar> |
| L-band wavelength is about 23 cm | Same NASA Earthdata page |
| A SAR instrument "sends out a pulse of energy" and "records the amount of that energy reflected back after it interacts with Earth" | Same NASA Earthdata page (T-06 claim 1, added 4:00 PM for RB-M01) |
| SAR can collect data "night or day, regardless of weather conditions" | Same NASA Earthdata page (T-06 claim 2) |
| NISAR's L-band radar is "unhindered by clouds or vegetation that impede optical sensors and higher-frequency radars" | Same JPL article (T-06 claim 3) |
| NISAR is "a joint mission developed by NASA and the Indian Space Research Organisation (ISRO)" | Same JPL article (T-06 claim 4) |
| NASA's JPL "provided the satellite's L-band SAR and antenna reflector" | Same JPL article (T-06 claim 5) |
| L-band's longer wavelength "enables it to penetrate more deeply through a tree canopy" | Same NASA Earthdata page (T-06 claim 6) |
| H is horizontal and V is vertical polarization; a signal "emitted in horizontal (H) and received in horizontal (H) would be indicated HH" | Same NASA Earthdata page (T-06 claim 7) |
| PROVISIONAL products are calibrated and validated at a limited set of sites; SME2 is not yet fully calibrated; use caution mixing BETA and PROVISIONAL | ASF, PROVISIONAL known issues (updated Jul 30, 2026): <https://nisar-docs.asf.alaska.edu/provisional-known-issues/> |
| **Source id `earthdata-sar` (added Sat 11:55 PM).** The page Monica linked, <https://www.earthdata.nasa.gov/learn/what-is-sar>, is the same page as the Earthdata rows above. Use the canonical link. Pulse, night or day, and H/V already have rows above. **The page does not say radar sees "through clouds", or that water looks dark.** For clouds, quote the JPL row ("unhindered by clouds or vegetation that impede optical sensors"). | NASA Earthdata, "Synthetic Aperture Radar (SAR)": <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar> |
| **Source id `unam-2007-chalco`.** The old Lake Chalco covered the plain "por varios miles de años hasta principios del siglo XX, cuando fue drenado" (for several thousand years, until the early 20th century, when it was drained). p. 39 | Ortiz Zamora, D. C., and Ortega Guerrero, M. A. (2007), "Origen y evolución de un nuevo lago en la planicie de Chalco: implicaciones de peligro por subsidencia e inundación de áreas urbanas en Valle de Chalco (Estado de México) y Tláhuac (Distrito Federal)", *Investigaciones Geográficas* (UNAM) no. 64, pp. 26–42: <https://scielo.org.mx/pdf/igeo/n64/n64a3.pdf> |
| A system of 14 wells, the Mixquic–Santa Catarina system, has pumped groundwater from the Chalco plain since 1984 (p. 30). **Do not say pumping "began" in 1984.** Intensive pumping in the Chalco sub-basin started in the early 1960s (p. 34). The abstract says the wells were "built in the 1980s". | Same UNAM 2007 study |
| In the centre of the plain, where the lakebed clay is thickest (300 m), pumping compacts the clay and the ground has sunk by up to 40 cm per year. Abstract: "hasta 40 cm/año"; body: "aproximadamente 40 cm/año" (p. 36). | Same UNAM 2007 study |
| The new lake formed in the sinking hollow "como consecuencia del bombeo" (as a consequence of pumping) (p. 39). Water first collected in 1988 as five pools of up to about 1 ha (p. 32). By 1991 the pools had joined into a small lake of about 100 ha (p. 33). | Same UNAM 2007 study |
| At the time of the study (2006 data), the lake surface was 12 m below the original ground level, meaning the level before intensive pumping began in the early 1960s (p. 34). The lake covered "un poco más de 1000 ha" (a little over 1,000 ha) (p. 33; the abstract says 1,000 ha). **The 12 m is a 2006 figure. Do not attach it to 1991.** | Same UNAM 2007 study |
| **A 2007 projection, not a fact.** At about 60 ha a year of growth, the lake would cover about 1,200 ha by 2010 and 1,500 ha by 2015, "incrementando el riesgo por inundación a las zonas urbanas de Tláhuac y Valle de Chalco" (increasing the flood risk to the urban areas of Tláhuac and Valle de Chalco). Abstract and p. 34. We have not checked whether this came true. | Same UNAM 2007 study |
| **A 2007 projection.** The 2015 hazard circle would also reach the eastern part of urban Tláhuac, "directamente las Colonias La Habana y San José, próximas al nuevo lago de Chalco" (directly the La Habana and San José neighbourhoods, next to the new Lake Chalco); about 25 ha of urban land would be flooded (p. 37). | Same UNAM 2007 study |
| **Source id `iahs-2020`.** "A Sentinel-1 based subsidence analysis shows that the highest velocities are located on the eastern sector of the city." Also: "the lower income inhabitants share a proportionally greater economic cost due to land subsidence and associated shallow faulting." Both from the abstract. | Fernández-Torres, E., Cabral-Cano, E., Solano-Rojas, D., Havazli, E., and Salazar-Tlaczani, L. (2020), "Land Subsidence risk maps and InSAR based angular distortion structural vulnerability assessment: an example in Mexico City", *Proc. IAHS* 382, 583: <https://piahs.copernicus.org/articles/382/583/2020/> |
| **Source id `ap-2024-chalco`. Context only.** Do not tie this flood to the lake, to subsidence or to our data; NISAR data starts in 2025. Wording checked word for word against the AP text, Sep 13, 2024, dateline "CHALCO, Mexico (AP)": "Chalco, a low-income suburb southeast of Mexico City"; floodwaters were in homes "for over a month"; "According to Chalco's government, more than 2,000 homes and over 7,000 residents have been affected."; "The water was as deep as 5 feet (160 centimeters) in some areas."; "The flooding delayed the start of the school year by two weeks for thousands of students." | AP, "Residents of Mexico City suburb are anxious after living over a month in black sewage water", Sep 13, 2024: <https://apnews.com/article/mexico-flooding-chalco-climate-8ecc2eb4d9fabd5219fe6850de5addf6>. **Our tools could not open apnews.com.** The text was checked on the AP-credited copy at KVIA: <https://kvia.com/news/2024/09/13/residents-of-mexico-city-suburb-are-anxious-after-living-over-a-month-in-black-sewage-water/>. Open the AP link once in a browser before the freeze. |
| **Attribute the cause to residents, not to AP.** "The low-lying area at the edge of what was once an ancient lake has long been plagued by seasonal flooding, but residents say this year has been worse, a combination of unchecked growth and failing infrastructure." A UNAM expert quoted in the same story, Omar Arellano-Aguilar, says "the combination of drainage failures and the geological structure of the area makes it more vulnerable to floods." The story does not mention heavy rain as a cause. | Same AP story |
| **Source id `nisar-gunw`, our own analysis.** Movement **along the radar line of sight**, Nov 11, 2025 to Oct 13, 2026 (336 days). Positive means away from the satellite (sign: `docs/T35_SIGN_CHECK.md`). Nezahualcoyotl 21.9 cm; Tlahuac 16.4 cm; airport area 15.3 cm; Centro Historico 9.2 cm; Chalco 7.6 cm; Angel de la Independencia 4.3 cm; Iztapalapa 3.3 cm. Treat about 2 cm as the uncertainty of any single number: the hills control point drifts by -2.2 cm. Quote "about", and say "line of sight" once on every card. | Our analysis of 27 consecutive NISAR GUNW pairs (PROVISIONAL, CRID P05023, track 19 / frame 11, HH), relative to a reference box in the western hills (-99.27 to -99.22 E, 19.33 to 19.38 N). Script and README in `poc/mexico_city_sinking/` (PR pending). Values per date in `landmark_series_los_cm.csv`. |
| Same analysis, as rates. About 2.0 cm per month at Nezahualcoyotl over the year. 1% of the valid area moves faster than 24 cm per year (99th percentile). About 338 km² moves faster than 10 cm per year, and about 105 km² faster than 20 cm per year. **Quote percentiles, never the maximum:** isolated unwrapping errors exceed 100 cm per year. Vertical sinking is larger than line of sight: dividing by cos(38°) gives about 1.27 times, assuming purely vertical motion (`docs/T35_SIGN_CHECK.md`). Say "about" and name the assumption whenever a vertical number is quoted. | Same analysis |
| About 3.2 million people live on the ground that moves faster than 10 cm per year along the line of sight (3.23 million on 338 km² when re-run on Nov 14, 11:50 PM). | WorldPop 2020, Mexico, 1 km, UN-adjusted population counts (`mex_ppp_2020_1km_Aggregated_UNadj.tif`, CC BY 4.0, <https://www.worldpop.org/>), laid over the line-of-sight rate map above. Each 80 m pixel takes its share of the 1 km cell's people. |

Anything not in this table needs a source added here before it appears in the app, the slides, or the project page.

**Checked Nov 14, 11:55 PM. These have no row, so keep them out of visible text:**
- "Water looks dark, buildings look bright": not on the Earthdata page.
- The "Dancing with the SARs" dielectric-constant line: not in `docs/challenge/README.md`. Paste the challenge page text there first.
- Tláhuac borders Valle de Chalco (CDMX IPDP), Tláhuac was once an island (CDMX tourism), and Santa Cecilia is next to San José (UNAM thesis): these sources were not read in this pass.
- "The ground around the new lake is among the fastest-moving": the lake point is not in `landmark_series_los_cm.csv`. Sample it before using the sentence.
- Diego's lake HV numbers (+1.2 dB rainy against dry): his lake check, not yet reviewed.
