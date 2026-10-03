# AUF-1-Tests: Ort des Codes und Importpfade

27 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · offen

## Runde 1
**Befund.** Die Schnittstelle in
[`aufstellenTest.py`](../../technik/tests/akzeptanz/phasen/aufstellenTest.py) trägt: Handlungen
heißen wie im [Glossar](../../domaene/glossar.md), jede Sperre prüft Grund und unveränderten
Zustand, die zwei Spieler haben gleiche Armeen und fangen so Vergleiche per Gleichheit statt
Identität. Zwei Punkte betreffen den Ort, beide auch nach der Überarbeitung:
1. [`conftest.py`](../../technik/tests/akzeptanz/conftest.py) stellt `technik/backend` vorne
   in den Suchpfad, samt zweimal `noqa: E402`. Den Ordner gibt es nicht und wird es nicht
   geben: Der Implementierer schreibt nur in `technik/arbiter/` (`schreibgrenze.py`), und
   `pyproject.toml` hat den Suchpfad `technik` schon
   ([Anliegen 36](36-suchpfadFuerDasProdukt.md)). Der `# Warum:`-Kommentar darüber
   begründet die Modulnamen, nicht den Eingriff.
2. `arbiter.domaene.armeen` und `arbiter.domaene.aufstellung` folgen nicht dem Grundschnitt
   in [`technik/architektur.md`](../../technik/architektur.md). `Sperre` und `Grund` kämen
   aus der Aufstellung, gelten aber in jeder Phase.

**Kosten.** Zu 1: toter Code, der wie eine Voraussetzung aussieht; jede künftige
`conftest.py` kopiert ihn. Zu 2: Baut der Implementierer nach diesen Importen, verstößt der
Code gegen die Architektur; baut er nach der Architektur, bleiben die Tests rot. Jede weitere
Phase importierte die Sperre aus der Aufstellung. Jetzt kostet es fünf Zeilen.

**Gegenvorschlag.** Die drei Importe aus
[`technik/architektur.md`](../../technik/architektur.md#grundschnitt-der-domäne), in
`conftest.py` und `aufstellenTest.py`. In `conftest.py` entfallen `sys`, `Path`, der
`sys.path`-Eingriff, sein Kommentar und beide `noqa`.

**Stellungnahme.** Offen.
