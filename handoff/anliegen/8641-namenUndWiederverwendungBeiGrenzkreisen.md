# Namen und Wiederverwendung bei Grenzkreisen

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet (Namen und Ablage von Hilfsfunktionen, keine Prüfung rot), Stand
4b2f2ec, Item grenzkreise.
1. `_einheitMitGrenzen` in
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) liefert
   die *ausgewählte* *Einheit* des *Spielers* *am Zug* in der *Bewegungsphase* (BEW-5.1,
   11.1) und entscheidet auch, ob „Vorrücken“ angeboten ist; der Name nennt nur die
   Grenzkreise. `vorrücken` und `vorrückenZurücknehmen` prüfen dieselbe Bedingung über die
   Eigenschaft ein zweites Mal und reichen dann `self._auswahl.einheit` weiter, das
   `Einheit | None` ist.
2. [grenze.js](../../technik/frontend/komponenten/grenze.js): `kennung` gibt den Einträgen
   der *Nahkampfreichweite* `…-bewegung` als Kennung; die Vorlage in
   [index.html](../../technik/frontend/index.html) heißt `grenzeBoyz`, nach einer
   Testeinheit.
3. `grenze` setzt Breite und Länge der Maske von Hand wie `flächeSetzen` in
   [karte.js](../../technik/frontend/komponenten/karte.js).

**Kosten.** Am Bildschirm nichts. Ein Leser sucht hinter „mit Grenzen“ eine Bedingung, die
es nicht gibt, und eine Bewegung hinter der Kennung eines Gegners. Umbau: etwa 15 Zeilen in
drei Dateien.

**Gegenvorschlag.**
1. `_ausgewählteEinheitAmZug`; `vorrücken` und `vorrückenZurücknehmen` holen die *Einheit*
   einmal daraus und rufen mit ihr `self._bewegungsphase.vorrückenBeginnen(einheit)` bzw.
   prüfen `vorrückenZurücknehmenAngeboten(einheit)`.
2. Die Kennung der Maske aus der Stelle in der Liste: `karte` gibt `grenze` die Nummer des
   Eintrags, `grenze-${nummer}`; die Vorlage heißt neutral `grenze`.
3. `flächeSetzen` nach [vorlage.js](../../technik/frontend/komponenten/vorlage.js) und in
   `grenze` für Maske und Rechteck aufrufen.

**Stellungnahme.**
