# Mockups der Bewegung: die ganze Einheit gekennzeichnet

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 9

## Runde 1
**Befund.** Wartet (Ich 3: Lücke abseits des Happy Path; die Kennzeichnung ist gebaut).
[bew-1](../../domaene/mockups/bew-1.html) und [bew-2](../../domaene/mockups/bew-2.html)
kennzeichnen nur einen Boy als *ausgewählt*. Gezogen werden aber alle zehn Boyz um 3″, also
ist die ganze *Einheit* die *Ebene* (AUF-20.6). Dann kennzeichnet die *Karte* jedes ihrer
*Modelle* (AUF-5.7, [Vertrag Bewegung](../../technik/architektur/vertrag/bewegung.md), V14).
Das Frontend macht es schon so: `technik/frontend/zeichnen.js`, Zeile 110, für jedes
*Modell* aus dem Spielstand.

**Kosten.** In beiden Mockups bekommen neun Kreise die Klasse `ausgewählt`. Bleibt es, sieht
der Stakeholder im Review mehr gekennzeichnete *Modelle* als im Mockup.

**Gegenvorschlag.** Alle zehn Kreise der Boyz (`spieler1`, `r="0.630"`) mit `ausgewählt`, in
bew-1 und bew-2. Gern schon früher, es ist billig.

**Stellungnahme.**
