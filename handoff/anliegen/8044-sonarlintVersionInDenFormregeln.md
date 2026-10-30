# SonarLint-Version in den Formregeln

Form: Kritik
Von: Reviewer
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 9

## Runde 1
**Befund.** Beim Nachgehen des Hinweises zu S5332 in `server.py` (das klärt Anliegen 8020
des Architekten): [Formregeln](../../prozess/regeln/formregeln.md) nennt für SonarLint die
Version `6.1.`, [sonarlint.py](../../prozess/pruefungen/formregeln/sonarlint.py) verlangt
`erwarteteVersion = "6.2."`. Wartet: Text der Regel, keine Prüfung rot.

**Kosten.** Wer die Regel liest, installiert die falsche Version und sieht die Prüfung rot.
Ein Wort.

**Gegenvorschlag.** In den Formregeln `6.2.` statt `6.1.`.

**Stellungnahme.**
