# Lücken aus dem vollen Mutationslauf gehen an ihren Autor, nicht nur in die Technikphase

1840 · Kritik · von Fachkritiker → Organisationsentwickler · Runde 1/3 · erledigt

## Runde 1
**Befund.** Kritik an der [Retro 6](../retro.md), P2: „Ganze Module, auch `web/`, nur im vollen
Lauf der Retro; er hält nichts auf, seine Lücken gehen in die Technikphase.“
1. Das widerspricht [Ich 3](../../prozess/praemissen/ich.md): Eine Lücke wartet auf die nächste
   Phase der Perspektive ihres Autors. Fehlt einem überlebenden Mutanten ein Kriterium, ist der
   Autor der Anforderungsautor, die Phase die Domänenphase.
2. Den Fall gibt es schon: Im [Review 6](../review.md#dod), DoD 1, erreicht `_loslassen` mit
   *Sperre* nur ein Klick, dessen *Formation* fremde *Bases* überdeckt, und der Reviewer
   urteilt „Kriterium fehlt, Plan 7 (AUF-18.7, 27)“. Ein Mutant in dieser Zeile überlebt, bis
   ein Kriterium den Fall regelt; in der Technikphase kann ihn niemand schließen.
3. P2 nimmt damit die Antwort auf F2 in [1671](1671-prozessphaseVorziehen.md) vorweg. F2 ist
   offen („Antwort: .“, die Klärung sagt „F2 bleibt offen“), und die Retro nennt keine Annahme
   ([Ich 1](../../prozess/praemissen/ich.md)). Die Empfehlung zu F2 (A) unterscheidet genau
   die beiden Fälle, P2 nennt nur einen.

Einordnung nach Ich 3: hält auf. Mit der Freigabe bekäme der Regelumsetzer den Auftrag, eine
Regel gegen eine Prämisse zu bauen, die nur der Stakeholder ausnehmen kann.

**Kosten.** Landet eine Lücke ohne Kriterium in der Technikphase, schreibt der Testautor
entweder einen Test, der mehr verlangt als das Kriterium (das prüfe ich als Befund am Test),
oder der Mutant bleibt stehen und zählt unter 95 % weiter. In beiden Fällen sieht der
Stakeholder am Bildschirm nichts davon, und der fehlende Fall wird nie entschieden: Was soll
geschehen, wenn eine *Formation* beim Klick fremde *Bases* überdeckt?

**Gegenvorschlag.** Bestehende Regel, kein neuer Text ([Ich 4](../../prozess/praemissen/ich.md)):
Ich 3 und die Empfehlung zu F2. P2 sagt statt „seine Lücken gehen in die Technikphase“:
„seine Lücken gehen nach Ich 3 an ihren Autor: Tests und Code in die Technikphase, ein
fehlendes Kriterium in die Domänenphase“. Bis der Stakeholder F2 beantwortet, steht in 1671
über der Antwort zu F2 `Annahme: …` mit dem, was P2 damit tut.

Erledigt, wenn P2 beide Fälle nennt und auf F2 verweist.

**Stellungnahme.** Umgesetzt in [Retro 6](../retro.md), P2: „seine Lücken nach 1671 F2: ein
fehlendes Kriterium in die Domänenphase, sonst in die Technikphase“. Zu 3: Inzwischen hat der
Stakeholder F2 in [1671](1671-prozessphaseVorziehen.md) mit A beantwortet; eine Annahme
braucht es nicht mehr. Den Satz „F2 bleibt offen“ in der Klärung dort hat die Antwort überholt.
