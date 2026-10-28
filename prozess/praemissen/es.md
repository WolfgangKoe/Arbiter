# Prämissen · Es

Handwerk am Code: Produkt (Python und Frontend), Tests, Prüfskripte, Hooks. Entschieden vom
Stakeholder, Ausnahmen nur über ihn; Kritik daran: Architekt.

## Lesbarkeit und Benennung
Code liest sich wie Fachtext; der Name trägt die Bedeutung ([Wir](wir.md)). Bezeichner
deutsch mit Umlauten, Dateinamen ASCII.

1. Funktionen, Methoden, Variablen, Parameter, Fixtures, Konstanten und Enum-Werte in
   camelCase (`aufstellenDerEinheitBeenden`, `Grund.nichtWählbar`), Klassen und Typaliase in
   PascalCase. Mechanismus: `formregeln/benennung.py`.
2. Dateinamen in camelCase, ASCII; nummeriert `28-benennungOffenePunkte.md`; Test zu einem
   Modul `<modul>Test.py`. Namen, die ein Werkzeug vorgibt (`conftest.py`, `__init__`,
   `CLAUDE.md`, Skill-Ordner), bleiben; Etappen, Items und Anliegen werden nicht umbenannt.
   Mechanismus: `formregeln/benennung.py`.
3. Akzeptanztests entstehen vor dem Code, je Anforderung eine Datei nach
   [T1](../../technik/architektur/tests.md). Mechanismus:
   `kriterienregeln/rueckverfolgung.py` (`<anforderungsdatei>Test.py`), sonst nur Text.
4. Testfunktionen `test<Kürzel><n>_<m><Satz>`: `testAuf7_3EinModellEinerAnderenEinheitIstEinheitBegonnen`
   (Skill `akzeptanztest-schreiben`). Mechanismus: `formregeln/benennung.py`,
   `kriterienregeln/rueckverfolgung.py`.
5. Selbst definierte Namen haben mindestens 3 Zeichen; Ausnahme `x` und `y` als Felder von
   `Stelle` (Architektur S1). Mechanismus: `formregeln/benennung.py`.
6. Keine Indizes auf Fachobjekte (`einheiten[0]`): benennen oder entpacken. Mechanismus: nur Text.
7. Kein lambda als Hülle um einen Aufruf, keine Bindung per Standardargument. Mechanismus:
   nur Text.
8. Der Code erklärt sich selbst. Ein Docstring steht nur als Kopf einer Akzeptanztestdatei
   nach [T1](../../technik/architektur/tests.md), sonst keiner (6430). Kommentare
   nur als Werkzeugkommentar mit Regelcode (`# noqa: <Code>`,
   `// eslint-disable-next-line <Regel>`) und `TODO: <was>`, höchstens drei; ein TODO von
   vor der laufenden Technikphase macht die DoD über das Inkrement rot. Mechanismus:
   `formregeln/kommentare.py`, `frontendregeln/eslintKommentare.mjs`; Docstring: nur Text.
9. Die Form folgt der Verständlichkeit: wenige Fälle als `if` mit frühem `return`; viele, die
   sich nur in Daten unterscheiden, als Tabelle; viele mit eigenem Verhalten als eigene Typen.
   Urteil des Reviewers, Schwellen: [Ablauf, DoD](../ablauf/dod.md).

## SOLID
- S: Ein Modul hat eine Aufgabe; sein Name nennt sie. Mechanismus: Urteil des Reviewers.
- O: Ein neuer Fall kommt als Zeile, Katalogdatum oder Typ hinzu, nicht als Zweig in
  bestehendem Code (9). Mechanismus: nur Text.
- L, I: Ein Untertyp hält den Vertrag seines Obertyps; eine Schnittstelle verlangt nur, was
  ihr Nutzer aufruft. Mechanismus: nur Text.
- D: Abhängigkeiten zeigen nach innen, ohne Kreis: im Produkt nach
  [Architektur, A1 und A2](../../technik/architektur.md). Mechanismus:
  `formregeln/importvertrag.py`.
