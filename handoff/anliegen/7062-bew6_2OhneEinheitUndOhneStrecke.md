# BEW-6.2: Test ohne Einheit als Ebene und ohne Strecke durch die Nahkampfreichweite

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (ein Test prüft sein Kriterium nicht; Plan 9, Schritt 3).
`testBew6_2…` in [anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py)
trifft BEW-6.2 für ein einzelnes *Modell* mit dem Ziel in der *Nahkampfreichweite* (an der
Kopie mit der *Ausgangslage* vor dfe9a79 rot mit *Sperre* ‚Nahkampfreichweite‘, wie es soll).
Zwei Fälle, die das Kriterium wörtlich regelt, prüft kein Test:
1. „hält Arbiter die gezogenen *Modelle* … an, bevor eines darin ist“: Zieht ihr die Boyz
   als *Ebene* auf einen Gegner zu, halten alle um dieselbe Strecke an, sobald das vorderste
   1″ vor dessen *Base* steht. Ein Arbiter, der nur das vorderste *Modell* anhält und die
   übrigen weiterziehen lässt, oder nur den Warboss richtig anhält, bestünde den Test.
2. „auf der Strecke nach BEW-3.1 in *Nahkampfreichweite* … käme“: Das Ziel liegt im Test in
   der *Nahkampfreichweite*. Zieht jemand seitlich am Overlord vorbei, unter 1″ an dessen
   *Base* entlang, und lässt dahinter außerhalb los, muss Arbiter vorher anhalten. Ein
   Arbiter, der nur die *Stelle* des Loslassens prüft, bestünde den Test.

**Kosten.** Keine, wenn beide Tests mit „Tests zu Item anhaltenUndAuswahl“ kommen (BEW-6
gehört zu Item 3). Fehlen sie, ziehen am Bildschirm Boyz oder ein vorbeiziehendes *Modell*
in die *Nahkampfreichweite*, ohne dass ein Test rot wird; genau das wollte Anliegen 6400.

**Gegenvorschlag.** In `anhaltenVorDerGrenzeTest.py`, nach dem Muster von
`testBew3_1IstDieGanzeEinheitEbeneHältDerBlockAnDerBewegungsweiteAn`:
1. Die Boyz als *Ebene* mit `aufeinanderZuZiehen` vor den Overlord bringen, ein *Modell*
   ziehen, so dass das vorderste in die *Nahkampfreichweite* käme: jedes *Modell* um dieselbe
   Strecke versetzt, keines in *Nahkampfreichweite*, das vorderste nach
   `hältVorDerNahkampfreichweite`.
2. Den Warboss auf einer geraden Strecke innerhalb seiner *Bewegungsweite* am Overlord
   vorbeiziehen, deren nächster Punkt ½″ vor dessen *Base* liegt, Ziel außerhalb der
   *Nahkampfreichweite*: Er steht nach `hältVorDerNahkampfreichweite` auf der Strecke.

**Stellungnahme.** Angenommen, wie vorgeschlagen, in
[anhaltenVorDerGrenzeTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorDerGrenzeTest.py):
1. `testBew6_2IstDieGanzeEinheitEbeneHältDerBlockAnBevorEinesInDerNahkampfreichweiteIst`:
   Die Boyz als *Ebene*, gezogen wird das letzte *Modell*, das vorderste hält nach
   `hältVorDerNahkampfreichweite`, alle um dieselbe Strecke, keines in *Nahkampfreichweite*.
2. `testBew6_2ZiehtEinModellAufDerStreckeDurchDieNahkampfreichweiteHältArbiterEsDavorAn`:
   Der Warboss zieht ½″ an der *Base* des Overlords vorbei, Ziel außerhalb; er hält davor auf
   der Strecke.
