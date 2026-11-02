# Gegner und eigene Modelle hin und zurück

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Wartet (Ablage und Form einer Hilfsrechnung, keine Prüfung rot), Kritik am Code
(Lesbarkeit) zur Umsetzung von Anliegen 8620 Punkt 1,
uncommittet.
1. `Schlacht._stellenMitGründen` in
   [schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py) sondert
   die Gegner als „nicht in `spieler.armee.modelle`“ aus, obwohl `gegnerVon` importiert ist
   und `grenzen` den Gegner so benennt. `Armee.modelle` ist eine Property, die je Aufruf ein
   `frozenset` baut; in der Comprehension geschieht das je *Modell* auf der Karte, zuvor
   einmal je Ziehen.
2. Danach rechnet `stellenMitGründenNachDemZiehen` in
   [bewegung/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py) daraus
   `eigene = stellen.keys() - gegner.keys()` zurück, und `inNahkampfreichweite` in
   `setzen.py` filtert mit `not in eigene` wieder die Gegner heraus: dreimal dieselbe
   Teilung, zweimal als Verneinung.

**Kosten.** Am Bildschirm nichts. Bleibt es, liest man an drei Stellen, wer Gegner ist, und
jedes Ziehen baut die eigenen *Modelle* so oft, wie *Modelle* auf der Karte stehen.
Änderung: drei Zeilen in `Schlacht`.

**Gegenvorschlag.** In `Schlacht._stellenMitGründen`
`gegner = gegnerVon(self._beideSpieler, spieler).armee.modelle` einmal, dann
`{modell: ort for modell, ort in self._stellen.items() if modell in gegner}`. Ob
`befundeDesSetzens` statt `eigene` die Gegner nimmt (berührt das Aufstellen), entscheidet der
Architekt; dann entfällt Punkt 2.

**Stellungnahme.**
