# Einheitstest des Katalogs mit der dritten Einheit je Armee

Form: Kritik
Von: Testautor
An: Implementierer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** `technik/tests/einheit/katalog/ausgangslageTest.py`, Test
`testDieAusgangslageLadenNenntDieEinheitenWieIhreDatenblätter`, entpackt
`boyz, warboss = ausgangslageLaden().ersterSpieler.armee.einheiten`. Mit dem Weirdboy
([10180](10180-etappe2LueckenNachPlan10.md)) bricht er ab (`too many values to unpack`),
gemessen an einer Kopie in `/tmp` ([10380](10380-fixturesDritteEinheit.md)).

**Kosten.** Ohne Nachzug kommen die Daten zum Weirdboy nicht grün an; Item 5 wartet darauf
([Plan 10](../plan.md), Reihenfolge).

**Gegenvorschlag.** Die *Einheiten* unabhängig von ihrer Zahl finden, etwa am Namen, wie die
Fixtures `boyz` und `warboss` in `technik/tests/akzeptanz/conftest.py`.

Wann: vor den Daten zu Weirdboy und Spinne.

**Stellungnahme.** Umgesetzt in `technik/tests/einheit/katalog/ausgangslageTest.py`: Der Test findet die Boyz am Namen und prüft, dass Boyz und Warboss in der *Armee* stehen, unabhängig von der Zahl der *Einheiten*. `technik/tests/einheit/katalog` grün (56). `prozess/pruefungen`: 960 grün, 1 rot (`rueckverfolgungTest`, fehlende Akzeptanztestdateien wie `orkPsionikerTest.py`, nicht aus diesem Anliegen).
