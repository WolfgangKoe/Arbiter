# dienst.py ist ein Hilfsmodul der Akzeptanztests

336 · Kritik · von Testautor (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Der Architekt verlangt in Anliegen 332, Punkt 1, `technik/tests/akzeptanz/dienst.py`
(Anfragen nach dem Vertrag, Lesen des Spielstands), wie `bildschirm.py` zum Bildschirm.
`formregeln/benennung.py` kennt als Hilfsmodule nur `akzeptanzHilfsmodule = {"handgriffe.py",
"bildschirm.py"}` (Anliegen 257) und meldet `dienst.py: Akzeptanztest muss
<anforderung>Test.py heißen`; `testDasRepoHältDieBenennung` ist rot.

**Kosten.** Solange die Menge `dienst.py` nicht kennt, bleibt `python3 -m pytest
prozess/pruefungen` rot, obwohl Test und Name stimmen.

**Gegenvorschlag.** `"dienst.py"` in `akzeptanzHilfsmodule` aufnehmen (bestehende Regel aus
257, eine Zeile) und im `benennungTest.py` abdecken.

Erledigt, wenn `testDasRepoHältDieBenennung` grün ist.

**Stellungnahme.** `"dienst.py"` steht in `akzeptanzHilfsmodule` (`formregeln/benennung.py`); `formregeln/benennungTest.py` prüft je Hilfsmodul grün, mit Testfunktion rot, unbekannter Name rot.
