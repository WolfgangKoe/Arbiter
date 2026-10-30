# Auswahl in der Schlacht nur an Modellen prüfen, mit Vorbedingung

Form: Kritik
Von: Architekt
An: Testautor
Runde: 1/3
Status: offen
Wartet auf: Technikphase 10

## Runde 1
**Befund.** Wartet auf die nächste Technikphase, aufhaltende Befunde gibt es keine: Die beiden
Dienst-Tests zu BEW-14.1 in
[wurfPerFlaecheTest.py](../../technik/tests/akzeptanz/phasen/bewegung/wurfPerFlaecheTest.py)
prüfen nach 8560 wirklich und halten Es und T1 ein (Aufbau, Handlung, Prüfung, keine Indizes,
Namen). Übrig bleiben zwei Lücken:
1. Dieselbe immer wahre Prüfung wie in 8560 steht noch in
   [abwaehlenTest.py](../../technik/tests/akzeptanz/phasen/bewegung/abwaehlenTest.py),
   `testBew9_1DerDienstNenntNachDemKlickAufDieLeereKarteKeineAuswahl`:
   `ausgewählteEinheitenIm(spielstand) == frozenset()`. In der *Schlacht* ist jede `armeeliste`
   leer (Vertrag [Spielstand](../../technik/architektur/vertrag/schlacht/spielstand.md)), die Zeile
   prüft nichts. Der Test bleibt wirksam, weil die nächste Zeile die Modelle prüft; die tote Zeile
   täuscht aber eine Prüfung vor, und der Name `ausgewählteEinheitenIm` lädt weiter dazu ein.
2. `testBew14_1DerDienstHebtNachDemKlickInDenGrenzkreisAusBew11DieAuswahlAuf` erwartet die leere
   Menge, ohne dass der Test selbst zeigt, dass vor dem Klick etwas *ausgewählt* war. Nimmt
   `wartetAufDenVorrückwurf` die *Auswahl* einmal nicht mehr vor, bleibt er grundlos grün; nur der
   Nachbartest zum Wurf 4 fiele dann auf (Absicht 1, Anliegen 692). Vorbild für die Vorbedingung
   im Aufbau: `testBew9_1EinKlickAufDieLeereKarteHebtAuchEineAuswahlMitEinemModellAlsEbeneAuf`
   (`assert ...modellIstEbene(angeklickt)`), für den Spielstand `testAuf5_9…` in
   [auswahlTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/auswahlTest.py)
   (`assert einheitenDerArmeelisten(spielstand)`).

**Kosten.** Je eine Zeile; keine Änderung am Produktcode, beide Tests bleiben grün.

**Gegenvorschlag.**
1. In `abwaehlenTest.py` die Zeile mit `ausgewählteEinheitenIm` und deren Import streichen.
   `ausgewählteEinheitenIm` gilt dann nur noch in Tests der *Aufstellung*.
2. Im Aufbau von `testBew14_1DerDienstHebtNachDemKlickInDenGrenzkreisAusBew11DieAuswahlAuf`
   nach `wartetAufDenVorrückwurf` die Vorbedingung
   `assert schlachtInDerBewegungsphase.ausgewählt(boyz)` ergänzen.

**Stellungnahme.**
