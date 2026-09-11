[1mdiff --git a/02_PROCESSING/00_dem_atvetites_eov.py b/02_PROCESSING/00_dem_atvetites_eov.py[m
[1mindex bf327fb..28cd75f 100644[m
[1m--- a/02_PROCESSING/00_dem_atvetites_eov.py[m
[1m+++ b/02_PROCESSING/00_dem_atvetites_eov.py[m
[36m@@ -1,39 +1,45 @@[m
 import rasterio[m
 from rasterio.warp import calculate_default_transform, reproject, Resampling[m
 [m
[31m-# Bemeneti (WGS84) és kimeneti (EOV) fájl elérési útja[m
 dem_path = "01_DATA/DEM/Kiskoros_pilot_DEM_raw.tif"[m
 dem_eov_path = "02_PROCESSING/Kiskoros_DEM_EOV.tif"[m
 [m
[31m-CEL_VETULET = "EPSG:23700"  # Magyar EOV[m
[32m+[m[32mCEL_VETULET = "EPSG:23700"   # Magyar EOV[m
[32m+[m[32mNODATA = -9999.0             # Ezzel jeloljuk az "itt nincs adat" pixeleket[m
[32m+[m[32mFELBONTAS = 30               # Meter - fix, negyzetes pixelracs[m
 [m
 with rasterio.open(dem_path) as src:[m
 [m
[31m-    # Kiszámoljuk, milyen méretű/elrendezésű lenne a raszter EOV-ban[m
[32m+[m[32m    # A resolution=30 kenyszeriti a tiszta, negyzetes 30x30 m-es racsot[m
     transform, width, height = calculate_default_transform([m
[31m-        src.crs, CEL_VETULET, src.width, src.height, *src.bounds[m
[32m+[m[32m        src.crs, CEL_VETULET,[m
[32m+[m[32m        src.width, src.height,[m
[32m+[m[32m        *src.bounds,[m
[32m+[m[32m        resolution=FELBONTAS[m
     )[m
 [m
[31m-    # Az eredeti metaadatok másolása, majd frissítése az új vetülethez[m
     kwargs = src.meta.copy()[m
     kwargs.update({[m
         "crs": CEL_VETULET,[m
         "transform": transform,[m
         "width": width,[m
[31m-        "height": height[m
[32m+[m[32m        "height": height,[m
[32m+[m[32m        "dtype": "float32",[m
[32m+[m[32m        "nodata": NODATA,      # <-- EZ a lenyeg: megjeloljuk a nodata erteket[m
[32m+[m[32m        "compress": "lzw",     # tomorites, kisebb fajlmeret[m
     })[m
 [m
[31m-    # Létrehozzuk az új fájlt, és belemásoljuk az adatokat úgy,[m
[31m-    # hogy közben át is vetítjük EOV-ba[m
     with rasterio.open(dem_eov_path, "w", **kwargs) as dst:[m
         reproject([m
             source=rasterio.band(src, 1),[m
             destination=rasterio.band(dst, 1),[m
             src_transform=src.transform,[m
             src_crs=src.crs,[m
[32m+[m[32m            src_nodata=src.nodata,[m
             dst_transform=transform,[m
             dst_crs=CEL_VETULET,[m
[31m-            resampling=Resampling.bilinear[m
[32m+[m[32m            dst_nodata=NODATA,      # <-- a sarkok ezt kapjak 0 helyett[m
[32m+[m[32m            resampling=Resampling.bilinear,[m
         )[m
 [m
[31m-print(f"Kész! Az EOV-vetületű DEM itt található: {dem_eov_path}")[m
\ No newline at end of file[m
[32m+[m[32mprint("Kesz! Az EOV-vetuletu DEM itt talalhato:", dem_eov_path)[m
\ No newline at end of file[m
