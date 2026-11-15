"""Regression coverage for native GCOV landmark sampling (AI-assisted)."""
import numpy as np
import pytest
from rasterio.warp import transform

from landmark_series import enrich


def test_centered_native_window_missing_pixels_and_provisional_count(tmp_path):
    lon, lat = -99.07, 19.44
    east, north = transform("EPSG:4326", "EPSG:32614", [lon], [lat])
    x = east[0] + np.arange(-3, 4) * 80
    y = north[0] - np.arange(-3, 4) * 80
    hh = np.ones((7, 7))
    hv = hh.copy()
    # Bright border tests the window bounds; a bright center tests use of the median.
    hh[1:6, 1:6], hv[1:6, 1:6] = 10**(-1.3), 10**(-2.1)
    hh[3, 3], hv[3, 3] = 1, 1
    hh[2, 2], hv[2, 2] = np.nan, 0
    path = tmp_path / "crop.npz"
    np.savez(path, granule="scene", xCoordinates=x, yCoordinates=y,
             projection=32614, HHHH=hh, HVHV=hv)
    dates = ["2026-04-16", "2025-11-11", "2025-12-17"]
    points = [{"lon": lon, "lat": lat}, {"lon": -98.97, "lat": 19.27}]
    covered, uncovered = enrich(points, dates, dict.fromkeys(dates[:2], (path, "scene")))
    series = covered["series"]
    assert [p["date"] for p in series["hh_db"]] == sorted(dates)
    assert [p["value"] for p in series["hh_db"]] == [pytest.approx(-13), None, None]
    assert [p["value"] for p in series["hv_db"]] == [pytest.approx(-21), None, None]
    assert series["water_months"] == {"count": 1, "valid_months": 1, "provisional": True}
    assert uncovered["series"] == {}
