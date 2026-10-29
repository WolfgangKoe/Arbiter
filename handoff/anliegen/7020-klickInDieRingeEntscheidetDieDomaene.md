# Klick in die Ringe: bew-13 widerspricht BEW-14.1, entscheiden soll die Domäne

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf (DoR 5 für Item [Grenzkreise und Vorrücken](../../domaene/items/grenzkreise.md):
Der Implementierer übernimmt das Mockup ohne Umschreiben, der Test zu BEW-14.1 verlangt anderes).
1. [bew-13](../../domaene/mockups/bew-13.html) wählt innerhalb der *Bewegungsweite* Wurf 1.
   Geprüft mit Playwright (`document.elementFromPoint` auf der *Karte*): Ein Klick bei (2.5, 28.62),
   5″ von der *Stelle* des Boys, also innerhalb des *Grenzkreises* aus BEW-11.1, trifft
   `grenzeBoyzWurf1`. Die Maske blendet nur aus, was man sieht; angeklickt wird die ganze
   Kreisfläche, und die Gruppe der *Bewegungsweite* lässt mit `pointer-events: none` durch. Nach
   [BEW-14.1](../../domaene/anforderungen/phasen/bewegung/wurfPerFlaeche.md) gilt dort BEW-9.1.
   Die Ringe selbst treffen richtig: 6,2″ Wurf 1, 7,4″ Wurf 2, 11,2″ Wurf 6.
2. Welcher Wurf gilt, ist eine Regel aus *Abständen* (BEW-14.1, `core_rules.txt:754`). Mit
   `.grenze.wählbar` (`pointer-events: fill`) entscheidet sie die Stapelfolge im Markup, also
   das Frontend. Das widerspricht [6995](6995-frontendUndBackendImOrdner.md), Runde 2: „Das Bild
   zeigt, die Domäne entscheidet“, und der Entscheidung zur `grenze` (Anliegen 7004): Die
   Komponente kennt keine Regel.

**Kosten.** Bleibt es, baut der Implementierer entweder das Mockup und der Test zu BEW-14.1 ist
rot, oder er schreibt das Mockup um. Die Änderung: zwei Zeilen in `vorschlag.css`, keine im Markup.

**Gegenvorschlag.** Entschieden nach DoR 5: Der Klick auf die *Karte* geht wie heute mit seiner
*Stelle* an die Domäne; sie bestimmt den Wurf nach BEW-14.1 oder BEW-9.1. Die Ringe sind nur
Anzeige wie jede `grenze`. In `vorschlag.css` wird `.grenze.wählbar` zu
```css
.grenze.wählbar {
  stroke-opacity: 0.7;
}
```
und `.grenze.wählbar:hover` entfällt (ohne Trefferfläche kein Hover; kein Kriterium verlangt
ihn). Markup von bew-13 bleibt.

**Stellungnahme.** Übernommen wie vorgeschlagen: In [vorschlag.css](../../domaene/mockups/vorschlag.css) ist `.grenze.wählbar` nur noch `stroke-opacity: 0.7`, `:hover` entfällt (auch `fill`, `pointer-events`, `cursor`); das Markup von [bew-13](../../domaene/mockups/bew-13.html) bleibt. Der Klick geht mit seiner *Stelle* an die Domäne (BEW-14.1, BEW-9.1).
