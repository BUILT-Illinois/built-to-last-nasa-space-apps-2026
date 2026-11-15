"""Chinampas vs rain-fed farmland: NISAR L-band backscatter over one year (exploratory, AI-assisted).

Drafted with AI assistance (Claude Code); see docs/AI_USAGE.md.
Usage: python poc/chinampas_vs_farmland/chinampas_poc.py --data data/Mexico_City
Needs numpy, pyproj, matplotlib, pillow. Step 1 downloads Sentinel-2 cloudless tiles (EOX, CC BY-NC-SA 4.0) only to
draw the plot boxes; the radar numbers do not use them.
"""
import argparse, sys
ap=argparse.ArgumentParser(); ap.add_argument("--data",default="data/Mexico_City"); ap.add_argument("--out",default="poc/chinampas_vs_farmland")
ARGS=ap.parse_args()
import numpy as np, glob, os
from pyproj import Transformer
D=ARGS.data
EXCL={"2025-12-05","2026-04-16"}  # D-17
files=sorted(glob.glob(D+"/mexico_city_gcov_*.npz"))
dates=[os.path.basename(f)[-14:-4] for f in files]
keep=[i for i,d in enumerate(dates) if d not in EXCL]
dates=[dates[i] for i in keep]; files=[files[i] for i in keep]
z=np.load(files[0]); x=z["xCoordinates"]; y=z["yCoordinates"]; epsg=int(z["projection"])
HH=np.empty((len(files),)+z["HHHH"].shape,np.float32); HV=HH.copy()
for k,f in enumerate(files):
    c=np.load(f)
    HH[k]=c["HHHH"]; HV[k]=c["HVHV"]
db=lambda a: 10*np.log10(np.where(a>0,a,np.nan))
HHdb,HVdb=db(HH),db(HV)
tr=Transformer.from_crs(4326,epsg,always_xy=True)
def rc(lon,lat):
    e,n=tr.transform(lon,lat); return int(round((y[0]-n)/80)),int(round((e-x[0])/80))
def lonlat_grid():
    return x,y

# ---- step 1: optical backdrop for the plot boxes
import math,io,urllib.request
from PIL import Image
Z=12
def t(lon,lat):
    n=2**Z; return int((lon+180)/360*n), int((1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n)
x0,y0=t(-99.22,19.36); x1,y1=t(-98.88,19.08)
im=Image.new("RGB",((x1-x0+1)*256,(y1-y0+1)*256))
for tx in range(x0,x1+1):
    for ty in range(y0,y1+1):
        u=f"https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2024_3857/default/g/{Z}/{ty}/{tx}.jpg"
        im.paste(Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"built-to-last-poc"}),timeout=30).read())),((tx-x0)*256,(ty-y0)*256))
im.save(ARGS.out+"/_optical.png"); print(im.size,(x0,y0,x1,y1))
def lon(x): return x/2**Z*360-180
def lat(y): return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/2**Z))))
print(lon(x0),lon(x1+1),lat(y0),lat(y1+1))

# ---- step 2: time series
import numpy as np, json, datetime as dt
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
W0,E0,N0,S0=-99.228515625,-98.876953125,19.39406789539661,19.062117883514652
def px2ll(px,py): return W0+px/1024*(E0-W0), N0-py/1024*(N0-S0)
# boxes in the optical image's pixel space (x0,y0,x1,y1)
PX={"Chinampas, Xochimilco":(380,330,470,400),
    "Chinampas, Tlahuac-Mixquic":(690,410,800,500),
    "Farmland SE (rain-fed?) A":(830,830,1000,990),
    "Farmland SW (rain-fed?) B":(100,760,220,880)}
BOX={k:(*px2ll(v[0],v[3]),*px2ll(v[2],v[1])) for k,v in PX.items()}  # west,south,east,north
im=Image.open(ARGS.out+"/_optical.png"); d=ImageDraw.Draw(im)
for k,v in PX.items(): d.rectangle(v,outline=(255,255,0),width=3); d.text((v[0],v[1]-12),k[:14],fill=(255,255,0))
im.save(ARGS.out+"/fig_plot_locations.png")
def mask(b):
    r0,c0=rc(b[0],b[3]); r1,c1=rc(b[2],b[1]); m=np.zeros(HVdb.shape[1:],bool); m[r0:r1+1,c0:c1+1]=True; return m
out={}
for k,b in BOX.items():
    m=mask(b)
    out[k]=dict(n=int(m.sum()),hv=np.nanmedian(HVdb[:,m],axis=1),hh=np.nanmedian(HHdb[:,m],axis=1),
                hv_lin=np.nanmean(HV[:,m],axis=1),hh_lin=np.nanmean(HH[:,m],axis=1))
    o=out[k]; o["rvi"]=4*o["hv_lin"]/(o["hh_lin"]+o["hv_lin"])
D=[dt.date.fromisoformat(s) for s in dates]
fig,ax=plt.subplots(3,1,figsize=(11,10),sharex=True)
col={"Chinampas, Xochimilco":"#1b7837","Chinampas, Tlahuac-Mixquic":"#5aae61","Farmland SE (rain-fed?) A":"#b35806","Farmland SW (rain-fed?) B":"#f1a340"}
for k,o in out.items():
    ax[0].plot(D,o["hv"],"o-",ms=3,color=col[k],label=f"{k} ({o['n']} px)")
    ax[1].plot(D,o["hv"]-o["hh"],"o-",ms=3,color=col[k])
    ax[2].plot(D,o["rvi"],"o-",ms=3,color=col[k])
ax[0].set_ylabel("HV backscatter, dB"); ax[1].set_ylabel("HV minus HH, dB"); ax[2].set_ylabel("radar vegetation index (4HV/(HH+HV))")
for a in ax: a.axvspan(dt.date(2026,5,15),dt.date(2026,10,15),color="#9ecae1",alpha=.25,lw=0); a.grid(alpha=.3)
ax[0].legend(fontsize=8); ax[0].set_title("NISAR L-band GCOV, track 19, 26 dates (PROVISIONAL), box medians")
plt.tight_layout(); plt.savefig(ARGS.out+"/fig_chinampas_vs_farmland.png",dpi=90)
for k,o in out.items():
    print(k,o["n"],"HV mean %.1f std %.2f range %.1f | RVI mean %.2f std %.3f | HV-HH %.1f"%(np.nanmean(o["hv"]),np.nanstd(o["hv"]),np.nanmax(o["hv"])-np.nanmin(o["hv"]),np.nanmean(o["rvi"]),np.nanstd(o["rvi"]),np.nanmean(o["hv"]-o["hh"])))
json.dump({k:{"box_lonlat":BOX[k],"n_px":v["n"],"hv_db":[float(x) for x in v["hv"]],"hh_db":[float(x) for x in v["hh"]],"rvi":[float(x) for x in v["rvi"]]} for k,v in out.items()}|{"dates":dates},open(ARGS.out+"/plot_series.json","w"))
