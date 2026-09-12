# Módszertani döntések naplója

> Ez a fájl minden lényeges választást rögzít **indoklással és dátummal**.
> A dolgozat „Anyag és módszer" fejezete közvetlenül ebből íródik majd.
> Minden új döntést ide vezess fel, amikor meghozod — utólag nem fogsz emlékezni, miért döntöttél így.

---

## D1 — Pilot terület: Duna–Tisza köze, Kiskőrös és térsége
**Dátum:** 2026.08.18

**Döntés:** A vizsgálat a Kiskunsági-homokhátság Kiskőrös központú részére irányul, Izsák (Kolon-tó), Kecel, Soltvadkert, Tabdi és Csengőd bevonásával.

**Indoklás:**
1. Helyismeret — a szerző Kiskőrösön él, ami segíti az eredmények szakmai értelmezését és terepi ellenőrzését.
2. A Kolon-tó (Kiskunsági Nemzeti Park) mintegy 15 km-re fekszik, ismert vízvisszatartási előzménnyel; kiváló validációs referenciapont.
3. Klasszikus Duna–Tisza közi aszályos terület, közvetlenül releváns a problémafelvetéshez.
4. Nincsenek nagy folyami tározók, így a feladat kisléptékű, elosztott beavatkozásokra irányul — nehezebb, de tudományosan érdekesebb, mint a Tisza-menti alternatíva.

**Elvetett alternatíva:** Tisza-menti vízgyűjtő (pl. Hármas-Körös). Előnye lett volna a VTT-tározókkal való közvetlen validáció, hátránya, hogy nem a homokhátsági aszályprobléma.

---

## D2 — Vetület: EOV (EPSG:23700)
**Dátum:** 2026.09.05

**Döntés:** Minden raszteres és vektoros réteg egységesen EOV-ba (Egységes Országos Vetület, EPSG:23700) kerül.

**Indoklás:** A globálisan elérhető domborzatmodellek WGS84-ben (EPSG:4326), fokokban érkeznek. Fokban végzett terület- és távolságszámítás torzít, és a pixel kelet–nyugati és észak–déli mérete is eltér. A 46,6° szélességen egy ívmásodperc kelet–nyugati irányban ~21 m, észak–déli irányban ~31 m. EOV-ban minden méteres és metrikus.

**Technikai megvalósítás:** `rasterio.warp.reproject`, bilineáris újramintavételezés, kényszerített 30 m-es négyzetes rács (`resolution=30`). Így minden pixel pontosan 900 m², ami a térfogatszámítást egyértelművé teszi.

---

## D3 — NoData explicit megjelölése
**Dátum:** 2026.09.05

**Döntés:** Az átvetítéskor `dst_nodata = -9999` beállítás.

**Indoklás:** Az EOV enyhén elfordul a földrajzi északhoz képest (a vizsgált területen ~0,3°), ezért a téglalap alakú WGS84-kivágat átvetítése után a kimeneti raszter sarkaiban üres háromszögek keletkeznek (a terület 0,97%-a, 37,5 km²). Alapértelmezetten ezek nulla értéket kapnának, amit a feltöltő algoritmus 100 m mély gödörként értelmezne, tönkretéve az egész elemzést. Az explicit nodata-jelöléssel ezek kimaradnak a számításból.

---

## D4 — Domborzatmodell: FABDEM V1-2 (DTM) a Copernicus GLO-30 (DSM) helyett
**Dátum:** 2026.09.10

**Döntés:** Az elsődleges elemzés a FABDEM V1-2 állományon fut; a Copernicus GLO-30 megmarad összehasonlításra.

**Indoklás:** A Copernicus GLO-30 felszínmodell (DSM), amely tartalmazza a növényzet és az épületek magasságát. A FABDEM ugyanebből az adatból készül, gépi tanulással eltávolított fa- és épületmagassággal (Hawker et al. 2022). A publikált validáció szerint sűrű lombkorona alatt a medián hiba 12,95 m-ről 0,45 m-re csökken.

**Miért kritikus ez itt:** A homokhátsági buckaközi mélyedések jellemzően 0,5–3 m mélyek. Egy 13 m-es adathibával a domborzat helyett a növényzet kerülne térképezésre — az erdőfoltok hamis gátakat képeznének, az erdősült mélyedések pedig eltűnnének.

**Mért igazolás a vizsgálati területen:**
- Átlagos DSM−DTM eltérés: 0,83 m
- Medián eltérés: 0,09 m
- 1 m feletti eltérés: a terület 21,5%-a (827 km²)
- 5 m feletti eltérés: a terület 6,1%-a (234 km²)

