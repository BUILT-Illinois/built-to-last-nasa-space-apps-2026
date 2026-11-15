"""Publish the Mexico City landmark series from cached native GCOV crops (AI-assisted)."""
import argparse
import json
from pathlib import Path

import numpy as np
from rasterio.warp import transform

from fetch_crops import monthly_dates, output_path
from quicklook import to_db

ROOT = Path(__file__).resolve().parents[1]
# D-17: anomalous acquisitions remain gaps and do not count toward water months.
EXCLUDED = {"2025-12-05", "2026-04-16"}
HH_CUTOFF, HV_CUTOFF = -12, -20

# The 7 landmark cards (T-19). The three gcov_19_* debug points were removed Sun Nov 15.
POINTS = (
    ("new_lake_chalco", "New Lake Chalco (Lago de Tláhuac-Xico)", -98.97, 19.27),
    ("tlahuac_ground_motion", "Tláhuac", -99.0, 19.28),
    ("nezahualcoyotl", "Nezahualcóyotl", -99.02, 19.4),
    ("aicm", "Benito Juárez International Airport", -99.07, 19.44),
    ("centro_historico", "Centro Histórico", -99.13, 19.43),
    ("angel_independencia", "Ángel de la Independencia", -99.17, 19.43),
    ("chalco_2024_flood", "Chalco", -98.90, 19.26),
)


def sample_crop(path, granule, points):
    with np.load(path, allow_pickle=False) as crop:
        if crop["granule"].item() != granule:
            raise ValueError(f"Crop {path.name} does not match published granule {granule}")
        x, y = crop["xCoordinates"], crop["yCoordinates"]
        if (x.size < 2 or y.size < 2 or not np.allclose(np.diff(x), 80)
                or not np.allclose(np.diff(y), -80)):
            raise ValueError(f"Crop {path.name} must use the native 80 m frequency-B grid")
        bands = [crop[name] for name in ("HHHH", "HVHV")]
        if any(band.shape != (y.size, x.size) for band in bands):
            raise ValueError(f"Crop {path.name} has an invalid band shape")
        px, py = transform("EPSG:4326", f"EPSG:{int(crop['projection'].item())}",
                           [p["lon"] for p in points], [p["lat"] for p in points])
        results = []
        for east, north in zip(px, py):
            col = int(np.floor((east - x[0]) / 80 + 0.5))
            row = int(np.floor((y[0] - north) / 80 + 0.5))
            if not (2 <= col < x.size - 2 and 2 <= row < y.size - 2):
                results.append((None, None))
                continue
            values = []
            for band in bands:
                window = to_db(band[row-2:row+3, col-2:col+3])
                valid = window[np.isfinite(window)]
                values.append(float(np.median(valid)) if valid.size else None)
            results.append(tuple(values))
    return results


def enrich(entries, dates, crops):
    if not entries:
        return []
    dates = sorted(dates)
    frames = [
        sample_crop(*crops[day], entries) if day in crops and day not in EXCLUDED
        else [(None, None)] * len(entries)
        for day in dates
    ]
    enriched = []
    for idx, entry in enumerate(entries):
        samples = [frame[idx] for frame in frames]
        series = {key: value for key, value in entry.get("series", {}).items()
                  if key not in {"hh_db", "hv_db", "water_months"}}
        for band, key in enumerate(("hh_db", "hv_db")):
            values = [sample[band] for sample in samples]
            if any(value is not None for value in values):
                series[key] = [{"date": day, "value": value} for day, value in zip(dates, values)]
        pairs = [(hh, hv) for hh, hv in samples if hh is not None and hv is not None]
        if pairs:
            series["water_months"] = {
                "count": sum(hh <= HH_CUTOFF and hv <= HV_CUTOFF for hh, hv in pairs),
                "valid_months": len(pairs),
                "provisional": True,
            }
        enriched.append({**entry, "series": series})
    return enriched


def include_points(entries):
    occupied = {(entry["lon"], entry["lat"]) for entry in entries}
    ids = {entry["id"] for entry in entries}
    return [*entries, *(
        {"id": key, "name": name, "lon": lon, "lat": lat,
         "summary": "Monthly radar backscatter sampling point.",
         "radarShows": "Median HH and HV backscatter around this point.",
         "weInfer": "The water threshold is provisional.",
         "drivers": {"human": None, "natural": None}, "sourceIds": ["nisar-gcov"]}
        for key, name, lon, lat in POINTS if (lon, lat) not in occupied and key not in ids
    )]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop-dir", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, default=ROOT / "app/public/data/mexico_city")
    args = parser.parse_args()
    path = args.bundle / "landmarks.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    manifest = json.loads((args.bundle / "manifest.json").read_text(encoding="utf-8"))
    if payload["regionId"] != "mexico_city" or manifest["region"]["id"] != "mexico_city":
        parser.error("Expected a mexico_city bundle")
    dates = monthly_dates("mexico_city")
    frames = {frame["date"]: frame["granules"]
              for layer in manifest["layers"] if layer["id"] == "gcov_hh"
              for frame in layer["frames"]}
    crops = {}
    for day in dates:
        if day in EXCLUDED:
            continue
        if len(frames.get(day, [])) != 1:
            parser.error(f"Expected one published HH granule for {day}")
        crop = args.crop_dir / output_path("mexico_city", "GCOV", day).name
        if not crop.is_file():
            parser.error(f"Missing monthly crop: {crop}")
        crops[day] = crop, frames[day][0]
    payload["landmarks"] = enrich(include_points(payload["landmarks"]), dates, crops)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                    encoding="utf-8")


if __name__ == "__main__":
    main()
