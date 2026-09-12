import os
import time
from whitebox import WhiteboxTools

wbt = WhiteboxTools()
wbt.set_verbose_mode(False)
wbt.set_working_dir(os.path.abspath("02_PROCESSING"))

# A lejteshez a VALODI terep kell (feltoltes nelkul),
# a lefolyashoz a fix_flats=True valtozat.
DEM_NYERS = "Kiskoros_FABDEM_EOV.tif"
DEM_HIDRO = "Kiskoros_FABDEM_filled_flats.tif"

def lepes(szam, osszes, leiras, fuggveny, *argumentumok, **kulcsszavak):
    print(f"{szam}/{osszes}  {leiras} ...", end=" ", flush=True)
    kezdet = time.time()
    fuggveny(*argumentumok, **kulcsszavak)
    print(f"kesz ({time.time() - kezdet:.0f} mp)")

# 1. Lejtes fokban - meredek helyre nem epitunk tarozot
lepes(1, 5, "Lejtes", wbt.slope, DEM_NYERS, "lejtes_fok.tif", units="degrees")

# 2. D8 lefolyasirany - minden pixel a legmeredekebb szomszedjaba folyik
lepes(2, 5, "D8 lefolyasirany", wbt.d8_pointer, DEM_HIDRO, "d8_irany.tif")

# 3. D8 akkumulacio - hany pixel vize erkezik ide
lepes(3, 5, "D8 vizgyujto-akkumulacio", wbt.d8_flow_accumulation,
      DEM_HIDRO, "d8_akkumulacio.tif", out_type="cells")

# 4. FD8 fajlagos vizgyujto terulet - tobbiranyu lefolyas, lapos terepre realisabb
lepes(4, 5, "FD8 fajlagos vizgyujto terulet", wbt.fd8_flow_accumulation,
      DEM_HIDRO, "fd8_sca.tif", out_type="specific contributing area")

# 5. Topografiai nedvessegi index: ln(SCA / tan(lejtes))
lepes(5, 5, "Topografiai nedvessegi index (TWI)", wbt.wetness_index,
      "fd8_sca.tif", "lejtes_fok.tif", "twi.tif")

print("\nA terepelemzes elkeszult. Kimenetek a 02_PROCESSING mappaban:")
for f in ["lejtes_fok.tif", "d8_irany.tif", "d8_akkumulacio.tif",
          "fd8_sca.tif", "twi.tif"]:
    print(f"  - {f}")