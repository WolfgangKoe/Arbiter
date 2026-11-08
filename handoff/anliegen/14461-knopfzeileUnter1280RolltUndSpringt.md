# Unter 1280 Pixeln Breite springt die Karte nach dem Rollen

Form: Kritik
Von: Fachkritiker
An: UX
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Die Knopfzeile von 3,5rem in `.spalteMitte` ([vorschlag.css](../../domaene/mockups/vorschlag.css)) fasst unter 1280 Pixeln Breite nur eine von zwei Zeilen. Die Spalte ragt 20 Pixel über. Rollt der Spieler und fällt die zweite Zeile weg, rückt die *Karte* 20 Pixel, gegen [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md). `scrollbar-gutter` aus 14080 hält nur die Breite still, nicht die Höhe. Messung: [14460](14460-ruhigeKarteNachDemRollenOhneTest.md). In 14080 stand der Nachteil als „man rollt“, der Sprung danach war nicht genannt.

**Kosten.** Der Implementierer übernimmt das CSS ohne Umschreiben (O3), der Test aus 14460 bliebe mit diesem Maß rot. Item ruhigeKarte käme nicht zur Abnahme.

**Gegenvorschlag.** In `vorschlag.css` unter 1280 Pixeln Breite die Zeile auf 6rem, die zwei Knopfzeilen fassen:

```
@media (max-width: 1279px) {
  .spalteMitte { grid-template-rows: minmax(0, 1fr) 7.5rem 6rem; }
}
```

Keine neue Klasse. Erprobt an einer Kopie des Stands 4fd5bd9 mit den Maßen des Mockups, ohne Rückwirkung auf das Gebaute: alle 88 Tests grün, die Spalte ragt in allen vier Fenstern nicht mehr über, die *Karte* steht nach dem Klick still. Die *Karte* wird nur unter 1280 Breite niedriger: 1024×768 von 357 auf 317 Pixel, 1100×800 von 389 auf 349; bei 1280×720 bleibt sie 309 hoch, wie in 14040 verlangt, bei 1920×1080 669. Den `scrollbar-gutter` macht das vermutlich überflüssig; ob er bleibt, wählst du. Andere Lösung ist dir frei. Erledigt, wenn in que-7 mit vier Knöpfen bei 1024×768 und 1100×800 nach dem Rollen und Klick auf „gemeinsam übergehen“ die *Karte* still steht und bei 1280×720 mindestens 309 Pixel hoch bleibt.

**Stellungnahme.** Zugestimmt, umgesetzt wie vorgeschlagen in
[vorschlag.css](../../domaene/mockups/vorschlag.css) (gleiche Regel wie in 14480). Der
`scrollbar-gutter` bleibt: Er hält die Breite still, falls die Spalte doch einmal rollt, und kostet
nichts. Ab 1280 Pixeln ändert sich nichts, 309 Pixel bei 1280×720 bleiben.
