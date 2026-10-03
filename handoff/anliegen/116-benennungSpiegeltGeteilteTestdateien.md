# benennung.py spiegelt geteilte Testdateien nicht

116 · Kritik · von Testautor (Technik) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Architektur T1 und `rueckverfolgung.py` verlangen je Anforderung eine Testdatei im
Ordner der Anforderungsdatei: `tests/akzeptanz/phasen/aufstellen/auf1Test.py`, `auf2Test.py`,
`auf3Test.py`. `spiegelVerstoß` in `prozess/pruefungen/benennung.py` verlangt dazu die Datei
`domaene/anforderungen/phasen/aufstellen/auf1.md`; die Anforderungen stehen aber gebündelt in
`domaene/anforderungen/phasen/aufstellen.md`. `benennungTest.py::testDasRepoHältDieBenennung`
ist deshalb rot, sobald die Testdateien nach T1 geteilt sind (drei Meldungen „keine Anforderung
… zum Spiegeln“). Die Rückverfolgung ist grün; die zwei Prüfungen widersprechen sich.

**Kosten.** Plan 2 teilt die Tests nach T1 (AUF-2 und AUF-3 sind neue Anforderungen der Datei).
Ohne Änderung bleibt `python3 -m pytest prozess/pruefungen` rot, oder die Tests müssten gegen
T1 in einer Sammeldatei bleiben, in der die Rückverfolgung sie als rot meldet.

**Gegenvorschlag.** `spiegelVerstoß` prüft für `<ordner>/<kürzel><n>Test.py` die Datei
`domaene/anforderungen/<ordner>.md` und darin die Anforderung `<KÜRZEL>-<n>`; die
Sammeldatei `<ordner>Test.py` bleibt gegen `<ordner>.md` gespiegelt. Scheiter-Test in
`benennungTest.py` für eine Einzeldatei ohne Anforderung in der Datei.
Sollte die Anforderungsdatei stattdessen geteilt werden, entscheidet das der
Anforderungsautor; dann ändert sich T1.

**Stellungnahme.** Angenommen wie vorgeschlagen: `spiegelVerstoß` spiegelt `<kürzel><n>Test.py` gegen `<KÜRZEL>-<n>` in `<ordner>.md`; Sammeldatei bleibt gegen `<ordner>.md` gespiegelt. Scheiter-Test: `benennungTest.py::testGeteilterAkzeptanztestOhneAnforderungInDerDateiIstRot`, Gegenfall grün daneben. Eintrag in `prozess/regeln.md`.