Az átlag és a medián közötti kilencszeres különbség kétarcú tájat jelez: a terület több mint fele nyílt mezőgazdasági felszín, ahol a két modell azonos, míg a fakorona-hatás koncentráltan, az erdő- és ültetvényfoltokon jelentkezik. Ez alátámasztja, hogy a DTM-re váltás nem kozmetikai, hanem szükségszerű.

**Ismert korlát:** A különbségtérkép −19,19 m-ig negatív értékeket is felvesz, ami fizikailag értelmezhetetlen. Oka a két állomány eltérő újramintavételezési útvonalából adódó szubpixeles regisztrációs hiba; a negatív értékek élek (épületszél, erdőszegély, csatornapart) mentén koncentrálódnak.

---

## D5 — Közös rács kikényszerítése
**Dátum:** 2026.09.12

**Döntés:** A FABDEM nem szabadon kerül átvetítésre, hanem a Copernicus EOV-állomány rácsgeometriájára (`dst_transform`, `dst_crs` a mesterfájlból).

**Indoklás:** A FABDEM 1°×1°-os csempékből áll össze, amelyek nem esnek egybe a Copernicus-kivágattal. Közös rács nélkül a két állomány nem vonható ki egymásból, és a későbbi rétegek (talaj, földhasználat) sem illeszthetők egységesen. A Copernicus EOV-fájl lett a „mester rács", amelyhez a projekt minden további rétege igazodik.

**Eredmény:** mindkét állomány 1836 × 2347 pixel, azonos határokkal és 30 m-es pixelmérettel.

---

## D6 — Kétféle mélyedés-feltöltés
**Dátum:** 2026.09.12

**Döntés:** A `fill_depressions` kétszer fut le, eltérő beállítással.

| Kimenet | `fix_flats` | Felhasználás |
|---|---|---|
| `..._filled.tif` | `False` | térfogatszámítás |
| `..._filled_flats.tif` | `True` | lefolyásirány, vízgyűjtő-akkumuláció |

**Indoklás:** A `fix_flats` kapcsoló apró mesterséges lejtést visz a feltöltés után keletkező tökéletesen lapos felületekre, hogy a lefolyásirány egyértelműen meghatározható legyen. A térfogatszámításnál viszont ez torzít: nagy lapos területeken a növekmények összeadódnak, és mélyedést mutatnának ott is, ahol nincs. A két felhasználásnak ezért külön állomány kell.

**Az alkalmazott algoritmus:** WhiteboxTools `fill_depressions`, amely a Wang–Liu, illetve Planchon–Darboux eljáráscsaládba tartozik. Ez bevált, évtizedek óta tesztelt módszer; újraimplementálása nem indokolt. A dolgozat saját algoritmikus hozzájárulása a 4–6. lépésben kezdődik.

---

## D7 — Térfogatszámítás és medence-definíció
**Dátum:** 2026.09.12

**Az algoritmus alapelve:**
```
mélység(x,y) = feltöltött_DEM(x,y) − eredeti_DEM(x,y)
térfogat(medence) = Σ mélység(x,y) × pixelterület
```
A feltöltött felszín a kifolyási pont (pour point) szintjéig tölti fel a mélyedést, így a különbség pontosan az a vízmennyiség, amely a mélyedésben megállna, mielőtt átbukna a legalacsonyabb peremen.

**Paraméterek és indoklásuk:**

| Paraméter | Érték | Indoklás |
|---|---|---|
| Kiterjedési küszöb | 0,05 m | Ennél mélyebb pixel tartozik egy medencéhez. Ez határozza meg a medence kiterjedését, nem a minősítését. |
| Minimális max. mélység | 0,50 m | Ennél sekélyebb mélyedés nem alkalmas tartós vízvisszatartásra, és a 30 m-es DEM függőleges pontossága sem támasztja alá. |
| Minimális pixelszám | 10 | 9 000 m² (0,9 ha) alatti foltok műtárgy-helyszínként nem értelmezhetők. |
| Szomszédsági szerkezet | 8-szomszédság | Az átlósan érintkező pixelek is egy medencéhez tartoznak, ami a természetes, szabálytalan alakú mélyedéseknek felel meg. |

**Kulcsfontosságú tervezési döntés — medencénkénti, nem pixelenkénti szűrés:** A mélységi küszöb nem pixelszinten kerül alkalmazásra, hanem a medence egészére (a legmélyebb pontja alapján). Pixelszintű vágás esetén egy valódi, 2 m mély medence sekély pereme levágódna, és a becsült térfogat alulbecsült lenne. Így a medence egészben marad, és csak a teljes objektum minősül.

