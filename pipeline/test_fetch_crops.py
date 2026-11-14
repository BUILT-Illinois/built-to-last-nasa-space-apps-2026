"""Offline crop smoke test. Drafted with AI assistance."""

from types import SimpleNamespace

import h5py
import numpy as np

import fetch_crops


def test_fetch_gcov_writes_mexico_city_window(tmp_path, monkeypatch):
    fixture = tmp_path / "granule.h5"
    pixels = np.arange(12).reshape(3, 4)
    with h5py.File(fixture, "w") as source:
        group = source.create_group(fetch_crops.GCOV_GRIDS.format(freq="B"))
        group["projection"] = 4326
        group["xCoordinates"] = [-100, -99.3, -99.0, -98.0]
        group["yCoordinates"] = [20.0, 19.4, 19.2]
        group["HHHH"] = pixels
        group["HVHV"] = pixels + 10

    def login(*, strategy):
        assert strategy == "netrc"
        return SimpleNamespace(authenticated=True)

    def open_granule(url, mode, **kwargs):
        assert url.startswith("https://nisar.")
        return fixture.open(mode)

    monkeypatch.setattr(fetch_crops.earthaccess, "login", login)
    monkeypatch.setattr(fetch_crops.earthaccess, "get_fsspec_https_session",
                        lambda: SimpleNamespace(open=open_granule))
    monkeypatch.setattr(fetch_crops, "OUTPUT_DIR", tmp_path / "interim")
    output = fetch_crops.fetch_crop("mexico_city", "GCOV", "2025-10-30")
    assert output.name == "mexico_city_gcov_2025-10-30.npz"
    with np.load(output) as crop:
        np.testing.assert_array_equal(crop["HHHH"], pixels[1:, 1:3])
        np.testing.assert_array_equal(crop["HVHV"], pixels[1:, 1:3] + 10)
        np.testing.assert_array_equal(crop["xCoordinates"], [-99.3, -99.0])
        np.testing.assert_array_equal(crop["yCoordinates"], [19.4, 19.2])
        assert crop["projection"].item() == 4326
