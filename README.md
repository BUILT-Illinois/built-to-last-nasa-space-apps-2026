# built-to-last-nasa-space-apps-2026

Main repo for B[U]ILT Team 2 @ NASA Space Apps 2026's Chicago local event.

> **Work in progress.** Sections marked _TBD_ are filled in as the app is built.

## Project overview

- **Challenge:** [Dancing with the SARs](https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/). Use NISAR radar data to track and visualize surface change at a place we choose.
- **Goal:** an interactive, open-source web map of Mexico City that shows what NISAR radar sees, which polarizations (HH, HV) reveal the changes, and what might cause them. _Story TBD (chosen Sat 5:30 PM)._
- **App:** a web map with radar layers, a swipe to compare two dates, and landmark cards that keep "what the radar shows" separate from "what we infer". Live URL: _TBD_.
- **Front end:** `app/`, Vite + React + TypeScript + MapLibre GL JS. It loads static data files, so it runs with no login and no API.
- **Back end:** `pipeline/` (Python) turns NISAR files into small images plus `manifest.json` and `landmarks.json`. `api/` (Azure Functions) serves the same data to other clients. The file format between them is [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md).
- **Data:** NISAR (NASA and ISRO), Level 2 GCOV, PROVISIONAL release. All NISAR data shown is provisional.

## What to run

**Web app** (Node 20 or newer), runs on the bundled sample data:

```bash
cd app
npm install
npm run dev        # opens at http://localhost:5173
```

**Pipeline** (Python 3.12 or newer):

```bash
python -m venv .venv
.venv/bin/pip install -r pipeline/requirements.txt
.venv/bin/python -m pytest pipeline     # run the tests
```

Reading real NISAR files needs a free [NASA Earthdata login](https://urs.earthdata.nasa.gov/). Never commit credentials.

## More

- Sources for every dataset and library: [docs/SOURCES.md](docs/SOURCES.md)
- How AI tools were used: [docs/AI_USAGE.md](docs/AI_USAGE.md)
- License: [MIT](LICENSE)
