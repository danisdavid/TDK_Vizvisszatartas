import rasterio
import numpy as np


utvonalak = {
    "Copernicus (EOV)": "02_PROCESSING/Kiskoros_DEM_EOV.tif",
    "FABDEM (EOV)":     "02_PROCESSING/Kiskoros_FABDEM_EOV.tif",
}

for nev, ut in utvonalak.items():
    with rasterio.open(ut) as dem:
        adat = dem.read(1)

        print(f"--- {nev} ---")
        print(f"  Megjelolt nodata ertek: {dem.nodata}")
        print(f"  Pixelmeret: {dem.res}")
        print(f"  Legkisebb ertek: {adat.min():.2f}")
        print(f"  Legnagyobb ertek: {adat.max():.2f}")

        # Hany pixel gyanusan alacsony? (a teruleten 70 m alatt nincs valodi terep)
        gyanus = np.sum(adat < 70)
        print(f"  70 m alatti pixelek: {gyanus} db ({gyanus / adat.size * 100:.2f}%)")

        # A hatarolo teglalap - ezt hasznaljuk majd a FABDEM letoltesehez
        print(f"  Hatarok: {dem.bounds}")
        print(f"  Meret (szelesseg x magassag): {dem.width} x {dem.height}")
        print()