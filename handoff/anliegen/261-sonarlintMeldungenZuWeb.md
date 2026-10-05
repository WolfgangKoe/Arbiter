# SonarLint-Meldungen zu web/

261 · Kritik · von Implementierer (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** `formregeln.sonarlint` endet mit Exit 0, meldet aber drei Hinweise zu `web/`:
`python:S4502` (CSRF) in `technik/arbiter/web/anwendung.py:14`, zweimal `python:S5332` (http)
in `technik/arbiter/web/server.py:18`. Beide sind hier unbegründet: nur GET-Routen, Adresse
nur für `127.0.0.1` ([Web](../../technik/architektur/web.md), W5).

**Kosten.** Jeder Lauf zeigt die drei Zeilen; ein Reviewer muss sie jedes Mal einordnen.

**Gegenvorschlag.** Entscheide, ob SonarLint diese beiden Regeln für `web/` ausnimmt oder die
Hinweise gelten. Erledigt, wenn der Lauf sie nicht mehr meldet oder dokumentiert ist, warum sie bleiben.

**Stellungnahme.** Angenommen: SonarLint nimmt die drei Funde aus, je Datei und Regel, nicht den Ordner `web/`
(`ausnahmen` in `prozess/pruefungen/formregeln/sonarlint.py`, Begründung dort und in [Regeln](../../prozess/regeln.md)).
Scheiter-Test: `formregeln/sonarlintTest.py` (dieselbe Regel in einer anderen Datei bleibt ein Fund).
