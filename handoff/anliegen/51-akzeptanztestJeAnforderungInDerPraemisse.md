# Prämisse 3 und Kennzahlen: Akzeptanztest je Anforderung

51 · Kritik · von Architekt (Technik) → Organisationsentwickler · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder hat entschieden (Anliegen 44, Commit `91905db`, F1 = A, F2 = A):
Eine Akzeptanztest-Datei gehört zu einer Anforderung, nicht zu einer Anforderungsdatei;
`aufstellenTest.py` bleibt, bis `aufstellen.md` eine zweite Anforderung bekommt. Die
Architektur steht in [`technik/architektur.md`](../../technik/architektur.md), Regel T1.
Drei Texte im Prozess sagen noch das Alte:
1. [`wir.md`](../../prozess/praemissen/wir.md) Nr. 3: „Der Akzeptanztest zu einer
   Anforderungsdatei `<anforderung>.md` heißt `<anforderung>Test.py`.“
2. [`kennzahlen.md`](../../prozess/kennzahlen.md), Höchstmaße: Akzeptanztest-Datei
   12.000/8.000. `aufstellenTest.py` hat 16.862 Zeichen für eine Anforderung (AUF-1); eine
   Anforderung darf 1.200 Zeichen haben und erzeugt bis etwa 17.000.
3. Skill `akzeptanztest-schreiben`, Abschnitt Datei: „Eine Testdatei je Anforderungsdatei“.

**Kosten.** Der Testautor folgt bei der zweiten Anforderung zu Aufstellen der Prämisse und
schreibt in dieselbe Datei; das Höchstmaß ist heute schon verletzt.

**Gegenvorschlag.**
1. Nr. 3: „Der Akzeptanztest zur Anforderung AUF-1 in `domaene/anforderungen/phasen/aufstellen.md`
   heißt `technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py`. Hat die Anforderungsdatei
   nur eine Anforderung, genügt `phasen/aufstellenTest.py`.“
2. `kennzahlen.md`: Akzeptanztest-Datei 20.000/12.000, getrennt von Code-Modul und
   Einheitstest; Zusatz: „Über dem Höchstmaß wird die Anforderung geteilt, nicht der Test.“
3. Skill: Abschnitt Datei wie Nr. 1; das Beispiel nennt `aufstellenTest.py` als heutige Form.

Mechanismus (Höchstmaß, Zuordnung) baut der Regelumsetzer:
[Anliegen 52](52-akzeptanztestJeAnforderung.md).

**Stellungnahme.**
