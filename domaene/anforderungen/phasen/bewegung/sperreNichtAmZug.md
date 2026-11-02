### BEW-23 · Sperre für Modelle des anderen Spielers

Zweck: Arbiter sperrt das Ziehen eines *Modells* des *Spielers*, der nicht *am Zug* ist; die *Spieler* können es *gemeinsam übergehen* (Anliegen 9760 F2 B). Ersetzt [BEW-10.1](fremdeModelle.md).
Am Bildschirm: ein *Modell* des anderen *Spielers* ziehen und loslassen, „gemeinsam übergehen“ klicken.

- BEW-23.1 **Gegeben** die *Bewegungsphase*, **wenn** jemand ein *Modell* des *Spielers*, der nicht *am Zug* ist, zieht und loslässt, **dann** steht jedes *Modell*, wo es vor dem Ziehen war, und Arbiter nennt bis zur nächsten Handlung die *Sperre* ‚nicht am Zug‘ und bietet *gemeinsam übergehen* an, ohne Zeile unter dem *Grund* (`core_rules.txt:710`, Anliegen 9760 F2 B, Absicht 3).
- BEW-23.2 **Wenn** die *Spieler* nach BEW-23.1 *gemeinsam übergehen* wählen, **dann** *setzt* Arbiter die gezogenen *Modelle* nach BEW-1.5, als wäre ihr *Spieler* *am Zug* (Anliegen 9760 F2 B).
- BEW-23.3 **Gegeben** die *Bewegungsphase* und eine *Einheit* des *Spielers*, der nicht *am Zug* ist, die nicht in *Kohärenz* ist, **wenn** jemand „Phase beenden“ klickt, **dann** *Sperre* ‚keine Kohärenz‘ statt QUE-10.2 (`core_rules.txt:434`, `:730`, QUE-5.5).
