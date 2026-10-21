# Sandbox statt bashSchreiben.py: auf diesem Rechner nicht erprobbar

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Zu P3 aus [Retro 6](../retro.md): Die Sandbox von Claude Code sollte das Schreiben
per Bash sperren, `bashSchreiben.py` verlöre dann, was sie sperrt. Ich habe den Entwurf an
einer Kopie unter `/tmp/arbiterKopie` angelegt, ihn aber nicht zum Laufen gebracht:
1. Mit `sandbox.enabled` scheitert jeder Bash-Aufruf mit `apply-seccomp: write
   /proc/self/setgroups (nested userns is capability-restricted)`. Ob die Sandbox in deiner
   Sitzung startet, weiß ich nicht.
2. Mit `network.allowAllUnixSockets: true` sperrte der Klassifizierer den Probelauf, weil er
   einen zweiten `claude` mit `bypassPermissions` startet. Das habe ich nicht umgangen.
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
Kopie: 7 Aufrufe in `/tmp/probe.txt`, 1, 2 und 6 sollen scheitern, 3 und 7 gelingen. Bestehen
sie, kürze ich `bashSchreiben.py` um Umleitung, `sed -i`, `cp`, `touch`, `tee`.

**Stellungnahme.**

**F1 · Probe durch dich?** Startet die Sandbox bei dir, und darf ich danach die Änderung
an `settings.json` und `bashSchreiben.py` umsetzen? Empfehlung: ja, erst nach bestandener
Probe; startet sie nicht, bleibt Anliegen 510 wie es ist.
Antwort: .
Kommentar: Ich weiß nicht, wie ich es probieren soll. Ich möchte aber nicht, dass die Sandbox ein Ort wird, wo du und andere diverse Dinge außerhalb der Regeln tun! Wie ließe sich das vermeiden?

**Klärung.** *Probe für dich, drei Schritte:* (1) Terminal in `/tmp/arbiterKopie`, dort
`claude` starten. (2) `/sandbox` tippen: Steht dort „enabled“, läuft sie; kommt eine
Fehlermeldung oder startet Claude gar nicht, startet sie bei dir nicht, und alles bleibt wie
es ist. (3) „Führe /tmp/probe.txt aus“ schreiben und mir die sieben Zeilen OK oder FEHLER
geben.*Gegen Missbrauch:* In der Kopie fehlte `.claude` in `denyWrite`; ergänze ich. Dann gilt:
- `allowUnsandboxedCommands: false`: Claude Code ignoriert das Ausweichen mit
  `dangerouslyDisableSandbox` (Doku). `failIfUnavailable`: Startet sie nicht,
  startet Claude nicht, statt still ohne Sperre zu laufen.
- `excludedCommands` sind genau drei, nur der Wortlaut zählt: Verkettetes, `cd`, Umleitung
  und `$(…)` bleiben in der Sandbox. `rm` und `mv` prüft weiter `entfernen.py`.
- Ein Scheiter-Test wird rot, wenn `settings.json` mehr als diese drei nennt, die Sperre
  lockert oder ein Wurzelordner in `denyWrite` fehlt. `settings.json` schreibt nur der
  Regelumsetzer, jede Änderung zeigt `git diff`.
- `bashSchreiben.py` bleibt bis Retro 7 als zweite Schicht. Gilt Sandbox, entfällt die
  Heuristik aus [2040](2040-pythonUeberBashNachFreigabeRetro6.md); gilt „Hook bleibt“, baue ich sie.

**F2 · Probe und Grenzen.** Probierst du die drei Schritte, und gelten die Grenzen oben?
Empfehlung: ja; das Ergebnis (läuft oder läuft nicht) schreibst du in die Antwort.
Antwort: (Stakeholder, übermittelt über den Koordinator) Probe in `/tmp/arbiterKopie` mit /sandbox
(„Sandbox commands, with auto-allow“):
1. `echo x > handoff/probe1.txt`: FEHLER, Dateisystem nur lesbar.
2. `python3 -c "open('prozess/probe2.txt','w')…"`: FEHLER, `[Errno 30] Read-only file system`.
3. `echo x > /tmp/probe3.txt`: FEHLER, Dateisystem nur lesbar.
4. `git add domaene && git status --short | head -2`: OK.
5. `pytest …/entfernenTest.py`: OK, 31 passed.
6. `echo y > probe6.txt`: OK.
7. `cd /tmp && echo z > /tmp/probe7.txt`: FEHLER, Dateisystem nur lesbar.
Spuren: `probe6.txt` in der Wurzel der Kopie; Aufruf 4 hat `domaene` gestaged.

**Auswertung.** Die Sandbox startet und sperrt, was `denyWrite` nennt (1, 2); `.git` bleibt
beschreibbar (4), die Tests laufen (5). Zwei Abweichungen vom Entwurf:
- **Wurzel (6).** Unbenannte Wurzeldateien bleiben schreibbar. Das lässt sich nicht
  schließen: Die Werkzeuge legen Caches in der Wurzel an (`.pytest_cache`, `.ruff_cache`,
  `.coverage`, `.complexipy_cache`, `dashboard.html`). Neue Dateien in der Wurzel sperrt
  weiter nur der Hook.
- **/tmp (3, 7).** Die Sandbox lässt außer dem Projekt nur ihren eigenen Temp-Ordner zu. Die
  Rollen brauchen `/tmp` für Kopien und Mutationstests. Das Fehlen von `.claude` in
  `denyWrite` ist der dritte Punkt: Dort läge `settings.json`.

**Anpassung der Kopie.** `filesystem.allowWrite: ["/tmp"]` und `.claude` in `denyWrite`
(Entwurf in `/tmp/arbiterKopie/.claude/settings.json`). `allowWrite` öffnet nur `/tmp`, nichts
im Projekt. Der Hook `schreibgrenze.py` bleibt für die Wurzel und für alles, was die Sandbox
nicht sieht (Write und Edit laufen ohnehin nicht in ihr). Kürzen darf `bashSchreiben.py` daher
nur, was in den gesperrten Ordnern liegt; die Wurzel bliebe Sache des Hooks, die Ersparnis ist
klein.

**F3 · Zweite Probe, danach Umsetzung?** Ich habe `/tmp/probe.txt` neu geschrieben (6 Aufrufe:
`.claude`, `/tmp` direkt und nach `cd`, Kopie nach `/tmp`, Wurzel, `handoff`). Erwartet:
1 FEHLER, 2 OK, 3 OK, 4 OK, 5 OK (bekannte Lücke), 6 FEHLER. Probierst du sie in derselben
Weise (Claude in `/tmp/arbiterKopie` neu starten, `/sandbox`, „Führe /tmp/probe.txt aus“)?
Und lohnt die Sandbox, wenn die Wurzel beim Hook bleibt, oder lässt du alles bei Anliegen 510?
Empfehlung: ja, zweite Probe; bei erwartetem Ergebnis setze ich `settings.json` um und kürze
`bashSchreiben.py` nur um Schreiben in die gesperrten Ordner.
Antwort: .
