import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import xy
from scipy import ndimage

# =====================================================================
# PARAMETEREK  - ezeket a dolgozatban dokumentalni es indokolni kell!
# =====================================================================
EREDETI    = "02_PROCESSING/Kiskoros_FABDEM_EOV.tif"
FELTOLTOTT = "02_PROCESSING/Kiskoros_FABDEM_filled.tif"
CIMKE      = "FABDEM"

KITERJEDES_KUSZOB = 0.05   # m   - ennel melyebb pixel tartozik egy medencehez
MIN_MAX_MELYSEG   = 0.50   # m   - a medence legmelyebb pontjanak minimuma
MIN_PIXELSZAM     = 10     # db  - 10 x 900 m2 = 0,9 ha alatti foltokat eldobunk

KIMENET_CSV  = f"03_OPTIMIZATION/medencek_{CIMKE}.csv"
KIMENET_GPKG = f"03_OPTIMIZATION/medencek_{CIMKE}.gpkg"
KIMENET_TIF  = f"03_OPTIMIZATION/melyedes_melyseg_{CIMKE}.tif"

# =====================================================================
# 1. BEOLVASAS
# =====================================================================
with rasterio.open(EREDETI) as src:
    eredeti = src.read(1).astype("float64")
    transform = src.transform
    profil = src.profile.copy()
    nodata_eredeti = src.nodata
    pixel_terulet = abs(src.res[0] * src.res[1])

with rasterio.open(FELTOLTOTT) as src:
    feltoltott = src.read(1).astype("float64")
    nodata_feltoltott = src.nodata

if eredeti.shape != feltoltott.shape:
    raise SystemExit("HIBA: az eredeti es a feltoltott DEM merete nem egyezik!")

print(f"Raszter: {eredeti.shape[0]} sor x {eredeti.shape[1]} oszlop")
print(f"Egy pixel terulete: {pixel_terulet:.0f} m2")

ervenyes = (
    (eredeti != nodata_eredeti)
    & (feltoltott != nodata_feltoltott)
    & np.isfinite(eredeti)
    & np.isfinite(feltoltott)
)
print(f"Ervenyes pixelek: {ervenyes.sum():,} / {eredeti.size:,}\n")

# =====================================================================
# 2. SAJAT ALGORITMUS - a melyedes melysege pixelenkent
#    melyseg = feltoltott felszin - eredeti terep
# =====================================================================
melyseg = np.zeros(eredeti.shape, dtype="float64")
melyseg[ervenyes] = feltoltott[ervenyes] - eredeti[ervenyes]
melyseg[melyseg < 0] = 0.0     # numerikus zaj miatti negativ ertekek kiszurese

print(f"Legnagyobb melyedes-melyseg: {melyseg.max():.2f} m")
print(f"Melyedeses pixelek aranya:   "
      f"{(melyseg > KITERJEDES_KUSZOB).sum() / ervenyes.sum() * 100:.2f}%\n")

# =====================================================================
# 3. OSSZEFUGGO MEDENCEK AZONOSITASA (klaszterezes)
#    8-szomszedsag: az atlosan erintkezo pixelek is egy medencehez tartoznak
# =====================================================================
medence_maszk = melyseg > KITERJEDES_KUSZOB
szomszedsag = np.ones((3, 3), dtype=int)

cimkek, medence_db = ndimage.label(medence_maszk, structure=szomszedsag)
print(f"Nyers medencek szama: {medence_db:,}")

if medence_db == 0:
    raise SystemExit("Nem talaltam egyetlen medencet sem. Csokkentsd a kuszoboket!")

# =====================================================================
# 4. MEDENCENKENTI STATISZTIKAK
#    FONTOS: nem for-ciklussal! 100 000+ medencenel az orakig tartana.
#    A np.bincount egyetlen vegigolvasassal osszegez cimke szerint.
# =====================================================================
cimkek_lapos  = cimkek.ravel()
melyseg_lapos = melyseg.ravel()

pixelszam = np.bincount(cimkek_lapos, minlength=medence_db + 1)
terfogat  = np.bincount(
    cimkek_lapos,
    weights=melyseg_lapos * pixel_terulet,
    minlength=medence_db + 1,
)

print("Legmelyebb pont keresese medenckent... (ez tarthat egy percig)")
max_melyseg = ndimage.maximum(melyseg, cimkek, index=np.arange(1, medence_db + 1))

# Sulypont (centroid) sor/oszlop koordinataja - szinten bincount-tal
sorok, oszlopok = np.indices(melyseg.shape)
sor_osszeg    = np.bincount(cimkek_lapos, weights=sorok.ravel(),    minlength=medence_db + 1)
oszlop_osszeg = np.bincount(cimkek_lapos, weights=oszlopok.ravel(), minlength=medence_db + 1)
del sorok, oszlopok

