# BEW-15 sagt nochmals, was BEW-11 und BEW-13 schon sagen

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 10

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

**Stellungnahme.**
