# built-to-last-nasa-space-apps-2026

Main repo for B[U]ILT Team 2 @ NASA Space Apps 2026's Chicago local event.

> **Work in progress.** Sections marked _TBD_ are filled in as the app is built.

## Project Lago

- **Challenge:** [Dancing with the SARs](https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/). Use NISAR radar data to track and visualize surface change at a place we choose.
- **Goal:** an interactive, open-source web map of a place we choose that shows what NISAR radar sees, which polarizations (HH, HV) reveal the changes, and what might cause them. The map shows surface change across 11 months of NISAR GCOV observations from November 2025 to October 2026, with 11 frames per radar layer and no April 2026 frame.
- **App:** a web map with radar layers, a swipe to compare two dates, and landmark cards that keep "what the radar shows" separate from "what we infer". See [Live app](#live-app).
- **Front end:** `app/`, Vite + React + TypeScript + MapLibre GL JS. The site only loads static files from `app/public/data/`, so it works with no login and without the API.
- **Back end:** `pipeline/` (Python) turns NISAR files into small images plus `manifest.json` and `landmarks.json`. Azure also runs a separate API (`api/`) that serves the same data to other clients; the site does not need it. The file format is [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md).
- **Data:** NISAR (NASA and ISRO), Level 2 GCOV and GUNW, PROVISIONAL release. The GUNW ground-motion layer shows annualized line-of-sight rates from 336 days of measurements (Nov 11, 2025 to Oct 13, 2026) across the Valley of Mexico. All NISAR data shown is provisional.

## What to run

**Web app** (Node 24, same as CI):

The app opens the Valley of Mexico dataset in `app/public/data/mexico_city_valley/`. Set `VITE_REGION_ID=sample` before starting Vite to use the generated test data in `app/public/data/sample/`.

```bash
cd app
npm install
npm run dev        # opens at http://localhost:5173
```

**Pipeline** (Python 3.12):

```bash
python -m venv .venv
.venv/bin/pip install -r pipeline/requirements.txt
.venv/bin/python -m pytest pipeline     # run the tests
```

Reading real NISAR files needs a free NASA Earthdata account ([sign up here](https://urs.earthdata.nasa.gov/users/new)). Never commit credentials.

## More

- Sources for every dataset and library: [docs/SOURCES.md](docs/SOURCES.md)
- How AI tools were used: [docs/AI_USAGE.md](docs/AI_USAGE.md)
- License: [MIT](LICENSE)

## Live app

- Azure (main): https://yellow-desert-02401091e.4.azurestaticapps.net
- Cloudflare (backup): https://built-to-last-6or.pages.dev
