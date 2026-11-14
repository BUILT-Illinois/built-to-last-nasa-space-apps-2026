"""Check a region data folder against docs/DATA_CONTRACT.md.

Usage (from the repo root):
    .venv/bin/python pipeline/validate_manifest.py app/public/data/sample

Exits 0 when the folder follows the contract, 1 and a list of problems otherwise.
Owner: Zainab. Written with AI assistance (Claude Code) and reviewed by Zainab.
See docs/AI_USAGE.md.

Every check returns a list of problem strings. An empty list means "OK".
Each problem says WHERE it is (for example "layers[0].frames[1].date") so the
person fixing it can find it fast.
"""


import datetime
import json
import re
import sys
from pathlib import Path

LAYER_KINDS = {"backscatter", "composite", "change", "displacement", "soil_moisture"}
POLARIZATIONS = {"HH", "HV", "HH+HV", None}
MAX_IMAGE_BYTES = 1_000_000        # each image under 1 MB
MAX_FOLDER_BYTES = 60_000_000      # each region folder under 60 MB

MANIFEST_FIELDS = ["schemaVersion", "generatedAt", "generatedBy", "region", "dataMaturity", "layers", "sources"]
REGION_FIELDS = ["id", "name", "bbox", "center", "zoom"]
LAYER_FIELDS = ["id", "title", "kind", "product", "polarization", "units", "bounds", "colormap",
                "description", "caveats", "frames"]
FRAME_FIELDS = ["date", "image", "granules", "track", "frame", "direction"]
LANDMARK_FIELDS = ["id", "name", "lon", "lat", "summary", "radarShows", "weInfer", "drivers", "sourceIds"]


# --------------------------------------------------------------------------
# The four small checks. Each returns a list of problems ([] means OK).
# Test with:  .venv/bin/python -m pytest pipeline/tests/test_validate.py -v
# --------------------------------------------------------------------------

def check_bbox(bbox, where: str) -> list[str]:
    """EXERCISE 1. A bbox is [west, south, east, north] in WGS84 degrees.

    Return a list with a problem string when:
      - it is not a list of exactly 4 numbers
      - west/east are outside -180..180, or south/north outside -90..90
      - west >= east, or south >= north   (this catches a swapped order)
    Return [] when it is fine.
    Every problem string must start with `where`, e.g. f"{where}: west must be less than east"
    """
    is_number = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    if not (isinstance(bbox, list) and len(bbox) == 4 and all(is_number(v) for v in bbox)):
        return [f"{where}: must be a list of 4 numbers [west, south, east, north]"]

    west, south, east, north = bbox
    problems = []
    if not (-180 <= west <= 180 and -180 <= east <= 180 and -90 <= south <= 90 and -90 <= north <= 90):
        problems.append(f"{where}: values out of range (did you swap lon and lat?)")
    if west >= east:
        problems.append(f"{where}: west must be less than east")
    if south >= north:
        problems.append(f"{where}: south must be less than north")
    return problems


def check_date(value, where: str) -> list[str]:
    """EXERCISE 2. Dates must be strings 'YYYY-MM-DD' AND a real calendar day.

    '2026-04-16' is fine. '2026-4-16', '16/04/2026', '2026-02-30', 20260416, None are not.
    Hint: re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", value) checks the shape;
          datetime.date.fromisoformat(value) raises ValueError if the day is not real.
    """
    if not (isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)):
        return [f"{where}: '{value}' is not a YYYY-MM-DD date"]
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return [f"{where}: '{value}' is not a real calendar day"]
    return []


def check_files_exist(manifest: dict, folder: Path) -> list[str]:
    """EXERCISE 3. Every layers[].frames[].image and vectors[].file must exist.

    Paths are relative to `folder` (the folder that holds manifest.json): folder / path.
    Return one problem per missing file, and include the file path in the message.
    `vectors` is optional: use manifest.get("vectors", []).
    """
    problems = []
    for i, layer in enumerate(manifest.get("layers", [])):
        for j, frame in enumerate(layer.get("frames", [])):
            if not (folder / frame["image"]).exists():
                problems.append(f"layers[{i}].frames[{j}].image: file not found: {frame['image']}")
    for k, vector in enumerate(manifest.get("vectors", [])):
        if not (folder / vector["file"]).exists():
            problems.append(f"vectors[{k}].file: file not found: {vector['file']}")
    return problems


def check_size_budget(manifest: dict, folder: Path) -> list[str]:
    """EXERCISE 4. Each frame image under MAX_IMAGE_BYTES, and the whole folder
    (every file inside it, recursively) under MAX_FOLDER_BYTES.

    Skip images that do not exist (check_files_exist already reports those).
    Include the image path in the message for a too-big image.
    Hint: path.stat().st_size gives bytes; folder.rglob("*") lists everything inside.
    """
    problems = []
    for layer in manifest.get("layers", []):
        for frame in layer.get("frames", []):
            image = folder / frame["image"]
            if image.exists() and image.stat().st_size > MAX_IMAGE_BYTES:
                problems.append(f"{frame['image']}: image is over 1 MB")

    total = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
    if total > MAX_FOLDER_BYTES:
        problems.append(f"{folder}: folder is {total / 1e6:.1f} MB, over the 60 MB budget")
    return problems


# --------------------------------------------------------------------------
# Plumbing (already done). Read it, and be ready to explain it back.
# --------------------------------------------------------------------------

