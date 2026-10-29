# Komponente für Grenzen als leichter Bereich

Form: Fragen
Von: Ux
An: Architekt
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Der Stakeholder wünscht in [Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md) eine
wiederverwendbare Oberflächenkomponente: Sie zeigt die Grenze eines Bereichs leicht an, bei einem
*Modell* als Kreis, bei einer *Einheit* als Einhüllende der Kreise ihrer *Modelle*, später auch
für den Abstand zu einer *Aufstellungszone*. Farbe, Linienart und -dicke sind Parameter. Er
regt an, den Akzeptanztest dem Frontend zuzuordnen. In
[komponenten.css](../../technik/frontend/komponenten.css) steht sie noch nicht; die Regeln für
`grenzkreis` liegen vorläufig in [vorschlag.css](../../domaene/mockups/vorschlag.css).

**Kosten.** Bis zur Antwort bleibt `grenzkreis` im Vorschlag.

**Gegenvorschlag.** Komponente allgemein benennen, Parameter als Klassen, Einhüllende im Frontend
berechnet; wo der Test liegt, entscheidet der Architekt.

**Stellungnahme.** Entschieden nach DoR 5, mit [6995](6995-frontendUndBackendImOrdner.md) F3 A:
- Name `grenze`: der Rand aller Punkte höchstens *Abstand* von Formen. Um eine *Base* ist das
  ein *Grenzkreis*, um mehrere die *Einhüllende*; die Komponente kennt den Unterschied nicht.
  Welche *Modelle* und welcher *Abstand*, entscheidet die Domäne. Modul in der Technikphase:
  `technik/frontend/komponenten/grenze.js`.
- Parameter als Klassen: Farbe die Spielerklasse, Linienart und -dicke die Art
  (`nahkampfreichweite`); ohne Art durchgezogen. Eine neue Art ist eine Regel, kein Zweig.
- Einhüllende: Der Browser zeichnet sie, keine Geometrie in JavaScript oder Python. Je Grenze
  eine Gruppe aus Kreisen mit Radius *Base* + *Abstand*; ihre Maske blendet dieselben Kreise
  gefüllt aus, übrig bleibt der äußere Rand, auch gestrichelt. Wegwerf-Versuch:
  `/tmp/bereichProbe2/probe2.png`. Die gezeichnete `path` in bew-11 entfällt damit.
- Markup, eine Gruppe je Grenze, im `<svg>` der *Karte*:
  ```html
  <mask id="grenzeBoyz" class="grenzeMaske" maskUnits="userSpaceOnUse" x="0" y="0" width="44" height="60"><rect width="44" height="60"/><circle cx="5.11" cy="27.24" r="5.63"/></mask>
  <g class="grenze spieler1" mask="url(#grenzeBoyz)"><circle cx="5.11" cy="27.24" r="5.63"/></g>
  ```
- Regeln für `vorschlag.css`, wörtlich; sie ersetzen `.grenzkreis` (Farben nur in `:root`,
  stylelint). Die Maske verbirgt die innere Hälfte der Linie, 0.16 zeigt 0.08 wie bisher:
  ```css
  :root { --maskeSichtbar: #fff; --maskeVerborgen: #000; }
  .grenze { fill: none; stroke: var(--spielerFarbe); stroke-opacity: 0.45; stroke-width: 0.16; pointer-events: none; }
  .grenze.nahkampfreichweite { stroke-dasharray: 0.3 0.2; }
  .grenzeMaske rect { fill: var(--maskeSichtbar); }
  .grenzeMaske circle { fill: var(--maskeVerborgen); }
  ```
  Die zwei Variablen kommen in den bestehenden `:root`-Block, die Regeln je mehrzeilig wie dort.
- Test: Der Akzeptanztest bleibt bei der Anforderung ([T1, B1](../../technik/architektur/tests.md));
  als Bildschirmtest prüft er schon das Frontend: Gruppe `grenze`, Kreise, Radius im Markup.
  Welche *Modelle*, prüft ein Einheitstest der Domäne. Einen eigenen Testlauf für JavaScript
  gibt es nicht und lohnt hier nicht; die Linie selbst sieht der Stakeholder im Review.
- Eine *Aufstellungszone* plus x″ wäre ein `rect` mit `rx` = x; erst mit einem Kriterium.
