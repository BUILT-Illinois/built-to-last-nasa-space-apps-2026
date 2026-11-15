"""Wet-day water vs sinking ground, from NISAR GCOV frequency A (10 m) and the line-of-sight rate (exploratory, AI-assisted).

Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md.
Usage: python flood_vs_sinking.py <gcovA_dir> <rate_tif> <rain_json> <out_dir>

1. Open water per date: HH below -15 dB at 40 m (4 x 4 looks). Calm open water is dark at L-band.
2. Wet-day change: per pixel, (a) new open water, and (b) HH brightening of 3 dB or more, relative to the
   median of the dry dates (Nov to Apr). (b) is how flooded vegetation and soaked ground usually show at L-band.
3. Compare where (a) and (b) happen against the line-of-sight sinking rate (positive = away = sinking, D-19).
Rain: Open-Meteo archive (reanalysis, about 10 km cells), days before the 6:05 AM local pass.
"""
import glob, json, os, sys, datetime as dt
import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC, RATE, RAIN, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
LOOK, WATER_DB, BRIGHT_DB = 4, -15.0, 3.0

files = sorted(glob.glob(os.path.join(SRC, "gcovA_*.npz")))
dates = [os.path.basename(f)[6:16] for f in files]
z = np.load(files[0])
x, y, epsg = z["xCoordinates"], z["yCoordinates"], int(z["projection"])
H, W = z["HHHH"].shape
h, w = H // LOOK, W // LOOK


def ml(a):
    a = np.where(np.isfinite(a) & (a > 0), a, np.nan)[: h * LOOK, : w * LOOK]
    return np.nanmean(a.reshape(h, LOOK, w, LOOK), axis=(1, 3))


HH = np.stack([10 * np.log10(ml(np.load(f)["HHHH"])) for f in files])
xl = x[0] + 10 * (LOOK - 1) / 2 + np.arange(w) * 10 * LOOK
yl = y[0] - 10 * (LOOK - 1) / 2 - np.arange(h) * 10 * LOOK

# Rate raster (80 m, same UTM zone) sampled at the 40 m pixel centres.
with rasterio.open(RATE) as r:
    assert r.crs.to_epsg() == epsg, (r.crs, epsg)
    rate_full = r.read(1).astype(np.float32)
    nod = r.nodata
    rows, cols = rasterio.transform.rowcol(r.transform, np.repeat(xl[None, :], h, 0), np.repeat(yl[:, None], w, 1))
rows, cols = np.asarray(rows).reshape(h, w), np.asarray(cols).reshape(h, w)
ok = (rows >= 0) & (rows < rate_full.shape[0]) & (cols >= 0) & (cols < rate_full.shape[1])
rate = np.full((h, w), np.nan, np.float32)
rate[ok] = rate_full[rows[ok], cols[ok]]
if nod is not None:
    rate[rate == nod] = np.nan
rate[np.abs(rate) > 50] = np.nan  # same mask as the published layer

rain = json.load(open(RAIN))
rmap = dict(zip(rain["daily"]["time"], rain["daily"]["precipitation_sum"]))
D = [dt.date.fromisoformat(d) for d in dates]
rain3 = np.array([sum((rmap.get((d - dt.timedelta(days=k)).isoformat()) or 0) for k in (1, 2, 3)) for d in D])
dry = np.array([d.month in (11, 12, 1, 2, 3, 4) for d in D])

base = np.nanmedian(HH[dry], axis=0)
base_water = base < WATER_DB
water = HH < WATER_DB
water_km2 = water.sum(axis=(1, 2)) * (10 * LOOK) ** 2 / 1e6
new_water = water & ~base_water
bright = (HH - base) >= BRIGHT_DB
new_water_km2 = new_water.sum(axis=(1, 2)) * (10 * LOOK) ** 2 / 1e6
bright_km2 = bright.sum(axis=(1, 2)) * (10 * LOOK) ** 2 / 1e6

