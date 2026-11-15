"""Windowed remote reads of NISAR GCOV frequency A (10 m) for the chinampas box (AI-assisted, see docs/AI_USAGE.md).

Usage: NETRC=~/.netrc python fetch_full_res_crops.py pipeline data/Mexico_City [YYYY-MM-DD ...]
"""
import sys, glob, os, time, numpy as np
sys.path.insert(0, sys.argv[1])  # pipeline dir
import earthaccess
from fetch_crops import read_with_retries, publish_crop
from quicklook import GCOV_GRIDS
from pathlib import Path
SRC = Path(sys.argv[2]); OUT = SRC / "gcov_freqA_chinampas"; OUT.mkdir(exist_ok=True)
BBOX = [-99.23, 19.06, -98.87, 19.40]
EXCL = {"2025-12-05", "2026-04-16"}
only = sys.argv[3:]  # optional dates
import csv
rows = {r["scene_name"]: r for r in csv.DictReader(open(Path(sys.argv[1]) / "reports" / "granules_mexico_city.csv", encoding="utf-8"))}
assert earthaccess.login(strategy="netrc").authenticated
session = earthaccess.get_fsspec_https_session()
for f in sorted(glob.glob(str(SRC / "mexico_city_gcov_*.npz"))):
    day = f[-14:-4]
    if day in EXCL or (only and day not in only): continue
    out = OUT / f"gcovA_{day}.npz"
    if out.exists(): print("skip", day, flush=True); continue
    g = str(np.load(f)["granule"])
    url = rows[g]["url"]
    t = time.time()
    crop = read_with_retries(session, url, GCOV_GRIDS.format(freq="A"), ("HHHH", "HVHV"), BBOX)
    publish_crop(out, crop, g)
    dx = np.diff(crop["xCoordinates"][:2])[0]
    print(day, crop["HHHH"].shape, f"spacing {dx:.1f} m", f"{out.stat().st_size/1e6:.0f} MB", f"{time.time()-t:.0f}s", flush=True)
