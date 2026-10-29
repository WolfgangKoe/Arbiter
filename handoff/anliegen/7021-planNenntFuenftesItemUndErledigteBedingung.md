# Plan 9: Fortschritt nennt ein fünftes Item, Freigabe wartet auf Erledigtes

Form: Kritik
Von: Architekt
An: Planer
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** Hält auf: Die Technikphase arbeitet den Fortschritt des [Plans](../plan.md) ab.
1. Der Fortschritt enthält neun Schritte zu Item `phaseBeendenNurImZug` (QUE-11), obwohl der Plan
   vier Items freigibt und QUE-11 unter „Danach“ für Plan 10 nennt. Ursache: `lesen/plan.py`
   (`itemNamen`) nimmt jeden Link auf `../domaene/items/` im ganzen Plan, auch den unter
   „Danach“.
2. „Bereit zur Freigabe nach Anliegen 7003; 7004 vor dem Vertrag zu Item 4“: Beide sind
   erledigt, der Satz lässt den Stakeholder auf nichts warten.

**Kosten.** Ohne 1 starten nach der Freigabe Testautor und Implementierer an QUE-11, ein Item,
das niemand freigegeben hat. Je eine Zeile.

**Gegenvorschlag.** Unter „Danach“ QUE-11 ohne Link nennen, dann schreibt das Skript den
Fortschritt ohne das Item neu; den Satz zu 7003 und 7004 streichen.

**Stellungnahme.** Angenommen, beides umgesetzt im [Plan](../plan.md). 1: Unter „Danach“
steht QUE-11 ohne Link; der Hook hat den Fortschritt neu geschrieben, er nennt nur noch die
vier Items. Die Ursache in `lesen/plan.py` liegt beim Regelumsetzer:
[7030](7030-fortschrittNimmtItemsNurAusDemAbschnittItems.md). 2: Der Satz zu 7003 und 7004
ist gestrichen, ebenso „Anliegen 7003, 7004“ im
[Item grenzkreise](../../domaene/items/grenzkreise.md).
