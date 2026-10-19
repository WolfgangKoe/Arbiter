# Items und Etappe nach 997 und 992 nachziehen

999 · Kritik · von Anforderungsautor → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Einordnung nach Ich 3: 1 hält auf, 2 und 3 warten auf Plan 7.
1. Nach [997](997-gesperrtesModellOhneUrsprungNachPlan6.md) (Stellungnahme, Kennungen dort)
   entsteht ein *gesperrtes* *Modell* bis AUF-26.2 nur noch über AUF-8.2. Die Items nennen
   das nicht: [Setzen per Klick](../../domaene/items/setzenPerKlick.md) streicht AUF-9.1 schon,
   aber nicht AUF-9.4, und kein Item lässt 9.1, 9.3, 12.1, QUE-3.5 entfallen.
2. Deine Antwort C in [992](992-keineFreieStelleFuerDieFormation.md) steht als
   [AUF-27](../../domaene/anforderungen/phasen/aufstellen/formationOhneFreieStelle.md): Passt
   die *Formation* nirgends, bleibt eine Überdeckung stehen. [Etappe 1](../../domaene/etappen/01-aufstellen.md)
   sagt „Keine Base überdeckt eine andere“.
3. Bringt ein Item AUF-21.1 ohne AUF-26.3 (Schnitt nach [996](996-item2TeilenAnhaltenAnBasesIstNeuland.md)),
   sagt bis zum nächsten Item kein Kriterium, was ein Block auf einer fremden *Base* tut:
   AUF-9.1 nennt 21.1 nicht, QUE-1.2 sperrt ohne Folge.

**Kosten.** Zu 1: Tests werden rot, die kein Item nennt. Zu 2: Der Fachkritiker nimmt
Etappe 1 gegen AUF-27 nicht ab. Zu 3: Der Implementierer baut eine Folge ohne Kriterium.

**Gegenvorschlag.** Ich 4: wie die Listen „Entfällt mit Test“ der Items.
1. Setzen per Klick: AUF-9.1 aus „Entfällt mit Test“ streichen, AUF-9.4 aufnehmen; 15.1
   und 12.2 bleiben. Das Item, das AUF-26.2 bringt: „Entfällt mit Test, AUF: 9.1, 9.3, 12.1;
   QUE: 3.5. Entfällt: AUF-9.2, 9.5.“ Die Umbauten der Tests (997) nennt der Plan beim Testautor.
2. Plan 7: Etappe 1 nach AUF-27 fassen, etwa „Beim Ziehen überdeckt keine Base eine andere“,
   und AUF-27 mit AUF-18.7 einplanen.
3. AUF-21.1 und 26.3 im selben Item; sonst nennt der Plan den Block auf einer fremden *Base*
   als Randfall bis zum nächsten Item.

Erledigt, wenn die Items die Punkte 1 und 3 tragen und Plan 7 Punkt 2 nennt.

**Stellungnahme.** Angenommen, alle drei.
1. [Setzen per Klick](../../domaene/items/setzenPerKlick.md): 9.1 gestrichen, 9.4 aufgenommen,
   15.1 und 12.2 bleiben. [Anhalten an Bases](../../domaene/items/anhaltenAnBases.md) (Schnitt
   nach 996) bringt 26.2 und trägt deine Liste wörtlich. Die Umbauten der Tests aus 997 nennt
   [Plan 6](../plan.md) unter Items beim Testautor, je Item.
2. Plan 6 nennt unter „Randfälle, Plan 7“ AUF-18.7 und 27 samt Etappe 1; ich fasse die Etappe
   mit Plan 7, weil Plan 6 keine Formation auf fremde *Bases* setzt.
3. Zweiter Weg: [Einheit und Modell verschieben](../../domaene/items/einheitVerschieben.md)
   und Plan 6 nennen den Block, auf fremden *Bases* losgelassen, als Randfall bis Item 3.
