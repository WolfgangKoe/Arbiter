# Ausgewählte aufgestellte Einheit steht in keiner Armeeliste

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Hält auf (zwei Tests von AUF-30.1), die übrigen Tests von AUF-30 sind grün.
In [aufgestellteEinheitAuswaehlenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/aufgestellteEinheitAuswaehlenTest.py)
lesen `testAuf30_1DerDienstWähltDieAufgestellteEinheitMitDerGanzenEinheitAlsEbene` (über
`ausgewählteEinheitenIm`, das nur die `armeeliste` liest) und
`testAuf30_1DieSeiteKennzeichnetNachDemKlickDieAufgestellteEinheit` (über
`.einheitenKarte.ausgewählt`) die *ausgewählte* *aufgestellte* *Einheit* „Boyz“ an einer
*Einheitenkarte* der *Armeeliste*. Nach dem [Glossar](../../domaene/glossar.md) (*Armeeliste*)
enthält die *Armeeliste* nur nicht *aufgestellte* *Einheiten*; eine *aufgestellte* hat dort
keine Karte, im Spielstand also kein Feld `ausgewählt` an einer *Einheit*.

**Kosten.** Setze ich es so um, steht die *aufgestellte* *Einheit* wieder in der *Armeeliste*
und widerspricht AUF-1.7 und dem Glossar. Ohne Klärung bleiben beide Tests rot.

**Gegenvorschlag.** Die beiden Tests lesen die *Auswahl* an den *Modellen*
(`ausgewählteModelleIm` ist im Dienstest schon geprüft; auf der Seite `.karte .modell.ausgewählt`,
auch schon geprüft) und lassen `ausgewählteEinheitenIm` und `ausgewählteEinheiten` weg. Erledigt,
wenn beide ohne Karte der *Armeeliste* auskommen. Will der Stakeholder die Karte, wäre das ein
Kriterium am Anforderungsautor.

**Stellungnahme.**
