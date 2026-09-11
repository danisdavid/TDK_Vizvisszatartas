import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

dem_path = "01_DATA/DEM/Kiskoros_FABDEM_raw.tif"
dem_eov_path = "02_PROCESSING/Kiskoros_FABDEM_EOV.tif"

CEL_VETULET = "EPSG:23700"   # Magyar EOV
NODATA = -9999.0             # Ezzel jeloljuk az "itt nincs adat" pixeleket
FELBONTAS = 30               # Meter - fix, negyzetes pixelracs

with rasterio.open(dem_path) as src:

    # A resolution=30 kenyszeriti a tiszta, negyzetes 30x30 m-es racsot
    transform, width, height = calculate_default_transform(
        src.crs, CEL_VETULET,
        src.width, src.height,
        *src.bounds,
        resolution=FELBONTAS
    )

    kwargs = src.meta.copy()
    kwargs.update({
        "crs": CEL_VETULET,
        "transform": transform,
        "width": width,
        "height": height,
        "dtype": "float32",
        "nodata": NODATA,      # <-- EZ a lenyeg: megjeloljuk a nodata erteket
        "compress": "lzw",     # tomorites, kisebb fajlmeret
    })

    with rasterio.open(dem_eov_path, "w", **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,
            dst_transform=transform,
            dst_crs=CEL_VETULET,
            dst_nodata=NODATA,      # <-- a sarkok ezt kapjak 0 helyett
            resampling=Resampling.bilinear,
        )

print("Kesz! Az EOV-vetuletu DEM itt talalhato:", dem_eov_path)