# Bash-Sandbox als Versuch, danach ohne Pfad-Heuristik

215 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in Anliegen 139 F2 mit A
entschieden: Bash-Sandbox von Claude Code, zuerst als Versuch. Anlass: Ein Skript im
Heredoc, `python3 -c` oder `cd <pfad> && …` kommt an der Heuristik von
`bashPositivliste.py` für Anliegen und nur lesbare Pfade vorbei
([138](138-anliegenPerSkriptAmBashSchutzVorbei.md)).

**Kosten.** Bis dahin kann eine Rolle per Bash Status, Runde oder Nummer setzen, ohne dass
Statusrecht und Nummernprüfung greifen; dort ist die Regel nur Text
([Ablauf, Anliegen](../../prozess/ablauf.md#anliegen)).

**Gegenvorschlag.** Nach [Sandboxing](https://code.claude.com/docs/en/sandboxing):
1. `.claude/settings.json`, Block `sandbox`: `enabled: true`; `failIfUnavailable: true`
   (sonst läuft Bash still ohne Sandbox, wenn `bwrap` nicht startet);
   `allowUnsandboxedCommands: false`; `filesystem.denyWrite` mit `handoff/anliegen/` und den
   Pfaden aus `agenten.nurLesbar`, relativ zur Projektwurzel; kein `excludedCommands`.
2. Scheiter-Test: rot, wenn eine dieser Einstellungen fehlt, ein Pfad aus
   `agenten.nurLesbar` oder `handoff/anliegen/` in `denyWrite` fehlt oder
   `excludedCommands` gesetzt ist.
3. Probelauf in einer Sitzung, die nach der Einstellung beginnt: je ein Schreibversuch auf
   ein Anliegen und auf `VORGEHEN.md` per Heredoc-Skript, `python3 -c`,
   `cd handoff/anliegen && rm …` und Umleitung; jeder scheitert. Grün bleiben
   `python3 -m pytest prozess/pruefungen` (das Löschen von `erledigteLoeschen.py` im
   Testlauf darf nicht rot werden), `sonarlint.py` (schreibt es unter `~`, dann
   `allowWrite` genau dafür) und ein Commit samt Hooks aus
   [216](216-commitHooksWirksamMachen.md).
4. Erst nach dem Probelauf entfällt der Pfadteil der Heuristik (`ändertPfad`, `istAnliegen`,
   `istNurLesbar` samt Tests), ebenso die Zeile „Bekannte Lücke“ in `prozess/regeln.md`. Die
   Rollen- und git-Regeln von `bashPositivliste.py` bleiben.

Bekannt aus der Doku: Hooks und die Werkzeuge Write und Edit laufen außerhalb der Sandbox,
`erledigteLoeschen.py` löscht danach nur noch im Hook SubagentStop. `.claude/`, `.vscode/`
und `.git/hooks` sperrt die Sandbox für Bash ohnehin; `pre-commit install` aus 216 geht
dann nur außerhalb, also vorher oder durch den Stakeholder.

Erledigt, wenn der Test aus 2 an je einem Gegenbeispiel rot wird, der Probelauf aus 3 so
ausgeht (Ergebnis in deiner Stellungnahme), `python3 -m pytest prozess/pruefungen` grün ist
und der Reviewer den Code geprüft hat
([Kritik am Code](../../prozess/ablauf.md#kritik-am-code)). Den Ablauf passe ich danach an.
