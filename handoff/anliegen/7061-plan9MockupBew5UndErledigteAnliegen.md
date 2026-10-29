# Plan 9: Mockup bew-5 und erledigte Anliegen als Bedingung

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Hält auf (Kritik, Schritt 5 des Happy Path und Freigabe).
1. [Item grenzkreise](../../domaene/items/grenzkreise.md) enthält BEW-5, verlinkt aber nur
   bew-11, bew-13 und bew-12. In keinem dieser drei Mockups steht „Vorrücken“ (siehe
   [7060](7060-vorrueckenFehltInBew11.md)), und zwar ein Knopf, mit dem Schritt 5 beginnt.
   Gezeigt wird er nur in [bew-5](../../domaene/mockups/bew-5.html), und auf bew-5 verlinkt
   kein Item. Nach der Domänenphase, Schritt 4, verlinkt das Item jedes Mockup seiner
   Anforderungen.
2. [Plan 9](../plan.md) nennt als Bedingung „Bereit zur Freigabe nach Anliegen 7003; 7004 vor
   dem Vertrag zu Item 4“, das Item nennt unter „Abhängigkeit“ „Anliegen 7003, 7004“. Beide
   sind erledigt und gelöscht (Commits 4286d1f, c5cc31b). Der Stakeholder liest daraus eine
   Bedingung, die schon erfüllt ist, und wartet oder fragt nach (Absicht 5).

**Kosten.** Je eine Zeile. Ohne 1 baut der Implementierer den Knopf ohne Mockup oder nach
bew-11; ohne 2 hält der Plan die Freigabe für etwas auf, das schon erledigt ist.

**Gegenvorschlag.** 1: Im Item grenzkreise bew-5 vor bew-11 verlinken. 2: Den Satz aus dem
Plan streichen, oder er lautet „Bereit zur Freigabe.“; im Item „Anliegen 7003, 7004“
streichen.

**Stellungnahme.** Angenommen, beides umgesetzt. 1: Das
[Item grenzkreise](../../domaene/items/grenzkreise.md) verlinkt bew-5 vor bew-11, bew-13 und
bew-12. 2: Im [Plan](../plan.md) ist der Satz zu 7003 und 7004 gestrichen, im Item „Anliegen
7003, 7004“ unter „Abhängigkeit“.
