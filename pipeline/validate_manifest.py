"""Check a region data folder against docs/DATA_CONTRACT.md and app/src/types/manifest.ts.

Usage (from the repo root):
    .venv/bin/python pipeline/validate_manifest.py app/public/data/sample

Exits 0 when the folder follows the contract, 1 and a list of problems otherwise.
Owner: Zainab. Written with AI assistance (Claude Code) and reviewed by Zainab.
See docs/AI_USAGE.md.

Every check returns a list of problem strings. An empty list means "OK".
Each problem says WHERE it is (for example "layers[0].frames[1].date").
Broken input is reported as a problem, never as a Python crash: every check
confirms a value is a list or an object before looking inside it.
"""

import datetime
import json
import re
import sys
from pathlib import Path

LAYER_KINDS = {"backscatter", "composite", "change", "displacement", "soil_moisture"}
POLARIZATIONS = {"HH", "HV", "HH+HV", None}
DIRECTIONS = {"ASCENDING", "DESCENDING"}
MAX_IMAGE_BYTES = 1_000_000        # each image under 1 MB
MAX_FOLDER_BYTES = 60_000_000      # each region folder under 60 MB

MANIFEST_FIELDS = ["schemaVersion", "generatedAt", "generatedBy", "region", "dataMaturity",
                   "layers", "vectors", "sources"]
REGION_FIELDS = ["id", "name", "bbox", "center", "zoom"]
LAYER_FIELDS = ["id", "title", "kind", "product", "polarization", "units", "bounds", "colormap",
                "description", "caveats", "frames"]
