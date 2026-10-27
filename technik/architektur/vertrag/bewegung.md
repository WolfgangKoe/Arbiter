# Vertrag: Bewegung

Die *Bewegungsphase* der *Schlacht* (BEW-1, BEW-2) und der Klick auf ein *Modell*
(AUF-20.6); Tür und Übergang: [Schlacht](schlacht.md), was alle Phasen teilen:
[Querschnitt](querschnitt.md).

## Auswahl
- **V14** `PUT …/modelle/<m>/anklicken` (`…` wie V5) → `modellAnklicken(modell)`, 200 mit
  dem Spielstand, in der *Aufstellung* an `Aufstellung`, danach an `Schlacht` (V11): Die
  *Einheit* des *gesetzten* *Modells* ist *ausgewählt* mit der ganzen *Einheit* als *Ebene*
  und keine andere, gleich wer *an der Reihe* oder *am Zug* ist (AUF-20.6). Ist sie schon
  *ausgewählt* oder das *Modell* nicht *gesetzt*, ändert es nichts, ohne `Sperre` (V5). Wie
  V3 ist es keine Handlung: ohne D2. Warum eine eigene Route statt V2: V2 nimmt nur eine
  *Einheit* der *Armeeliste* (404), in der *Schlacht* ist jede leer.
- Spielstand: `ausgewählt` an jedem *Modell* der *ausgewählten* *Einheit* (AUF-5.7). AUF-25
  gilt nur in der *Aufstellung*: in der *Schlacht* kein `ebene`; V9 bleibt bei der
  *Aufstellung* und antwortet 404, denn dort ist keine *Einheit* mehr *ausgewählt* (AUF-5.10).

## Handlungen
Am Bildschirm | Anfrage (V5) | `Schlacht`
---|---|---
*Modell* auf der *Karte* loslassen (BEW-1.1, BEW-2, QUE-10.5) | `PUT …/modelle/<m>/stelle`, `{"x": 39.5, "y": 30}` | `modellLoslassen`
„Bewegung der Einheit beenden“ (BEW-1.2, 1.3) | `PUT /api/bewegungDerEinheitBeenden` | `bewegungDerEinheitBeenden`

- **V15** In der Domäne: Ob der Block oder ein *Modell* geht, entscheidet die *Ebene*
  (BEW-1.1, AUF-20.4), nicht die Seite; die *Distanz* zählt die Domäne ab den *Stellen* zu
  Beginn der *Bewegungsphase* (Glossar, S2). Jeder *Grund* aus QUE-1 und BEW-2 wirft
  `Sperre` in der Reihenfolge von `Grund` (V6, BEW-2.3); fremd nach AUF-29.3 (BEW-2.2, 2.4).
  Ohne *Einheit in Bewegung* ändert `bewegungDerEinheitBeenden` nichts, ohne `Sperre` (V5).
- Spielstand: `schlacht.einheitInBewegung` ([Schlacht](schlacht.md#spielstand)) nennt
  `spieler` und `einheit` wie `einheitInAufstellung` oder ist `null`.

Beispiele (V6), nur die genannten Schlüssel: [bewegung.json](bewegung.json): `schlacht` nach
den Anfragen von [schlacht.json](schlacht.json), dann
`PUT /api/spieler/1/einheiten/2/modelle/1/stelle` 3″ weiter in x (Warboss, BEW-1.1).
[weiterAlsB.json](weiterAlsB.json): `gründe` derselben Anfrage, aber weiter als sein *B*
(BEW-2.1); `spielstand` gleich dem davor.

## Ziehen
V10 in jeder *Phase* der *Schlacht*: `stellenBeimLoslassen(modell, stelle)` nennt jedes
*Modell*, das `modellLoslassen` dort *setzen* würde (BEW-1.4), ohne Hineinrücken und
Anhalten (BEW-1.1), mit denselben Wächtern und *Gründen*: bei einer *Sperre* 409, die
*Karte* zeigt weiter die letzte 200 dieses Zugs. Außerhalb der *Bewegungsphase* ist die
Antwort 200 mit leerem `modelle[]` (QUE-10.5). Warum 409: BEW-1.1 *setzt* nur ohne *Sperre*;
die *Karte* zeigt keine *Stelle*, an die nichts *gesetzt* würde.

## Seite
- Klick (V8) auf ein *Modell*: in der *Schlacht* V14; in der *Aufstellung* V9 auf einem der
  *Einheit*, die in der *Armeeliste* `ausgewählt` trägt, sonst V14
  ([Aufstellen](aufstellen.md#seite)). Im *Spielfeld* außerhalb eines *Modells*: in der
  *Schlacht* nichts.
- Zug (V8, V10): Trägt das gezogene *Modell* `ausgewählt`, folgen alle mit `ausgewählt`;
  Loslassen im *Spielfeld* V5, daneben nach V10.
- Knöpfe (V7), Mockups bew-1, bew-2: „Bewegung der Einheit beenden“ vor „Phase beenden“,
  wenn `einheitInBewegung` nicht `null` ist.

Prüft wie im Querschnitt: 200 nach dem Loslassen gleich `bewegung.json`, 409 gleich
`weiterAlsB.json`; V14 mit `einheitJederSeite`; V10 außerhalb der *Bewegungsphase* leer.
