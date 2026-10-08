# AUF-5.5 regelt einen Fall, den die Ausgangslage ausschließt

318 · Kritik · von Fachkritiker (Domäne) → Anforderungsautor · Runde 1/3 · angenommen

## Runde 1
**Befund.** AUF-5.5 ([Aufstellen](../../domaene/anforderungen/phasen/aufstellen.md)) regelt,
was geschieht, wenn AUF-5.3 eine dritte *Einheit* desselben *Spielers* *ausgewählt* macht. Die
*Ausgangslage* hat je *Armee* genau zwei *Einheiten* (AUF-2.6,
[ausgangslage.yaml](../../domaene/daten/ausgangslage.yaml): Boyz, Warboss; Necron Warriors,
Overlord), und eine andere *Ausgangslage* kennt Etappe 1 nicht. Der Deckel „zwei je *Spieler*“
aus 309 F2 B (git) fällt damit mit „alle *Einheiten* des *Spielers*“ zusammen; eine dritte gibt
es nicht. Das Mockup [auf-5.html](../../domaene/mockups/auf-5.html) kann den Fall deshalb nicht
zeigen, und der Stakeholder sieht ihn in Review 4 nicht. Auch die Begründung in 309 Runde 3
(git), man könne eine *aufgestellte* *Einheit* abwählen, „indem ihr zwei andere *Einheiten*
desselben *Spielers* auswählt“, trägt in Etappe 1 nicht: Nach dem Aufstellen hat der *Spieler*
nur noch eine. Die übrigen Kriterien von Item 2 und Item 1 treffen die Mockups.

**Kosten.** Item 2 ([Auswählen in der Ablage](../../domaene/items/auswaehlenInDerAblage.md))
nennt AUF-5.5 im Umfang. Der Akzeptanztest dazu braucht eine *Armee* mit drei *Einheiten*, die
es nach AUF-2.6 nicht gibt: Der Testautor müsste sie erfinden, oder der Test bleibt rot, ohne
dass ein Bildschirmtest oder der Stakeholder den Fall je erreicht. Code dafür ist in Etappe 1
toter Zweig.

**Gegenvorschlag.** Eine Entscheidung, die ich nicht treffe; ich bitte dich, sie dem
Stakeholder vorzulegen (Fragen-Anliegen, Kosten wie oben):
- A: AUF-5.5 bleibt in Item 2; das Kriterium nennt, dass sein Test eine *Armee* außerhalb der
  *Ausgangslage* verwendet.
- B: AUF-5.5 bleibt in der Anforderung, kommt aber aus Item 2 heraus, bis eine *Ausgangslage*
  eine *Armee* mit mehr als zwei *Einheiten* hat (Planer zieht Item 2 nach).
- C: AUF-5.5 entfällt; ein Deckel wird gefragt, wenn eine *Armee* mehr als zwei *Einheiten* hat.

Erledigt, wenn AUF-5.5 und Item 2 der Antwort entsprechen.

**Stellungnahme.** Befund geteilt, auch zu meiner Begründung in 309 Runde 3; die trägt seit
AUF-5.10 ohnehin nicht mehr. Die Frage liegt dem Stakeholder in
[320](320-deckelDerAuswahlOhneDritteEinheit.md) vor, mit Empfehlung B. Nach seiner Antwort
passe ich AUF-5.5 an (A, C) oder bitte den Planer, Item 2 nachzuziehen (B).
Der Stakeholder hat B gewählt (320, git). AUF-5.5 bleibt deshalb unverändert. (Planer) AUF-5.5
ist aus dem Umfang von Item 2 und aus Plan 4 genommen; die Bedingung oben ist erfüllt. Laut
Entscheidung des Stakeholders steht dafür kein `· wartet auf` im Kopf.
