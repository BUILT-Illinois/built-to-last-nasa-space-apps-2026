"""Chinampas vs farmland at full resolution (NISAR GCOV frequency A, 10 m), exploratory, AI-assisted.

Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md.
Usage: python analyze_freqA.py <crop_dir> <out_dir> <optical_png>
Same four boxes as the 80 m version. Adds what 10 m allows: a land-cover mask per pixel
(drops water and buildings), per-pixel seasonal range, and a count of growth cycles per pixel.
"""
import glob, json, os, sys, datetime as dt
import numpy as np
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

CROPS, OUT, OPTICAL = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
LOOK = 4  # 4x4 averaging of linear power: 40 m pixels, 16 looks, for per-pixel statistics

# Optical image extent (EOX tiles z12, 919..922 x 1823..1826) and the boxes in its pixel space.
W0, E0, N0, S0 = -99.228515625, -98.876953125, 19.39406789539661, 19.062117883514652
PX = {"Chinampas, Xochimilco": (380, 330, 470, 400),
      "Chinampas, Tlahuac-Mixquic": (690, 410, 800, 500),
      "Farmland SE (rain-fed?) A": (830, 830, 1000, 990),
      "Farmland SW (rain-fed?) B": (100, 760, 220, 880)}
COL = {"Chinampas, Xochimilco": "#1b7837", "Chinampas, Tlahuac-Mixquic": "#5aae61",
       "Farmland SE (rain-fed?) A": "#b35806", "Farmland SW (rain-fed?) B": "#f1a340"}


def px2ll(px, py):
    return W0 + px / 1024 * (E0 - W0), N0 - py / 1024 * (N0 - S0)


BOX = {k: (*px2ll(v[0], v[3]), *px2ll(v[2], v[1])) for k, v in PX.items()}  # W, S, E, N

files = sorted(glob.glob(os.path.join(CROPS, "gcovA_*.npz")))
dates = [os.path.basename(f)[6:16] for f in files]
first = np.load(files[0])
x, y, epsg = first["xCoordinates"], first["yCoordinates"], int(first["projection"])
spacing = float(x[1] - x[0])
H, W = first["HHHH"].shape
h, w = H // LOOK, W // LOOK


def multilook(a):
    a = np.where(np.isfinite(a) & (a > 0), a, np.nan)[: h * LOOK, : w * LOOK]
    return np.nanmean(a.reshape(h, LOOK, w, LOOK), axis=(1, 3))


HH = np.empty((len(files), h, w), np.float32)
HV = np.empty_like(HH)
granules = []
for k, f in enumerate(files):
    c = np.load(f)
    assert c["HHHH"].shape == (H, W), f
    HH[k], HV[k] = multilook(c["HHHH"]), multilook(c["HVHV"])
    granules.append(str(c["granule"]))
HHdb, HVdb = 10 * np.log10(HH), 10 * np.log10(HV)
xl = x[0] + spacing * (LOOK - 1) / 2 + np.arange(w) * spacing * LOOK
yl = y[0] - spacing * (LOOK - 1) / 2 - np.arange(h) * spacing * LOOK
to_grid = Transformer.from_crs(4326, epsg, always_xy=True)


def box_mask(b):
    (e0, n0), (e1, n1) = [to_grid.transform(lo, la) for lo, la in ((b[0], b[1]), (b[2], b[3]))]
    cols = (xl >= e0) & (xl <= e1)
    rows = (yl >= n0) & (yl <= n1)
    return rows[:, None] & cols[None, :]


# Land-cover mask from the radar itself: drop open water (dark in HH most of the year) and
# buildings (very bright HH, low HV/HH). Thresholds are rough, chosen by eye, not calibrated.
hh_med = np.nanmedian(HHdb, axis=0)
ratio_med = np.nanmedian(HVdb - HHdb, axis=0)
water = hh_med < -16
built = (hh_med > -2) | (ratio_med < -11)
veg = ~water & ~built & np.isfinite(hh_med)

# Growth cycles per pixel: rises of at least 3 dB in HV from a trough, then a fall of at
# least 3 dB (16-look noise is about 1.1 dB per date, so 3 dB is about 3 sigma).
AMP = 3.0


def cycles(series):
    s = series[np.isfinite(series)]
    if s.size < 10:
        return np.nan
    n, lo, hi, rising = 0, s[0], s[0], False
    for v in s[1:]:
        if not rising:
            lo = min(lo, v)
            if v - lo >= AMP:
                rising, hi = True, v
        else:
            hi = max(hi, v)
            if hi - v >= AMP:
                n += 1
                rising, lo = False, v
    return n


