# Tests mit ‚über eine Base‘ als Mittel

Form: Kritik
Von: Testautor
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Nach [9272](9272-testsOhneKriteriumNach8840.md) sind die Tests zu BEW-2, BEW-8.1,
8.2 und AUF-12.6 fort. Weitere Tests haben noch ihr Kriterium, erzeugen ihre *Sperre* aber mit
‚über eine Base‘, das seit [8840](8840-baseNichtUeberdeckenAnhaltenStattSperre.md) keine
Anforderung mehr nennt, oder übergehen ‚Base überdeckt‘, was QUE-1.4 verbietet:
- QUE-5.1 bis 5.4 in `technik/tests/akzeptanz/querschnitt/uebergehenTest.py` (Fixture
  `zugÜberEineBase`, Handgriffe `boyÜberDenWarbossÜbergehen` und `warbossÜberDieBoyzÜbergehen`
  in `technik/tests/akzeptanz/schlacht.py`);
- QUE-6, Fixtures `seiteMitProtokoll` und `seiteZumTippen` in
  `technik/tests/akzeptanz/querschnitt/leistenTest.py`;
- `testBew1_7DerDienstAntwortetBeiEinerSperreWieBeimLoslassenMitDemGrundUndDemStandWieDavor` in
  `technik/tests/akzeptanz/phasen/bewegung/normaleBewegungTest.py`;
- die Beispiele `uebergehbar.json` und `protokoll.json` unter `technik/architektur/vertrag/`
  (Architekt).

**Kosten.** Heute grün gegen den alten Code. Entfernt der Implementierer ‚über eine Base‘
nach BEW-17, werden sie rot, ohne dass ein Kriterium verletzt ist. Ein neues Mittel
(Übergehen eines Anhaltens nach BEW-8.3 bis 8.5) hängt an der Schnittstelle dieses Items.

**Gegenvorschlag.** Das Item aus [9271](9271-anhaltenVorFremdenBasesPlanen.md) umfasst auch
den Umbau dieser Tests; ich schreibe sie mit den Tests zu BEW-8.3 bis 8.5 um. Etwa ein
Drittel Item mehr.

**Stellungnahme.**
Angenommen, umgesetzt im Item [anhaltenUebergehen](../../domaene/items/anhaltenUebergehen.md):
Es baut die genannten Tests auf das Übergehen eines Anhaltens um und kommt vor
[anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md), das ‚über eine Base‘ entfernt;
so werden sie nicht rot ohne verletztes Kriterium. Die Beispiele unter
`technik/architektur/vertrag/` gehören zum Vertrag dieses Items (Architekt). Die Folge hängt an
[9271](9271-anhaltenVorFremdenBasesPlanen.md) F1; mit A plane ich neu und schreibe dir hier.
