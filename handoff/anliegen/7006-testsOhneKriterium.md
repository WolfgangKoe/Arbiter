# Tests zu MIV-1.3 ohne Kriterium

Form: Kritik
Von: Anforderungsautor
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Nach [Anliegen 4881](4881-datenblaetterImGlossarUndInDenDaten.md) ersetzt
[MIV-1.5](../../domaene/anforderungen/missionsvorbereitung/ausgangslage.md) das Kriterium
MIV-1.3 (neue Kennung, weil MIV-1.3 Tests hat). Die drei Tests `testMiv1_3…` in
`technik/tests/akzeptanz/missionsvorbereitung/ausgangslageTest.py` gehören zu keinem Kriterium
mehr; der Stand ist dadurch rot (`kriterienregeln/rueckverfolgung.py`: „Test zu MIV-1.3, das
… fehlt“), und mit ihm jeder Commit.

**Kosten.** Bis sie fort sind, kann niemand committen, auch nicht die Freigabe von Plan 9.

**Gegenvorschlag.** Jetzt die drei Tests zu MIV-1.3 löschen. Tests zu MIV-1.5 kommen mit
Item 1 von [Plan 9](../plan.md); bis zur Freigabe nennt der Stand MIV-1.5 nur als wartend.

Wann: jetzt, Domänenphase 9.

**Stellungnahme.** Angenommen und umgesetzt: Die drei Tests `testMiv1_3…` und ihr Handgriff
`durchmesserDerArmeen` sind aus
[ausgangslageTest.py](../../technik/tests/akzeptanz/missionsvorbereitung/ausgangslageTest.py)
entfernt; `rueckverfolgungTest.py` ist grün. Tests zu MIV-1.5 schreibe ich mit Item 1 von
Plan 9.
