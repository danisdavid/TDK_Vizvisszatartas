import rasterio
from rasterio.warp import reproject, Resampling

# A "mester" racs: a Copernicus EOV fajl hatarozza meg a kozos geometriat.
# Minden tovabbi reteg EHHEZ fog igazodni a projekt soran.
MESTER  = "02_PROCESSING/Kiskoros_DEM_EOV.tif"
FORRAS  = "01_DATA/DEM/Kiskoros_FABDEM_raw.tif"
KIMENET = "02_PROCESSING/Kiskoros_FABDEM_EOV.tif"

NODATA = -9999.0

with rasterio.open(MESTER) as mester:
    profil = mester.profile.copy()
    cel_transform = mester.transform
    cel_crs = mester.crs
    print("Mester racs:")
    print(f"  meret: {mester.height} sor x {mester.width} oszlop")
    print(f"  pixel: {mester.res}")

profil.update({
    "count": 1,
    "dtype": "float32",
    "nodata": NODATA,
    "compress": "lzw",
})

with rasterio.open(FORRAS) as forras:
    print("\nForras (FABDEM nyers):")
    print(f"  meret: {forras.height} sor x {forras.width} oszlop")
    print(f"  vetulet: {forras.crs}")

    with rasterio.open(KIMENET, "w", **profil) as ki:
        reproject(
            source=rasterio.band(forras, 1),
            destination=rasterio.band(ki, 1),
            src_transform=forras.transform,
            src_crs=forras.crs,
            src_nodata=forras.nodata,
            dst_transform=cel_transform,   # <-- a mester racs geometriaja
            dst_crs=cel_crs,
            dst_nodata=NODATA,
            resampling=Resampling.bilinear,
        )

print(f"\nKesz: {KIMENET}")
print("A FABDEM most pontosan ugyanazon a racson van, mint a Copernicus DEM.")