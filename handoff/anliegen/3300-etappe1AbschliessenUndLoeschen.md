# Etappe 1 abschließen und ihre Datei löschen

Form: Kritik
Von: Reviewer
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Im Auftrag des Stakeholders: In der Freigabe von [Review 7](../review.md) schreibt
er „Wir können Etappe 1 somit auch abschließen und die Datei löschen.“ Nach
[Domäne](../../domaene/CLAUDE.md) wird Erreichtes gelöscht, aktuell ist die kleinste Nummer.
[01-aufstellen.md](../../domaene/etappen/01-aufstellen.md) steht noch; der Stand nennt deshalb
„Etappe 1 von 10 (Aufstellen)“, er nimmt die erste Etappendatei
(`standregeln/phasenfolge.py`, `aktuelleEtappe`).

**Kosten.** Stand, Dashboard und Plan 8 nennen eine erreichte Etappe als aktuelle. Hält
Plan 8 auf, nicht die Retro.

**Gegenvorschlag.**
1. `rm domaene/etappen/01-aufstellen.md`; danach nennt der Stand „Etappe 2 von 10“.
2. `handoff/plan.md`, Zeile 3, verlinkt die Datei noch; der Link fällt mit Plan 8. Im Review
   habe ich ihn schon entfernt.
3. Für [Etappe 2](../../domaene/etappen/02-bewegen.md) gibt es keinen Commit „Freigabe
   Etappe 2“. Der [Ablauf](../../prozess/ablauf.md#fortschritt) sieht Domäne 1 bis 3 nur ohne
   Etappe vor, zugleich gibt der Stakeholder die Etappe mit „.“ frei
   ([Freigabe und Kommentare](../../prozess/ablauf.md#freigabe-und-kommentare)). Meine
   Empfehlung: Du nennst Etappe 2 in Plan 8 und bittest dort um ihr „.“.

Erledigt, wenn die Datei gelöscht ist und der Stand Etappe 2 nennt.

**Stellungnahme.** Angenommen, alle drei Punkte.
1. `01-aufstellen.md` ist gelöscht; der Stand nennt „Etappe 2 von 10 (Phasen und
   Bewegungsphase)“.
2. Der Link in Plan 7 bleibt, bis Plan 8 die Datei ersetzt; den freigegebenen Plan ändere
   ich nicht.
3. Plan 8 nennt [Etappe 2](../../domaene/etappen/02-bewegen.md) und bittet in der Freigabe
   um ihr „.“.

Die übrigen Verweise auf Etappe 1 in Daten, Glossar und zwei Anforderungen gehen an den
Anforderungsautor ([3500](3500-verweiseAufEtappe1.md)), sie warten auf die Domänenphase.
