# Docstrings in den Akzeptanztests außer dem Kopf

Form: Kritik
Von: Regelumsetzer
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Nach [Es 8](../../prozess/praemissen/es.md) steht ein Docstring nur als Kopf
einer Akzeptanztestdatei. In `technik/tests/akzeptanz/` stehen 118 weitere, zusätzlich zu den
31 Köpfen; sechs Fixtures bestehen nur aus dem Docstring und brauchen `...` an seiner Stelle.
Die Prüfung `docstringVerstößeUnterTechnik` in
[kommentare.py](../../prozess/pruefungen/formregeln/kommentare.py) meldet sie ab
`Freigabe Plan 9` (Test `testDasRepoHältDieDocstringregelUnterTechnik`); sie hält keinen
Commit auf, macht aber die DoD über das Inkrement rot.

**Kosten.** Am Bildschirm nichts. Bleiben sie, ist die DoD der Technikphase 9 rot.
Token: eine mechanische Änderung, je Docstring eine Zeile weniger; den Kopf lässt du stehen
([spiegel.py](../../prozess/pruefungen/formregeln/spiegel.py) prüft seinen Wortlaut weiter).

**Gegenvorschlag.** Entferne jeden Docstring außer dem Modul-Docstring der Datei; wo er die
einzige Anweisung ist, setze `...`. Prüfe mit
`python3 -m pytest prozess/pruefungen/formregeln/kommentareTest.py`.

**Stellungnahme.** Umgesetzt wie vorgeschlagen: In `technik/tests/akzeptanz/` steht nur noch
der Kopf jeder Testdatei; entfernt sind 117 Docstrings in 19 Dateien, auch die Modulköpfe der
Hilfsmodule (`handgriffe.py`, `conftest.py` und andere), die keine Akzeptanztestdateien sind.
Sechs Funktionen bestehen nur noch aus `...`, nach `ruff format` auf einer Zeile. Das Verhalten
ist unverändert: Der Syntaxbaum jeder Datei gleicht dem vorigen ohne die Docstrings, und
nichts liest `__doc__`. `kommentareTest.py` ist grün, `ruff check` und `ruff format --check`
auch.
