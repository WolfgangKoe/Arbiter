# Docstrings in technik/arbiter und den Unit-Tests

Form: Kritik
Von: Regelumsetzer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
**Befund.** Nach [Es 8](../../prozess/praemissen/es.md) steht ein Docstring nur als Kopf
einer Akzeptanztestdatei. In `technik/arbiter/` stehen 71, in `technik/tests/einheit/` einer.
Die Prüfung `docstringVerstößeUnterTechnik` in
[kommentare.py](../../prozess/pruefungen/formregeln/kommentare.py) meldet sie ab
`Freigabe Plan 9` (Test `testDasRepoHältDieDocstringregelUnterTechnik`); sie hält keinen
Commit auf, macht aber die DoD über das Inkrement rot.

**Kosten.** Am Bildschirm nichts. Bleiben sie, ist die DoD der Technikphase 9 rot.
Token: eine mechanische Änderung. Wo ein Docstring etwas erklärt, das der Name nicht trägt,
benenne um ([Es, Lesbarkeit](../../prozess/praemissen/es.md)).

**Gegenvorschlag.** Entferne jeden Docstring; wo er die einzige Anweisung ist, setze `...`.
Prüfe mit `python3 -m pytest prozess/pruefungen/formregeln/kommentareTest.py`.

**Stellungnahme.**
