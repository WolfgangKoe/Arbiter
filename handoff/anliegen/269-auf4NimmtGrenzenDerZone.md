# AUF-4.6 nimmt die Grenzen der Zone aus der Ausgangslage

269 · Kritik · von Architekt (Technik) → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik am Code von 9977e0e (Schnittstelle). Nach
Anliegen 263 liefert `Ausgangslage.grenzenDerZone(zone)` die
Fläche einer *Aufstellungszone*, Produktcode ruft nur noch diese Abfrage. Die Hilfsfunktion
`grenzenInXDerZone` ist nur deshalb noch öffentlich, weil
`technik/tests/akzeptanz/phasen/aufstellen/auf4Test.py` sie importiert,
in `testAuf4_6NachDerWahlZeigtDieKarteJedeZoneInDerFarbeDerModelleIhresSpielers`. Dafür holt
der Test `breite` und `tiefen[zone]` aus der Ausgangslage und setzt die Fläche selbst
zusammen, das, was 263 aus `web/` entfernt hat.

**Kosten.** Zwei Zeilen im Test: Der Import fällt weg, die Zeile `breite, _ = …` auch. Danach
macht der Implementierer `grenzenInXDerZone` privat, die Schnittstelle der Phase wird um eine
Funktion kleiner. Ohne die Änderung bleibt eine Hilfsfunktion öffentlich, die nur ein Test
braucht. Was der Test prüft, ändert sich nicht.

**Gegenvorschlag.**
`(zoneBeginnt, _), _ = ausgangslage.grenzenDerZone(zone)` statt
`grenzenInXDerZone(zone, breite, ausgangslage.tiefen[zone])`. Am billigsten zusammen mit
[259](259-handgriffeImportierenStattFixtures.md) und
[260](260-auf4WaehlenUndAlleBenennen.md), die dieselbe Datei ändern.

Erledigt, wenn `auf4Test.py` `grenzenInXDerZone` nicht mehr importiert und
`python3 -m pytest technik/tests` dieselben Tests grün hat wie vorher.

**Stellungnahme.** Angenommen, umgesetzt in `auf4Test.py`: Der Test nimmt `(zoneBeginnt, _), _ = ausgangslage.grenzenDerZone(zone)`; `grenzenInXDerZone` und die Zeile `breite, _ = …` sind weg, der Import entfällt. Der Implementierer kann `grenzenInXDerZone` privat machen.
