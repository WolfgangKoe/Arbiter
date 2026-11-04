# Vertrag: Bewegung · Fliegen

Abschnitt der *Bewegungsphase* (BEW-18, MIV-3), die anderen: [Architektur](../../../architektur.md#schichten);
ändert V10 und V16 ([Ziehen](ziehen.md), [Handlungen](handlungen.md)) und V18
([Übergehen](../schlacht/uebergehen.md)) für eine *Einheit* mit *Fliegen*.

- Daten: `Einheit.fliegen: bool = False` (`spielobjekte.py`), gelesen nach
  [Katalog](../../katalog.md) K3, K7; erst die Zeile (11840), dann der Wert (9340). Web und
  Seite unverändert: kein Schlüssel im Spielstand, die Seite zeichnet die Antworten (V6).
- Eingabe: `Schlacht` gibt `einheit.fliegen` des gezogenen *Modells* an die
  `Bewegungsphase`, gebündelt mit Ebene, gezogenem *Modell*, Ziel und `weiter` in einem
  unveränderlichen `Gezogen` (ersetzt die Parameter, die heute `# noqa: PLR0913` brauchen);
  `Angebot` merkt sich `fliegen`.
- **Ziehen** (V10, BEW-18.1): wie V16, ohne 17.1 bis 17.4 (`weiter` zählt nicht, Antwort
  `angehaltenAufDemWeg` falsch), 6.2 nach 18.3, ohne QUE-1.2 (nach BEW-19.1 ist dann jede
  *Base*, die sperren könnte, nach AUF-29.3 fremd; das löst 18.2 beim Loslassen). So zeigt
  die *Karte* die Spinne über fremden *Bases* (8840, „nur darüber hinwegziehen“). Die Gleichheit von V10 und V5 (AUF-28.2, BEW-17.2,
  20.1) gilt nur, solange keine fremde *überdeckt* ist; sonst *setzt* V5 nach 18.2.
- **18.3** in `phasen/bewegung/fliegen.py`: Ende ist der kleinere Anteil von 3.1 und 6.1
  (6.3). Ist dort keines in *Nahkampfreichweite*, ist der Anteil von 6.2 1; sonst das größte
  k/n bis zum Ende (Raster S3), an dem keines darin ist. Rechnung rückwärts: Für jedes Paar,
  das am Schritt berührt, den ersten berührenden Schritt davor (Intervall, konvex), weiter
  ab dem kleinsten minus 1, bis keines berührt; unter 0 ist er 0 (wie BEW-25.1). Neu in
  `messen.py` (M1): Anteil vor der letzten Berührung bis zu einem Anteil.
- **18.2** beim `modellLoslassen`, in `fliegen.py`: *Überdeckt* an den *Stellen* nach V10
  eine eine fremde, sucht Arbiter den kürzesten Weg w, mit dem jede verschobene *Stelle*
  frei ist: keine fremde *überdeckt* (ohne die Ausnahme des Gleitens), *Distanz* höchstens
  *Bewegungsweite* plus *Vorrückwurf*, *ganz in* dem *Spielfeld*, nicht in
  *Nahkampfreichweite*; geprüft exakt mit den Messungen von V16 und QUE-1 (S2). Neu in
  `messen.py` (M1): `wegInDieFreieFläche(ränder, frei, zurück) -> Weg | None`. `ränder`
  nennt im Raum der Wege je Paar Kreise, die gemieden werden (Summe der Radien, bei
  *Nahkampfreichweite* plus 1″), je *Modell* den Kreis der *Bewegungsweite* und das Rechteck
  des *Spielfelds*. Kandidaten, aufsteigend nach Länge: die Lotpunkte auf jeden Rand, die
  Schnittpunkte je zweier Ränder, als `float` gerechnet und mit Toleranz 10⁻⁶ vorgefiltert;
  je Kandidat der auf Nenner 10⁶ gerundete Punkt und 16 Richtungen in den Abständen 1/2000,
  1/1000, 1/500, 1/250″; der erste, den `frei` exakt bestätigt, gilt. So liegt er höchstens
  1/100″ weiter als die nächste freie *Stelle*. `zurück` (der Weg zur *Stelle* vor dem
  Ziehen) begrenzt die Suche: Ränder weiter weg zählen nicht. Findet sie keinen, sperrt
  QUE-1.2 (V15, BEW-18.6). Kein *Grund*, 200; das Angebot nach V18 folgt 3.1 und 6.2
  (18.3) wie sonst, nicht dem Rücken.
- **Übergehen** (V18 mit `fliegen`, BEW-18.5): ohne Gleiten, an den Punkt, an der
  *Spielfeldkante* angehalten (BEW-8.4 zeigt nach 18.1). *Überdeckt* dort eine eine fremde,
  rückt Arbiter nach 18.2 (*Bewegungsweite* ab der gemerkten *Stelle* vor dem Ziehen), dann
  QUE-1 ohne QUE-1.3 wie V18; findet sie keinen, sperrt QUE-1.2, das Angebot bleibt. Die
  *Gründe* nach BEW-8.5 auf dem Weg von der *Stelle* davor zu der danach (V18), 6.2 nach
  18.3; gerückt also keiner.
- Aufbau: `fliegen.py` hält 18.2, 18.3 und das Rücken von 18.5; die Weiche in
  `Bewegungsphase` ist ein `if` mit frühem `return` je Methode. Wächst `phasen/bewegung/__init__.py` (heute 10.248 Zeichen)
  über das Höchstmaß, geht das Gleiten aus `_gezeigt` nach
  `phasen/bewegung/anhaltenVorFremdenBases.py`.

Warum so (Versuch zu 10321, `/tmp/arch12985`): Die nächste *Stelle* liegt am Rand der freien
Fläche, also auf einem Lotpunkt oder einer Ecke; Wurzeln nur in den Kandidaten, das Urteil
exakt. 30 zufällige Lagen (25 *Modelle*, Spinne 60 mm): höchstens 19 ms, nie weiter als die
beste Stelle eines Rasters von 1/20″; mitten in 36 sich berührenden Boyz 40 ms, drei Flieger
166 ms. Ohne Vorfilter dauerte dieselbe Lage Minuten; nur im Loslassen gerechnet, nicht in V10.

Prüft wie im Querschnitt: MIV-3.1 und 3.2 an `ausgangslageLaden()` (K7). Am Dienst mit der
Spinne, denn nur V10 ändert seine Antwort: 18.1 über einem Necron Warrior gehalten, V10 200,
*Stelle* am Punkt, auch mit `zuvorX`, `zuvorY`, `angehaltenAufDemWeg`. An `Schlacht`, exakt
(rational, Radien in mm): 18.1 ebenso; 18.2 knapp neben der Mitte eines einzelnen Warriors
losgelassen (achsparallel versetzt): die *Stelle* frei und höchstens 1/100″ weiter als die
nächste freie; an der *Bewegungsweite* auf einem Warrior: die *Distanz* höchstens 6″; an der
*Spielfeldkante*: *ganz in* dem *Spielfeld*; neben dem Warboss: nicht in *Nahkampfreichweite*;
*Protokoll* unverändert. Warum der Warboss: eine *Einheit* aus einem *Modell*; ein einzelner
Boy verlöre auf dem Weg zur Spinne die *Kohärenz*. 18.3: durch die *Nahkampfreichweite* des
Warboss gezogen, Ende außerhalb: *Stelle* am Punkt; Ende darin, der Weirdboy davor an der
Strecke: nicht darin, `abstandHöchstens` 1+1/100″, außer der *Nahkampfreichweite* des
Weirdboys (ohne ihn hielte schon 6.2 an derselben *Stelle* an). 18.5: an der
*Bewegungsweite* angehalten, Punkt auf einem Warrior, übergangen: *Stelle* wie bei 18.2, ein
*Eintrag* mehr ohne *Grund*.
Am Bildschirm: Kreis der Spinne beim Halten über der fremden *Base*, nach dem Loslassen an
der *Stelle* des Spielstands; die Rechnung von 18.2 nur Unit-Tests zu `messen.py`.
