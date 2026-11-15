"""Mask the swath-edge artifact in the valley-wide sinking rasters.

Drafted with AI assistance (Claude Code), see docs/AI_USAGE.md.

On the 27 valley-wide crops (lon -99.60 to -98.60, lat 19.00 to 19.90), the north-west corner of the
box reaches the edge of the radar swath. A band about 60 pixels (5 km) wide along that edge reads
80 to 90 cm/yr away from the satellite, then ramps down to the normal 20 cm/yr. That is far beyond
any published rate and follows the swath edge, not the geology, so it is an edge artifact.

This script fits a straight line to the swath edge (the first valid column of each row near the
top) and sets every pixel within BUFFER_PX columns of that line to NaN, in both GeoTIFFs. It writes
*_masked.tif next to the inputs and leaves the originals untouched.

Usage: python mask_swath_edge.py <folder with los_rate_cm_per_year.tif and los_total_cm.tif>
"""
import sys
from pathlib import Path

import numpy as np
import rasterio

BUFFER_PX = 75  # 6 km at 80 m; the artifact plus its ramp is about 65 pixels wide
FIT_ROWS = 85   # rows where the swath edge is inside the box

folder = Path(sys.argv[1])
with rasterio.open(folder / "los_rate_cm_per_year.tif") as src:
    rate = src.read(1)
valid = ~np.isnan(rate)
rows = [r for r in range(FIT_ROWS) if valid[r].any() and not valid[r, 0]]
first = [int(np.argmax(valid[r])) for r in rows]
slope, intercept = np.polyfit(rows, first, 1)
r_idx, c_idx = np.indices(rate.shape)
edge_mask = c_idx < (intercept + slope * r_idx + BUFFER_PX)
print(f"swath edge: col = {intercept:.1f} + {slope:.2f} * row; masking {int((edge_mask & valid).sum())} valid pixels")

for name in ("los_rate_cm_per_year", "los_total_cm"):
    with rasterio.open(folder / f"{name}.tif") as src:
        band = src.read(1)
        profile, tags = src.profile, src.tags()
    band[edge_mask] = np.nan
    tags["swath_edge_mask"] = f"pixels within {BUFFER_PX} px of the swath edge set to NaN (mask_swath_edge.py)"
    out = folder / f"{name}_masked.tif"
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(band, 1)
        dst.update_tags(**tags)
    left = np.nanpercentile(band, [1, 50, 99])
    print(f"wrote {out.name}: p1/p50/p99 {left.round(1)}, pixels > 40: {int((band > 40).sum())}")
