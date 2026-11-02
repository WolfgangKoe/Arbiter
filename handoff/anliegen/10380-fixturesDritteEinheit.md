# Fixtures unabhängig von der Zahl der Einheiten je Armee

Form: Kritik
Von: Planer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Etappe 2 bringt je *Armee* eine dritte *Einheit*: den Weirdboy bei den Orks
([MIV-2](../../domaene/anforderungen/missionsvorbereitung/orkPsioniker.md)) und die
Canoptek-Spinne bei den Necrons ([9340](9340-fliegenDerSpinne.md)). Die Fixtures `boyz`,
`warboss`, `necronWarriors` und `overlord` (`technik/tests/akzeptanz/conftest.py:157` bis
`:177`) erwarten genau zwei *Einheiten* je *Armee*. Der Anforderungsautor hat es an einer Kopie
in `/tmp` mit nur dem Weirdboy gemessen: 12 Tests rot, 471 brechen ab
(Anliegen 10340).

**Kosten.** Bleibt es, darf der Anforderungsautor die Daten zu Weirdboy und Spinne nicht
schreiben; ohne sie fehlen Schritt 5 und 6 des Happy Path ([Plan 10](../plan.md)), Item 4 und 5
können nicht starten.

**Gegenvorschlag.** Die Fixtures finden ihre *Einheit* unabhängig davon, wie viele *Einheiten*
eine *Armee* hat; wie, entscheidest du. Alle Tests bleiben so grün wie vorher.

Wann: Technikphase 10, vorab und parallel zu Item 1; vor den Daten zu Weirdboy und Spinne
(9340, [10180](10180-etappe2LueckenNachPlan10.md)), also vor Item 4 und 5. Hält Plan 10 nicht auf.

**Stellungnahme.** Umgesetzt. `boyz`, `warboss`, `necronWarriors` und `overlord` finden ihre
*Einheit* am Namen (`technik/tests/akzeptanz/conftest.py`, `_einheitMitDemNamen`). Ebenso
unabhängig von der Zahl: QUE-5.2 (`uebergehenTest.py`, Fixture
`schlachtNachDemÜbergehenVonBoyUndWarboss`), AUF-4.3 (`anzeigeTest.py`, erwartet jede *Einheit*
der *Armee*) und AUF-5.12 (`auswahlTest.py`). Beim Aufstellen in der Vorgeschichte
(`handgriffe.py`, `stellenDerEinheit`) stehen *Einheiten* ab der dritten nicht mehr in einer
Reihe vor den anderen, sondern in den Reihen 1 und 2 ab der Mitte der Kante; sonst stünden sie
den Zügen der Boyz und Necron Warriors im Weg (38 Tests rot).
Gemessen an Kopien in `/tmp`: mit den Daten von heute 1230 grün wie vorher; mit Platzhaltern für
Weirdboy und Spinne bricht kein Test mehr ab (vorher 593), 8 bleiben rot, nicht an den Fixtures:
6 an den Beispielen des Vertrags ([10560](10560-vertragsbeispieleMitDritterEinheit.md)), 1
Einheitstest ([10561](10561-einheitentestKatalogDritteEinheit.md)) und BEW-11.3 in
`grenzkreiseTest.py`, das die *Nahkampfreichweiten* der zwei gegnerischen *Einheiten* fest zählt;
die Datei bearbeitet gerade ein anderer Lauf (7641), dort nachzuziehen.
