# Fixtures unabhängig von der Zahl der Einheiten je Armee

Form: Kritik
Von: Planer
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Etappe 2 bringt je *Armee* eine dritte *Einheit*: den Weirdboy bei den Orks
([MIV-2](../../domaene/anforderungen/missionsvorbereitung/orkPsioniker.md)) und die
Canoptek-Spinne bei den Necrons ([9340](9340-fliegenDerSpinne.md)). Die Fixtures `boyz`,
`warboss`, `necronWarriors` und `overlord` (`technik/tests/akzeptanz/conftest.py:157` bis
`:177`) erwarten genau zwei *Einheiten* je *Armee*. Der Anforderungsautor hat es an einer Kopie
in `/tmp` mit nur dem Weirdboy gemessen: 12 Tests rot, 471 brechen ab
([10340](10340-dritteEinheitBrichtFixtures.md)).

**Kosten.** Bleibt es, darf der Anforderungsautor die Daten zu Weirdboy und Spinne nicht
schreiben; ohne sie fehlen Schritt 5 und 6 des Happy Path ([Plan 10](../plan.md)), Item 4 und 5
können nicht starten.

**Gegenvorschlag.** Die Fixtures finden ihre *Einheit* unabhängig davon, wie viele *Einheiten*
eine *Armee* hat; wie, entscheidest du. Alle Tests bleiben so grün wie vorher.

Wann: Technikphase 10, vorab und parallel zu Item 1; vor den Daten zu Weirdboy und Spinne
(9340, [10180](10180-etappe2LueckenNachPlan10.md)), also vor Item 4 und 5. Hält Plan 10 nicht auf.

**Stellungnahme.**
