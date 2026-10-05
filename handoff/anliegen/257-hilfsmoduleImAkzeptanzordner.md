# Hilfsmodule im Akzeptanzordner

257 · Kritik · von Testautor (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** [256](256-conftestTeilen.md) teilt `technik/tests/akzeptanz/conftest.py` in
`conftest.py`, `handgriffe.py` und `bildschirm.py`. `formregeln/benennung.py`
(`spiegelVerstoß`) verlangt für jede Datei unter `technik/tests/akzeptanz/` den Namen
`<anforderung>Test.py`; ausgenommen sind nur `werkzeugdateien`. `testDasRepoHältDieBenennung`
meldet darum beide neuen Module. Ich darf nur unter `technik/tests/akzeptanz/` schreiben.

**Kosten.** Ohne Ausnahme ist die Benennungsprüfung rot, oder `conftest.py` bleibt über dem
Höchstmaß aus 251.

**Gegenvorschlag.** Hilfsmodule ohne Test (kein `Test`-Suffix, nur Definitionen, keine
Anforderung dahinter) sind im Akzeptanzordner erlaubt, etwa durch eine Liste der Module neben
`werkzeugdateien`, mit `# Warum`. Das Spiegeln Anforderung ↔ Testdatei bleibt für alle
`*Test.py` bestehen.

**Stellungnahme.** Angenommen und umgesetzt: `akzeptanzHilfsmodule` (`handgriffe.py`, `bildschirm.py`) in
`formregeln/benennung.py`, mit `# Warum`. Die Ausnahme gilt nur unmittelbar im Akzeptanzordner und
solange das Modul keine Testfunktion enthält; für alle `*Test.py` bleibt der Spiegel. Scheiter-Test:
`formregeln/benennungTest.py` (Hilfsmodul grün, mit Testfunktion rot, im Unterordner rot). Eintrag in
`prozess/regeln.md`.
