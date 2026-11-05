# Namen und Wiederverwendung in fliegen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), vorgemerkter Stand von Item fliegen, Abschnitt 1.
Wartet nach [Kritik](../../prozess/ablauf/kritik.md): Namen und Ablage, keine Prüfung rot.
1. In [messen.py](../../technik/arbiter/domaene/messen.py) sagen die Felder nicht, was sie
   bedeuten: `Kreisrand.darin` heißt „erlaubt ist das Innere“, `Geradenrand.inX` „die Gerade
   x = wert“, `aufwärts` „erlaubt ist die Seite mit größerem Wert“; der Leser erschließt es
   erst aus `_zulässig` und `_kreisMitGerade`.
2. `anteilVorDerLetztenBerührung` und `anteilBisZurBerührungAufDemWeg` bauen dieselben
   `paare` und denselben Schluss `Fraction(max(…, 0), schritte)`; `_ersterSchrittBis`
   wiederholt den Kern von `_ersterBerührenderSchritt` (innere Funktion
   `berührtBeiSchritt`, dann `ersterSchrittMit`).
3. In [fliegen.py](../../technik/arbiter/domaene/phasen/bewegung/fliegen.py) baut
   `_überdecktFremde` `_hindernisse(umgebung)` je *Modell* neu, und `_frei` läuft je
   Kandidat bis zu 65-mal; Kandidaten an derselben Stelle (Berührpunkt zweier Kreise:
   zwei Schnittpunkte und ein Lotpunkt) prüft `wegInDieFreieFläche` mehrfach.
4. [fliegenTest.py](../../technik/tests/einheit/domaene/phasen/bewegung/fliegenTest.py)
   bringt die achte gleiche `stelleAn`; dazu [8041](8041-stelleAnInDenEinheitstestsEinmal.md).

**Kosten.** Am Bildschirm nichts. 1 kostet jeden Leser der Geometrie Zeit; 2 ändert sich
an zwei Stellen, wenn sich das Raster ändert; 3 nur Laufzeit im Loslassen, findet
`wegInDieFreieFläche` keinen Weg. Umbau etwa 25 Zeilen.

**Gegenvorschlag.**
1. Sprechende Felder, etwa `Kreisrand(mitte, radius, innenErlaubt)` und
   `Geradenrand(senkrecht, wert, größerErlaubt)`.
2. Eine gemeinsame Hilfe für Paare und Schluss; `_ersterSchrittBis` und
   `_ersterBerührenderSchritt` teilen `berührtBeiSchritt`.
3. `hindernisse = _hindernisse(umgebung)` einmal je Aufruf; Kandidaten vor der Suche auf
   den gerundeten Punkt entdoppeln.
4. Mit 8041 erledigen.

**Stellungnahme.**
