"""Offline sinking ingest tests. Drafted with AI assistance (Codex)."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import rasterio
from PIL import Image
from rasterio.transform import from_bounds
from rasterio.warp import transform_bounds

PIPELINE = Path(__file__).resolve().parents[1]
BBOX = json.loads((PIPELINE / "config/regions.json").read_text(encoding="utf-8"))["regions"]["mexico_city"]["bbox"]


def command(tiff, output, units, sign):
    return [
        sys.executable, str(PIPELINE / "ingest_sinking.py"), str(tiff),
        "--units", units, "--sign", sign, "--reference", "Generated test area",
        "--since", "2025-11-11", "--date", "2026-10-13", "--synthetic", "--output", str(output),
    ]


@pytest.mark.parametrize(("units", "sign", "factor"), [
    ("mm/yr", "positive-away", -10), ("cm/yr", "negative-away", 1),
])
def test_synthetic_rate_clips_converts_and_masks(tmp_path, units, sign, factor):
    west, south, east, north = transform_bounds("EPSG:4326", "EPSG:3857", *BBOX)
    # Cover the western two thirds of the bbox and extend one column beyond its west edge.
    dx = (east - west) / 3
    tiff = tmp_path / "synthetic-rate.tif"
    with rasterio.open(
        tiff, "w", driver="GTiff", width=3, height=3, count=1, dtype="float32",
        crs="EPSG:3857", transform=from_bounds(west - dx, south, east - dx, north, 3, 3),
        nodata=-9999,
    ) as raster:
        raster.write(np.array([
            [99, -40 * factor, 40 * factor],
            [99, -15 * factor, 0],
            [99, -9999, np.nan],
        ], dtype=np.float32), 1)
        raster.update_tags(status="SYNTHETIC", synthetic="true", granules="[]")

    output = tmp_path / "fixture" / "mexico_city"
    subprocess.run(command(tiff, output, units, sign), check=True, capture_output=True, text=True)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataMaturity"] == "SYNTHETIC"
    assert manifest["synthetic"] is True
    assert len(manifest["layers"]) == 1
    layer = manifest["layers"][0]
    assert layer["id"] == "sinking"
    assert layer["bounds"] == BBOX
    assert layer["units"] == "cm/yr"
    assert layer["referenceArea"] == "Generated test area"
    assert layer["awaySign"] == "positive"
    assert layer["losLabel"] == "Radar line-of-sight rate"
    assert layer["colormap"] == {"name": "los-blue-white-red", "min": -30, "max": 30}
    frame, = layer["frames"]
    assert frame["granules"] == []
    assert (frame["since"], frame["date"]) == ("2025-11-11", "2026-10-13")
    with Image.open(output / frame["image"]) as png:
        assert png.format == "PNG"
        image = png.convert("RGBA")
    w, h = image.size
    assert image.getpixel((0, h // 6)) == (178, 24, 43, 255)
    assert image.getpixel((w // 2, h // 6)) == (33, 102, 172, 255)
    assert image.getpixel((w // 6, h // 2)) == (217, 140, 150, 255)
    assert image.getpixel((w // 2, h // 2)) == (255, 255, 255, 255)
    for xy in [(w - 1, h // 6), (w // 6, h - 1), (w // 2, h - 1)]:
        assert image.getpixel(xy)[3] == 0


def test_synthetic_ingest_refuses_public_data(tmp_path):
    output = tmp_path / "app" / "public" / "data" / "mexico_city"
    result = subprocess.run(
        command(tmp_path / "unused.tif", output, "cm/yr", "negative-away"),
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "Synthetic output cannot go under app/public/data" in result.stderr
    assert not output.exists()
