# Kennzahlen und Höchstmaße

## Kennzahlen
Jede Kennzahl nennt Bedeutung, Schwelle und Reaktion. Über der Schwelle ist sie ein Befund
für die Retro. Mechanismus: nur Text.

- Prozesslast: Anteil der seit der letzten `Freigabe Retro` angelegten Anliegen, die an den
  Regelumsetzer oder den Organisationsentwickler gehen. Bedeutung: Der Prozess bindet die
  Arbeit, die das Produkt bräuchte. Schwelle: ein Drittel. Reaktion: Die Retro löscht
  mindestens einen Mechanismus, bevor sie einen neuen beauftragt, der nicht auf ein Anliegen
  des Stakeholders zurückgeht. Mechanismus: nur Text.

## Höchstmaße
In Zeichen. Geprüft (`hoechstmassTest.py`): Etappen, Agentendefinition, Beschreibung,
Root- und Ordner-CLAUDE.md, Anliegen, `handoff/moderation.md` (4.000), Akzeptanztest-Datei
(20.000), Plan, Review, Retro je 4.000 (jede Zeile `Kommentar:` zählt als `Kommentar: .`,
Anliegen 167), je Datei in `domaene/mockups/` 8.000, Architektur (`technik/architektur.md`
und je Datei in `technik/architektur/`) 6.000, zusammen 24.000 (Anliegen 159, 211). Nur
Text: Anforderung, Item, Glossarzeile (`domaene/CLAUDE.md`).

Lebende Artefakte haben Höchst- und Kürzungsmaß: Über dem Höchstmaß sperrt die Prüfung, daraus
wird ein Item bis zum Kürzungsmaß; bis dahin wächst die Datei nicht. Kürzen heißt aufteilen,
weil Read die ganze Datei lädt. Code-Modul und Einheitstest-Datei 12.000/8.000,
Akzeptanztest-Datei 20.000/12.000 (darüber wird die Anforderung geteilt: Architektur, T1),
Anforderungsdatei 12.000/8.000, Backlog je Perspektive 3.000/2.000. Mechanismus: das
Höchstmaß der Akzeptanztest-Datei prüft `hoechstmassTest.py`, alles andere hier nur Text.