D = [dt.date.fromisoformat(d) for d in dates]
dry = np.array([(d.month in (11, 12, 1, 2, 3, 4)) for d in D])
stats, series = {}, {}
for k, b in BOX.items():
    m = box_mask(b)
    mv = m & veg
    hv = HVdb[:, mv]
    rng = np.nanpercentile(hv, 90, axis=0) - np.nanpercentile(hv, 10, axis=0)
    cyc = np.array([cycles(hv[:, i]) for i in range(hv.shape[1])])
    dry_mean = np.nanmean(hv[dry], axis=0)
    wet_mean = np.nanmean(hv[~dry], axis=0)
    stats[k] = {
        "pixels_40m": int(m.sum()), "vegetated_pixels": int(mv.sum()),
        "share_water": float((m & water).sum() / m.sum()), "share_built": float((m & built).sum() / m.sum()),
        "hv_median_db": float(np.nanmedian(hv)),
        "seasonal_range_db_p50": float(np.nanmedian(rng)),
        "wet_minus_dry_db_p50": float(np.nanmedian(wet_mean - dry_mean)),
        "cycles_share": {str(n): float(np.mean(cyc == n)) for n in range(0, 5)},
        "cycles_mean": float(np.nanmean(cyc)),
    }
    series[k] = {"hv_db": np.nanmedian(hv, axis=1).tolist(), "hh_db": np.nanmedian(HHdb[:, mv], axis=1).tolist(),
                 "hv_p25": np.nanpercentile(hv, 25, axis=1).tolist(), "hv_p75": np.nanpercentile(hv, 75, axis=1).tolist(),
                 "cycles": cyc}

# Noise check: the same cycle count on a box of dense forest in the southern hills, which
# should show close to zero real cycles.
forest = (-99.16, 19.10, -99.10, 19.14)
fm = box_mask(forest) & veg
fhv = HVdb[:, fm]
fcyc = np.array([cycles(fhv[:, i]) for i in range(fhv.shape[1])])
stats["Control: forest, southern hills"] = {"vegetated_pixels": int(fm.sum()), "cycles_mean": float(np.nanmean(fcyc)),
                                            "cycles_share": {str(n): float(np.mean(fcyc == n)) for n in range(0, 5)}}

# Figure 1: time series (median and interquartile band of vegetated 40 m pixels)
fig, ax = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
for k, s in series.items():
    ax[0].plot(D, s["hv_db"], "o-", ms=3, color=COL[k], label=f"{k} ({stats[k]['vegetated_pixels']} veg. px)")
    ax[0].fill_between(D, s["hv_p25"], s["hv_p75"], color=COL[k], alpha=0.12, lw=0)
    ax[1].plot(D, np.array(s["hv_db"]) - np.array(s["hh_db"]), "o-", ms=3, color=COL[k])
ax[0].set_ylabel("HV backscatter, dB\n(median and 25-75% of pixels)")
ax[1].set_ylabel("HV minus HH, dB")
for a in ax:
    a.axvspan(dt.date(2026, 5, 15), dt.date(2026, 10, 15), color="#9ecae1", alpha=0.25, lw=0)
    a.grid(alpha=0.3)
ax[0].legend(fontsize=8)
ax[0].set_title(f"NISAR GCOV frequency A ({spacing:.0f} m, averaged to {spacing*LOOK:.0f} m), {len(dates)} dates, PROVISIONAL. Water and buildings masked.")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_full_res_series.png"), dpi=90)

# Figure 2: distribution of growth cycles per pixel
fig, ax = plt.subplots(figsize=(9, 4))
labels = list(series) + ["Control: forest, southern hills"]
wbar = 0.16
for i, k in enumerate(labels):
    shares = [stats[k]["cycles_share"][str(n)] * 100 for n in range(5)]
    ax.bar(np.arange(5) + (i - 2) * wbar, shares, wbar, label=k, color=COL.get(k, "#777777"))
ax.set_xticks(range(5))
ax.set_xlabel(f"growth cycles per 40 m pixel in the year (HV rise and fall of at least {AMP:.0f} dB)")
ax.set_ylabel("% of vegetated pixels")
ax.legend(fontsize=7)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_full_res_cycles.png"), dpi=90)

# Figure 3: zoomed 10 m view of the Tlahuac chinampas, HV on a dry and a wet date, plus mask
k = "Chinampas, Tlahuac-Mixquic"
b = BOX[k]
full = np.load(files[0])
(e0, n0), (e1, n1) = [to_grid.transform(lo, la) for lo, la in ((b[0], b[1]), (b[2], b[3]))]
c0, c1 = np.searchsorted(x, e0), np.searchsorted(x, e1)
r0, r1 = np.searchsorted(-y, -n1), np.searchsorted(-y, -n0)
iw = int(np.argmin([abs((d - dt.date(2026, 9, 1)).days) for d in D]))
idr = int(np.argmin([abs((d - dt.date(2026, 3, 1)).days) for d in D]))
fig, ax = plt.subplots(1, 2, figsize=(13, 6))
for a, i in zip(ax, (idr, iw)):
    hv10 = 10 * np.log10(np.where(np.load(files[i])["HVHV"][r0:r1, c0:c1] > 0, np.load(files[i])["HVHV"][r0:r1, c0:c1], np.nan))
    a.imshow(hv10, cmap="gray", vmin=-26, vmax=-8)
    a.set_title(f"HV, {dates[i]}, {spacing:.0f} m pixels (Tlahuac-Mixquic box)")
    a.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_full_res_tlahuac_dry_vs_wet.png"), dpi=90)

json.dump({"dates": dates, "granules": granules, "pixel_spacing_m": spacing, "look": LOOK, "boxes_lonlat": BOX,
           "stats": stats, "series": {k: {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in s.items() if kk != "cycles"} for k, s in series.items()}},
          open(os.path.join(OUT, "full_res_stats.json"), "w"), indent=1)
for k, s in stats.items():
    print(k, json.dumps(s))
