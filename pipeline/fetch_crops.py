"""Fetch a NISAR crop over HTTPS. Drafted with AI assistance."""

import argparse
import csv
import json
import subprocess
import sys
from datetime import date
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import monotonic, sleep, time

import earthaccess
import h5py
import numpy as np
from aiohttp import ClientConnectionError, ClientPayloadError, ClientResponseError

from quicklook import CONFIG_PATH, GCOV_GRIDS, GUNW_UNW, region_bbox, window_for_bbox

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE.parent / "data" / "interim"
HTTP_TIMEOUT_SECONDS = 30
RETRY_DELAYS = (2, 4, 8)
FETCH_DEADLINES = {"GCOV": 180, "GUNW": 300}
MEXICO_CITY_BBOX = [-99.40, 19.10, -98.85, 19.65]
MEXICO_CITY_GCOV = {
    "track": 19, "frame": 11, "direction": "ASCENDING", "release": "P05023",
    # D-17 excludes 2025-12-05 and 2026-04-16 from published GCOV frames.
    "dates": (
        "2025-11-11", "2025-12-17", "2026-01-10", "2026-02-15",
        "2026-03-11", "2026-05-10", "2026-06-15",
        "2026-07-09", "2026-08-14", "2026-09-19", "2026-10-13",
    ),
}
DATASETS = {
    "GCOV": (GCOV_GRIDS.format(freq="B"), ("HHHH", "HVHV")),
    "GUNW": (GUNW_UNW, (
        "unwrappedPhase", "coherenceMagnitude", "connectedComponents", "ionospherePhaseScreen",
    )),
}


def gcov_config(region):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    try:
        regions = config["regions"]
        catalog_region = regions[region].get("gcov_reference_region", region)
        entry = regions[catalog_region]
        settings = entry.get("gcov", MEXICO_CITY_GCOV) if catalog_region == "mexico_city" else entry["gcov"]
        return {**settings, "catalog_region": catalog_region}
    except KeyError:
        raise ValueError(f"Add a gcov configuration for region {region}") from None


def monthly_dates(region):
    try:
        dates = [date.fromisoformat(day).isoformat() for day in gcov_config(region)["dates"]]
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"Configure monthly GCOV dates in YYYY-MM-DD for {region}") from None
    if len(dates) < 2 or len(set(dates)) != len(dates):
        raise ValueError(f"Configure at least two distinct GCOV dates for {region}")
    return sorted(dates)


def selection(settings):
    try:
        return tuple(str(settings[key]) for key in ("track", "frame", "direction", "release"))
    except KeyError as error:
        raise ValueError(f"Missing GCOV selection field {error.args[0]} for {region}") from None


def find_granule(region, product, day):
    settings = gcov_config(region) if product == "GCOV" else MEXICO_CITY_GCOV
    catalog_region = settings.get("catalog_region", region)
    if catalog_region != region and day not in settings["dates"]:
        raise ValueError(f"No approved {product} granule for {region} on {day}")
    track, frame, direction, release = selection(settings)
    report = HERE / "reports" / f"granules_{catalog_region}.csv"
    if not report.is_file():
        raise ValueError(f"No catalog report for {region}: {report.name}")
    with report.open(newline="", encoding="utf-8") as catalog:
        for row in csv.DictReader(catalog):
            geometry = (row["track"], row["frame"], row["direction"])
            if (row["product_type"] == product and row["start_time"][:10] == day
                    and row["maturity"] == "PROVISIONAL" and row["crid"] == release
                    and geometry == (track, frame, direction)):
                return row
    raise ValueError(f"No approved {product} granule for {region} on {day}")


def read_crop(session, url, group_path, names, bbox):
    # fsspec uses seconds for the metadata deadline and forwards the same
    # numeric timeout to aiohttp for each HTTP range request.
    with session.open(url, "rb", block_size=256 * 1024, cache_type="readahead",
                      timeout=HTTP_TIMEOUT_SECONDS) as remote:
        with h5py.File(remote, "r") as source:
            group = source[group_path]
            rows, cols = window_for_bbox(group, bbox)
            crop = {name: group[name][rows, cols] for name in names}
            crop["xCoordinates"] = group["xCoordinates"][cols]
            crop["yCoordinates"] = group["yCoordinates"][rows]
            crop["projection"] = group["projection"][()]
    return crop


