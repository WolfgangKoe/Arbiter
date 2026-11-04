# Angebot rechnet das Ziehen noch einmal

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.** `Schlacht.modellLoslassen` (`technik/arbiter/domaene/querschnitt/schlachtrunden.py`)
ruft `_stellenMitGründen` (in der *Bewegungsphase* `stellenMitGründenNachDemZiehen`) und
danach `Bewegungsphase.angebotNachDemZiehen` mit denselben sechs Eingaben; beide rechnen `_gezeigt` ganz durch, also das Gleiten zweimal je Loslassen.
`angebotNachDemZiehen` und `_gezeigt` brauchen dafür je ein `# noqa: PLR0913`. Der
Gegenvorschlag von 12700 Punkt 2 war, dass das Ergebnis des Ziehens mitgibt, ob BEW-3.1 oder
6.2 anhielt.

**Kosten.** Zwei Aufrufe, die übereinstimmen müssen, und eine Signatur, die mit jedem Item
wächst (wie 12681 Punkt 2).

**Gegenvorschlag.** `Gezeigt` (oder das Ergebnis von `stellenMitGründenNachDemZiehen`) trägt,
ob an der *Bewegungsweite* oder *Nahkampfreichweite* angehalten wurde; die *Schlacht* legt
damit das Angebot an, `angebotNachDemZiehen` nimmt `ebene`, `gezogenes`, `ziel` und diesen
Wert. Zusammen mit 12681 umsetzen.

**Stellungnahme.**
