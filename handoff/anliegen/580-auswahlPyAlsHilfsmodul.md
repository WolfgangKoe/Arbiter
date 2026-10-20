# auswahl.py als Hilfsmodul der Akzeptanztests zulassen

580 · Kritik · von Testautor → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Anliegen [550](550-auswahlGehoertNichtZumZiehen.md) verlangt die Hilfen zur
*Auswahl* in einem eigenen Modul `technik/tests/akzeptanz/auswahl.py`. Die Liste
`akzeptanzHilfsmodule` in [benennung.py](../../prozess/pruefungen/formregeln/benennung.py)
nennt es nicht; die Benennungsprüfung würde die Datei als Akzeptanztest ohne Anforderung melden.

**Kosten.** Ohne den Eintrag ist die Prüfung rot, sobald das Modul angelegt ist.

**Gegenvorschlag.** Wie in Anliegen 465 für `ziehen.py`: `"auswahl.py"` in
`akzeptanzHilfsmodule` aufnehmen (eine Zeile). Erledigt, wenn
`python3 -m pytest prozess/pruefungen/formregeln/benennungTest.py` mit einer vorhandenen
`auswahl.py` grün ist. Ich lege das Modul an, sobald der Eintrag steht.

**Stellungnahme.** Angenommen und umgesetzt: `"auswahl.py"` steht in `akzeptanzHilfsmodule`.
Scheiter-Test `testAuswahlPyIstEinHilfsmodulDerAkzeptanztests` in `benennungTest.py` (ohne
Eintrag rot), Eintrag in [Regeln](../../prozess/regeln.md). Das Modul kann angelegt werden.
