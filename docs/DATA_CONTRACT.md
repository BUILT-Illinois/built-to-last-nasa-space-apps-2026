# Data contract v0.1

This is the interface between the Python pipeline and the web app. The pipeline writes these files, the app and the API only read them. If both sides follow this page, five people can work in parallel against the sample data.

- Owner of the contract: Elias. Write-up kept current by Zainab.
- A change to field names or meanings needs Elias's yes and a line in `docs/DECISIONS.md`. Adding an optional field does not.
- Drafted with AI assistance (Claude Code) and reviewed by the team.
- Sinking contract and ingest instructions drafted with AI assistance (Codex).

## Files per region

```text
app/public/data/<region_id>/
  manifest.json          what layers exist and where their images are
  landmarks.json         places, their text, and their time series
  layers/<layer_id>/<date>.webp     one image per layer per date
  layers/sinking/<date>-<hash>.png  optional single LOS rate overlay
  vectors/<name>.geojson            optional context layers (boundaries and so on)
app/public/data/sample/             same structure, tiny, always in git
```

The app loads `/data/<region_id>/manifest.json` as a same-origin static file. The API serves the same JSON for other clients. The app must work with the API switched off.

## manifest.json

```json
{
  "schemaVersion": "0.1",
  "generatedAt": "2026-11-14T22:00:00Z",
  "generatedBy": "pipeline/build_manifest.py (AI-assisted code, see docs/AI_USAGE.md)",
  "region": {
    "id": "mexico_city",
    "name": "Mexico City (Valley of Mexico)",
    "bbox": [-99.40, 19.10, -98.85, 19.65],
    "center": [-99.13, 19.40],
    "zoom": 10
  },
  "dataMaturity": "PROVISIONAL",
  "layers": [
    {
      "id": "gcov_hh",
      "title": "Radar brightness, HH",
      "kind": "backscatter",
      "product": "GCOV",
      "polarization": "HH",
      "units": "dB",
      "bounds": [-99.40, 19.10, -98.85, 19.65],
      "colormap": { "name": "gray", "min": -25, "max": 0 },
      "description": "One or two plain sentences a non-expert can read.",
      "caveats": ["Provisional NISAR data. Not validated for this area."],
      "frames": [
        {
          "date": "2026-04-16",
          "image": "layers/gcov_hh/2026-04-16.webp",
          "granules": ["NISAR_L2_PR_GCOV_..."],
          "track": 19,
          "frame": 11,
          "direction": "ASCENDING"
        }
      ]
    }
  ],
  "vectors": [
    { "id": "alcaldias", "title": "Boroughs", "file": "vectors/alcaldias.geojson", "source": "source id from sources[]" }
  ],
  "sources": [
    { "id": "nisar-gcov", "title": "NISAR L2 GCOV PROVISIONAL V1", "url": "https://...", "license": "..." }
  ]
}
```

Rules:

- `bbox` and `bounds` are `[west, south, east, north]` in degrees, WGS84.
- Images are rendered in Web Mercator (EPSG:3857) so they line up on the web map. `bounds` are the image's edges.
- Image paths are relative to the folder that holds `manifest.json`.
- `kind` is one of `backscatter`, `composite`, `change`, `displacement`, `soil_moisture`.
- `polarization` is `HH`, `HV`, `HH+HV` (composites), or `null`.
- Dates are `YYYY-MM-DD` in UTC. For `displacement` layers a frame's `date` is the end date and the frame also has `"since": "YYYY-MM-DD"`.
- `colormap.min` and `colormap.max` are in the layer's `units`, and they are what the legend shows.
- Pixels with no data are transparent.
- Every frame lists the exact granule names it came from, so any image can be traced back to NASA's archive.
- Size budget: each image under 1 MB, each region folder under 60 MB.

### Optional Mexico City sinking layer

`sinking` is a `displacement` layer derived from provisional NISAR GUNW. It contains one frame: `since` and `date` are the first and last acquisition dates used to estimate the rate, and `granules` lists the exact GUNW input IDs. This frame shows an annual rate, not cumulative motion. The manifest adds:

