# QUE-3.1: Klick und Tippen teilen sich eine Aufstellung

Form: Kritik
Von: Reviewer
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Kritik am Code, `git diff 90801c5 819896b`. Hält auf nach
[Kritik](../../prozess/ablauf/kritik.md): eine Prüfung ist rot.
`testQue3_1EinTippenAufDieKarteLöstDasselbeAusWieEinKlick`
([bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py)) ist seit
`819896b` rot (`data-ebene` fehlt), auf `90801c5` grün (beide Stände erprobt, der alte als
`git archive` in `/tmp`).
Ursache ist der Test, nicht der Code: Beide Seiten laufen auf zwei Servern, aber mit derselben
`aufstellungNachDerZonenwahl`. Der Klick mit der Maus macht das *Modell* zur *Ebene*; das
Tippen auf der zweiten Seite trifft dieselbe *Aufstellung* und macht nach AUF-25.2 die ganze
*Einheit* wieder zur *Ebene*. Bisher fiel das nicht auf, weil die Seite ein `PUT …/ebene`
schickte, das zweimal dasselbe tat; seit Anliegen 8030 geht jeder Klick über
`modellAnklicken`, und der wechselt.

**Kosten.** Bleibt es, ist QUE-3.1 rot, obwohl Klick und Tippen gleich wirken, und die DoD über
das Inkrement bleibt rot. Eine Fixture und zwei Zeilen.

**Gegenvorschlag.** Jede Seite bekommt ihre eigene *Aufstellung*, etwa die zweite als
`copy.deepcopy(aufstellungNachDerZonenwahl)` nach `modelleSetzen`; dann prüft der Test, dass
dieselbe Handlung auf zwei gleichen Ständen dasselbe zeigt. Prüfe dabei auch die übrigen Tests
der Datei, die `seiteZu` zweimal mit derselben *Aufstellung* rufen (sie sind heute nur grün,
weil die *Einheitenkarte* ihren Zustand aus der eigenen Seite liest).

**Stellungnahme.**
