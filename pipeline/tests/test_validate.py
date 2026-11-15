"""Tests for pipeline/validate_manifest.py (T-08).

Written with AI assistance (Claude Code); reviewed by Zainab. See docs/AI_USAGE.md.
Run from the repo root:  .venv/bin/python -m pytest pipeline/tests/test_validate.py -v
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_manifest as vm  # noqa: E402

SAMPLE = Path(__file__).resolve().parents[2] / "app" / "public" / "data" / "sample"


# ---- check_bbox -------------------------------------------------------------

def test_bbox_good():
    assert vm.check_bbox([-99.40, 19.10, -98.85, 19.65], "b") == []

@pytest.mark.parametrize("bad", [
    [19.10, -99.40, 19.65, -98.85],   # lat/lon swapped: south -99.4 is out of range
    [-98.85, 19.10, -99.40, 19.65],   # west and east swapped
    [-99.40, 19.65, -98.85, 19.10],   # south and north swapped
    [-99.40, 19.10, -98.85],          # only 3 numbers
    "not a list",
    [-99.40, 19.10, "east", 19.65],   # not a number
    [-200, 19.10, -98.85, 19.65],     # out of range
])
def test_bbox_bad(bad):
    problems = vm.check_bbox(bad, "region.bbox")
    assert problems, f"should reject {bad!r}"
    assert all("region.bbox" in p for p in problems), "each problem should say where it is"


# ---- check_date -------------------------------------------------------------

def test_date_good():
    assert vm.check_date("2026-04-16", "d") == []

@pytest.mark.parametrize("bad", ["2026-4-16", "16/04/2026", "2026-02-30", "2026-04-16T00:00:00Z", 20260416, None, ""])
def test_date_bad(bad):
    problems = vm.check_date(bad, "frames[0].date")
    assert problems, f"should reject {bad!r}"
    assert "frames[0].date" in problems[0]


# ---- check_files_exist and check_size_budget, on a tiny manifest ------------

def tiny_manifest(images, vectors=None):
    m = {"layers": [{"id": "gcov_hh", "frames": [{"image": img} for img in images]}]}
    if vectors is not None:
        m["vectors"] = vectors
    return m

def test_files_exist_good(tmp_path):
    (tmp_path / "layers").mkdir()
    (tmp_path / "layers" / "a.webp").write_bytes(b"x")
    assert vm.check_files_exist(tiny_manifest(["layers/a.webp"]), tmp_path) == []

def test_files_exist_missing_image(tmp_path):
    problems = vm.check_files_exist(tiny_manifest(["layers/missing.webp"]), tmp_path)
    assert len(problems) == 1 and "missing.webp" in problems[0]

def test_files_exist_missing_vector(tmp_path):
    m = tiny_manifest([], vectors=[{"id": "v", "file": "vectors/nope.geojson"}])
    problems = vm.check_files_exist(m, tmp_path)
    assert len(problems) == 1 and "nope.geojson" in problems[0]

@pytest.mark.parametrize("path, expected", [
    ("../outside.webp", "outside the region folder"),
    ("/etc/hosts", "outside the region folder"),
    ("manifest.json", "must be a .webp file"),
    ("layers", "must be a .webp file"),        # a folder, not an image
])
def test_files_exist_rejects_bad_paths(tmp_path, path, expected):
    (tmp_path / "manifest.json").write_text("{}")
    (tmp_path / "layers").mkdir()
    problems = vm.check_files_exist(tiny_manifest([path]), tmp_path)
    assert any(expected in p for p in problems), problems

def test_size_budget_image_too_big(tmp_path):
    (tmp_path / "big.webp").write_bytes(b"0" * (vm.MAX_IMAGE_BYTES + 1))
    problems = vm.check_size_budget(tiny_manifest(["big.webp"]), tmp_path)
    assert problems and "big.webp" in problems[0]

def test_size_budget_skips_missing_and_passes_small(tmp_path):
    (tmp_path / "small.webp").write_bytes(b"0" * 100)
    assert vm.check_size_budget(tiny_manifest(["small.webp", "gone.webp"]), tmp_path) == []

def test_size_budget_folder_too_big_uses_the_constant(tmp_path, monkeypatch):
    monkeypatch.setattr(vm, "MAX_FOLDER_BYTES", 500)
    (tmp_path / "a.bin").write_bytes(b"0" * 300)
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.bin").write_bytes(b"0" * 300)
    problems = vm.check_size_budget(tiny_manifest([]), tmp_path)
    assert len(problems) == 1 and "over the 0.0005 MB budget" in problems[0]


# ---- The real sample folder -------------------------------------------------

def test_sample_folder_passes():
    problems = vm.validate_folder(SAMPLE)
    assert problems == [], "\n".join(problems)

def test_cli_exit_codes(tmp_path):
    assert vm.main(["x", str(SAMPLE)]) == 0
    (tmp_path / "manifest.json").write_text("{ not json")
    assert vm.main(["x", str(tmp_path)]) == 1


# ---- Broken copies of the sample: each must report the RIGHT problem ---------
# Each case: (what we break, the edit, text that must appear in a problem).

@pytest.fixture
def broken_copy(tmp_path):
    dst = tmp_path / "sample"
    shutil.copytree(SAMPLE, dst)
    return dst

def edit_json(folder, name, change):
    path = folder / name
    data = json.loads(path.read_text())
    change(data)
    path.write_text(json.dumps(data))

def set_bbox_swapped(m):
    w, s, e, n = m["region"]["bbox"]
    m["region"]["bbox"] = [s, w, n, e]

def layer0(m):
    return m["layers"][0]

def frame0(m):
    return m["layers"][0]["frames"][0]

MANIFEST_CASES = [
    ("swapped bbox",            set_bbox_swapped,                                      "region.bbox"),
    ("swapped center",          lambda m: m["region"].update(center=[19.40, -99.13]),  "region.center"),
    ("text zoom",               lambda m: m["region"].update(zoom="10"),               "region.zoom"),
    ("unknown kind",            lambda m: layer0(m).update(kind="photo"),              "layers[0].kind"),
    ("bad date",                lambda m: frame0(m).update(date="16/04/2026"),         "layers[0].frames[0].date"),
    ("bad direction",           lambda m: frame0(m).update(direction="ASC"),           "layers[0].frames[0].direction"),
    ("text track",              lambda m: frame0(m).update(track="19"),                "layers[0].frames[0].track"),
    ("colormap without name",   lambda m: layer0(m)["colormap"].pop("name"),           "layers[0].colormap.name"),
    ("text colormap min",       lambda m: layer0(m)["colormap"].update(min="0"),       "layers[0].colormap"),
    ("image leaves the folder", lambda m: frame0(m).update(image="../mexico_city/x.webp"), "outside the region folder"),
    ("image is not a .webp",    lambda m: frame0(m).update(image="../sample/manifest.json"), "must be a .webp file"),
    ("missing sources",         lambda m: m.pop("sources"),                            "missing field 'sources'"),
    ("missing vectors",         lambda m: m.pop("vectors"),                            "missing field 'vectors'"),
    ("no granules on real data", lambda m: m.update(synthetic=False),                  "granules"),
    ("synthetic is text",       lambda m: m.update(synthetic="yes"),                   "manifest.synthetic"),
    # These used to crash the validator (review on PR #6):
    ("frame without image",     lambda m: frame0(m).pop("image"),                      "missing field 'image'"),
    ("vector without file",     lambda m: m["vectors"].append({"id": "v", "title": "t", "source": "nisar-gcov"}),
                                                                                       "vectors[0]: missing field 'file'"),
    ("layers is null",          lambda m: m.update(layers=None),                       "manifest.layers: must be a list"),
    ("frames is null",          lambda m: layer0(m).update(frames=None),               "layers[0].frames: must be a non-empty list"),
    ("layer is a string",       lambda m: m["layers"].append("oops"),                  "layers[3]: expected an object"),
]

@pytest.mark.parametrize("name, change, expected", MANIFEST_CASES, ids=[c[0] for c in MANIFEST_CASES])
def test_broken_manifest_reports_the_right_problem(broken_copy, name, change, expected):
    edit_json(broken_copy, "manifest.json", change)
    problems = vm.validate_folder(broken_copy)       # must not raise
    assert any(expected in p for p in problems), f"{name}: expected '{expected}' in {problems}"

def landmark0(lm):
    return lm["landmarks"][0]

LANDMARK_CASES = [
    ("unknown source id",       lambda lm: landmark0(lm).update(sourceIds=["nope"]),   "landmarks[0].sourceIds"),
    # These used to crash the validator (review on PR #6):
    ("lon is null",             lambda lm: landmark0(lm).update(lon=None),             "lon and lat must be numbers"),
    ("lon is text",             lambda lm: landmark0(lm).update(lon="-99.07"),         "lon and lat must be numbers"),
    ("series is a list",        lambda lm: landmark0(lm).update(series=[]),            "landmarks[0].series: expected an object"),
    ("point is a bare number",  lambda lm: landmark0(lm)["series"].update(hh_db=[5]),  "landmarks[0].series.hh_db[0]"),
    ("value is text",           lambda lm: landmark0(lm)["series"]["hh_db"][0].update(value="-7"),
                                                                                       "must be a number or null"),
]

@pytest.mark.parametrize("name, change, expected", LANDMARK_CASES, ids=[c[0] for c in LANDMARK_CASES])
def test_broken_landmarks_reports_the_right_problem(broken_copy, name, change, expected):
    edit_json(broken_copy, "landmarks.json", change)
    problems = vm.validate_folder(broken_copy)       # must not raise
    assert any(expected in p for p in problems), f"{name}: expected '{expected}' in {problems}"

def test_missing_image_file_reports_it(broken_copy):
    (broken_copy / "layers" / "gcov_hh" / "2026-04-16.webp").unlink()
    problems = vm.validate_folder(broken_copy)
    assert any("file not found: layers/gcov_hh/2026-04-16.webp" in p for p in problems), problems

def test_duplicate_key_reports_it(broken_copy):
    # The bug from the first landmarks draft: the same key written twice.
    (broken_copy / "landmarks.json").write_text(
        '{"schemaVersion": "0.1", "regionId": "sample", "regionId": "sample", "landmarks": []}'
    )
    problems = vm.validate_folder(broken_copy)
    assert any("duplicate key" in p for p in problems), problems

def test_landmark_series_may_be_omitted(broken_copy):
    edit_json(broken_copy, "landmarks.json", lambda doc: doc["landmarks"][0].pop("series"))
    assert vm.validate_folder(broken_copy) == []
