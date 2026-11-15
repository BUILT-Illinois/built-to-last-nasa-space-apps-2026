"""Add a Mexico City line-of-sight rate overlay. Drafted with AI assistance (Codex)."""

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from io import BytesIO
from math import ceil
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import rasterio
from PIL import Image
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject, transform_bounds

from validate_manifest import check_date, validate_folder

ROOT = Path(__file__).resolve().parents[1]
REGION = "mexico_city"
CONFIG = ROOT / "pipeline" / "config" / "regions.json"
LIVE_DATA = ROOT / "app" / "public" / "data"
WEB_CRS = "EPSG:3857"
PIXEL_METERS = 80
MAX_ABS_LOS_RATE_CM_PER_YEAR = 50
SCALE = {"name": "los-blue-white-red", "min": -30, "max": 30}
LOS_LABEL = "Radar line-of-sight rate"
SOURCE = {
    "id": "nisar-gunw",
    "title": "NISAR L2 GUNW PROVISIONAL V1 (NASA/ISRO, ASF DAAC)",
    "url": "https://nisar-docs.asf.alaska.edu/earthdata-search/",
    "license": "NASA Earthdata open data (see Earthdata Data Use Guidance)",
}


def render(path, bbox, units, sign):
    west, south, east, north = transform_bounds("EPSG:4326", WEB_CRS, *bbox)
    width = ceil((east - west) / PIXEL_METERS)
    height = ceil((north - south) / PIXEL_METERS)
    target = from_bounds(west, south, east, north, width, height)
    with rasterio.open(path) as source:
        if source.driver != "GTiff" or source.count != 1 or source.crs is None:
            raise ValueError("Input must be a single-band GeoTIFF with a CRS")
        if np.dtype(source.dtypes[0]).kind not in "iuf":
            raise ValueError("Input band must contain real numeric rates")
        band = source.read(1, masked=True, out_dtype="float64").filled(np.nan)
        band = band * source.scales[0] + source.offsets[0]
        if units == "mm/yr":
            band /= 10
        if sign == "negative-away":
            band *= -1
        band[~np.isfinite(band) | (np.abs(band) > MAX_ABS_LOS_RATE_CM_PER_YEAR)] = np.nan
        rates = np.full((height, width), np.nan)
        reproject(
            band, rates, src_transform=source.transform, src_crs=source.crs, src_nodata=np.nan,
            dst_transform=target, dst_crs=WEB_CRS, dst_nodata=np.nan, resampling=Resampling.nearest,
        )
    valid = np.isfinite(rates)
    if not valid.any():
        raise ValueError("No valid rate pixels inside the Mexico City bounds")

    # Palette index 0 is transparent; 1–255 are linearly spaced from min to max.
    indexes = np.zeros(rates.shape, dtype=np.uint8)
    low, high = SCALE["min"], SCALE["max"]
    indexes[valid] = 1 + np.rint((np.clip(rates[valid], low, high) - low) * 254 / (high - low)).astype(np.uint8)
    anchors = ((33, 102, 172), (255, 255, 255), (178, 24, 43))
    palette = np.column_stack([np.interp(np.arange(255), [0, 127, 254], channel) for channel in zip(*anchors)])
    image = Image.fromarray(indexes)
    image.putpalette([0, 0, 0, *np.rint(palette).astype(np.uint8).ravel().tolist()])
    png = BytesIO()
    image.save(png, format="PNG", transparency=0, optimize=True)
    return png.getvalue()


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def ingest(args):
    reference = args.reference.strip()
    if not reference:
        raise ValueError("--reference must name the reference area")
    if args.synthetic:
        if args.granules:
            raise ValueError("Synthetic data must have an empty granule list")
        if args.output is None:
            raise ValueError("--synthetic requires a separate --output folder")
    elif not args.granules or any(not item.strip() for item in args.granules):
        raise ValueError("--granules requires the exact GUNW granule IDs")
    problems = check_date(args.since, "--since") + check_date(args.date, "--date")
    if problems or args.since >= args.date:
        raise ValueError("; ".join(problems) or "--since must be earlier than --date")

    output = (args.output or LIVE_DATA / REGION).resolve()
    if args.synthetic:
        parts = tuple(part.casefold() for part in output.parts)
        if any(parts[i:i + 3] == ("app", "public", "data") for i in range(len(parts))):
            raise ValueError("Synthetic output cannot go under app/public/data")
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise ValueError("Synthetic output requires a new or empty folder")

    region = json.loads(CONFIG.read_text(encoding="utf-8"))["regions"][REGION]
    bbox = region["bbox"]
    if args.synthetic:
        manifest = {
            "schemaVersion": "0.1", "dataMaturity": "SYNTHETIC", "synthetic": True,
            "region": {
                "id": REGION, "name": region["name"], "bbox": bbox, "zoom": 10,
                "center": [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2],
            },
            "layers": [], "vectors": [], "sources": [],
        }
    else:
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        if (manifest["region"]["id"] != REGION or manifest["region"]["bbox"] != bbox
                or manifest["dataMaturity"] != "PROVISIONAL" or manifest.get("synthetic")):
            raise ValueError("Real ingest needs an existing PROVISIONAL mexico_city bundle with the configured bbox")
        if not any(source["id"] == SOURCE["id"] for source in manifest["sources"]):
            manifest["sources"].append(SOURCE)

    png = render(args.tiff, bbox, args.units, args.sign)
    digest = hashlib.sha256(png).hexdigest()[:16]
    relative = Path("layers") / "sinking" / f"{args.date}-{digest}.png"
    layer = {
        "id": "sinking", "title": "Ground motion along the radar line of sight",
        "kind": "displacement", "product": "GUNW", "polarization": "HH", "units": "cm/yr",
        "bounds": bbox, "colormap": SCALE, "losLabel": LOS_LABEL,
        "referenceArea": reference, "awaySign": "positive",
        "description": ("Generated test pattern. " if args.synthetic else "") +
                       "Annual rate of motion along the radar line of sight, relative to the reference area.",
        "caveats": ["Positive means away from the satellite.", "No conversion to vertical motion.",
                    "Synthetic test data." if args.synthetic else "Provisional NISAR data.",
                    f"Pixels with absolute rates above {MAX_ABS_LOS_RATE_CM_PER_YEAR} cm/yr "
                    "are masked as likely phase-unwrapping artifacts."],
        "frames": [{
            "date": args.date, "since": args.since, "image": relative.as_posix(),
            "granules": args.granules,
            # T-33 uses the single approved Mexico City GUNW geometry (D-01).
            "track": 19, "frame": 11, "direction": "ASCENDING",
        }],
    }
    manifest["layers"] = [entry for entry in manifest["layers"] if entry["id"] != "sinking"] + [layer]
    manifest["generatedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    manifest["generatedBy"] = "pipeline/ingest_sinking.py (AI-assisted code, see docs/AI_USAGE.md)"

    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".sinking-", dir=output.parent) as directory:
        stage = Path(directory)
        if args.synthetic:
            write_json(stage / "landmarks.json", {"schemaVersion": "0.1", "regionId": REGION, "landmarks": []})
        else:
            shutil.copytree(output, stage, dirs_exist_ok=True)
        (stage / relative).parent.mkdir(parents=True, exist_ok=True)
        (stage / relative).write_bytes(png)
        write_json(stage / "manifest.json", manifest)
        problems = validate_folder(stage)
        if problems:
            raise ValueError("Staged bundle failed validation:\n  " + "\n  ".join(problems))
        destination = output / relative
        if not destination.resolve().is_relative_to(output):
            raise ValueError("Overlay path points outside the region folder")
        destination.parent.mkdir(parents=True, exist_ok=True)
        (stage / relative).replace(destination)
        if args.synthetic:
            (stage / "landmarks.json").replace(output / "landmarks.json")
        (stage / "manifest.json").replace(output / "manifest.json")
    return output / "manifest.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tiff", type=Path)
    parser.add_argument("--units", required=True, choices=("mm/yr", "cm/yr"))
    parser.add_argument("--sign", required=True, choices=("negative-away", "positive-away"))
    parser.add_argument("--reference", required=True)
    parser.add_argument("--granules", nargs="+", default=[], metavar="ID")
    parser.add_argument("--since", required=True, help="First acquisition date (YYYY-MM-DD)")
    parser.add_argument("--date", required=True, help="Last acquisition date (YYYY-MM-DD)")
    parser.add_argument("--output", type=Path, help="Region bundle (default: app/public/data/mexico_city)")
    parser.add_argument("--synthetic", action="store_true", help="Write only to a new or empty test folder")
    try:
        manifest = ingest(parser.parse_args())
    except (ValueError, OSError, KeyError, rasterio.errors.RasterioError) as error:
        parser.exit(1, f"Sinking ingest failed: {error}\n")
    print(f"Wrote {manifest}")


if __name__ == "__main__":
    main()
