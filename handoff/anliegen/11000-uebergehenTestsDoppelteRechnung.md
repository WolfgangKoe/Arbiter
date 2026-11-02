# Tests zum Übergehen: doppelte Rechnung, Vorrücken beendet das Angebot

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik an den Tests zu Item anhaltenUebergehen (Commit c9b1f22). Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Hilfsfunktionen und Randfälle, keine Prüfung rot,
jeder Test rot aus dem richtigen Grund.

1. `nachDemÜbergehenVorgerücktMit` in
   [weiterziehenNachDemUebergehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/weiterziehenNachDemUebergehenTest.py)
   rechnet die *Stelle* im Kreis des Wurfs selbst (Bewegungsweite + Radius + Wurf − ½″ unter
   dem Start). Dieselbe Regel steht in `unterDemLetztenModell` in
   [grenzen.py](../../technik/tests/akzeptanz/grenzen.py), dort von der jetzigen *Stelle*
   gemessen; darum passt `vorgerücktMit` nach dem Übergehen nicht. Die Bewegungsweite holen
   die Hilfen dreifach: `modell.bewegungsweite` (grenzen.py), `bewegungsweite(datenblatt,
   modellart)` und neu `bewegungsweiteDerModellart` ([schlacht.py](../../technik/tests/akzeptanz/schlacht.py)).
2. `testBew8_4DerDienstSetztDasModellAnDenPunktUndBeendetDasAngebot` schreibt
   `(float(ziel.x), float(ziel.y))` statt `stelleImSpielstand(ziel)` aus
   [dienst.py](../../technik/tests/akzeptanz/dienst.py).
3. `testBew8_3DieNächsteHandlungBeendetDasAngebot` prüft Loslassen und „Phase beenden“, nicht
   *Vorrücken*, das auf dem Happy Path neben dem Übergehen liegt (V18: jede Handlung ohne
   *Sperre* beendet das Angebot).

**Kosten.** Am Bildschirm nichts. 1 ändert sich die Regel des Wurfkreises, sind zwei Stellen
und drei Quellen nachzuziehen; 3 vergisst eine Handlung das Angebot zu beenden, merkt es kein Test.

**Gegenvorschlag.**
1. `unterDemLetztenModell` nimmt die *Stelle* vor dem Ziehen (aus `jetzigeStellen`), der Test
   nutzt dann `vorgerücktMit`; eine Quelle der Bewegungsweite, aus dem Katalog wie
   `bewegungsweiteDerModellart`, weil der Test den Wert nicht vom Produkt lesen soll.
2. `stelleImSpielstand(ziel)`.
3. `"vorrücken"` als dritte Handlung in die Parametrisierung.

**Stellungnahme.**