def missing_fields(obj, fields: list[str], where: str) -> list[str]:
    if not isinstance(obj, dict):
        return [f"{where}: expected an object"]
    return [f"{where}: missing field '{f}'" for f in fields if f not in obj]


def check_manifest(manifest: dict, folder: Path) -> list[str]:
    problems = missing_fields(manifest, MANIFEST_FIELDS, "manifest")
    if problems:
        return problems  # structure is too broken to check further

    region = manifest["region"]
    problems += missing_fields(region, REGION_FIELDS, "region")
    if isinstance(region, dict) and "bbox" in region:
        problems += check_bbox(region["bbox"], "region.bbox")

    source_ids = {s.get("id") for s in manifest["sources"] if isinstance(s, dict)}

    for i, layer in enumerate(manifest["layers"]):
        at = f"layers[{i}]"
        layer_problems = missing_fields(layer, LAYER_FIELDS, at)
        problems += layer_problems
        if layer_problems:
            continue
        if layer["kind"] not in LAYER_KINDS:
            problems.append(f"{at}.kind: '{layer['kind']}' is not one of {sorted(LAYER_KINDS)}")
        if layer["polarization"] not in POLARIZATIONS:
            problems.append(f"{at}.polarization: '{layer['polarization']}' is not allowed")
        problems += check_bbox(layer["bounds"], f"{at}.bounds")
        cmap = layer["colormap"]
        if not (isinstance(cmap, dict) and cmap.get("min") is not None and cmap.get("max") is not None
                and cmap["min"] < cmap["max"]):
            problems.append(f"{at}.colormap: needs name, and min < max")
        if not layer["frames"]:
            problems.append(f"{at}.frames: a layer needs at least one frame")
        for j, frame in enumerate(layer["frames"]):
            fat = f"{at}.frames[{j}]"
            frame_problems = missing_fields(frame, FRAME_FIELDS, fat)
            problems += frame_problems
            if frame_problems:
                continue
            problems += check_date(frame["date"], f"{fat}.date")
            if layer["kind"] == "displacement":
                problems += check_date(frame.get("since"), f"{fat}.since")
            if not frame["granules"]:
                problems.append(f"{fat}.granules: list the source granule names")

    for k, vec in enumerate(manifest.get("vectors", [])):
        problems += missing_fields(vec, ["id", "title", "file", "source"], f"vectors[{k}]")
        if isinstance(vec, dict) and vec.get("source") not in source_ids:
            problems.append(f"vectors[{k}].source: '{vec.get('source')}' is not an id in sources[]")

    problems += check_files_exist(manifest, folder)
    problems += check_size_budget(manifest, folder)
    return problems


def check_landmarks(landmarks: dict, region_id: str, source_ids: set) -> list[str]:
    problems = missing_fields(landmarks, ["schemaVersion", "regionId", "landmarks"], "landmarks.json")
    if problems:
        return problems
    if landmarks["regionId"] != region_id:
        problems.append(f"landmarks.json regionId '{landmarks['regionId']}' != manifest region.id '{region_id}'")
    seen = set()
    for i, lm in enumerate(landmarks["landmarks"]):
        at = f"landmarks[{i}]"
        lm_problems = missing_fields(lm, LANDMARK_FIELDS, at)
        problems += lm_problems
        if lm_problems:
            continue
        if lm["id"] in seen:
            problems.append(f"{at}.id: duplicate id '{lm['id']}'")
        seen.add(lm["id"])
        if not (-180 <= lm["lon"] <= 180 and -90 <= lm["lat"] <= 90):
            problems.append(f"{at}: lon/lat out of range (did you swap them?)")
        for sid in lm["sourceIds"]:
            if sid not in source_ids:
                problems.append(f"{at}.sourceIds: '{sid}' is not an id in manifest sources[]")
        for name, points in lm.get("series", {}).items():
            for p, point in enumerate(points):
                problems += check_date(point.get("date"), f"{at}.series.{name}[{p}].date")
                if "value" not in point:
                    problems.append(f"{at}.series.{name}[{p}]: missing 'value' (use null for no data)")
    return problems


def load_json(path: Path) -> tuple[dict | None, list[str]]:
    """Read a JSON file. Duplicate keys are an error (JSON would silently keep only the last one)."""
    if not path.exists():
        return None, [f"{path.name}: file not found"]

    def no_duplicates(pairs):
        keys = [k for k, _ in pairs]
        dupes = sorted({k for k in keys if keys.count(k) > 1})
        if dupes:
            raise ValueError(f"duplicate key(s) {dupes}")
        return dict(pairs)

    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates), []
    except ValueError as e:  # JSONDecodeError is a ValueError too
        return None, [f"{path.name}: not valid JSON ({e})"]


def validate_folder(folder: Path) -> list[str]:
    folder = Path(folder)
    manifest, problems = load_json(folder / "manifest.json")
    if manifest is None:
        return problems
    problems += check_manifest(manifest, folder)

    landmarks, lm_load = load_json(folder / "landmarks.json")
    problems += lm_load
    if landmarks is not None and isinstance(manifest.get("region"), dict):
        source_ids = {s.get("id") for s in manifest.get("sources", []) if isinstance(s, dict)}
        problems += check_landmarks(landmarks, manifest["region"].get("id"), source_ids)
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python pipeline/validate_manifest.py <region data folder>")
        return 2
    problems = validate_folder(Path(argv[1]))
    if problems:
        print(f"FAIL: {len(problems)} problem(s) in {argv[1]}")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"OK: {argv[1]} follows the data contract")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
