# Commits: Befehl nimmt die Pfade mit `--aus` aus dem Arbeitsbaum der Rolle

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** [Commits](../../prozess/ablauf/commits.md) beschreibt den Befehl
`gemeinsam.commitImArbeitsbaum` so, dass er die Pfade aus dem gemeinsamen Arbeitsbaum übernimmt.
Seit Anliegen 16721 (Antwort A) kennt er `--aus <Arbeitsbaum>` vor der Nachricht: Die Pfade kommen
dann aus dem Arbeitsbaum der Rolle unter `.claude/worktrees/<name>/`; der kurze Arbeitsbaum des
Commits bleibt unter `/tmp`. Ohne `--aus` ist es wie bisher der Projektordner. Der Index der Pfade
wird im Quellordner angeglichen, bei Scheitern bleibt er unberührt. Gebaut und getestet:
[commitImArbeitsbaum.py](../../prozess/pruefungen/gemeinsam/commitImArbeitsbaum.py), Test
`testCommitNimmtDiePfadeAusDemArbeitsbaumDerRolleUndNichtAusDemProjektordner`.

**Kosten.** Eine Änderung in `prozess/ablauf/commits.md` (Schritte 2 und 3, Satz vor dem Befehl);
ohne sie weiß der Koordinator nichts von `--aus`.

**Gegenvorschlag.** In `commits.md` nach dem Satz zur Nachricht einfügen: „Schrieb die Rolle in
ihrem Arbeitsbaum unter `.claude/worktrees/<name>/`, steht vor der Nachricht
`--aus <Arbeitsbaum>` (Anliegen 16721); sonst ist der Quellordner der Projektordner.“ In Schritt 2
und 3 sowie im Satz zum Scheitern „gemeinsamen Arbeitsbaum“ durch „Quellordner“ ersetzen.

**Stellungnahme.** Umgesetzt wie vorgeschlagen in [Commits](../../prozess/ablauf/commits.md):
Der Satz zu `--aus <Arbeitsbaum>` steht nach dem Satz zur Nachricht; in Schritt 2 und 3 und im
Satz zum Scheitern heißt es jetzt „Quellordner“. Geprüft am Befehl: `main` nimmt `--aus` als
erstes Argument, ohne bleibt der Projektordner.
