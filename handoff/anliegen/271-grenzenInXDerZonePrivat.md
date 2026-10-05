# grenzenInXDerZone wird privat

271 · Kritik · von Architekt (Technik) → Implementierer · Runde 1/3 · offen

## Runde 1
**Befund.** Folge aus 269 (Schnittstelle): Seit 50ab353 importiert kein Test mehr
`grenzenInXDerZone` aus `technik/arbiter/domaene/phasen/aufstellen.py`; der einzige Aufrufer
ist `Ausgangslage.grenzenDerZone` in derselben Datei. Die Funktion ist trotzdem öffentlich.
Wer `aufstellen` liest oder importiert, sieht damit zwei Wege zur Fläche einer
*Aufstellungszone*. Einer verlangt `breite` und `tiefe` und lässt den Aufrufer die Fläche
selbst zusammensetzen. Genau das hat 263 aus `web/` entfernt. Daneben steht
`_teilenSichArmeeOderModell`: Dort zeigt der Unterstrich schon, was nur das Modul braucht.

**Kosten.** Eine Umbenennung in zwei Zeilen, kein Test ändert sich. Ohne sie bleibt die
Schnittstelle der Phase um eine Funktion größer, und der nächste Aufrufer kann wieder am
Glossarbegriff vorbei rechnen.

**Gegenvorschlag.** `grenzenInXDerZone` heißt `_grenzenInXDerZone`. Erledigt, wenn außerhalb
von `aufstellen.py` niemand sie importiert (grep) und `python3 -m pytest technik/tests` grün
ist.

**Stellungnahme.**
