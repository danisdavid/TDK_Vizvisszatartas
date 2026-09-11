import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Bemeneti (WGS84) és kimeneti (EOV) fájl elérési útja
dem_path = "01_DATA/DEM/Kiskoros_pilot_DEM_raw.tif"
dem_eov_path = "02_PROCESSING/Kiskoros_DEM_EOV.tif"

CEL_VETULET = "EPSG:23700"  # Magyar EOV

with rasterio.open(dem_path) as src:

    # Kiszámoljuk, milyen méretű/elrendezésű lenne a raszter EOV-ban
    transform, width, height = calculate_default_transform(
        src.crs, CEL_VETULET, src.width, src.height, *src.bounds
    )

    # Az eredeti metaadatok másolása, majd frissítése az új vetülethez
    kwargs = src.meta.copy()
    kwargs.update({
        "crs": CEL_VETULET,
        "transform": transform,
        "width": width,
        "height": height
    })

    # Létrehozzuk az új fájlt, és belemásoljuk az adatokat úgy,
    # hogy közben át is vetítjük EOV-ba
    with rasterio.open(dem_eov_path, "w", **kwargs) as dst:
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=CEL_VETULET,
            resampling=Resampling.bilinear
        )

print(f"Kész! Az EOV-vetületű DEM itt található: {dem_eov_path}")