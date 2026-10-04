# Werkzeug fest und Importvertrag für die Akzeptanztests

249 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik am Code von 09a195e (schränkt `pyproject.toml` die Technik richtig ein?)
und ein erreichter Auslöser aus [Web](../../technik/architektur/web.md):
1. `serverStarten` (W2) braucht einen Server mit freiem Port, der sich beenden lässt; das
   gibt Flask nur über `werkzeug.serving.make_server`, wie im Wegwerf-Versuch. `web/`
   importiert Werkzeug also selbst. Flask 3.1 verlangt nur `werkzeug>=3.1.0`, ohne obere
   Grenze: Ein Werkzeug 4 käme mit `Flask==3.1.*` still dazu. Die feste Minor-Version, mit der
   `pyproject.toml` Flask begründet („damit ein Update nicht still das Verhalten ändert“),
   greift für den Teil nicht, den `server.py` aufruft.
2. B1 sagt: Ein Bildschirmtest importiert weder `flask` noch `werkzeug`; Auslöser für den
   Importvertrag auch über `tests/akzeptanz/` ist der erste Bildschirmtest. Er steht seit
   c007cfc (`querschnitt/que2Test.py`, `phasen/aufstellen/auf4Test.py`). Heute hält ihn nur
   die Disziplin des Testautors; ein `from flask import …` in `conftest.py`, etwa für einen
   Testclient, bliebe grün und machte den Test zum Test der Verdrahtung statt der Seite.

**Kosten.** 1: eine Zeile und ein Tabelleneintrag. Ohne sie kann ein Update den Start der
Bildschirmtests brechen, ohne dass sich eine Zeile im Projekt ändert. 2: eine Regel in
`formregeln/importvertrag.py` mit Scheiter-Test. Ohne sie prüft niemand B1. Beides blockiert
den Implementierer nicht.

**Gegenvorschlag.**
1. `"Werkzeug==3.1.*"` in `[project] dependencies` mit `Warum` (direkt importiert von
   `web/server.py`); geprüft als weitere Zeile des Tabellentests aus
   [247](247-abhaengigkeitstestsAlsTabelle.md), sonst wie `testFlaskIst…`.
2. Importvertrag: Module unter `technik/tests/akzeptanz/` importieren weder `flask` noch
   `werkzeug` (auch `from flask import …`, Untermodule wie `werkzeug.serving`).
   Scheiter-Test in `formregeln/importvertragTest.py`: `import werkzeug.serving` in einer
   Probe unter `tests/akzeptanz/` rot, `playwright.sync_api` grün. In B1 setze ich danach
   „Prüft“ auf diesen Test.

Erledigt, wenn beide Scheiter-Tests grün sind und `python3 -m pytest prozess/pruefungen`
grün bleibt.

**Stellungnahme.**
