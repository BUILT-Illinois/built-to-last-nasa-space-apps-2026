"""Quick look at a local NISAR file: crop to a region and save PNG pictures.

AI-generation notice: this file was generated with AI assistance (Claude Code)
and reviewed by the team. See docs/AI_USAGE.md.

Purpose
    Exploration only. It lets us see what the radar data looks like over our
    study area before we decide what story to tell. The pictures are not the
    final map layers (no reprojection to web map coordinates, rough colors).

What it reads (dataset names confirmed on real files, Nov 14, 2026)
    GCOV: /science/LSAR/GCOV/grids/frequency{A|B}/HHHH and HVHV
          frequencyA = 10 m pixels, frequencyB = 80 m pixels, UTM coordinates
    GUNW: /science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH/
          unwrappedPhase, coherenceMagnitude, connectedComponents (80 m pixels)

Usage
    python pipeline/quicklook.py gcov  <file.h5> --out data/quicklooks
    python pipeline/quicklook.py gcov  <file.h5> --frequency A --bbox -99.12 19.38 -98.95 19.52
    python pipeline/quicklook.py gunw  <file.h5> --out data/quicklooks
    python pipeline/quicklook.py change <earlier_gcov.h5> <later_gcov.h5>

Needs: h5py, numpy, pyproj, pillow.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import h5py
import numpy as np
from PIL import Image
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config" / "regions.json"
SPEED_OF_LIGHT = 299_792_458.0  # meters per second

GCOV_GRIDS = "/science/LSAR/GCOV/grids/frequency{freq}"
GUNW_UNW = "/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH"
GUNW_FREQ = "/science/LSAR/GUNW/grids/frequencyA"


def region_bbox(region_key: str | None) -> list[float]:
    """Return [west, south, east, north] for a region in config/regions.json."""
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    key = region_key or config["default_region"]
    return config["regions"][key]["bbox"]


def window_for_bbox(group: h5py.Group, bbox: list[float]) -> tuple[slice, slice]:
    """Find the row and column range of a grid that covers a lon/lat box.

    The grid is in a UTM projection (its EPSG code is stored in `projection`).
    yCoordinates run north to south, xCoordinates west to east.
    """
    epsg = int(group["projection"][()])
    to_grid = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    west, south, east, north = bbox
    xs, ys = to_grid.transform([west, east, west, east], [south, south, north, north])
    x = group["xCoordinates"][:]
    y = group["yCoordinates"][:]
    cols = np.where((x >= min(xs)) & (x <= max(xs)))[0]
    rows = np.where((y >= min(ys)) & (y <= max(ys)))[0]
    if cols.size == 0 or rows.size == 0:
        raise SystemExit("The file does not cover this bounding box.")
    return slice(rows[0], rows[-1] + 1), slice(cols[0], cols[-1] + 1)


def to_db(power: np.ndarray) -> np.ndarray:
    """Convert linear backscatter to decibels. Empty or invalid pixels become NaN."""
    out = np.full(power.shape, np.nan, dtype=np.float32)
    good = np.isfinite(power) & (power > 0)
    out[good] = 10.0 * np.log10(power[good])
    return out


def stretch(values: np.ndarray, low: float, high: float) -> np.ndarray:
    """Scale values to 0..255 between low and high. NaN becomes 0."""
    scaled = (values - low) / (high - low)
    scaled = np.clip(np.nan_to_num(scaled, nan=0.0), 0.0, 1.0)
    return (scaled * 255).astype(np.uint8)


def percentile_range(values: np.ndarray, low: float = 2, high: float = 98) -> tuple[float, float]:
    """Return the low and high percentiles of the valid values."""
    valid = values[np.isfinite(values)]
    return float(np.percentile(valid, low)), float(np.percentile(valid, high))


def diverging_rgb(values: np.ndarray, limit: float) -> np.ndarray:
    """Color values blue (negative) to white (zero) to red (positive). NaN is gray."""
    t = np.clip(np.nan_to_num(values, nan=0.0) / limit, -1.0, 1.0)
    red = np.where(t < 0, 1.0 + t, 1.0)
    green = 1.0 - np.abs(t)
    blue = np.where(t > 0, 1.0 - t, 1.0)
    rgb = np.stack([red, green, blue], axis=-1)
    rgb[~np.isfinite(values)] = 0.5
    return (rgb * 255).astype(np.uint8)


def save(array: np.ndarray, path: Path) -> None:
    """Save a uint8 array (gray or RGB) as a PNG."""
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array).save(path)
    print(f"  wrote {path}  {array.shape[1]}x{array.shape[0]} px")


def describe(name: str, values: np.ndarray, unit: str) -> None:
    """Print simple statistics of the valid values."""
    valid = values[np.isfinite(values)]
    share = 100.0 * valid.size / values.size
    p2, p50, p98 = np.percentile(valid, [2, 50, 98])
    print(f"  {name}: valid {share:.1f}%  p2 {p2:.2f}  median {p50:.2f}  p98 {p98:.2f} {unit}")


def read_gcov(path: str, frequency: str, bbox: list[float]) -> dict:
    """Read HH and HV backscatter in dB for a box, plus identifying metadata."""
    with h5py.File(path, "r") as h5:
        group = h5[GCOV_GRIDS.format(freq=frequency)]
        rows, cols = window_for_bbox(group, bbox)
        ident = h5["/science/LSAR/identification"]
        return {
            "hh": to_db(group["HHHH"][rows, cols]),
            "hv": to_db(group["HVHV"][rows, cols]),
            "spacing_m": float(group["xCoordinateSpacing"][()]),
            "date": ident["zeroDopplerStartTime"][()].decode()[:10],
            "crid": ident["compositeReleaseId"][()].decode(),
        }


def cmd_gcov(args: argparse.Namespace) -> None:
    """Write HH, HV and color-composite pictures for one GCOV file."""
    bbox = args.bbox or region_bbox(args.region)
    data = read_gcov(args.file, args.frequency, bbox)
    tag = f"gcov_{data['date']}_{data['crid']}_freq{args.frequency}{args.suffix}"
    print(f"GCOV {data['date']}  release {data['crid']}  {data['spacing_m']:.0f} m pixels")
    describe("HH", data["hh"], "dB")
    describe("HV", data["hv"], "dB")
    hh_lo, hh_hi = percentile_range(data["hh"])
    hv_lo, hv_hi = percentile_range(data["hv"])
    ratio = data["hh"] - data["hv"]
    r_lo, r_hi = percentile_range(ratio)
    out = Path(args.out)
    save(stretch(data["hh"], hh_lo, hh_hi), out / f"{tag}_HH.png")
    save(stretch(data["hv"], hv_lo, hv_hi), out / f"{tag}_HV.png")
    composite = np.stack(
        [stretch(data["hh"], hh_lo, hh_hi), stretch(data["hv"], hv_lo, hv_hi), stretch(ratio, r_lo, r_hi)],
        axis=-1,
    )
    save(composite, out / f"{tag}_composite_R-HH_G-HV_B-ratio.png")


def cmd_change(args: argparse.Namespace) -> None:
    """Write pictures of the dB difference between two GCOV dates (later minus earlier)."""
    bbox = args.bbox or region_bbox(args.region)
    early = read_gcov(args.earlier, args.frequency, bbox)
    late = read_gcov(args.later, args.frequency, bbox)
    if early["hh"].shape != late["hh"].shape:
        raise SystemExit("The two files are on different grids. Use files from the same track and frame.")
    print(f"Change {early['date']} ({early['crid']}) to {late['date']} ({late['crid']})")
    if early["crid"] != late["crid"]:
        print("  WARNING: different processing releases. Differences can come from processing, not the ground.")
    out = Path(args.out)
    for pol in ("hh", "hv"):
        diff = late[pol] - early[pol]
        describe(f"{pol.upper()} change", diff, "dB")
        name = f"change_{early['date']}_to_{late['date']}_{pol.upper()}_freq{args.frequency}{args.suffix}.png"
        save(diverging_rgb(diff, limit=6.0), out / name)
    print("  colors: red = brighter in the later date, blue = darker, full color at 6 dB")


def cmd_gunw(args: argparse.Namespace) -> None:
    """Write coherence and line-of-sight change pictures for one GUNW pair."""
    bbox = args.bbox or region_bbox(args.region)
    with h5py.File(args.file, "r") as h5:
        group = h5[GUNW_UNW]
        rows, cols = window_for_bbox(group, bbox)
        phase = group["unwrappedPhase"][rows, cols].astype(np.float32)
        coherence = group["coherenceMagnitude"][rows, cols]
        components = group["connectedComponents"][rows, cols]
        frequency_hz = float(h5[GUNW_FREQ]["centerFrequency"][()])
        ident = h5["/science/LSAR/identification"]
        ref = ident["referenceZeroDopplerStartTime"][()].decode()[:10]
        sec = ident["secondaryZeroDopplerStartTime"][()].decode()[:10]
        crid = ident["compositeReleaseId"][()].decode()
        direction = ident["orbitPassDirection"][()].decode()

    wavelength_cm = SPEED_OF_LIGHT / frequency_hz * 100.0
    good = np.isfinite(phase) & (coherence >= args.min_coherence) & (components > 0)
    phase[~good] = np.nan
    # Quick-look reference: subtract the median of the whole box. The real
    # pipeline must use a named stable reference area instead.
    phase -= np.nanmedian(phase)
    # Range change along the line of sight. The SIGN CONVENTION IS NOT YET
    # CONFIRMED against the product specification. Do not label a color
    # "sinking" until it is.
    los_cm = phase * wavelength_cm / (4.0 * math.pi)

    print(f"GUNW {ref} to {sec}  {direction}  release {crid}  wavelength {wavelength_cm:.2f} cm")
    describe("coherence", np.where(np.isfinite(coherence), coherence, np.nan), "")
    describe("line-of-sight change", los_cm, "cm (sign unconfirmed)")
    out = Path(args.out)
    tag = f"gunw_{ref}_to_{sec}_{crid}{args.suffix}"
    save(stretch(coherence, 0.0, 1.0), out / f"{tag}_coherence.png")
    save(diverging_rgb(los_cm, limit=args.limit_cm), out / f"{tag}_los_cm.png")
    print(f"  colors: full color at +/- {args.limit_cm} cm, gray = masked (low coherence)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Quick-look pictures from local NISAR files.")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--region", help="region key from config/regions.json")
        p.add_argument("--bbox", nargs=4, type=float, metavar=("W", "S", "E", "N"),
                       help="override the region with a custom box")
        p.add_argument("--out", default="data/quicklooks", help="output folder (git-ignored)")
        p.add_argument("--suffix", default="", help="text added to output file names")

    gcov = sub.add_parser("gcov", help="HH, HV and composite for one GCOV file")
    gcov.add_argument("file")
    gcov.add_argument("--frequency", choices=["A", "B"], default="B")
    common(gcov)
    gcov.set_defaults(run=cmd_gcov)

    change = sub.add_parser("change", help="dB difference between two GCOV files")
    change.add_argument("earlier")
    change.add_argument("later")
    change.add_argument("--frequency", choices=["A", "B"], default="B")
    common(change)
    change.set_defaults(run=cmd_change)

    gunw = sub.add_parser("gunw", help="coherence and line-of-sight change for one GUNW pair")
    gunw.add_argument("file")
    gunw.add_argument("--min-coherence", type=float, default=0.3)
    gunw.add_argument("--limit-cm", type=float, default=3.0)
    common(gunw)
    gunw.set_defaults(run=cmd_gunw)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
