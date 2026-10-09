# Importvertrag W2: Flask nur in anwendung.py und server.py

343 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Web, W2](../../technik/architektur/web.md#aufbau) sagt nach Anliegen 341:
Flask und Werkzeug importieren nur `anwendung.py` und `server.py`. `formregeln/importvertrag.py`
prüft es nur für eine Datei (`darstellungsDatei = "darstellung.py"`, `webVerstöße`); das neue
`web/kennungen.py` (c1416e2) und jedes weitere Modul von `web/` bleiben ungeprüft, der Test
`testW2FlaskInAnderemWebModulIstGrün` hält genau diese Lücke fest.

**Kosten.** Ein `from flask import abort` in `kennungen.py` bliebe grün; dann hinge die
Zählung der Kennungen an Flask und ließe sich nicht mehr ohne Anwendung prüfen. Jedes neue
Modul von `web/` bräuchte sonst eine eigene Zeile in der Prüfung (Es, O).

**Gegenvorschlag.** Bestehende Regel anpassen, keine neue: in `webVerstöße` statt der einen
verbotenen Datei die zwei erlaubten, etwa `flaskModule = ("anwendung.py", "server.py")` und
`if datei.name not in flaskModule`. Scheiter-Tests: Flask in `kennungen.py` und in einem
unbekannten Modul von `web/` rot, in `anwendung.py` und `server.py` grün; Zeile in
`prozess/regeln.md` angleichen.

Erledigt, wenn ein Flask-Import in einem Modul von `web/` außer `anwendung.py` und
`server.py` rot ist.

**Stellungnahme.** `webVerstöße` in `formregeln/importvertrag.py` meldet Flask und Werkzeug in jedem Modul von `web/` außer `flaskModule = ("anwendung.py", "server.py")`; Scheiter-Tests in `formregeln/importvertragTest.py`, Zeile in `prozess/regeln.md` angeglichen.
