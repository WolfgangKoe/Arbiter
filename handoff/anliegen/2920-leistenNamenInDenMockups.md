# Die Mockups nennen die Leisten nicht und den Griff noch Ablage

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Domänenphase. Die *Leisten* baut erst Item
[gemeinsamUebergehen](../../domaene/items/gemeinsamUebergehen.md); kein Schritt des Happy Path
von Plan 7 ist betroffen. Auf Anliegen 2215 legt
[Oberfläche, O4](../../technik/architektur/oberflaeche.md) jetzt fest: Jede *Leiste* trägt ein
`aria-label` mit ihrem Inhalt, ihr *Griff* dasselbe mit „ein- und ausfahren“. In
[que-5.html](../../domaene/mockups/que-5.html) und [que-7.html](../../domaene/mockups/que-7.html)
hat keine `<aside class="leiste">` einen Namen, und die *Griffe* heißen noch
„Ablage Spieler 1“ und „Ablage Spieler 2“, obwohl die *Ablage* *Armeeliste* heißt (Anliegen 2221).

**Kosten.** Je Mockup sechs Attribute. Bleibt es so, übernimmt der Implementierer nach O3
Markup, das O4 widerspricht, und SonarLint meldet je Datei dreimal Web:S5255.

**Gegenvorschlag.** In beiden Mockups:
- `<aside class="leiste leisteLinks" aria-label="Armeeliste Spieler 1">`, der *Griff* darin
  `aria-label="Armeeliste Spieler 1 ein- und ausfahren"`;
- `<aside class="leiste leisteRechts" aria-label="Armeeliste Spieler 2">`, der *Griff*
  `aria-label="Armeeliste Spieler 2 ein- und ausfahren"`;
- `<aside class="leiste leisteUnten" aria-label="Protokoll">`, der *Griff*
  `aria-label="Protokoll ein- und ausfahren"`.

Erledigt, wenn in `domaene/mockups/` jede `<aside class="leiste …">` und jeder `leistenGriff`
den Namen nach O4 trägt und „Ablage“ dort nicht mehr vorkommt.

**Stellungnahme.** Einverstanden, umgesetzt. In [que-5.html](../../domaene/mockups/que-5.html)
und [que-7.html](../../domaene/mockups/que-7.html) trägt jede *Leiste* ihren Namen und jeder
*Griff* „… ein- und ausfahren“ nach O4; „Ablage“ kommt nicht mehr vor.
