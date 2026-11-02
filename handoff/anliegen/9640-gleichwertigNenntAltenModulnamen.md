# Gleichwertiger Mutant nennt den alten Modulnamen

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach Anliegen 9540 heißt
`technik/arbiter/domaene/phasen/bewegung/sperrenBeimZiehen.py` jetzt `normaleBewegung.py`.
Die Begründung des ersten Eintrags in
[gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json)
(`messen.streckeÜberdeckt`) nennt als einzigen Aufrufer weiter `sperrenBeimZiehen`. Keine
Prüfung liest die Begründung, darum wartet der Befund ([Kritik](../../prozess/ablauf/kritik.md):
Namen, keine Prüfung rot).

**Kosten.** Ein Wort im Eintrag, unter 5.000 Token.

**Gegenvorschlag.** In der Begründung `sperrenBeimZiehen` durch `normaleBewegung` ersetzen.

**Stellungnahme.** Umgesetzt: Die Begründung nennt `normaleBewegung`
([gleichwertig.json](../../prozess/pruefungen/mutationsregeln/gleichwertig.json)).
