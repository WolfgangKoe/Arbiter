# Kennzahlen und Höchstmaße

## Kennzahlen
Jede Kennzahl nennt Bedeutung, Schwelle und Reaktion. Über der Schwelle ist sie ein Befund
für die Retro. Mechanismus: nur Text.

- Prozesslast: Anteil der seit der letzten `Freigabe Retro` angelegten Anliegen, die an den
  Regelumsetzer oder den Organisationsentwickler gehen. Bedeutung: Der Prozess bindet die
  Arbeit, die das Produkt bräuchte. Schwelle: ein Drittel. Reaktion: Die Retro löscht
  mindestens einen Mechanismus, bevor sie einen neuen beauftragt, der nicht auf ein Anliegen
  des Stakeholders zurückgeht. Mechanismus: nur Text.
- Deckel: höchstens 10 offene Anliegen an den Regelumsetzer (Anliegen 296). Bedeutung: Die
  Kette einer Rolle hält das Produkt nicht auf. Reaktion: Darüber legt niemand ein neues an
  ihn an, außer bei Fehlverhalten ([Ablauf, Kritik am Code](ablauf.md#kritik-am-code)) oder
  vom Stakeholder, und der Koordinator beauftragt keinen neuen Mechanismus. Mechanismus: nur
  Text; der Stand nennt die offenen je Rolle (`standregeln/anliegenText.py`).

## Höchstmaße
In Zeichen. Geprüft (`formregeln/hoechstmassTest.py`): Etappen, Agentendefinition, Beschreibung,
Root- und Ordner-CLAUDE.md, Anliegen, `handoff/moderation.md` (4.000), Akzeptanztest-Datei
(20.000), Plan, Review, Retro je 4.000 (jede Zeile `Kommentar:` zählt als `Kommentar: .`,
Anliegen 167), je Datei in `domaene/mockups/` 8.000, Architektur (`technik/architektur.md`
und je Datei in `technik/architektur/`) 6.000, zusammen 24.000 (Anliegen 159, 211). Nur
Text: Anforderung, Item, Glossarzeile (`domaene/CLAUDE.md`), je Datei in `prozess/praemissen/`
3.000 (bis Anliegen 276).

Lebende Artefakte haben Höchst- und Kürzungsmaß: Über dem Höchstmaß sperrt die Prüfung, daraus
wird ein Item bis zum Kürzungsmaß; bis dahin wächst die Datei nicht. Kürzen heißt aufteilen,
weil Read die ganze Datei lädt. Code-Modul (auch `conftest.py`, Anliegen 251) und
Einheitstest-Datei 12.000/8.000, Akzeptanztest-Datei 20.000/12.000 (darüber wird die
Anforderung geteilt: Architektur, T1),
Anforderungsdatei 12.000/8.000, Backlog je Perspektive 3.000/2.000. Mechanismus: das
Höchstmaß der Akzeptanztest-Datei prüft `formregeln/hoechstmassTest.py`, alles andere hier nur Text.
