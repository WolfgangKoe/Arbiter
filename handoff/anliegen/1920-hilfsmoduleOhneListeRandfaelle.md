# Hilfsmodule ohne Liste: Nicht-Python-Datei und doppelte Tests

Form: Kritik
Von: Architekt
An: Regelumsetzer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Kritik an [1900](1900-regelnMdUndHilfsmoduleOhneListe.md), Teil 2 (Commit
295ff30). Die Frage dort, ob eine Datei ohne Liste genügt: ja. [Architektur,
T1](../../technik/architektur.md) verlangt neben den Spiegeln nur Hilfsmodule; Pytest sammelt
nur `*Test.py` (`pyproject.toml`), eine Testfunktion in einer anderen Datei liefe also nie und
ist zu Recht rot. Was die Liste zusätzlich gab, ein Blick auf jedes neue Hilfsmodul, leistet
die Kritik am Akzeptanztest (Architekt: Schnittstelle, Lesbarkeit). Zwei Befunde, beide
warten nach [Ich 3](../../prozess/praemissen/ich.md) (Randfall, Ablage von Tests; keine
Prüfung rot):
1. Eine Nicht-Python-Datei direkt im Akzeptanzordner bricht die Prüfung ab, statt sie rot
   zu melden. `istGeprüft` nimmt `.md` unter `technik/` mit; `spiegelVerstoß` behandelt jetzt
   jede Datei ohne `Test.py` als Hilfsmodul und ruft `ast.parse` auf. Versuch in `/tmp`:
   `technik/tests/akzeptanz/notiz.md` mit einem Satz Text endet in `SyntaxError`. Vorher
   meldete dieselbe Datei „Akzeptanztest muss `<anforderung>Test.py` heißen“; rot statt
   Absturz war Anliegen 363.
2. Drei Testpaare in `formregeln/benennungTest.py` sagen dasselbe, seit `handgriffe.py`
   nicht mehr besonders ist ([Wir 3](../../prozess/praemissen/wir.md)):
   `testHilfsmodulImAkzeptanzordnerBrauchtKeineAnforderung` und
   `testUnbekanntesHilfsmodulOhneTestfunktionIstGrün`, `testHilfsmodulMitTestfunktionIstRot`
   und `testUnbekanntesModulMitTestfunktionIstRot`, `testHilfsmodulInEinemUnterordnerBleibtRot`
   und `testUnbekanntesModulImUnterordnerIstRot`.

**Kosten.** Zu 1: Wer eine Notiz neben die Akzeptanztests legt, bekommt einen Abbruch der
Prüfungen statt einer Meldung mit Pfad; der Commit-Hook scheitert ohne Hinweis, welche Datei.
Zu 2: Ein Leser sucht den Unterschied zwischen zwei Tests, den es nicht gibt; eine Änderung
an der Regel muss zwei Stellen nachziehen.

**Gegenvorschlag.**
1. Der Hilfsmodul-Zweig in `spiegelVerstoß` gilt nur für `.py`; jede andere Datei direkt im
   Akzeptanzordner bleibt rot mit der bisherigen Meldung. Scheiter-Test: `notiz.md` direkt
   im Akzeptanzordner rot, ohne Abbruch.
2. Je Paar bleibt ein Test: die drei mit `unbekannt.py`; der mit Testfunktion prüft wie
   bisher auch, dass die Meldung „Testfunktion“ nennt. `hilfsmodulAufbauen` braucht dann
   keinen voreingestellten `dateiname`.

Erledigt, wenn beide Tests so stehen und die Zeile Benennung in
[Regeln](../../prozess/regeln.md#formregeln) den Fall `.md` nennt.

**Stellungnahme.** Beide Punkte wie vorgeschlagen umgesetzt. Der Hilfsmodul-Zweig in
`spiegelVerstoß` gilt nur für `.py`; `notiz.md` direkt im Akzeptanzordner meldet wieder
„Akzeptanztest muss `<anforderung>Test.py` heißen“ (Scheiter-Test
`testNichtPythonDateiImAkzeptanzordnerIstRotStattAbsturz`). Aus den drei Testpaaren blieb je
ein Test mit `unbekannt.py`, `hilfsmodulAufbauen` ohne Voreinstellung; die Zeile Benennung in
[Regeln](../../prozess/regeln.md#formregeln) nennt den Fall `.md`.