# =====================================================================
# 5. SZELI MEDENCEK MEGJELOLESE (csonka terfogatuak)
# =====================================================================
gyanus = ndimage.binary_dilation(~ervenyes)
gyanus[0, :] = True
gyanus[-1, :] = True
gyanus[:, 0] = True
gyanus[:, -1] = True

szeli_cimkek = set(np.unique(cimkek[gyanus]).tolist()) - {0}
print(f"Szelen vagy nodata mellett fekvo medencek: {len(szeli_cimkek):,}\n")

# =====================================================================
# 6. TABLAZAT OSSZEALLITASA
# =====================================================================
azonositok = np.arange(1, medence_db + 1)
px = pixelszam[1:]

tabla = pd.DataFrame({
    "id": azonositok,
    "pixelszam": px,
    "terulet_m2": px * pixel_terulet,
    "terulet_ha": px * pixel_terulet / 10_000,
    "terfogat_m3": terfogat[1:],
    "max_melyseg_m": max_melyseg,
    "atlag_melyseg_m": terfogat[1:] / (px * pixel_terulet),
    "sor": sor_osszeg[1:] / px,
    "oszlop": oszlop_osszeg[1:] / px,
})

tabla["szelen_van"] = tabla["id"].isin(szeli_cimkek).astype(int)

# Sulypont atvaltasa EOV koordinatakra
eov_x, eov_y = xy(transform, tabla["sor"].values, tabla["oszlop"].values)
tabla["eov_x"] = eov_x
tabla["eov_y"] = eov_y

# =====================================================================
# 7. SZURES ES RANGSOROLAS
# =====================================================================
megfelel = (
    (tabla["max_melyseg_m"] >= MIN_MAX_MELYSEG)
    & (tabla["pixelszam"] >= MIN_PIXELSZAM)
)

eredmeny = (
    tabla[megfelel]
    .sort_values("terfogat_m3", ascending=False)
    .reset_index(drop=True)
)
eredmeny.insert(0, "rang", np.arange(1, len(eredmeny) + 1))

print("=" * 58)
print(f"Nyers medencek:          {medence_db:>10,}")
print(f"Szures utan megmaradt:   {len(eredmeny):>10,}")
print(f"Ebbol szeli (csonka):    {int(eredmeny['szelen_van'].sum()):>10,}")
print("-" * 58)
print(f"Ossz. terfogat:          {eredmeny['terfogat_m3'].sum() / 1e6:>10.2f} millio m3")
print(f"Ossz. terulet:           {eredmeny['terulet_ha'].sum():>10.1f} ha")
print("=" * 58)

print("\nA 10 legnagyobb medence:")
print(
    eredmeny.head(10)[
        ["rang", "terfogat_m3", "terulet_ha", "max_melyseg_m", "eov_x", "eov_y", "szelen_van"]
    ].to_string(index=False, float_format=lambda v: f"{v:,.1f}")
)

# =====================================================================
# 8. MENTES
# =====================================================================
eredmeny.to_csv(KIMENET_CSV, index=False)
print(f"\nMentve: {KIMENET_CSV}")

# Szurt melyseg-raszter: csak a megtartott medencek latszanak
megtart = np.zeros(medence_db + 1, dtype=bool)
megtart[eredmeny["id"].values] = True
megtartott_pixelek = megtart[cimkek]

kimenet_raszter = np.full(melyseg.shape, -9999.0, dtype="float32")
kimenet_raszter[megtartott_pixelek] = melyseg[megtartott_pixelek].astype("float32")

profil.update({"count": 1, "dtype": "float32", "nodata": -9999.0, "compress": "lzw"})
with rasterio.open(KIMENET_TIF, "w", **profil) as ki:
    ki.write(kimenet_raszter, 1)
print(f"Mentve: {KIMENET_TIF}")

# Sulypontok QGIS-hez
try:
    import geopandas as gpd
    pontok = gpd.GeoDataFrame(
        eredmeny.drop(columns=["sor", "oszlop"]),
        geometry=gpd.points_from_xy(eredmeny["eov_x"], eredmeny["eov_y"]),
        crs="EPSG:23700",
    )
    pontok.to_file(KIMENET_GPKG, driver="GPKG")
    print(f"Mentve: {KIMENET_GPKG}")
except Exception as hiba:
    print(f"A GPKG mentes nem sikerult ({hiba}) - a CSV viszont megvan.")