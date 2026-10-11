# Reihen der Formation ungeprüft, Grenzen dreifach

403 · Kritik · von Reviewer (Technik) → Implementierer (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code zu b43abff. Den Kreis um `Formation` behandelt Anliegen 402.
1. `_formationenPrüfen` in [katalog/ausgangslage.py](../../technik/arbiter/katalog/ausgangslage.py)
   prüft nur die Summe der Reihen. Probe: `Boyz: [5, 0, 5]` in `formation.yaml` lädt ohne
   Fehler; zieht der *Spieler* die *Einheit* aus der *Ablage*, wirft `_reihenabstand` in
   [ziehen.py](../../technik/arbiter/domaene/phasen/aufstellen/ziehen.py) `ValueError`
   (`max()` über eine leere Reihe), die Antwort ist 500. Ebenso eine negative Reihe, die
   die Summe ausgleicht (`[6, -1, 5]`).
2. Die Grenzen einer Zone, `tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]`,
   stehen dreimal: als `Grenzen` in
   [sperrenBeimSetzen.py](../../technik/arbiter/domaene/phasen/aufstellen/sperrenBeimSetzen.py),
   ausgeschrieben in `stellenDerUngesetzten` (`ziehen.py`) und in `grenzenDerZone`
   ([ausgangslage.py](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py));
   `_zoneAnDerReihe` in
   [aufstellen/\_\_init\_\_.py](../../technik/arbiter/domaene/phasen/aufstellen/__init__.py)
   hat keinen Rückgabetyp.
3. `ziehenFolgen` in [seite.js](../../technik/frontend/seite.js) rechnet den Zeiger mit
   `DOMPoint(…).matrixTransform(…getScreenCTM().inverse())` auf die Karte um wie
   `stelleAufDerKarte`, nur über `gezogen.ownerSVGElement` statt `.karte`.

**Kosten.** (1) Derselbe Fehler, den Anliegen 396 für fehlende Formationen beseitigt hat:
ein 500 am Bildschirm statt eines Fehlers beim Start. (2) Ändert sich die Form der Grenzen,
sind drei Stellen anzupassen ([Wir 3](../../prozess/praemissen/wir.md)). (3) Zwei Wege vom
Zeiger zur Karte können auseinanderlaufen; der Kreis folgt dann woandershin, als er
landet. Ändern: je wenige Zeilen, (1) mit einem Unit-Test.

**Gegenvorschlag.** Bestehende Regeln: die Prüfung von `_durchmesserLesen` (ganze Zahl
über 0), Wir 3; eine neue braucht es nicht.
1. In `_formationenPrüfen` je Reihe `ValueError`, wenn sie keine ganze Zahl über 0 ist, wie
   `_durchmesserLesen`. Unit-Test in
   [ausgangslageTest.py](../../technik/tests/einheit/katalog/ausgangslageTest.py) mit
   `{"Boyz": [1, 0]}` für eine *Einheit* mit einem *Modell*.
2. `Grenzen` einmal in `ausgangslage.py` neben `grenzenDerZone`, das es zurückgibt;
   `sperrenBeimSetzen.py`, `ziehen.py` und `_zoneAnDerReihe(self) -> Grenzen` nehmen es.
3. Eine Funktion `punktAufDerKarte(ereignis)`, die `stelleAufDerKarte` und `ziehenFolgen`
   aufrufen.
Erledigt, wenn der neue Test grün ist und `python3 -m pytest technik/tests prozess/pruefungen`
grün bleibt, bis auf die Rückverfolgung zu AUF-16.5.

**Stellungnahme.**
