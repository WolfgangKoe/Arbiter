# Prämissen · Wir

Sprache und Kultur des Agentensystems, entschieden vom Stakeholder. Ausnahmen nur über ihn.

## Lesbarkeit und Benennung
Gilt für jeden Code: Produkt (Python und Frontend), Tests, Prüfskripte in
`prozess/pruefungen/`, Hooks. Code liest sich wie Fachtext; der Name trägt die Bedeutung.
Bezeichner sind deutsch mit Umlauten, Dateinamen ASCII.

1. Funktionen, Methoden, Variablen, Parameter und Fixtures in camelCase
   (`einheitInAufstellungWählen`), Klassen und Typaliase in PascalCase (`Aufstellungszone`).
   Mechanismus: `benennung.py`.
2. Dateinamen in camelCase, ASCII. Bestehende Dateien, die ohnehin gelöscht werden (Etappen,
   Items, Anliegen), werden nicht umbenannt; Anforderungsdateien schon. Mechanismus: `benennung.py`.
3. Je Anforderung eine Akzeptanztest-Datei; Name und Ort nach
   [Architektur, T1](../../technik/architektur.md). Mechanismus: `benennung.py`,
   `rueckverfolgung.py` für `<anforderungsdatei>Test.py`; die Datei je Anforderung: nur Text
   (Anliegen 52).
4. Testfunktionen heißen `test<Kürzel><n>_<m><Satz>`, Kriterium AUF-1.4:
   `testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen`. Mechanismus: `benennung.py`,
   `rueckverfolgung.py`.
5. Selbst definierte Namen haben mindestens 3 Zeichen; keine einbuchstabigen Namen.
   Ausnahme: die Achsen `x` und `y` als Felder von `Stelle` (Architektur S1, Anliegen 135).
   Mechanismus: `benennung.py` (`koordinatenfelder`).
6. Keine Indizes auf Fachobjekte (`einheiten[0]`): benennen oder entpacken.
   Mechanismus: nur Text.
7. Keine lambda-Tricks: kein lambda als Hülle um einen Aufruf, keine Bindung per
   Standardargument (`lambda e=einheit: …`). Mechanismus: nur Text.
8. Kommentare nur einzeilig als `# Regel: <Fundstelle>` (nicht offensichtlicher
   Regel-Sonderfall) oder `# Warum: …` (nicht offensichtliche technische Entscheidung);
   Docstrings höchstens einzeilig; kein TODO, FIXME oder Prozessverweis. Mechanismus:
   `kommentare.py` (Python: Form, einzeilig, TODO und FIXME); Prozessverweis: nur Text.
9. Die Form folgt der Verständlichkeit: wenige Fälle als `if` mit frühem `return`; viele,
   die sich nur in Daten unterscheiden, als Tabelle oder Katalogdaten; viele mit eigenem
   Verhalten als eigene Typen. Es urteilt der Reviewer. Mechanismus: nur Text; die Schwellen
   für Verschachtelung und Zahl der Fälle: [Ablauf, DoD](../ablauf.md#dod-item-fertig).

Namen, die ein Werkzeug vorgibt (`conftest.py`, `__init__`, `CLAUDE.md`, Skill-Ordner),
bleiben. Konstanten und Enum-Werte in camelCase wie Variablen (`Grund.nichtWählbar`).
Nummerierte Dateien: Nummer, Bindestrich, camelCase (`28-benennungOffenePunkte.md`).
Testdateien zu einem Modul: `<modul>Test.py`. Mechanismus: `benennung.py`.
Wie ein Akzeptanztest danach aussieht: Skill `akzeptanztest-schreiben`.
