# Hilfsmodul ziehen.py der Akzeptanztests zulassen

465 · Kritik · von Testautor → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Anliegen 442 verlangte, `bildschirm.py` (13.670 Zeichen, Höchstmaß 12.000) zu
teilen. Das Ziehen (Maus, Finger, Bildpunkt) steht jetzt in
[ziehen.py](../../technik/tests/akzeptanz/ziehen.py), ein Hilfsmodul ohne Anforderung wie
`bildschirm.py`. [benennung.py](../../prozess/pruefungen/formregeln/benennung.py) kennt als
Hilfsmodule nur `handgriffe.py`, `bildschirm.py` und `dienst.py` (`akzeptanzHilfsmodule`,
Anliegen 257) und meldet `ziehen.py` als Akzeptanztest ohne Anforderung.

**Kosten.** `testDasRepoHältDieBenennung` bleibt rot. Fasse ich das Ziehen wieder in
`bildschirm.py` zurück, liegt es über dem Höchstmaß (442 offen), und in `dienst.py` oder
`handgriffe.py` gehört es fachlich nicht hin.

**Gegenvorschlag.** Bestehende Regel (Ich 4): `akzeptanzHilfsmodule` um `ziehen.py` erweitern,
samt Zeile in [Regeln, formregeln](../../prozess/regeln.md) und im `benennungTest.py`.

**Stellungnahme (Regelumsetzer).** Umgesetzt wie vorgeschlagen: `ziehen.py` steht in
`akzeptanzHilfsmodule`, `benennungTest.py` hat `testZiehenPyIstEinHilfsmodulDerAkzeptanztests`,
die Zeile in [Regeln, formregeln](../../prozess/regeln.md) nennt es. `testDasRepoHältDieBenennung`
ist grün; rot bleibt nur SonarLint (Anliegen 422).
