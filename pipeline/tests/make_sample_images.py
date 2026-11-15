"""Make tiny SYNTHETIC placeholder images for app/public/data/sample/.

Written by Zainab with AI assistance (Claude Code). See docs/AI_USAGE.md.
These are math patterns, not NASA data and not AI imagery. They exist so the
front end has real image files to load before the pipeline makes real ones.

Run from the repo root:
    .venv/bin/python pipeline/tests/make_sample_images.py
"""

from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path("app/public/data/sample/layers")
SIZE = 256                              # pixels per side, keeps files tiny
DATE_SEEDS = {"2026-10-13": 1}


# makes a grid of x/y positions from 0 to 1, runs them through sines and cosine to get the smooth waves
# then rescales the results to the range 0 to 1. Changing the seed shifts the waves.
def pattern(seed):
    #A smooth pattern of values from 0 to 1. A different seed gives a different picture.
    y, x = np.mgrid[0:SIZE, 0:SIZE] / SIZE
    z = np.sin(6 * x + seed) * np.cos(5 * y - seed)
    return (z - z.min()) / (z.max() - z.min())


# the save function adds a 4th channel, alpha(transparency). Alpha 0 in the top-left corner.
# The data data contract says pixels with no data must be transparent, so this test that the map handles it.
def save(rgb, path):
    #Save an RGB array as WebP, with the top-left corner transparent ("no data").
    y, x = np.mgrid[0:SIZE, 0:SIZE]
    alpha = np.where(x + y > SIZE // 3, 255, 0)
    rgba = np.dstack([rgb, alpha]).astype(np.uint8)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(path, "WEBP")
    print(path)


# for each date, a grey HH image (the same values in R, G, B), a gray HV image and a colour
# cmposite, using the same colour scheme the plan uses for real data.
for date, i in DATE_SEEDS.items():
    hh = pattern(seed=i)
    hv = pattern(seed=i + 2)
    save(np.dstack([hh, hh, hh]) * 255, OUT / "gcov_hh" / f"{date}.webp")
    save(np.dstack([hv, hv, hv]) * 255, OUT / "gcov_hv" / f"{date}.webp")
    # Composite as in PLAN section 7: red = HH, green = HV, blue = HH minus HV
    blue = np.clip(hh - hv + 0.5, 0, 1)
    save(np.dstack([hh, hv, blue]) * 255, OUT / "gcov_composite" / f"{date}.webp")
