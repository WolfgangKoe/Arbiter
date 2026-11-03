# Hindernis: Kritik an den Tests zu Item loslassenNebenDerKarte

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Diese Tests sind grün, bevor der Code besteht: testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[maus-nebenDerKarte], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerEins], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-aufDerArmeelisteVonSpielerZwei], testAuf16_8EinModellEinerAufgestelltenEinheitStehtNebenDerKarteLosgelassenWieDavor[finger-nebenDerKarte]. Mache sie rot oder nenne die Stelle, die das Kriterium schon erfüllt. Das hält den Schritt „Kritik an den Tests zu Item loslassenNebenDerKarte“ von Architekt im Fortschritt auf.

Meine Einordnung: Die Stelle steht schon in deiner Stellungnahme zu
Anliegen 11262 (AUF-16.8: `stelleDesZugs` und
`ziehenBeenden` in `frontend/bedienung.js`). Ein Verweis darauf genügt; die Prüfung kennt nur
Hindernisse desselben Schritts, darum dieses zweite ([11500](11500-abhakenKenntNurDenEigenenSchritt.md)).

**Kosten.** Der Schritt bleibt offen, die Phase kommt nicht weiter.

**Gegenvorschlag.** Testautor beseitigt das Hindernis.

**Stellungnahme.** Angenommen, die sechs Tests bleiben grün, weil AUF-16.8 schon erfüllt ist;
die Stelle steht wie in meiner Stellungnahme zu Anliegen 11262: `stelleDesZugs` in
[bedienung.js:31-33](../../technik/frontend/bedienung.js) gibt neben der *Karte* keine
*Stelle*, darauf zeichnet `ziehenBeenden` (Zeilen 123-125) den letzten Spielstand ohne
Anfrage. Die Tests halten fest, dass AUF-28.1 das nicht auf *aufgestellte* *Einheiten*
ausdehnt; scheitern können sie erst mit dem Code dafür.
