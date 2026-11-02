# Dritte Einheit je Armee bricht die Fixtures der Akzeptanztests

Form: Kritik
Von: Anforderungsautor
An: Planer
Runde: 1/3
Status: offen

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

**Stellungnahme.**
