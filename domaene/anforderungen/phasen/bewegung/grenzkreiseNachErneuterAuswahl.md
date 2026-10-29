### BEW-15 · Grenzkreise nach erneuter Auswahl

Etappe: 2
Zweck: Auch nach Abwählen und erneuter *Auswahl* zeigt die *Karte* die *Grenzkreise* von den *Stellen* zu Beginn der *Bewegungsphase* aus (`core_rules.txt:745`, wie BEW-1.6).
Am Bildschirm: eine *Einheit* ziehen, abwählen ([BEW-9](abwaehlen.md)), eine andere ziehen, die erste wieder *auswählen*.

- BEW-15.1 **Gegeben** die *Bewegungsphase* und eine gezogene *Einheit* des *Spielers* *am Zug*, die nach BEW-9.1 nicht *ausgewählt* war, während eine andere gezogen wurde, **wenn** jemand eines ihrer *Modelle* anklickt (AUF-20.6), **dann** zeigt die *Karte* die *Einhüllende* aus BEW-11.5 um die *Stellen* ihrer *Modelle* zu Beginn der *Bewegungsphase*, nicht um die jetzigen (`core_rules.txt:745`).
- BEW-15.2 **Gegeben** 15.1, **wenn** jemand danach eines ihrer *Modelle* anklickt (BEW-7.1), **dann** zeigt die *Karte* um dieses den *Grenzkreis* aus BEW-11.1 um seine *Stelle* zu Beginn der *Bewegungsphase* (`core_rules.txt:745`).
- BEW-15.3 **Gegeben** 15.1 oder 15.2 und die *Einheit* ist *vorgerückt*, **dann** zeigt die *Karte* dazu nur den aus BEW-13.2 für ihren *Vorrückwurf* (`core_rules.txt:754`).
