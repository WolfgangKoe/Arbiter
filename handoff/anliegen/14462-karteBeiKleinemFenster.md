# Die ruhige Karte wird kleiner: Reicht dir das zum Ziehen?

Form: Fragen
Von: Fachkritiker
An: Stakeholder
Runde: 2/3
Status: erledigt

## Runde 1
**Befund.** Damit die *Karte* stehen bleibt, hält Arbiter unter ihr immer Platz für *Gründe*, Knöpfe und *Protokoll* frei. Sie wird dadurch auch dann kleiner, wenn dort nichts steht. 14040 nannte 309 Pixel „so hoch wie vorher“; das war das Mockup. Im Gebauten ist sie heute höher:

Fenster | *Karte* hoch, heute → danach | Kreis eines Boy | kürzester gerader Zug
---|---|---|---
1280×720 | 503 → 309 Pixel | 10,5 → 6,4 Pixel | 0,48 → 0,78 *Zoll*
1100×800 | 583 → 389 Pixel | 12,2 → 8,1 Pixel | 0,41 → 0,62 *Zoll*
1024×768 | 551 → 357 Pixel | 11,5 → 7,5 Pixel | 0,44 → 0,68 *Zoll*
1920×1080 | 863 → 669 Pixel | 15,5 → 14,0 Pixel | 0,32 → 0,36 *Zoll*

Am Bildschirm heißt das: Ein Zug beginnt erst nach 4 Pixeln, wie in ArbiterMap. Zieht ihr bei 1280×720 einen Boy gerade um einen halben *Zoll*, sind das 2,6 Pixel: Er bleibt stehen, Arbiter nimmt es als Klick. Weiter ziehen und zurück geht. Sechs Tests zum Ziehen brachen darum und laufen nun bei 1920×1080; die Regel prüfen sie dort weiter, aber das kleine Fenster belegen sie für diesen kurzen Zug nicht mehr. Das Mockup [que-7](../../domaene/mockups/que-7.html) zum Plan zeigte die kleinere *Karte*, die Folge fürs Ziehen stand nirgends. Kommt Anliegen 14461 durch, werden die *Karten* bei 1100×800 und 1024×768 noch 40 Pixel niedriger. Warum bei dir: Wie klein die *Karte* in deinem Fenster sein darf, kann nur du beurteilen; wir kennen dein Fenster nicht.

**Kosten.** Bleibt es so, entstehen keine Kosten in der Technik. Kurze Züge werden in kleinen Fenstern umständlicher, ein Kreis von 6 Pixeln ist mit dem Finger schwer zu treffen. Mehr Platz kostet Umbau an Mockup und Tests in einem weiteren Zyklus.

**Gegenvorschlag.** Maße lassen, nach Item ruhigeKarte am Bildschirm in deinem Fenster prüfen.

**F1 · Wie soll es bei kleinen Fenstern sein?**
Annahme: Ich prüfe weiter mit A; das Item läuft mit den Maßen des Mockups weiter.
A: Maße bleiben, kurze Züge in kleinen Fenstern gehen nur über „weiter und zurück“; kein Mehraufwand (Anliegen 14040).
B: UX sucht der *Karte* mehr Platz, etwa eine niedrigere Zeile für *Gründe*; Zug und Kreis werden etwas größer, viele *Gründe* rollen dann, ein Anliegen an UX, Tests bleiben (neu).
C: Ein Zug beginnt schon nach 2 Pixeln; der halbe *Zoll* geht auch bei 1280×720, aber ein unruhiger Klick zählt schneller als Zug, das weicht von ArbiterMap ab, kleiner Umbau mit neuen Tests (neu).
Empfehlung: A, das Ziehen bleibt möglich, und du urteilst am gebauten Bildschirm; B oder C kosten erst, wenn du es dort wirklich störend findest.
Antwort: Die Karte soll eigentlich im minimalen Zoom vollständig in das Fenster passen. So wie es jetzt ist, ist die Karte kleiner als das, wie wenn noch weiter hinausgezoomt werden könnte. Das Zoomen ist nicht Teil dieser Etappe, daher wäre die Kartengröße okay. ABER, wenn die Seitenleisten rechts, links und unten nacheinander eingezogen werden, verschiebt sich die Karte immer noch. Meine Erwartung wäre, dass gerade das nicht mehr geschieht.

**Stellungnahme.**

## Runde 2
**Befund.** Deine Antwort lese ich als A für diese Etappe: Die Maße bleiben, bis das Zoomen kommt. Neu ist deine Erwartung, dass die *Karte* auch stehen bleibt, wenn ihr eine *Leiste* *einfahrt*. Das Gebaute tut, was die Anforderung verlangt: [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) nimmt den *Griff* ausdrücklich aus (Anliegen 13980), und die Architektur lässt eine offene *Leiste* der *Karte* Platz nehmen ([O4](../../technik/architektur/frontend.md)). Darum rückt die *Karte* zur Seite, wenn ihr die linke oder rechte *Leiste* *einfahrt*, und wird größer, wenn ihr die untere *einfahrt*. Das Kriterium zu ändern habe ich dem Anforderungsautor in [15100](15100-griffVerschiebtDieKarteNicht.md) geschrieben, für die Domänenphase 11. Offen ist, wie die *Karte* stehen bleibt; das siehst du am Bildschirm, darum F1.

**Kosten.** Beide Wege kosten ein Item in Zyklus 11: Kriterium, Mockup [que-7](../../domaene/mockups/que-7.html), O4, Tests. A kostet mehr als B, weil sich auch Größe und Lage der *Karte* ändern und die Tests dazu mit.

**Gegenvorschlag.** Die *Leisten* liegen über der *Karte* wie in ArbiterMap.

**F1 · Wie soll die Karte stehen bleiben, wenn ihr eine Leiste ein- oder ausfahrt?**
Annahme: Ich prüfe mit A weiter; 15100 nennt beide Wege, der Anforderungsautor arbeitet mit deiner Antwort.
A: Die *Leisten* liegen über der *Karte* wie in ArbiterMap; die *Karte* hat das Fenster für sich und kann größer werden; eine offene *Leiste* verdeckt den Rand des *Spielfelds* hinter ihr, in einem schmalen Fenster auch eine *Aufstellungszone*, dann fahrt ihr sie ein, ohne dass sich etwas verschiebt (ArbiterMap, `ArbiterMap/frontend/templates/map.html:118`).
B: Die *Karte* behält Größe und Platz wie heute, als wären alle *Leisten* offen; eine *eingefahrene* *Leiste* lässt ihren Platz leer, Einfahren gewinnt der *Karte* nichts (Architektur O4).
Empfehlung: A, so kennst du es aus ArbiterMap, Einfahren schafft wirklich Platz, und es passt zu deinem Ziel, dass die *Karte* das Fenster füllt; B ist billiger, wenn dir die Größe von heute genügt.
Antwort: A

**Stellungnahme.**
