"""Cache the T-33 frequency-B crops. Drafted with AI assistance (Codex).

From the repository root, use the pipeline Python environment to run
`python data/fetch_monthly_gcov.py`. Completed crops stay in data/interim/.
"""

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from time import monotonic, strftime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import fetch_crops

REGION = "mexico_city"
SCENE_TIMEOUT_SECONDS = 120
DATES = (
    "2025-11-11", "2025-12-17", "2026-01-10", "2026-02-15",
    "2026-03-11", "2026-04-16", "2026-05-10", "2026-06-15",
    "2026-07-09", "2026-08-14", "2026-09-19", "2026-10-13",
)


def log(message):
    print(f"{strftime('%H:%M:%S')} {message}", flush=True)


def fetch_one(day, staging):
    fetch_crops.OUTPUT_DIR = Path(staging)
    fetch_crops.fetch_crop(REGION, "GCOV", day)


def main():
    output = fetch_crops.OUTPUT_DIR
    output.mkdir(parents=True, exist_ok=True)
    for day in DATES:
        fetch_crops.find_granule(REGION, "GCOV", day)

    start = monotonic()
    skipped = downloaded = 0
    failures = []
    for index, day in enumerate(DATES, start=1):
        prefix = f"[{index}/{len(DATES)}] {day}"
        destination = output / f"{REGION}_gcov_{day}.npz"
        if destination.is_file():
            skipped += 1
            log(f"{prefix} SKIP cached")
            continue
        log(f"{prefix} FETCH")
        scene_start = monotonic()
        try:
            with TemporaryDirectory(dir=output, prefix=".monthly-gcov-") as staging:
                subprocess.run(
                    [sys.executable, __file__, "--fetch-one", day, staging],
                    check=True, timeout=SCENE_TIMEOUT_SECONDS,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                (Path(staging) / destination.name).replace(destination)
            downloaded += 1
            log(f"{prefix} DONE {destination.stat().st_size:,} bytes in {monotonic() - scene_start:.1f}s")
        except (subprocess.SubprocessError, OSError) as error:
            failures.append(day)
            log(f"{prefix} FAILED ({type(error).__name__})")
    log(f"Finished in {monotonic() - start:.0f}s: {downloaded} fetched, {skipped} cached, "
        f"{len(failures)} failed")
    if failures:
        log(f"Failed dates: {', '.join(failures)}")
    return bool(failures)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--fetch-one":
        fetch_one(sys.argv[2], sys.argv[3])
    else:
        sys.exit(main())
