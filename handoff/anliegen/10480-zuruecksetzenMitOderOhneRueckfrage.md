# Einheit zurücksetzen: mit oder ohne Rückfrage?

Form: Fragen
Von: Anforderungsautor
An: Stakeholder
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Du hast in 2364 F4 A entschieden, dass man eine gezogene *Einheit* bis zum Ende
der *Bewegungsphase* zurücksetzen kann, nicht wie. [BEW-24](../../domaene/anforderungen/phasen/bewegung/einheitZuruecksetzen.md)
und das Mockup [bew-24](../../domaene/mockups/bew-24.html) zeigen „Einheit zurücksetzen“ als
Knopf unter der *Karte*: Ein Klick, und jedes *Modell* steht wieder, wo es zu Beginn der Phase
stand. ArbiterMap fragt nach: Auf der Karte der *ausgewählten* *Einheit* steht „Zurücksetzen
(…″)“ mit der gezogenen Strecke; der Klick öffnet einen Dialog mit Skizze von alter und neuer
*Stelle* je *Modell*, erst „Bestätigen“ setzt zurück, „Abbrechen“ lässt alles stehen
(`ArbiterMap/frontend/CLAUDE.md:350`). Eine Abweichung vom Vorbild entscheidest du
([DoR 6](../../prozess/ablauf/dor.md)); der Fachkritiker hat sie in
[10400](10400-zuruecksetzenOhneRueckfrage.md) gefunden.

**Kosten.** A: nichts, BEW-24 und bew-24 bleiben, Item
[zuruecksetzenUndLuecken](../../domaene/items/zuruecksetzenUndLuecken.md) baut es in Zyklus 10.
B: ein Kriterium für den Dialog, ein Mockup und ein Test mehr, nach dem Fachkritiker erst in
Zyklus 11; bis dahin siehst du im Review 10 den Klick ohne Rückfrage.

**Gegenvorschlag.**
**F1 · Wie setzt man eine gezogene Einheit zurück?**
A: Ein Klick auf „Einheit zurücksetzen“ unter der *Karte*, ohne Rückfrage, wie „Einheit zurücklegen“ (AUF-23) und „Vorrücken zurücknehmen“ (BEW-12) (Anliegen 2220, 7000).
B: Wie ArbiterMap: Knopf mit der gezogenen Strecke auf der Karte der *Einheit*, Dialog mit Skizze, „Bestätigen“ oder „Abbrechen“ (ArbiterMap).
Empfehlung: A, gleiche Bedienung wie die beiden anderen Rücknahmen, und ein Fehlklick kostet nichts: Die *Einheit* zieht man neu.
Annahme: BEW-24 und bew-24 bleiben, wie sie sind; mit deiner Antwort schreibe ich sie als Quelle an BEW-24.1.
Antwort: A

**Stellungnahme.**
