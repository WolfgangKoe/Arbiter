# Bash-Schreiben im Arbeitsbaum unter .claude/worktrees/ ist nicht erlaubt

Form: Fragen
Von: Regelumsetzer
An: Stakeholder
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Seit Anliegen 16380 dürfen Rollen im
Arbeitsbaum `.claude/worktrees/<name>/` mit Write und Edit schreiben. `rm` und `mv`
([Anliegen 418](../../prozess/regeln/rollenregeln.md)) prüft `rollenregeln/entfernen.py` noch gegen
den Projektordner; ein Pfad im Arbeitsbaum liegt dort in keinem Schreibpfad und wird gesperrt.
Eine Rolle im Arbeitsbaum kann daher Dateien weder löschen noch umbenennen.

**Kosten.** A: eine kleine Änderung in `entfernen.py` mit Test, ein Lauf des Regelumsetzers.

**Stellungnahme.**

**F1 · Sollen `rm` und `mv` im Arbeitsbaum wie im Projektordner gelten?**
A: Ja, `entfernen.py` kürzt `.claude/worktrees/<name>/` wie die Schreibgrenze; Scheiter-Test:
`rm` einer Datei in `…/prozess/…` erlaubt, in `…/domaene/…` gesperrt. (Anliegen 14360)
B: Nein, Löschen und Umbenennen bleiben im Projektordner. (neu)
Empfehlung: A, sonst bleibt die Parallelarbeit im Arbeitsbaum halb. Ohne Probe; Rückweg: Commit
zurücknehmen.
Antwort: A

## Stellungnahme des Regelumsetzers
Umgesetzt: `rollenregeln/entfernen.py` kürzt `.claude/worktrees/<name>/` wie die Schreibgrenze;
Scheiter-Tests in `rollenregeln/entfernenTest.py` (`rm` und `mv` in `prozess/` erlaubt, in
`domaene/` und `ArbiterMap/` gesperrt). Eingetragen in [rollenregeln](../../prozess/regeln/rollenregeln.md).
