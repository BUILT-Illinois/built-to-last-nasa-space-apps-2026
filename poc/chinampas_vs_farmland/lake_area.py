import numpy as np, glob, os, json, datetime as dt, sys
from pyproj import Transformer
# Exploratory, AI-assisted (Claude Code), see docs/AI_USAGE.md. Usage: python lake_area.py <rain_json> [gcovA_dir]
D=sys.argv[2] if len(sys.argv) > 2 else "data/Mexico_City/gcov_freqA_chinampas"
files=sorted(glob.glob(D+"/*.npz")); z=np.load(files[0]); x,y=z["xCoordinates"],z["yCoordinates"]
tr=Transformer.from_crs(4326,int(z["projection"]),always_xy=True)
def win(w,s,e,n):
    (e0,n0),(e1,n1)=tr.transform(w,s),tr.transform(e,n)
    return slice(int((y[0]-n1)/10),int((y[0]-n0)/10)), slice(int((e0-x[0])/10),int((e1-x[0])/10))
LAKES={"Lago de Tlahuac-Xico (new Lake Chalco)":(-99.00,19.255,-98.95,19.285),
       "Xochimilco lagoon area (Cuemanco)":(-99.09,19.265,-99.05,19.29)}
rain=json.load(open(sys.argv[1])); rm=dict(zip(rain["daily"]["time"],rain["daily"]["precipitation_sum"]))
L=3
for name,b in LAKES.items():
    r,c=win(*b); print(name)
    for f in files:
        d=os.path.basename(f)[6:16]; t=dt.date.fromisoformat(d)
        a=np.load(f)["HHHH"][r,c]; h,w=(a.shape[0]//L)*L,(a.shape[1]//L)*L
        a=np.nanmean(np.where(a>0,a,np.nan)[:h,:w].reshape(h//L,L,w//L,L),axis=(1,3))
        db=10*np.log10(a); area=(db<-15).sum()*(10*L)**2/1e6
        r3=sum((rm.get((t-dt.timedelta(days=k)).isoformat()) or 0) for k in (1,2,3))
        print(f"  {d} rain3 {r3:5.1f} mm  dark-water area {area:5.2f} km2")
