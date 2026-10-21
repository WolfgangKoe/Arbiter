# seite.js wächst über dem Höchstmaß weiter

1542 · Kritik · von Architekt → Implementierer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code nach den Stellungnahmen zu 1540 und
[1550](1550-anhaltenStreifenUndHilfen.md). [seite.js](../../technik/frontend/seite.js) hat
12.227 Zeichen, bei [1541](1541-seiteJsTeilen.md) 12.124. Über dem Höchstmaß von 12.000
„wächst die Datei nicht“ ([Kennzahlen](../../prozess/kennzahlen.md#höchstmaße)); die
Stellungnahme zu 1550, Punkt 5, sagt dasselbe. Der Zuwachs liegt in `stelleBeimLoslassenAbfragen`:
`let nächster = null` und der Kommentar „Der wartende Punkt gehört zu seinem Zug …“ (101 Zeichen).
Nach [Ich 3](../../prozess/praemissen/ich.md) hält es auf: neuer Code verletzt ein Höchstmaß der
Architektur. Sonst nichts; `technik/tests` 724 grün, `prozess/pruefungen` 735 grün, `ruff` grün.

**Kosten.** Jedes weitere Item mit Oberfläche findet die Datei noch weiter über dem Maß; die
Teilung nach 1541 wird größer.

**Gegenvorschlag.** Nach deinem Urteil, etwa:
1. Übernahme und Folgeabfrage in den `finally`-Block, mit `const nächster`; `let nächster = null`
   entfällt. Wirft `fetch`, folgt dann trotzdem der jüngste Punkt.
2. Den Kommentar in die Regelzeile über `abfrageLäuft` ziehen: „V10, höchstens eine Abfrage
   zugleich, danach nur mit dem jüngsten Punkt seines Zugs“.

Erledigt: `seite.js` höchstens 12.124 Zeichen (`wc -m`), Bildschirmtests grün, Verhalten
unverändert außer der Folgeabfrage nach einem Fehler in 1.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt. Die Folgeabfrage steht im `finally`-Block
mit `const nächster`, der Kommentar ist in die Regelzeile über `abfrageLäuft` gezogen („… jüngsten
Punkt seines Zugs“). Dazu entfällt `const kreis`, denn `gezogen` wird vor dem ersten `await`
gelesen; `modellPfad(gezogen)` ist gleichwertig. Ein Fehler von `fetch` wird mit `catch` abgefangen
([1551](1551-haltOhneHaltUndUngepruefteRaender.md), Punkt 3), die Folgeabfrage läuft dennoch.
`seite.js` hat 12.124 Zeichen (`wc -m`).
