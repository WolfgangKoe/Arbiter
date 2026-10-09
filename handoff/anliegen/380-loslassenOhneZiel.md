# Loslassen ohne Ziel

380 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · offen
Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Der Architekt fragt in [378](378-ungeregelteFaelleBeimZiehenUndBeenden.md) F3, was
beim Loslassen geschieht, wenn keine Anforderung ein Ziel dafür kennt. Regeln und Ziel sagen
nichts. Geregelt ist bisher: ein *Modell* auf der *Karte* umsetzen
([AUF-8](../../domaene/anforderungen/phasen/aufstellen/ziehen.md)), auf die eigene *Ablage*
*zurücklegen*, eine *Einheit* aus der *Ablage* auf die *Karte* ziehen
([AUF-14](../../domaene/anforderungen/phasen/aufstellen/restDerEinheit.md)). Ein *Modell* einer
*aufgestellten* *Einheit* auf eine *Ablage* gezogen ist *Sperre* ‚nicht wählbar‘ (AUF-8.4); was
gezogen wurde, kommt dann an seinen alten Ort zurück
([AUF-12.2](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md)).

**Kosten.** Bis zur Antwort fehlt für diese Fälle ein Kriterium. Dann entscheidet der
Implementierer, und kein Test hält es fest.

**Gegenvorschlag.**

**F1 · Nichts zu tun.** Du ziehst die Boyz aus der *Ablage* auf die *Karte*, obwohl alle zehn
schon *gesetzt* sind; die *Ablage* zeigt sie noch (AUF-4.3). Oder du lässt eine *Einheit* oder
ein *Modell* neben *Karte* und *Ablagen* los.
- A: Was du gezogen hast, kommt an seinen alten Ort zurück, ohne Meldung.
- B: wie A, dazu *Sperre* ‚nicht wählbar‘ mit *Grund*.

Empfehlung: A. Hier ist nichts regelwidrig, es gibt nur kein Ziel.

Antwort: .

**F2 · Falsche Ablage.** Ein *Modell* der *Einheit in Aufstellung* lässt du auf der *Ablage* des
anderen *Spielers* los.
- A: wie F1 A: Es kommt an seinen alten Ort zurück, ohne Meldung.
- B: *Sperre* ‚nicht wählbar‘, wie bei AUF-8.4; das *Modell* kommt an seinen alten Ort zurück,
  und Arbiter nennt den *Grund* bis zur nächsten Handlung (AUF-12.3).

Empfehlung: B. Ein eigenes *Modell* in der *Ablage* des Gegners ist nicht erlaubt, und „was
nicht erlaubt ist, wird gesperrt“ ([Ziel](../../domaene/ziel.md)). Bei AUF-8.4 hast du denselben
Fall schon so entschieden.

Antwort: .

**Stellungnahme.**
