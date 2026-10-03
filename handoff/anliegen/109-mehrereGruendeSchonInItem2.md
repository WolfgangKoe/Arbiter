# Mehrere Gründe an einer Stelle betreffen schon Item 2

109 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.** Wie [108](108-auf35UndNahkampfreichweiteInPlan2.md): Zwei *Gründe* an einer
*Stelle* gibt es schon in Item 2 (QUE-1.2 und AUF-3.2 zugleich). Dazu kommt AUF-3.6: „der
einzige *Grund*“ setzt voraus, dass eine *Sperre* mehrere nennen kann.

**Kosten, technisch.** Heute trägt eine `Sperre` genau einen `grund`
(`technik/arbiter/domaene/sperre.py`); die AUF-1-Tests lesen ihn an 21 Stellen. Kommt AUF-3.5
erst in Zyklus 3, baut Zyklus 2 weiter auf einem einzigen Grund, und der erste geprüfte Grund
gewinnt, ohne dass das jemand entschieden hat. In Zyklus 3 wird aus `grund` dann eine Menge:
Es ändern sich `Sperre`, alle Sperrtests zu AUF-1 und alle aus Zyklus 2, und zwar gegen
grüne Tests. In Zyklus 2 ist es eine Änderung an einer Schnittstelle, die ohnehin angefasst
wird (Setzen mit *Stelle*).

**Gegenvorschlag.** 108, Punkt 1: AUF-3.5 in Item `sperren-beim-setzen`. Im Plan entfällt
„Plan 2 hängt nicht daran“. Erledigt sich mit 108, wenn du Punkt 1 annimmst.

**Stellungnahme.** Angenommen mit [108](108-auf35UndNahkampfreichweiteInPlan2.md), Punkt 1:
AUF-3.5 steht in Item 2, der Satz „Plan 2 hängt nicht daran“ ist gestrichen. Unter den Kosten
von Item 2 nennt der Plan jetzt auch die Sperre mit mehreren Gründen.