# Sinking classes (cm/yr, line of sight)
classes = [("stable (< 2)", -99, 2), ("2 to 10", 2, 10), ("10 to 20", 10, 20), ("> 20", 20, 99)]
valid = np.isfinite(rate) & ~base_water
wet = ~dry
freq_new_water = new_water[wet].mean(axis=0)
freq_bright = bright[wet].mean(axis=0)
freq_new_water_dry = new_water[dry].mean(axis=0)
freq_bright_dry = bright[dry].mean(axis=0)
table = []
for name, lo, hi in classes:
    m = valid & (rate >= lo) & (rate < hi)
    table.append({"class_cm_per_yr": name, "area_km2": float(m.sum() * 0.0016),
                  "new_water_wet_pct": float(100 * np.mean(freq_new_water[m])),
                  "new_water_dry_pct": float(100 * np.mean(freq_new_water_dry[m])),
                  "brightening_wet_pct": float(100 * np.mean(freq_bright[m])),
                  "brightening_dry_pct": float(100 * np.mean(freq_bright_dry[m]))})

# Figure 1: water area per date and rain
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.bar(D, rain3, width=6, color="#9ecae1", label="rain in the 3 days before the pass, mm (Open-Meteo)")
ax.set_ylabel("rain, mm")
a2 = ax.twinx()
a2.plot(D, water_km2, "o-", color="#08519c", label="open water, km2 (HH < -15 dB)")
a2.plot(D, bright_km2, "s-", color="#b35806", ms=4, label="HH brightened >= 3 dB vs dry median, km2")
a2.set_ylabel("km2")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
ax.set_title("South-east Mexico City (Xochimilco, Tlahuac, Chalco), NISAR GCOV 10 m averaged to 40 m, PROVISIONAL")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "fig_water_area_vs_rain.png"), dpi=90)

# Figure 2: maps
ext = [xl[0], xl[-1], yl[-1], yl[0]]
fig, ax = plt.subplots(1, 3, figsize=(17, 6))
im0 = ax[0].imshow(rate, cmap="RdBu_r", vmin=-30, vmax=30, extent=ext)
ax[0].set_title("Line-of-sight rate, cm/yr (red = sinking)")
plt.colorbar(im0, ax=ax[0], shrink=0.7)
im1 = ax[1].imshow(np.where(base_water, np.nan, freq_bright * 100), cmap="magma", vmin=0, vmax=60, extent=ext)
ax[1].contour(xl, yl, np.nan_to_num(rate), levels=[10], colors="cyan", linewidths=0.8)
ax[1].set_title("% of rainy-season dates with HH brightening >= 3 dB\n(cyan: sinking 10 cm/yr contour)")
plt.colorbar(im1, ax=ax[1], shrink=0.7)
im2 = ax[2].imshow(np.where(base_water, 1, np.nan), cmap="Blues", vmin=0, vmax=1.2, extent=ext)
ax[2].imshow(np.where(freq_new_water > 0.25, 1, np.nan), cmap="autumn", vmin=0, vmax=1, extent=ext)
ax[2].contour(xl, yl, np.nan_to_num(rate), levels=[10], colors="k", linewidths=0.8)
ax[2].set_title("Blue: dry-season open water. Orange: new open water on > 25% of\nrainy-season dates. Black: sinking 10 cm/yr contour")
for a in ax:
    a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(os.path.join(OUT, "fig_wet_change_vs_sinking.png"), dpi=80)

json.dump({"dates": dates, "rain_3day_mm": rain3.tolist(), "open_water_km2": water_km2.tolist(),
           "new_water_km2": new_water_km2.tolist(), "brightened_km2": bright_km2.tolist(),
           "dry_baseline_water_km2": float(base_water.sum() * 0.0016), "by_sinking_class": table},
          open(os.path.join(OUT, "flood_vs_sinking.json"), "w"), indent=1)
print("dry-baseline open water km2: %.2f" % (base_water.sum() * 0.0016))
for d, r3, wk, nk, bk in zip(dates, rain3, water_km2, new_water_km2, bright_km2):
    print(f"{d} rain3 {r3:5.1f} mm  water {wk:6.2f} km2  new {nk:5.2f}  bright {bk:6.2f}")
for t in table:
    print(t)
