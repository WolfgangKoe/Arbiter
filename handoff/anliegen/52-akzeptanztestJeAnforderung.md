# Prüfungen: Akzeptanztest je Anforderung und sein Höchstmaß

52 · Kritik · von Architekt (Technik) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Entschieden vom Stakeholder (Anliegen 44, Commit `91905db`): je Anforderung eine
Akzeptanztest-Datei, Regel T1 in [`technik/architektur.md`](../../technik/architektur.md);
Text der Prämisse: [Anliegen 51](51-akzeptanztestJeAnforderungInDerPraemisse.md).
1. [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py) sucht Tests nur in
   `<pfad>Test.py`. Liegen die Tests zu AUF-2 in `phasen/aufstellen/auf2Test.py`, meldet sie
   „AUF-2.1 hat keinen Test“.
2. [`hoechstmassTest.py`](../../prozess/pruefungen/hoechstmassTest.py) prüft keine
   Testdatei; `kennzahlen.md` nennt das Höchstmaß „nur Text“. `aufstellenTest.py` hat 16.862
   Zeichen, vorgeschlagen sind 20.000 (Anliegen 51).

**Kosten.** Ohne 1 bricht die Prüfung, sobald der Testautor bei der zweiten Anforderung zu
Aufstellen teilt; ohne 2 wächst eine Datei unbemerkt, Read lädt sie ganz.

**Gegenvorschlag.**
1. `rueckverfolgung.py`: Die Tests zur Anforderung `<KÜRZEL>-<n>` in
   `domaene/anforderungen/<pfad>.md` stehen in `technik/tests/akzeptanz/<pfad>/<kürzel><n>Test.py`.
   Hat die Anforderungsdatei genau eine Anforderung, gilt stattdessen `<pfad>Test.py`; ab der
   zweiten ist `<pfad>Test.py` rot („teilen nach Anforderung“). So erzwingt die Prüfung den
   Zeitpunkt, den der Stakeholder gewählt hat (F2 = A). Jede Datei enthält nur Tests ihrer
   Anforderung. `benennung.py` erkennt die neue Form als Testdatei.
2. `hoechstmassTest.py`: `technik/tests/akzeptanz/**/*Test.py` gegen den Wert aus
   `kennzahlen.md`, sobald Anliegen 51 ihn festlegt.
3. Scheiter-Tests: zweite Anforderung mit Tests in `<pfad>Test.py` ist rot; Test zu AUF-2 in
   `auf1Test.py` ist rot; Testdatei über dem Höchstmaß ist rot.

**Stellungnahme.** Umgesetzt: Testdatei je Anforderung ab der zweiten (`<pfad>/<kürzel><n>Test.py`), `<pfad>Test.py` ab dann rot, Test in fremder Anforderungsdatei rot; Höchstmaß 20.000 für Akzeptanztests in `hoechstmassTest.py`. In `prozess/kennzahlen.md` und `technik/architektur.md` steht noch „nur Text“ bzw. „bisher nur die Form“; das ändert der Organisationsentwickler bzw. der Architekt.
