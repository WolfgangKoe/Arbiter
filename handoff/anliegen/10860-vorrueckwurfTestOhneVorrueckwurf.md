# Test zum Vorrückwurf der anderen Einheit nimmt keinen Vorrückwurf

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (ein Test prüft nicht, was er nennt), Kritik am Code (Lesbarkeit) zur
Umsetzung von [8740](8740-vorrueckwurfNurFuerDieEigeneEinheitGeprueft.md) Punkt 1,
uncommittet.
1. `testDerVorrückwurfEinerEinheitGiltNichtFürDasModellEinerAnderenEinheit` in
   [bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py) klickt für
   den *Vorrückwurf* auf `stelleAn(0, 26)`, 6 Zoll vom *Modell* an `stelleAn(0, 20)`. Die
   Grenze der *Bewegung* liegt bei Radius 5 plus *Bewegungsweite* 5 = 10 Zoll; der Klick
   liegt darin, `vorrückwurfNehmen` gibt `False` zurück, die *Einheit* ist nicht
   *vorgerückt*. Probe in `/tmp`: Liefert `_vorrückwurfDes` den Wurf irgendeiner *Einheit*
   (`next(iter(self._vorrückwürfe.values()), 0)`), bleiben alle sechs Tests grün; mit Klick
   auf `stelleAn(0, 33)` (Wurf 3) und `assert` auf das Ergebnis von `vorrückwurfNehmen` wird
   der Test rot, mit dem echten Code grün. Damit ist 8740 Punkt 1 nicht umgesetzt.
2. Der Name verspricht „das *Modell* einer anderen *Einheit*“; `normalesModell` gehört im
   Test keiner *Einheit* an. `vorgerückteModell` liest sich nicht als Deutsch
   (`vorgerücktesModell`).

**Kosten.** Am Bildschirm heute nichts. Bleibt 1, fällt ein Umbau der Suche nach der
*Einheit* weiter keinem Test auf; die zweite Orks-*Einheit* liefe dann mit dem Wurf der
ersten ohne *Sperre* zu weit. Änderung: drei Zeilen im Test.

**Gegenvorschlag.**
1. Klick außerhalb der Grenze der *Bewegung*, etwa `stelleAn(0, 33)`, und die Vorbedingung
   prüfen: `assert bewegungsphase.vorrückwurfNehmen(vorgerückt, vorgerückt.modelle,
   stelleAn(0, 33))`.
2. `normalesModell` in eine zweite *Einheit* (`Einheit("Normal", (normalesModell,))`);
   `vorgerücktesModell`.

**Stellungnahme.** Angenommen. 1: Klick auf `stelleAn(0, 32)` (außerhalb der Grenze der
*Bewegung*) und `assert` auf `vorrückwurfNehmen` in
[bewegungTest.py](../../technik/tests/einheit/domaene/phasen/bewegungTest.py); die Probe mit
`max(...)` in `_vorrückwurfDes` macht den Test rot. 2: `vorgerücktesModell` ist umbenannt.
Eine zweite `Einheit` für `normalesModell` setze ich nicht um: Die Phase kennt nur die
vorgerückten *Einheiten*, die Zugehörigkeit des normalen *Modells* ginge nirgends in den Test
ein, und ein unbenutztes Objekt wäre tote Zeile.
