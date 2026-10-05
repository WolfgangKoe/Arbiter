# Prämissen · Es

Handwerk am Code: Produkt (Python und Frontend), Tests, Prüfskripte, Hooks. Entschieden vom
Stakeholder, Ausnahmen nur über ihn; Kritik daran: Architekt.

## Lesbarkeit und Benennung
Code liest sich wie Fachtext; der Name trägt die Bedeutung ([Wir](wir.md)). Bezeichner
deutsch mit Umlauten, Dateinamen ASCII.

1. Funktionen, Methoden, Variablen, Parameter, Fixtures, Konstanten und Enum-Werte in
   camelCase (`einheitInAufstellungWählen`, `Grund.nichtWählbar`), Klassen und Typaliase in
   PascalCase. Mechanismus: `formregeln/benennung.py`.
2. Dateinamen in camelCase, ASCII; nummeriert `28-benennungOffenePunkte.md`; Test zu einem
   Modul `<modul>Test.py`. Namen, die ein Werkzeug vorgibt (`conftest.py`, `__init__`,
   `CLAUDE.md`, Skill-Ordner), bleiben; Etappen, Items und Anliegen werden nicht umbenannt.
   Mechanismus: `formregeln/benennung.py`.
3. Je Anforderung eine Akzeptanztest-Datei nach [Architektur, T1](../../technik/architektur.md).
   Mechanismus: `kriterienregeln/rueckverfolgung.py` (`<anforderungsdatei>Test.py`), sonst nur Text.
4. Testfunktionen `test<Kürzel><n>_<m><Satz>`: `testAuf1_4EinModellDerEinheitInAufstellungLässtSichSetzen`
   (Skill `akzeptanztest-schreiben`). Mechanismus: `formregeln/benennung.py`,
   `kriterienregeln/rueckverfolgung.py`.
5. Selbst definierte Namen haben mindestens 3 Zeichen; Ausnahme `x` und `y` als Felder von
   `Stelle` (Architektur S1). Mechanismus: `formregeln/benennung.py`.
6. Keine Indizes auf Fachobjekte (`einheiten[0]`): benennen oder entpacken. Mechanismus: nur Text.
7. Kein lambda als Hülle um einen Aufruf, keine Bindung per Standardargument. Mechanismus:
   nur Text.
8. Kommentare nur einzeilig als `# Regel: <Fundstelle>` oder `# Warum: …` (nicht
   offensichtlich); Docstrings einzeilig; kein TODO, FIXME, Prozessverweis. Mechanismus:
   `formregeln/kommentare.py`; Prozessverweis: nur Text.
9. Die Form folgt der Verständlichkeit: wenige Fälle als `if` mit frühem `return`; viele, die
   sich nur in Daten unterscheiden, als Tabelle; viele mit eigenem Verhalten als eigene Typen.
   Urteil des Reviewers, Schwellen: [Ablauf, DoD](../ablauf.md#dod-item-fertig).

## SOLID
- S: Ein Modul hat eine Aufgabe; sein Docstring nennt sie. Urteil des Reviewers. Mechanismus:
  nur Text.
- O: Ein neuer Fall kommt als Zeile, Katalogdatum oder Typ hinzu, nicht als Zweig in
  bestehendem Code (9). Mechanismus: nur Text.
- L: Ein Untertyp hält den Vertrag seines Obertyps. Noch ohne Anlass: keine Klassenhierarchie.
- I: Eine Schnittstelle verlangt nur, was ihr Nutzer aufruft. Noch ohne Anlass.
- D: Abhängigkeiten zeigen nach innen, ohne Kreis: im Produkt nach
  [Architektur, A1 und A2](../../technik/architektur.md), in den Prüfskripten nach den
  Schichten aus Anliegen 253. Mechanismus: `formregeln/importvertrag.py`, für die
  Prüfskripte nur Text.
