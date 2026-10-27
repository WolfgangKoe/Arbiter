# Vertrag: Bewegung

Die *Bewegungsphase* der *Schlacht* (BEW-1 bis BEW-4, Anliegen 5180 F5 bis F7) und der Klick auf
ein *Modell* (AUF-20.6); Tür und Übergang: [Schlacht](schlacht.md), was alle Phasen teilen:
[Querschnitt](querschnitt.md).

## Auswahl
- **V14** `PUT …/modelle/<m>/anklicken` (`…` wie V5) → `modellAnklicken(modell)`, 200 mit
  dem Spielstand, in der *Aufstellung* an `Aufstellung`, danach an `Schlacht` (V11): Die
  *Einheit* des *gesetzten* *Modells* ist *ausgewählt* mit der ganzen *Einheit* als *Ebene*
  und keine andere, gleich wer *an der Reihe* oder *am Zug* ist (AUF-20.6). Ist sie schon
  *ausgewählt*, das *Modell* nicht *gesetzt* oder in der *Aufstellung* seine *Einheit* schon
  *aufgestellt* (Annahme aus Anliegen 5181 F1 A, wie V3), ändert es nichts, ohne `Sperre` (V5). Wie
  V3 ist es keine Handlung: ohne D2. Warum eine eigene Route statt V2: V2 nimmt nur eine
  *Einheit* der *Armeeliste* (404), in der *Schlacht* ist jede leer.
- Spielstand: `ausgewählt` an jedem *Modell* der *ausgewählten* *Einheit* (AUF-5.7). AUF-25
  gilt nur in der *Aufstellung*: in der *Schlacht* kein `ebene`; V9 bleibt bei der
  *Aufstellung* und antwortet 404, denn dort ist keine *Einheit* mehr *ausgewählt* (AUF-5.10).

## Handlungen
Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
*Modell* auf der *Karte* loslassen (BEW-1.5, BEW-2, BEW-3, QUE-10.5) | `PUT …/modelle/<m>/stelle`, `{"x": 39.5, "y": 30}` | `modellLoslassen`
„Phase beenden“ in der *Bewegungsphase* (BEW-4) | `PUT /api/phaseBeenden` (V13) | `phaseBeenden`

- **V15** In der Domäne: Ob der Block oder ein *Modell* geht, entscheidet die *Ebene*
  (BEW-1.5, AUF-20.4), nicht die Seite. Jede *Einheit* des *Spielers* *am Zug* zieht in der
  *Bewegungsphase* beliebig oft, in beliebiger Reihenfolge, auch zurück (BEW-1.6); es gibt
  keine *Einheit in Bewegung*. Die *Distanz* ist die gerade Strecke von der *Stelle* zu
  Beginn der *Bewegungsphase* zur jetzigen, verglichen als Quadrat (S2, Anliegen 5400 F1 A).
  Jeder *Grund* aus QUE-1 und BEW-2.5 wirft `Sperre` in der Reihenfolge von `Grund` (V6,
  BEW-2.6); fremd nach AUF-29.3 (BEW-2.5, 2.7).
- **V16** Anhalten an der *Bewegungsweite* (BEW-3.1): Stünde ein *Modell* der *Ebene* an der
  gezogenen *Stelle* weiter als seine *Bewegungsweite*, kürzt `modellLoslassen` den Zug auf
  der geraden Strecke von der vorigen zur gezogenen *Stelle*, für alle *Modelle* der *Ebene*
  um denselben Anteil: das größte k/n (n wie S3), bei dem jedes höchstens seine
  *Bewegungsweite* steht, exakt nachgeprüft (S2), in
  `phasen/bewegung/anhaltenAnDerBewegungsweite.py`. So hält der Block, sobald eines seine
  *Bewegungsweite* erreicht, höchstens 1/100″ davor. Erst danach
  prüfen QUE-1 und BEW-2.5 die gekürzten *Stellen*. Anhalten ist kein *Grund*: 200.
- **V17** `phaseBeenden` in der *Bewegungsphase*: Ist eine *Einheit* des *Spielers* *am Zug*
  nicht in *Kohärenz*, `Sperre` ‚keine Kohärenz‘ (BEW-4.1, QUE-5.5), die *Phase* bleibt (D2);
  409 mit `gründe` wie [sperre.json](sperre.json). `Schlacht` lässt das die Regeln in
  `phasen/bewegung/` prüfen (V11).
- Spielstand: kein eigener Schlüssel; die *Stellen* stehen in `modelle` (V1).

## Ziehen
V10 in jeder *Phase* der *Schlacht*: `stellenBeimLoslassen(modell, stelle)` nennt jedes
*Modell*, das `modellLoslassen` dort *setzen* würde (BEW-1.7), mit Anhalten an der *Bewegungsweite* (V16),
ohne Hineinrücken, mit denselben Wächtern und *Gründen*: bei einer *Sperre* 409, die *Karte*
zeigt weiter die letzte 200 dieses Zugs. Außerhalb der *Bewegungsphase* ist die Antwort 200
mit leerem `modelle[]` (QUE-10.5). Warum 409: BEW-1.5 *setzt* nur ohne *Sperre*; die *Karte*
zeigt keine *Stelle*, an die nichts *gesetzt* würde.

## Seite
- Klick (V8) auf ein *Modell*: in der *Schlacht* V14; in der *Aufstellung* V9 auf einem der
  *Einheit*, die in der *Armeeliste* `ausgewählt` trägt, sonst V14
  ([Aufstellen](aufstellen.md#seite)). Im *Spielfeld* außerhalb eines *Modells*: in der
  *Schlacht* nichts.
- Zug (V8, V10): Trägt das gezogene *Modell* `ausgewählt`, folgen alle mit `ausgewählt`;
  Loslassen im *Spielfeld* V5, daneben nach V10.
- Knöpfe (V7): nur „Phase beenden“ ([Schlacht](schlacht.md#seite)); auf 409 die
  `sperrmeldung` wie bei jeder Handlung.

Prüft wie im Querschnitt: Loslassen über der *Bewegungsweite* hält nach V16, 200, die *Stellen* danach
gleich denen, die V10 am selben Punkt nannte; Korrigieren einer schon gezogenen *Einheit*
zählt ab der *Stelle* zu Beginn der *Bewegungsphase*; V17 mit 409 und unveränderter
*Phase*, am Dienst und am Bildschirm; V14 mit `einheitJederSeite`; V10 außerhalb der
*Bewegungsphase* leer.
