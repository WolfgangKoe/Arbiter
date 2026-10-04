# `.gitignore` bekommt einen Besitzer: den Regelumsetzer

178 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · erledigt

## Runde 1
**Befund.** [Anliegen 177](177-coverageDateiNichtIgnoriert.md): Im Wurzelordner liegt die
Messdatei `.coverage` (Lauf von `coverage run` von Hand), `.gitignore` nennt sie nicht, und
keine Rolle hat `.gitignore` in ihren Schreibpfaden. Die Mechanismen selbst schreiben über
`COVERAGE_FILE` in ein temporäres Verzeichnis.

**Kosten.** Mit `git add -A` landet die Binärdatei im Commit; der Stand zählt sie als
uncommittete Datei. Jede Wegwerf-Messung erzeugt sie neu. Ohne Besitzer bleibt jede solche
Lücke liegen, bis der Stakeholder selbst eingreift.

**Gegenvorschlag.** Der Regelumsetzer bekommt `.gitignore` in seine Schreibpfade
([Agentendefinition](../../.claude/agents/regelumsetzer.md)); es ist Werkzeugkonfiguration
wie `pyproject.toml` und `.pre-commit-config.yaml`, die er schon schreibt. Er trägt
`.coverage` und `.coverage.*` ein und löscht die liegende Datei. Den Altbestand
(`/Arbiter-old/`, `/ArbiterMap/`) entfernt er nur auf Anweisung des Stakeholders.

**F1 · Darf der Regelumsetzer `.gitignore` schreiben (Schreibpfad in seiner Definition)?**
Empfehlung: ja. Alternative: Der Stakeholder pflegt `.gitignore` selbst und trägt
`.coverage` und `.coverage.*` ein.
Antwort: .
