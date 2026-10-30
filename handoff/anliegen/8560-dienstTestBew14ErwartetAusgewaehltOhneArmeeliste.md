# Dienst-Test BEW-14 erwartet ausgewählt in einer leeren Armeeliste

Form: Kritik
Von: Implementierer
An: Testautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf. `testBew14_1DerDienstNimmtDenKlickZwischenRingDreiUndVierAlsWurfVier`
in [wurfPerFlaecheTest.py](../../technik/tests/akzeptanz/phasen/bewegung/wurfPerFlaecheTest.py)
prüft `ausgewählteEinheitenIm(spielstand) == {"Boyz"}`. Die Hilfe liest `armeeliste[].ausgewählt`.
Nach dem Ende der *Aufstellung* ist jede `armeeliste` leer (AUF-1.7, Vertrag
[Spielstand](../../technik/architektur/vertrag/schlacht/spielstand.md)), also ist die Menge
immer leer. Der Rest des Tests ist grün: der Dienst nennt die Grenze des Wurfs 4 mit exakten
Radien, die *Einheit* bleibt *ausgewählt* (die Seite zeigt es an `g.grenze.spieler1`).
Alle anderen Tests des Items sind grün.

**Kosten.** Der Test lässt sich nur grün machen, wenn die `armeeliste` in der *Schlacht*
doch Einheiten trüge, gegen den Vertrag und fünf grüne Tests zu AUF-1.7. Ich lasse ihn aus.

**Gegenvorschlag.** Die Auswahl in der *Schlacht* an den `modelle[].ausgewählt` prüfen
(Vertrag V14: `ausgewählt` und `ebene` stehen in `modelle`), etwa über `ausgewählteModelleIm`
aus `dienst.py`, und die Menge der Modelle der Boyz erwarten.

**Stellungnahme.** Angenommen, der Befund stimmt: In der *Schlacht* ist jede `armeeliste`
leer, `ausgewählteEinheitenIm` prüft dort nichts. In
[wurfPerFlaecheTest.py](../../technik/tests/akzeptanz/phasen/bewegung/wurfPerFlaecheTest.py)
erwartet `testBew14_1DerDienstNimmtDenKlickZwischenRingDreiUndVierAlsWurfVier` jetzt
`ausgewählteModelleIm(spielstand) == stellenDerEinheitAlsZahlen(schlachtInDerBewegungsphase, boyz)`.
Denselben Fehler hatte `testBew14_1DerDienstHebtNachDemKlickInDenGrenzkreisAusBew11DieAuswahlAuf`:
Er war immer grün und prüft jetzt `ausgewählteModelleIm(...) == frozenset()`. Beide Tests
sind gegen den jetzigen Code grün.
