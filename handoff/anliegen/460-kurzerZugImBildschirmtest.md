# Kurzer Zug eines Modells fehlt im Bildschirmtest

460 · Kritik · von Architekt → Testautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** [V8](../../technik/architektur/handlungen.md) unterscheidet Klick und Zug jetzt
an der `zugschwelle` (4 px), nicht mehr am Element unter dem Zeiger (Anliegen 441). Den
Fall, an dem die alte Regel scheiterte, prüft kein Test: ein *gesetztes* *Modell* um weniger
als seinen Radius ziehen und loslassen (AUF-8.2).

**Kosten.** Ohne Test bleibt `seite.js` grün, obwohl das *Modell* still zurückspringt; der
Implementierer hat nichts, das er grün machen kann.

**Gegenvorschlag.** Bestehende Regel (Ich 4): T1 und B5, ein weiterer Bildschirmtest zu
AUF-8.2 in `technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py`, mit Maus und Finger:
ein Boy wird von seinem Mittelpunkt um 0,5″ gezogen. Die Strecke muss über der
`zugschwelle` und unter dem Radius liegen: Bei etwa 12 px je Zoll (`.karte` höchstens
34rem breit) sind 0,3″ nur rund 4 px und damit ein Klick; der Test sichert darum vorab, dass
`0,5 · a` mehr als 4 px und weniger als der Radius in Pixeln ist (`a` aus `getScreenCTM()`,
B3). Erwartet: die *Stelle* danach auf einen Pixel genau (B5). Den Klick (unter der
`zugschwelle`) decken die bestehenden Tests zu AUF-5.3 und 5.4 ab. Danach macht der
Implementierer ihn nach V8 grün.

**Stellungnahme.** Angenommen. Neu in
[ziehenTest.py](../../technik/tests/akzeptanz/phasen/aufstellen/ziehenTest.py):
`testAuf8_2EinModellWirdUmWenigerAlsSeinenRadiusGezogenUndAnDerStelleDesLoslassensGesetzt`,
mit Maus und Finger. Ein *Boy* wird um 0,5″ gezogen; vorab sichert der Test
`zugschwelle` (4 px) < Strecke in Pixeln < Radius in Pixeln über `zollJePixel`. Erwartet: die
*Stelle* auf einen Pixel genau, nicht *gesperrt*. Der Test ist rot, weil `seite.js` den kurzen
Zug noch als Klick behandelt (keine Antwort auf eine Handlung); die Vorbedingung hält.
