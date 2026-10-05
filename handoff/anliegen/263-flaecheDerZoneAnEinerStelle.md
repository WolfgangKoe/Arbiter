# Wo eine Aufstellungszone liegt, an einer Stelle

263 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Kritik am Code von 488d8da (Schnitt). Wo eine *Aufstellungszone* liegt, wird an
drei Orten zusammengesetzt:
1. Domäne, `Aufstellung._nichtGanzInDerZone`: x aus `grenzenInXDerZone(zone, breite,
   tiefen[zone])`, y als `(Fraction(0), länge)`.
2. `web/darstellung.py`, `_zone`: holt dafür `spielfeld.seitenlängen` und `tiefen[zone]` aus
   `aufstellung.ausgangslage` und ruft `grenzenInXDerZone` noch einmal; y fehlt.
3. `frontend/seite.js`, `karte`: `y: 0, height: länge`. Dass die Zone über die ganze Länge
   reicht, weiß damit das Frontend.

Ein Beispiel: Die Mission ändert sich, und die Zonen liegen an den kurzen Kanten. Dann
ändern sich Domäne, `darstellung.py` und `seite.js`, und vergisst man eine Stelle, prüft der
Validator eine andere Zone, als die Karte zeigt. Die Ursache steht in meinem eigenen Text:
W2 ([Web](../../technik/architektur/web.md)) nennt `grenzenInXDerZone` als Quelle der
Längen. Das ist nur die halbe Fläche. Vorbild aus dem Altbestand ist
`ArbiterMap/backend/app/domain/rule_checks.py`: Dort rechnet nur die Domäne, `app/services/`
übersetzt bloß Datensätze in `ModelState`. Bei uns rechnen die äußeren Schichten mit.

**Kosten.** Rund zehn Zeilen in drei Dateien, kein Akzeptanztest ändert sich: QUE-2.3
prüft die Attribute des `rect`, nicht ihre Herkunft. Ohne die Änderung bleibt jede neue
Zone eine Änderung an drei Orten in zwei Sprachen. Das Item blockiert es nicht.

**Gegenvorschlag.**
1. Die Domäne liefert die ganze Fläche, zum Beispiel als Abfrage der `Ausgangslage`:
   `ausgangslage.grenzenDerZone(zone) -> (grenzenInX, grenzenInY)`. Das ist genau die Form,
   die `messen.ganzIn` erwartet. `_nichtGanzInDerZone` wird zu
   `messen.ganzIn(modell.base, stelle, *self._ausgangslage.grenzenDerZone(zone))`.
   `grenzenInXDerZone` wird privat. Den Namen wählst du. Ein Begriff des Glossars wird er
   nicht, er sagt nur, wo *Aufstellungszone* im Code liegt.
2. `darstellung._zone` gibt `{"x", "y", "breite", "länge", "spieler"}`, so wie
   `spielfeld`. `seite.js` zeichnet Spielfeld und Zone dann mit denselben vier Werten und
   weiß nicht mehr, dass die Zone ein Streifen ist.
3. Danach ersetze ich in W2 „`grenzenInXDerZone`“ durch die neue Abfrage.

Erledigt, wenn außerhalb von `phasen/aufstellen.py` niemand mehr die Fläche einer Zone
zusammensetzt (`web/` ruft nur die Abfrage, `seite.js` setzt kein festes `y`) und
`python3 -m pytest technik/tests` grün ist.

**Stellungnahme.** Umgesetzt wie vorgeschlagen. `Ausgangslage.grenzenDerZone(zone)` (`phasen/aufstellen.py`) liefert die Grenzen in x und y; `_nichtGanzInDerZone` und `darstellung._zone` rufen nur sie, `_zone` gibt `x, y, breite, länge`, `seite.js` setzt kein festes `y` mehr. `grenzenInXDerZone` bleibt öffentlich, weil `auf4Test.py` (gesperrt) es importiert; außerhalb von `aufstellen.py` ruft es kein Produktcode mehr. Alle Tests grün. Der JSON-Schlüssel `tiefe` entfällt, W2 ist deine Sache.
