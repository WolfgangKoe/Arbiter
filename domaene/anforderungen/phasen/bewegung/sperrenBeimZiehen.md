### BEW-2 · Sperren beim Ziehen

Etappe: 2
Zweck: Beim Loslassen im *Normal Move* sperrt Arbiter außer nach [QUE-1](../../querschnitt/setzen.md) ein *Modell*, das weiter als *M* zöge oder über eine fremde *Base* (`core_rules.txt:729`, `:745`); jedes Ziehen gilt als gerade Strecke (Anliegen 02 F5, 03 F8, git).
Am Bildschirm: ein *Modell* ziehen und loslassen ([BEW-1](normalMove.md)).

- BEW-2.1 **Wenn** BEW-1.1 ein *Modell* *setzen* würde, dessen *Weg* danach länger als sein *M* ist, **dann** *Sperre* ‚weiter als M‘ (`core_rules.txt:745`).
- BEW-2.2 **Wenn** BEW-1.1 ein *Modell* *setzen* würde und seine *Base* auf der geraden Strecke von der vorigen zur neuen *Stelle* eine fremde *Base* nach AUF-29.3 *überdeckt*, **dann** *Sperre* ‚über eine Base‘ (`core_rules.txt:729`).
- BEW-2.3 **Gegeben** eine *Sperre* nach BEW-2.1, 2.2 oder QUE-1, **dann** steht jedes *Modell* danach, wo es vor dem Ziehen war, und Arbiter nennt jeden *Grund* bis zur nächsten Handlung (Anliegen 03 F8).
