# Tests zu den Grenzkreisen: Einhüllende am Bildschirm, Modell im Ring

Form: Kritik
Von: Fachkritiker
An: Testautor
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Kritik an den Tests zu Item grenzkreise. Wartet nach
[Kritik](../../prozess/ablauf/kritik.md): Lücken abseits des Happy Path, Namen.

1. BEW-11.5 und das [Glossar](../../domaene/glossar.md) verlangen, dass die *Karte* die
   *Einhüllende* „statt dieser *Grenzkreise*“ zeigt. Die Tests der Seite zählen nur die
   `g.grenze` und ihre Klassen (wie der [Vertrag](../../technik/architektur/vertrag/bewegung/grenzkreise.md)
   es vorgibt); zehn einzelne Kreise in einer `g.grenze` bestünden sie auch.
2. BEW-14.1 gilt nur, „wo kein *Modell* ist“. Mit einem *Modell* als *Ebene* stehen die
   übrigen *Modelle* derselben *Einheit* in den Ringen 1 bis 6. Kein Test klickt, während sie
   auf den *Vorrückwurf* wartet, ein solches an und stellt fest, dass kein Wurf gilt.
3. „Ring“ und „Grenze“ stehen in Namen von Tests und Hilfen (`stelleImRing`,
   `…ZwischenRingDreiUndVier…`, `…KeineGrenze`), nicht im Glossar; die Anforderungen sagen
   *Grenzkreis* und *Einhüllende*. Keine Prüfung ist rot.

**Kosten.** Am Bildschirm nichts, solange die Seite richtig zeichnet; der *Stakeholder* sieht
1 im Review. Ohne Test kann 1 oder 2 später unbemerkt brechen. Je ein Test.

**Gegenvorschlag.** 1: prüfen, dass jede `g.grenze` ihre `grenzeMaske` nutzt (Attribut
`mask`), mit dem Architekten abgestimmt. 2: ein Test zu BEW-14.1 mit einem *Modell* als
*Ebene*, Klick auf ein anderes *Modell* der *Einheit* im Ring: kein *Vorrückwurf*, die
*Einheit* wartet weiter. 3: Namen aus Anforderung und Glossar, oder „Ring“ über den
Anforderungsautor ins Glossar (der Plan nutzt es schon).

**Stellungnahme.** Angenommen, alle drei umgesetzt; die Tests sind grün, der Code kann es schon.
1. Neu `testBew11_5DieSeiteZeigtJedeEinhüllendeDurchIhreMaskeAusDenselbenGrenzkreisen` in
   [grenzkreiseTest.py](../../technik/tests/akzeptanz/phasen/bewegung/grenzkreiseTest.py) und
   `testBew13_1DieSeiteZeigtJedeDerSiebenEinhüllendenDurchIhreEigeneMaske` in
   [grenzkreiseBeimVorrueckenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/grenzkreiseBeimVorrueckenTest.py):
   Jede `g.grenze` verweist über `mask` auf eine `mask.grenzeMaske` mit denselben Kreisen, und
   jede hat so viele Kreise, wie ihre *Einheit* *Modelle* hat. Hilfe
   `kreiseDerGrenzenUndIhrerMasken` in [bildschirm.py](../../technik/tests/akzeptanz/bildschirm.py).
   Das hält sich an den Abschnitt Seite des
   [Vertrags](../../technik/architektur/vertrag/bewegung/grenzkreise.md) (`grenzeMaske` je Eintrag);
   der Architekt sieht es bei seiner Kritik an den Tests.
2. Neu in [wurfPerFlaecheTest.py](../../technik/tests/akzeptanz/phasen/bewegung/wurfPerFlaecheTest.py):
   `testBew14_1EinKlickAufEinModellImGrenzkreisEinesWurfsWähltKeinenWurf` (Domäne) und
   `testBew14_1AmBildschirmWähltEinKlickAufEinModellImGrenzkreisEinesWurfsKeinenWurf` (Maus und
   Finger). Der letzte Boy ist *Ebene*, die *Einheit* wartet; Klick auf den dritten Boy, der nur im
   *Grenzkreis* für 4 steht: kein *Vorrückwurf*, nicht *vorgerückt*, sie wartet weiter, am
   Bildschirm bleiben sechs `wählbar`.
3. „Ring“ ist aus allen Namen heraus: `stelleNurImGrenzkreisDesWurfs`,
   `stelleAufDemGrenzkreisDesWurfs`, `außerhalbDerSechsGrenzkreise`, Tests `…NurImGrenzkreisFürVier…`,
   `…AnJederAnderenStelle…` (Wortlaut von BEW-14.1). Tests, die sagen, was die *Karte* zeigt,
   heißen jetzt nach *Grenzkreis* und *Einhüllende*: `…KeinenGrenzkreis`, `…SechsWählbarenEinhüllenden`,
   `…EinhüllendeDesWurfs…` (BEW-5.2, 11, 12.2, 13). „Grenze“ bleibt nur in Hilfen, die die
   Abfrage `grenzen` aus V20 und V21 des Vertrags lesen (`grenzenDerEinheit`, `GrenzeDerKarte`):
   Das ist der Name der Schnittstelle, nicht der Fachsprache.
