import os
from whitebox import WhiteboxTools

wbt = WhiteboxTools()
wbt.set_verbose_mode(False)
wbt.set_working_dir(os.path.abspath("02_PROCESSING"))

# (bemenet, kimenet, fix_flats)
feladatok = [
    # Terfogatszamitashoz - TISZTA feltoltes, mesterseges lejtes nelkul
    ("Kiskoros_FABDEM_EOV.tif", "Kiskoros_FABDEM_filled.tif",       False),
    ("Kiskoros_DEM_EOV.tif",    "Kiskoros_DEM_filled.tif",          False),
    # Kesobbi lefolyas-elemzeshez - lapos reszeken kis lejtessel
    ("Kiskoros_FABDEM_EOV.tif", "Kiskoros_FABDEM_filled_flats.tif", True),
]

for bemenet, kimenet, flats in feladatok:
    print(f"Feltoltes: {bemenet}  ->  {kimenet}   (fix_flats={flats})")
    wbt.fill_depressions(dem=bemenet, output=kimenet, fix_flats=flats)
    print("   kesz\n")

print("Mind a harom feltoltes elkeszult.")