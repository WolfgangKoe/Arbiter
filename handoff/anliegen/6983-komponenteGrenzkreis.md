# Komponente Grenzkreis für Bewegung und Nahkampfreichweite

Form: Auftrag
Von: Ux
An: Architekt
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Der Stakeholder will Grenzen von *Nahkampfreichweite* und *Bewegung* als leichten Kreis auf der *Karte* sehen ([Anliegen 6410](6410-grenzkreiseNahkampfUndBewegung.md)). [komponenten.css](../../technik/frontend/komponenten.css) hat keine Komponente dafür; ein Mockup darf nur vorhandene nutzen.

**Kosten.** Ohne Komponente kein einbaufähiges Mockup; Ux erfindet sie nicht.

**Gegenvorschlag.** Nimm eine Komponente `grenzkreis` (ein `<circle>` ohne Füllung, schwacher Strich, ein Kreis je *Modell*) in die Komponentenseite auf, oder nenne eine andere Form. Ux zeichnet das Mockup, sobald sie steht und [6984](6984-kriteriumGrenzkreise.md) ein Kriterium liefert.

**Stellungnahme.** Entschieden nach [DoR 5](../../prozess/ablauf/dor.md): Komponente `grenzkreis`, ein Kreis je *Modell*. Ux übernimmt die Regeln wörtlich in [vorschlag.css](../../domaene/mockups/vorschlag.css), der Implementierer trägt sie in der Technikphase in [komponenten.css](../../technik/frontend/komponenten.css) ein.
```css
.grenzkreis {
  fill: none;
  stroke: var(--spielerFarbe);
  stroke-opacity: 0.45;
  stroke-width: 0.08;
  pointer-events: none;
}

.grenzkreis.nahkampfreichweite {
  stroke-dasharray: 0.3 0.2;
}
```
Markup: `<circle class="grenzkreis spieler1" cx="…" cy="…" r="…"/>` mit `cx`, `cy` des *Modells*, in der Karte vor den *Modellen*, damit sie obenauf liegen. Durchgezogen ist die Grenze der Bewegung (*Normale Bewegung* oder *Vorrücken*), gestrichelt die *Nahkampfreichweite*; die Farbe ist die des *Spielers* des *Modells*.

Warum so:
- Ein Kreis je *Modell* wie [ArbiterMap, Abschnitt 5](../../ArbiterMap/docs/spec/interaction_map.md) (Variante A in [Item 013](../../ArbiterMap/steering/backlog/items/013-spike-reichweiten-darstellung.md)). Eine Hülle um die ganze *Einheit* (Variante B) bräuchte Winkelrechnung und wäre an den Rändern ungenau; sie wäre ein Fall für ein eigenes Kriterium.
- `pointer-events: none`: Die Bedienung findet das gezogene *Modell* über das angeklickte Element (`technik/frontend/bedienung.js`, Zeile 73 und 85). Ohne die Regel träfe ein Klick auf den Strich den Kreis statt des *Modells* darunter, und Auswahl und Ziehen gingen ins Leere.
- Strich und Striche in *Zoll* (die Karte rechnet in *Zoll*, `viewBox="0 0 44 60"`), nicht in Pixeln wie `.modell.ausgewählt`: So rechnen alle Browser die Striche gleich. Mit Pixel-Strich (`vector-effect`) ist mir das ungeprüft, ich würde es erst erproben. 0,08″ sind bei voller Kartenbreite etwa ein Pixel. Solange die Karte nicht zoomt, sieht man keinen Unterschied.
- Nur ein Zusatz (`nahkampfreichweite`), denn nur zwei Arten verlangt der Stakeholder. Einen *Vorrückwurf*-Ring zeichnet man mit derselben Klasse und anderem Radius. Kommt eine dritte Art hinzu, kommt eine Zeile dazu (Es, O).

Nicht Teil der Komponente ist der Radius, er kommt aus dem Kriterium ([6984](6984-kriteriumGrenzkreise.md)). Weil der *Abstand* von der *Base* aus gemessen wird, liegt die Grenze im Radius der *Base* plus Weite um den Mittelpunkt des *Modells*. So zeichnet es ArbiterMap: `r="2463"` = 63 + 2400 für 24″ in Hundertstel-*Zoll*. Wo der Radius berechnet wird (im Backend oder im Frontend), entscheide ich in der Technikphase.
