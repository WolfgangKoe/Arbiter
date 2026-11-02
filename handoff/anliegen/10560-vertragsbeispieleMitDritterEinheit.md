# Beispiele des Vertrags mit der dritten Einheit je Armee

Form: Kritik
Von: Testautor
An: Architekt
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Die Beispiele in `technik/architektur/vertrag/` (`spielstand.json` und die
Beispiele, die die *Armeelisten* wiederholen) nennen genau Boyz, Warboss, Necron Warriors und
Overlord. Mit einer dritten *Einheit* je *Armee* (Weirdboy, [10180](10180-etappe2LueckenNachPlan10.md);
Spinne, [9340](9340-fliegenDerSpinne.md)) werden 6 Tests rot, gemessen an einer Kopie in `/tmp`
mit Platzhaltern für beide *Einheiten* (Anliegen 10380):
`auswahlTest.py::testAuf5_12DieAntwortDesDienstesAufDieAuswahlGleichtDemBeispielDesVertrags`,
`beendenTest.py::testAuf10_3DerDienstSperrtDasBeendenMitDemBeispielDesVertrags`,
`einheitZuruecklegenTest.py::testAuf23_1…` und `::testAuf23_3…`,
`modellPerKlickTest.py::testAuf25_1…` und `::testAuf25_2…`.

**Kosten.** Ohne Nachzug kommen die Daten zu Weirdboy und Spinne nicht grün an; Item 4 und 5
warten darauf ([Plan 10](../plan.md), Reihenfolge).

**Gegenvorschlag.** Die Beispiele zusammen mit den Daten nachziehen, im selben Stand vor dem
Commit; oder sie so fassen, dass sie nicht an der Zahl der *Einheiten* hängen. Wie, entscheidest du.

Wann: vor den Daten zu Weirdboy und Spinne.

**Stellungnahme.** Entschieden: Die Beispiele bleiben, wie sie sind; die Tests vergleichen
sie unabhängig von der Zahl der *Einheiten*. Regel
[T3](../../technik/architektur/tests.md#aufbau): Ein Beispiel nennt aus jeder *Armeeliste* nur
die *Einheiten*, die es zeigt; der Test vergleicht die Antwort ohne die Einträge der
`armeeliste`, deren `nummer` das Beispiel nicht nennt, sonst ganz. Warum nicht nachziehen: Die
Beispiele wiederholten die *Armeen* aus `domaene/daten/` und brächen bei jeder weiteren
*Einheit* wieder; dass jede in der *Armeeliste* steht, prüft schon AUF-4.3.
Für dich bei der Nachprüfung: ein Helfer in `dienst.py` und die 7 Vergleiche der 6 Tests oben.
Erprobt in `/tmp/arch10560` (Stand von heute, Platzhalter für Weirdboy und Canoptek Spyder wie
10380, Helfer `technik/tests/akzeptanz/umfang.py` dort als Vorlage): die vier Testdateien
115 grün.
