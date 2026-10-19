# Der Test aus 622 prüft nach Item 1 die Zugschwelle nicht mehr

977 · Kritik · von Architekt → Reviewer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: hält auf. Ein Test prüft dann sein Kriterium nicht.
Der Gegenvorschlag in [622](622-zugschwelleUngeprueft.md) prüft die Zugschwelle an einer
Karte der *Ablage*: drücken, 3 Pixel bewegen, loslassen. [Plan 6](../plan.md) setzt 622 vor
Item 1. Aber Item 1 ([Setzen per Klick](../../domaene/items/setzenPerKlick.md)) streicht
jedes Ziehen einer *Einheit* (AUF-8.5, 8.6, 16.1, 16.4, 16.5 entfallen). Danach kann man die
Karte in der *Ablage* nur noch anklicken. Setzt jemand `zugschwelle` auf 0, wählt der Test sie
trotzdem aus und bleibt grün. Damit lässt sich 622 nach Item 1 nicht mehr erfüllen
(„dieselbe Probeänderung macht den Test rot“). Die Schwelle zählt dann nur noch beim *Modell*
auf der *Karte*. Mit Item 2 („Ganze Einheit“, AUF-21.1) verschiebt ein Zittern um ein Pixel
die ganze *Einheit*.

**Kosten.** Ein Test vor Item 1 wird mit Item 1 wertlos oder fällt weg. Die Zugschwelle bleibt
dann ohne Test, genau dort, wo sie nach Item 2 am meisten bewirkt.

**Gegenvorschlag.** Fasse den Test in 622 für das *Modell* auf der *Karte*: ein *gesetztes*
*Modell* mit Maus und Finger drücken (B5), 3 Pixel bewegen, loslassen. Erwartet: keine
Handlung an den Server, das *Modell* steht wie vorher. Das geht schon heute (V8: ohne Zug
geschieht auf einem *Modell* nichts) und gilt auch nach Item 1. Die Reihenfolge im Plan
bleibt.

Erledigt, wenn 622 die Zugschwelle am *Modell* auf der *Karte* prüft.

**Stellungnahme.** Umgesetzt in [622](622-zugschwelleUngeprueft.md), Kosten und
Gegenvorschlag: Der Test drückt ein *gesetztes* *Modell* auf der *Karte* mit Maus und Finger
(B5), bewegt es um 3 Pixel und lässt los, mit dem vorhandenen `ziehenOhneAnfrage`; erwartet:
keine Handlung an den Server, jedes *Modell* an seiner *Stelle* wie vorher. Nachgelesen in
`technik/frontend/seite.js`: Mit Schwelle 0 beginnt der Zug schon beim ersten Pixel, und
`modellLoslassen` schickt die neue *Stelle*; der Test würde also rot. Nach Item 1 gilt er
weiter, denn AUF-18.1 nimmt den Klick auf ein *Modell* aus. Der Link auf V8 in 622 zeigt jetzt
auf `handlungen.md`. Die Reihenfolge im Plan bleibt.
