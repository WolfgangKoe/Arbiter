# Importvertrag A4: web/ kennt nur anwendung/

694 · Kritik · von Architekt → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder hat das hexagonale Zielbild angenommen (Anliegen 692, F1 A,
F2 A): eine Schicht `technik/arbiter/anwendung/` zwischen `web/` und der Domäne
([Architektur, A4](../../technik/architektur.md), [Anwendung](../../technik/architektur/anwendung.md)).
`formregeln/importvertrag.py` prüft A1, W1, W2 und B1, nicht A4:
- `web/` importiert von `arbiter` nur `arbiter.anwendung` und sich selbst, nie
  `arbiter.domaene`, `arbiter.katalog` oder `arbiter.speicher`.
- `anwendung/` importiert nur die Standardbibliothek, `arbiter.domaene` und sich selbst.

Heute importiert `web/` die Domäne direkt (`anwendung.py`, `darstellung.py`, `kennungen.py`,
`server.py`); das bleibt bis zum Umbau mit dem ersten Item zum Speicher (F2 A). Beim Umbau
heißt `web/anwendung.py` dann `web/routen.py`; `flaskModule` in `importvertrag.py` und die
Ausnahme `python:S4502` in `sonarlint.py` nennen den alten Namen.

**Kosten.** Ohne A4 wachsen Regeln und das Wiederholen der Handlungen unbemerkt in `web/`
zurück, wie in `ArbiterMap/backend/app/routes/map.py` (40.000 Zeichen); ich müsste jeden
Import von Hand prüfen. Erst beim Umbau gebaut wäre zu spät: Prüfungen ändern sich nur in
der Prozessphase (Retro 5, P1), der Umbau liegt in einer Technikphase, und mit der alten
Fassung von W2 und S4502 wäre die Umbenennung rot.

**Gegenvorschlag.** Bestehende Regeln (Ich 4): A1 und W2 in `formregeln/importvertrag.py`
(`erlaubt`, `webVerstöße`, `flaskModule`), die Ausnahmen in `formregeln/sonarlint.py`, die
Zeile zum Importvertrag in [Regeln](../../prozess/regeln.md#formregeln). Ein Schalter: Besteht
`technik/arbiter/anwendung/`, gilt das Zielbild:
1. A4 wie im Befund, je Verstoß eine Meldung „verboten nach A4“, relative Importe aufgelöst
   wie bei A1.
2. Flask und Werkzeug nur in `web/routen.py` und `web/server.py` (W2), die Ausnahme S4502
   für `web/routen.py` statt `web/anwendung.py`.

Fehlt der Ordner, bleibt alles wie heute. Erledigt, wenn Scheiter-Tests zeigen: ohne
`anwendung/` ist `from arbiter.domaene… import` in `web/` grün; mit `anwendung/` rot, auch
relativ (`from ..domaene`), `from arbiter.anwendung… import` grün; in `anwendung/` sind
`flask`, `yaml`, `arbiter.web`, `arbiter.katalog` und `arbiter.speicher` rot, `fractions`,
`typing` und `arbiter.domaene` grün; Flask in `web/routen.py` grün, in `web/anwendung.py`
rot, sobald `anwendung/` besteht. Geschätzt 30 Zeilen Prüfcode und 10 Tests.

**Stellungnahme.**
