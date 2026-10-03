# Benennung: drei offene Punkte

28 · Fragen · von Organisationsentwickler (Prozess) → Stakeholder · Runde 1/3 · angenommen

## Runde 1
**Befund.** Deine Entscheidung zur Benennung steht in
[`prozess/praemissen/wir.md`](../../prozess/praemissen/wir.md). Drei Fälle regelt sie nicht;
der Regelumsetzer braucht sie für die Prüfung, der Testautor für `aufstellenTest.py`.

**Kosten.** Ohne Antwort lässt die Prüfung diese Fälle aus, oder sie rät.

**F1 · Wie heißen Konstanten und Enum-Werte?** Heute `Grund.NICHT_WÄHLBAR` und `ZONE` in
`test_auf_1.py`. A: groß mit Unterstrich wie heute (PEP 8). B: camelCase wie Variablen
(`Grund.nichtWählbar`). Empfehlung A: Ein fester Wert ist auf einen Blick von einer
Variablen zu unterscheiden.

Antwort: B

**F2 · Wie heißen nummerierte Dateien (Etappen, Anliegen)?** A: Nummer, Bindestrich,
camelCase: `28-benennungOffenePunkte.md`. B: ohne Bindestrich: `28BenennungOffenePunkte.md`.
Empfehlung A: Die Nummer bleibt sichtbar getrennt; so ist diese Datei benannt.

Antwort: .

**F3 · Wie heißen Testdateien zu einem Modul (Unit-Tests, Tests der Prüfskripte)?** Heute
`test_bash_positivliste.py`. A: `<modul>Test.py` wie bei Akzeptanztests:
`bashPositivlisteTest.py`. B: `test<Modul>.py`: `testBashPositivliste.py`. Empfehlung A: eine
Form für alle Tests, Test und Modul stehen im Ordner nebeneinander.

Antwort: .

**Stellungnahme.**
