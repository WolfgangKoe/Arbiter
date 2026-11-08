# Auch der Griff einer Leiste verschiebt die Karte nicht

Form: Kritik
Von: Fachkritiker
An: Anforderungsautor
Runde: 1/3
Status: offen
Wartet auf: Domänenphase 11

## Runde 1
**Befund.** [QUE-7.1](../../domaene/anforderungen/querschnitt/ruhigeKarte.md) und der Zweck von QUE-7 nehmen den *Griff* aus: „außer ein *Spieler* klickt einen *Griff* und will damit den Platz ändern“ (Anliegen 13980). Der Stakeholder erwartet das Gegenteil, Antwort zu F1 in Anliegen 14462: „wenn die Seitenleisten rechts, links und unten nacheinander eingezogen werden, verschiebt sich die Karte immer noch. Meine Erwartung wäre, dass gerade das nicht mehr geschieht.“ Im Gebauten ist es so: `.spielbereich:has(> .leiste)` teilt das Fenster in Spalten auf, und eine *eingefahrene* *Leiste* blendet ihren Inhalt aus (`technik/frontend/komponenten.css:256`, `:291`). Fährt ein *Spieler* die linke oder rechte *Leiste* ein, rückt die *Karte* zur Seite; fährt er die untere ein, wird sie größer. In ArbiterMap liegen die Leisten über der Karte (`fixed`, `translate`), die Karte bleibt stehen (`ArbiterMap/frontend/templates/map.html:118`, `:133`, `:204`).

**Kosten.** Bleibt die Ausnahme stehen, belegt kein Test, was der Stakeholder am Bildschirm erwartet, und jedes Ein- und Ausfahren verschiebt jede *Stelle*, wie in Anliegen 670 beim *Grund*. Ändert sich das Kriterium, ändern sich mit: der Satz in [O4](../../technik/architektur/frontend.md) „Eine ausgefahrene Leiste nimmt der Karte Platz“ (Architekt), das Mockup [que-7](../../domaene/mockups/que-7.html) (UX), Tests zu QUE-7.1 und die CSS, also ein Item in Zyklus 11. Wie die *Karte* stehen bleibt, hat der Stakeholder in 14462, Runde 2, entschieden: A, die *Leisten* liegen über der *Karte* wie in ArbiterMap; die *Karte* hat das Fenster für sich, eine offene *Leiste* verdeckt den Rand des *Spielfelds* hinter ihr, in einem schmalen Fenster auch eine *Aufstellungszone*.

**Gegenvorschlag.** In QUE-7.1 und im Zweck die Ausnahme für den *Griff* streichen, etwa: „… **wenn** neben ihr etwas zu sehen beginnt oder aufhört, etwa ein *Grund*, …, eine *Leiste* *eingefahren* wird oder nicht mehr, …“ (Anliegen 14462). Weil QUE-7.1 schon Tests hat, gegebenenfalls als neues Kriterium QUE-7.2. Nach der Antwort A aus 14462 Runde 2 sagt die Anforderung, dass die *Leisten* über der *Karte* liegen und eine offene *Leiste* den Rand des *Spielfelds* verdecken darf; im [Glossar](../../domaene/glossar.md) steht die *Leiste* dann nicht mehr „neben der *Karte*“, sondern über ihrem Rand. Das Anliegen an den Architekten zu O4 schreibst du, wie in 13980 vorgesehen: Die *Karte* nimmt das Fenster ein, eine ausgefahrene *Leiste* nimmt ihr keinen Platz, und „statt eine *Aufstellungszone* zu verdecken (O2)“ entfällt. Erledigt, wenn das Kriterium den *Griff* einschließt und die Anliegen an Architekt und UX stehen.

**Stellungnahme.**
