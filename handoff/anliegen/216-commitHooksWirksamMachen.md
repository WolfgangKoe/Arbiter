# Commit-Hooks wirksam machen, damit SonarLint sperrt

216 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder verlangt SonarLint scharf
([150](150-sonarlintAbdeckungUndToterCode.md)). `sonarlint.py` sperrt nur als Hook in
`.pre-commit-config.yaml`. `pre-commit` steht nicht in `pyproject.toml` und ist nicht
installiert (`python3 -m pre_commit`: kein Modul), `.git/hooks/` enthält nur `*.sample`.
Darum läuft heute keiner der fünf Hooks der Datei: `erledigteLoeschen`, `pruefungen`,
`benennung`, `abdeckungPruefskripte`, `sonarlint`. `prozess/regeln.md` nennt sie als
Mechanismus; nur die Zeile zu ruff sagt „läuft nur nach `pre-commit install`“.

**Kosten.** SonarLint und die Abdeckung der Prüfskripte (DoD 1 und 2) laufen nur, wenn
jemand sie aufruft. Ein Fund, den der Stakeholder in VS Code sieht, kann in einen Commit
gelangen. `regeln.md` nennt Mechanismen, die nicht greifen.

**Gegenvorschlag.**
1. `pre-commit` mit fester Minor-Version in `dependency-groups.entwicklung`, installiert in
   `.venv`, dann einmal `pre-commit install`. Sperrt dich die Bash-Positivliste oder die
   Sandbox ([215](215-bashSandboxAlsVersuch.md)), führt der Stakeholder den Befehl aus; er
   steht in der Meldung aus 2.
2. Scheiter-Test im Lauf von `python3 -m pytest prozess/pruefungen`: rot, wenn
   `.git/hooks/pre-commit` fehlt oder nicht `pre-commit` aufruft.
3. Probe: Ein Commit mit einem SonarLint-Fund in einer `.py`-Datei wird abgewiesen. Ein
   Commit mit roten Akzeptanztests (Technikphase, Schritt 1) geht durch, sonst nennst du
   den Hook, der ihn sperrt. Nenne die Dauer eines Commits mit allen Hooks.
4. `regeln.md`: „läuft nur nach `pre-commit install`“ ersetzt die Prüfung aus 2.

Geht 1 nicht, dann ein PreToolUse-Hook in `.claude/settings.json` auf `git commit`, der
dieselben Prüfungen ruft; er läuft außerhalb der Sandbox, sperrt aber nur Commits über
Claude Code.

Erledigt, wenn der Test aus 2 ohne Installation rot und mit ihr grün ist, die Probe aus 3
so ausgeht, `python3 -m pytest prozess/pruefungen` grün ist und der Reviewer den Code
geprüft hat ([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)). DoD 2 im Ablauf
setze ich danach von „nur Text“ zurück.
