# Hindernis: Kritik an den Tests zu Item fliegen

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testMiv3_1DieArmeeDerNecronsHatEineEinheitCanoptekSpyderAusEinemModell, testBew17_1DerDienstHältDasModellAufDerStreckeVorDerFremdenBaseAn, testBew17_1AmFreienZielZeigtDerDienstDasZielAuchWennDerWegÜberEineBaseFührt, testBew17_1StehtDerPunktHinterEinerBaseAnDerBewegungsweiteHältDerDienstDasModellVorIhrAn[ohneAbfrageDavor], testBew17_1StehtDerPunktHinterEinerBaseAnDerBewegungsweiteHältDerDienstDasModellVorIhrAn[nachEinerAbfrageDieVorIhrAnhielt], testBew17_1EineBaseHinterDerBewegungsweiteLenktDasModellNichtAb, testBew17_1DerDienstHältAufDerStreckeAbDerZuvorGezeigtenStelleAn, testBew17_1DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[beideTeileFreiWaagrecht], testBew17_1DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurSenkrechtFrei], testBew17_1DerDienstZeigtDasModellUmDenFreienTeilDesWegesVerschoben[nurWaagrechtFrei], testBew17_1HältDieBewegungsweiteAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke, testBew17_1HältDieSpielfeldkanteAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke, testBew17_1HältDieNahkampfreichweiteAufDemFreienTeilAnZeigtDerDienstDasModellAufDerStrecke, testBew17_1AlleinGezogenHältDerDienstVorDemModellDerselbenEinheitAn, testBew17_1IstDieGanzeEinheitEbeneHältDerDienstAlleIhreModelleGemeinsamAn. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item fliegen“ von Architekt im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis. Nach meiner Prüfung genügt, die Stellen
zu nennen: MIV-3.1 erfüllt schon `domaene/daten/ausgangslage.yaml` (`Canoptek Spyder: 1`);
BEW-17.1 gehört nicht zum Umfang des Items, sondern zur Zeile „Abhängigkeit“, sein Code steht
seit dem Item anhaltenAufDemWeg. Dass die Prüfung diese Zeile mitnimmt:
[13102](13102-testsRotNimmtKriterienDerAbhaengigkeit.md).

**Stellungnahme.** Angenommen, die Stellen:
- `testMiv3_1DieArmeeDerNecronsHatEineEinheitCanoptekSpyderAusEinemModell`: MIV-3.1 erfüllt
  schon [ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml), Zeilen 33 bis 35
  (`Canoptek Spyder: 1`), committet vor den Tests (Daten zu MIV-3, Plan Schritt 5).
- Die vierzehn Tests zu BEW-17.1 in
  [anhaltenVorFremdenBasesTest.py](../../technik/tests/akzeptanz/phasen/bewegung/anhaltenVorFremdenBasesTest.py):
  BEW-17.1 steht im [Item](../../domaene/items/fliegen.md) nur unter „Abhängigkeit“, nicht im
  Umfang; sein Code kam mit Item anhaltenAufDemWeg (Commit 7c8d127 „Item anhaltenAufDemWeg
  gelöscht“), `technik/arbiter/domaene/phasen/aufstellen/anhaltenAufDemWeg.py`. Diese Tests
  habe ich für fliegen weder geschrieben noch geändert.
