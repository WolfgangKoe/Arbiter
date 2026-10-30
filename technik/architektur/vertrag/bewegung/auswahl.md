# Vertrag: Bewegung · Auswahl

Abschnitt der *Bewegungsphase*, dazu der Klick auf ein *Modell* (AUF-20.6, 25) schon in der
*Aufstellung*; die anderen: [Architektur](../../../architektur.md#schichten); was alle Phasen
teilen: [Querschnitt](../querschnitt.md).

- **V14** `PUT …/modelle/<m>/anklicken` (`…` wie V5) → `modellAnklicken(modell)`, 200 mit
  dem Spielstand, in der *Aufstellung* an `Aufstellung`, danach an `Schlacht`
  ([V11](../schlacht/tuer.md)): Die *Einheit* des *gesetzten* *Modells* ist *ausgewählt* mit
  der ganzen *Einheit* als *Ebene* und keine andere, gleich wer *an der Reihe* oder *am Zug*
  ist (AUF-20.6), in der *Aufstellung* auch eine *aufgestellte* (AUF-30.1). Ist sie schon
  *ausgewählt*, wird das *Modell* ihre *Ebene*, war es das schon, die ganze *Einheit*
  (AUF-25.1, 25.2, BEW-7.1, 7.2). Ein nicht *gesetztes* *Modell* ändert nichts, ohne
  `Sperre` (V5). Das entscheidet die Domäne, nicht die Seite. Wie [V3](../aufstellen/auswahl.md) keine Handlung: ohne D2. Warum eine eigene Route
  statt V2: V2 nimmt nur eine *Einheit* der *Armeeliste*.
- **V19** `PUT /api/karteAnklicken` (Körper wie V5) in der *Schlacht*:
  `Schlacht.karteAnklicken(stelle)`, danach ist keine *Einheit* *ausgewählt* (BEW-9.1), 200.
- Spielstand: `ausgewählt` und `ebene` wie in der *Aufstellung* (AUF-5.7, 25.1, 25.4,
  BEW-7.4).

Prüft wie im Querschnitt: V14 mit `einheitJederSeite`; V14 zweimal auf dasselbe *Modell*
der *ausgewählten* *Einheit*: erst `ebene` an ihm, dann an keinem.
