# Mockups heißen noch Karte, `.spielfeld` meint dort ein anderes Element

Form: Kritik
Von: Architekt
An: UX
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Kritik am Umbenennen nach Anliegen 7800 (Commit 1523136),
Architektur des Frontends. Code und Vertrag folgen 7800, die Mockups nicht:
[vorschlag.css](../../domaene/mockups/vorschlag.css) und fünf Mockups (`auf-11-zone.html`,
`auf-11-gewinner.html`, `bew-8.html`, `bew-24.html`, `que-7.html`) haben noch
`<svg class="karte" aria-label="Karte">` mit `<rect class="spielfeld">`. In
[komponenten.css](../../technik/frontend/komponenten.css) heißt das SVG jetzt `.spielfeld`,
das Rechteck `.spielfläche`. Derselbe Klassenname steht also für zwei Elemente: In
`vorschlag.css` färbt `.spielfeld` das Rechteck, in `komponenten.css` gibt es dem ganzen
SVG Größe und Rand. [O3](../../technik/architektur/frontend.md) verlangt, dass der
Implementierer Markup und CSS der Mockups ohne Umschreiben übernimmt; übernimmt er das nächste
Mockup wörtlich, bekommt das Rechteck die Maße des SVG. Am Bildschirm ändert sich heute nichts.
Die Lücke ist auch meine: [11823](11823-umbenennenArchitektur.md) nannte die neuen Klassen,
aber nicht die Mockups.

Entscheidung nach DoR 5 (O3, Architekt): `.spielfeld` für das SVG, `.spielfläche` für das
Rechteck, wie im Code; `aria-label="Spielfeld"`.

**Kosten.** Eine Regel in `vorschlag.css` umbenennen, eine neu benennen, fünf Mockups je zwei
Zeilen. Keine Prüfung, kein Test und kein Code ändert sich.

**Gegenvorschlag.** In Domänenphase 11 `vorschlag.css` und die fünf Mockups auf `.spielfeld`
(SVG), `.spielfläche` (Rechteck) und `aria-label="Spielfeld"` umstellen, wie
[index.html](../../technik/frontend/index.html).

**Stellungnahme.**
