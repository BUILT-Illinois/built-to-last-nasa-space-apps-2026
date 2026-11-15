"""Proof of concept: 336 days of Mexico City ground motion from NISAR.

AI-generation notice: this file was generated with AI assistance (Claude Code)
for Eduardo's T-31 (pipeline/science/displacement.py will be the cleaned-up
version). See docs/AI_USAGE.md.

Input: the 27 consecutive 12-day GUNW pairs of track 19 / frame 11 (ascending,
PROVISIONAL P05023), Nov 11, 2025 to Oct 13, 2026, already cropped to the
Mexico City box in <data>/mexico_city_gunw_<reference date>.npz, where <data>
is data/Mexico_City/ by default. Any pair touching Oct 30, 2025 is skipped
(D-13). Optional: the GCOV crops in the same folder, used only as a gray
background (Oct 30, Dec 5 and Apr 16 left out, D-13 and D-17).

Method (each step fixes a known way the simple sum goes wrong):
  1. Subtract each pair's ionosphere phase screen.
  2. Keep the connected component that holds the reference area. Other large
     components are re-attached by the whole number of 2-pi cycles that best
     matches the neighbouring pairs; pixels in component 0 are dropped.
  3. Subtract the median of a fixed reference area (western hills) from every
     pair, so all pairs share one zero.
  4. Fill a pixel's missing pairs (at most MAX_FILLED) from its own average
     rate, drop pixels missing more, then add the pairs in order.
     Atmospheric noise of each date enters once with + and once with -, so it
     mostly cancels; the sum behaves like one 336-day measurement.
  5. Convert phase to centimeters along the radar line of sight.
No tilt is removed from single pairs: the sinking bowls cover much of the box,
and a fitted tilt would absorb part of the signal.

Usage (from the repo root):
  python poc/mexico_city_sinking/sinking_poc.py [--data path/to/Mexico_City]
Writes to poc/mexico_city_sinking/ (git-tracked): the figure, the landmark CSV
and provenance.json. Writes next to the crops (git-ignored): the full stack
displacement_cumulative.npz, and the GeoTIFFs los_total_cm.tif (year total) and
los_rate_cm_per_year.tif (per-pixel rate), both in the crops' UTM grid.
"""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import os
import time
import warnings
from datetime import date
from pathlib import Path

import numpy as np
from pyproj import Transformer

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DEFAULT_DATA = REPO / "data" / "Mexico_City"

# Acquisitions left out (D-13: measurement errors on Oct 30, 2025). A GUNW pair is
# skipped if either of its dates is listed.
EXCLUDED_DATES = {"2025-10-30"}
# GCOV dates also left out of the gray background (D-17: scene-wide darkening).
BACKGROUND_EXCLUDED_DATES = EXCLUDED_DATES | {"2025-12-05", "2026-04-16"}

# Radar wavelength. The track 19 crops do not carry the center frequency; this is
# the value stored in a GUNW of the same 40 MHz mode (track 113, read Nov 14).
CENTER_FREQUENCY_HZ = 1.239e9
WAVELENGTH_CM = 299_792_458.0 / CENTER_FREQUENCY_HZ * 100

# Reference area, assumed stable: western hills near Santa Fe (west, south, east, north).
REFERENCE_BOX = (-99.27, 19.33, -99.22, 19.38)
MIN_COMPONENT_PIXELS = 500
MAX_FILLED = 4   # a pixel may miss at most this many of the 27 pairs (filled from its own rate)

SIGN = ("positive = range increase = moving away from the satellite (sinking shows as positive). "
        "INFERRED from where the known sinking zones are, NOT confirmed against the GUNW "
        "specification (JPL D-102272); T-35 confirms it.")

# Label offsets in points, so names near each other do not overlap.
LABEL_OFFSET = {"Airport area (AICM)": (6, 6), "Centro Historico": (-70, 8), "Angel de la Independencia": (-60, -12)}

