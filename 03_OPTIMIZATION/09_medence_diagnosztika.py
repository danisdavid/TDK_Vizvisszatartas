import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import xy
from pyproj import Transformer

CSV = "03_OPTIMIZATION/medencek_FABDEM.csv"
TOP = 20

trf = Transformer.from_crs("EPSG:23700", "EPSG:4326", always_xy=True)

def hol_van(x, y):
    """EOV koordinatabol Google Maps link."""
    lon, lat = trf.transform(x, y)
    return lat, lon, f"https://www.google.com/maps?q={lat:.5f},{lon:.5f}"

# ------------------------------------------------------------------
# 1. A legnagyobb medencek helye
# ------------------------------------------------------------------
tabla = pd.read_csv(CSV)
top = tabla.head(TOP).copy()

print("=" * 108)
print(f"A {TOP} LEGNAGYOBB MEDENCE")
print("=" * 108)
print(f"{'rang':>4} {'M m3':>8} {'ha':>8} {'max m':>6} {'szeli':>5}  {'szel.':>7} {'hossz.':>7}  link")
print("-" * 108)

sorok = []
for _, s in top.iterrows():
    lat, lon, link = hol_van(s["eov_x"], s["eov_y"])
    sorok.append({**s.to_dict(), "lat": lat, "lon": lon, "maps": link})
    print(f"{int(s['rang']):>4} {s['terfogat_m3']/1e6:>8.1f} {s['terulet_ha']:>8.0f} "
          f"{s['max_melyseg_m']:>6.1f} {int(s['szelen_van']):>5}  "
          f"{lat:>7.4f} {lon:>7.4f}  {link}")

pd.DataFrame(sorok).to_csv("03_OPTIMIZATION/top20_helyszinek.csv", index=False)

# ------------------------------------------------------------------
# 2. Kelet-nyugati megoszlas: mennyi terfogat van a nyugati savban?
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("TERFOGAT MEGOSZLASA KELET-NYUGATI IRANYBAN")
print("=" * 60)

hatarok = [635000, 650000, 660000, 670000, 680000, 690000, 710000]
for bal, jobb in zip(hatarok[:-1], hatarok[1:]):
    sav = tabla[(tabla["eov_x"] >= bal) & (tabla["eov_x"] < jobb)]
    if len(sav) == 0:
        continue
    _, lon_bal, _ = hol_van(bal, 140000)
    _, lon_jobb, _ = hol_van(jobb, 140000)
    print(f"EOV x {bal:,}–{jobb:,}  (hossz. {lon_bal:.2f}–{lon_jobb:.2f}°): "
          f"{len(sav):>5} medence, {sav['terfogat_m3'].sum()/1e6:>7.1f} M m3")

# ------------------------------------------------------------------
# 3. Szelsoseges pontok megkeresese a raszterekben
# ------------------------------------------------------------------
def szelsoertek_helye(ut, cimke):
    with rasterio.open(ut) as src:
        adat = src.read(1)
        nodata = src.nodata
        tr = src.transform
    ervenyes = adat != nodata
    idx = np.argmax(np.where(ervenyes, adat, -np.inf))
    sor, oszlop = np.unravel_index(idx, adat.shape)
    x, y = xy(tr, int(sor), int(oszlop))
    lat, lon, link = hol_van(x, y)
    print(f"\n{cimke}: {adat[sor, oszlop]:.2f}")
    print(f"  {link}")

print("\n" + "=" * 60)
print("SZELSOERTEKEK")
print("=" * 60)
szelsoertek_helye("02_PROCESSING/Kiskoros_DEM_EOV.tif",
                  "Legmagasabb pont a Copernicus DSM-en (m)")
szelsoertek_helye("02_PROCESSING/Kiskoros_FABDEM_EOV.tif",
                  "Legmagasabb pont a FABDEM DTM-en (m)")
szelsoertek_helye("02_PROCESSING/DSM_minusz_DTM.tif",
                  "Legnagyobb DSM-DTM elteres (m)")