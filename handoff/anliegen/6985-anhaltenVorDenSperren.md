# Anhalten vor der Nahkampfreichweite oder Sperre beim Loslassen auf einem Gegner

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Im Happy Path von [BEW-6](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md)
(„an … einen Gegner ziehen“) sperrt nach dem Wortlaut eine *Sperre*, wo der Stakeholder
Anhalten verlangt ([Anliegen 6400](6400-anhaltenVorDerNahkampfreichweite.md): „an der Grenze …
stehen bleiben“, nicht „auf die ursprüngliche Position zurückgesetzt“).
Lässt jemand ein *Modell* auf oder hinter einem *Modell* des anderen *Spielers* los, prüfen
[BEW-1.5](../../domaene/anforderungen/phasen/bewegung/normaleBewegung.md) („es sperren nur
QUE-1 und BEW-2“) und [BEW-2.5](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md)
die *Stelle*, an die BEW-1.5 *setzen* würde. BEW-1.5 nimmt davon nur BEW-3 aus, nicht BEW-6.
Damit greifen dort ‚Base überdeckt‘ (QUE-1.2) und ‚über eine Base‘ (BEW-2.5), und nach BEW-2.6
springt das *Modell* zurück. BEW-6.2 ersetzt nur QUE-1.3. Welche Regel zuerst greift, sagt
kein Kriterium.
Regeltext und Vorbild halten an: „no model can be moved within Engagement Range of enemy
models“ (`core_rules.txt:745`). ArbiterMap hält den Zug „an der ersten aktiven Sperrscheibe —
Base eines fremden Modells oder Nahkampfzone (1″) eines Gegners“ an
(`ArbiterMap/docs/spec/interaction_map.md:402`).
Weil die *Nahkampfreichweite* 1″ vor der *Base* des Gegners beginnt, *überdeckt* ein vor ihr
angehaltenes *Modell* sie nie.

**Kosten.** Ohne Klärung wählt der Testautor eine Lesart. Liest er wörtlich, prüfen die Tests
den Rücksprung, den der Stakeholder in 6400 abgelehnt hat. Die Klärung kostet ein Kriterium
und einen Test; BEW-1.5 und BEW-2.5 bleiben, wie sie sind.

**Gegenvorschlag.** Ein neues Kriterium in BEW-6, etwa BEW-6.5: „**Wenn** BEW-3.1, 6.1 oder 6.2 nach
6.3 anhält, **dann** prüfen QUE-1 und BEW-2.5 die *Stelle*, an der Arbiter anhält, und die
Strecke bis dorthin, und BEW-8.2 *setzt* dorthin (`core_rules.txt:745`, Vorbild
`interaction_map.md:402`).“ Eine *Base* der eigenen Armee auf der Strecke bis zur
angehaltenen *Stelle* sperrt dann weiter ‚über eine Base‘.

**Stellungnahme.** Angenommen, umgesetzt in [BEW-2.8](../../domaene/anforderungen/phasen/bewegung/sperrenBeimZiehen.md)
statt BEW-6.5, weil BEW-6 sonst über 1.200 Zeichen käme: Hält BEW-6 an, prüfen QUE-1 und
BEW-2.5 die angehaltene *Stelle* und die Strecke bis dorthin, BEW-8.2 *setzt* dorthin.
Dazu [BEW-6.2](../../domaene/anforderungen/phasen/bewegung/anhaltenVorDerGrenze.md): Es hält an,
sobald ein *Modell* auf der Strecke nach BEW-3.1 in *Nahkampfreichweite* käme, nicht erst an
der Zielstelle. Sonst sperrte ‚über eine Base‘ weiter, wenn jemand hinter einem Gegner
loslässt, und ein *Modell* zöge durch die *Nahkampfreichweite* (`core_rules.txt:745`, Vorbild
`interaction_map.md:402`). BEW-6.1 verweist für das Anhalten auf BEW-3.1, inhaltlich gleich;
BEW-6 hat noch keinen Test.
