# Vertrag: Grenzkreise und Vorrücken

Abschnitt der *Bewegungsphase*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md). Die Domäne rechnet jede Grenze und entscheidet jeden Klick,
die Seite zeichnet nur, was der Spielstand nennt (W2, O5).

## Domäne
- **V20** `phasen/bewegung/vorruecken.py` hält je *Einheit*, ob sie auf ihren *Vorrückwurf*
  wartet, *vorgerückt* ist und mit welchem Wurf; `phasen/bewegung/grenzkreise.py` rechnet
  die *Grenzkreise* als `Kreis(stelle, radius)` in *Zoll*, den Radius aus `messen.py`
  (halber *Durchmesser* plus *Abstand*, M1). `Schlacht` gibt weiter: `vorrücken()`,
  `vorrückenZurücknehmen()`, `karteAnklicken(stelle)` (V19), Abfrage `grenzen`: je Eintrag
  `Grenze(einheit, kreise, wurf, wählbar, nahkampfreichweite)`, Felder wie V21.
  - BEW-11: um die *ausgewählte* *Einheit* des *Spielers* *am Zug* in der
    *Bewegungsphase* je *Modell* der *Ebene* ein Kreis um seine *Stelle* zu Beginn der
    *Bewegungsphase* (BEW-15.1), *Abstand* seine *Bewegungsweite*; je *Einheit* des anderen
    *Spielers* einer um jedes *gesetzte* *Modell*, *Abstand* 1″. Sonst keine (11.4).
  - BEW-13: wartet sie, dazu sechs mit *Abstand* plus 1″ bis 6″, `wählbar`; ist sie
    *vorgerückt*, nur der ihres Wurfs, nicht `wählbar`.
  - BEW-14, 5.3: `karteAnklicken(stelle)` setzt, während sie wartet, den kleinsten Wurf,
    dessen Kreise die *Stelle* enthalten, wenn die aus BEW-11 sie nicht enthalten; sonst
    BEW-9.1. Enthalten: Quadrat des Abstands zum Mittelpunkt höchstens Quadrat des Radius
    (S2). Danach hält V16 an *Bewegungsweite* plus Wurf.
  - BEW-5.1, 12: `vorrücken()` und `vorrückenZurücknehmen()` gelten der *ausgewählten*
    *Einheit*; wo BEW-5.1 oder 12.1 sie nicht anbieten, ändern sie nichts, ohne `Sperre`
    (wie `zurücklegen`). Zurücknehmen *setzt* jedes ihrer *Modelle* an seine *Stelle* zu
    Beginn der *Bewegungsphase* (12.2). Beides sind Handlungen (D2).

## Anfragen
Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
„Vorrücken“ (BEW-5.2) | `PUT /api/vorrücken` | `vorrücken`
„Vorrücken zurücknehmen“ (BEW-12.2) | `PUT /api/vorrückenZurücknehmen` | `vorrückenZurücknehmen`
Klick in einen Ring (BEW-14.1) | `PUT /api/karteAnklicken` (V19) | `karteAnklicken`

- **V21** Vor dem Ende der *Aufstellung* 404 wie V12. Spielstand: `schlacht.grenzen`, je
  *Grenzkreis* oder *Einhüllende* ein Eintrag `{"spieler": 1, "einheit": 1, "kreise": [{"x": 7.5,
  "y": 28.62, "radius": 5.63}]}`, dazu `"wurf": <n>` bei einem der sechs, `"wählbar": true` nach
  BEW-13.1, `"nahkampfreichweite": true` beim anderen *Spieler*; fehlt er, gilt er nicht.
  `schlacht.vorrücken`: `{"angeboten": <bool>, "zurücknehmen": <bool>}` nach BEW-5.1, 12.1.

## Seite
- Je Eintrag zeichnet `frontend/komponenten/grenze.js` (O5) eine `grenzeMaske` und
  eine `g.grenze spieler<n>`, dazu `nahkampfreichweite`, `wählbar`, wie Mockups bew-5,
  bew-11, bew-12, bew-13; die Kennung der Maske aus `spieler`, `einheit`, `wurf`. Ein Kreis
  ist die *Einhüllende* seines Eintrags, gerechnet wird nicht. Grenzen liegen unter den
  *Modellen*; ein Klick auf sie ist ein Klick auf die *Karte* (V19).
- Knöpfe (V7): „Vorrücken“, wenn `angeboten`, „Vorrücken zurücknehmen“, wenn
  `zurücknehmen`, vor „Phase beenden“.

Prüft wie im Querschnitt: `grenzen` am Dienst mit exakten Radien (B3) für Modell, *Einheit*,
Gegner, Wurf; ein Klick zwischen Ring 3 und 4 macht 4, im Ring aus BEW-11 hebt er die
*Auswahl* auf; BEW-15 mit dem Weg der Anforderung; am Bildschirm Zahl und Klassen der
`g.grenze`.
