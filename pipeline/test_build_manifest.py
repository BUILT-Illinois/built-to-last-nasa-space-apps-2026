"""Test the GCOV app bundle. Drafted with AI assistance (Codex)."""

import json
import csv
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

import build_manifest as builder
import fetch_crops as fetcher

REGION = "mexico_city"
DATES = ("2025-10-30", "2025-11-11")
MONTHLY_DATES = (*DATES, "2025-12-17")


@pytest.fixture
def crops(tmp_path):
    bbox = json.loads(builder.CONFIG_PATH.read_text())["regions"][REGION]["bbox"]
    shape, transform = builder.map_grid(bbox)
    rows, cols = np.indices(shape)
    x = transform.c + transform.a * (np.arange(shape[1]) + 0.5)
    y = transform.f + transform.e * (np.arange(shape[0]) + 0.5)
    for index, day in enumerate(MONTHLY_DATES):
        # The north half is brighter. Values common to both dates must render
        # the same, even though the second date has a wider HH distribution.
        hh = np.where(rows < shape[0] // 2, 0.1, 0.01 if index == 0 else 0.001)
        hh[165:225, :] = 0.025
        hv = np.where(cols < shape[1] // 2, 0.01, 0.001)
        hh[:20, :20] = 0
        hv[30:50, :20] = np.inf
        granule = builder.find_granule(REGION, "GCOV", day)["scene_name"]
        np.savez(tmp_path / f"{REGION}_gcov_{day}.npz", HHHH=hh, HVHV=hv,
                 xCoordinates=x, yCoordinates=y, projection=3857, granule=granule)
    return tmp_path


@pytest.mark.parametrize("dates", [DATES, MONTHLY_DATES])
def test_cli_writes_app_bundle(crops, tmp_path, dates):
    output = tmp_path / "bundle"
    subprocess.run(
        [sys.executable, builder.__file__, "--dates", *reversed(dates), "--offline",
         "--crop-dir", str(crops), "--output", str(output)],
        check=True,
    )
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["schemaVersion"] == "0.1"
    assert manifest["dataMaturity"] == "PROVISIONAL"
    assert manifest["region"]["id"] == REGION
    bbox = manifest["region"]["bbox"]
    assert [layer["id"] for layer in manifest["layers"]] == [
        "gcov_hh", "gcov_hv", "gcov_composite",
    ]
    images = {}
    for layer in manifest["layers"]:
        assert layer["bounds"] == bbox
        assert [frame["date"] for frame in layer["frames"]] == list(dates)
        for frame in layer["frames"]:
            day = frame["date"]
            assert frame["granules"] == [builder.find_granule(REGION, "GCOV", day)["scene_name"]]
            assert (frame["track"], frame["frame"], frame["direction"]) == (19, 11, "ASCENDING")
            asset = output / frame["image"]
            assert frame["image"] == f"layers/{layer['id']}/{day}.webp"
            assert asset.stat().st_size < builder.IMAGE_LIMIT
            with Image.open(asset) as image:
                assert image.format == "WEBP"
                assert (image.height, image.width) == builder.map_grid(bbox)[0]
                images[layer["id"], day] = np.asarray(image.convert("RGBA"))
    hh, hv, composite = (images[layer, DATES[0]] for layer in
                         ("gcov_hh", "gcov_hv", "gcov_composite"))
    assert hh[8, 8, 3] == composite[8, 8, 3] == 0
    assert hv[8, 8, 3] == 255
    assert hh[40, 8, 3] == 255
    assert hv[40, 8, 3] == composite[40, 8, 3] == 0
    assert hh[110, 100, 0] > hh[-100, 100, 0]
    np.testing.assert_allclose(hh[195, 100, :3], images["gcov_hh", DATES[1]][195, 100, :3], atol=4)
    assert composite[110, 100, 2] < composite[110, -100, 2]
    assert manifest["layers"][0]["colormap"]["min"] == pytest.approx(-30)
    assert manifest["layers"][0]["colormap"]["max"] == pytest.approx(-10)
    landmarks = json.loads((output / "landmarks.json").read_text())
    assert landmarks["schemaVersion"] == "0.1"
    assert landmarks["regionId"] == REGION
    assert "landmarks" in landmarks
    assert sum(path.stat().st_size for path in output.rglob("*") if path.is_file()) < builder.TIER_1_REGION_LIMIT


def test_fetches_only_the_missing_crop(crops, tmp_path, monkeypatch):
    missing = crops / f"{REGION}_gcov_{DATES[1]}.npz"
    fetched = missing.rename(crops / "fetched.npz")
    monkeypatch.setattr(builder, "OUTPUT_DIR", tmp_path / "uncached")
    calls = []

    def fetch(region, product, day):
        calls.append((region, product, day))
        return fetched

    monkeypatch.setattr(builder, "fetch_crop", fetch)
    builder.build(REGION, DATES, crops, tmp_path / "output")
    assert calls == [(REGION, "GCOV", DATES[1])]


def test_offline_missing_crop_preserves_existing_manifest(crops, tmp_path, monkeypatch):
    (crops / f"{REGION}_gcov_{DATES[1]}.npz").unlink()
    monkeypatch.setattr(builder, "OUTPUT_DIR", tmp_path / "uncached")
    output = tmp_path / "output"
    output.mkdir()
    manifest = output / "manifest.json"
    manifest.write_text("previous")
    with pytest.raises(ValueError, match="No cached GCOV crop"):
        builder.build(REGION, DATES, crops, output, offline=True)
    assert list(output.iterdir()) == [manifest]
    assert manifest.read_text() == "previous"


def test_rejects_unapproved_crop(crops, tmp_path):
    first = crops / f"{REGION}_gcov_{DATES[0]}.npz"
    second = crops / f"{REGION}_gcov_{DATES[1]}.npz"
    second.replace(first)
    with pytest.raises(ValueError, match="does not match approved granule"):
        builder.build(REGION, DATES, crops, tmp_path / "output", offline=True)


def test_configured_region_and_bbox_cache(crops, tmp_path, monkeypatch):
    config = json.loads(builder.CONFIG_PATH.read_text())
    region = "new_region"
    config["regions"][region] = {
        "name": "New Region", "bbox": config["regions"][REGION]["bbox"][:],
        "gcov": {"track": 42, "frame": 5, "direction": "DESCENDING",
                 "release": "P05023", "dates": list(reversed(DATES))},
    }
    config_path = tmp_path / "regions.json"
    config_path.write_text(json.dumps(config))
    monkeypatch.setattr(builder, "CONFIG_PATH", config_path)
    monkeypatch.setattr(fetcher, "CONFIG_PATH", config_path)
    monkeypatch.setattr(fetcher, "region_bbox",
                        lambda key: json.loads(config_path.read_text())["regions"][key]["bbox"])
    monkeypatch.setattr(fetcher, "HERE", tmp_path)
    reports = tmp_path / "reports"
    reports.mkdir()
    with (reports / f"granules_{region}.csv").open("w", newline="") as stream:
        fields = ["product_type", "start_time", "maturity", "crid", "track", "frame",
                  "direction", "scene_name"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for day in DATES:
            scene_name = f"fixture_{day}"
            writer.writerow(dict(zip(fields, ["GCOV", day, "PROVISIONAL", "P05023",
                                               42, 5, "DESCENDING", scene_name])))
            path = crops / fetcher.output_path(region, "GCOV", day).name
            with np.load(crops / f"{REGION}_gcov_{day}.npz") as source:
                np.savez(path, **{**dict(source), "granule": scene_name})

    output = tmp_path / "output"
    builder.build(region, fetcher.monthly_dates(region), crops, output, offline=True)
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["schemaVersion"] == "0.1"
    assert manifest["region"]["id"] == region
    assert [f["date"] for f in manifest["layers"][0]["frames"]] == list(DATES)
    assert all((f["track"], f["frame"], f["direction"]) == (42, 5, "DESCENDING")
               for f in manifest["layers"][0]["frames"])

    before = fetcher.output_path(REGION, "GCOV", DATES[0])
    assert before.name == f"{REGION}_gcov_{DATES[0]}.npz"
    config["regions"][REGION]["bbox"][0] -= 0.1
    config_path.write_text(json.dumps(config))
    assert fetcher.output_path(REGION, "GCOV", DATES[0]) != before
