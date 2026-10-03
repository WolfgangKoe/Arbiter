# AUF-1-Tests: Sperrtests ohne unveränderten Zustand

48 · Kritik · von Reviewer (Technik) → Testautor · Runde 1/3 · angenommen

## Runde 1
Gegenstand: [`aufstellenTest.py`](../../technik/tests/akzeptanz/phasen/aufstellenTest.py).

**Befund 1 · D2 ist bei sieben Sperrtests nicht belegt.** [`architektur.md`](../../technik/architektur.md)
D2: „Prüft: jeder Akzeptanztest einer Sperre prüft den unveränderten Zustand.“ Nur den
`Grund` prüfen:
- `testAuf1_2DieAufstellungszoneVorDemGewinnerIstNichtWählbar` (Gewinner, Zone)
- `testAuf1_4VorDerWahlIstSetzenNichtInAufstellung` (`erstesModell.gesetzt`)
- `testAuf1_4OhneEinheitInAufstellungIstBeendenNichtInAufstellung` (`anDerReihe`)
- `testAuf1_4VorDerWahlIstBeendenNichtInAufstellung` (`anDerReihe`, `beendet`)
- `testAuf1_4NachDemBeendenGibtEsKeineEinheitZumErneutenBeenden` (`anDerReihe`)
- `testAuf1_5NachDerAufstellungIstKeineEinheitWählbar` (`einheitInAufstellung`)
- `testAuf1_5GegenEineNichtWählbareEinheitGiltNichtWählbarAuchNachBegonnenerEinheit`
  (`einheitInAufstellung is begonneneEinheit`)

Kosten: Setzt `aufstellenDerEinheitBeenden` erst `anDerReihe` weiter und sperrt dann, bleiben
alle Tests grün. Genau diese Reihenfolge braucht später das Übergehen.
Gegenvorschlag: je eine Zeile `assert` auf den in Klammern genannten Zustand.

**Befund 2 · Doppelter Test.** `testAuf1_2ErstDerGewinnerDannDieAufstellungszoneIstErlaubt`
macht dieselben Schritte und prüft dasselbe wie
`testAuf1_1DieGewählteAufstellungszoneGehörtDemGewinner` mit `ersteZone`.
Kosten: rund 300 Zeichen in einer Datei, die über dem Kürzungsmaß liegt
([Anliegen 44](44-akzeptanztestDateiZuLang.md)).
Gegenvorschlag: streichen; AUF-1.2 bleibt durch die übrigen `testAuf1_2…` belegt.

**Befund 3 · Parameter als Zeichenkette mit Nachschlagen.**
`testAuf1_5NachDerAufstellungIstKeineEinheitWählbar` parametrisiert über vier Namen und holt
die Einheit per `einheiten[gewählteEinheit]` aus einem Wörterbuch; das ist der Zugriff, den
[`wir.md`](../../prozess/praemissen/wir.md) Nr. 6 vermeiden will, und zehn Zeilen Aufbau.
Gegenvorschlag: ohne Parameter in einer Schleife über alle vier Einheiten den Grund prüfen
(`assert all(sperrgrund(…, einheit) is Grund.nichtWählbar for einheit in …)`), oder die
Einheiten-Fixtures direkt parametrisieren.

**Stellungnahme.** Angenommen. Befund 1: Die sieben Sperrtests prüfen jetzt den unveränderten
Zustand (`gewinner`, `aufstellungszone`, `gesetzt`, `anDerReihe`, `beendet`,
`einheitInAufstellung`). Befund 2: der doppelte Test ist gestrichen. Befund 3: eine Liste der
Gründe über die vier Einheiten statt Parameter und Wörterbuch.
