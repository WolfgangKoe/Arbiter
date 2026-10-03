# Akzeptanztest-Datei: Höchstmaß ohne Prüfung, Teilung bricht den Spiegel

44 · Fragen · von Architekt (Technik) → Stakeholder · Runde 1/3 · offen

## Runde 1
Deine Frage: Gibt es eine obere Grenze für Akzeptanztest-Dateien, und ist sie umgesetzt?

**Befund.**
- Eine Grenze gibt es, nur als Text: [`prozess/kennzahlen.md`](../../prozess/kennzahlen.md),
  Abschnitt Höchstmaße: Akzeptanztest-Datei 12.000 Zeichen Höchstmaß, 8.000 Kürzungsmaß,
  „Mechanismus: nur Text“. [`hoechstmassTest.py`](../../prozess/pruefungen/hoechstmassTest.py)
  prüft Etappen, Agenten, CLAUDE.md und Anliegen, keine Testdatei.
- Die Grenze ist schon überschritten: `aufstellenTest.py` hat 16.862 Zeichen, für eine
  einzige Anforderung (AUF-1, 7 Kriterien, 39 Tests). Gemessen schreibt ein Kriterium rund
  2.400 Zeichen Test; eine Anforderung darf 1.200 Zeichen haben
  ([`domaene/CLAUDE.md`](../../domaene/CLAUDE.md)) und erzeugt damit bis etwa 17.000.
- Teilen geht heute nicht: Prämisse 3 in [`wir.md`](../../prozess/praemissen/wir.md) verlangt
  genau eine Testdatei je Anforderungsdatei, und
  [`rueckverfolgung.py`](../../prozess/pruefungen/rueckverfolgung.py) sucht die Tests nur in
  `<anforderung>Test.py`. Stünde die zweite Hälfte in `aufstellen2Test.py`, meldete die
  Prüfung „AUF-1.5 hat keinen Test“.

**Kosten.** Die Datei wächst mit jeder Anforderung zu Aufstellen weiter; Read lädt sie ganz,
der Implementierer zahlt das bei jedem Lauf. Wer sie halbiert, bricht Prämisse und Prüfung.

**F1 · Wonach wird eine Akzeptanztest-Datei geteilt?**
- A: Eine Testdatei je Anforderung, im Ordner der Anforderungsdatei:
  `phasen/aufstellen.md` → `technik/tests/akzeptanz/phasen/aufstellen/auf1Test.py`.
  Höchstmaß 20.000, Kürzungsmaß 12.000. Wird eine Datei zu groß, ist die Anforderung zu groß
  und wird geteilt, nicht der Test. Der Schnitt ist fachlich und eindeutig.
- B: Eine Datei je Anforderungsdatei wie heute, 12.000 Zeichen. AUF-1 müsste schon jetzt
  Fälle streichen, gegen „Fälle vollständig“ in `.claude/agents/testautor.md`.
- C: Eine Datei je Kriterium (`auf1_4Test.py`, rund 2.400 Zeichen). Klein, aber 7 Dateien je
  Anforderung; die Helfer (`nachDerWahl`, `sperrgrund`) wandern in `conftest.py`.

Empfehlung A. Beispiel aus dem Altbestand: `ArbiterMap/backend/app/domain/rule_checks.py`
trennt nach Fachfrage (`check_coherency`, `check_engagement_range`), nicht nach Zeilenzahl;
ebenso schneidet A nach der
Anforderung, die schon Name und Zweck hat. A macht außerdem den Sprung aus
[Anliegen 46](46-sprungKriteriumUndTest.md) für die Anforderung trivial: `### AUF-1` gehört zu
genau einer Datei.

Antwort:

**F2 · Gilt die Teilung schon vor Review 1?** A: Nein, `aufstellenTest.py` bleibt bis zur
zweiten Anforderung zu Aufstellen; dann teilt der Testautor. B: Ja, sofort.
Empfehlung A: Unter A liegt die Datei mit 16.862 zwischen Kürzungs- und Höchstmaß und ist
erlaubt; eine Umbenennung jetzt kostet einen Testlauf und eine Kritikrunde ohne Gewinn.

Antwort:

**Nach deiner Antwort.** Ich passe `technik/architektur.md` (Tests) an. Prämisse 3 und
`kennzahlen.md` ändert der Organisationsentwickler; der Regelumsetzer erweitert
`hoechstmassTest.py` um `technik/tests/akzeptanz/**/*Test.py` und `rueckverfolgung.py` um
die neue Zuordnung, je mit Scheiter-Test.

**Stellungnahme.**
