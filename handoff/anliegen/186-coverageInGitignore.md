# `.coverage` in `.gitignore` eintragen und die liegende Datei löschen

186 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer (Prozess) · Runde 1/3 · offen

## Runde 1
Weitergereicht aus [Anliegen 177](177-coverageDateiNichtIgnoriert.md); der Stakeholder hat
dir `.gitignore` mit Anliegen 178 zugewiesen, der Schreibpfad
steht in deiner [Definition](../../.claude/agents/regelumsetzer.md).

**Befund.** Im Wurzelordner liegt die Messdatei `.coverage` (SQLite, von einem Lauf von
`coverage run` von Hand). `.gitignore` nennt sie nicht; die Mechanismen selbst schreiben
über `COVERAGE_FILE` in ein temporäres Verzeichnis.

**Kosten.** Mit `git add -A` landet die Binärdatei im Commit; der Stand zählt sie als
uncommittete Datei. Jede Wegwerf-Messung erzeugt sie neu.

**Gegenvorschlag.** Trage `.coverage` und `.coverage.*` in `.gitignore` ein und lösche die
liegende `.coverage`. Den Altbestand (`/Arbiter-old/`, `/ArbiterMap/`) entfernst du nur auf
Anweisung des Stakeholders. Erledigt-Bedingung: `git status --short` nennt keine
`.coverage`, `git check-ignore .coverage .coverage.x` nennt beide.
