"""Phase 1 data reality check: list NISAR granules over a study region.

AI-generation notice: this file was generated with AI assistance (Claude Code)
and reviewed by the team. See docs/AI_USAGE.md.

What it does
    Queries the ASF catalog (no login needed for search) for NISAR products
    that intersect a region's bounding box, then writes:
      * pipeline/reports/granules_<region>.csv   one row per granule
      * pipeline/reports/summary_<region>.md     counts, date ranges, sizes
    It never downloads data.

Usage
    python pipeline/search_granules.py                     # default region
    python pipeline/search_granules.py --region monterrey
    python pipeline/search_granules.py --all --count-only  # quick look at every region
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import asf_search as asf

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config" / "regions.json"
REPORT_DIR = HERE / "reports"

# Product types we care about. GCOV = backscatter by polarization,
# GUNW = unwrapped interferogram (ground movement), SME2 = soil moisture.
PRODUCT_TYPES = ["GCOV", "GUNW", "SME2", "GSLC", "RSLC"]

WIFI_MBPS = 60  # venue Wi-Fi, megabits per second
WIFI_EFFICIENCY = 0.6  # assume we really get about 60% of the nominal speed

CSV_FIELDS = [
    "product_type", "collection", "maturity", "scene_name", "start_time",
    "stop_time", "track", "frame", "direction", "pol_freq_a", "pol_freq_b",
    "range_bandwidth", "frame_coverage", "joint_observation", "crid",
    "size_gb", "processing_date", "url",
]


def load_config() -> dict:
    """Read the region config file."""
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_region(key: str | None) -> tuple[str, dict]:
    """Return (region_key, region_dict). Uses the default region when key is None."""
    config = load_config()
    key = key or config["default_region"]
    if key not in config["regions"]:
        options = ", ".join(config["regions"])
        raise SystemExit(f"Unknown region: {key}. Options: {options}")
    return key, config["regions"][key]


def bbox_to_wkt(bbox: list[float]) -> str:
    """Turn [west, south, east, north] into a WKT polygon string."""
    west, south, east, north = bbox
    return (
        f"POLYGON(({west} {south},{east} {south},{east} {north},"
        f"{west} {north},{west} {south}))"
    )


def maturity_of(collection: str) -> str:
    """Classify a collection short name as PROVISIONAL, BETA or OTHER."""
    name = (collection or "").upper()
    if "PROVISIONAL" in name:
        return "PROVISIONAL"
    if "BETA" in name:
        return "BETA"
    return "OTHER"


def size_gb(bytes_field: dict | None) -> float:
    """Size of the main data file in GB (the largest file listed for the granule)."""
    if not bytes_field:
        return 0.0
    sizes = [entry.get("bytes") or 0 for entry in bytes_field.values()]
    return round(max(sizes, default=0) / 1e9, 3)


def to_row(product) -> dict:
    """Flatten one asf_search product into a CSV row."""
    p = product.properties
    collection = p.get("collectionName") or ""
    return {
        "product_type": p.get("processingLevel"),
        "collection": collection,
        "maturity": maturity_of(collection),
        "scene_name": p.get("sceneName"),
        "start_time": p.get("startTime"),
        "stop_time": p.get("stopTime"),
        "track": p.get("pathNumber"),
        "frame": p.get("frameNumber"),
        "direction": p.get("flightDirection"),
        "pol_freq_a": "+".join(p.get("mainBandPolarization") or []),
        "pol_freq_b": "+".join(p.get("sideBandPolarization") or []),
        "range_bandwidth": "+".join(str(x) for x in (p.get("rangeBandwidth") or [])),
        "frame_coverage": p.get("frameCoverage"),
        "joint_observation": p.get("jointObservation"),
        "crid": p.get("crid"),
        "size_gb": size_gb(p.get("bytes")),
        "processing_date": p.get("processingDate"),
        "url": p.get("url"),
    }


def search_region(region: dict) -> list[dict]:
    """Search every product type for one region and return CSV rows."""
    wkt = bbox_to_wkt(region["bbox"])
    rows: list[dict] = []
    for product_type in PRODUCT_TYPES:
        results = asf.search(
            dataset=asf.DATASET.NISAR,
            processingLevel=product_type,
            intersectsWith=wkt,
        )
        rows.extend(to_row(product) for product in results)
    rows.sort(key=lambda r: (r["product_type"] or "", r["start_time"] or "", r["scene_name"] or ""))
    return rows


def download_minutes(gigabytes: float) -> float:
    """Rough download time in minutes at the venue Wi-Fi speed."""
    megabytes_per_second = WIFI_MBPS / 8 * WIFI_EFFICIENCY
    return round(gigabytes * 1000 / megabytes_per_second / 60, 1)


def summarize(rows: list[dict]) -> list[dict]:
    """Group rows by product type, collection, track, frame and direction."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (row["product_type"], row["collection"], row["track"], row["frame"], row["direction"])
        groups[key].append(row)
    summary = []
    for (ptype, collection, track, frame, direction), items in sorted(groups.items(), key=str):
        dates = sorted(r["start_time"][:10] for r in items if r["start_time"])
        total = round(sum(r["size_gb"] for r in items), 2)
        summary.append({
            "product_type": ptype,
            "collection": collection,
            "track": track,
            "frame": frame,
            "direction": direction,
            "count": len(items),
            "first": dates[0] if dates else "",
            "last": dates[-1] if dates else "",
            "pols": ", ".join(sorted({r["pol_freq_a"] for r in items if r["pol_freq_a"]})),
            "total_gb": total,
            "avg_gb": round(total / len(items), 2),
            "download_min": download_minutes(total),
        })
    return summary


