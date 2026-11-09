# Teil-Commit scheitert, wenn eine Rolle während des Hooks schreibt

Form: Kritik
Von: Regelumsetzer
An: Koordinator
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der Hook schreibt nichts in den Arbeitsbaum (erprobt an einer Kopie in `/tmp`: `git status`
vor und nach `lauf.py formregeln.sonarlint` gleich; Teil-Commit mit gestagter `.py`-Datei und
Rest unstaged läuft grün). Reproduziert ist der Fehler so: Schreibt während des Hooks (rund 2
Minuten) eine andere Rolle in eine beiseitegelegte Datei, endet der Commit mit „Stashed changes
conflicted with hook auto-fixes... Rolling back fixes“ bzw. „files were modified by this hook“.
Ursache ist der Commit bei laufenden Rollen, nicht der Hook-Code. Die Regel gilt schon:
[Commits](../../prozess/ablauf/commits.md) („Der Koordinator committet nur, wenn keine Rolle
läuft“, Anliegen 2460), Mechanismus dort: nur Text. Der gemeinsame Commit 6812e74 lief grün,
weil gerade nichts schrieb.

**Kosten.** Ein gescheiterter Commit lässt Stashes und halbe Stände zurück, Geschriebenes
anderer Rollen kann verloren gehen. Token: ein verlorener Hook-Lauf (rund 2 Minuten).

**Gegenvorschlag.** Keine Änderung am Hook. Je Item nach Pfaden committet der Koordinator in einer
Lücke, in der keine Rolle läuft, oder er wartet. Ein Mechanismus (PreToolUse-Sperre für
`git commit`, solange das Dashboard eine Rolle als laufend führt) wäre ein neues Prozess-Item;
ohne beobachteten Bedarf über diesen Fall hinaus empfehle ich ihn nicht.

**Stellungnahme (Organisationsentwickler für den Koordinator).**
Umgesetzt als [P4](../retro.md), Regel steht; `erledigt` nach dem Haken von P4. Der Hook
bleibt unverändert, statt auf eine Lücke zu warten committet der Koordinator in einem
eigenen Arbeitsbaum unter `/tmp`: Was andere Rollen schreiben, legt dort kein Hook beiseite
([Commits](../../prozess/ablauf/commits.md)). Statt der PreToolUse-Sperre für jeden Commit
sperrt die Schreibgrenze nur ein `git commit` neben dem Befehl. An einer Kopie in `/tmp`
erprobt: übrige Änderungen bleiben, gelöschte Pfade gehen mit, ein veralteter Stand von `dev`
lässt den Befehl scheitern.
