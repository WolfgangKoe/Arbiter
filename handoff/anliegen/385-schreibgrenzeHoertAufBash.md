# Schreibgrenze hört auf Bash

385 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat in [384](384-schreibgrenzeAuchFuerBash.md) F1 mit A
entschieden. [Ich 2](../../prozess/praemissen/ich.md) sagt jetzt: Eine Rolle schreibt Dateien
nur mit Write und Edit und committet nicht; Bash nur zum Lesen, für Prüfungen, Tests und in
`/tmp`. [schreibgrenze.py](../../prozess/pruefungen/rollenregeln/schreibgrenze.py) hört nur
auf Write und Edit (`schreibwerkzeuge`, Matcher `Write|Edit` in `.claude/settings.json`);
Bash und Commit sind daher nur Text. Belege für Schreiben per Bash und eigene Commits in
Zyklus 5: Befund von 384.

**Kosten.** Ich 2 und 3 gelten nur auf dem Papier: Eine Rolle ändert ein fremdes Artefakt
unbemerkt, ein eigener Commit überspringt die Prüfung des Koordinators.

**Gegenvorschlag.** Bestehenden Mechanismus erweitern, keine neue Regel (384, Teil 3):
1. Matcher `Write|Edit|Bash`. Einer Rolle verweigert der Hook bei Bash: `sed -i`, `tee`,
   Umleitung `>` und `>>` außer nach `/dev/null` und `/tmp`, `rm`, `mv`, `cp`, `touch`,
   Python mit Skript in der Eingabe (`python3 -`, `python3 -c`) und git-Befehle, die Index,
   Arbeitsbaum oder Verlauf ändern (`add`, `commit`, `checkout`, `restore`, `reset`,
   `stash`, `rm`, `mv`), außer in einem Repo unter `/tmp`. Den Koordinator (ohne Rolle)
   betrifft das nicht.
2. Die Meldung nennt Write und Edit als Weg.
3. Scheiter-Test je Fall in `rollenregeln/schreibgrenzeTest.py`, dazu je ein erlaubter
   Aufruf: `python3 -m pytest …`, `git log`, `git status`, Umleitung nach `/tmp`.
4. Die Zeile in [Regeln](../../prozess/regeln.md#rollenregeln) nennt Bash statt „nicht Bash“.
   Bekannte Lücke: ein Skript aus `/tmp`, das selbst Dateien öffnet.

Erledigt, wenn die Tests grün sind und eine Rolle mit `sed -i` auf eine Datei im Projekt
verweigert wird. Danach ersetze ich bei Ich 2 „Bash und Commit: nur Text“ und setze 384
auf `angenommen`.

**Stellungnahme.**
