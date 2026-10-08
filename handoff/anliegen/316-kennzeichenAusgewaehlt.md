# Komponente „ausgewählt“ für Ablage und Karte

316 · Fragen · von UX (Domäne) → Architekt (Technik) · Runde 1/3 · angenommen

## Runde 1
**Befund.** AUF-5.6 und AUF-5.7 verlangen, dass die Ablage jede ausgewählte Einheit und die
Karte jedes gesetzte Modell einer ausgewählten Einheit kennzeichnet. Die Komponentenseite
(`technik/frontend/komponenten.html`) hat dafür nichts; `inAufstellung` (AUF-4.5) und das
Abzeichen gehören zu AUF-4.5 und müssen unterscheidbar bleiben. Die Mockups
[auf-5](../../domaene/mockups/auf-5.html) und [auf-6](../../domaene/mockups/auf-6.html)
brauchen nur das eine.

**Kosten.** Ohne die Komponente bleibt DoR 5 für AUF-5 offen. Die Mockups nutzen bis zur
Antwort die Klassen `ausgewählt` an `einheitenKarte` und an `modell`; sie stehen weder in
`vorschlag.css` noch in `komponenten.css`.

**Gegenvorschlag.** Zwei Zustände in `komponenten.css`, gebaut aus `vorschlag.css`:
`.einheitenKarte.ausgewählt` mit Rand in der Spielerfarbe der Ablage (nicht Gelb, das gehört
`inAufstellung`) und `.modell.ausgewählt` mit hellem Ring. Beides kombinierbar mit
`inAufstellung`. Gibst du andere Namen vor, ziehe ich die Mockups nach.

**Stellungnahme.** Angenommen mit einer Änderung. Name `ausgewählt` wie vorgeschlagen:
Zustandsklasse mit dem Glossarbegriff, wie `inAufstellung` und `anDerReihe`. Die Komponente:
```css
.einheitenKarte.ausgewählt {
  outline: 2px solid var(--spielerFarbe);
  outline-offset: 2px;
}

.modell.ausgewählt {
  stroke: var(--text);
  stroke-width: 2px;
  vector-effect: non-scaling-stroke;
}
```
- Karte in der Ablage: `outline` statt Rand. `inAufstellung` belegt schon `border-color` und
  `box-shadow`; zwei Regeln auf derselben Eigenschaft entscheidet die Reihenfolge in der
  Datei, kombiniert sähe man nur eine. `outline` ist eine eigene Eigenschaft: Beide Zustände
  sind zugleich sichtbar (gelb innen, Spielerfarbe außen), ohne dritte Regel.
- Modell: Die Karte rechnet in Zoll (Web, O2); ohne `non-scaling-stroke` wäre der Ring
  2 Zoll breit. Hell ist `--text`, nicht `--akzentHell` (gehört `inAufstellung`).
- Wegwerf-Versuch: `auf-5.html` mit beiden Regeln in Chromium (Playwright). Ring und
  Umriss sichtbar, die kombinierte Karte unterscheidbar; `getComputedStyle` trennt die
  Zustände (`outlineStyle` `solid`/`none`, `stroke`), also prüfbar nach Web, B3;
  stylelint mit `.stylelintrc.json` grün.

Weg: In der Domänenphase arbeite ich nicht in `technik/`, `technik/frontend/` schreibt der
Implementierer. Du übernimmst die beiden Regeln wörtlich in `vorschlag.css`; der
Implementierer trägt sie in der Technikphase in `komponenten.css` ein und zeigt in
`komponenten.html` die Zustände `ausgewählt`, `inAufstellung ausgewählt` und ein `modell`
mit `ausgewählt` (Web, O3). Die Mockups bleiben wie sie sind.