| Field | Value |
|---|---|
| `units` | `cm/yr` |
| `losLabel` | `Radar line-of-sight rate` |
| `referenceArea` | Name of the reference area Eduardo used |
| `awaySign` | `negative` (negative means away from the satellite) |
| `colormap` | `{"name":"los-red-white-blue","min":-30,"max":30}` |

The PNG uses a fixed scale: −30 cm/yr is red (`#b2182b`), zero is white, and +30 cm/yr is blue (`#2166ac`). Colors interpolate between these points and saturate at the ends. No-data and uncovered pixels are transparent. The pipeline resamples to an approximately 80 m Web Mercator grid whose edges match the configured Mexico City bbox. It converts units and, when needed, flips the input sign. It does not change the reference area or convert radar line-of-sight motion into vertical motion.

After Eduardo's science check (T-32), confirm the raster is the approved HH ascending track 19/frame 11 product (D-01). From the repo root with the pipeline requirements installed, run this one line in PowerShell. Enter the delivered metadata at the prompts, with the granule IDs separated by spaces.

```powershell
python pipeline/ingest_sinking.py (Read-Host 'GeoTIFF path') --units (Read-Host 'Units: mm/yr or cm/yr') --sign (Read-Host 'Input sign: negative-away or positive-away') --reference (Read-Host 'Reference area') --since (Read-Host 'First acquisition YYYY-MM-DD') --date (Read-Host 'Last acquisition YYYY-MM-DD') --granules ((Read-Host 'Exact GUNW IDs, space-separated').Trim() -split '\s+')
```

The command validates the updated bundle and adds the PNG and layer to the existing `app/public/data/mexico_city/` bundle. Keep the input TIFF outside public data. If the GCOV bundle is rebuilt, rerun the sinking ingest afterward. The existing API manifest route serves the layer on its next build; the asset path remains relative to the static region folder.

For fixtures, use `--synthetic --output <new-or-empty-test-folder>` outside `app/public/data` and omit `--granules`. The fixture records `dataMaturity: "SYNTHETIC"`, `synthetic: true`, and `granules: []`.

## landmarks.json

Text is hand-written in `content/landmarks/<region_id>.json` (Monica writes, Eduardo reviews the science). The pipeline copies it and adds the `series` values sampled from the rasters.

```json
{
  "schemaVersion": "0.1",
  "regionId": "mexico_city",
  "landmarks": [
    {
      "id": "aicm",
      "name": "Benito Juarez International Airport",
      "lon": -99.072,
      "lat": 19.436,
      "summary": "One plain sentence.",
      "radarShows": "What the data shows here, with no interpretation.",
      "weInfer": "What we think causes it, worded as a hypothesis.",
      "drivers": { "human": "text or null", "natural": "text or null" },
      "sourceIds": ["jpl-2026-mexico-city"],
      "series": {
        "hh_db": [{ "date": "2026-04-16", "value": -7.2 }],
        "hv_db": [{ "date": "2026-04-16", "value": -14.9 }],
        "los_displacement_cm": [{ "date": "2025-11-11", "value": -0.6 }]
      }
    }
  ]
}
```

Rules:

- A series a landmark does not have is left out. The app hides the matching chart.
- `value` may be `null` for a date with no valid data. The chart shows a gap, not a zero.
- `los_displacement_cm` is cumulative movement along the radar's line of sight since the first date, relative to our reference area. Negative means away from the satellite. It is not vertical sinking unless we say how we converted it.
- Coordinates in the example above are placeholders. Take real ones from a named source.

## API (same data, typed)

| Route | Returns |
|---|---|
| `GET /api/health` | `{ "ok": true, "version": "<git sha>" }` |
| `GET /api/regions` | list of `{ id, name, bbox }` |
| `GET /api/regions/{id}/manifest` | the manifest |
| `GET /api/regions/{id}/landmarks` | the landmarks file |

Errors use `{ "success": false, "message": "..." }` with a matching HTTP status. The TypeScript types live in `app/src/types/manifest.ts` and are shared with `api/`.

## Checking a file

`python pipeline/validate_manifest.py app/public/data/<region_id>` must exit 0 before a data folder is committed. It checks required fields, date formats, bounds order, that every image and vector file exists, and the size budget.
