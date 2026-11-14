# Decision memo: what we build over Mexico City

Status: **the story is open. The team analyses the data and decides by Sat Nov 14, 5:30 PM CT (gate GS).** Updated 2:45 PM with a first look at the files in `Datasets/`. Updated 3:55 PM: gates G2 and G3 merged into one go/no-go at Sun 1:00 AM (plan v0.3).

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

- **Surface change is visible in GCOV right away.** Between the two dates (same season, one year apart) the dark lakebed zone north-east of the airport is clearly darker in HV in 2026, and patches in the southern wetland and farm zone are brighter. Place names here are read off pixel positions and must be checked on a map. The whole scene is also about 1.4 dB brighter in HV in 2026, which is probably the two different processing releases and not the ground. So the pattern is promising and the numbers are not yet trustworthy.
- **Ground sinking is not visible in one GUNW pair.** The raw 12-day picture is a smooth tilt of several centimeters across the valley. After removing the tilt, blobs of about 1 cm remain everywhere, including over the mountains where nothing should be sinking. The motion we expect in 12 days is about that size, so one pair cannot separate signal from noise. Showing sinking needs many pairs added together, which means either remote reads working (gate G1) or 32 to 65 GB of downloads.
- **The file layout matches the documentation**, so cropping and picture-making take seconds per file.

## What the catalog shows

Evidence: [pipeline/reports/summary_mexico_city.md](../pipeline/reports/summary_mexico_city.md) and [granules_mexico_city.csv](../pipeline/reports/granules_mexico_city.csv), produced by `python pipeline/search_granules.py` at 19:32 UTC on Nov 14.

- Two tracks cover 100% of our Mexico City box: **track 19 / frame 11 (ascending)** and track 113 / frame 79 (descending). Three other track/frame combinations touch 0 to 2% of the box and are ignored.
- On track 19 / frame 11 the PROVISIONAL collection holds **29 GCOV dates** (Oct 30, 2025 to Oct 13, 2026, every 12 days with one 24-day step in August) and **28 GUNW pairs that form one unbroken chain** over the same 348 days.
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
| PROVISIONAL products are calibrated and validated at a limited set of sites; SME2 is not yet fully calibrated; use caution mixing BETA and PROVISIONAL | ASF, PROVISIONAL known issues (updated Jul 30, 2026): <https://nisar-docs.asf.alaska.edu/provisional-known-issues/> |

Anything not in this table needs a source added here before it appears in the app, the slides, or the project page.