# Approximate locations (lon, lat), for sampling and labels. Check on a map before
# any of these names go into the app.
LANDMARKS = {
    "Airport area (AICM)": (-99.072, 19.436),
    "Nezahualcoyotl": (-99.015, 19.400),
    "Centro Historico": (-99.133, 19.433),
    "Angel de la Independencia": (-99.168, 19.427),
    "Iztapalapa": (-99.057, 19.358),
    "Tlahuac": (-99.004, 19.286),
    "Chalco": (-98.897, 19.263),
    "Sierra de Guadalupe (control, hills)": (-99.120, 19.570),
}
# JPL's published NISAR window was Oct 25, 2025 to Jan 17, 2026. Our closest: Nov 11 to Jan 22.
JPL_COMPARE_END = "2026-01-22"


def pair_dates(granule: str) -> tuple[str, str]:
    """Reference and secondary dates (YYYY-MM-DD) from a GUNW granule name."""
    parts = granule.split("_")
    fmt = lambda s: f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return fmt(parts[11][:8]), fmt(parts[13][:8])


def is_excluded(granule: str) -> bool:
    """True if either date of the pair is an excluded acquisition (D-13)."""
    return bool(set(pair_dates(granule)) & EXCLUDED_DATES)


def load_pairs(data: Path) -> tuple[list[dict], np.ndarray, np.ndarray, int]:
    """Load the GUNW crops in time order, skip excluded dates, check they form one unbroken chain."""
    files = sorted(glob.glob(str(data / "mexico_city_gunw_*.npz")))
    if not files:
        raise SystemExit(f"No GUNW crops in {data}")
    pairs = []
    for f in files:
        with np.load(f) as crop:
            if is_excluded(str(crop["granule"])):
                print(f"   skipping {Path(f).name}: touches an excluded date (D-13)")
                continue
            pairs.append(dict(crop))
    for a, b in zip(pairs, pairs[1:]):
        if pair_dates(str(a["granule"]))[1] != pair_dates(str(b["granule"]))[0]:
            raise SystemExit(f"Chain broken between {a['granule']} and {b['granule']}")
    return pairs, pairs[0]["xCoordinates"], pairs[0]["yCoordinates"], int(pairs[0]["projection"])


def box_mask(x: np.ndarray, y: np.ndarray, epsg: int, box: tuple) -> np.ndarray:
    """Boolean grid mask for a lon/lat box."""
    to_grid = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    x0, y0 = to_grid.transform(box[0], box[1])
    x1, y1 = to_grid.transform(box[2], box[3])
    return (x[None, :] >= x0) & (x[None, :] <= x1) & (y[:, None] >= y0) & (y[:, None] <= y1)


def increments(pairs: list[dict], ref: np.ndarray) -> np.ndarray:
    """Per-pair phase increments (radians) on one shared zero, with components joined."""
    n = len(pairs)
    inc = np.full((n,) + ref.shape, np.nan)
    extra = []  # (pair index, component mask) still to re-attach
    for k, p in enumerate(pairs):
        phase = p["unwrappedPhase"].astype(np.float64) - p["ionospherePhaseScreen"].astype(np.float64)
        cc = p["connectedComponents"]
        comps, counts = np.unique(cc[ref & (cc > 0)], return_counts=True)
        main = comps[np.argmax(counts)]
        ok = (cc == main) & np.isfinite(phase)
        inc[k] = np.where(ok, phase - np.median(phase[ref & ok]), np.nan)
        for comp in np.unique(cc):
            if comp not in (0, main) and (cc == comp).sum() >= MIN_COMPONENT_PIXELS:
                extra.append((k, cc == comp, np.where(cc == comp, phase - np.median(phase[ref & ok]), np.nan)))
    for k, mask, values in extra:
        neighbours = [inc[j] for j in (k - 1, k + 1) if 0 <= j < n]
        with warnings.catch_warnings():  # pixels empty in both neighbours are expected; they become NaN
            warnings.simplefilter("ignore", RuntimeWarning)
            expected = np.nanmean(np.stack(neighbours), axis=0)
        diff = np.nanmedian((expected - values)[mask])
        cycles = round(diff / (2 * math.pi))
        inc[k][mask] = values[mask] + 2 * math.pi * cycles
        print(f"   pair {k + 1}: re-attached a component of {mask.sum():,} pixels with {cycles:+d} cycles")
    return inc


