import os
from whitebox import WhiteboxTools

wbt = WhiteboxTools()
wbt.set_verbose_mode(False)

# A WhiteboxTools abszolut utvonalakkal dolgozik, ezert megadjuk a munkakonyvtarat
munkakonyvtar = os.path.abspath("02_PROCESSING")
wbt.set_working_dir(munkakonyvtar)
print("Munkakonyvtar:", munkakonyvtar)

# Melyik DEM-et toltsuk fel? Cserelheto a masik modellre is.
bemenet = "Kiskoros_FABDEM_EOV.tif"
kimenet = "Kiskoros_FABDEM_filled.tif"

print("Feltoltes indul... ez 1-3 percig tarthat.")

wbt.fill_depressions(
    dem=bemenet,
    output=kimenet,
    fix_flats=True,     # a keletkezo teljesen lapos reszeket is kezeli
)

print("Kesz:", os.path.join(munkakonyvtar, kimenet))