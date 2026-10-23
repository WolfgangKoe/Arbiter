# Kennzahlen und Höchstmaße

## Kennzahlen
Jede Kennzahl nennt Bedeutung, Schwelle und Reaktion. Über der Schwelle ist sie ein Befund
für die Retro. Mechanismus: nur Text.

- Prozesslast: Anteil der seit der letzten `Freigabe Retro` angelegten Anliegen, die an den
  Regelumsetzer oder den Organisationsentwickler gehen. Bedeutung: Der Prozess bindet die
  Arbeit, die das Produkt bräuchte. Schwelle: ein Drittel. Reaktion: Die Retro löscht
  mindestens einen Mechanismus, bevor sie einen neuen beauftragt, der nicht auf ein Anliegen
  des Stakeholders zurückgeht. Mechanismus: nur Text.
- Prüfcode gegen Produktcode: neue Zeilen in `prozess/pruefungen/` gegen neue Zeilen in
  `technik/arbiter/` und `technik/frontend/`, beide ohne Tests, von der letzten
  `Freigabe Retro` bis `Freigabe Review`: `git diff --shortstat <von> <bis> --
  prozess/pruefungen ':!*Test.py' ':!*conftest.py'`, ebenso über die Produktordner.
  Bedeutung wie Prozesslast. Schwelle: mehr Prüfcode als Produktcode. Reaktion: wie
  Prozesslast (Anliegen 630, 730). Mechanismus: nur Text.
- Fortschritt des Produkts: aktuelle Etappe von allen, belegte Kriterien von allen. Die
  aktuelle ist die kleinste Nummer in `domaene/etappen/`, die Zahl aller die größte.
  Belegt ist ein Kriterium, das einen Akzeptanztest hat und das kein offenes Item des
  freigegebenen Plans nennt (`kriterienregeln/rueckverfolgung.py`); grün ist es dann nach
  DoD 1. Gezählt ohne Testlauf über alle Kriterien; je Etappe: [Backlog](backlog.md).
  Schwelle: kein Zuwachs in einem Zyklus. Reaktion: Die Retro nennt die Ursache; ihre
  Prozess-Items gelten nur ihr, Aufträge des Stakeholders und eine wiederholt verletzte
  Prämisse bleiben erlaubt (Anliegen 630, 691, 3451). Mechanismus: nur Text; Anzeige im Stand: Retro 5, P2.

## Höchstmaße
In Zeichen: Etappen, Agentendefinition, Beschreibung, Root- und Ordner-CLAUDE.md, Anliegen,
`handoff/moderation.md` (4.000), Plan, Review, Retro je 4.000 (jede Zeile `Kommentar:` zählt
als `Kommentar: .`, Anliegen 167; ohne den Abschnitt
[Fortschritt](ablauf.md#fortschritt), Anliegen 421), je Datei in `domaene/mockups/` 8.000, Architektur:
Regeln (`technik/architektur.md` und je Datei in `technik/architektur/`) je 6.000, zusammen
24.000 (Anliegen 159, 211); Vertrag je Phase eine Datei in `technik/architektur/vertrag/` zu
je 6.000, ohne Summe (Anliegen 2570); Anforderung, Item, Glossarzeile (`domaene/CLAUDE.md`), je Datei in
`prozess/praemissen/` 3.000.

Lebende Artefakte haben Höchst- und Kürzungsmaß: Über dem Höchstmaß wird daraus ein Item bis
zum Kürzungsmaß; bis dahin wächst die Datei nicht. Kürzen heißt aufteilen, weil Read die
ganze Datei lädt. Code-Modul (auch `conftest.py`, Anliegen 251) und Einheitstest-Datei
12.000/8.000, Akzeptanztest-Datei 20.000/12.000 (darüber wird die Anforderung geteilt:
Architektur, T1), Backlog je Perspektive 3.000/2.000.

Mechanismus: nur Text.
