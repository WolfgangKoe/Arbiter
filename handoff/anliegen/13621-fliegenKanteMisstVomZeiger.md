# Fliegen: Kantentest misst vom Zeiger statt von der gezeigten Stelle

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `testBew18_2AnDerSpielfeldkanteRücktArbiterDieSpinneGanzInDasSpielfeld` in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py) misst „höchstens
1/100″ weiter“ von `punkt`, dem Zeiger außerhalb des *Spielfelds*. Die *Karte* zeigt die
Spinne aber an der *Spielfeldkante* (BEW-18.1, Architektur
[Fliegen](../../technik/architektur/vertrag/bewegung/fliegen.md): 18.2 rückt die *Stellen*
nach V10). Der Test zur *Bewegungsweite* misst richtig von `gezeigteStelle`. Von dort liegt
die nächste freie *Stelle* etwa 0,48″ entfernt (Nordschnittpunkt von Kante und Warrior-Kreis);
die Südstelle, die der Test erwartet (1,72″ vom Zeiger), ist von dort 3,1″ weit. Arbiter setzt
die Spinne frei, ganz im *Spielfeld*, an die nächste freie *Stelle* von der gezeigten aus; der
Test ist der einzige rote der 29.

**Kosten.** Der Test bleibt rot, obwohl BEW-18.2 nach Lesart der Architektur erfüllt ist; wer
ihn grün macht, ändert die Rechnung von der *Karte* weg.

**Gegenvorschlag.** Den erwarteten Weg von der gezeigten *Stelle* (Punkt auf der Kante auf der
Strecke von der Spinne zum Zeiger) rechnen statt von `punkt`.

**Stellungnahme.** Angenommen: 18.2 setzt 18.1 voraus, gerückt wird von der *Stelle*, an der
die *Karte* die Spinne zeigt, wie im Test zur *Bewegungsweite*. Die Nachrechnung ergab mehr:
Von der gezeigten *Stelle* liegt die nächste freie nicht an der *Spielfeldkante*, sondern
0,44″ weg vom Warrior mitten im *Spielfeld*; die Kante hielt nichts an, der Test hätte 18.2
an ihr nicht geprüft. Darum in
[fliegenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/fliegenTest.py),
`testBew18_2AnDerSpielfeldkanteRücktArbiterDieSpinneGanzInDasSpielfeld`: Der Warrior steht 2″
vor der Kante, so drückt er die Spinne gegen sie (Vorbedingung im Test geprüft, ebenso, dass die
gezeigte *Stelle* ihn *überdeckt*); erwartet wird der Schnitt von Kante und Warrior-Kreis,
gemessen von `gezeigteStelle` (0,26″; ohne die Kante wären es 0,23″ aus dem *Spielfeld*
hinaus). Der Test ist mit dem jetzigen Code grün, die Datei 29 von 29.
