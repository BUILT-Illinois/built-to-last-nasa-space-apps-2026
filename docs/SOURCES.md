# Sources

Every dataset, text, library and tool the project uses. This list feeds the "Space Agency Partner Data and Other References" field on the project page (T-52). Owner: Zainab. Add a line whenever you use something new.

**Datasets**
- NISAR L2 GCOV (radar backscatter, HH and HV), collection `NISAR_L2_GCOV_PROVISIONAL_V1`, track 19 / frame 11, NASA and ISRO | <https://nisar-docs.asf.alaska.edu/>
  - Exact granule names for every image are listed in each region's `manifest.json`.
- NISAR L2 GUNW (ground motion), only if Tier 2 ships | <https://nisar-docs.asf.alaska.edu/>

**Text sources** (claims we may quote are in the "Numbers we may quote" table of [DECISION_MEMO.md](DECISION_MEMO.md))
- NASA/JPL, "US-Indian Space Mission Maps Extreme Subsidence in Mexico City", Apr 29, 2026 | <https://www.jpl.nasa.gov/news/us-indian-space-mission-maps-extreme-subsidence-in-mexico-city/>
- NASA Earthdata, "What is Synthetic Aperture Radar?" | <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar>
- Chaussard et al. (2021), JGR Solid Earth, doi:10.1029/2020JB020648 | <https://doi.org/10.1029/2020JB020648>
- ASF, "PROVISIONAL known issues" | <https://nisar-docs.asf.alaska.edu/provisional-known-issues/>

**Learning resources**
- NASA Earthdata Search | <https://search.earthdata.nasa.gov/search>
- ASF Vertex | <https://search.asf.alaska.edu/>
- NISAR Data User Guide | <https://nisar-docs.asf.alaska.edu/>
- Intro to Remote Sensing | <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/remote-sensing>
- Intro to SAR | <https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar>
- NASA ARSET trainings | <https://appliedsciences.nasa.gov/get-involved/training>
- NISAR StoryMaps | <https://nisar.jpl.nasa.gov/applications/arcgis-storymaps/>
- NISAR Applications White Papers | <https://nisar.jpl.nasa.gov/applications/societal-benefit/>
- UAVSAR Postcards | <https://uavsar.jpl.nasa.gov/education/postcards.html>
- CSA SAR Python and QGIS tutorial | <https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial>

**Libraries**
- Web app (`app/package.json`): MapLibre GL JS, React, Zustand, Vite, Vitest, TypeScript, ESLint
- Pipeline (`pipeline/requirements.txt`): asf_search, earthaccess, h5py, NumPy, pyproj, Pillow, rasterio, pytest

**Map layers**
- Basemap and optical imagery: _TBD (T-09, with license and attribution)_

**Tools**
- Claude Code (Anthropic) and Codex (OpenAI), AI coding assistants, see [AI_USAGE.md](AI_USAGE.md)
- GitHub (code and reviews), Azure Static Web Apps (hosting), VS Code (editor)
