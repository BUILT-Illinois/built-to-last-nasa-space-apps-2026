# Project Lago

**Mexico City is sinking, and NISAR measured a year of it.**

An interactive, open-source web map of Mexico City built from NASA–ISRO NISAR radar data, by team B[U]ILT to Last at the NASA Space Apps Challenge 2026 Chicago local event.

## Live app

- Azure (main): https://yellow-desert-02401091e.4.azurestaticapps.net
- Cloudflare (backup): https://built-to-last-6or.pages.dev
- Demo Deck: <https://canva.link/r6v27asvbes25e1>

All NISAR data shown is **PROVISIONAL** (NASA and ISRO, CRID P05023).


## Project overview

- **Challenge:** [Dancing with the SARs](https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/). Use NISAR radar data to track and visualize surface change at a place we choose.
- **Story:** the ground under Mexico City is sinking, fastest in the east, on the old lakebed. Where it sank, a new lake formed. The app shows what NISAR measured over one year, from November 2025 to October 2026.
- **What the app shows:**
  - **GUNW ground-motion layer:** the yearly rate of ground motion (cm/yr) along the radar line of sight, from 27 consecutive NISAR GUNW pairs (Nov 11, 2025 to Oct 13, 2026).
  - **Radar brightness layers** from NISAR GCOV: HH, HV and an HH/HV color composite, at 11 dates between November 2025 and October 2026.
  - A **swipe** to compare two layers or two dates.
  - **7 landmark cards** that keep "what the radar shows" separate from "what we infer".
  - A **guided tour** and a "How to read this map" guide.
- **Front end:** `app/`, Vite + React + TypeScript + MapLibre GL JS. The site only loads static files from `app/public/data/`, so it works with no login and without the API.
- **Back end:** `pipeline/` (Python) turns NISAR files into small images plus `manifest.json` and `landmarks.json`. Azure also runs a separate API (`api/`) that serves the same data to other clients; the site does not need it. The file format is [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md).

## Data

- **NISAR L2 GUNW** (geocoded unwrapped interferograms, HH): `NISAR_L2_GUNW_PROVISIONAL_V1`. Source of the ground-motion layer.
- **NISAR L2 GCOV** (radar backscatter, HH and HV): `NISAR_L2_GCOV_PROVISIONAL_V1`. Source of the radar brightness layers.
- Both from the ASF DAAC, track 19, frame 11, ascending. All products are PROVISIONAL.

**How to read the ground motion:** it is measured **along the radar line of sight, not straight down**, relative to a reference area in the western hills (-99.27 to -99.22 E, 19.33 to 19.38 N). Positive means the ground moved away from the satellite.

## What to run

**Web app** (Node 24, same as CI):

The app opens the Valley of Mexico dataset in `app/public/data/mexico_city_valley/`. Set `VITE_REGION_ID=sample` before starting Vite to use the generated test data in `app/public/data/sample/`.

```bash
cd app
npm install
npm run dev                              # the real NISAR data (Valley of Mexico), as on the live site; opens at http://localhost:5173
npm test                                 # app tests
```


**Pipeline** (Python 3.12):

```bash
python -m venv .venv
.venv/bin/pip install -r pipeline/requirements.txt
.venv/bin/python -m pytest pipeline     # run the tests
```

Reading real NISAR files needs a free NASA Earthdata account ([sign up here](https://urs.earthdata.nasa.gov/users/new)). Never commit credentials.

## Team

- **Eduardo:** team lead, science, map screen
- **Elias:** data pipeline, API, deploy
- **Monica:** story, guided tour, design, submission
- **Zainab:** documentation, landmark panel, manifest validator
- **Diego:** data acquisition, layer controls

## More

- Sources and credits for every dataset, basemap and library: [docs/SOURCES.md](docs/SOURCES.md)
- How AI tools were used: [docs/AI_USAGE.md](docs/AI_USAGE.md)
- License: [MIT](LICENSE)