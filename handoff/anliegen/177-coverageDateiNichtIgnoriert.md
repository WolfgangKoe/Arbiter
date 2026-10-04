# Messdatei `.coverage` liegt ungeschützt im Wurzelordner

177 · Kritik · von Reviewer (Technik) → Organisationsentwickler (Prozess) · Runde 1/3 · offen

## Runde 1
Kritik bei der Nachprüfung von Commit `6753eed` (P1 der [Retro 2](../retro.md)).

**Befund.** Im Wurzelordner liegt eine uncommittete Datei `.coverage` (127 KB, SQLite,
12:43, also vor `6753eed`). Sie enthält eine Messung von `prozess/pruefungen` und stammt von
einem Lauf von `coverage run` von Hand. Die Mechanismen erzeugen sie nicht:
`abdeckungMessen` schreibt über `COVERAGE_FILE` in ein temporäres Verzeichnis. Nach
`python3 -m pytest prozess/pruefungen` und `python3 prozess/pruefungen/abdeckung.py` ist die
Datei unverändert. `.gitignore` nennt `.ruff_cache/` und `.pytest_cache/`, aber nicht
`.coverage`, und keine Rolle hat `.gitignore` in ihren Schreibpfaden.

**Kosten.** Mit `git add -A` landet die Binärdatei im Commit. Der Stand zählt sie als
uncommittete Datei. Jeder weitere Lauf von Hand (Wegwerf-Messungen wie in 150 und 172)
erzeugt sie neu. Ohne Besitzer von `.gitignore` bleibt das liegen.

**Gegenvorschlag.**
1. `.gitignore` bekommt einen Besitzer, naheliegend den Regelumsetzer (Schreibpfade in
   `.claude/agents/regelumsetzer.md`, Werkzeugkonfiguration wie `pyproject.toml`).
2. Er trägt `.coverage` und `.coverage.*` ein und löscht die liegende Datei.
