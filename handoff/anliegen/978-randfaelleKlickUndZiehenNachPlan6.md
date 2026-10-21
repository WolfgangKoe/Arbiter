# Randfälle nach Plan 6: Ziehen aus der Ablage, Klick neben die Zone

Form: Kritik
Von: Architekt
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet. Das sind Lücken abseits des Happy Path.
1. Nach Item 1 sagt kein Kriterium, was geschieht, wenn jemand eine *Einheit* aus der
   *Ablage* zieht. AUF-8.5, 8.6, 16.1, 16.4 und 16.5 entfallen. Der Zweck von
   [AUF-8](../../domaene/anforderungen/phasen/aufstellen/ziehen.md) sagt aber weiter: „Die
   *Spieler* ziehen *Einheiten* aus der *Ablage* auf die *Karte*“.
2. [AUF-11.3](../../domaene/anforderungen/phasen/aufstellen/gewinnerUndZone.md) regelt nur
   den Klick in eine *Aufstellungszone*. Offen ist der Klick vor der Wahl in die Mitte der
   *Karte*. Ein Klick in eine Zone vor dem *Gewinner* zeigt nach AUF-1.2 den *Grund*
   ‚nicht wählbar‘. Damit erscheint ein *Grund*, den der Plan unter „Am Bildschirm dabei nur“
   nicht nennt.

**Kosten.** Ohne Kriterium entscheidet die Technik selbst. Bis zur nächsten Domänenphase tut
sie Folgendes: Eine Karte in der *Ablage* lässt sich nicht ziehen, und ein Klick neben die
Zonen ändert nichts. Ein Test dazu fehlt.

**Gegenvorschlag.** In der nächsten Domänenphase:
1. Den Zweck von AUF-8 auf *Modelle* beschränken. Ein Kriterium sagt, dass das Ziehen einer
   *Einheit* der *Ablage* nichts ändert und keinen *Grund* nennt (wie AUF-16.6).
2. Bei AUF-11 ein Kriterium für den Klick vor der Wahl außerhalb jeder *Aufstellungszone*:
   Es ändert nichts und nennt keinen *Grund*.

Erledigt, wenn beide Fälle ein Kriterium haben oder du begründest, warum keins nötig ist.

**Stellungnahme.**
