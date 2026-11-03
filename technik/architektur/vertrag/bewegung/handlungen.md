# Vertrag: Bewegung · Handlungen

Abschnitt der *Bewegungsphase* der *Schlacht* (BEW-1 bis BEW-4, Anliegen 5180 F5 bis F7),
die anderen: [Architektur](../../../architektur.md#schichten); Tür und Übergang:
[Schlacht](../schlacht/tuer.md), was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
*Modell* auf der *Karte* loslassen (BEW-1.5, BEW-3, BEW-17, QUE-10.5) | `PUT …/modelle/<m>/stelle`, `{"x": 39.5, "y": 30}` | `modellLoslassen`
„Phase beenden“ in der *Bewegungsphase* (BEW-4) | `PUT /api/phaseBeenden` ([V13](../schlacht/handlungen.md)) | `phaseBeenden`

- **V15** In der Domäne: Ob der Block oder ein *Modell* geht, entscheidet die *Ebene*
  (BEW-1.5, AUF-20.4), nicht die Seite. Jede *Einheit* des *Spielers* *am Zug* zieht in der
  *Bewegungsphase* beliebig oft, in beliebiger Reihenfolge, auch zurück (BEW-1.6); es gibt
  keine *Einheit in Bewegung*. Die *Distanz* ist die gerade Strecke von der *Stelle* zu
  Beginn der *Bewegungsphase* zur jetzigen, verglichen als Quadrat (S2, Anliegen 5400 F1 A).
  Jeder *Grund* aus QUE-1 wirft `Sperre` in der Reihenfolge von `Grund` (V6). Vor fremden
  *Bases* hält es an ([Ziehen](ziehen.md)); `Grund.überEineBase` entfällt (BEW-17.1).
- **V16** Anhalten an der *Bewegungsweite* (BEW-3.1): Stünde ein *Modell* der *Ebene* an der
  gezogenen *Stelle* weiter als seine *Bewegungsweite*, kürzt `modellLoslassen` den Zug auf
  der geraden Strecke von der vorigen zur gezogenen *Stelle*, für alle *Modelle* der *Ebene*
  um denselben Anteil: das größte k/n (n wie S3), bei dem jedes höchstens seine
  *Bewegungsweite* steht, exakt nachgeprüft (S2), in
  `phasen/bewegung/anhaltenAnDerBewegungsweite.py`. So hält der Block, sobald eines seine
  *Bewegungsweite* erreicht, höchstens 1/100″ davor. Ebenso hält er vor dem ersten Schritt,
  an dem eine *Base* nicht *ganz in* dem *Spielfeld* läge (BEW-6.1) oder ein *Modell* in
  *Nahkampfreichweite* eines des anderen *Spielers* käme (6.2); es gilt der früheste der drei
  (6.3). Diese Grenzen in `phasen/bewegung/anhaltenVorDerGrenze.py`. Steht schon an der
  vorigen *Stelle* ein *Modell* der *Ebene* über seiner *Bewegungsweite* oder in
  *Nahkampfreichweite* und ist der Weg nicht 0, ist deren Anteil 0 (BEW-25.1). Erst danach
  prüft QUE-1 die gekürzten *Stellen*. Anhalten ist kein *Grund*: 200.
  Ein *Modell* des anderen *Spielers* *setzt* nichts: V10 leer, V5 200 (BEW-10.1).
- **V17** `phaseBeenden` in der *Bewegungsphase*: Ist eine *Einheit* des *Spielers* *am Zug*
  nicht in *Kohärenz*, `Sperre` ‚keine Kohärenz‘ (BEW-4.1, QUE-5.5), die *Phase* bleibt (D2);
  409 mit `gründe` wie [sperre.json](../sperre.json). `Schlacht` lässt das die Regeln in
  `phasen/bewegung/` prüfen (V11).
- Spielstand: kein eigener Schlüssel; die *Stellen* stehen in `modelle` (V1).

Prüft wie im Querschnitt: Loslassen über der *Bewegungsweite* hält nach V16, 200, die
*Stellen* danach gleich denen, die V10 am selben Punkt nannte; Korrigieren einer schon
gezogenen *Einheit* zählt ab der *Stelle* zu Beginn der *Bewegungsphase*; V17 mit 409 und
unveränderter *Phase*, am Dienst und am Bildschirm.
