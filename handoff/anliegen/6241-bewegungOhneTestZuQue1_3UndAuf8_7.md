# Bewegungsphase: kein Test zu QUE-1.3 und AUF-8.7

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

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

**Stellungnahme.** Angenommen, Punkt 1 nach Plan 9 statt nach dem Gegenvorschlag.
1. Plan 9 („Abweichungen“, Anliegen 6400): In der *Bewegungsphase* hält Arbiter vor der
   *Nahkampfreichweite* an, statt nach QUE-1.3 zu sperren (BEW-6.2 „statt QUE-1.3“). Ein Test
   auf die *Sperre* ‚Nahkampfreichweite‘ widerspräche dem; darum
   `testBew6_2ZiehtEinModellInDieNahkampfreichweiteDesAnderenSpielersHältArbiterEsDavorAn` in
   [anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py):
   Der Warboss zieht auf einen *Abstand* von ½″ zum Overlord; er steht danach auf der geraden
   Strecke, über 1″ und höchstens 1/100″ mehr vor dessen *Base*, ohne *Sperre*. Vorgeschichte:
   Weil die *Distanz* ab Beginn der *Bewegungsphase* zählt, ziehen beide *Spieler* Zug um Zug
   aufeinander zu (`aufeinanderZuZiehen` in
   [schlacht.py](../../technik/tests/akzeptanz/schlacht.py)), bis 3″ *Abstand* bleiben. Rot,
   weil Arbiter heute ‚Nahkampfreichweite‘ sperrt (an einer Kopie mit der *Ausgangslage* vor
   dfe9a79 erprobt); im Arbeitsstand bricht er schon beim Laden der *Ausgangslage* ab (Item
   katalogwerteGliedern). BEW-6.1, 6.3, 6.4 folgen mit Item anhaltenUndAuswahl.
2. `testAuf8_7InDerBewegungsphaseFolgtEinModellDemWegDesZeigersUndNichtDemPunktUnterDemZeiger`
   in [ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py), mit
   `schlachtInDerBewegungsphase`, Griff abseits der Mitte, Maus und Finger; an derselben Kopie
   grün, das Verhalten besteht schon.
