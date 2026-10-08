# Wählen am Bildschirm: Gewinner, Zone, Anzeige der Sperre, Neustart

307 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · erledigt

Legende: Status im Kopf · als Empfänger angenommen, rückfrage, abgelehnt · als Absender erledigt, offen (neue Runde) · unter einer Frage `Antwort: .` (Empfehlung), `Antwort: B` oder `Antwort: <Text>`

## Runde 1
**Befund.** Zyklusziel aus [Review 3](../review.md): Wählen per Klick (Gewinner, Zone,
Einheit) mit Speicher und Anzeige der *Sperre* ‚nicht wählbar‘. Geschrieben sind
[AUF-5](../../domaene/anforderungen/phasen/aufstellen.md) (Einheit per Klick in der *Ablage*,
Vorbild ArbiterMap) und [QUE-3](../../domaene/anforderungen/querschnitt.md) (Tippen wie
Klick, Neuladen zeigt dasselbe). Regeln und Ziel sagen nicht, wie *Gewinner* und
*Aufstellungszone* gewählt werden, wo die *Sperre* steht und was ein Neustart zeigt.

**Kosten.** Ohne Antwort bringt Plan 4 nur die Wahl der *Einheit*; Gewinner und Zone sind am
Bildschirm nicht wählbar, die *Aufstellung* beginnt also nie. Die Kriterien unten trage ich
nach deiner Antwort ein.

**F1 · Wie wird der Gewinner gewählt?**
- A: Der *Spielaktionsbereich* fragt „Wer hat den Roll-off gewonnen?“ mit je einem Knopf
  „Spieler 1“ und „Spieler 2“; nach der Wahl verschwindet die Frage.
- B: Klick auf den Namen des *Spielers* über seiner *Ablage*.

Empfehlung A: Beide sehen die Frage an einem Ort; bei B weiß keiner, dass er klicken soll.

Antwort: .

**F2 · Wie wird die Aufstellungszone gewählt?** Klick auf die Zone der *Karte* oder zwei
Knöpfe; Empfehlung Klick, weil Only War den Zonen keine Namen gibt.

Antwort: 

**F3 · Wo steht die Sperre einer Wahl?** **F4 · Was zeigt ein Neustart?** **F5 · Begriff
Spielaktionsbereich.** Ausführlicher und neu gefasst in Anliegen 309.

Antwort: 

**Stellungnahme.** Ich bin mir nicht sicher, ob ich das Problem aus deinen Fragen richtig verstanden habe. Deine Sätze und auch deine Ziele und auch der Zweck in den Anforderungen ist in Teilen sehr knapp, so dass scheinbar einige Informationen fehlen. Gehen wir nochmal ein Stück zurück. Was wäre aus deiner Sicht denn ein passender Start oder eine Voraussetzung, die wir schaffen sollten, bevor eine Einheit auswählbar ist? In Anbetracht dessen, dass wir irgendwo anfangen müssen, könnte man sich auch überlegen, dass Gewinner des Rolloff, Wahl der Aufstellungszone etc. bereits gewählt ist und es hier eine technische Krücke braucht, die das ermöglicht. Diese müsste durch ein entsprechenden Test kenntlich gemacht werden, dass man sie durch eine solide technische Lösung ersetzt. Dafür bräuchte es ggf. eine neue Anforderung. Denke nochmal darüber nach und bringe hier Vorschläge.

**Klärung.** Deine Idee ist der Schnitt V1 aus [308](308-startDerAufstellung.md), dort
angenommen: Arbiter beginnt mit gewähltem Gewinner und gewählter Zone, und Plan 4 bringt die
Wahl der *Einheit* in der *Ablage*. Die Krücke steht als eigene Anforderung
[AUF-6](../../domaene/anforderungen/phasen/aufstellen.md): Spieler 1 ist *Gewinner* mit der
Zone neben seiner *Ablage*, Spieler 2 *an der Reihe*. Ihr Test zeigt sie als vorläufig: Er
geht mit AUF-6, sobald ihr am Bildschirm wählt. Den Zweck von AUF-5 und QUE-3 habe ich
ausführlicher gefasst.

Was offen bleibt:
- Für Plan 4: wo und wie lange die *Sperre* einer Wahl steht und wie der Satz lautet, und was
  Arbiter nach einem Neustart zeigt. Beides neu gefasst, mit mehr Erklärung, in Anliegen 309.
  Der Begriff aus F5 ist für Plan 4 nicht mehr nötig; ich frage danach mit Plan 6.
- Für Plan 6 (Gewinner und Zone am Bildschirm): F1 hat deine Antwort „.“, also Empfehlung A;
  sie gilt dann. F2 frage ich mit Plan 6 neu.

Damit erledigt.
