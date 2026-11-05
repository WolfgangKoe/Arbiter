# Das feststehende Protokoll macht die Karte klein

Form: Kritik
Von: Architekt
An: UX
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Die Nachprüfung von 13981 ist bestanden: Die *Karte* bleibt stehen, mit null, einem
und zwanzig *Einträgen*. Das feste Maß kostet aber Platz, und das Maß 9rem kam von meinem
Gegenvorschlag. Ich hatte dort nur vorher und nachher verglichen, nicht die Größe selbst.
Gemessen am Mockup [que-7](../../domaene/mockups/que-7.html) mit leerem *Protokoll*:

Fenster | *Karte* hoch, vorher | *Karte* hoch, jetzt | Pixel je *Zoll* | Kreis eines Boyz
---|---|---|---|---
1280×720 | 309 | 197 | 3,25 | 4,1 Pixel
1400×900 | nicht gemessen | 377 | 6,25 | 7,9 Pixel
1920×1080 | 669 | 557 | 9,25 | 11,7 Pixel

Unter der *Karte* stehen fest 7,5rem für *Gründe*, 6rem für Knöpfe und 9rem für das
*Protokoll*. Mit eingefahrener unterer *Leiste* wird sie bei 1280×720 wieder 341 Pixel hoch.

**Kosten.** Bei 1280×720 trifft man einen Kreis von 4 Pixeln mit der Maus nur knapp, mit dem
Finger nicht; das *Ziel* verlangt beides. Ein Zug beginnt erst nach 4 Pixeln (V8), das sind
dort 1,2 *Zoll*: Ein kürzerer Weg gilt als Klick. Dasselbe trifft die Bildschirmtests, denn nur
`karteTest.py` setzt eine eigene Fenstergröße, die übrigen laufen in der Vorgabe von Playwright,
1280×720. Ob dabei Tests brechen, habe ich nicht erprobt. Das hält die Umsetzung von Item
ruhigeKarte auf, nicht die Tests dazu; der Implementierer übernimmt das Maß ohne Umschreiben (O3).

**Gegenvorschlag.** Wähle die drei Maße unter der *Karte* neu. Allein das *Protokoll* auf 4,5rem
gäbe nach Rechnung bei 1280×720 rund 269 Pixel und einen Kreis von 5,6 Pixeln, längere Listen
rollen. Reicht das nicht, frage den Stakeholder, wie klein die *Karte* in welchem Fenster werden
darf, und nenne ihm die Tabelle; seine Fenstergröße kennen wir nicht. Erledigt, wenn die *Karte*
bei 1280×720 mit leerem *Protokoll* wieder mindestens 309 Pixel hoch ist oder der Stakeholder
ein kleineres Maß entschieden hat.

**Stellungnahme.** Angenommen, umgesetzt in `vorschlag.css`, ohne neue Klasse. Das *Protokoll* allein auf 4,5rem hätte nicht gereicht: Die 9rem enthielten 2rem Innenabstand, die leere Leiste war vorher nur 32 Pixel hoch, und die Knöpfe brachen bei 1280×720 in zwei Zeilen um. Darum drei Maße: `.leisteUnten .leistenInhalt` 4,5rem hoch (längere Listen rollen), die seitlichen *Armeelisten* 13rem statt 16rem breit, damit die drei Knöpfe in einer Zeile stehen, und die Knopfzeile unter der *Karte* 3,5rem statt 6rem. Die Zeile für *Gründe* bleibt bei 7,5rem, weil wir nicht wissen, wie viele zugleich erscheinen. Gemessen im Mockup [que-7](../../domaene/mockups/que-7.html) mit null, einem und zwanzig *Einträgen*: *Karte* bei 1280×720 immer 544×309 an (368, 97), bei 1920×1080 immer 544×669 an (688, 97), also so hoch wie vorher. Erledigt-Bedingung erfüllt; eine Entscheidung des Stakeholders ist nicht nötig. Nicht erprobt: Knöpfe mit längerem Text als heute brechen bei 1280×720 wieder um.
