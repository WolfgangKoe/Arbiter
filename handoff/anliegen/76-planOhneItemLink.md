# Stand: Plan ohne Item-Link überspringt die Abnahme

76 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · angenommen

## Runde 1
**Befund.** [`stand.py`](../../prozess/pruefungen/stand.py) (`offeneItems`) erkennt ein Item
nur am Link `](../domaene/items/<id>.md)` in `handoff/plan.md`; ohne Link gilt der Plan als
ohne offenes Item. Plan 1 nennt sein Item als `*Reihenfolge der Aufstellung*`, ohne Link.
Mit dieser Form hätte der Stand nach dem Review die Prozessphase gemeldet, die Abnahme
übersprungen: genau der Fehler aus Zyklus 1, den der Stand jetzt verhindern soll. Die Form
steht seit heute in [`ablauf.md`](../../prozess/ablauf.md#domänenphase), Schritt 5, und in
der Definition des Planers, als „nur Text“.

**Kosten.** Ein einziger Plan ohne Link schaltet die Prüfung still ab; niemand merkt es, bis
die Abnahme fehlt.

**Gegenvorschlag.** Der Stand meldet einen Plan, der Items nennt, aber keinen Link auf
`domaene/items/` enthält: Solange `Freigabe Plan <n>` fehlt, statt „Plan n wartet auf Kritik
(Architekt) und Freigabe“ den Schritt „Planer: Items von Plan n als Link auf
`domaene/items/`“. Ob ein Link auf ein schon gelöschtes Item zählt: ja, es geht um die Form,
nicht um die Datei. Scheiter-Tests:
1. Plan n ohne Freigabe, kein Link auf `domaene/items/` → Stand nennt den Planer und den Link.
2. Plan n ohne Freigabe, ein Link → „Plan n wartet auf Kritik (Architekt) und Freigabe“.

Eintrag in `prozess/regeln.md`; dann ersetze ich in `ablauf.md`, Domänenphase Schritt 5,
„nur Text“.

**Stellungnahme.** Umgesetzt: `plan.py` (`itemsOhneLink`) und `stand.py`: Plan mit Abschnitt `## Item(s)` ohne Link auf `domaene/items/` und ohne Freigabe nennt „Planer: Items von Plan n als Link auf domaene/items/“. Scheiter-Tests 1 und 2 in `standTest.py`; Eintrag in `prozess/regeln.md`.
