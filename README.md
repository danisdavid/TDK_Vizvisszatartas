# TDK: Vízvisszatartási műtárgyak algoritmikus helyszín-optimalizálása

**Pilot terület:** Kiskőrös és térsége, Duna–Tisza köze
**Utolsó frissítés:** 2026.09.12

---

## Hol tart a projekt

| Fázis | Állapot |
|---|---|
| 1. Tervezés, adatgyűjtés | ✅ kész |
| 2. Fejlesztői környezet | ✅ kész |
| 3. DEM előfeldolgozás | ✅ kész |
| 4. Térfogat-analízis | ✅ kész (első saját algoritmus) |
| 5. Terepelemzés (lejtés, lefolyás, TWI) | 🔄 folyamatban |
| 6. Vizsgálati terület véglegesítése | ⏭️ következik |
| 7. Alkalmassági modell (MCDA + AHP) | ⬜ hátravan |
| 8. Optimalizálás (greedy + genetikus) | ⬜ hátravan |
| 9. Validáció | ⬜ hátravan |
| 10. Dolgozat írása | ⬜ hátravan |

---

## Eddigi eredmények

**Adatalap**
- Copernicus GLO-30 DSM és FABDEM V1-2 DTM, mindkettő EOV-ba (EPSG:23700) vetítve
- Közös rács: 1836 sor × 2347 oszlop, 30 × 30 m pixel, 3 878 km² befoglaló terület
- Érvényes adatterület: 4 267 468 pixel ≈ 3 841 km²

**DSM–DTM különbségelemzés**
- Átlagos eltérés 0,83 m, medián 0,09 m, szórástartomány −19,19 … +22,63 m
- 1 m feletti eltérés a terület 21,5%-án (827 km²)
- 5 m feletti eltérés a terület 6,1%-án (234 km²)

**Térfogat-analízis (FABDEM alapon)**
- 11 112 nyers mélyedés azonosítva
- Szűrés után (max. mélység ≥ 0,5 m ÉS ≥ 10 pixel): **2 025 medence**
- Ebből 53 érinti a terület szélét (csonka térfogatú)
- Összes becsült térfogat: 691 millió m³ / 82 848 ha
- ✅ **A Kolon-tó az 5. helyezettként azonosítva** (20,1 millió m³, 2 117 ha) — első sikeres validáció

---

## Ismert problémák

| # | Probléma | Hatás | Terv |
|---|---|---|---|
| P1 | A bounding box nyugati széle túlnyúlik a Duna-völgybe | A 2., 3., 4. legnagyobb medence a Duna ártere; a teljes térfogat 26%-a nem releváns | Vizsgálati terület újradefiniálása (6. fázis) |
| P2 | Medence-összeolvadás sekély nyergeken át | A legnagyobb medence 40,6 km², nem értelmezhető műtárgy-helyszínként | Hierarchikus mélyedés-bontás |
| P3 | Negatív DSM−DTM értékek élek mentén | Szubpixeles regisztrációs hiba | Dokumentálandó korlát, nem javítandó |
| P4 | Nincs még konzulens | Szakmai validáció hiányzik | Szeptemberi egyeztetés |

---

## Mappastruktúra

```
vs_code/
├── 01_DATA/DEM/              nyers letöltött domborzatmodellek
├── 02_PROCESSING/            előfeldolgozás, terepelemzés
│   ├── 00_dem_ellenorzes.py
│   ├── 00_dem_atvetites_eov.py
│   ├── 01_adatminoseg_ellenorzes.py
│   ├── 04_fabdem_kozos_racsra.py
│   ├── 05_dsm_dtm_kulonbseg.py
│   ├── 06_dem_feltoltes.py
│   └── 08_terepelemzes.py
├── 03_OPTIMIZATION/          medencék, alkalmassági modell, optimalizálás
│   ├── 07_terfogat_analizis.py
│   ├── 09_medence_diagnosztika.py
│   ├── medencek_FABDEM.csv
│   └── medencek_FABDEM.gpkg
├── 04_VALIDATION/            VTT és történelmi térképi validáció
├── 05_VISUALIZATION/         térképek, interaktív megjelenítés
├── 06_DOLGOZAT/              a dolgozat fejezetei
└── MODSZERTANI_DONTESEK.md   minden módszertani döntés indoklással
```

---

## Fontos fájlok

- **MODSZERTANI_DONTESEK.md** — minden választás és indoklása; ebből íródik majd az „Anyag és módszer" fejezet
- **PROJECT_BOARD.md** — feladatlista, határidők
- **medencek_FABDEM.csv** — a rangsorolt medencelista

---

## Adatforrások és idézési kötelezettségek

**FABDEM V1-2** (CC BY-NC-SA 4.0, nem kereskedelmi felhasználás)
> Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C. & Neal, J. (2022): A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters* 17(2), 024016.
> FABDEM is produced using Copernicus WorldDEM-30 © DLR e.V.

**Copernicus GLO-30** — OpenTopography portálon keresztül letöltve.

**WhiteboxTools** — nyílt forráskódú geoprocesszáló könyvtár, John Lindsay (University of Guelph).