**Széli medencék kezelése:** A terület szélét vagy a nodata-zónát érintő medencék valódi kiterjedése kilóg a vizsgált területből, így térfogatuk csonka. Ezeket az algoritmus megjelöli (`szelen_van = 1`), nem dobja el; az értelmezésnél külön kezelendők.

**Teljesítményi megjegyzés:** A medencénkénti statisztikák `numpy.bincount` alapon, egyetlen tömbolvasással készülnek. Ciklusban, medencénkénti maszkolással a futásidő nagyságrendekkel hosszabb lenne (11 112 medence × 4,3 millió pixel).

**Eredmény (2026.09.12):**
- 11 112 nyers medence
- 2 025 medence a szűrés után, ebből 53 széli
- 691 millió m³ összes becsült térfogat, 82 848 ha összes felület

---

## D8 — Első validáció: Kolon-tó
**Dátum:** 2026.09.12

**Megállapítás:** Az algoritmus a Kolon-tó medencéjét az 5. legnagyobb térfogatú mélyedésként azonosította (súlypont: EOV 672 718 / 157 896 ≈ 46,79°É 19,35°K; 20,1 millió m³, 2 117 ha, 2,5 m maximális mélység).

**Jelentősége:** Az eljárás kizárólag domborzati adatból, mindenféle előzetes hidrológiai vagy természetvédelmi információ nélkül megtalálta a terület egyik legismertebb természetes vizes élőhelyét, amely a Kiskunsági Nemzeti Park része és ismert vízszint-rehabilitációs előzménnyel rendelkezik. Ez az első független megerősítése annak, hogy a módszer valós tájelemekre mutat rá.

**Korlát:** A 2 117 ha meghaladja a tó mai kiterjedését, ami a P2 problémára (medence-összeolvadás) utal.

---

## NYITOTT KÉRDÉSEK — eldöntendő

### P1 — A vizsgálati terület újradefiniálása
**Felmerült:** 2026.09.12

A letöltött bounding box nyugati széle (18,864°) túlnyúlik a homokhátságon, bele a Duna-völgybe. Az első négy legnagyobb medencéből három (2., 3., 4. rang, összesen 183 millió m³ = a teljes térfogat 26%-a) a Duna árterében fekszik, és nem tárgya a vizsgálatnak. Kettő ráadásul széli, azaz csonka.

**Lehetséges megoldások:**
1. Vágás a hátsági peremvonal mentén (magassági küszöb vagy geomorfológiai határ alapján)
2. Vágás a kiválasztott települések közigazgatási határára (D1 szerint)
3. Hidrológiai vízgyűjtő lehatárolása lefolyás-akkumulációból

**Terv:** a terepelemzés (lejtés, lefolyás, akkumuláció) a **teljes kivágaton** fut le, hogy ne lépjenek fel peremhatások; a végleges határ ezután, a lefolyási adatok ismeretében kerül kijelölésre.

### P2 — Medence-összeolvadás
**Felmerült:** 2026.09.12

A legnagyobb medence 4 065 ha (40,6 km²), a 6. helyezett 3 255 ha-on mindössze 1,0 m maximális mélységgel. A lapos homokhátságon a szomszédos buckaközi mélyedéseket sekély nyergek kötik össze, amelyeken a feltöltő algoritmus átbukva egyetlen tájegység-méretű objektummá olvasztja őket. Ilyen méretű egység nem értelmezhető műtárgy-helyszínként.

**Lehetséges megoldások:** hierarchikus mélyedésbontás (nested depression analysis), többszintű küszöbölés, vagy vízválasztó-alapú szegmentálás a mélységfelszínen.

### P3 — Lechner DDM5 (5 m felbontás)
Jelenleg nem elérhető. Ha megszerezhető, a felbontásváltás 36-szoros pixelszám-növekedéssel jár (4,3 millióról 155 millióra), ami a vizsgálati terület szűkítését vagy csempés feldolgozást tesz szükségessé. Egyben lehetőséget ad egy felbontás-érzékenységi fejezetre.

### P4 — A „vízfolyástól való távolság" kritérium újragondolása
**Felmerült:** 2026.09.12

Az eredeti módszertani terv a vízfolyástól mért távolságot szerepeltette alkalmassági kritériumként. A homokhátság azonban nagyrészt **lefolyástalan (endorheikus)** táj: nincsenek természetes felszíni vízfolyások, a csapadék helyben gyűlik mélyedésekbe, majd elszivárog vagy elpárolog. A feltöltött DEM-ből kinyert „vízfolyás-hálózat" ezért részben mesterséges.

**Következmény:** a vízellátottság mérőszáma nem a folyótól mért távolság, hanem a **medence saját vízgyűjtő területe** (mennyi felszíni lefolyás érkezik bele) kell legyen. Ez a terepelemzés után számszerűsíthető.
