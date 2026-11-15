"""Build the GCOV map bundle. Drafted with AI assistance (Codex)."""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from math import ceil
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject, transform_bounds

from fetch_crops import OUTPUT_DIR, fetch_crop, find_granule, monthly_dates, output_path
from landmark_series import EXCLUDED, enrich, include_points
from quicklook import CONFIG_PATH, stretch, to_db

ROOT = Path(__file__).resolve().parents[1]
WEB_CRS = "EPSG:3857"
GEOGRAPHIC_CRS = "EPSG:4326"
PIXEL_METERS = 80
IMAGE_LIMIT = 1_000_000
TIER_1_REGION_LIMIT = 30_000_000
TIER_2_REGION_LIMIT = 60_000_000
LAYERS = (
    ("gcov_hh", "Radar brightness, HH", "backscatter", "HH", "dB",
     "Radar brightness when the signal is transmitted and received horizontally."),
    ("gcov_hv", "Radar brightness, HV", "backscatter", "HV", "dB",
     "Radar brightness when the signal is transmitted horizontally and received vertically."),
    ("gcov_composite", "HH/HV color composite", "composite", "HH+HV", "normalized",
     "Red shows HH, green shows HV, and blue shows HH minus HV in dB. "
     "Each channel is scaled independently using the same limits across dates."),
)
GCOV_SOURCE = {
    "id": "nisar-gcov",
    "title": "NISAR L2 GCOV PROVISIONAL V1 (NASA/ISRO, ASF DAAC)",
    "url": "https://nisar-docs.asf.alaska.edu/earthdata-search/",
    "license": "NASA Earthdata open data (see Earthdata Data Use Guidance)",
}


def merge_sources(sources, extra):
    """Add the card file's sources to the manifest, keeping the first entry for each id.

    The landmark cards cite sources by id, and the validator checks every id against the
    manifest's sources[]. Added Sun Nov 15 so the cards' citations validate (PR #35)."""
    seen = {source.get("id") for source in sources}
    merged = list(sources)
    for source in extra:
        if isinstance(source, dict) and source.get("id") not in seen:
            merged.append(source)
            seen.add(source.get("id"))
    return merged


def map_grid(bbox):
    west, south, east, north = transform_bounds(GEOGRAPHIC_CRS, WEB_CRS, *bbox)
    width = ceil((east - west) / PIXEL_METERS)
    height = ceil((north - south) / PIXEL_METERS)
    return (height, width), from_bounds(west, south, east, north, width, height)


def read_scene(path, granule, shape, target):
    with np.load(path, allow_pickle=False) as crop:
        if crop["granule"].item() != granule:
            raise ValueError(f"Crop {path.name} does not match approved granule {granule}")
        x, y = crop["xCoordinates"], crop["yCoordinates"]
        dx, dy = np.diff(x), -np.diff(y)
        if not (dx.size and dy.size and dx[0] > 0 and dy[0] > 0
                and np.allclose(dx, dx[0]) and np.allclose(dy, dy[0])):
            raise ValueError(f"Crop {path.name} must use a regular north-up grid")
        source = from_bounds(x[0] - dx[0] / 2, y[-1] - dy[0] / 2,
                             x[-1] + dx[0] / 2, y[0] + dy[0] / 2, x.size, y.size)
        bands = []
        for name in ("HHHH", "HVHV"):
            power = crop[name]
            if power.shape != (y.size, x.size):
                raise ValueError(f"Crop {path.name} has an invalid {name} shape")
            band = np.empty(shape, dtype=np.float32)
            reproject(
                to_db(power), band, src_transform=source,
                src_crs=f"EPSG:{int(crop['projection'].item())}", src_nodata=np.nan,
                dst_transform=target, dst_crs=WEB_CRS, dst_nodata=np.nan,
                resampling=Resampling.bilinear,
            )
            if not np.isfinite(band).any():
                raise ValueError(f"Crop {path.name} has no valid {name} pixels in the map bounds")
            bands.append(band)
    hh, hv = bands
    return hh, hv, hh - hv


def percentile_limits(bands):
    valid = np.concatenate([band[np.isfinite(band)] for band in bands])
    if not valid.size:
        raise ValueError("No overlapping valid HH and HV pixels for the composite")
    low, high = map(float, np.percentile(valid, [2, 98]))
    return (low, high) if low < high else (low - 0.5, high + 0.5)


