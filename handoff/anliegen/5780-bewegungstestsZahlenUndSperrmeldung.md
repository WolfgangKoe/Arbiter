# Bewegungstests: B als Zahl, Indizes, Sperrmeldung ohne Text

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3). Lauf über `phasen/bewegung`: 50 rot, nur weil Produktcode fehlt;
ruff und Formregeln grün.

1. Ein Test prüft sein Kriterium nicht:
   [beendenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/beendenTest.py),
   `testBew4_1DieSeiteNenntBeimKlickAufPhaseBeendenDenGrundKeineKohärenz` prüft nur
   `assert sperrmeldungWarten(…)`. Das ist wahr, sobald irgendeine eine Meldung dasteht
   (`to_have_count(1)`). ‚über eine Base‘ statt ‚keine Kohärenz‘ wäre auch grün.
2. Eine Zahl steht für den Begriff *B* (Es: der Name trägt die Bedeutung). In
   [anhaltenAmBTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenAmBTest.py)
   heißen zwei Tests „genau so weit wie sein B“, ziehen aber `fünfZoll`. Ändert sich das *B*
   des Warboss in `ausgangslage.yaml`, bleiben sie grün und prüfen „genau B“ nicht mehr.
   Genauso hängt „weiter als B“ an der Zahl: `sechsZoll`, `zehnZoll` (BEW-3.1, Dienst,
   Seite) und `zuWeitNachOsten` in
   [normaleBewegungTest.py](../../technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py).
   Die gelöschten Tests zu BEW-2.1 nahmen `bewegungsweite("Warboss")`.
3. Indizes auf Fachobjekte (Es 6): `schrägOhneHindernis[0]`, `[1]` in zwei Tests zu BEW-3.1;
   `einigeZoll[0]` und `gezeigt[0]`, `[1]` in normaleBewegungTest.py.
4. `testBew1_7DieKarteZeigtBeimHaltenWeiterAlsBDasModellAmBOhneSperrmeldung` rechnet im
   Prüfblock fünf Zeilen Geometrie mit `hypot`. Dabei steht `hundertstel = 0.01` ein zweites
   Mal, neben `hundertstelZoll` in
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py) (Wir 3). In `testBew1_6…` steht
   eine Annahme über die Testdaten (`2 * einigeZoll[0] > B`) im Prüfblock, nicht im Aufbau
   (T1, 4).

**Kosten.** Etwa 20 Zeilen, keine neue Fixture. Ohne Punkt 1 ist BEW-4.1 am Bildschirm
mit jeder Sperrmeldung grün. Ohne Punkt 2 prüfen die Tests nach einer Änderung der Daten
still etwas anderes.

**Gegenvorschlag.**
1. `assert sperrmeldungWarten(seite, gründe) == gründeAlsText(gründe)` wie in
   sperrenBeimZiehenTest.py.
2. `bewegungsweite("Warboss")` für „genau B“, `bewegungsweite("Warboss") + 1` für „weiter als
   B“; schräg als `gestreckt(schrägOhneWurzel, …)`.
3. Ein Handgriff `gestreckt(weg, faktor)` in `handgriffe.py` neben `versetzt`, sonst
   Entpacken (`gezeigtX, gezeigtY = gezeigt`).
4. Ein Handgriff in `ziehen.py` neben `liegtEinPixelGenauAn`, etwa
   `hältAmBAufEinenPixelGenau(seite, davor, gezeigt, bewegungsweite)`. Er nimmt
   `hundertstelZoll` und die Toleranz nach Tests B5. Die Annahme in `testBew1_6…` gehört in
   den Aufbau oder entfällt, wenn der Weg aus `bewegungsweite` folgt.

Stellungnahme: Alle vier Punkte angenommen. 1: BEW-4.1 vergleicht mit `gründeAlsText`.
2: `bewegungsweite(…)` und `+ 1` statt Zahlen, schräg mit neuem Handgriff `gestreckt`
(handgriffe.py). 3: keine Indizes mehr. 4: Handgriff `hältAmBAufEinenPixelGenau` in ziehen.py
(nutzt `hundertstelZoll`); die Annahme in BEW-1.6 entfällt, der Weg folgt aus `bewegungsweite`.
