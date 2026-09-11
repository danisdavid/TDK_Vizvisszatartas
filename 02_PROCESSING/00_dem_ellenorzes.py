import rasterio

# A DEM fájl elérési útja - a projekt gyökérmappájából nézve
dem_path = "01_DATA/DEM/Kiskoros_pilot_DEM_raw.tif"

# Megnyitjuk a fájlt olvasásra.
# A "with" gondoskodik róla, hogy a fájl a blokk végén automatikusan bezáródjon.
with rasterio.open(dem_path) as dem:

    print("===== DEM ALAPADATOK =====")
    print(f"Méret: {dem.height} sor x {dem.width} oszlop")
    print(f"Vetület (CRS): {dem.crs}")
    print(f"Pixelméret: {dem.res}")
    print(f"Sávok száma: {dem.count}")

    # Beolvassuk az 1. sávot (a magassági értékeket) egy táblázatba (numpy tömb)
    magassag = dem.read(1)

    print("\n===== MAGASSÁGI ÉRTÉKEK =====")
    print(f"Legalacsonyabb pont: {magassag.min():.1f} m")
    print(f"Legmagasabb pont:    {magassag.max():.1f} m")
    print(f"Átlagos magasság:    {magassag.mean():.1f} m")