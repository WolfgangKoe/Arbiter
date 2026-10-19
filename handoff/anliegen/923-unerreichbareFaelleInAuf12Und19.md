# Fälle, die kein Klick und kein Zug erreicht (AUF-12.5, 19.4, 19.5, 21)

923 · Kritik · von Architekt → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: alle vier warten, keiner liegt auf dem Happy Path.
1. [AUF-19.4](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md) nennt AUF-22.2.
   Eine *aufgestellte* *Einheit* ist nie *ausgewählt* (AUF-5.10), ein Klick nach AUF-18.1
   erreicht sie also nicht.
2. [AUF-12.5](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md) nennt beim
   Loslassen AUF-7.3 und 22.1. Ziehen kann man nur *gesetzte* *Modelle* (AUF-8.2); außer der
   *Einheit in Aufstellung* sind das nur *aufgestellte*, für die AUF-22.2 gilt. Erreichbar
   sind beide nur über eine zweite, veraltete Seite (QUE-3.2), die ein nicht *gesetztes*
   *Modell* loslässt. Was dann gilt, regelt kein Kriterium: Heute *setzt* es Arbiter einfach,
   an der *Auswahl* vorbei (AUF-18.1, 19.5).
3. Gibt es ein *gesperrtes* *Modell* und zwei *ausgewählte* *Einheiten*: ‚Modell gesperrt‘
   allein (AUF-12.1, „keinen anderen *Grund*“) oder ‚mehrere ausgewählt‘ (AUF-19.5)?
4. Der Plan sagt „wandert die ganze *Einheit* mit“, also während des Ziehens; AUF-21 sagt
   nur, wo sie nach dem Loslassen steht. ArbiterMap zeigt den Block schon beim Ziehen,
   gerückt (`interaction_map.md:392`).

**Kosten.** Zu 1 und 2: Der Testautor baut Tests über einen Weg, den die Oberfläche nicht hat,
oder lässt Fälle aus, die das Kriterium nennt. Zu 3: Die Technik wählt die Reihenfolge der
Wächter selbst. Zu 4: Was der Plan verspricht, prüft kein Test.

**Gegenvorschlag.** 1: AUF-22.2 aus AUF-19.4 nehmen. 2: AUF-7.3 und 22.1 aus AUF-12.5 nehmen
und den Stakeholder fragen, was ein Loslassen eines nicht *gesetzten* *Modells* tut
(Empfehlung: nichts, wie AUF-16.6). 3: in AUF-19.5 „außer nach AUF-12.1“ oder umgekehrt.
4: ein Kriterium zum Bild während des Ziehens oder den Plansatz durch den Planer auf „nach
dem Loslassen“ ändern lassen. Erledigt, wenn jeder Punkt geregelt ist oder du begründest,
warum nicht.

**Stellungnahme.** Angenommen, alle vier, in
[AUF-19](../../domaene/anforderungen/phasen/aufstellen/gesperrterKlick.md),
[AUF-12.5](../../domaene/anforderungen/phasen/aufstellen/sperreOhneStelle.md),
[AUF-16.7](../../domaene/anforderungen/phasen/aufstellen/loslassenOhneZiel.md) und
[AUF-24.1](../../domaene/anforderungen/phasen/aufstellen/blockAlsGanzes.md).
1. AUF-22.2 aus AUF-19.4 genommen.
2. AUF-7.3 und 22.1 aus AUF-12.5 genommen; das Loslassen eines nicht *gesetzten* *Modells*
   regelt AUF-16.7 mit der Empfehlung, gefragt in [930](930-modellLoslassenDasNichtMehrGesetztIst.md).
3. AUF-12.1 geht vor, wie sein „keinen anderen *Grund*“ schon sagt (Ich 4): AUF-19.5 nennt bei
   *gesperrtem* *Modell* nur AUF-12.1. Dazu fasst AUF-19.4 den Klick, der einer *Einheit* gilt,
   statt nur das *Setzen* nach 18.2: Nach [890](890-zuruecklegenInGanzeEinheit.md) ist AUF-18.4
   gelöscht, und ein Klick für die *Einheit in Aufstellung* mit *gesperrtem* *Modell* fiele
   sonst durch.
4. Kriterium statt Plansatz: AUF-24.1 nach dem Vorbild `interaction_map.md:391`. In Item 2 nimmt
   es der Planer auf ([932](932-plan6NachZuruecklegenUndBlock.md)).
