# Etappe 1 verspricht das Anhalten vor fremden Bases, Plan 7 bringt es nicht

Form: Kritik
Von: Fachkritiker
An: Planer
Runde: 1/3
Status: erledigt

## Runde 1
**Befund.** Einordnung nach [Ich 3](../../prozess/praemissen/ich.md): hält auf. Der Plan sagt
„Nach Plan 7 ist Etappe 1 erreicht“, und dein „.“ gibt Etappe 1 frei, wie sie steht. Ein Satz
aus „Erreicht, wenn“ in [Etappe 1](../../domaene/etappen/01-aufstellen.md) wird damit nicht
erreicht: „Beim Ziehen klemmen Block und Modell wie in ArbiterMap an der Zone und vor fremden
Bases.“
1. An der Zone: gebaut und getestet ([AUF-26.1](../../domaene/anforderungen/phasen/aufstellen/anhaltenAnEinerBase.md),
   AUF-21).
2. Vor fremden Bases: Das regelt nur noch
   [AUF-29](../../domaene/anforderungen/phasen/aufstellen/anhaltenAufDemWeg.md); AUF-26 verweist
   im Zweck darauf. AUF-29 steht im Item
   [Anhalten auf dem Weg](../../domaene/items/anhaltenAufDemWeg.md), nach deiner Antwort 2361
   F2 A in Etappe 3, und [Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md) sagt es
   noch einmal: „das Ziehen hält an fremden Bases an und gleitet an ihnen entlang“. Dieselbe
   Aussage steht in zwei Etappen ([Wir 3](../../prozess/praemissen/wir.md)).
3. Das Anhalten an der ersten fremden Base ist zwar gebaut, aber ohne Kriterium und ohne
   Akzeptanztest: AUF-26.2 und 26.3 sind gestrichen (Commit „Domänenphase 7 als
   Zwischenstand…“). Die Abnahme in Schritt 5 kann es an keinem Kriterium von Etappe 1 prüfen.

**Kosten.** Gibt der Stakeholder frei, misst das Review 7 Etappe 1 an einem Satz, den kein
Item des Plans und kein Kriterium von Etappe 1 trägt; entweder erklärt es Etappe 1 für
erreicht, obwohl „wie in ArbiterMap vor fremden Bases“ fehlt (das Entlanggleiten, AUF-29.2),
oder Etappe 1 bleibt offen, obwohl der Plan das Gegenteil verspricht.

**Gegenvorschlag.** Etappe 1 folgt 2361 F2 A: Der Satz lautet „Beim Ziehen klemmen Block und
Modell wie in ArbiterMap an der Zone.“; das Anhalten vor fremden Bases steht nur in Etappe 3.
Ein Item ändert sich nicht, Plan 7 erreicht Etappe 1 dann. Ob der gebaute Halt an der ersten
Base ohne Kriterium bis Etappe 3 bleibt, ist Sache des Architekten (Rückverfolgung), nicht der
Etappe.
Erledigt, wenn kein Satz aus „Erreicht, wenn“ von Etappe 1 ohne Kriterium in einem gebauten
oder geplanten Item steht.

**Stellungnahme.** Angenommen, wie vorgeschlagen.
[Etappe 1](../../domaene/etappen/01-aufstellen.md) sagt jetzt „Beim Ziehen klemmen Block und
Modell wie in ArbiterMap an der Zone.“; das Anhalten vor fremden *Bases* steht nur noch in
[Etappe 3](../../domaene/etappen/03-angriffUndFallBack.md) mit dem Item
[Anhalten auf dem Weg](../../domaene/items/anhaltenAufDemWeg.md), wie 2361 F2 A es legt. Die
Items von Plan 7 bleiben; der [Plan](../plan.md) nennt die Änderung unter „Annahmen“, damit
der Stakeholder sie mit seinem „.“ sieht. Den gebauten Halt an der ersten *Base* ohne
Kriterium lasse ich, wie du sagst, beim Architekten.
