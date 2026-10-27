### BEW-2 · Sperren beim Ziehen

Etappe: 2
Zweck: Beim Loslassen in der *Normalen Bewegung* sperrt Arbiter außer nach [QUE-1](../../querschnitt/setzen.md) ein *Modell*, das weiter als *B* zöge oder über eine fremde *Base* (`core_rules.txt:729`, `:745`, Anliegen 02 F5, 03 F8, git, 4280 F3 A).
Am Bildschirm: ein *Modell* ziehen und loslassen ([BEW-1](normaleBewegung.md)).

- BEW-2.1 **Wenn** BEW-1.1 ein *Modell* *setzen* würde, dessen *Distanz* danach länger als sein *B* ist, **dann** *Sperre* ‚weiter als B‘ (`core_rules.txt:745`).
- BEW-2.2 **Wenn** BEW-1.1 ein *Modell* *setzen* würde und seine *Base* auf der geraden Strecke von der vorigen bis einschließlich der neuen *Stelle* eine fremde *Base* nach AUF-29.3 *überdeckt*, **dann** *Sperre* ‚über eine Base‘ (`core_rules.txt:729`).
- BEW-2.3 **Gegeben** eine *Sperre* nach BEW-2.1, 2.2 oder QUE-1, **dann** steht jedes *Modell* danach, wo es vor dem Ziehen war, und Arbiter nennt jeden *Grund* bis zur nächsten Handlung (Anliegen 03 F8).
- BEW-2.4 **Gegeben** die *Ebene* ist die ganze *Einheit*, **dann** sperrt QUE-1.2 in BEW-1.1 kein *Modell* wegen eines anderen derselben *Einheit* an dessen voriger oder neuer *Stelle* (wie AUF-24.2).
