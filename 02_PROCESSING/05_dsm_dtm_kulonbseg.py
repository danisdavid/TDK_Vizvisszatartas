import numpy as np
import rasterio

DSM = "02_PROCESSING/Kiskoros_DEM_EOV.tif"       # Copernicus - felszin (fakkal)
DTM = "02_PROCESSING/Kiskoros_FABDEM_EOV.tif"    # FABDEM - talaj (fak nelkul)
KIMENET = "02_PROCESSING/DSM_minusz_DTM.tif"

NODATA = -9999.0

with rasterio.open(DSM) as a:
    dsm = a.read(1).astype("float64")
    dsm_nodata = a.nodata
    profil = a.profile.copy()

with rasterio.open(DTM) as b:
    dtm = b.read(1).astype("float64")
    dtm_nodata = b.nodata

if dsm.shape != dtm.shape:
    raise SystemExit("HIBA: a ket raszter merete nem egyezik! Futtasd a 04-es szkriptet.")

# Csak ott szamolunk, ahol MINDKET fajlban van ervenyes adat
ervenyes = (dsm != dsm_nodata) & (dtm != dtm_nodata)

kulonbseg = np.full(dsm.shape, NODATA, dtype="float32")
kulonbseg[ervenyes] = (dsm[ervenyes] - dtm[ervenyes]).astype("float32")

ertekek = kulonbseg[ervenyes]

print(f"Ervenyes pixelek: {ervenyes.sum():,}")
print(f"Atlagos elteres:  {ertekek.mean():6.2f} m")
print(f"Median elteres:   {np.median(ertekek):6.2f} m")
print(f"Legnagyobb:       {ertekek.max():6.2f} m")
print(f"Legkisebb:        {ertekek.min():6.2f} m")
print()

for kuszob in (1, 2, 5, 10):
    db = int(np.sum(ertekek > kuszob))
    print(f"  {kuszob:2d} m-nel nagyobb elteres: {db:>9,} pixel  "
          f"({db / ertekek.size * 100:5.2f}%)  = {db * 900 / 1e6:6.1f} km2")

profil.update({"count": 1, "dtype": "float32", "nodata": NODATA, "compress": "lzw"})
with rasterio.open(KIMENET, "w", **profil) as ki:
    ki.write(kulonbseg, 1)

print(f"\nKesz: {KIMENET}")