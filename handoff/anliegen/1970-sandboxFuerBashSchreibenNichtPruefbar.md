# Sandbox statt bashSchreiben.py: auf diesem Rechner nicht erprobbar

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md): Die Sandbox von Claude Code sollte das Schreiben
per Bash sperren, `bashSchreiben.py` verlöre dann, was sie sperrt. Ich habe den Entwurf an
einer Kopie unter `/tmp/arbiterKopie` angelegt, ihn aber nicht zum Laufen gebracht:
1. Mit `sandbox.enabled` scheitert jeder Bash-Aufruf mit `apply-seccomp: write
   /proc/self/setgroups (nested userns is capability-restricted)`. Auf dem Rechner geht
   `bwrap` allein, aber keine zweite User-Namespace darin (`unshare -Ur` unter `bwrap`:
   „Vorgang nicht zulässig“). Ob die Sandbox in deiner Sitzung startet, weiß ich nicht.
2. Mit `network.allowAllUnixSockets: true` (ohne Seccomp-Filter) sperrte der Klassifizierer
   den Probelauf, weil er einen zweiten `claude` mit `bypassPermissions` startet. Das habe
   ich nicht umgangen.
3. Die Sandbox kennt keine Rollen: Sie sperrt für alle gleich. Der Koordinator committet über
   Bash, `rm` und `mv` der Rollen (Anliegen 418) und die Skripte `lauf.py` schreiben ins
   Projekt. Der Entwurf nimmt sie über `excludedCommands` aus; dann bleibt die Prüfung für
   sie beim Hook.

**Kosten.** Ohne Probe wäre `bashSchreiben.py` zu kürzen ein Schritt ins Blaue: Läuft die
Sandbox nicht, fiele die Sperre still weg; mit `failIfUnavailable` startet Claude Code gar
nicht. Deshalb bleiben Hook und `settings.json` unverändert.

**Gegenvorschlag.** Entwurf in `/tmp/arbiterKopie/.claude/settings.json` (Block `sandbox`):
`enabled`, `failIfUnavailable`, `allowUnsandboxedCommands: false`, `filesystem.denyWrite` für
`domaene`, `handoff`, `prozess`, `technik`, `ArbiterMap`, `Arbiter-old`, die Wurzeldateien
(`CLAUDE.md`, `VORGEHEN.md`, `pyproject.toml`, `package*.json`, Linter-Dateien,
`.gitignore`, `.vscode`) und `excludedCommands` für `python3 prozess/pruefungen/gemeinsam/lauf.py *`,
`rm *`, `mv *`. `.git` bleibt schreibbar, damit der Koordinator committet. Probe in der
Kopie (7 Aufrufe in `/tmp/probe.txt`): nach `/sandbox` dort sollten 1, 2 und 6 an
`handoff`, `prozess` und der Wurzel scheitern oder gelingen wie gewollt, 3 und 7 gelingen.
Bestehen sie, kürze ich `bashSchreiben.py` um Umleitung, `sed -i`, `cp`, `touch`, `tee`
(`rm`, `mv`, `git` bleiben) und kürze die Tests entsprechend; dazu ein Scheiter-Test, dass
`denyWrite` jeden Ordner der Wurzel nennt außer den Zwischenspeichern.

**Stellungnahme.**

**F1 · Probe durch dich?** Startet die Sandbox bei dir, und darf ich danach die Änderung
an `settings.json` und `bashSchreiben.py` umsetzen? Empfehlung: ja, erst nach bestandener
Probe; startet sie nicht, bleibt Anliegen 510 wie es ist.
Antwort: .
Kommentar: Ich weiß nicht, wie ich es probieren soll. Ich möchte aber nicht, dass die Sandbox ein Ort wird, wo du und andere diverse Dinge außerhalb der Regeln tun! Wie ließe sich das vermeiden?
