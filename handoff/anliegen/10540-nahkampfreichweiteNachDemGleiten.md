# Nahkampfreichweite nach dem Gleiten

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Erprobung zu Item [anhaltenAufDemWeg](../../domaene/items/anhaltenAufDemWeg.md)
(10321): Nach einem Gleiten nach [BEW-17.1](../../domaene/anforderungen/phasen/bewegung/anhaltenVorFremdenBases.md)
liegt die zuvor gezeigte *Stelle* neben der geraden Strecke, auf der BEW-3.1 und 6.2 messen
(von der *Stelle* vor dem Ziehen zum Zeiger). Würde das nächste Weiterrücken keine fremde
*Base* *überdecken*, zeigt die *Karte* das *Modell* nach BEW-1.7 dort, ohne dass jemand prüft,
ob es auf dem Weg von der zuvor gezeigten *Stelle* dorthin in *Nahkampfreichweite* kam.
Beispiel: Ein Boy gleitet links an einem Krieger vorbei, der Zeiger springt nach rechts
oben; die gerade Strecke ab der *Stelle* vor dem Ziehen bleibt außerhalb der
*Nahkampfreichweite* eines zweiten Kriegers, der Weg ab der gezeigten *Stelle* führt
hindurch. Ungeregelt ist also, ob
BEW-6.2 auf dem gezeigten Weg gilt oder nur auf der Strecke ab der *Stelle* vor dem Ziehen
(`core_rules.txt:745`: „at any point during the move“).

**Kosten.** Ohne Regel entscheidet der Vertrag; nach dem Regeltext hielte Arbiter dann
nicht an, wo er müsste. Technisch ist beides gleich teuer (ein Aufruf mehr je Weiterrücken).

**Gegenvorschlag.** In BEW-17.1 oder BEW-6.2: Hat die *Karte* das *Modell* in diesem Zug nach
BEW-17.1 gezeigt, hält 6.2 auch auf der Strecke von der zuvor gezeigten *Stelle* an.

Wann: vor dem Vertrag zu Item anhaltenAufDemWeg; sonst schreibe ich die Strecke ab der
*Stelle* vor dem Ziehen in den Vertrag (heutiger Wortlaut).
