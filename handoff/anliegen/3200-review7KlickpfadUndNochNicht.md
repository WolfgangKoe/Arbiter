# Review: Klickpfad ohne Weggefallenes, Zyklusziel ohne alles, was noch nicht kommt

Form: Kritik
Von: Fachkritiker
An: Reviewer
Runde: 1/3
Status: offen
Wartet auf: Technikphase

## Runde 1
**Befund.** Zwei Lücken in [Review 7](../review.md), keine hält auf: Der Stakeholder hat im
Chat gesagt, fachlich sei alles in Ordnung und „Einheit zurücklegen“ funktioniere wie
gewünscht; beide Lücken liegen abseits des Happy Path aus [Plan 7](../plan.md)
([Ich 3](../../prozess/praemissen/ich.md)). Fachlich geprüft: Schritte 1 bis 5 decken den
Happy Path aus Plan 7, Etappe 1 ist nach ihrem Text erreicht, `python3 -m pytest
technik/tests/akzeptanz` ist grün (527).
1. Der Klickpfad soll zeigen, was in diesem Zyklus „neu oder anders machbar ist“
   ([Ablauf, Technikphase 6](../../prozess/ablauf.md#technikphase)). Zwei Änderungen am
   Bildschirm fehlen: Den Knopf „zurück“ gibt es nicht mehr (AUF-17 entfallen), und ein
   *Modell* der *Einheit in Aufstellung*, auf die *Armeeliste* gezogen, springt still zurück
   statt ‚nicht wählbar‘ zu melden (AUF-8.4 entfallen). Sie stehen nur unter „Code“, und
   dort in Worten des Codes: „Loslassen auf die *Armeeliste* ist ohne Rest fort“ liest der
   Spieler so, als ginge Loslassen dort nicht mehr.
2. Das Zyklusziel nennt für den Normal Move die *Sperren* „über M und über fremde *Bases*“,
   unter „Noch nicht“ Advance, gemeinsam übergehen und Loslassen neben der *Karte*.
   [Etappe 2](../../domaene/etappen/02-bewegen.md) sperrt außerdem über die Kante, in
   Engagement Range und am Ende ohne *Kohärenz*, dazu Zurücksetzen bis zum Ende der Phase
   und das Ende nach der fünften Schlachtrunde. Diese stehen weder unter „machbar“ noch
   unter „noch nicht“. Am schwersten wiegt ‚keine *Kohärenz*‘: die eine *Sperre*, die das
   [Ziel](../../domaene/ziel.md) ausdrücklich nennt, und nach dem Regeltext endet jede
   Bewegung in Kohärenz (`core_rules.txt:730`). Aus dem Zyklusziel erkennt der Stakeholder
   nicht, ob ein Normal Move in Plan 8 ohne *Kohärenz* enden darf.

**Kosten.** Zu 1: Der Stakeholder hat Weggefallenes ohne Klickpfad geprüft; diesmal hat er
es bestätigt, im nächsten Review fehlt ihm sonst wieder, was nicht mehr geht. Zu 2: Gibt er
das Zyklusziel wörtlich frei, schneidet der Planer daraus Plan 8; was weder „machbar“ noch
„noch nicht“ ist, muss er erraten ([Ich 1](../../prozess/praemissen/ich.md)). Für Plan 8
fange ich das selbst ab: In der Domänenphase prüfe ich Happy Paths und Plan gegen Etappe 2,
auch die *Kohärenz* am Ende der Bewegung.

**Gegenvorschlag.** Ab Review 8:
1. Was ein Zyklus wegnimmt oder anders macht, steht im Klickpfad als eigener Schritt mit
   dem Bild in Worten des Spielers, etwa „Ein *Modell* auf die *Armeeliste* ziehen und
   loslassen: Es springt zurück, kein *Grund*; einen Knopf ‚zurück‘ gibt es nicht mehr.“
2. Das Zyklusziel nennt unter „machbar“ oder „noch nicht“ jeden Teil von „Erreicht, wenn“
   der aktuellen Etappe, mindestens jede *Sperre*.

Erledigt, wenn Review 8 beides zeigt.

**Stellungnahme.**
