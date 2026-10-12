# AUF-16.5 ohne Test gegen den Vertrag

407 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Commit 960d2ce prüft AUF-16.5 in der Domäne und am Bildschirm, aber nicht die
Anfrage, die [V5](../../technik/architektur/handlungen.md) dafür neu festlegt
(`DELETE /api/spieler/<s>/einheiten/<e>/stelle?ablage=<a>`). „Prüft“ in `handlungen.md`
verlangt je Kriterium einen Test mit dem Flask-Testclient gegen V5 und V6.
`testAuf16_5DieSeiteNenntBei…` wartet mit `aufDieHandlungWarten` auf irgendein `PUT` oder
`DELETE` und prüft nur `409`. Beispiel: Schickte die Seite beim Loslassen der Boyz auf der
*Ablage* von Spieler 2 stattdessen `DELETE …/einheiten/1/modelle/1/stelle?ablage=2`
(Zeile *Modell* auf der *Ablage*, AUF-16.3), käme dieselbe *Sperre* ‚nicht wählbar‘ zurück
und der Test bliebe grün. Weder Pfad und Methode noch der Körper der 409 (`gründe` und
unveränderter `spielstand`, V6) hat einen Test. Die Unit-Tests des Implementierers prüfen nur
400 und 404.

**Kosten.** Klein: ein Handgriff und ein Test, etwa 15 Zeilen. Ohne sie kann die Zeile in V5
von Seite und `web/` gemeinsam abweichen, ohne dass ein Test rot wird; V5 wäre dann die
einzige Zeile der Tabelle ohne Testclient-Test.

**Gegenvorschlag.**
1. In `technik/tests/akzeptanz/dienst.py` neben `modellZurücklegen` ein Handgriff
   `einheitAufAblageLoslassen(dienst, aufstellung, einheit, spielernummer)` über
   `pfadDerEinheit` und `query_string={"ablage": spielernummer}`.
2. In `loslassenOhneZielTest.py` ein Test wie
   `testAuf16_5DerDienstSperrtEineEinheitAufDerAblageDesAnderenSpielersMitNichtWählbar`:
   `davor = spielstandVon(dienst)`, dann der Handgriff mit den Boyz und Spieler 2;
   `assert antwort.status_code == HTTPStatus.CONFLICT` und
   `assert antwort.get_json() == {"gründe": [Grund.nichtWählbar.value], "spielstand": davor}`.
   Vorbild: `testAuf9_1…` in `gesperrtesModellTest.py` (`modellLoslassen(dienst, …)`).

Domänentest und Bildschirmtest bleiben, wie sie sind: Sie lesen sich wie das Kriterium,
benennen nach es.md 4 und folgen 16.4 in Aufbau und Prüfungen.

**Stellungnahme.** Angenommen, beide Punkte umgesetzt. Der Handgriff `einheitAufAblageLoslassen`
steht in [dienst.py](../../technik/tests/akzeptanz/dienst.py). Der Test
`testAuf16_5DerDienstSperrtEineEinheitAufDerAblageDesAnderenSpielersMitNichtWählbar` in
[loslassenOhneZielTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/loslassenOhneZielTest.py)
prüft 409, `gründe` und unveränderten `spielstand`. Er läuft für beide Fälle aus 409 (Boyz auf
der Ablage von Spieler 2, Necron Warriors auf der von Spieler 1).
