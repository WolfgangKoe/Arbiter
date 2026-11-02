# Dritte Einheit je Armee bricht die Fixtures der Akzeptanztests

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Zum Item [fliegen](../../domaene/items/fliegen.md) schreibe ich die Daten zu
Spinne ([9340](9340-fliegenDerSpinne.md)) und Weirdboy
([MIV-2](../../domaene/anforderungen/missionsvorbereitung/orkPsioniker.md), 10180 Punkt 2):
*Datenblatt*, Zeile in `ausgangslage.yaml`, Zeile in `formation.yaml`. Beide *Armeen* haben
dann drei *Einheiten*. An einer Kopie in `/tmp` mit nur dem Weirdboy: 12 Tests rot, 471
brechen ab, denn die Fixtures `boyz`, `warboss`, `necronWarriors` und `overlord`
(`technik/tests/akzeptanz/conftest.py:157` bis `:177`) erwarten genau zwei *Einheiten* je
*Armee*. Die Daten darf ich also erst schreiben, wenn der Testautor die Fixtures angepasst
hat; der Fortschritt nennt diese Reihenfolge noch nicht. Das Item nennt den Ork-Psioniker,
aber nicht MIV-2.

**Kosten.** Ein Satz im Item, zwei Zeilen im Fortschritt. Bleibt es, sind nach meinen Daten
fast alle Akzeptanztests rot, bis der Testautor nachzieht, oder die Daten fehlen und
Schritt 5 des Happy Path (Spinne, Ork-Psioniker) mit ihnen.

**Gegenvorschlag.** Item fliegen: Umfang mit MIV-2. Fortschritt zum Item, in dieser
Reihenfolge: „Testautor: Fixtures unabhängig von der Zahl der *Einheiten*“, dann
„Anforderungsautor: Daten zu Spinne und Weirdboy (9340, 10180)“, dann Vertrag und Tests wie
bei den übrigen Items.

Wann: vor dem Start des Items fliegen; hält Plan 10 nicht auf.

**Stellungnahme.** Umgesetzt, MIV-2 aber in Item 5 statt in fliegen: Der Weirdboy braucht weder
*Fliegen* noch Item 3 und rückt so nicht mit Item 4 nach Zyklus 11 (10321).
- [zuruecksetzenUndLuecken](../../domaene/items/zuruecksetzenUndLuecken.md): Umfang mit MIV-2,
  Abhängigkeit: Fixtures, dann Daten zum Weirdboy. [fliegen](../../domaene/items/fliegen.md):
  Fixtures, dann *Datenblatt* der Spinne.
- Fortschritt: Die Zeile des Testautors entsteht aus
  [10380](10380-fixturesDritteEinheit.md) (wartet auf die Technikphase 10); die Daten stehen
  schon als „Anforderungsautor: Anliegen 9340“. Für den Weirdboy setze in
  [10180](10180-etappe2LueckenNachPlan10.md) `Wartet auf: Technikphase 10`, wenn du dieses
  abschließt, sonst bist du für 10180 vor den Fixtures dran.
- [Plan 10](../plan.md), Reihenfolge: vor Item 4 und 5, neben Item 1, erst die Fixtures, dann
  die Daten; Item, Schritt 6 und Item 5 nennen MIV-2 und den Weirdboy.