FRAME_FIELDS = ["date", "image", "granules", "track", "frame", "direction"]
VECTOR_FIELDS = ["id", "title", "file", "source"]
LANDMARK_FIELDS = ["id", "name", "lon", "lat", "summary", "radarShows", "weInfer", "drivers",
                   "sourceIds"]


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def is_number(value) -> bool:
    """True for int or float. (bool counts as int in Python, so exclude it.)"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def missing_fields(obj, fields: list[str], where: str) -> list[str]:
    if not isinstance(obj, dict):
        return [f"{where}: expected an object"]
    return [f"{where}: missing field '{f}'" for f in fields if f not in obj]


def each_frame(manifest: dict):
    """Yield (where, frame) for every frame that is an object. Skips broken entries."""
    layers = manifest.get("layers")
    for i, layer in enumerate(layers if isinstance(layers, list) else []):
        frames = layer.get("frames") if isinstance(layer, dict) else None
        for j, frame in enumerate(frames if isinstance(frames, list) else []):
            if isinstance(frame, dict):
                yield f"layers[{i}].frames[{j}]", frame


# --------------------------------------------------------------------------
# Value checks
# --------------------------------------------------------------------------

def check_bbox(bbox, where: str) -> list[str]:
    """A bbox is [west, south, east, north] in WGS84 degrees."""
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
    """Dates must be strings 'YYYY-MM-DD' AND a real calendar day."""
    if not (isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)):
        return [f"{where}: '{value}' is not a YYYY-MM-DD date"]
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return [f"{where}: '{value}' is not a real calendar day"]
    return []


def check_path(path, folder: Path, suffix: str, where: str) -> list[str]:
    """A data file path must stay inside the region folder, have the right suffix, and exist."""
    if not (isinstance(path, str) and path):
        return [f"{where}: must be a relative file path"]
    full = (folder / path).resolve()
    if not full.is_relative_to(folder.resolve()):
        return [f"{where}: '{path}' points outside the region folder"]
    if full.suffix != suffix:
        return [f"{where}: '{path}' must be a {suffix} file"]
    if not full.is_file():
        return [f"{where}: file not found: {path}"]
    return []


def check_colormap(cmap, where: str) -> list[str]:
    if not isinstance(cmap, dict):
        return [f"{where}: expected an object"]
    problems = []
    if not (isinstance(cmap.get("name"), str) and cmap["name"]):
        problems.append(f"{where}.name: must be a non-empty string")
    low, high = cmap.get("min"), cmap.get("max")
    if not (is_number(low) and is_number(high) and low < high):
        problems.append(f"{where}: min and max must be numbers with min < max")
    return problems


def check_series(series, where: str) -> list[str]:
    """series is an object like {"hh_db": [{"date": ..., "value": number or null}, ...]}."""
    if not isinstance(series, dict):
        return [f"{where}: expected an object of named series"]
    problems = []
    for name, points in series.items():
        if name == "water_months":
            if not (
                isinstance(points, dict)
                and type(points.get("count")) is int
                and type(points.get("valid_months")) is int
                and 0 <= points["count"] <= points["valid_months"] <= 12
                and points["valid_months"] > 0
                and points.get("provisional") is True
            ):
                problems.append(f"{where}.{name}: expected a provisional count within valid months")
            continue
        if not isinstance(points, list):
            problems.append(f"{where}.{name}: must be a list")
            continue
        for p, point in enumerate(points):
            at = f"{where}.{name}[{p}]"
            if not isinstance(point, dict):
                problems.append(f"{at}: expected an object with date and value")
                continue
            problems += check_date(point.get("date"), f"{at}.date")
            if "value" not in point:
                problems.append(f"{at}: missing 'value' (use null for no data)")
            elif point["value"] is not None and not is_number(point["value"]):
                problems.append(f"{at}.value: must be a number or null")
    return problems


# --------------------------------------------------------------------------
# File checks
# --------------------------------------------------------------------------

def check_files_exist(manifest: dict, folder: Path) -> list[str]:
    """Every frame image (.webp) and vector file (.geojson) must exist inside the folder.
    Entries with a missing key are skipped here; check_manifest reports them."""
    problems = []
    for where, frame in each_frame(manifest):
        if "image" in frame:
            problems += check_path(frame["image"], folder, ".webp", f"{where}.image")
    vectors = manifest.get("vectors")
    for k, vector in enumerate(vectors if isinstance(vectors, list) else []):
        if isinstance(vector, dict) and "file" in vector:
            problems += check_path(vector["file"], folder, ".geojson", f"vectors[{k}].file")
    return problems


def check_size_budget(manifest: dict, folder: Path) -> list[str]:
    """Each frame image under MAX_IMAGE_BYTES; the whole folder under MAX_FOLDER_BYTES."""
    problems = []
    for where, frame in each_frame(manifest):
        image = folder / str(frame.get("image", ""))
        if image.is_file() and image.stat().st_size > MAX_IMAGE_BYTES:
            problems.append(f"{where}.image: {frame['image']} is over {MAX_IMAGE_BYTES / 1e6:g} MB")

    total = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
    if total > MAX_FOLDER_BYTES:
        problems.append(f"{folder}: folder is {total / 1e6:g} MB, over the {MAX_FOLDER_BYTES / 1e6:g} MB budget")
    return problems


# --------------------------------------------------------------------------
# manifest.json
# --------------------------------------------------------------------------

def check_region(region) -> list[str]:
    problems = missing_fields(region, REGION_FIELDS, "region")
    if problems:
        return problems
    bbox_problems = check_bbox(region["bbox"], "region.bbox")
    problems += bbox_problems

    center = region["center"]
    if not (isinstance(center, list) and len(center) == 2 and all(is_number(v) for v in center)):
        problems.append("region.center: must be [lon, lat]")
    elif not bbox_problems:
        west, south, east, north = region["bbox"]
        lon, lat = center
        if not (west <= lon <= east and south <= lat <= north):
            problems.append("region.center: [lon, lat] is outside region.bbox (swapped?)")

    if not is_number(region["zoom"]):
        problems.append("region.zoom: must be a number")
    return problems


def check_frame(frame, kind: str, where: str, synthetic: bool = False) -> list[str]:
    problems = missing_fields(frame, FRAME_FIELDS, where)
    if problems:
        return problems
    problems += check_date(frame["date"], f"{where}.date")
    if kind == "displacement":
        problems += check_date(frame.get("since"), f"{where}.since")
    if not isinstance(frame["granules"], list) or (not frame["granules"] and not synthetic):
        problems.append(f"{where}.granules: list the source granule names (empty only when synthetic)")
    if frame["direction"] not in DIRECTIONS:
        problems.append(f"{where}.direction: '{frame['direction']}' is not one of {sorted(DIRECTIONS)}")
    for key in ("track", "frame"):
        if not (isinstance(frame[key], int) and not isinstance(frame[key], bool)):
            problems.append(f"{where}.{key}: must be a whole number")
    return problems


def check_layer(layer, where: str, synthetic: bool = False) -> list[str]:
    problems = missing_fields(layer, LAYER_FIELDS, where)
    if problems:
        return problems
    if layer["kind"] not in LAYER_KINDS:
        problems.append(f"{where}.kind: '{layer['kind']}' is not one of {sorted(LAYER_KINDS)}")
    if layer["polarization"] not in POLARIZATIONS:
        problems.append(f"{where}.polarization: '{layer['polarization']}' is not allowed")
    problems += check_bbox(layer["bounds"], f"{where}.bounds")
    problems += check_colormap(layer["colormap"], f"{where}.colormap")

    frames = layer["frames"]
    if not (isinstance(frames, list) and frames):
        return problems + [f"{where}.frames: must be a non-empty list"]
    for j, frame in enumerate(frames):
        problems += check_frame(frame, layer["kind"], f"{where}.frames[{j}]", synthetic)
    return problems


def check_manifest(manifest, folder: Path) -> list[str]:
    problems = missing_fields(manifest, MANIFEST_FIELDS, "manifest")
    if problems:
        return problems  # structure is too broken to check further
    for key in ("layers", "vectors", "sources"):
        if not isinstance(manifest[key], list):
            problems.append(f"manifest.{key}: must be a list")
    if problems:
        return problems

    problems += check_region(manifest["region"])
    if "synthetic" in manifest and not isinstance(manifest["synthetic"], bool):
        problems.append("manifest.synthetic: must be true or false")
    for i, layer in enumerate(manifest["layers"]):
        problems += check_layer(layer, f"layers[{i}]", manifest.get("synthetic") is True)

    source_ids = {s.get("id") for s in manifest["sources"] if isinstance(s, dict)}
    for k, vector in enumerate(manifest["vectors"]):
        vector_problems = missing_fields(vector, VECTOR_FIELDS, f"vectors[{k}]")
        problems += vector_problems
        if not vector_problems and vector["source"] not in source_ids:
            problems.append(f"vectors[{k}].source: '{vector['source']}' is not an id in sources[]")

    problems += check_files_exist(manifest, folder)
    problems += check_size_budget(manifest, folder)
    return problems


# --------------------------------------------------------------------------
# landmarks.json
# --------------------------------------------------------------------------

def check_landmarks(landmarks, region_id, source_ids: set) -> list[str]:
    problems = missing_fields(landmarks, ["schemaVersion", "regionId", "landmarks"], "landmarks.json")
    if problems:
        return problems
    if not isinstance(landmarks["landmarks"], list):
        return ["landmarks.json landmarks: must be a list"]
    if landmarks["regionId"] != region_id:
        problems.append(f"landmarks.json regionId '{landmarks['regionId']}' != manifest region.id '{region_id}'")

    seen = set()
    for i, landmark in enumerate(landmarks["landmarks"]):
        at = f"landmarks[{i}]"
        landmark_problems = missing_fields(landmark, LANDMARK_FIELDS, at)
        problems += landmark_problems
        if landmark_problems:
            continue
        if landmark["id"] in seen:
            problems.append(f"{at}.id: duplicate id '{landmark['id']}'")
        seen.add(landmark["id"])

        lon, lat = landmark["lon"], landmark["lat"]
        if not (is_number(lon) and is_number(lat)):
            problems.append(f"{at}: lon and lat must be numbers")
        elif not (-180 <= lon <= 180 and -90 <= lat <= 90):
            problems.append(f"{at}: lon/lat out of range (did you swap them?)")

        if not isinstance(landmark["sourceIds"], list):
            problems.append(f"{at}.sourceIds: must be a list")
        else:
            for sid in landmark["sourceIds"]:
                if sid not in source_ids:
                    problems.append(f"{at}.sourceIds: '{sid}' is not an id in manifest sources[]")

        if "series" in landmark:
            problems += check_series(landmark["series"], f"{at}.series")
    return problems


# --------------------------------------------------------------------------
# Whole folder and command line
# --------------------------------------------------------------------------

def load_json(path: Path):
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


def validate_folder(folder) -> list[str]:
    folder = Path(folder)
    manifest, problems = load_json(folder / "manifest.json")
    if manifest is None:
        return problems
    problems += check_manifest(manifest, folder)

    landmarks, load_problems = load_json(folder / "landmarks.json")
    problems += load_problems
    if landmarks is not None and isinstance(manifest, dict):
        region = manifest.get("region")
        region_id = region.get("id") if isinstance(region, dict) else None
        sources = manifest.get("sources")
        source_ids = {s.get("id") for s in sources if isinstance(s, dict)} if isinstance(sources, list) else set()
        problems += check_landmarks(landmarks, region_id, source_ids)
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
