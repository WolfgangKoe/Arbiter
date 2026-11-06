# Die ruhige Karte wird kleiner: Reicht dir das zum Ziehen?

Form: Fragen
Von: Fachkritiker
An: Stakeholder
Runde: 1/3
Status: offen

## Runde 1
**Befund.** Damit die *Karte* stehen bleibt, hält Arbiter unter ihr immer Platz für *Gründe*, Knöpfe und *Protokoll* frei. Sie wird dadurch auch dann kleiner, wenn dort nichts steht. 14040 nannte 309 Pixel „so hoch wie vorher“; das war das Mockup. Im Gebauten ist sie heute höher:

Fenster | *Karte* hoch, heute → danach | Kreis eines Boy | kürzester gerader Zug
---|---|---|---
1280×720 | 503 → 309 Pixel | 10,5 → 6,4 Pixel | 0,48 → 0,78 *Zoll*
1100×800 | 583 → 389 Pixel | 12,2 → 8,1 Pixel | 0,41 → 0,62 *Zoll*
1024×768 | 551 → 357 Pixel | 11,5 → 7,5 Pixel | 0,44 → 0,68 *Zoll*
1920×1080 | 863 → 669 Pixel | 15,5 → 14,0 Pixel | 0,32 → 0,36 *Zoll*

Am Bildschirm heißt das: Ein Zug beginnt erst nach 4 Pixeln, wie in ArbiterMap. Zieht ihr bei 1280×720 einen Boy gerade um einen halben *Zoll*, sind das 2,6 Pixel: Er bleibt stehen, Arbiter nimmt es als Klick. Weiter ziehen und zurück geht. Sechs Tests zum Ziehen brachen darum und laufen nun bei 1920×1080; die Regel prüfen sie dort weiter, aber das kleine Fenster belegen sie für diesen kurzen Zug nicht mehr. Das Mockup [que-7](../../domaene/mockups/que-7.html) zum Plan zeigte die kleinere *Karte*, die Folge fürs Ziehen stand nirgends. Kommt [14461](14461-knopfzeileUnter1280RolltUndSpringt.md) durch, werden die *Karten* bei 1100×800 und 1024×768 noch 40 Pixel niedriger. Warum bei dir: Wie klein die *Karte* in deinem Fenster sein darf, kann nur du beurteilen; wir kennen dein Fenster nicht.

**Kosten.** Bleibt es so, entstehen keine Kosten in der Technik. Kurze Züge werden in kleinen Fenstern umständlicher, ein Kreis von 6 Pixeln ist mit dem Finger schwer zu treffen. Mehr Platz kostet Umbau an Mockup und Tests in einem weiteren Zyklus.

**Gegenvorschlag.** Maße lassen, nach Item ruhigeKarte am Bildschirm in deinem Fenster prüfen.

**F1 · Wie soll es bei kleinen Fenstern sein?**
Annahme: Ich prüfe weiter mit A; das Item läuft mit den Maßen des Mockups weiter.
A: Maße bleiben, kurze Züge in kleinen Fenstern gehen nur über „weiter und zurück“; kein Mehraufwand (Anliegen 14040).
B: UX sucht der *Karte* mehr Platz, etwa eine niedrigere Zeile für *Gründe*; Zug und Kreis werden etwas größer, viele *Gründe* rollen dann, ein Anliegen an UX, Tests bleiben (neu).
C: Ein Zug beginnt schon nach 2 Pixeln; der halbe *Zoll* geht auch bei 1280×720, aber ein unruhiger Klick zählt schneller als Zug, das weicht von ArbiterMap ab, kleiner Umbau mit neuen Tests (neu).
Empfehlung: A, das Ziehen bleibt möglich, und du urteilst am gebauten Bildschirm; B oder C kosten erst, wenn du es dort wirklich störend findest.
Antwort: .

**Stellungnahme.**
