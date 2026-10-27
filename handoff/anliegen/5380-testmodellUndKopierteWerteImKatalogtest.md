# Testmodell der Einheitstests und kopierte Werte im Katalogtest

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 9

## Runde 1
Kritik am Code aus Commit „Modell mit Bewegungsweite, QUE-10-Tests abgenommen“. Die
Architektur hält er ein: Die Domäne bekommt `Modell.bewegungsweite` und
`Ausgangslage.letzteSchlachtrunde` als Werte, `katalog/` liest sie aus `domaene/daten/`
(A2, A3, K4); dass die Architektur `letzteSchlachtrunde` nicht nennt, ist richtig so, sie
zählt die Felder der Ausgangslage nicht auf. Die Gliederung nach K2 und K3 (B je Modellart,
Tabelle der Schlüssel) kommt mit [Anliegen 4882](4882-itemKatalogwerteGliedern.md). Zwei
Befunde betreffen Ablage und Namen von Hilfen in den Tests; sie warten
([Ich 3](../../prozess/praemissen/ich.md)).

**Befund 1 · `testmodell` mit `__test__ = False`.** `technik/tests/einheit/modelle.py`
beginnt mit `test`; jedes `*Test.py`, das es importiert, böte es pytest als Test an, darum
`testmodell.__test__ = False`. Wer `aufstellenTest.py` liest, sieht den Grund nicht. Dazu hat
`modelle.py` kein Gegenstück in `arbiter/`, obwohl `tests/einheit/` es spiegelt
([Tests](../../technik/architektur/tests.md), Aufbau).
Gegenvorschlag: wie `zehnZoll` in `technik/tests/einheit/conftest.py`, als Fixture, die ein
*Modell* zu einer *Base* baut (`modellMit`), oder eine Funktion ohne `test` am Anfang; dann
entfällt `__test__`.

**Befund 2 · Katalogtest mit kopierten Werten.** In `technik/tests/einheit/katalog/ausgangslageTest.py`
lesen `testDieBewegungsweiteJedesModellsKommtAusDerAusgangslage` und
`testDieLetzteSchlachtrundeKommtAusOnlyWar` die echten Dateien (`ausgangslageLaden()`) und
vergleichen mit kopierten 5; ändert sich ein Wert in `domaene/daten/`, wird der Einheitstest
rot, obwohl `katalog/` richtig liest. Die übrigen Tests der Datei geben `ausgangslageAus`
eigene Daten; der Akzeptanztest liest die Werte ausdrücklich „nicht kopiert“
(`technik/tests/akzeptanz/schlacht.py`, `letzteSchlachtrunde`). Die Variable `zehnBoyz`
hält eine Menge von Bewegungsweiten, keine Boyz.
Gegenvorschlag: beide Tests über `ausgangslageAus` mit `einheitMitDurchmesser` und
`onlyWarMitKante(60)`, verglichen mit deren Werten.

**Kosten.** Je Befund wenige Zeilen in den Tests, kein Produktcode. Bis dahin prüfen die
Tests richtig; es kostet nur Lesezeit und einen grundlos roten Test bei neuen Daten.

**Stellungnahme.**
