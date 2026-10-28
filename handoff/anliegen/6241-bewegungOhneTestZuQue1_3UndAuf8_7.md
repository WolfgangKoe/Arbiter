# Bewegungsphase: kein Test zu QUE-1.3 und AUF-8.7

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Lücken abseits des Happy Path; alle Akzeptanztests grün).
1. BEW-1.5: „es sperren nur QUE-1 und BEW-2“. In der *Bewegungsphase* prüfen die Tests
   QUE-1.2 (‚Base überdeckt‘, `sperrenBeimZiehenTest.py`), aber nicht QUE-1.3. Der Code sperrt
   ‚Nahkampfreichweite‘ dort schon (`befundeDesSetzens` in `technik/arbiter/domaene/querschnitt/__init__.py`),
   Plan 8 führt *Nahkampfreichweite* unter „Noch nicht“.
2. AUF-8.7 (Anliegen 6100 F1 A: „in *Aufstellung* und *Bewegungsphase*“) prüft
   `testAuf8_7…` ([ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py))
   nur in der *Aufstellung*; die Tests der *Normalen Bewegung* greifen jedes *Modell* in der Mitte.

**Kosten.** Keine in Zyklus 8. Bleibt es, fällt ein Bruch beider Fälle in der
*Bewegungsphase* keinem Test auf; am Bildschirm sperrt Arbiter ‚Nahkampfreichweite‘, ohne
dass ein Test es belegt.

**Gegenvorschlag.** 1: ein Test in `sperrenBeimZiehenTest.py` (oder `normaleBewegungTest.py`),
der ein *Modell* in der *Bewegungsphase* innerhalb seiner *Bewegungsweite* bis auf unter 1″
an ein *Modell* des anderen *Spielers* zieht: *Sperre* ‚Nahkampfreichweite‘, Stand wie davor.
2: `testAuf8_7…` zusätzlich mit `schlachtInDerBewegungsphase` (Griff abseits der Mitte, Maus
und Finger).

**Stellungnahme.**
