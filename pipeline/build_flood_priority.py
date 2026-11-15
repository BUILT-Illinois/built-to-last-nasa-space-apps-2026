"""Build the Mexico City flood-prevention screening layer (AI-assisted, see docs/AI_USAGE.md)."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.transform import rowcol, xy
from rasterio.warp import Resampling, reproject

from build_manifest import (
    ROOT, TIER_2_REGION_LIMIT, WEB_CRS, map_grid, read_scene, write_json, write_webp,
)
from fetch_crops import find_granule, monthly_dates, output_path
from quicklook import stretch

REGION = "mexico_city"
CONFIG = Path(__file__).with_name("config") / "flood_priority.json"
SCORING_POINTS = CONFIG.with_name("flood_priority_points.json")
CELL_METERS = 500
TO_UTM = Transformer.from_crs(WEB_CRS, "EPSG:32614", always_xy=True)
TO_WEB = Transformer.from_crs("EPSG:4326", WEB_CRS, always_xy=True)
TO_LONLAT = Transformer.from_crs("EPSG:32614", "EPSG:4326", always_xy=True)
METHOD = "0.5 × (clipped LOS away rate / positive-rate p95) + 0.5 × (water months / 12)"
DESCRIPTION = "Screening index for where to investigate flood-prevention investment first."
CAVEATS = [
    "GUNW measures motion along the radar line of sight relative to a reference area, not true vertical sinking.",
    "Dark HH and HV flag possible open water. Vegetation can hide water and other dark surfaces can be flagged.",
    "This screening index does not predict flooding. It excludes drainage capacity, rainfall and exposure.",
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def water_persistence(crop_dir, bbox, config):
    dates = monthly_dates(REGION)
    if len(dates) != 12 or dates[0] != "2025-11-11" or dates[-1] != "2026-10-13":
        raise ValueError("T-34 requires the approved 12 monthly GCOV dates")
    shape, grid = map_grid(bbox)
    water = np.zeros(shape, dtype=np.uint8)
    coverage = np.ones(shape, dtype=bool)
    granules = []
    for day in dates:
        row = find_granule(REGION, "GCOV", day)
        granules.append(row["scene_name"])
        path = crop_dir / output_path(REGION, "GCOV", day).name
        hh, hv, _ = read_scene(path, granules[-1], shape, grid)
        coverage &= np.isfinite(hh) & np.isfinite(hv)
        water += (hh <= config["hh_db"]) & (hv <= config["hv_db"])
    return dates, grid, granules, water, coverage


def pixel(grid, point):
    return rowcol(grid, *TO_WEB.transform(point["lon"], point["lat"]))


def valid_pixel(mask, row, col):
    return 0 <= row < mask.shape[0] and 0 <= col < mask.shape[1] and bool(mask[row, col])


def read_los(path, metadata, shape, grid):
    for key in ("units", "referenceArea", "source", "granules", "positiveDirection",
                "track", "frame", "direction"):
        if not metadata.get(key):
            raise ValueError(f"LOS metadata requires {key}")
    if metadata["units"] not in {"mm/year", "cm/year", "m/year"}:
        raise ValueError("LOS units must be mm/year, cm/year or m/year")
    if metadata["positiveDirection"] not in {"toward", "away"}:
        raise ValueError("LOS positiveDirection must be toward or away the sensor")
    if (metadata["track"], metadata["frame"], metadata["direction"]) != (19, 11, "ASCENDING"):
        raise ValueError("T-34 requires GUNW track 19/frame 11 ascending")
    if not isinstance(metadata["granules"], list) or not all(
        isinstance(name, str) and name.startswith("NISAR_L2_PR_GUNW_") for name in metadata["granules"]
    ):
        raise ValueError("LOS granules must list the exact GUNW source granule names")

    with rasterio.open(path) as source:
        if source.count != 1 or not source.crs:
            raise ValueError("LOS raster must be a single-band georeferenced GeoTIFF")
        values = source.read(1, masked=True).astype(np.float32).filled(np.nan)
        values[~np.isfinite(values)] = np.nan
        rate = np.full(shape, np.nan, dtype=np.float32)
        reproject(
            values, rate, src_transform=source.transform, src_crs=source.crs, src_nodata=np.nan,
            dst_transform=grid, dst_crs=WEB_CRS, dst_nodata=np.nan, resampling=Resampling.nearest,
        )
    return rate


def score_pixels(rate, water, valid, positive_direction):
    away = rate if positive_direction == "away" else -rate
    positive = away[valid & (away > 0)]
    if not positive.size:
        raise ValueError("No valid motion away from the sensor for normalization. Check coverage and sign.")
    reference = float(np.percentile(positive, 95))
    score = (np.clip(away / reference, 0, 1) + water / 12) / 2
    return score, reference


def ranked_cells(grid, valid, rate, water, score, positive_direction):
    rows, cols = np.indices(valid.shape)
    x, y = TO_UTM.transform(*xy(grid, rows.ravel(), cols.ravel()))
    cells = np.floor(np.column_stack((x, y)) / CELL_METERS).astype(int)
    keys, membership = np.unique(cells, axis=0, return_inverse=True)
    selected = membership[valid.ravel()]
    n = np.bincount(selected, minlength=len(keys))
    total = np.bincount(membership, minlength=len(keys))
    qualified = np.flatnonzero((n > 0) & (n * 2 >= total))
    if qualified.size < 10:
        raise ValueError("Fewer than ten 500 m cells have sufficient joint coverage")
    averages = [
        np.bincount(selected, weights=band[valid], minlength=len(keys))[qualified] / n[qualified]
        for band in (rate, water, score)
    ]
    away_rates = averages[0] if positive_direction == "away" else -averages[0]
    # Competition rank among the same eligible cells, using unclipped mean LOS rates.
    sinking_ranks = 1 + len(away_rates) - np.searchsorted(np.sort(away_rates), away_rates, side="right")
    results = {}
    previous_score = None
    for position, index in enumerate(np.argsort(-averages[2], kind="stable"), 1):
        key = qualified[index]
        easting, northing = map(int, keys[key] * CELL_METERS)
        lon, lat = TO_LONLAT.transform(easting + CELL_METERS / 2, northing + CELL_METERS / 2)
        los, months, cell_score = (float(values[index]) for values in averages)
        if cell_score != previous_score:
            rank = position
        results[(easting // CELL_METERS, northing // CELL_METERS)] = {
            "rank": rank, "cellId": f"{easting}-{northing}", "lon": lon, "lat": lat,
            "losRate": los, "waterMonths": months, "score": cell_score,
            "validFraction": float(n[key] / total[key]), "sinkingRank": int(sinking_ranks[index]),
        }
        previous_score = cell_score
    return results


def point_result(point, grid, coverage, valid, rate, water, score, cells):
    row, col = pixel(grid, point)
    has_water = valid_pixel(coverage, row, col)
    has_score = valid_pixel(valid, row, col)
    x, y = TO_UTM.transform(*TO_WEB.transform(point["lon"], point["lat"]))
    containing = cells.get((int(x // CELL_METERS), int(y // CELL_METERS))) if has_water else None
    return {
        **point, "gcovCoverage": has_water,
        "losRate": float(rate[row, col]) if has_score else None,
        "waterMonths": int(water[row, col]) if has_water else None,
        "score": float(score[row, col]) if has_score else None,
        "cellRank": containing["rank"] if containing else None,
        "sinkingRank": containing["sinkingRank"] if containing else None,
    }


def build(crop_dir, output, los_path=None, metadata_path=None, *, water_output=None):
    config = read_json(CONFIG)
    manifest = read_json(output / "manifest.json")
    if manifest["region"]["id"] != REGION or manifest["schemaVersion"] != "0.1":
        raise ValueError("Expected a Mexico City v0.1 manifest")
    bbox = manifest["region"]["bbox"]
    dates, grid, gcov_granules, water, coverage = water_persistence(crop_dir, bbox, config)
    checks = read_json(SCORING_POINTS)
    lake = next(point for point in checks if point["id"] == "new-lake-chalco")
    lake_row, lake_col = pixel(grid, lake)
    if not valid_pixel(coverage, lake_row, lake_col):
        raise ValueError("New Lake Chalco has incomplete GCOV coverage")
    print(f"Water thresholds: HH <= {config['hh_db']} dB; HV <= {config['hv_db']} dB")
    for point in checks:
        row, col = pixel(grid, point)
        months = int(water[row, col]) if valid_pixel(coverage, row, col) else None
        print(f"{point['name']}: {months if months is not None else 'incomplete GCOV coverage'}"
              + (f" of {len(dates)} open-water months" if months is not None else ""))
    if water_output is not None:
        water_output.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(
            water_output, "w", driver="GTiff", height=water.shape[0], width=water.shape[1],
            count=1, dtype="uint8", crs=WEB_CRS, transform=grid, nodata=255, compress="deflate",
        ) as raster:
            raster.write(np.where(coverage, water, 255), 1)
            raster.set_band_description(1, "GCOV open-water months")
            raster.update_tags(dates=",".join(dates), hh_db=config["hh_db"], hv_db=config["hv_db"])
    if los_path is None:
        return

    metadata = read_json(metadata_path)
    rate = read_los(los_path, metadata, water.shape, grid)
    valid = coverage & np.isfinite(rate)
    score, reference = score_pixels(rate, water, valid, metadata["positiveDirection"])
    cells = ranked_cells(grid, valid, rate, water, score, metadata["positiveDirection"])
    landmarks = read_json(output / "landmarks.json")["landmarks"]
    points = [{key: entry[key] for key in ("id", "name", "lon", "lat")} for entry in landmarks]

    def sample(point):
        return point_result(point, grid, coverage, valid, rate, water, score, cells)

    hotspots = {
        "schemaVersion": "0.1", "regionId": REGION, "units": {"losRate": metadata["units"],
                                                            "waterMonths": "months", "score": "index (0–1)"},
        "method": METHOD, "los": metadata, "awayRateP95": reference, "dates": dates,
        "waterThresholdDb": {"HH": config["hh_db"], "HV": config["hv_db"]},
        "cellSizeMeters": CELL_METERS, "rankedCellCount": len(cells),
        "areas": list(cells.values())[:10], "landmarks": [sample(point) for point in points],
        "checks": [sample(point) for point in checks if point["id"] != lake["id"]],
        "lakeCheck": sample(lake),
    }
    image = Path("layers") / "flood_priority" / f"{dates[-1]}.webp"
    layer = {
        "id": "flood_priority", "title": "Flood-prevention priority",
        "kind": "priority", "product": "GCOV+GUNW", "polarization": None, "units": "index (0–1)",
        "bounds": bbox, "colormap": {"name": "gray", "min": 0, "max": 1},
        "description": DESCRIPTION, "caveats": CAVEATS,
        "frames": [{
            "date": dates[-1], "image": image.as_posix(),
            "granules": list(dict.fromkeys(gcov_granules + metadata["granules"])),
            "track": metadata["track"], "frame": metadata["frame"], "direction": metadata["direction"],
        }],
    }
    manifest["layers"] = [entry for entry in manifest["layers"] if entry["id"] != layer["id"]] + [layer]
    manifest["generatedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    manifest["generatedBy"] = "pipeline/build_flood_priority.py (AI-assisted code, see docs/AI_USAGE.md)"
    with TemporaryDirectory(prefix=".flood-priority-", dir=output.parent) as tmp:
        stage = Path(tmp)
        gray = stretch(np.where(valid, score, 0), 0, 1)
        write_webp(stage / image, [gray] * 3, valid)
        write_json(stage / "hotspots.json", hotspots)
        write_json(stage / "manifest.json", manifest)
        files = (image, Path("hotspots.json"), Path("manifest.json"))
        existing_size = sum(path.stat().st_size for path in output.rglob("*")
                            if path.is_file() and path.relative_to(output) not in files)
        if existing_size + sum((stage / path).stat().st_size for path in files) >= TIER_2_REGION_LIMIT:
            raise ValueError("Region folder must stay under 60 MB")
        (output / image).parent.mkdir(parents=True, exist_ok=True)
        for path in files:
            (stage / path).replace(output / path)
    print(f"Wrote {output / 'hotspots.json'} and the flood-priority layer")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop-dir", required=True, type=Path)
    parser.add_argument("--output", default=ROOT / "app/public/data" / REGION, type=Path)
    parser.add_argument("--water-output", type=Path, help="Write an optional local persistence GeoTIFF")
    parser.add_argument("--los", type=Path, help="Eduardo's line-of-sight rate GeoTIFF")
    parser.add_argument("--los-metadata", type=Path, help="JSON provenance for the LOS rate")
    args = parser.parse_args()
    if (args.los is None) != (args.los_metadata is None):
        parser.error("--los and --los-metadata are required together")
    try:
        build(args.crop_dir, args.output, args.los, args.los_metadata, water_output=args.water_output)
    except (ValueError, OSError, KeyError, rasterio.errors.RasterioError) as error:
        parser.exit(1, f"Flood-priority build failed: {error}\n")


if __name__ == "__main__":
    main()
