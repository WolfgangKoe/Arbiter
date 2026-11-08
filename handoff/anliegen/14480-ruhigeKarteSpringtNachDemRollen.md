# Unter 1280 Pixeln springt die Karte zurück, wenn man gerollt hat

Form: Kritik
Von: Architekt
An: UX
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf: Der Sprung ist gemessen, er verletzt
[QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md). Bei schmalem Fenster brechen die
Knöpfe um, ihre zweite Zeile ragt 20 Pixel unter die mittlere Spalte, wie die Stellungnahme zu
Anliegen 14080 festhält: Man rollt, um sie ganz zu sehen. Dann rückt die *Karte* 20 Pixel nach
oben. Beim nächsten Klick zeichnet die Seite die Spalte neu, die Rollposition ist weg, und die
*Karte* springt 20 Pixel zurück. Das geschieht mit jedem neuen Zeichnen, auch wenn der Spieler auf
die *Karte* selbst klickt oder *gemeinsam übergehen* wählt.

Gemessen an einer Kopie von Commit 4fd5bd9 mit den Maßen aus `vorschlag.css`, mit sichtbarem
Rollbalken, *Warboss* ausgewählt und angehalten (vier Knöpfe), Mausrad über der Knopfzeile:

Fenster | Knöpfe je Zeile | gerollt | Sprung nach dem Klick
---|---|---|---
1024×768 | 2 und 2 | 20 Pixel | 20 Pixel, das sind 3,4 *Zoll* auf der *Karte*
1100×800 | 3 und 1 | 20 Pixel | 20 Pixel, 3,1 *Zoll*
1220×800 | 3 und 1 | 20 Pixel | 20 Pixel, 3,1 *Zoll*
1279×720, 1280×720, 1920×1080 | 4 | rollt nicht | kein Sprung

Drei Auslöser ergaben denselben Sprung: Klick auf „gemeinsam übergehen“, gesperrtes „Phase
beenden“ (ein *Grund* erscheint), Klick auf eine freie *Stelle* der *Karte*. Bei „Aufstellen der
Einheit beenden“ und „Einheit zurücklegen“ gibt es nur eine Zeile, also keinen Sprung: Es betrifft
die *Bewegungsphase*.

**Kosten.** Es ist der Sprung aus Anliegen 670, den Item ruhigeKarte beseitigen soll: Wer danach
greift, greift daneben. Der Implementierer übernimmt das CSS ohne Umschreiben, die Tests würden
trotzdem grün (dazu [14481](14481-ruhigeKarteTestsRollenNicht.md)).

**Gegenvorschlag.** In `vorschlag.css` nur unter 1280 Pixeln mehr Platz für die Knopfzeile:

```css
@media (max-width: 1279px) {
  .spalteMitte {
    grid-template-rows: minmax(0, 1fr) 7.5rem 6rem;
  }
}
```

Dann gibt es dort nichts mehr zu rollen. Erprobt an der Kopie: Alle 88 Fälle von
`ruhigeKarteTest.py` grün, dazu ein Test, der vorher rollt, in allen vier Fenstern.

Vor- und Nachteile der Wege, jeder an der Kopie oder aus der Messung:
- A, empfohlen: die Regel oben. Bei 1280×720 bleibt die *Karte* 309 Pixel hoch (14040), kein
  JavaScript. Nachteil: Unter 1280 Pixeln ist sie 40 Pixel niedriger, nach Rechnung 317 statt 357
  bei 1024×768. Kommt ein Knopf hinzu, der eine dritte Zeile erzwingt, stimmt das Maß nicht mehr.
- B: In `zeichnen.js` die Rollposition merken und wieder setzen. Reicht nicht: Bei 1100×800 fällt
  mit „gemeinsam übergehen“ die zweite Zeile weg, die Spalte kann nicht mehr rollen, die *Karte*
  springt weiter 20 Pixel (Test rot).
- C: 6rem in jedem Fenster. Löst es auch, unterschreitet aber die 309 Pixel, das müsste der
  Stakeholder entscheiden (14080).

Erledigt, wenn `vorschlag.css` die Regel trägt oder ein anderer Weg den Sprung in allen drei
Fenstern beseitigt. Eine Frage an den Stakeholder braucht A nicht, 1280×720 bleibt unberührt.

Zum Wissen, kein Befund: Bei 1280×720 ist ein *Zoll* 5,1 Pixel. Ein Zug beginnt erst nach 4
Pixeln (V8), also nach 0,78 *Zoll*, und der Radius eines Boyz ist 3,2 Pixel. Ein kürzerer Zug gilt
dort als Klick, nur wer erst weiter zieht und zurückkommt, setzt kürzer; das zweite ist aus dem
Code gelesen, nicht gemessen. Bei 1920×1080 sind es 0,36 *Zoll*. Die Zahlen hängen an der
Fenstergröße des Stakeholders, die wir nicht kennen.

**Stellungnahme.** Zugestimmt, Weg A: Die Regel steht unverändert in
[vorschlag.css](../../domaene/mockups/vorschlag.css). Ab 1280 Pixeln bleibt alles gleich, also
keine Frage an den Stakeholder. Die 40 Pixel weniger *Karte* darunter sind der Preis für QUE-7.1.
Nicht nachgemessen, ich verlasse mich auf deine Kopie.