def write_reports(key: str, region: dict, rows: list[dict]) -> None:
    """Write the CSV of granules and the Markdown summary."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / f"granules_{key}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# NISAR granules over {region['name']}",
        "",
        "Generated by `pipeline/search_granules.py` (AI-assisted code, see docs/AI_USAGE.md).",
        "",
        f"- Query time: {now}",
        f"- Bounding box [W, S, E, N]: {region['bbox']}",
        "- Query: `asf_search.search(dataset='NISAR', processingLevel=<type>, intersectsWith=<bbox WKT>)`",
        f"- Product types searched: {', '.join(PRODUCT_TYPES)}",
        f"- Total granules: {len(rows)}",
        f"- Download time assumes {WIFI_MBPS} Mbps at {int(WIFI_EFFICIENCY * 100)}% efficiency.",
        "",
        "| Product | Collection | Track | Frame | Dir | Count | First | Last | Pols (freq A) | Total GB | Avg GB | Download min |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for s in summarize(rows):
        lines.append(
            f"| {s['product_type']} | {s['collection']} | {s['track']} | {s['frame']} | "
            f"{s['direction']} | {s['count']} | {s['first']} | {s['last']} | {s['pols']} | "
            f"{s['total_gb']} | {s['avg_gb']} | {s['download_min']} |"
        )
    (REPORT_DIR / f"summary_{key}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {csv_path.name} and summary_{key}.md ({len(rows)} granules)")


def count_only(key: str, region: dict) -> None:
    """Print granule counts per product type without writing files."""
    wkt = bbox_to_wkt(region["bbox"])
    counts = {
        ptype: asf.search_count(dataset=asf.DATASET.NISAR, processingLevel=ptype, intersectsWith=wkt)
        for ptype in ("GCOV", "GUNW", "SME2")
    }
    print(f"{key:22s} " + "  ".join(f"{ptype}={n}" for ptype, n in counts.items()))


def main() -> None:
    parser = argparse.ArgumentParser(description="List NISAR granules over a study region.")
    parser.add_argument("--region", help="region key from config/regions.json")
    parser.add_argument("--all", action="store_true", help="run for every region in the config")
    parser.add_argument("--count-only", action="store_true", help="print counts, write nothing")
    args = parser.parse_args()

    keys = list(load_config()["regions"]) if args.all else [load_region(args.region)[0]]
    for key in keys:
        _, region = load_region(key)
        if args.count_only:
            count_only(key, region)
        else:
            write_reports(key, region, search_region(region))


if __name__ == "__main__":
    main()
