# Akzeptanztests nach 978bc13: Handgriffe hängen am Dienst, Reste doppelt, Reihenfolge

337 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Geprüft: 978bc13 nach [Es](../../prozess/praemissen/es.md) und
[Wir 3](../../prozess/praemissen/wir.md). 331 und 332 sind erledigt; neu ist:
1. Richtung (Es, D): `handgriffe.py:12` importiert `dienst.py` für `spielstandDesVertrags`.
   Das Modul, das Spielstände mit der Domäne baut, hängt damit am Modul, das `web/` lädt
   (`dienst.py:7`); die Trennung aus 332 zeigt jetzt von innen nach außen. Importiert
   `dienst.py` einmal einen Handgriff, entsteht ein Kreis. Dazu nimmt
   `modelleAnDenStellenDesVertragsSetzen` alle `modelle` der Datei, ohne `spieler` zu lesen;
   das stimmt nur, weil das Beispiel allein Modelle von Spieler 2 hat.
2. Dieselbe Aussage mehrfach (Wir 3), in 332 von mir übersehen: Den Locator „Spieler an der
   Reihe“ schreiben `auf4Test.py:193` und `:208` noch aus, `spielerAnDerReihe` gibt es;
   `que2Test.py:11` hat `_anzahlGesetzterModelle = 3` neben
   `handgriffe.anzahlGesetzterModelle`.
3. Reihenfolge in `auf5Test.py`: Die zwei Bildschirmtests zum Beispiel (320, 330) stehen hinter
   AUF-5.10, der Dienst-Test (545) am Dateiende. Die Datei ist sonst je Block nach Kriterium
   geordnet; wer AUF-5.6 sucht, findet es an vier Stellen statt an zwei.

**Kosten.** 1: Ein Umbau des Dienstes (etwa eine zweite Route, Anliegen 249 Punkt 2 als
Importvertrag für `tests/akzeptanz/`) trifft dann auch die Handgriffe; bei einem zweiten
Beispiel im Vertrag mit Modellen beider Spieler setzt die Fixture still falsche Stellen.
2: je eine zweite Stelle, die beim nächsten Umbau der Kopfzeile vergessen wird. 3: Suchzeit
beim Lesen. Zusammen etwa 10 Zeilen, kein Zeichen mehr in `auf5Test.py`.

**Gegenvorschlag.** Bestehende Helfer statt neuer: `modelleSetzen` und `spielstandDesVertrags`.
1. `dienst.py` liest, `handgriffe.py` baut, `conftest.py` verbindet:
   ```
   # dienst.py
   def stellenDesVertrags(spielernummer: int) -> list[Stelle]: ...
   # handgriffe.py
   def modelleAnStellenSetzen(aufstellung, einheit, stellen) -> None: ...
   # conftest.py, aufstellungDesBeispiels
   modelleAnStellenSetzen(ausgangsaufstellung, necronWarriors, stellenDesVertrags(2))
   ```
   `handgriffe.py` importiert dann nichts aus `tests.akzeptanz.dienst`; `dienst.py` darf die
   Domäne kennen (`Stelle`), die Richtung zeigt nach innen.
2. `spielerAnDerReihe(seite)` in `auf4Test.py`; `anzahlGesetzterModelle` aus `handgriffe.py`
   in `que2Test.py`.
3. Die drei Tests hinter die übrigen ihres Kriteriums im selben Block schieben.

Erledigt, wenn `grep -n "akzeptanz.dienst" technik/tests/akzeptanz/handgriffe.py` leer ist,
die Stellen des Beispiels nach `spieler` gelesen werden und die Punkte 2 und 3 umgesetzt oder
einzeln begründet abgelehnt sind.

**Stellungnahme.** Angenommen, alle drei Punkte umgesetzt: `stellenDesVertrags(spielernummer)` in `dienst.py` liest nach `spieler`, `modelleAnStellenSetzen` in `handgriffe.py`, die Fixture verbindet beide; `handgriffe.py` importiert `dienst.py` nicht mehr. `spielerAnDerReihe` in `auf4Test.py`, `anzahlGesetzterModelle` in `que2Test.py`. Die drei Tests stehen bei ihrem Kriterium.
