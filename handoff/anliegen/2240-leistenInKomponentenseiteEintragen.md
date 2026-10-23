# Leisten und Protokoll in die Komponentenseite eintragen

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: erledigt
Wartet auf: Technikphase

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): wartet auf die
Technikphase. In Anliegen 2230 habe ich *Leiste*, *Griff*, den
Inhalt der *Leiste*, das *Protokoll* und den Protokolleintrag als Komponenten entschieden. Ux
hat ihre Regeln in [vorschlag.css](../../domaene/mockups/vorschlag.css) übernommen. In
[komponenten.css](../../technik/frontend/komponenten.css) und
[komponenten.html](../../technik/frontend/komponenten.html) fehlen sie noch. Nach
[DoR 5](../../prozess/ablauf.md#dor-item-bereit) trägst du sie ein. Kein Mechanismus erinnert
daran, wie schon in [2130](2130-goldenerRahmenInKomponentenCss.md).

**Kosten.** Rund 90 Zeilen CSS, wörtlich übernommen, und etwa 30 Zeilen Markup. Kein Test
ändert sich. Fehlt der Eintrag, fehlt dem Mockup zu QUE-5 und QUE-6 die Vorlage. Dann sieht die
Seite anders aus als `que-5.html`, wenn das Item gebaut wird.

**Gegenvorschlag.** In `komponenten.css`, wörtlich aus `vorschlag.css`
([O3](../../technik/architektur/oberflaeche.md)):
- in `body` die dritte Zeile im Raster: `grid-template-rows: auto 1fr auto;`;
- den Block ab `.spielbereich:has(> .leiste)` bis einschließlich `.protokollGrund`.

In `komponenten.html` gilt das Markup aus
[que-5.html](../../domaene/mockups/que-5.html) und O4:
- Die beiden `<aside class="spalte">` werden zu `<aside class="leiste leisteLinks">` und
  `<aside class="leiste leisteRechts">`. Jede bekommt einen *Griff*
  (`<button class="leistenGriff" type="button" aria-expanded="true" aria-label="…">`) und um
  die vorhandenen `armeeKarte` ein `<div class="leistenInhalt">`. Die Varianten der
  *Ablagen* bleiben.
- Nach `</main>` kommt `<aside class="leiste leisteUnten">` mit *Griff* und
  `<ul class="protokoll">`. Darin stehen zwei `protokollEintrag`, je einer mit `spieler1` und
  mit `spieler2`, damit beide Farben zu sehen sind. Die Gründe stammen aus vorhandenen
  Mockups, zum Beispiel „keine Kohärenz“ und „nicht ganz in der Zone“.
- Alle *Leisten* sind ausgefahren wie beim Start (QUE-6.2). *Eingefahren* zeigt die Seite
  nicht, denn das blendete die Varianten aus; die Regel dazu steht im CSS.

Erledigt, wenn jede neue Klasse aus `vorschlag.css` in `komponenten.html` vorkommt (O3: keine
tote Klasse) und `frontendregeln.frontend` grün ist.

**Stellungnahme.** Angenommen und umgesetzt in
[komponenten.css](../../technik/frontend/komponenten.css) und
[komponenten.html](../../technik/frontend/komponenten.html), wie vorgeschlagen. Einzige
Abweichung: Jede `<aside class="leiste …">` trägt ein `aria-label`, weil SonarLint (Web:S5255)
sonst warnt; `vorschlag.css` ist davon nicht berührt.
