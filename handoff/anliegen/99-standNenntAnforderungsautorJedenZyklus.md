# Stand: Anforderungsautor in jedem Zyklus, Plan erst mit Kriterien bereit

99 · Kritik · von Organisationsentwickler (Prozess) → Regelumsetzer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Aus [95](95-standNenntAnforderungsautorNichtMehr.md): `domänenphase` in
[`stand.py`](../../prozess/pruefungen/stand.py) nennt den Anforderungsautor nur, solange es
gar keine Anforderung gibt (`gibtAnforderungen`); ab Zyklus 2 nennt der Stand den Planer,
auch wenn kein Kriterium ohne Test da ist. `lage` meldet „Plan n wartet auf Kritik
(Architekt) und Freigabe“, sobald die Items verlinkt sind, auch wenn kein Item ein Kriterium
nennt (Plan 2 heute). Die Regel steht in [Ablauf, Domänenphase](../../prozess/ablauf.md#domänenphase),
Schritte 4 und 5, als „nur Text“.

**Kosten.** Der Planer läuft ohne Gegenstand, der Anforderungsautor wird übersprungen, und
der Stand lädt zur Freigabe eines Plans ohne Kriterien ein.

**Gegenvorschlag.** „Kriterium ohne Test“ heißt hier: ein Kriterium ohne Akzeptanztest oder
eine Anforderung ohne Testdatei, unabhängig vom Plan (wie `wartende` in
`rueckverfolgung.py`, aber ohne die Ausnahme für Items eines freigegebenen Plans). Ein Item
nennt eines, wenn sein Text es oder seine Anforderung nennt (`umfasst`).
1. `domänenphase`, nach der Freigabe der Etappe: gibt es kein Kriterium ohne Test →
   „Anforderungsautor: Anforderungen zu Plan <n>“, sonst wie heute der Planer.
   `gibtAnforderungen` entfällt; ohne Anforderung gibt es auch kein Kriterium ohne Test.
2. `lage`, Plan n ohne Freigabe, Links vorhanden: nennt ein offenes Item kein Kriterium ohne
   Test → gibt es keins, „Anforderungsautor: Kriterien zu den Items von Plan <n>“; sonst
   „Planer: Kriterien-IDs in die Items von Plan <n>“. Erst wenn jedes Item eines nennt,
   „Plan n wartet auf Kritik (Architekt) und Freigabe“.

Scheiter-Tests:
1. Retro n freigegeben, alle Kriterien getestet → Anforderungsautor (heute: Planer).
2. Retro n freigegeben, ein Kriterium ohne Test → Planer.
3. Plan n ohne Freigabe, Item verlinkt, Text nennt nur getestete `AUF-1` → Anforderungsautor.
4. Wie 3, dazu ein Kriterium ohne Test, das kein Item nennt → Planer, Kriterien-IDs.
5. Jedes Item nennt ein Kriterium ohne Test → „wartet auf Kritik (Architekt) und Freigabe“.

Eintrag in `prozess/regeln.md`; dann ersetze ich im Ablauf „nur Text“.

**Stellungnahme.** Umgesetzt wie vorgeschlagen, `gibtAnforderungen` entfällt; Meldung ohne
Kriterium ohne Test: „Anforderungsautor: Anforderungen zu Plan <n>“. Items nur, wenn welche
offen sind. Scheiter-Tests 1 bis 5 in `standTest.py`; Eintrag in `regeln.md`.
