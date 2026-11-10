# Änderungen aus dem Arbeitsbaum unter .claude/worktrees/ kommen nicht nach dev

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: rückfrage

## Runde 1
**Befund.** Nach [Anliegen 16380](16380-arbeitsbaumUnterClaudeWorktrees.md) schreibt eine Rolle
im eigenen Arbeitsbaum. Der Commit ([Commits](../../prozess/ablauf/commits.md), P4) läuft über
`gemeinsam/commitImArbeitsbaum.py` und nimmt die Pfade aus dem Projektordner; er kennt nur einen
Arbeitsbaum unter `/tmp`. Wie die Änderungen aus `.claude/worktrees/<name>/` nach `dev` kommen,
ist nicht geregelt.

**Kosten.** A: ein Lauf des Regelumsetzers, Änderung in `commitImArbeitsbaum.py` samt Test; sie
berührt den Commit-Weg aller Rollen.

**Stellungnahme.**

**F1 · Wie kommen Änderungen des Arbeitsbaums nach `dev`?**
A: Der Commit-Befehl nimmt die Pfade aus dem Arbeitsbaum der Rolle und committet sie wie bisher in
`/tmp` auf `dev`; der Koordinator ruft ihn mit dem Arbeitsbaum als Quelle. (Anliegen 14360)
B: Der Koordinator führt den Arbeitsbaum vor dem Commit von Hand in den Projektordner zurück.
(neu)
Empfehlung: A, es bleibt beim einen Weg des Commits. Ohne Probe; Rückweg: Commit zurücknehmen.
Antwort: A
Kommentar: Kann es passieren, dass der Inhalt von tmp nach Neustart des Rechners oder von VS Code gelöscht wird? Falls ja, wäre das nicht ein Risiko?
Stellungnahme: Ja, `/tmp` wird gelöscht: beim Neustart des Rechners (Ubuntu räumt es beim Start) und nach 30 Tagen Nichtgebrauch; VS Code selbst löscht es nicht. Ein Risiko für deine Arbeit ist das nicht. In `/tmp` liegt nur der kurze Arbeitsbaum, den der Commit-Befehl für die Dauer eines Commits anlegt und danach entfernt (`finally` in `commitImArbeitsbaum.py`). Die Änderungen der Rolle liegen davor im Projektordner (bei A in `.claude/worktrees/`), der Commit danach in `.git` (`refs/heads/dev`); beides nicht in `/tmp`. Stürzt der Rechner mitten im Commit ab, geht nur die Kopie in `/tmp` verloren: `dev` ist dann unverändert, die Änderungen liegen unberührt im Projektordner, der Befehl lässt sich erneut ausführen. Ein toter Eintrag in `.git/worktrees/` verschwindet mit `git worktree prune`. Gelesen, nicht erprobt. A gilt; ein Lauf des Regelumsetzers setzt es um, sobald er beauftragt ist.
