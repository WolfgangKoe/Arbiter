# Vertrag: Grenzkreise, Vorrücken und Zurücksetzen

Abschnitt der *Bewegungsphase*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md). Die Domäne rechnet jede Grenze und entscheidet jeden Klick,
die Seite zeichnet nur, was der Spielstand nennt (W2, O5).

## Domäne
- **V20** `Bewegungsphase` hält je *Einheit*, ob sie auf ihren *Vorrückwurf* wartet,
  *vorgerückt* ist und mit welchem Wurf; das brauchen BEW-5, 12, 13, 14 und V16 zusammen
  ([Grundschnitt](../../domaene.md#grundschnitt-der-domäne)). `phasen/bewegung/grenzkreise.py`
  rechnet je Eintrag eine `Einhüllende(einheit, kreise, wurf, wählbar, nahkampfreichweite)`
  aus `Grenzkreis(stelle, radius)` in *Zoll*, Radius `messen.radiusInZoll` plus *Abstand*
  (M1); bei einem *Modell* ist sie sein *Grenzkreis*. `Schlacht` gibt weiter: `vorrücken()`,
  `vorrückenZurücknehmen()`, `karteAnklicken(stelle)` (V19), Abfrage `grenzen` mit diesen
  Einträgen, Felder wie V21.
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
  - BEW-22.1: Steht ein *Modell* der *Einheit* an seiner jetzigen *Stelle* (die Anforderung:
    „ist“) in *Nahkampfreichweite* eines des anderen *Spielers*
    (`querschnitt/setzen.inNahkampfreichweite`), bietet `Schlacht` „Vorrücken“ nicht an,
    auch nicht nach BEW-5.1; Regel in `phasen/bewegung/keinVorrueckenAusDerNahkampfreichweite.py`.
    Zurücknehmen (12.1) bleibt.
  - BEW-9.2: V19 hebt nur die *Auswahl* auf; das Warten hält `Bewegungsphase` je *Einheit*,
    bis 5.3 oder 12.2 es beendet. Nichts Neues.
  - BEW-24: `einheitZurücksetzen()` und Abfrage `einheitZurücksetzenAngeboten` gelten der
    *ausgewählten* *Einheit*. Angeboten (24.1) in der *Bewegungsphase*, wenn 12.1 nicht
    anbietet und eine *Stelle* eines ihrer *Modelle* nicht gleich der zu Beginn der
    *Bewegungsphase* ist (nach Inhalt, D1); Regel in `phasen/bewegung/einheitZuruecksetzen.py`.
    Eine *Einheit* des anderen *Spielers* steht immer dort (V16), darum gleicht es dem
    Angebot nur für den *Spieler* *am Zug* wie bei `vorrücken`. Ohne Angebot ändert es nichts,
    ohne `Sperre`; sonst steht jedes ihrer *Modelle* an seiner *Stelle* zu Beginn (24.2), ohne
    `Sperre` und Eintrag im *Protokoll*, die *Auswahl* bleibt. Eine Handlung (D2): Sie beendet
    das Angebot aus V18. Überdeckt eine *Base* dann eine fremde: offen in Anliegen 10322.

## Anfragen
Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
„Vorrücken“ (BEW-5.2) | `PUT /api/vorrücken` | `vorrücken`
„Vorrücken zurücknehmen“ (BEW-12.2) | `PUT /api/vorrückenZurücknehmen` | `vorrückenZurücknehmen`
„Einheit zurücksetzen“ (BEW-24.2) | `PUT /api/einheitZurücksetzen`, ohne Körper | `einheitZurücksetzen`
Klick in einen Ring (BEW-14.1) | `PUT /api/karteAnklicken` (V19) | `karteAnklicken`

- **V21** Vor dem Ende der *Aufstellung* 404 wie V12. Spielstand: `schlacht.grenzen`, je
  *Grenzkreis* oder *Einhüllende* ein Eintrag `{"spieler": 1, "einheit": 1, "kreise": [{"x": 7.5,
  "y": 28.62, "radius": 5.63}]}`, dazu `"wurf": <n>` bei einem der sechs, `"wählbar": true` nach
  BEW-13.1, `"nahkampfreichweite": true` beim anderen *Spieler*; fehlt er, gilt er nicht.
  `schlacht.vorrücken`: `{"angeboten": <bool>, "zurücknehmen": <bool>}` nach BEW-5.1, 12.1, 22.1;
  `schlacht.einheitZurücksetzen`: `{"angeboten": <bool>}` nach BEW-24.1. Beispiel
  [einheitZurueckzusetzen.json](../einheitZurueckzusetzen.json), nur `schlacht`: Stand von
  [schlacht.json](../schlacht.json), dann den Warboss anklicken
  (`PUT /api/spieler/1/einheiten/2/modelle/1/anklicken`) und 3″ nach Osten loslassen.

## Seite
- Je Eintrag zeichnet `frontend/komponenten/grenze.js` (O5) eine `grenzeMaske` und
  eine `g.grenze spieler<n>`, dazu `nahkampfreichweite`, `wählbar`; die Kennung der Maske aus `spieler`, `einheit`, `wurf`. Ein Kreis
  ist die *Einhüllende* seines Eintrags, gerechnet wird nicht. Grenzen liegen unter den
  *Modellen*; ein Klick auf sie ist ein Klick auf die *Karte* (V19).
- Knöpfe (V7): „Vorrücken“, wenn `angeboten`, „Vorrücken zurücknehmen“, wenn
  `zurücknehmen`, dann „Einheit zurücksetzen“, wenn `einheitZurücksetzen.angeboten`, alle vor
  „Phase beenden“ (Mockup [bew-24](../../../../domaene/mockups/bew-24.html)).

Prüft wie im Querschnitt: `grenzen` am Dienst mit exakten Radien (B3) für Modell, *Einheit*,
Gegner, Wurf; ein Klick zwischen Ring 3 und 4 macht 4, im Ring aus BEW-11 hebt er die
*Auswahl* auf; BEW-15 mit dem Weg der Anforderung; am Bildschirm Zahl und Klassen der
`g.grenze`. BEW-22.1: ein *Modell* in *Nahkampfreichweite* (etwa nach BEW-8.4), `angeboten`
falsch und `PUT /api/vorrücken` ändert nichts. BEW-24 mit dem Beispiel, dann
`PUT /api/einheitZurücksetzen`: *Stellen* exakt wie zu Beginn (B3), `angeboten` falsch, ein
zweites `PUT` ändert nichts; nicht angeboten, solange die *Einheit* wartet oder *vorgerückt* ist.
