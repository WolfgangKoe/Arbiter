# Eine Base ist nie überdeckt, auch nicht nach dem Übergehen

Form: Kritik
Von: Planer
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** Hält den Happy Path nicht auf, betrifft Etappe 7. Der Stakeholder hat in
[16100](16100-sperreNachDemUebergehenBisEtappe7.md) entschieden: Eine *Base* darf nie eine
andere *überdecken*, auch nicht, nachdem die *Spieler* *gemeinsam übergehen* gewählt haben;
die Anforderungen enthalten hier einen Fehler.

Die Anforderungen lassen eine überdeckte *Base* an einer Stelle zu: Passt eine *Formation*
nirgends in die eigene *Aufstellungszone*, ohne eine *Base* zu *überdecken*, stellt Arbiter
sie trotzdem auf und markiert die überdeckenden *Modelle* rot
([AUF-27.1, AUF-27.2](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md)).
Das geht auf seine Antwort C in Anliegen 992 (F1) zurück; Antwort A dort hätte die
*Formation* gar nicht aufgestellt. Er hat sich also jetzt anders entschieden als damals.
Davon hängen ab:
- [BEW-18.6](../../domaene/anforderungen/phasen/bewegung/fliegen.md): Findet Arbiter für ein
  fliegendes *Modell* nach dem Übergehen keine freie *Stelle*, sperrt er mit ‚Base überdeckt‘.
  Ohne AUF-27 gibt es diesen Fall nicht, denn frei ist immer zumindest die *Stelle*, an der
  das *Modell* vor dem Ziehen stand (Anliegen 13020).
- [BEW-21](../../domaene/anforderungen/phasen/bewegung/sperreBeimLoslassen.md): Der Absatz
  „Am Bildschirm“ setzt ein *Modell* voraus, das schon vor dem Ziehen eine fremde *Base*
  überdeckt, also AUF-27.
- [16101](16101-angebotNachDerSperreBeimUebergehen.md) fragt, ob nach der *Sperre* aus BEW-18.6
  *gemeinsam übergehen* angeboten bleibt; ohne BEW-18.6 erübrigt sich das.

**Kosten.** Mit AUF-27 entfallen zwei Kriterien. Was stattdessen geschieht, wenn eine
*Formation* nicht passt, legt ein Kriterium fest. BEW-18.6 entfällt oder wird neu begründet,
BEW-21 bekommt ein anderes Beispiel für den Bildschirm. Im Code bleibt bis dahin die Zeile, mit der Arbiter nach
dem Übergehen sperrt
([schlachtrunden.py](../../technik/arbiter/domaene/querschnitt/schlachtrunden.py), Zeile 149),
ohne Test. Am Bildschirm ändert sich bis Etappe 7 nichts.

**Gegenvorschlag.** In Domänenphase 11 AUF-27 so fassen, dass keine *Base* eine andere
*überdeckt*, und BEW-18.6, BEW-21 und 16101 danach ausrichten. Was Arbiter tut, wenn eine
*Formation* nirgends passt, fragst du den Stakeholder mit Empfehlung. Anliegen 992 F1 A
(kein *Modell* kommt dazu, Arbiter nennt den *Grund*) entspräche seiner Antwort in 16100.

**Stellungnahme.**
