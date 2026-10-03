# Prämissen · Wir

Sprache und Kultur des Agentensystems, entschieden vom Stakeholder. Ausnahmen nur über ihn.

## Lesbarkeit und Benennung
Gilt für jeden Code: Produkt (Python und Frontend), Tests, Prüfskripte in
`prozess/pruefungen/`, Hooks. Code liest sich wie Fachtext; der Name trägt die Bedeutung.
Bezeichner sind deutsch mit Umlauten, Dateinamen ASCII.

1. Funktionen, Methoden, Variablen, Parameter und Fixtures in camelCase
   (`einheitInAufstellungWählen`), Klassen in PascalCase (`Aufstellungszone`).
   Mechanismus: `benennung.py`.
2. Dateinamen in camelCase, ASCII. Bestehende Dateien, die ohnehin gelöscht werden (Etappen,
   Items, Anliegen), werden nicht umbenannt; Anforderungsdateien schon. Mechanismus: `benennung.py`.
3. Der Akzeptanztest zu einer Anforderungsdatei `<anforderung>.md` heißt
   `<anforderung>Test.py`, im gespiegelten Ordner: `domaene/anforderungen/phasen/aufstellen.md`
   → `technik/tests/akzeptanz/phasen/aufstellenTest.py`. Mechanismus: `benennung.py`,
   `rueckverfolgung.py`.
4. Testfunktionen heißen `test<Kürzel><n>_<m><Satz>`, Kriterium AUF-1.4:
   `testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen`. Mechanismus: `benennung.py`,
   `rueckverfolgung.py`.
5. Selbst definierte Namen haben mindestens 3 Zeichen; keine einbuchstabigen Namen.
   Mechanismus: `benennung.py`.
6. Keine Indizes auf Fachobjekte (`einheiten[0]`): benennen oder entpacken.
   Mechanismus: nur Text.
7. Keine lambda-Tricks: kein lambda als Hülle um einen Aufruf, keine Bindung per
   Standardargument (`lambda e=einheit: …`). Mechanismus: nur Text.
8. Kommentare nur einzeilig als `# Regel: <Fundstelle>` (nicht offensichtlicher
   Regel-Sonderfall) oder `# Warum: …` (nicht offensichtliche technische Entscheidung);
   Docstrings höchstens einzeilig; kein TODO, FIXME oder Prozessverweis. Mechanismus: nur Text.

Namen, die ein Werkzeug vorgibt (`conftest.py`, `__init__`, `CLAUDE.md`, Skill-Ordner),
bleiben. Offen: Konstanten und Enum-Werte, nummerierte Dateinamen, Testdateien zu Modulen
([Anliegen 28](../../handoff/anliegen/28-benennungOffenePunkte.md)).
Wie ein Akzeptanztest danach aussieht: Skill `akzeptanztest-schreiben`.
