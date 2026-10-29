# BEW-15 sagt nochmals, was BEW-11 und BEW-13 schon sagen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** [BEW-11.1](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md) legt den
Mittelpunkt des *Grenzkreises* jeder *ausgewählten* *Einheit* schon auf die *Stelle* zu Beginn
der *Bewegungsphase*, gleich wie sie *ausgewählt* wurde und ob sie vorher abgewählt war; 11.5
übernimmt das für die *Einhüllende*.
[BEW-13.1 und 13.2](../../domaene/anforderungen/phasen/bewegung/grenzkreiseBeimVorruecken.md)
gelten ebenso für jede *ausgewählte* *Einheit*. Damit beantworten BEW-11 und BEW-13 die Frage
des Stakeholders schon: 15.1 wiederholt 11.5, 15.2 wiederholt 11.1, 15.3 wiederholt 13.2
([Wir 3](../../prozess/praemissen/wir.md): jede Aussage genau einmal). Dass der wartende
*Vorrückwurf* fehlt, ist folgerichtig nur, weil 13.1 ihn allgemein regelt; dasselbe gilt
für alles in BEW-15. Dazu ist 15.1 enger als die Spielweise am Tisch: Abgewählt wird die
erste *Einheit* meist nicht nach BEW-9.1, sondern indem jemand gleich ein *Modell* der
anderen anklickt (AUF-20.6, „keine andere“). Diesen Weg nennt BEW-15 nicht; ein Test nach
15.1 prüfte nur den selteneren. Im Gebauten hält die Domäne die *Stellen* zu Beginn je
*Bewegungsphase*, nicht je *Auswahl* (`technik/arbiter/domaene/querschnitt/schlachtrunden.py:50`,
`:100`); Grenzkreise sind noch nicht gebaut.

**Kosten.** Bleibt BEW-15, schreibt der Testautor drei Tests, deren Aussage die Tests zu
BEW-11 und BEW-13 schon tragen, und der Zähler der Etappe 2 wächst um drei Kriterien ohne
neues Verhalten am Bildschirm. Fällt es weg: eine Datei löschen, der Planer nimmt BEW-15 aus
dem Item [Grenzkreise](../../domaene/items/grenzkreise.md) und aus dem Plan. Die Frage des
Stakeholders bleibt beantwortet; den Weg „ziehen, abwählen, andere ziehen, wieder auswählen“
kann der Testautor als *Gegeben* eines Tests zu 11.5 nehmen, ohne mehr zu verlangen als das
Kriterium.

**Gegenvorschlag.** BEW-15 streichen und dem Stakeholder mit Link auf BEW-11.1 antworten:
„Die Grenze zeigt immer von der *Stelle* zu Beginn der *Bewegungsphase* aus, auch nach
Abwählen und erneuter *Auswahl*.“ Will der Anforderungsautor den Weg ausdrücklich sehen,
nennt er ihn in „Am Bildschirm“ von BEW-11, nicht als eigenes Kriterium. Bleibt BEW-15
doch, dann ohne Bindung an BEW-9.1: „die nicht mehr *ausgewählt* war“.

**Stellungnahme.** Angenommen in deiner Rückfalllösung, Streichen abgelehnt.
15.2 und 15.3 sind gestrichen: Sie wiederholen 11.1 und 13.2, wie du sagst. 15.1 bleibt,
ohne Bindung an BEW-9.1: „die nicht mehr *ausgewählt* war“; „Am Bildschirm“ nennt beide
Wege, das *Modell* der anderen *Einheit* (AUF-20.6) und die leere *Karte* (BEW-9)
([BEW-15](../../domaene/anforderungen/phasen/bewegung/grenzkreiseNachErneuterAuswahl.md)).
Warum nicht streichen: 15.1 sagt keinen zweiten Satz zu 11.5, es verlangt den Fall, der
zwei Bauweisen trennt. Ein Test zu 11.1 oder 11.5 zieht die *ausgewählte* *Einheit* und
sieht die Grenze an der alten *Stelle*; das besteht auch Code, der die *Stellen* bei jeder
*Auswahl* neu merkt. Erst abwählen, die andere ziehen, wieder *auswählen* zeigt den
Unterschied, und genau diesen Fall will der Stakeholder geprüft sehen. Als *Gegeben* eines
Tests zu 11.5 stünde er dem Testautor frei, in „Am Bildschirm“ von BEW-11 entstünde kein
Test. Dass das Gebaute die *Stellen* je *Bewegungsphase* hält (`schlachtrunden.py:50`),
sagt nicht, dass die noch nicht gebauten *Grenzkreise* sie dort lesen. Kosten: ein
Kriterium statt drei.
