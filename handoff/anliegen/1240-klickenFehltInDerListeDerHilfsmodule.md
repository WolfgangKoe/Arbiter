# `klicken.py` fehlt in der Liste der Hilfsmodule der Akzeptanztests

1240 · Kritik · von Testautor → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf, denn eine Prüfung ist rot.
`testDasRepoHältDieBenennung` ([benennungTest.py](../../prozess/pruefungen/formregeln/benennungTest.py))
meldet `technik/tests/akzeptanz/klicken.py: Akzeptanztest muss <anforderung>Test.py heißen`. Die
Liste `akzeptanzHilfsmodule` in [benennung.py](../../prozess/pruefungen/formregeln/benennung.py)
kennt `handgriffe`, `bildschirm`, `dienst`, `ziehen` und `auswahl`, aber nicht `klicken.py`
(Klickhandgriffe von Maus und Finger, in ebeneTest, modellPerKlickTest und weiteren benutzt).

**Kosten.** Die Prüfung bleibt rot, der Commit gesperrt.

**Gegenvorschlag.** `klicken.py` in `akzeptanzHilfsmodule` aufnehmen.

**Stellungnahme.**
Anders behoben: Die Klickhandgriffe stehen in `ziehen.py`, `klicken.py` ist gelöscht; die Liste
bleibt unverändert.
