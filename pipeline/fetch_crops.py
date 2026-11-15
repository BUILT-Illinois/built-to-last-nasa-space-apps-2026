"""Fetch a NISAR crop over HTTPS. Drafted with AI assistance."""

import argparse
import csv
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import sleep

import earthaccess
import h5py
import numpy as np
from aiohttp import ClientConnectionError, ClientPayloadError, ClientResponseError

from quicklook import GCOV_GRIDS, GUNW_UNW, region_bbox, window_for_bbox

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE.parent / "data" / "interim"
HTTP_TIMEOUT_SECONDS = 30
RETRY_DELAYS = (2, 4, 8)
DATASETS = {
    "GCOV": (GCOV_GRIDS.format(freq="B"), ("HHHH", "HVHV")),
    "GUNW": (GUNW_UNW, (
        "unwrappedPhase", "coherenceMagnitude", "connectedComponents", "ionospherePhaseScreen",
    )),
}


def find_granule(region, product, day):
    report = HERE / "reports" / f"granules_{region}.csv"
    if not report.is_file():
        raise ValueError(f"No catalog report for {region}: {report.name}")
    with report.open(newline="", encoding="utf-8") as catalog:
        for row in csv.DictReader(catalog):
            geometry = (row["track"], row["frame"], row["direction"])
            if (row["product_type"] == product and row["start_time"][:10] == day
                    and row["maturity"] == "PROVISIONAL" and row["crid"] == "P05023"
                    and geometry == ("19", "11", "ASCENDING")):
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


def fetch_crop(region, product, day):
    try:
        bbox = region_bbox(region)
    except KeyError:
        raise ValueError(f"Unknown region: {region}") from None
    path = OUTPUT_DIR / f"{region}_{product.lower()}_{day}.npz"
    if product == "GUNW" and path.is_file():
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
    args = parser.parse_args()
    try:
        fetch_crop(args.region, args.product, args.date.isoformat())
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
