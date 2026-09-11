import fabdem

# Sorrend: (nyugat, del, kelet, eszak) - WGS84 fokokban.
# Ezeket a 01_adatminoseg_ellenorzes.py irta ki az EREDETI fajlhoz!
hatarok = (18.86402776666668, 46.36319445555555, 19.778749988888904, 46.85625001111111)   # <-- ird at a sajat ertekeidre

fabdem.download(
    hatarok,
    output_path="01_DATA/DEM/Kiskoros_FABDEM_raw.tif",
    show_progress=True,
)

print("FABDEM letoltve.")