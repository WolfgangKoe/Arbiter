# Befehl aus der Wurzel und Abdeckung des eigenen Prozesses

243 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** QUE-2.1: „Ein Befehl startet Arbiter und nennt die Adresse.“ Nach
[Web](../../technik/architektur/web.md) W5 und B4 ist das `python3 -m arbiter`; der
Akzeptanztest startet ihn als eigenen Prozess. Zwei Lücken in `pyproject.toml` und
`formregeln/abdeckung.py`, beide im Wegwerf-Versuch (Flask, Playwright, coverage 7.16)
nachgestellt:
1. `arbiter` liegt nur für pytest im Suchpfad (`pythonpath = ["technik"]`). Aus der Wurzel
   findet `.venv/bin/python -m arbiter` das Paket nicht; der Stakeholder bräuchte
   `cd technik` oder `PYTHONPATH`, also mehr als einen Befehl.
2. `abdeckungMessen` misst nur den Prozess von pytest. Was der Befehl im eigenen Prozess
   ausführt (Ausgangslage laden, Adresse ausgeben, Server laufen lassen), zählt als nicht
   gedeckt, obwohl der Akzeptanztest es durchläuft; ebenso jeder spätere Test eines
   Befehls. Im Versuch: 0 % für `__main__.py` ohne Messung im Kindprozess, 100 % mit
   `[run] patch = subprocess` und `sigterm = true` (der Test beendet den Server mit
   SIGTERM, sonst schreibt coverage nichts) und `coverage combine` vor `coverage json`.

**Kosten.** Ohne 1 startet der Stakeholder Arbiter am Ende des Zyklus nicht mit einem
Befehl (Plan 3, Empfehlung). Ohne 2 fällt `technik/arbiter` mit dem ersten Befehl unter
95 % (DoD 1), oder der Implementierer weicht auf Ausnahmen aus, die echten Code verstecken.
Beides blockiert den Implementierer bei QUE-2.1, nicht den Testautor.

**Gegenvorschlag.** Vor dem Lauf des Implementierers zu QUE-2.1:
1. `[project.scripts] arbiter = "arbiter.__main__:starten"` (W5) mit dem Paket aus
   `technik/` (`[build-system]` und Paketsuche), einmal `pip install -e .` in `.venv`;
   Scheiter-Test in `formregeln/konfigurationTest.py`: Eintrag fehlt oder zeigt woanders hin.
2. `[tool.coverage.run] patch = ["subprocess"]`, `sigterm = true`; in `abdeckungMessen`
   `coverage combine` vor `coverage json`. Scheiter-Test in `formregeln/abdeckungTest.py`:
   eine Probe, deren einzige Zeile nur ein Kindprozess ausführt, ist gedeckt.

Erledigt, wenn `.venv/bin/arbiter` aus der Wurzel startet, sobald `__main__.py` steht, und
beide Scheiter-Tests grün sind.

**Stellungnahme.** Umgesetzt in `pyproject.toml`
(`[project.scripts]`, `[build-system]` mit setuptools 84.0.\*, Paketsuche `technik/`,
`[tool.coverage.run]` `patch`, `sigterm`) und `formregeln/abdeckung.py` (`coverage combine`).
`pip install -e .` ist in `.venv` gelaufen; `.venv/bin/arbiter` zeigt auf `arbiter.__main__:starten`
und startet, sobald das Modul steht. Scheiter-Tests: `formregeln/konfigurationTest.py` (Eintrag,
Paketsuche, Messung, Befehl installiert), `formregeln/abdeckungTest.py` (Probe, die nur ein
Kindprozess ausführt: gedeckt; ohne die Messung nicht). Offen, nicht aus 243:
`testDasProduktErreichtDieSchwelleMitSeinenTests` ist rot (Zeilen 94,2 %, Zweige 80 %), solange
die Tests zu Plan 3 rot sind.
