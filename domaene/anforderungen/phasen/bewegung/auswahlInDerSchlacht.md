### BEW-7 · Auswahl in der Schlacht

Etappe: 2
Zweck: In der *Schlacht* macht ein Klick ein *Modell* zur *Ebene* wie in der *Aufstellung* (Anliegen 5180 F3 B, 6420, Vorbild `ArbiterMap/frontend/static/js/model_selection.js:336`).
Am Bildschirm: ein *Modell* der *ausgewählten* *Einheit* anklicken und ziehen.

- BEW-7.1 **Gegeben** die *Schlacht* und eine *ausgewählte* *Einheit*, **wenn** jemand eines ihrer *Modelle* anklickt, das nicht ihre *Ebene* ist, **dann** ist ihre *Ebene* dieses *Modell* (wie AUF-25.1, Anliegen 5180 F3 B).
- BEW-7.2 **Gegeben** die *Schlacht* und eine *ausgewählte* *Einheit*, deren *Ebene* ein *Modell* ist, **wenn** jemand dieses anklickt, **dann** ist ihre *Ebene* die ganze *Einheit* (wie AUF-25.2).
- BEW-7.3 **Gegeben** die *Bewegungsphase* und eine *ausgewählte* *Einheit*, deren *Ebene* ein *Modell* ist, **wenn** jemand es zieht und loslässt, **dann** *setzt* BEW-1.5 nur dieses, jedes andere steht wie davor (Anliegen 6420).
- BEW-7.4 **Gegeben** die *Schlacht* und eine *ausgewählte* *Einheit*, deren *Ebene* ein *Modell* ist, **dann** kennzeichnet die *Karte* nur dieses (wie AUF-25.4).