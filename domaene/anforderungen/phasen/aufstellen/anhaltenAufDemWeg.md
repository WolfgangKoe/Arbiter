### AUF-29 · Anhalten auf dem Weg

Etappe: 3
Zweck: Beim Ziehen hält Arbiter vor einer fremden *Base* an und gleitet an ihr entlang; je Weiterrücken zählt nur, wo es endet (Anliegen 1820, 2090, Vorbild `ArbiterMap/…/model_drag.js:887`, `:964`, `ArbiterMap/…/interaction_map.md:427`).
Am Bildschirm: an fremden *Bases* vorbeiziehen.

- AUF-29.1 **Wenn** beim Ziehen der Zeiger weiterrückt und eine gezeigte *Base* an der *Stelle*, an die AUF-8.2 und 26.1 oder 21.1 und 21.2 sie *setzen* würden, eine fremde *überdecken* würde, die sie an der zuvor gezeigten *Stelle* nicht *überdeckt*, **dann** zeigt die *Karte* die gezogenen *Modelle* gemeinsam so weit auf dem geraden Weg zwischen beiden *Stellen*, wie keine solche *überdeckt* wird.
- AUF-29.2 **Gegeben** AUF-29.1, **wenn** der waagrechte oder der senkrechte Teil dieses Weges nicht null ist und für sich keine solche *überdecken* würde, **dann** zeigt die *Karte* sie statt nach 29.1 um diesen Teil verschoben, bei beiden um den waagrechten (Vorbild `:897`).
- AUF-29.3 **Gegeben** die *Ebene* ist die ganze *Einheit*, **dann** ist fremd in 29.1 jede *Base* einer anderen *Einheit*, sonst jede eines anderen *Modells* (Vorbild `interaction_map.md:401`).