def nearest_value(stack: np.ndarray, x: np.ndarray, y: np.ndarray, epsg: int, lon: float, lat: float) -> np.ndarray:
    """Median over a 7 x 7 pixel window (560 m) around a point, for each layer of a stack."""
    to_grid = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    gx, gy = to_grid.transform(lon, lat)
    r, c = int(np.argmin(np.abs(y - gy))), int(np.argmin(np.abs(x - gx)))
    window = stack[..., max(r - 3, 0):r + 4, max(c - 3, 0):c + 4]
    return np.nanmedian(window.reshape(window.shape[:-2] + (-1,)), axis=-1)


def background(data: Path) -> np.ndarray | None:
    """Mean HH backscatter in dB from the GCOV crops, as a gray background, if present."""
    files = [f for f in sorted(glob.glob(str(data / "mexico_city_gcov_*.npz")))
             if Path(f).stem.rsplit("_", 1)[-1] not in BACKGROUND_EXCLUDED_DATES]
    if not files:
        return None
    hh = [np.load(f)["HHHH"] for f in files[:: max(len(files) // 6, 1)]]
    with np.errstate(divide="ignore", invalid="ignore"):
        return 10 * np.log10(np.nanmean(np.stack(hh), axis=0))


def write_geotiff(path: Path, band: np.ndarray, x: np.ndarray, y: np.ndarray, epsg: int,
                  description: str, units: str) -> None:
    """Single-band float32 GeoTIFF on the crop grid (coordinates are pixel centers), NaN = no data."""
    import rasterio
    from rasterio.transform import from_bounds

    dx, dy = float(x[1] - x[0]), float(y[0] - y[1])
    if not (dx > 0 and dy > 0 and np.allclose(np.diff(x), dx) and np.allclose(-np.diff(y), dy)):
        raise SystemExit("The crops must use a regular north-up grid")
    transform = from_bounds(x[0] - dx / 2, y[-1] - dy / 2, x[-1] + dx / 2, y[0] + dy / 2, x.size, y.size)
    tmp = path.with_name(path.stem + ".partial.tif")
    with rasterio.open(tmp, "w", driver="GTiff", width=x.size, height=y.size, count=1, dtype="float32",
                       crs=f"EPSG:{epsg}", transform=transform, nodata=np.nan, compress="deflate") as dst:
        dst.write(band.astype(np.float32), 1)
        dst.set_band_description(1, description)
        dst.update_tags(units=units, sign=SIGN, reference_box_lonlat=",".join(map(str, REFERENCE_BOX)),
                        data="NISAR L2 GUNW PROVISIONAL (P05023), line of sight, relative to the reference area",
                        generated_by="poc/mexico_city_sinking/sinking_poc.py (AI-assisted, see docs/AI_USAGE.md)")
    os.replace(tmp, path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mexico City ground motion from the NISAR GUNW chain.")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA,
                        help="folder with the mexico_city_gunw_*.npz crops (default: data/Mexico_City/)")
    args = parser.parse_args()
    data = args.data.resolve()
    started = time.perf_counter()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pairs, x, y, epsg = load_pairs(data)
    dates = [pair_dates(str(pairs[0]["granule"]))[0]] + [pair_dates(str(p["granule"]))[1] for p in pairs]
    print(f"{len(pairs)} pairs, {dates[0]} to {dates[-1]}, grid {x.size} x {y.size} at 80 m, EPSG:{epsg}")

    ref = box_mask(x, y, epsg, REFERENCE_BOX)
    inc = increments(pairs, ref)

    # Gap filling. Some acquisitions lose coherence in places (for example a strip
    # on 2026-03-23, and the airport on 2025-11-23), which knocks out the two pairs
    # that share that date. Where a pixel misses at most MAX_FILLED pairs, fill each
    # missing increment with that pixel's average rate times the pair's length.
    # The atmosphere of the bad date cancels in the sum anyway; what is lost is
    # the real motion over those days, which we interpolate.
    days_per_pair = np.array([(date.fromisoformat(b) - date.fromisoformat(a)).days
                              for a, b in (pair_dates(str(p["granule"])) for p in pairs)], dtype=float)
    missing = ~np.isfinite(inc)
    n_missing = missing.sum(axis=0)
    valid_days = np.where(missing, 0.0, days_per_pair[:, None, None]).sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        rate_per_day = np.nansum(inc, axis=0) / valid_days
    fill = missing & (n_missing <= MAX_FILLED)[None]
    inc[fill] = (rate_per_day[None] * days_per_pair[:, None, None] * np.ones_like(inc))[fill]
    valid = n_missing <= MAX_FILLED
    pixel_share = {"all_pairs": float((n_missing == 0).mean()),
                   "gap_filled": float(((n_missing > 0) & valid).mean()),
                   "dropped": float((~valid).mean())}
    print(f"Pixels with all pairs: {pixel_share['all_pairs']:.0%}; with 1 to {MAX_FILLED} pairs gap-filled: "
          f"{pixel_share['gap_filled']:.0%}; dropped: {pixel_share['dropped']:.0%}")
    cum_cm = np.concatenate([np.zeros((1,) + valid.shape),
                             np.cumsum(inc, axis=0) * WAVELENGTH_CM / (4 * math.pi)])
    cum_cm[:, ~valid] = np.nan
    days = np.array([(date.fromisoformat(d) - date.fromisoformat(dates[0])).days for d in dates])
    years = days[-1] / 365.25
    total = cum_cm[-1]
    rate_cm_yr = total / years
    print(f"Pixels kept: {valid.mean():.0%}")
    print(f"Total line-of-sight change, 1st / 50th / 99th percentile: "
          f"{np.nanpercentile(total, 1):.1f} / {np.nanpercentile(total, 50):.1f} / {np.nanpercentile(total, 99):.1f} cm "
          f"over {days[-1]} days")

    # Whole-map numbers quoted in the README.
    jpl_index = dates.index(JPL_COMPARE_END)
    pixel_km2 = abs(float(x[1] - x[0]) * float(y[0] - y[1])) / 1e6
    with np.errstate(invalid="ignore"):
        stats = {
            "total_cm_p1": float(np.nanpercentile(total, 1)),
            "total_cm_p50": float(np.nanpercentile(total, 50)),
            "total_cm_p99": float(np.nanpercentile(total, 99)),
            "rate_cm_per_year_p99": float(np.nanpercentile(rate_cm_yr, 99)),
            "area_km2_faster_than_10_cm_per_year": float((rate_cm_yr > 10).sum() * pixel_km2),
            "area_km2_faster_than_20_cm_per_year": float((rate_cm_yr > 20).sum() * pixel_km2),
            f"cm_by_{JPL_COMPARE_END}_p99_9": float(np.nanpercentile(cum_cm[jpl_index], 99.9)),
        }
    print(f"Rate 99th percentile {stats['rate_cm_per_year_p99']:.1f} cm/yr; "
          f"area > 10 cm/yr {stats['area_km2_faster_than_10_cm_per_year']:.0f} km2, "
          f"> 20 cm/yr {stats['area_km2_faster_than_20_cm_per_year']:.0f} km2; "
          f"fastest 0.1% by {JPL_COMPARE_END}: {stats[f'cm_by_{JPL_COMPARE_END}_p99_9']:.1f} cm")

    granules = [str(p["granule"]) for p in pairs]
    np.savez_compressed(data / "displacement_cumulative.npz", cumulative_los_cm=cum_cm.astype(np.float32),
                        dates=np.array(dates), xCoordinates=x, yCoordinates=y, projection=np.uint32(epsg),
                        filled_pairs=n_missing.astype(np.uint8), granules=np.array(granules),
                        reference_box_lonlat=np.array(REFERENCE_BOX), wavelength_cm=np.float64(WAVELENGTH_CM),
                        note=f"{SIGN} Relative to the western-hills reference. PROVISIONAL.")

    # Rasters for the ground-motion layer (T-33) and the flood-priority map (T-34, PR #20).
    total_tif, rate_tif = data / "los_total_cm.tif", data / "los_rate_cm_per_year.tif"
    write_geotiff(total_tif, total, x, y, epsg,
                  f"cumulative line-of-sight displacement {dates[0]} to {dates[-1]}", "cm")
    write_geotiff(rate_tif, rate_cm_yr, x, y, epsg,
                  f"line-of-sight rate, year total / {years:.4f} years", "cm/year")

    # Provenance, git-tracked. Top-level keys follow --los-metadata in PR #20 (docs/FLOOD_PRIORITY.md)
    # and describe the rate raster; "files" describes every output.
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]
    provenance = {
        "_comment": "Written by poc/mexico_city_sinking/sinking_poc.py (AI-assisted code, see docs/AI_USAGE.md). "
                    "PROVISIONAL data. Line of sight, not vertical.",
        "units": "cm/year",
        "positiveDirection": "away",
        "signConvention": SIGN,
        "signStatus": "INFERRED, not confirmed (T-35)",
        "referenceArea": "Western hills near Santa Fe, assumed stable (not yet a literature-named outcrop); "
                         "its median is zero on every date",
        "referenceBoxLonLat": list(REFERENCE_BOX),
        "source": f"poc/mexico_city_sinking/sinking_poc.py (sha256 {script_sha}) on NISAR L2 GUNW PROVISIONAL "
                  "crops (CRID P05023) from ASF DAAC",
        "collection": "NISAR_L2_GUNW_PROVISIONAL_V1 (CRID P05023)",
        "track": 19, "frame": 11, "direction": "ASCENDING",
        "granules": granules,
        "dates": dates,
        "excludedDates": sorted(EXCLUDED_DATES),
        "excludedDatesReason": "D-13: measurement errors in the Oct 30, 2025 acquisition",
        "wavelengthCm": round(WAVELENGTH_CM, 4),
        "wavelengthNote": f"from centerFrequency {CENTER_FREQUENCY_HZ:.4g} Hz of a same-mode (40 MHz) GUNW on "
                          "track 113; the track 19 crops do not store it (effect on numbers about 1 to 2%)",
        "maxFilledPairs": MAX_FILLED,
        "gapFilling": f"pixels missing at most {MAX_FILLED} of {len(pairs)} pairs are filled from their own average "
                      "rate (count per pixel in filled_pairs in the stack); pixels missing more are NaN",
        "pixelShare": {k: round(v, 4) for k, v in pixel_share.items()},
        "grid": {"crs": f"EPSG:{epsg}", "pixelMeters": round(abs(float(x[1] - x[0])), 3),
                 "width": int(x.size), "height": int(y.size),
                 "coordinates": "pixel centers, north-up"},
        "statistics": {k: round(v, 2) for k, v in stats.items()},
        "statisticsNote": "percentiles over valid pixels; quote percentiles, never the maximum (isolated "
                          "unwrapping errors exceed 100 cm/year)",
        "files": {
            "rate": {"file": rate_tif.name, "units": "cm/year", "nodata": "NaN",
                     "quantity": f"line-of-sight rate: year total divided by {years:.4f} years"},
            "total": {"file": total_tif.name, "units": "cm", "nodata": "NaN",
                      "quantity": f"cumulative line-of-sight displacement since {dates[0]}, at {dates[-1]}"},
            "stack": {"file": "displacement_cumulative.npz",
                      "quantity": f"cumulative line-of-sight cm since {dates[0]} for every date; key "
                                  f"cumulative_los_cm, shape {len(dates)} x {y.size} x {x.size}, plus filled_pairs"},
            "folder": "the --data folder, data/Mexico_City/ by default (git-ignored)",
        },
    }
    (HERE / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

    # Landmark table and CSV.
    rows = []
    print(f"\n{'Place':38s} {'total cm':>8s} {'cm/yr':>6s} {'cm/month':>8s}  {dates[0]} to {JPL_COMPARE_END}")
    for name, (lon, lat) in LANDMARKS.items():
        series = nearest_value(cum_cm, x, y, epsg, lon, lat)
        rate = series[-1] / years if np.isfinite(series[-1]) else float("nan")
        print(f"{name:38s} {series[-1]:8.1f} {rate:6.1f} {rate / 12:8.2f}  {series[jpl_index]:6.1f} cm")
        rows.append((name, lon, lat, series))
    with open(HERE / "landmark_series_los_cm.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["place", "lon", "lat"] + dates)
        for name, lon, lat, series in rows:
            writer.writerow([name, lon, lat] + [f"{v:.2f}" for v in series])

    # Figure: map of the year's total, and time series at the landmarks.
    to_ll = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    west, south = to_ll.transform(x[0], y[-1])
    east, north = to_ll.transform(x[-1], y[0])
    extent = (west, east, south, north)
    fig, (ax_map, ax_ts) = plt.subplots(1, 2, figsize=(15, 7), dpi=110, gridspec_kw={"width_ratios": [1.15, 1]})
    bg = background(data)
    if bg is not None:
        ax_map.imshow(bg, cmap="gray", vmin=np.nanpercentile(bg, 2), vmax=np.nanpercentile(bg, 98), extent=extent)
    im = ax_map.imshow(np.ma.masked_invalid(total), cmap="YlOrRd", vmin=0, vmax=25, alpha=0.85, extent=extent)
    fig.colorbar(im, ax=ax_map, shrink=0.8, label="cm moved away from the satellite (line of sight)")
    rx = [REFERENCE_BOX[0], REFERENCE_BOX[2], REFERENCE_BOX[2], REFERENCE_BOX[0], REFERENCE_BOX[0]]
    ry = [REFERENCE_BOX[1], REFERENCE_BOX[1], REFERENCE_BOX[3], REFERENCE_BOX[3], REFERENCE_BOX[1]]
    ax_map.plot(rx, ry, color="cyan", lw=1.5, label="reference area (assumed stable)")
    for name, (lon, lat) in LANDMARKS.items():
        ax_map.plot(lon, lat, "o", ms=5, mfc="white", mec="black")
        ax_map.annotate(name.split(" (")[0], (lon, lat), xytext=LABEL_OFFSET.get(name, (4, 3)),
                        textcoords="offset points", fontsize=7,
                        bbox={"boxstyle": "round,pad=0.1", "fc": "white", "alpha": 0.6, "lw": 0})
    ax_map.legend(loc="lower left", fontsize=7)
    ax_map.set_title(f"Ground motion {dates[0]} to {dates[-1]} ({len(pairs)} NISAR pairs, track 19)", fontsize=10)
    ax_map.set_xlabel("Longitude")
    ax_map.set_ylabel("Latitude")

    t = [date.fromisoformat(d) for d in dates]
    for name, _, _, series in rows:
        style = "--" if "control" in name else "-"
        ax_ts.plot(t, series, style, marker=".", label=name)
    ax_ts.axvline(date.fromisoformat(JPL_COMPARE_END), color="gray", lw=0.8, ls=":")
    ax_ts.text(date.fromisoformat(JPL_COMPARE_END), ax_ts.get_ylim()[0] + 0.3, " end of JPL's published window (approx.)",
               fontsize=7, color="gray", va="bottom")
    ax_ts.set_ylabel("cm moved away from the satellite since Nov 11, 2025")
    ax_ts.set_title("Every 12 days at selected places (median of 560 m around each point)", fontsize=10)
    ax_ts.legend(fontsize=7, loc="upper left")
    ax_ts.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.text(0.01, 0.005, "Data: NASA/ISRO NISAR L2 GUNW PROVISIONAL (P05023), ASF DAAC. Line-of-sight motion, not purely vertical; "
             "relative to the reference area; sign set so that motion away from the satellite is positive (inferred). "
             f"Gaps: pixels missing more than {MAX_FILLED} of {len(pairs)} pairs (water, steep forest); up to {MAX_FILLED} "
             "missing pairs are filled from the pixel's own rate. Place locations approximate.",
             fontsize=6.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out = HERE / "fig_mexico_city_year_of_sinking.png"
    fig.savefig(out, bbox_inches="tight")
    for path in (out, HERE / "landmark_series_los_cm.csv", HERE / "provenance.json",
                 data / "displacement_cumulative.npz", total_tif, rate_tif):
        print(f"wrote {path}")
    print(f"done in {time.perf_counter() - started:.0f} s")


if __name__ == "__main__":
    main()
