# Weiche für Flieger in der Bewegungsphase einfacher

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** Kritik am Code (Lesbarkeit), Item fliegen, Abschnitt 2. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Vereinfachung, Namen und Hilfsfunktionen, keine
Prüfung rot (ruff, complexipy grün).
1. Schalter statt Weiche: `_gründe(…, mitBaseÜberdeckt=True)` ist nur `gründeBeimZiehen`;
   `Schlacht._stellenMitGründen(…, losgelassen=True)` wählt per Schalter die Methode, die
   `modellLoslassen` selbst aufrufen könnte. In `stellenMitGründenNachDemLoslassen` rechnet
   der Aufruf der Ziehen-Variante für Flieger *Gründe*, die gleich verworfen werden.
2. `fremde = {anderes: ort … if anderes not in ebene}` steht viermal in
   [\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/bewegung/__init__.py).
3. `Weite` und `_inDerWeite` in `fliegen.py` wiederholen `_distanzÜberDerBewegungsweite`
   (`bewegungsweite + vorrückwurf`, Abstand im Quadrat) aus `anhaltenAnDerBewegungsweite.py`;
   `Fraction(modell.bewegungsweite + vorrückwurf)` umhüllt schon eine `Fraction`.
4. Gleichnamiges `anteilBisZurNahkampfreichweite` in `fliegen.py` und
   `anhaltenVorDerGrenze.py`, darum der Alias `…DesFliegers` beim Import.
5. `abstandsquadrat` in `bewegungsphaseTest.py` baut `messen.abstandImQuadrat` nach.

**Kosten.** Am Bildschirm nichts. Leser folgen Schaltern über drei Methoden; die Regel
„Bewegungsweite plus Vorrückwurf“ ändert sich an zwei Stellen. Umbau etwa 25 Zeilen.

**Gegenvorschlag.**
1. Loslassen ruft `gründeBeimZiehen` direkt; `modellLoslassen` ruft
   `stellenMitGründenNachDemLoslassen` direkt, ohne `losgelassen`.
2. Eine Hilfe `_fremde(stellen, ebene)`.
3. Eine gemeinsame Funktion für die Weite eines *Modells*, die beide nutzen.
4. Die Funktion in `fliegen.py` nach ihrer Aufgabe benennen, etwa
   `anteilVorDerNahkampfreichweiteBisZumEnde`; dann ohne Alias.
5. `messen.abstandImQuadrat` nutzen.

**Stellungnahme.**
