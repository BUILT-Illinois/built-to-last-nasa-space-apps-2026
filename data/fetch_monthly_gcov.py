"""Cache the T-33 frequency-B crops. Drafted with AI assistance (Codex).

From the repository root, use the pipeline Python environment to run
`python data/fetch_monthly_gcov.py`. Completed crops stay in data/interim/.
"""

import argparse
import sys
from pathlib import Path
from time import monotonic, strftime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import fetch_crops

def log(message):
    print(f"{strftime('%H:%M:%S')} {message}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", default="mexico_city")
    region = parser.parse_args().region
    output = fetch_crops.OUTPUT_DIR
    fetch_crops.clean_stale_temps(output)
    try:
        dates = fetch_crops.monthly_dates(region)
        for day in dates:
            fetch_crops.find_granule(region, "GCOV", day)
    except ValueError as error:
        parser.error(str(error))

    start = monotonic()
    skipped = downloaded = 0
    failures = []
    for index, day in enumerate(dates, start=1):
        prefix = f"[{index}/{len(dates)}] {day}"
        destination = fetch_crops.output_path(region, "GCOV", day)
        if destination.is_file():
            skipped += 1
            log(f"{prefix} SKIP cached")
            continue
        log(f"{prefix} FETCH")
        if fetch_crops.fetch_bounded(region, "GCOV", day):
            downloaded += 1
        else:
            failures.append(day)
    log(f"Finished in {monotonic() - start:.0f}s: {downloaded} fetched, {skipped} cached, "
        f"{len(failures)} failed")
    if failures:
        log(f"Failed dates: {', '.join(failures)}")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
