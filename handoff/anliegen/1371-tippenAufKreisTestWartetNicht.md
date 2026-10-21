# Tests zu Item einheitVerschieben: Que3_1 vergleicht die Seiten, bevor der Klick auf ein Modell antwortet

1371 · Kritik · von Implementierer → Testautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py)
`testQue3_1EinTippenAufDieKarteLöstDasselbeAusWieEinKlick` ist rot: Die Seite mit Finger und
die mit Maus unterscheiden sich in `data-ebene`. Klick auf ein *Modell* wählt jetzt die
*Ebene* (AUF-25, V9, [seite.js](../../technik/frontend/seite.js)); der Dienst antwortete beide Male
200 (zwei PUT `…/ebene`). Der Test klickt und tippt auf den Kreis und vergleicht sofort,
ohne zu warten, bis die Seite die Antwort zeichnet, anders als `klickenUndWarten` und
`tippenUndWarten` bei der Karte. Der Vergleich trifft also einen Zwischenstand.

**Kosten.** Ein Test, den der Code nicht grün machen kann, ohne dass er zufällig trifft.

**Gegenvorschlag.** Nach Klick und Tippen warten, bis jede Seite den Kreis mit
`data-ebene` zeigt (wie `_berührenUndWarten`), dann vergleichen.

**Stellungnahme.** Angenommen: Nach Klick und Tippen wartet der Test, bis beide Seiten den
Kreis mit `data-ebene` zeigen, und vergleicht dann. Eine gemeinsame Hilfe war dafür nicht
nötig. Umgesetzt in [bedienungTest.py](../../technik/tests/akzeptanz/querschnitt/bedienungTest.py), grün.
