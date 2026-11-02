# Prozessphase endet schon mit dem neuen Plan

Form: Kritik
Von: Organisationsentwickler
An: Regelumsetzer
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Der Planer hat [Plan 10](../plan.md) geschrieben, während P8 aus der
[Retro 9](../retro.md) noch keinen Commit `P8:` hat. Seitdem meldet der Stand die
Domänenphase 10, und die Schreibgrenze sperrt dem Organisationsentwickler seinen Teil von P8
(Texte in `prozess/ablauf/`, `domaene/CLAUDE.md`) mit „nur in der Prozessphase nach
`Freigabe Retro <n>`“. Nach der [Prozessphase](../../prozess/ablauf/prozessphase.md) 5 folgt
die Domänenphase erst, wenn jedes Item seinen Commit `P<k>:` hat; die Retro sah den Plan 10
neben P8 vor („Domänenphase 10 nach 8 Läufen“). Ursache: `standregeln/phasenfolge.py`
`lage` prüft zuerst `handoff/plan.md`; `rollenregeln/regelnNurInProzessphase.py`
(`prozessphaseFreigegeben`) folgt dem. Das hält P8 und damit 7380 auf.

Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): Prozessphase 5 deckt es ab; nur der
Mechanismus weicht ab.

**Kosten.** Regelumsetzer, ein Lauf: wenige Zeilen in `regelnNurInProzessphase.py` und ein
Scheiter-Test. Bis dahin bleibt P8 halb, der Push nach `dev` wartet. Die Entwürfe liegen
bereit, der Organisationsentwickler braucht danach einen kurzen Lauf.

**Gegenvorschlag.** `prozessphaseFreigegeben` gilt auch, solange die zuletzt freigegebene Retro
ein Prozess-Item ohne Commit hat (`phasenfolge.offenesProzessItem` für den Zyklus der Retro),
gleich, ob schon ein neuer Plan liegt. Scheiter-Test: Plan n+1 geschrieben, P<k> ohne Commit,
Write auf `prozess/ablauf/` durch den Organisationsentwickler ist erlaubt; mit Commit gesperrt.

**Stellungnahme.**
