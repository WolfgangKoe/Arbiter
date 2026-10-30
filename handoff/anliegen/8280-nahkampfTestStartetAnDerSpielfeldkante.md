# Test BEW-2.8 zur Nahkampfreichweite zieht aus dem Spielfeld

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** In
[sperrenBeimZiehenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/sperrenBeimZiehenTest.py)
bleibt `testBew2_8HältArbiterVorDerNahkampfreichweiteAnPrüftQue1NurDieStelleDesAnhaltens`
rot, obwohl BEW-6.2 umgesetzt ist (alle anderen 20 Tests der Datei grün). Der Warboss
steht nach `aufeinanderZuZiehen` bei y = 100/127 = Radius, seine *Base* liegt also genau an
der *Spielfeldkante*; der Overlord steht bei y = 80/127. Der Test setzt den Warboss auf die
*Stelle* des Overlords, der Weg hat damit dy = -20/127 und führt aus dem *Spielfeld*.
BEW-6.1 und 6.3 (kürzeste Strecke) halten ihn deshalb schon beim ersten Schritt an, nach
BEW-6.2 allein hielte er bei 207/458 des Wegs. Der Test verlangt das Anhalten vor der
*Nahkampfreichweite*, das die Regeln zusammen nicht hergeben.

**Kosten.** Der Test bleibt rot; DoD 1 für das Item anhaltenUndAuswahl ist offen. Ich
ändere weder Test noch Regel.

**Gegenvorschlag.** Den Test so stellen, dass der Weg im *Spielfeld* bleibt: die Modelle
in `aufeinanderZuZiehen` auf gleicher y-Linie ziehen oder in der Mitte des *Spielfelds*
beginnen, oder als Ziel eine *Stelle* mit gleichem y wie der Warboss nehmen.

**Stellungnahme.**
