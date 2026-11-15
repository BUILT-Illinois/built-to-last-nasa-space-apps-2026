# T-34 flood-prevention priority

The index screens for places to investigate first. GUNW measures relative line-of-sight
motion, which can include horizontal movement. Persistent low radar return is a proxy for
open water, with false detections possible on other dark surfaces and missed detections on
vegetated or rough water. Drain slopes, flood depth, drainage capacity, rainfall, and
exposure were not measured. The 2024 flood locations predate the radar series and are
plausibility checks. Conagua also reports a new collector serving both areas.
[Conagua](https://www.gob.mx/conagua/prensa/la-entrada-en-operacion-del-colector-chalco-reduce-riesgos-de-inundaciones-en-el-municipio-de-chalco?idiom=es-MX)

## GCOV checks

The 12 approved HH/HV crops run from 2025-11-11 through 2026-10-13. The builder uses the
existing GCOV map grid and dB reprojection, then counts months in which HH ≤ −12 dB and
HV ≤ −20 dB together. It requires both channels to be valid in all 12 months.

At the supplied New Lake Chalco point (19.27, −98.97), the thresholds flag 7 of 12 months.
The median in the surrounding 5×5 pixels is 6 months. Cutoffs of −14/−22 dB flag 2 months
at the point and a median of 0 in the window. At the adopted thresholds, 0.13% of the
GCOV study grid is flagged in all 12 months. The cutoffs are provisional.
[Lake context from the team's data exploration](../coordination/claude_status_monica.md)

At Centro (Zócalo), Nezahualcóyotl, and the Angel of Independence, all 25 pixels in each
5×5 window registered zero open-water months. The airport point registered zero, with a
window median of zero and a maximum of two. We kept the cutoffs after these checks.
All 11 temporary points have both GCOV channels in all 12 months. New Lake Chalco is
the only point that flagged open water. Bosque de Tláhuac lake registered zero in its
entire 5×5 window, so some known water is missed at these cutoffs. The two 2024 flood
checks are street locations and each registered zero in the later GCOV series.

| 2024 flood check | Latitude | Longitude | Geocode |
| --- | ---: | ---: | --- |
| Culturas de México | 19.2651324 | −98.90459718 | [Municipal service point BACH-20](https://datosabiertos.chalco.gob.mx/repositorio/reportes-de-bacheo/) |
| San Miguel Jacalones II | 19.2708333 | −98.8977778 | [Municipal risk atlas locality point, code 027](https://www.scribd.com/document/682368048/Atlas-Chalco-2019-009) |

The scores and ranks require Eduardo's rate raster. Each geocode checks the cell
containing a representative point. [Estado de México 2025 flood atlas](https://caem.edomex.gob.mx/sites/caem.edomex.gob.mx/files/files/AtlasInundaciones/Atlas2025/VersionEjecutivaAtlasXXXI2025.pdf)

## Score and ranking

For pixels with both measurements, convert the signed LOS rate to positive-away for
scoring. Divide by the 95th percentile of positive-away rates across the joint coverage
and clip to [0, 1]. Average that normalized rate with water months divided by 12, giving
each input equal weight. The API reports signed LOS rates in the supplied source units.

Group jointly valid pixels by center in 500 m × 500 m UTM zone 14N cells. Rank cells by
the mean pixel score, highest first. A cell needs at least half of its in-region pixels
to have both inputs. The output reports the mean signed LOS rate and mean water months
for the same pixels. Exact ties share a rank, with UTM coordinates ordering rows in a
tie. The top ten cell rows are bundled with the point results. Sinking-only rank orders
the same eligible cells by mean LOS motion away from the sensor, highest first, using
the unclipped rate and the same jointly valid pixels. Both ranks are reported for the
cells containing the two 2024 flood-zone points.

The temporary file [flood_priority_points.json](../pipeline/config/flood_priority_points.json)
supplies the 11 scoring points while the landmark content is pending. The build samples
their pixel values and attaches the ranks of their containing cells. It reads the published
landmark file independently and also scores any entries it contains.

## Build

Run from the repository root against the current region bundle after the monthly GCOV
build. Run this again after any monthly GCOV rebuild to republish the priority manifest entry.

```sh
python pipeline/build_flood_priority.py --crop-dir path/to/gcov/crops \
  --los path/to/los-rate.tif --los-metadata path/to/los-rate.json
```

Omit the two LOS arguments to check the water inputs without publishing a layer. Add
`--water-output data/water_persistence.tif` to save the local 0–12 month count raster. Use
`--output` to run against a copy of the region bundle. The input GeoTIFF needs one rate
band, a CRS, and a nodata value or mask for pixels without a rate. The local provenance
JSON supplies the following fields. Use Eduardo's actual values.

| Key | Value |
| --- | --- |
| `units` | `mm/year`, `cm/year`, or `m/year` |
| `positiveDirection` | `toward` or `away` the sensor |
| `referenceArea` | Named GUNW reference area |
| `source` | Source file name and revision or public provenance link |
| `granules` | Exact contributing NISAR GUNW granule names |
| `track`, `frame`, `direction` | 19, 11, `ASCENDING` |

Commit the derived WebP, hotspots JSON, and manifest. The generator enforces the 1 MB
image and 60 MB region caps. The static deployment includes the JSON next to the
manifest. Azure also serves it at `GET /api/regions/mexico_city/hotspots`.
