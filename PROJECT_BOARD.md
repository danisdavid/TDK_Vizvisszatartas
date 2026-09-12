# Feladatlista

**Frissítve:** 2026.09.12
Jelölés: ✅ kész · 🔄 folyamatban · ⬜ hátravan · ⚠️ akadály

---

## 1. FÁZIS — Tervezés és adatgyűjtés ✅

| | Feladat | Megjegyzés |
|---|---|---|
| ✅ | Pilot terület kiválasztása | Kiskőrös és térsége, Duna–Tisza köze |
| ✅ | Copernicus GLO-30 letöltése | OpenTopography, 3 878 km² |
| ✅ | FABDEM V1-2 letöltése | `fabdem` Python-csomag |
| ⚠️ | Lechner DDM5 hozzáférés | Nem elérhető; konzulensen keresztül újrapróbálni |
| ⬜ | CORINE Land Cover 2018 | Az alkalmassági modellhez kell |
| ⬜ | Talajadatok (AGROTOPO / DOSZTIK) | Beszivárgási kritériumhoz |
| ⬜ | OVF vízhálózat, csatornák | Duna-völgyi-főcsatorna, belvízcsatornák |
| ⬜ | Természetvédelmi területek (Natura 2000, KNP) | Kizáró kritérium |
| ⬜ | Közigazgatási határok | Területlehatároláshoz |

---

## 2. FÁZIS — Fejlesztői környezet ✅

| | Feladat |
|---|---|
| ✅ | Python 3.12 + venv |
| ✅ | rasterio, numpy, scipy, geopandas, matplotlib, folium, pandas |
| ✅ | whitebox (WhiteboxTools) |
| ✅ | fabdem |
| ✅ | QGIS |
| ✅ | VS Code + Python bővítmény |
| ✅ | Git + GitHub repó |
| ⬜ | `requirements.txt` kiírása (`pip freeze > requirements.txt`) |

---

## 3. FÁZIS — DEM előfeldolgozás ✅

| | Feladat | Szkript |
|---|---|---|
| ✅ | DEM alapadatok ellenőrzése | `00_dem_ellenorzes.py` |
| ✅ | Átvetítés EOV-ba, 30 m-es négyzetes rácsra | `00_dem_atvetites_eov.py` |
| ✅ | NoData helyes megjelölése | ugyanott |
| ✅ | Adatminőség-ellenőrzés | `01_adatminoseg_ellenorzes.py` |
| ✅ | FABDEM közös rácsra igazítása | `04_fabdem_kozos_racsra.py` |
| ✅ | DSM−DTM különbségtérkép | `05_dsm_dtm_kulonbseg.py` |
| ✅ | Mélyedés-feltöltés (2 változat) | `06_dem_feltoltes.py` |

---

## 4. FÁZIS — Térfogat-analízis ✅

| | Feladat | Szkript |
|---|---|---|
| ✅ | Mélyedés-mélység pixelenként | `07_terfogat_analizis.py` |
| ✅ | Összefüggő medencék klaszterezése | ugyanott |
| ✅ | Medencénkénti térfogat, terület, mélység | ugyanott |
| ✅ | Széli medencék megjelölése | ugyanott |
| ✅ | Export: CSV, GeoPackage, GeoTIFF | ugyanott |
| ✅ | Kolon-tó validáció | 5. helyezett ✅ |

---

## 5. FÁZIS — Terepelemzés 🔄

| | Feladat | Szkript |
|---|---|---|
| 🔄 | Medence-diagnosztika (hol vannak?) | `09_medence_diagnosztika.py` |
| 🔄 | Lejtés (fok) | `08_terepelemzes.py` |
| 🔄 | D8 lefolyásirány | ugyanott |
| 🔄 | D8 vízgyűjtő-akkumuláció | ugyanott |
| 🔄 | FD8 fajlagos vízgyűjtő terület | ugyanott |
| 🔄 | Topográfiai nedvességi index (TWI) | ugyanott |
| ⬜ | Medencénkénti vízgyűjtő terület számítása | új szkript |

---

## 6. FÁZIS — Vizsgálati terület véglegesítése ⬜

| | Feladat | Megjegyzés |
|---|---|---|
| ⬜ | A Duna-völgyi rész leválasztása | P1 probléma |
| ⬜ | Hátsági peremvonal meghatározása | magassági vagy geomorfológiai alapon |
| ⬜ | Végleges maszk elkészítése | minden réteg erre vágva |
| ⬜ | Térfogat-analízis újrafuttatása a végleges területen | |

---

## 7. FÁZIS — Medence-finomítás ⬜

| | Feladat | Megjegyzés |
|---|---|---|
| ⬜ | Összeolvadt medencék bontása | P2 probléma |
| ⬜ | Meglévő állóvizek kiszűrése | a tavak már vizesek, nem építendő helyszínek |
| ⬜ | Végleges medencekatalógus | |

---

## 8. FÁZIS — Alkalmassági modell (MCDA + AHP) ⬜

| | Feladat |
|---|---|
| ⬜ | Kritériumok véglegesítése |
| ⬜ | AHP párosítási mátrix felépítése |
| ⬜ | Súlyok számítása sajátvektorral |
| ⬜ | Konzisztencia-arány (CR) ellenőrzése |
| ⬜ | Kritériumrétegek normalizálása 0–1 közé |
| ⬜ | Súlyozott alkalmassági térkép |

---

## 9. FÁZIS — Optimalizálás ⬜

| | Feladat |
|---|---|
| ⬜ | Költségmodell felállítása |
| ⬜ | Mohó (greedy) heurisztika |
| ⬜ | Genetikus algoritmus |
| ⬜ | Futásidő és megoldásminőség összehasonlítása |
| ⬜ | Érzékenységi vizsgálat (költségvetés ±20%) |

---

## 10. FÁZIS — Validáció ⬜

| | Feladat |
|---|---|
| ⬜ | Kolon-tó részletes összevetés |
| ⬜ | Történelmi térképek (MAPIRE, katonai felmérések) |
| ⬜ | DSM vs. DTM érzékenységi vizsgálat |
| ⬜ | Meglévő vizes élőhelyekkel való egyezés |

---

## 11. FÁZIS — Vizualizáció ⬜

| | Feladat |
|---|---|
| ⬜ | Térképsorozat (matplotlib / QGIS export) |
| ⬜ | Interaktív folium-térkép |
| ⬜ | Ábrák a dolgozathoz |

---

## 12. FÁZIS — Dolgozat ⬜

| | Fejezet |
|---|---|
| ⬜ | Bevezetés |
| ⬜ | Irodalmi áttekintés |
| ⬜ | Anyag és módszer (a MODSZERTANI_DONTESEK.md alapján) |
| ⬜ | Eredmények |
| ⬜ | Megvitatás |
| ⬜ | Következtetések |
| ⬜ | Irodalomjegyzék, mellékletek |
| ⬜ | Kivonat (magyar + angol) |

---

## Egyéb, nem technikai

| | Feladat | Határidő |
|---|---|---|
| ⚠️ | **Konzulens felkérése** | szeptember eleje — ez a legsürgősebb |
| ⬜ | TDK jelentkezési határidő megkeresése | |
| ⬜ | Irodalomkutatás indítása (GIS-MCDA site selection) | |
