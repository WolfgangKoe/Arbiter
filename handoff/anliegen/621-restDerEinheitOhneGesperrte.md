# Test zu AUF-14.1 prüft nicht, dass der Rest in der Ablage bleibt

621 · Kritik · von Reviewer → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** `testAuf14_1EineEinheitMitGesetztemUndNichtGesetztemModellBekommtGenauEinModellDazu`
in `technik/tests/akzeptanz/phasen/aufstellen/restDerEinheitTest.py` zählt nur die
*gesetzten* *Modelle*. Ich habe den Code probeweise so geändert, dass beim Ziehen einer
angefangenen *Einheit* alle nicht *gesetzten* *Modelle* an die *Stelle* des Loslassens
kommen: Das erste wird *gesetzt*, die übrigen bleiben *gesperrt* stehen (Base überdeckt).
Der Test blieb grün; erst ein Test zu AUF-12.4 wurde rot. AUF-14.1 verlangt „genau eines
ihrer nicht *gesetzten* *Modelle*“; die anderen bleiben in der *Ablage*.

**Kosten.** Ein Fehler, bei dem der Spieler nach dem Ziehen neun *gesperrte* Boyz auf der
*Karte* sieht, fiele im Test zu seinem Kriterium nicht auf, nur zufällig in einem anderen.

**Gegenvorschlag.** Im Test zusätzlich prüfen, dass kein *Modell* der *Einheit* *gesperrt*
ist, etwa `assert not any(aufstellungNachDerZonenwahl.gesperrt(modell) for modell in boyz.modelle)`.
Erledigt, wenn dieselbe Probeänderung den Test zu AUF-14.1 rot macht.

**Stellungnahme.**
