"""T-34 regression for masked LOS pixels, signed rates, cell ranks and bundle publishing."""

import json

import numpy as np
import rasterio
from PIL import Image
from rasterio.transform import rowcol
from rasterio.warp import transform

import build_flood_priority as priority


def test_priority_build(tmp_path, monkeypatch):
    output = tmp_path / "mexico_city"
    output.mkdir()
    bbox = [-99.40, 19.10, -98.85, 19.65]
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps({
        "schemaVersion": "0.1", "region": {"id": "mexico_city", "bbox": bbox},
        "layers": [{"id": "gcov_hh"}],
    }), encoding="utf-8")
    landmark_path = output / "landmarks.json"
    landmark_path.write_text('{"landmarks":[{"id":"lake","name":"Lake","lon":-98.97,"lat":19.27}]}',
                             encoding="utf-8")
    original_landmarks = landmark_path.read_bytes()
    shape, grid = priority.map_grid(bbox)
    water = np.full(shape, 6, dtype=np.uint8)
    coverage = np.ones(shape, dtype=bool)
    gcov = "NISAR_L2_PR_GCOV_test"
    gunw = "NISAR_L2_PR_GUNW_test"
    dates = priority.monthly_dates("mexico_city")
    monkeypatch.setattr(priority, "water_persistence", lambda *_: (dates, grid, [gcov], water, coverage))
    rate = np.full(shape, -20, dtype=np.float32)
    x, y = transform("EPSG:4326", "EPSG:3857", [-98.97], [19.27])
    row, col = rowcol(grid, x[0], y[0])
    rate[row, col] = -9999
    los_path = tmp_path / "los.tif"
    with rasterio.open(los_path, "w", driver="GTiff", height=shape[0], width=shape[1], count=1,
                       dtype="float32", crs=priority.WEB_CRS, transform=grid, nodata=-9999) as raster:
        raster.write(rate, 1)
    metadata_path = tmp_path / "los.json"
    metadata_path.write_text(json.dumps({
        "units": "mm/year", "positiveDirection": "toward", "referenceArea": "Test reference",
        "source": "Test raster", "granules": [gunw], "track": 19, "frame": 11, "direction": "ASCENDING",
    }), encoding="utf-8")

    priority.build(tmp_path, output, los_path, metadata_path)
    manifest = priority.read_json(manifest_path)
    assert [layer["id"] for layer in manifest["layers"]] == ["gcov_hh", "flood_priority"]
    frame = manifest["layers"][-1]["frames"][0]
    assert frame["granules"] == [gcov, gunw]
    with Image.open(output / frame["image"]) as image:
        assert image.getpixel((col, row))[3] == 0
        assert image.getpixel((col + 1, row))[3] == 255
    hotspots = priority.read_json(output / "hotspots.json")
    assert hotspots["awayRateP95"] == 20
    assert len(hotspots["areas"]) == 10
    for area in hotspots["areas"]:
        assert (area["rank"], area["losRate"], area["waterMonths"], area["score"]) == (1, -20, 6, 0.75)
    assert hotspots["landmarks"][0]["losRate"] is None
    assert hotspots["landmarks"][0]["waterMonths"] == 6
    assert hotspots["landmarks"][0]["score"] is None
    assert hotspots["landmarks"][0]["cellRank"] == 1
    assert landmark_path.read_bytes() == original_landmarks
