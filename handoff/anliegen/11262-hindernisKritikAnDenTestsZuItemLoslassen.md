# Hindernis: Kritik an den Tests zu Item loslassenNebenDerKarte

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-nebenDerKarte], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-nebenDerKarte], testAuf28_1DerDienstSetztAmPunktDerLetztenStelleWieDasBeispielImVertrag. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item loslassenNebenDerKarte“ von Fachkritiker im Fortschritt auf.

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

Fachlich sehe ich keinen weiteren Befund an den Tests des Items: Jeder trifft sein Kriterium,
die roten scheitern am fehlenden Senden neben der *Karte* (Seite) und am Setzen eines nicht
*gesetzten* *Modells* (AUF-16.7, Domäne). Mein Vorschlag zur Stellungnahme, ohne Änderung an
den Tests: AUF-16.8 erfüllt heute [bedienung.js:123-125](../../technik/frontend/bedienung.js)
(neben der *Karte* keine *Stelle*, also zurück wie vor dem Ziehen); die sechs Tests halten fest,
dass AUF-28.1 das nicht auf *aufgestellte* *Einheiten* ausdehnt, und können erst mit dem Code
dafür scheitern. Den Dienst-Test zu AUF-28.1 erfüllt der vorhandene `PUT …/stelle` (AUF-8.2);
das Kriterium selbst prüfen die Tests an der Seite. Nennst du beide Stellen, ist das Hindernis
für mich beseitigt.

**Stellungnahme.**
