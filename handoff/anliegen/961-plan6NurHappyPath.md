# Plan 6 nur mit dem Happy Path: Verweise auf Randfälle lösen

961 · Kritik · von Planer → Anforderungsautor · Runde 1/3 · erledigt

## Runde 1
**Befund.** Der Stakeholder gibt Plan 6 nicht frei (Kommentar unter
[Freigabe](../plan.md#freigabe)): Er will genau seinen Happy Path, alles andere sind Randfälle.
[Plan 6](../plan.md) ist darauf neu geschnitten. Die Items nennen Kriterien, die auf Randfälle
verweisen oder ihnen fehlen:
1. AUF-22 und AUF-3.9 kommen in Plan 7 (neuer Hinweis „Spieler 2 ist an der Reihe“). Damit
   bleiben AUF-3.8 und AUF-7.2 stehen, statt nach
   [801](801-plan6KriterienDieEntfallen.md) zu entfallen. AUF-19.4 nennt aber 22.1, AUF-12.5
   nennt 22.2.
2. AUF-23 kommt in Plan 7. AUF-8.3 entfällt trotzdem: Ein einzelnes *Modell* geht nicht zurück
   (Anliegen 890). Für Plan 6 sagt dann kein Kriterium, was ein Zug auf die eigene *Ablage* tut.
3. [960](960-happyPathOffeneEntscheidungen.md) F3, Annahme A: höchstens eine *ausgewählte*
   *Einheit*. Das ändert AUF-5.3 (getestet), AUF-18.1 („als einzige“); AUF-19.5 entfällt.
4. [945](945-etappe1OhneFehlendeModelle.md), Annahme A, die Antwort des Stakeholders beschreibt
   genau sie: AUF-10.2, 10.4 und 10.5 erreicht niemand; Verweise darauf stehen in AUF-10 (Zweck),
   12.4, 13, 17.1.
5. Item 3 baut AUF-11, AUF-6 entfällt mit Test; [AUF-1](../../domaene/anforderungen/phasen/aufstellen/reihenfolge.md)
   nennt am Bildschirm noch AUF-6.

**Kosten.** Ohne Nachzug testet der Testautor in Plan 6 Randfälle mit oder Verweise ins Leere,
und das Plan-6-Inkrement zeigt Hinweise, die der Stakeholder gerade abgelehnt hat.

**Gegenvorschlag.** Bestehende Regeln vor neuen (Ich 4):
1. In AUF-19.4 und 12.5 AUF-7.2 statt 22.1 und 22.2 nennen; 3.8 und 7.2 nicht löschen.
   AUF-22 und 3.9 bleiben unverändert für Plan 7 (beide ohne Test).
2. AUF-16.6 (ohne Test) um die eigene *Ablage* erweitern: Das *Modell* springt still zurück, kein
   *Grund*, bis AUF-23 in Plan 7 kommt.
3. Nach F3 A ein neues Kriterium, das AUF-5.3 ersetzt; AUF-19.5 löschen. Antwortet der
   Stakeholder B, bleibt 19.5 für Plan 7, und du legst fest, was ein Klick bei zwei
   *ausgewählten* *Einheiten* bis dahin tut, ohne neuen *Grund*.
4. AUF-10.2, 10.4, 10.5 löschen und die Verweise nachziehen.
5. AUF-1 nach AUF-11 ausrichten.
Kein Kriterium in Plan 6 verlangt einen neuen *Grund* oder Knopf, außer „Roll-off gewonnen“
(AUF-11) und dem Umschalter (AUF-20).

Erledigt, wenn: Jedes Kriterium, das die drei Items von Plan 6 nennen, existiert und verweist nur
auf Gebautes oder auf Kriterien dieser Items; AUF-10.2, 10.4, 10.5 sind gelöscht; deine
Stellungnahme nennt die neuen und gelöschten Kennungen, damit ich die Items nachziehe.

**Stellungnahme.** Angenommen, eine Abweichung bei 4.
1. AUF-19.4 nennt 7.2, 7.3, 12.1; AUF-12.5 nennt 7.2, 8.4, 12.1, 16.3. AUF-22 sagt, dass es 7.2
   auch dort ersetzt.
2. AUF-16.6 um die eigene *Ablage* erweitert; AUF-23 sagt, dass es das ersetzt.
3. Neu AUF-5.11 (nur sie *ausgewählt*); 5.8, 20.2, 18.1 und das Glossar (*Auswahl*) nachgezogen.
   Gelöscht: AUF-19.5, 5.5 (ohne Test). Entfällt mit Test: AUF-5.3.
4. Gelöscht: AUF-10.5. AUF-10.2 und 10.4 haben Tests; sie zu löschen machte die
   Rückverfolgung rot. Sie entfallen mit Test wie in 801. Die Tests von AUF-12.4 prüfen
   ‚Modelle fehlen‘, also neu AUF-12.7 ohne 10.2; 12.4 entfällt mit Test. Ohne 10.2 geändert:
   AUF-10 (Zweck), 13, 17.1 (sein Test gilt weiter). Aus QUE-4 (Zweck) und dem Glossar
   ist *vernichtet* entfernt.
5. AUF-1 nennt AUF-6 nicht mehr.

Für die Items: neu AUF-5.11, 12.7; entfällt mit Test AUF-5.3, 10.2, 10.4, 12.4.
AUF-5 (1.285 Zeichen) liegt bis zum Löschen über 1.200.
