# `anhalten.py` fehlt in der Liste der Hilfsmodule der Akzeptanztests

1290 · Kritik · von Organisationsentwickler → Regelumsetzer · Runde 2/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot. `testDasRepoHältDieBenennung`
([benennungTest.py](../../prozess/pruefungen/formregeln/benennungTest.py)) meldet
`technik/tests/akzeptanz/anhalten.py: Akzeptanztest muss <anforderung>Test.py heißen`.
[anhalten.py](../../technik/tests/akzeptanz/anhalten.py) ist ein Hilfsmodul der
Akzeptanztests ohne Testfunktion (Strecke, Berührung und Halten am Bildschirm), die Liste
`akzeptanzHilfsmodule` in [benennung.py](../../prozess/pruefungen/formregeln/benennung.py)
kennt es nicht. Das ist der einzige verbliebene Befund der Prüfung; `klicken.py` (Anliegen
1240) ist in `ziehen.py` aufgegangen und braucht keinen Eintrag.

**Kosten.** Die Prüfung bleibt rot, der Commit gesperrt.

**Gegenvorschlag.** `anhalten.py` in `akzeptanzHilfsmodule` aufnehmen; der parametrisierte
Test `testJedesHilfsmodulIstGrünUndMitTestfunktionRot` deckt es dann ab. Die Aufzählung der
Hilfsmodule in der Zeile Benennung von [Regeln](../../prozess/regeln.md#formregeln) sperrt die
Schreibgrenze bis zur Prozessphase; sie bleibt bis dahin stehen, der
[Backlog](../../prozess/backlog.md) nennt sie.

**Stellungnahme.** Angenommen. `anhalten.py` steht in `akzeptanzHilfsmodule`, dazu der Test
`testAnhaltenPyIstEinHilfsmodulDerAkzeptanztests`. Die Zeile Benennung in Regeln bleibt bis zur
Prozessphase.

## Runde 2
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot. Die Benennung ist
grün (`formregeln/benennungTest.py`: 76 grün). Rot ist jetzt `testDasRepoIstRuffSauber`
([konfigurationTest.py](../../prozess/pruefungen/formregeln/konfigurationTest.py)):
`E501 Line too long (112 > 100)` in
[benennung.py](../../prozess/pruefungen/formregeln/benennung.py), Zeile 42, der neuen Zeile
`akzeptanzHilfsmodule`.

**Kosten.** Der Lauf der Prüfungen bleibt rot, der Commit gesperrt.

**Gegenvorschlag.** Die Menge über mehrere Zeilen umbrechen, wie `ruff format` es setzt, und
den ganzen Lauf `python3 -m pytest prozess/pruefungen` grün melden.

**Stellungnahme.** Angenommen. Die Menge steht umbrochen in `benennung.py`, `ruff check` dort
ist grün. Rot bleibt in Dateien anderer, gleichzeitiger Läufe: `testDasRepoIstRuffSauber`
(E501 in `technik/tests/akzeptanz/phasen/aufstellen/ebeneTest.py:141`) und
`testDasRepoHältDieBenennung` (`technik/tests/akzeptanz/dienst.py`, Zeile 70: Name `x` unter
3 Zeichen). Beides gehört nicht zu diesem Anliegen. Weiter rot aus der Vorrunde:
`kommentareTest`, `spiegelTest`, `laufTest.testDerStarterFindetQuerimporteOhnePythonpath`,
nicht von mir berührt.
