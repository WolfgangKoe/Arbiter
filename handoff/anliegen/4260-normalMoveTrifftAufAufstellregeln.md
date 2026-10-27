# Normal Move trifft auf die Regeln des Aufstellens

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Ich 3: eine *Sperre* greift zu Unrecht, Schritt 3 des Happy Path
fehlt am Bildschirm). [BEW-1.1](../../domaene/anforderungen/phasen/bewegung/normalMove.md)
lässt Arbiter nach AUF-8.2 *setzen*. Was beim *Setzen* sonst noch greift, ist nicht auf die
*Aufstellung* begrenzt:
1. [AUF-7.2](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md) sperrt
   ‚nicht wählbar‘, wenn jemand ein *Modell* einer *aufgestellten* *Einheit* *setzt* oder
   eines *Spielers* nicht *an der Reihe*; der Zweck von AUF-7 sperrt „jedes *Setzen* außer der
   Reihe“. In der *Bewegungsphase* ist jede *Einheit* *aufgestellt* und nach AUF-1.7 keiner
   *an der Reihe*: Wörtlich sperrt jedes Ziehen. BEW-2 nennt nur, was „außer nach QUE-1“ dazu
   kommt, nicht, was wegfällt.
2. Was die *Karte* beim Ziehen zeigt, regeln nur
   [AUF-26.5](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md) und
   [AUF-24.3](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md): an der *Stelle*
   nach AUF-26.1 bzw. 21.2, also in die eigene *Aufstellungszone* gerückt. BEW-1.1 rückt beim
   Loslassen nicht. Gilt AUF-26.5 in der *Bewegungsphase*, klebt ein *Modell* beim Ziehen an
   der Grenze der *Aufstellungszone* und springt beim Loslassen hinaus; gilt es nicht, sagt
   keine Anforderung, dass das *Modell* dem Zeiger folgt. In ArbiterMap folgt es ihm
   (`ArbiterMap/docs/spec/interaction_map.md:748`: außerhalb der Aufstellung hält nur die
   Feldkante an).
3. „bei der ganzen *Einheit* als *Ebene* nach AUF-21.1“ ist in Etappe 2 nicht erreichbar:
   AUF-21.1 setzt eine *Einheit in Aufstellung* voraus, die es nicht mehr gibt; eine *Ebene*
   hat nur eine *ausgewählte* *Einheit*; *ausgewählt* wird nach AUF-5.11 in der *Armeeliste*,
   die nur nicht *aufgestellte* *Einheiten* führt (Glossar), oder per Klick auf ein *Modell*
   nach AUF-20.6, das nach Anliegen 4220 erst zu Etappe 7 gehört; AUF-5.10 hebt die *Auswahl*
   beim *Aufstellen* auf. In ArbiterMap wählt ein Klick auf ein *Modell* die *Einheit* mit der
   ganzen *Einheit* als *Ebene*, ein Zug verschiebt sie als Block
   (`interaction_map.md:376`); die Etappe verlangt „Ziehen wie in ArbiterMap“.

**Kosten.** Ohne Klärung schreibt der Testautor Tests gegen eine Sperre, die den Happy Path
verhindert, oder der Implementierer entscheidet selbst; der Stakeholder sieht beim Ziehen
ein *Modell* an der Zonengrenze kleben. Ein Teil von BEW-1.1 lässt sich am Bildschirm nicht
abnehmen. Die Nachbesserung kostet zwei bis drei Sätze in BEW-1, die Tests sind noch nicht
geschrieben.

**Gegenvorschlag.**
1. BEW-1.1 nennt abschließend, was beim Loslassen prüft: nur QUE-1 und BEW-2, nicht AUF-3,
   AUF-7 und AUF-22, ohne in eine *Aufstellungszone* zu rücken.
2. Ein neues Kriterium in BEW-1: **Gegeben** die *Bewegungsphase*, **wenn** jemand ein
   *Modell* nach BEW-1.1 zieht und noch nicht loslässt, **dann** zeigt die *Karte* jedes
   gezogene *Modell* an der *Stelle*, an die BEW-1.1 es beim Loslassen dort *setzen* würde
   (Vorbild `interaction_map.md:748`).
3. Für die *Ebene* eins von beiden: (a) AUF-20.6 zu Etappe 2 ziehen, das Kriterium gibt es
   schon (ArbiterMap), und BEW-1.1 bezieht die ganze *Einheit* auf die *Ebene* der
   *ausgewählten* *Einheit* statt auf AUF-21.1; der Planer nimmt AUF-20.6 in Item normalMove.
   (b) Den Halbsatz streichen; in Etappe 2 zieht man *Modell* für *Modell*, der Block wartet.
   Empfehlung: (a), weil die Etappe Ziehen wie in ArbiterMap verlangt und eine *Einheit* mit
   zehn Boyz sonst zehn Züge je *Bewegungsphase* braucht.

**Stellungnahme.** Angenommen, alle drei, in
[BEW-1](../../domaene/anforderungen/phasen/bewegung/normalMove.md):
1. BEW-1.1 nennt abschließend: rückt nicht, es sperren nur QUE-1 und BEW-2.
2. Neu BEW-1.4: Die *Karte* zeigt beim Ziehen jedes *Modell* dort, wo BEW-1.1 es setzen würde.
3. (a): BEW-1.1 bezieht den Block auf die *Ebene*, nicht mehr auf AUF-21.1; AUF-20.6 endet mit
   `(Etappe 2)`. Ins Item normalMove nimmt es der Planer: [4281](4281-auf20_6InsItemNormalMove.md).
Gekürzt, damit BEW-1 unter 1.200 Zeichen bleibt: Den Satz zu QUE-4 und die Regelstelle `:434`
habe ich aus BEW-1.2 gestrichen, `:730` und QUE-5.5 belegen es. Aus BEW-1.3 ist „jedes ihrer
*Modelle* bleibt an seiner *Stelle*“ gestrichen; das sagte nichts, was nicht schon gilt.
