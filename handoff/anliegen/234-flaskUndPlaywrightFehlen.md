# Flask und Playwright fehlen in pyproject.toml

234 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** [Plan 3](../plan.md) verlangt einen Start im Browser (QUE-2.1) und
Bildschirmtests. Dafür braucht die Technik Flask (CLAUDE.md, Technik-Rahmen) und Playwright
mit Chromium (Anliegen 146 Punkt 4, git). `pyproject.toml` nennt als Abhängigkeit nur
PyYAML, in `.venv` fehlen beide (`import flask`, `import playwright`: ModuleNotFoundError).
Chromium liegt schon unter `~/.cache/ms-playwright/` (Build 1223). `pyproject.toml` schreibt
nur der Regelumsetzer (implementierer.md); in deiner Reihenfolge der Moderation steht das
nicht.

**Kosten.** Ohne die Abhängigkeiten scheitern der Wegwerf-Versuch zum Bildschirmtest und jeder
rote Test am Import statt am fehlenden Verhalten; der Testautor kann nicht zeigen, dass sein
Test das Kriterium trifft. Es blockiert das Inkrement von Zyklus 3, nicht die Freigabe.

**Gegenvorschlag.** Nach der Freigabe von Plan 3, vor meinem Wegwerf-Versuch:
- `dependencies`: Flask mit fester Minor-Version, Begründung wie bei PyYAML.
- `entwicklung`: Playwright für Python mit fester Minor-Version; passt sie nicht zum
  Chromium-Build im Cache, lädt `playwright install chromium` den passenden.
- `konfigurationTest.py` prüft beide wie PyYAML
  (`testPyYamlIstLaufzeitAbhängigkeitMitFesterMinorVersion`).

Erledigt, wenn `.venv/bin/python -c "import flask, playwright"` ohne Fehler läuft und die
Prüfungen grün sind. eslint und stylelint (ablauf.md, Werkzeuge) kommen mit dem ersten
JavaScript, nicht hier.

**Stellungnahme.**
