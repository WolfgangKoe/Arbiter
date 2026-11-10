# Änderungen aus dem Arbeitsbaum unter .claude/worktrees/ kommen nicht nach dev

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Nach Anliegen 16380 schreibt eine Rolle
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

## Runde 2
**Befund.** Deine Frage: Wird `/tmp` nach Neustart oder durch VS Code gelöscht, und ist das ein
Risiko? Ja, beim Neustart räumt Ubuntu `/tmp`, und Dateien über 30 Tage ohne Zugriff verfallen;
VS Code löscht es nicht. Ein Risiko für deine Arbeit ist das nicht: `/tmp` enthält nur den
Arbeitsbaum, den der Commit-Befehl für die Dauer eines Commits anlegt und danach entfernt
(`finally` in `commitImArbeitsbaum.py`). Die Änderungen der Rolle liegen davor im Projektordner
(bei A in `.claude/worktrees/`), der Commit danach in `.git` (`refs/heads/dev`). Stürzt der Rechner
mitten im Commit ab, geht nur die Kopie in `/tmp` verloren: `dev` bleibt unverändert, die Änderungen
liegen unberührt im Projektordner, der Befehl lässt sich erneut ausführen. Ein toter Eintrag in
`.git/worktrees/` verschwindet mit `git worktree prune`. Gelesen, nicht erprobt.

**Kosten.** Bleibt es bei `/tmp`: keine. Anderer Ort: Änderung in `commitImArbeitsbaum.py` samt Test
im selben Lauf wie A.

**Gegenvorschlag.** Siehe F1.

**Stellungnahme.**

**F1 · Bleibt der kurze Arbeitsbaum des Commits unter `/tmp`?**
A: Ja, er bleibt unter `/tmp`; er lebt nur Sekunden, ein Verlust kostet nichts. (Anliegen 11100)
B: Er liegt im Projektordner unter `.git/`, damit ihn kein Neustart berührt. (neu)
Empfehlung: A, es geht nichts verloren und es ändert sich nichts. Ohne Probe; Rückweg: keiner nötig.
Antwort: A

**Stellungnahme (Regelumsetzer, umgesetzt).** Der Befehl kennt `--aus <Arbeitsbaum>`, nimmt die
Pfade von dort und committet im kurzen Arbeitsbaum unter `/tmp`. Mechanismus
[commitImArbeitsbaum.py](../../prozess/pruefungen/gemeinsam/commitImArbeitsbaum.py), Scheiter-Test
`testCommitNimmtDiePfadeAusDemArbeitsbaumDerRolleUndNichtAusDemProjektordner`, eingetragen in
[Rollenregeln](../../prozess/regeln/rollenregeln.md). Die Beschreibung in `commits.md` gehört dem
Organisationsentwickler: Anliegen 16820.
