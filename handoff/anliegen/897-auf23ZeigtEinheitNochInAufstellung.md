# Mockup auf-23 zeigt die zurückgelegte Einheit noch „in Aufstellung“

897 · Kritik · von Fachkritiker → Ux · Runde 1/3 · erledigt

## Runde 1
**Befund.** [auf-23](../../domaene/mockups/auf-23.html) zeigt den Zustand nach
[AUF-23.1](../../domaene/anforderungen/phasen/aufstellen/einheitZuruecklegen.md). Die *Ablage*
von Spieler 1 hat dort „Boyz“ mit dem Abzeichen „in Aufstellung“ und 10 nicht *gesetzten*
*Modellen*. Ist keines ihrer *Modelle* mehr *gesetzt*, ist sie nach
[AUF-7.1](../../domaene/anforderungen/phasen/aufstellen/einheitInAufstellung.md) aber nicht mehr
die *Einheit in Aufstellung*. Es gibt dann keine, und
[AUF-4.5](../../domaene/anforderungen/phasen/aufstellen/anzeige.md) kennzeichnet keine.

Einordnung nach Ich 3: Die *Sperre* fehlt nicht, und sie greift im Produkt auch nicht zu
Unrecht. Der Test `testAuf4_5OhneEinheitInAufstellungKennzeichnetDieAblageKeine` hält das
Abzeichen fern. Deshalb hält der Befund nicht auf.

**Kosten.** Das Bild sagt dem Stakeholder etwas Falsches: Nach dem Zurücklegen wären die Boyz
weiter begonnen, und der Warboss wäre nach AUF-7.3 gesperrt (‚Einheit begonnen‘). Nach AUF-7.1
darf Spieler 1 nach dem Zurücklegen aber jede seiner *Einheiten* *setzen*. Wer Antwort B in
[890](890-zuruecklegenInGanzeEinheit.md) nach dem Mockup beurteilt, sieht eine Einschränkung,
die es nicht gibt.

**Gegenvorschlag.** In auf-23 bei „Boyz“ das Abzeichen „in Aufstellung“ und die Klasse
`inAufstellung` streichen. „ausgewählt“, „Ganze Einheit“ gewählt und die 10 bleiben. Erledigt,
wenn das Mockup keine *Einheit in Aufstellung* mehr kennzeichnet.

**Stellungnahme.** Der Befund trifft zu (AUF-7.1). In [auf-23](../../domaene/mockups/auf-23.html)
sind Abzeichen und Klasse `inAufstellung` gestrichen; „ausgewählt“, „Ganze Einheit“ und die 10
bleiben. Der Knopf „Aufstellen der Einheit beenden“ bleibt: Ohne *Einheit in Aufstellung* ist
*Aufstellen der Einheit beenden* wählbar und gesperrt mit ‚nicht in Aufstellung‘ (AUF-7.4), und
QUE-7.1 verbietet, dass er die *Karte* verschiebt, wenn er erscheint oder verschwindet.
