"""Local frequency-A crop runner. Drafted with AI assistance (Codex)."""

import argparse
import sys
from pathlib import Path
from time import monotonic, strftime

import asf_search
from shapely.geometry import Point, box, shape

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import fetch_crops

DATES = ("2025-11-11", "2026-10-13")
POINTS = (
    (19.27, -98.97), (19.2922, -99.0494), (19.277, -99.0028),
    (19.30, -98.94), (19.26, -98.90), (19.44, -99.07),
)


def bounds(lat, lon):
    if (lat, lon) == POINTS[0]:
        return (-98.99, 19.25, -98.94, 19.29)
    return (lon - 0.0048, lat - 0.0045, lon + 0.0048, lat + 0.0045)


def check_coverage(granules):
    ids = [row["scene_name"] for row in granules.values()]
    results = asf_search.granule_search(ids)
    footprints = {item.properties["sceneName"]: shape(item.geometry) for item in results}
    if not all(name in footprints for name in ids):
        raise ValueError("ASF catalog did not return both requested scene footprints")
    windows = []
    for lat, lon in POINTS:
        bbox = bounds(lat, lon)
        statuses = []
        for day, row in granules.items():
            footprint = footprints[row["scene_name"]]
            inside = footprint.covers(Point(lon, lat))
            full_window = footprint.covers(box(*bbox))
            statuses.append(inside and full_window)
            print(f"{day} {lat:.4f},{lon:.4f} center={inside} window={full_window}", flush=True)
        if all(statuses):
            windows.append((lat, lon, bbox))
    return windows


def crop_path(day, lat, lon):
    key = f"{lat:.4f}_{lon:.4f}_{day}"
    return fetch_crops.OUTPUT_DIR / "landmark_frequencyA" / f"{key}.npz"


def fetch_one(day, lat, lon):
    row = fetch_crops.find_granule("mexico_city", "GCOV", day)
    if not fetch_crops.earthaccess.login(strategy="netrc").authenticated:
        raise ValueError("Earthdata login failed")
    session = fetch_crops.earthaccess.get_fsspec_https_session()
    dataset = fetch_crops.GCOV_GRIDS.format(freq="A")
    crop = fetch_crops.read_with_retries(session, row["url"], dataset, ("HHHH", "HVHV"),
                                        bounds(lat, lon))
    fetch_crops.publish_crop(crop_path(day, lat, lon), crop, row["scene_name"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    granules = {day: fetch_crops.find_granule("mexico_city", "GCOV", day) for day in DATES}
    windows = check_coverage(granules)
    if args.check_only or not windows:
        return int(len(windows) != len(POINTS))
    fetch_crops.clean_stale_temps(fetch_crops.OUTPUT_DIR)
    fetch_crops.clean_stale_temps(fetch_crops.OUTPUT_DIR / "landmark_frequencyA")
    failures = 0
    overall = monotonic()
    for day in granules:
        for lat, lon, _ in windows:
            key = f"{lat:.4f}_{lon:.4f}_{day}"
            path = crop_path(day, lat, lon)
            if path.is_file():
                print(f"{strftime('%H:%M:%S')} SKIP {key}", flush=True)
                continue
            print(f"{strftime('%H:%M:%S')} FETCH {key}", flush=True)
            command = [sys.executable, str(Path(__file__).resolve()), "--fetch-one",
                       day, str(lat), str(lon)]
            if not fetch_crops.run_fetch(command, fetch_crops.FETCH_DEADLINES["GCOV"], key):
                failures += 1
    print(f"Finished in {monotonic() - overall:.0f}s: {failures} failed", flush=True)
    return bool(failures)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 5 and sys.argv[1] == "--fetch-one":
            fetch_one(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
        else:
            sys.exit(main())
    except Exception as error:
        print(f"Batch setup failed ({type(error).__name__})", flush=True)
        sys.exit(1)
