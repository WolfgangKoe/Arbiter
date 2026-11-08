# Ruhige Karte: Die Umbruchstelle der Knopfzeile steht in Pixeln, die Maße in rem

Form: Kritik
Von: Reviewer
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** In [komponenten.css](../../technik/frontend/komponenten.css) bekommt die Knopfzeile unter der *Karte* erst unterhalb von `max-width: 1279px` die Höhe für zwei Zeilen (`6rem`), darüber nur `3.5rem`. Ob die Knöpfe umbrechen, hängt aber an rem: *Leisten* `13rem`, Knöpfe mit Schrift und Abstand in rem. Die Grenze 1279 Pixel gilt nur bei 16 Pixeln Grundschrift. Wer im Browser eine größere Grundschrift eingestellt hat, etwa 20 Pixel, hat bei 1280 Pixeln Breite für die Knöpfe rund 630 statt 750 Pixel, die Knöpfe sind dabei ein Viertel breiter: Sie brechen um, die zweite Zeile ragt aus ihren `3.5rem`, die mittlere Spalte rollt, und nach dem Klick springt die *Karte* wieder, der Fehler aus 14480. Ein Randfall abseits des Happy Path, darum wartend; die Tests laufen mit 16 Pixeln und bemerken es nicht.

**Kosten.** Bleibt es so: bei größerer Grundschrift in Fenstern ab 1280 Pixeln verletzt die Seite QUE-7.1. Der Gegenvorschlag ist eine Zeile, ohne neue Tests.

**Gegenvorschlag.** Die Umbruchstelle in em statt Pixeln: `@media (max-width: 79.99em)`; em in einer Media Query folgt der Grundschrift des Browsers und ist bei 16 Pixeln dieselbe Stelle wie heute. Im Mockup [vorschlag.css](../../domaene/mockups/vorschlag.css) steht dieselbe Zeile; gleichziehen lässt sie die UX.

**Stellungnahme.**
