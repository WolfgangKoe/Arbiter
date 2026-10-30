# Testmodell der Einheitstests und kopierte Werte im Katalogtest

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 2/3
Status: erledigt

## Runde 1
Kritik am Code aus Commit „Modell mit Bewegungsweite, QUE-10-Tests abgenommen“. Die
Architektur hält er ein: Die Domäne bekommt `Modell.bewegungsweite` und
`Ausgangslage.letzteSchlachtrunde` als Werte, `katalog/` liest sie aus `domaene/daten/`
(A2, A3, K4); dass die Architektur `letzteSchlachtrunde` nicht nennt, ist richtig so, sie
zählt die Felder der Ausgangslage nicht auf. Die Gliederung nach K2 und K3 (B je Modellart,
Tabelle der Schlüssel) kommt mit Anliegen 4882. Zwei
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
Befund 1: angenommen, zum Teil. `testmodell` heißt jetzt `modellMit` in
`technik/tests/einheit/modelle.py`, `__test__` entfällt. Eine Fixture in `conftest.py` taugt
nicht: `aufstellenTest.py` und `spielobjekteTest.py` bauen Modelle in Hilfsfunktionen und
mit `Base(durchmesser=32)`, ohne Fixture. Dass `modelle.py` kein Gegenstück in `arbiter/`
hat, lehne ich ab: es ist eine Testhilfe wie `conftest.py`, kein gespiegeltes Modul.
Befund 2: angenommen. Der Test der Bewegungsweite las schon `ausgangslageAus` mit eigenen
Daten. `testDieLetzteSchlachtrundeKommtAusOnlyWar` gibt jetzt eigene Daten (Runde 7) und
vergleicht mit ihnen; `einheitMitDurchmesser` gibt es nicht, `laden` genügt.

Status: angenommen

## Runde 2
Nachgeprüft an der uncommitteten Änderung: `modellMit` ohne `__test__`, alle Aufrufer in
`technik/tests/einheit/` umgestellt; `ausgangslageTest.py` gibt beiden Tests eigene Daten,
`zehnBoyz` ist weg. Einheitstests von `domaene/` und `katalog/ausgangslageTest.py` grün,
ruff sauber. Befund 2 ist erledigt.
Zu Befund 1 nehme ich deinen Widerspruch an: Eine Funktion ohne `test` am Anfang war mein
zweiter Vorschlag, und `modelle.py` ist eine Hilfe wie `handgriffe.py` bei den
Akzeptanztests. Den Satz dazu („daneben nur Hilfsmodule“) ergänze ich in
[Tests](../../technik/architektur/tests.md) beim Spiegel von `tests/einheit/`.

**Befund 3 · Docstring in `modelle.py`, hält auf.** Die Datei beginnt mit
`"""Modelle der Einheitstests: eine Base und die Bewegungsweite 5 Zoll."""`. Einen Docstring
gibt es nur als Kopf einer Akzeptanztestdatei ([Es 8](../../prozess/praemissen/es.md));
`modelle.py` ist die einzige Datei unter `technik/tests/einheit/` mit einem. Die Zeile wurde
in dieser Änderung angefasst, und sie stimmt nicht mehr: `modellMit` nimmt jede *Base*, nicht
eine; die 5 steht schon in `bewegungsweiteDerTestmodelle`. Runde 1 hat das übersehen.
Gegenvorschlag: Docstring streichen; die Namen `modellMit` und
`bewegungsweiteDerTestmodelle` sagen es.

**Kosten.** Eine Zeile, kein Produktcode.

**Stellungnahme.** Befund 3 angenommen: Der Docstring in
`technik/tests/einheit/modelle.py` ist gestrichen.
