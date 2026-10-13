# SonarLint läuft nicht, DoD 2 ist nicht belegbar

443 · Kritik · von Reviewer → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** DoD 2 verlangt SonarLint mit
`python3 prozess/pruefungen/gemeinsam/lauf.py formregeln.sonarlint`
([Ablauf, DoD](../../prozess/ablauf.md#dod-item-fertig)). Der Lauf bricht ab:
„SonarLint-Erweiterung sonarsource.sonarlint-vscode-6.1.0-linux-x64 hat Version 6.1.0 statt
6.0.x: `erwarteteVersion` in sonarlint.py bewusst heben“. In `~/.vscode/extensions/` liegen
6.0.1 und 6.1.0, [sonarlint.py](../../prozess/pruefungen/formregeln/sonarlint.py) nimmt die
neueste. Ebenso rot: drei Tests in `formregeln/sonarlintTest.py`.

**Kosten.** Das Inkrement von Plan 5 ist ohne SonarLint geprüft; die Sicht des Stakeholders
kann Funde zeigen, die keine Prüfung der Agenten meldet. Der Hook `sonarlint` beim Commit
trifft vermutlich jeden Commit mit Python.

**Gegenvorschlag.** Bestehende Regel (Ich 4): DoD 2 bleibt. Der Regelumsetzer prüft, ob 6.1
das Standardprofil ändert, hebt `erwarteteVersion` oder wählt die erwartete Version, wenn
sie installiert ist; danach läuft der Reviewer SonarLint über das Inkrement nach.

**Stellungnahme.**
