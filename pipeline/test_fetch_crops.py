"""Offline crop smoke test. Drafted with AI assistance."""

from types import SimpleNamespace

import h5py
import numpy as np
import pytest

import fetch_crops


@pytest.mark.parametrize("product,group_path,layers", [
    ("GCOV", "/science/LSAR/GCOV/grids/frequencyB", {
        "HHHH": "float32", "HVHV": "float32",
    }),
    ("GUNW", "/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH", {
        "unwrappedPhase": "float32", "coherenceMagnitude": "float32",
        "connectedComponents": "uint16", "ionospherePhaseScreen": "float32",
    }),
])
def test_fetch_writes_mexico_city_window(tmp_path, monkeypatch, product, group_path, layers):
    fixture = tmp_path / "granule.h5"
    pixels = np.arange(12).reshape(3, 4)
    with h5py.File(fixture, "w") as source:
        group = source.create_group(group_path)
        group["projection"] = 4326
        group["xCoordinates"] = [-100, -99.3, -99.0, -98.0]
        group["yCoordinates"] = [20.0, 19.4, 19.2]
        for index, (name, dtype) in enumerate(layers.items()):
            group[name] = (pixels + index * 10).astype(dtype)

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
    output = fetch_crops.fetch_crop("mexico_city", product, "2025-10-30")
    assert output.name == f"mexico_city_{product.lower()}_2025-10-30.npz"
    with np.load(output) as crop:
        for index, (name, dtype) in enumerate(layers.items()):
            np.testing.assert_array_equal(crop[name], pixels[1:, 1:3] + index * 10)
            assert crop[name].dtype == np.dtype(dtype)
        np.testing.assert_array_equal(crop["xCoordinates"], [-99.3, -99.0])
        np.testing.assert_array_equal(crop["yCoordinates"], [19.4, 19.2])
        assert crop["projection"].item() == 4326


def test_existing_gunw_crop_skips_without_login(tmp_path, monkeypatch, capsys):
    output = tmp_path / "mexico_city_gunw_2025-10-30.npz"
    np.savez_compressed(output, unwrappedPhase=[1])
    original = output.read_bytes()
    monkeypatch.setattr(fetch_crops, "OUTPUT_DIR", tmp_path)

    def unexpected_login(**kwargs):
        pytest.fail("An existing GUNW crop must skip before authentication")

    monkeypatch.setattr(fetch_crops.earthaccess, "login", unexpected_login)
    assert fetch_crops.fetch_crop("mexico_city", "GUNW", "2025-10-30") == output
    assert capsys.readouterr().out == f"skip {output}\n"
    assert output.read_bytes() == original
