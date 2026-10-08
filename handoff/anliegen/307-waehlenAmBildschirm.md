# Wählen am Bildschirm: Gewinner, Zone, Anzeige der Sperre, Neustart

307 · Fragen · von Anforderungsautor (Domäne) → Stakeholder · Runde 1/3 · rückfrage

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

**F2 · Wie wird die Aufstellungszone gewählt?**
- A: Nach F1 fordert der *Spielaktionsbereich* den *Gewinner* auf: „Spieler 1: Wähle deine
  Aufstellungszone auf der Karte.“ Ein Klick auf eine *Aufstellungszone* der *Karte* wählt
  sie, solange keine gewählt ist; danach ist ein Klick auf eine Zone keine Wahl mehr.
- B: Zwei Knöpfe im *Spielaktionsbereich*.

Empfehlung A: Only War gibt den Zonen keine Namen (`core_rules.txt:2322`, Glossar), ein
Knopf bräuchte einen erfundenen. Ein Klick auf eine Zone vor F1 trifft die *Sperre*
‚nicht wählbar‘ (AUF-1.2).

Antwort: 

**F3 · Wo und wie lange steht die Sperre einer Wahl, mit welchem Satz?**
- A: Im *Spielaktionsbereich*, bis zur nächsten Handlung. Sätze: ‚nicht wählbar‘ „Das ist
  jetzt nicht wählbar.“, ‚Einheit begonnen‘ „Erst die begonnene Einheit fertig
  aufstellen.“
- B: Neben dem, was geklickt wurde (*Einheit* in der *Ablage*, Zone auf der *Karte*), sonst
  wie A.
- C: Du nennst andere Sätze.

Empfehlung A: Ein Ort für alle Sperren einer Wahl. Das Ziel lässt jede *Sperre* übergehen;
kommt „gemeinsam übergehen“ (Plan 3, Danach), bleibt sie dort stehen, bis die *Spieler*
„zurück“ oder „gemeinsam übergehen“ wählen.

Antwort: 

**F4 · Was zeigt Arbiter nach einem Neustart?** QUE-3.2 gilt, solange Arbiter läuft.
- A: Die *Ausgangslage*; frühere Partien bleiben gespeichert, aber nicht sichtbar.
- B: Die letzte Partie; eine neue beginnt erst mit einer eigenen Handlung „Neue Partie“, die
  eine eigene Anforderung wird.

Empfehlung A: Etappe 1 kennt keine Handlung „Neue Partie“, und das Aufstellen dauert
Minuten. B wird wichtig, wenn Partien Stunden dauern (Etappe 3); dann frage ich neu.

Antwort: 

**F5 · Neuer Begriff.** *Spielaktionsbereich* | – | `spielAktionsBereich` | Ort auf dem
Bildschirm, an dem Arbiter fragt, was als Nächstes zu wählen ist, und eine *Sperre* einer
Wahl mit *Grund* zeigt. Dein Name aus Anliegen 223 F1 (git), dort die `gameActionsArea` aus
Arbiter-old (`Arbiter-old/docs/spec/ui_layout.md:307`). A: so freigeben, mit dem Plan.
B: anderes Wort.

Empfehlung A.

Antwort: 

**Stellungnahme.** Ich bin mir nicht sicher, ob ich das Problem aus deinen Fragen richtig verstanden habe. Deine Sätze und auch deine Ziele und auch der Zweck in den Anforderungen ist in Teilen sehr knapp, so dass scheinbar einige Informationen fehlen. Gehen wir nochmal ein Stück zurück. Was wäre aus deiner Sicht denn ein passender Start oder eine Voraussetzung, die wir schaffen sollten, bevor eine Einheit auswählbar ist? In Anbetracht dessen, dass wir irgendwo anfangen müssen, könnte man sich auch überlegen, dass Gewinner des Rolloff, Wahl der Aufstellungszone etc. bereits gewählt ist und es hier eine technische Krücke braucht, die das ermöglicht. Diese müsste durch ein entsprechenden Test kenntlich gemacht werden, dass man sie durch eine solide technische Lösung ersetzt. Dafür bräuchte es ggf. eine neue Anforderung. Denke nochmal darüber nach und bringe hier Vorschläge.
