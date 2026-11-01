# Gleichwertiger Mutant nennt den alten Modulnamen

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Nach [9540](9540-commitNach8840ModulOhneAnforderung.md) heißt
`technik/arbiter/domaene/phasen/bewegung/sperrenBeimZiehen.py` jetzt `normaleBewegung.py`.
Die Begründung des ersten Eintrags in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json)
(`messen.streckeÜberdeckt`) nennt als einzigen Aufrufer weiter `sperrenBeimZiehen`. Keine
Prüfung liest die Begründung, darum wartet der Befund ([Kritik](../../prozess/ablauf/kritik.md):
Namen, keine Prüfung rot).

**Kosten.** Ein Wort im Eintrag, unter 5.000 Token.

**Gegenvorschlag.** In der Begründung `sperrenBeimZiehen` durch `normaleBewegung` ersetzen.

**Stellungnahme.**
