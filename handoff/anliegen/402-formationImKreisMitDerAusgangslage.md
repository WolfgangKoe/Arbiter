# Formation im Kreis zwischen Ausgangslage und Aufstellen

402 · Kritik · von Architekt (Technik) → Implementierer (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Zu b43abff, Folge von Punkt 4 meines Gegenvorschlags in Anliegen 399: `Formation`
liegt jetzt in [ziehen.py](../../technik/arbiter/domaene/phasen/aufstellen/ziehen.py), die
`Ausgangslage` hält `formationen` und importiert `Formation` nur unter `TYPE_CHECKING`
([ausgangslage.py](../../technik/arbiter/domaene/missionsvorbereitung/ausgangslage.py)). Wer
ein Modul des Pakets `phasen/aufstellen` importiert, lädt dessen `__init__.py`, und das
importiert `ausgangslage.py`. Die Missionsvorbereitung kennt so die Phase danach; der Kreis
ist nur versteckt, `formregeln/importvertrag.py` sieht ihn nicht.

**Kosten.** [Es](../../prozess/praemissen/es.md), D: „ohne Kreis“. Jeder weitere Typ aus
einer Phase in der `Ausgangslage` braucht denselben Kniff, ein Import zur Laufzeit bricht
beim Laden. Ändern kostet einen Lauf ohne neues Verhalten: `ziehen.py`, `ausgangslage.py`,
`katalog/ausgangslage.py`, `ziehenTest.py`.

**Gegenvorschlag.** Bestehende Regel: Es, D, und der Weg aus 399, Zustand rein, Befund raus.
Die Daten der *Formation* gehören zur `Ausgangslage` wie die `tiefen`, die Regel AUF-8.5
bleibt in `ziehen.py`:
- `Formation` mit `reihen` und `abstand`, ohne Methoden, zieht nach
  `missionsvorbereitung/ausgangslage.py`; `TYPE_CHECKING` und sein `# Warum:` entfallen.
- `Formation.stellen` wird in `ziehen.py` die Funktion `stellenDerFormation(formation, base,
  mitte, grenzenInX, grenzenInY)`; `stellenDerUngesetzten` und `ziehenTest.py` rufen sie.
So liest `ziehen.py` aus der `Ausgangslage`, wie `sperrenBeimSetzen.py` deren Zonengrenzen.
Erledigt, wenn `TYPE_CHECKING` unter `technik/arbiter/domaene` fehlt und
`python3 -m pytest technik/tests prozess/pruefungen` grün ist, bis auf die Rückverfolgung zu
AUF-16.5.

**Stellungnahme.**
