# Kommentar des Stakeholders zählt nicht zur Länge

Form: Kritik
Von: Regelumsetzer
An: Organisationsentwickler
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Wortlaut des Stakeholders: „Meine Kommentare und Zusätze sollten nicht unter die
Kürzungsregel fallen.“ Anlass: [15900](15900-bewegenAlsOberklasse.md) hatte durch seinen
Kommentar 4.935 Zeichen und blockierte jeden Commit. Die Prüfung
`anliegenregeln/anliegenLaenge.py` zählt nun auch jede Zeile `Kommentar:` als
`Kommentar: .` ([Anliegenregeln](../../prozess/regeln/anliegenregeln.md)). Weitere Zeilenanfänge
nur des Stakeholders in Anliegen gibt es nicht: `Freigabe:` steht nur in Plan, Review und
Retro ([Freigabe](../../prozess/ablauf/freigabe.md)), `Stellungnahme:` schreibt der Autor.
Bestehende Regel, die angepasst wird (Ich 4): [Anliegen](../../prozess/ablauf/anliegen.md),
Zeilen 4 und 5.

**Kosten.** Eine Textzeile; kein Mechanismus.

**Gegenvorschlag (Regelumsetzer).** In `prozess/ablauf/anliegen.md` den Satz „jede Zeile
`Antwort:` zählt als `Antwort: .`“ ändern in „jede Zeile des Stakeholders (`Antwort:`,
`Kommentar:`) zählt als `Antwort: .` oder `Kommentar: .`“. Gesperrt bis „Freigabe Retro 10“.
Probe in `/tmp`: Prüfungen und Tests grün, 15900 besteht; Rückweg: die zwei Änderungen in
`anliegenLaenge.py` und seinem Test zurücknehmen.

**Stellungnahme.** Umgesetzt nach Freigabe Retro 10: [Anliegen](../../prozess/ablauf/anliegen.md)
nennt jetzt jede Zeile des Stakeholders (`Antwort:`, `Kommentar:`), wie vorgeschlagen.
