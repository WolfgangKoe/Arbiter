# AUF-1-Tests: Ort des Codes und Importpfade

27 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Die [Schnittstelle](../../technik/tests/akzeptanz/conftest.py) trägt: Handlungen
heißen wie im [Glossar](../../domaene/glossar.md), jede Sperre prüft Grund und unveränderten
Zustand, a und b haben gleiche Armeen und fangen so Vergleiche per Gleichheit statt Identität.
Drei Punkte betreffen den Ort:
1. Der Code soll unter `technik/backend/arbiter/` liegen. Der Implementierer darf nur in
   `technik/arbiter/` schreiben (Schreibpfade, `schreibgrenze.py`), so auch die Zielstruktur
   in `VORGEHEN.md`. Der `sys.path`-Eingriff samt `noqa` gilt nur hier; Einheits- und
   Architekturtests bräuchten ihn erneut.
2. `armeen` und `aufstellung` folgen nicht dem Grundschnitt in `VORGEHEN.md` (`spielobjekte/`,
   `phasen/<phase>/`), an dem der Spiegel Tests und Code abgleicht. `Sperre` und `Grund` liegen
   in `aufstellung`, gelten aber in jeder Phase (Übergehen und Protokoll, `domaene/ziel.md`).
3. Die Docstrings nennen Prozess („vom Architekten zu prüfen“, „Plan 1“, „Plan: keine Sperren
   beim Beenden“); E36 erlaubt nur einzeilige Docstrings ohne Prozessverweis.

**Kosten.** Zu 1: Die Tests bleiben rot, der Implementierer kann sie nicht grün machen. Zu 2:
Jede weitere Phase importierte die Sperre aus der Aufstellung; ein späterer Umzug ändert jede
Testdatei. Ein Importvertrag wie „`arbiter.domaene` importiert weder `flask` noch
`arbiter.web`“ (import-linter) braucht feste Pakete. Jetzt kostet es vier Zeilen.

**Gegenvorschlag.**
```python
from arbiter.domaene.spielobjekte import Armee, Einheit, Modell, Spieler
from arbiter.domaene.phasen.aufstellung import Aufstellung, Aufstellungszone
from arbiter.domaene.sperre import Grund, Sperre
```
Code unter `technik/arbiter/`, Suchpfad `pythonpath = ["technik"]` in `pyproject.toml`
(schreibt der Implementierer); `sys.path` und `noqa` entfallen. Ein Modul wird später ohne
Importänderung zum Paket. Docstrings: „Testdaten der Akzeptanztests: kleine Armeen ohne
Ausgangslage.“ und „Wählt die Einheit, setzt alle ihre Modelle und beendet.“

**Stellungnahme.** Offen.
