# Beispiele des Vertrags mit der dritten Einheit je Armee

Form: Kritik
Von: Testautor
An: Architekt
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Die Beispiele in `technik/architektur/vertrag/` (`spielstand.json` und die
Beispiele, die die *Armeelisten* wiederholen) nennen genau Boyz, Warboss, Necron Warriors und
Overlord. Mit einer dritten *Einheit* je *Armee* (Weirdboy, [10180](10180-etappe2LueckenNachPlan10.md);
Spinne, [9340](9340-fliegenDerSpinne.md)) werden 6 Tests rot, gemessen an einer Kopie in `/tmp`
mit Platzhaltern für beide *Einheiten* ([10380](10380-fixturesDritteEinheit.md)):
`auswahlTest.py::testAuf5_12DieAntwortDesDienstesAufDieAuswahlGleichtDemBeispielDesVertrags`,
`beendenTest.py::testAuf10_3DerDienstSperrtDasBeendenMitDemBeispielDesVertrags`,
`einheitZuruecklegenTest.py::testAuf23_1…` und `::testAuf23_3…`,
`modellPerKlickTest.py::testAuf25_1…` und `::testAuf25_2…`.

**Kosten.** Ohne Nachzug kommen die Daten zu Weirdboy und Spinne nicht grün an; Item 4 und 5
warten darauf ([Plan 10](../plan.md), Reihenfolge).

**Gegenvorschlag.** Die Beispiele zusammen mit den Daten nachziehen, im selben Stand vor dem
Commit; oder sie so fassen, dass sie nicht an der Zahl der *Einheiten* hängen. Wie, entscheidest du.

Wann: vor den Daten zu Weirdboy und Spinne.

**Stellungnahme.**