def write_webp(path, rgb, valid):
    path.parent.mkdir(parents=True, exist_ok=True)
    rgba = np.dstack((*rgb, valid.astype(np.uint8) * 255))
    image = Image.fromarray(rgba)
    for quality in (88, 75, 60, 45, 25):
        image.save(path, format="WEBP", quality=quality, method=4)
        if path.stat().st_size < IMAGE_LIMIT:
            return
    raise ValueError(f"{path.name} exceeds the 1 MB per-image budget")


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def build(region_id, dates, crop_dir, output, *, offline=False):
    dates = sorted(dates)
    if len(dates) < 2 or len(set(dates)) != len(dates):
        raise ValueError("Provide at least two distinct scene dates")
    region_limit = TIER_1_REGION_LIMIT if len(dates) == 2 else TIER_2_REGION_LIMIT
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if region_id not in config["regions"]:
        raise ValueError(f"Unknown region: {region_id}")
    region = config["regions"][region_id]
    bbox = region["bbox"]
    shape, target = map_grid(bbox)

    # Resolve every date before fetching anything.
    catalog = {day: find_granule(region_id, "GCOV", day) for day in dates}
    scenes = {}
    crop_inputs = {}
    for day, row in catalog.items():
        path = crop_dir / output_path(region_id, "GCOV", day).name
        if not path.is_file():
            path = OUTPUT_DIR / path.name
        if not path.is_file():
            if offline:
                raise ValueError(f"No cached GCOV crop for {day}")
            print(f"Fetching GCOV window for {day} over HTTPS", flush=True)
            try:
                path = fetch_crop(region_id, "GCOV", day)
            except Exception:
                raise ValueError(
                    f"GCOV window fetch failed for {day}. Check Earthdata login and connectivity."
                ) from None
        scenes[day] = read_scene(path, row["scene_name"], shape, target)
        crop_inputs[day] = path, row["scene_name"]

    # Pool each channel across all dates so the swipe and time slider use a consistent scale.
    limits = [percentile_limits(bands) for bands in zip(*scenes.values())]
    manifest = {
        "schemaVersion": "0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "generatedBy": "pipeline/build_manifest.py (AI-assisted code, see docs/AI_USAGE.md)",
        "region": {
            "id": region_id, "name": region["name"], "bbox": bbox,
            "center": [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2],
            "zoom": 10,
        },
        "dataMaturity": "PROVISIONAL",
        "layers": [],
        "vectors": [],
        "sources": [GCOV_SOURCE],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".gcov-", dir=output.parent) as directory:
        stage = Path(directory)
        for index, (layer_id, title, kind, polarization, units, description) in enumerate(LAYERS):
            composite = kind == "composite"
            low, high = (0, 1) if composite else limits[index]
            layer = {
                "id": layer_id, "title": title, "kind": kind, "product": "GCOV",
                "polarization": polarization, "units": units, "bounds": bbox,
                "colormap": {"name": "rgb" if composite else "gray", "min": low, "max": high},
                "description": description,
                "caveats": ["Provisional NISAR data. Interpret with caution."],
                "frames": [],
            }
            for day, bands in scenes.items():
                relative = Path("layers") / layer_id / f"{day}.webp"
                if composite:
                    rgb = [stretch(band, *scale) for band, scale in zip(bands, limits)]
                else:
                    rgb = [stretch(bands[index], low, high)] * 3
                write_webp(stage / relative, rgb, np.isfinite(bands[index]))
                row = catalog[day]
                layer["frames"].append({
                    "date": day, "image": relative.as_posix(), "granules": [row["scene_name"]],
                    "track": int(row["track"]), "frame": int(row["frame"]), "direction": row["direction"],
                })
            manifest["layers"].append(layer)

        content_path = ROOT / "content" / "landmarks" / f"{region_id}.json"
        landmarks = {"schemaVersion": "0.1", "regionId": region_id, "landmarks": []}
        if content_path.is_file():
            content = json.loads(content_path.read_text(encoding="utf-8"))
            entries = content if isinstance(content, list) else content["landmarks"]
            landmarks["landmarks"] = [{"series": {}, **entry} for entry in entries]
            if isinstance(content, dict):
                manifest["sources"] = merge_sources(manifest["sources"], content.get("sources", []))
        elif (output / "landmarks.json").is_file():
            landmarks = json.loads((output / "landmarks.json").read_text(encoding="utf-8"))
        if region_id == "mexico_city":
            months = monthly_dates(region_id)
            if set(months) - EXCLUDED <= crop_inputs.keys():
                landmarks["landmarks"] = enrich(
                    include_points(landmarks["landmarks"]), months, crop_inputs
                )
        write_json(stage / "landmarks.json", landmarks)
        write_json(stage / "manifest.json", manifest)

        files = [path for path in stage.rglob("*") if path.is_file()]
        paths = {path.relative_to(stage) for path in files}
        existing_size = sum(path.stat().st_size for path in output.rglob("*")
                            if path.is_file() and path.relative_to(output) not in paths)
        if existing_size + sum(path.stat().st_size for path in files) >= region_limit:
            raise ValueError(f"Region folder must stay under {region_limit // 1_000_000} MB")
        validator = Path(__file__).with_name("validate_manifest.py")
        if validator.is_file():
            result = subprocess.run([sys.executable, str(validator), str(stage)], check=False)
            if result.returncode:
                raise ValueError("Staged GCOV bundle failed manifest validation")
        # Put assets in place before publishing the manifest that refers to them.
        for relative in sorted(paths - {Path("manifest.json")}):
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            (stage / relative).replace(destination)
        (stage / "manifest.json").replace(output / "manifest.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    dates_group = parser.add_mutually_exclusive_group(required=True)
    dates_group.add_argument("--dates", nargs="+", type=date.fromisoformat,
                             metavar="DATE", help="Two or more distinct scene dates in YYYY-MM-DD")
    dates_group.add_argument("--monthly", action="store_true", help="Use configured GCOV dates")
    parser.add_argument("--region", default="mexico_city")
    parser.add_argument("--crop-dir", type=Path, default=OUTPUT_DIR,
                        help="Also look for cached T-03 crops in this folder")
    parser.add_argument("--output", type=Path, help="Defaults to app/public/data/<region>/")
    parser.add_argument("--offline", action="store_true", help="Require all crops to be cached")
    args = parser.parse_args()
    output = args.output or ROOT / "app" / "public" / "data" / args.region
    try:
        dates = monthly_dates(args.region) if args.monthly else [day.isoformat() for day in args.dates]
        build(args.region, dates, args.crop_dir, output, offline=args.offline)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"GCOV build failed: {error}\n")
    print(f"Wrote {output / 'manifest.json'}")


if __name__ == "__main__":
    main()
