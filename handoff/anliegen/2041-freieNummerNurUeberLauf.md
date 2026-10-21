# Der Befehl für freie Nummern läuft nicht wie in den Regeln genannt

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** [Regeln](../../prozess/regeln.md#anliegenregeln) nennen den Befehl
`python3 prozess/pruefungen/anliegenregeln/freieNummer.py <erste> <letzte>`, der Koordinator
gibt ihn so in jeden Auftrag. Aus dem Projektordner bricht er ab:
`ModuleNotFoundError: No module named 'gemeinsam'`. Es läuft
`python3 prozess/pruefungen/gemeinsam/lauf.py anliegenregeln.freieNummer 2040 2059`.

**Kosten.** Jede Rolle, die neue Anliegen schreibt, stößt darauf; wer den Umweg nicht findet,
vergibt Nummern von Hand.

**Gegenvorschlag.** Bestehende Regel: die Zeile zu `freieNummer` in `prozess/regeln.md`. Dort
den Befehl über `gemeinsam/lauf.py` nennen, wie bei den übrigen Befehlen, oder das Skript
direkt lauffähig machen; ein Test startet den genannten Befehl als Kindprozess.

**Stellungnahme.**
