"""Tests for pipeline/validate_manifest.py (T-08 part 2).

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


# ---- Exercise 1: check_bbox ------------------------------------------------

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


# ---- Exercise 2: check_date ------------------------------------------------

def test_date_good():
    assert vm.check_date("2026-04-16", "d") == []

@pytest.mark.parametrize("bad", ["2026-4-16", "16/04/2026", "2026-02-30", "2026-04-16T00:00:00Z", 20260416, None, ""])
def test_date_bad(bad):
    problems = vm.check_date(bad, "frames[0].date")
    assert problems, f"should reject {bad!r}"
    assert "frames[0].date" in problems[0]


# ---- Exercises 3 and 4 use a tiny manifest in a temporary folder -----------

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

def test_size_budget_image_too_big(tmp_path):
    (tmp_path / "big.webp").write_bytes(b"0" * (vm.MAX_IMAGE_BYTES + 1))
    problems = vm.check_size_budget(tiny_manifest(["big.webp"]), tmp_path)
    assert problems and "big.webp" in problems[0]

def test_size_budget_skips_missing_and_passes_small(tmp_path):
    (tmp_path / "small.webp").write_bytes(b"0" * 100)
    assert vm.check_size_budget(tiny_manifest(["small.webp", "gone.webp"]), tmp_path) == []

def test_size_budget_folder_too_big(tmp_path, monkeypatch):
    monkeypatch.setattr(vm, "MAX_FOLDER_BYTES", 500)
    (tmp_path / "a.bin").write_bytes(b"0" * 300)
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.bin").write_bytes(b"0" * 300)
    assert vm.check_size_budget(tiny_manifest([]), tmp_path), "600 bytes is over a 500 byte budget"


# ---- The real sample folder, and broken copies of it -----------------------

def test_sample_folder_passes():
    problems = vm.validate_folder(SAMPLE)
    assert problems == [], "\n".join(problems)

@pytest.fixture
def broken_copy(tmp_path):
    dst = tmp_path / "sample"
    shutil.copytree(SAMPLE, dst)
    return dst

def edit_manifest(folder, change):
    path = folder / "manifest.json"
    m = json.loads(path.read_text())
    change(m)
    path.write_text(json.dumps(m))

def test_broken_swapped_bbox_fails(broken_copy):
    def swap(m):
        w, s, e, n = m["region"]["bbox"]
        m["region"]["bbox"] = [s, w, n, e]
    edit_manifest(broken_copy, swap)
    assert vm.validate_folder(broken_copy)

def test_broken_missing_image_fails(broken_copy):
    m = json.loads((broken_copy / "manifest.json").read_text())
    (broken_copy / m["layers"][0]["frames"][0]["image"]).unlink()
    assert vm.validate_folder(broken_copy)

def test_broken_bad_date_fails(broken_copy):
    edit_manifest(broken_copy, lambda m: m["layers"][0]["frames"][0].update(date="16/04/2026"))
    assert vm.validate_folder(broken_copy)

def test_broken_unknown_kind_fails(broken_copy):
    edit_manifest(broken_copy, lambda m: m["layers"][0].update(kind="photo"))
    assert vm.validate_folder(broken_copy)

def test_broken_missing_field_fails(broken_copy):
    edit_manifest(broken_copy, lambda m: m.pop("sources"))
    assert vm.validate_folder(broken_copy)

def test_broken_duplicate_key_fails(broken_copy):
    # The bug from the first landmarks draft: the same key written twice.
    # Plain JSON would silently keep only the last one.
    (broken_copy / "landmarks.json").write_text(
        '{"schemaVersion": "0.1", "regionId": "sample", "regionId": "sample", "landmarks": []}'
    )
    assert vm.validate_folder(broken_copy)

def test_cli_exit_codes(broken_copy):
    assert vm.main(["x", str(SAMPLE)]) == 0
    (broken_copy / "manifest.json").write_text("{ not json")
    assert vm.main(["x", str(broken_copy)]) == 1