def read_with_retries(session, url, group_path, names, bbox):
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            return read_crop(session, url, group_path, names, bbox)
        except (OSError, ClientConnectionError, ClientPayloadError, ClientResponseError) as error:
            if isinstance(error, ClientResponseError) and not (
                error.status in (408, 429) or 500 <= error.status < 600
            ):
                raise ValueError(f"Remote crop read failed (HTTP {error.status})") from None
            if attempt == len(RETRY_DELAYS):
                raise ValueError("Remote crop read failed after 4 attempts") from None
            delay = RETRY_DELAYS[attempt]
            print(f"Remote crop read failed ({type(error).__name__}); retrying in {delay}s",
                  flush=True)
            sleep(delay)


def publish_crop(path, crop, granule):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Publish only complete archives so a failed write can be retried.
    with NamedTemporaryFile(dir=path.parent, suffix=".npz", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        np.savez_compressed(temporary_path, **crop, granule=granule)
        temporary_path.replace(path)
    finally:
        temporary_path.unlink(missing_ok=True)


def clean_stale_temps(directory):
    # A worker is bounded to five minutes. Leave recent saves alone in case
    # another batch is still publishing a crop.
    cutoff = time() - 2 * max(FETCH_DEADLINES.values())
    for path in directory.glob("tmp*.npz"):
        try:
            if path.is_file() and path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)
        except FileNotFoundError:
            continue


def run_fetch(command, timeout, label):
    """Supervise a worker, including reads that never return an HTTP error."""
    for attempt in range(1, 4):
        started = monotonic()
        try:
            subprocess.run(command, check=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            result = "HANG"
        except subprocess.CalledProcessError:
            result = "FAIL"
        else:
            result = "OK"
        print(f"{label} {result} {monotonic() - started:.1f}s (attempt {attempt}/3)", flush=True)
        if result == "OK":
            return True
        if attempt < 3:
            sleep(20 * attempt)
    return False


def output_path(region, product, day):
    tag = ""
    if product == "GCOV":
        bbox = region_bbox(region)
        scene = selection(gcov_config(region))
        if (region, bbox, scene) != ("mexico_city", MEXICO_CITY_BBOX, ("19", "11", "ASCENDING", "P05023")):
            # A changed window or selection must not reuse an old crop.
            tag = "_" + sha256(json.dumps([bbox, scene]).encode()).hexdigest()[:16]
    return OUTPUT_DIR / f"{region}_{product.lower()}_{day}{tag}.npz"


def fetch_bounded(region, product, day):
    path = output_path(region, product, day)
    if path.is_file():
        print(f"skip {path}", flush=True)
        return True
    find_granule(region, product, day)
    command = [sys.executable, str(Path(__file__).resolve()), "--worker",
               "--region", region, "--product", product, "--date", day]
    return run_fetch(command, FETCH_DEADLINES[product], f"{product} {day}")


def fetch_crop(region, product, day):
    try:
        bbox = region_bbox(region)
    except KeyError:
        raise ValueError(f"Unknown region: {region}") from None
    path = output_path(region, product, day)
    if path.is_file():
        print(f"skip {path}")
        return path

    granule = find_granule(region, product, day)
    if not earthaccess.login(strategy="netrc").authenticated:
        raise ValueError("Earthdata login failed. Check your user netrc file.")
    session = earthaccess.get_fsspec_https_session()
    group_path, names = DATASETS[product]
    crop = read_with_retries(session, granule["url"], group_path, names, bbox)
    publish_crop(path, crop, granule["scene_name"])
    print(f"Wrote {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", required=True)
    parser.add_argument("--product", required=True, choices=DATASETS)
    parser.add_argument("--date", required=True, type=date.fromisoformat,
                        help="Granule start date (YYYY-MM-DD)")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        day = args.date.isoformat()
        if args.worker:
            fetch_crop(args.region, args.product, day)
            return 0
        clean_stale_temps(OUTPUT_DIR)
        return int(not fetch_bounded(args.region, args.product, day))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.exit(main())
