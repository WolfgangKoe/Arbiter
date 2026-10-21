# Sandbox statt bashSchreiben.py: auf diesem Rechner nicht erprobbar

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 3/3
Status: erledigt

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md): Die Sandbox von Claude Code sollte das Schreiben
per Bash sperren. Sie kennt keine Rollen und sperrt für alle gleich; der Koordinator committet
über Bash, `rm` und `mv` der Rollen (Anliegen 418) und `lauf.py` schreiben ins Projekt. Sie
bleiben als `excludedCommands` draußen, ihre Prüfung bleibt beim Hook.

**Gegenvorschlag.** Block `sandbox` in `.claude/settings.json`: `enabled`,
`failIfUnavailable`, `allowUnsandboxedCommands: false` (Claude Code ignoriert dann
`dangerouslyDisableSandbox`), `filesystem.denyWrite` für `.claude`, die Perspektivordner,
`ArbiterMap`, `Arbiter-old` und die Wurzeldateien; `.git` bleibt beschreibbar.

**Stellungnahme.**

**F1 · Probe durch dich?** Antwort: Er will keinen Ort, an dem Rollen Dinge außerhalb der
Regeln tun. Die Klärung (nur drei `excludedCommands`, ein Scheiter-Test gegen jede Lockerung,
`settings.json` nur vom Regelumsetzer) nahm er an.

**F2 · Erste Probe.** Antwort: Die Sandbox startet. Gesperrt waren `handoff/` und `prozess/`
(auch für `python3`), `.git` blieb beschreibbar, die Tests liefen, die Wurzel blieb
beschreibbar, `/tmp` war gesperrt.

**F3 · Zweite Probe, danach Umsetzung?** Nach Anpassung (`allowWrite: ["/tmp"]`, `.claude` in
`denyWrite`): Lohnt die Sandbox, wenn die Wurzel beim Hook bleibt?
Antwort: Probe wie erwartet. `.claude/probe1.txt` und `handoff/probe6.txt` FEHLER (nur lesbar);
`/tmp/probe2.txt`, `cd /tmp && echo z > /tmp/probe3.txt`, Kopie nach `/tmp/probe4` und
`probe5.txt` in der Wurzel OK. Zur Frage, ob sie lohnt, schwieg er und widersprach der
Empfehlung nicht.

## Runde 2
**Annahme.** Die Sandbox gilt, weil er der Empfehlung nicht widersprach.

**Umsetzung.**
- `.claude/settings.json`: Block `sandbox` wie in der Probe, `excludedCommands` genau
  `lauf.py *`, `rm *`, `mv *`.
- Scheiter-Test `rollenregeln/sandboxGrenzenTest.py` (Prüfung `rollenregeln/sandboxGrenzen.py`):
  rot bei jeder Lockerung (aus, ohne `failIfUnavailable`, Ausweichen erlaubt, vierte oder
  fehlende Ausnahme, `allowWrite` über `/tmp`, fehlender Eintrag in `denyWrite`).
- `bashSchreiben.py` bleibt unverändert: Der Hook erkennt nicht, welcher Pfad in einem
  gesperrten Ordner liegt, ohne Pfade zu deuten; Kürzen wäre mehr Code ohne Ersparnis. Er
  prüft weiter die Wurzel und die drei `excludedCommands`.
- Offen: Neue Dateien in der Wurzel sperrt nur der Hook, ein Skript in einer Datei
  schreibt dort weiter (Anliegen 510).

## Runde 3
**Abschluss.** Der Stakeholder hat P3 gestrichen: Er sieht den Mehrwert nicht mehr, die Rollen
müssen arbeiten und committen können. Die Umsetzung ist zurückgebaut (`sandboxGrenzen.py`,
Scheiter-Test, Regelzeile). Die Lücke bleibt in [Regeln](../../prozess/regeln.md#rollenregeln)
bei `rollenregeln/schreibgrenze.py` stehen: Ein Python-Skript, das selbst Dateien schreibt,
umgeht die Prüfung. Den Sandbox-Block, `PRE_COMMIT_HOME` und die Zeilen in `.gitignore` setzt
er selbst auf den Stand des letzten Commits zurück.
