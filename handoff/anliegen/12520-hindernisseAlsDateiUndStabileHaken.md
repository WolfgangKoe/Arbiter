# Hindernisse als Datei in handoff, Haken im Fortschritt stabil

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: offen
Wartet auf: Prozessphase

## Runde 1
**Befund.** Wortlaut des Stakeholders:
„Ein Wunsch für die nächste Prozessphase in Bezug auf den gezeigten Screenshot:
1. Ja, ich möchte, dass Hindernisse im Fortschritt eingefügt werden.
2. Hindernisse sollten ähnlich einem Anliegen ausführlich als Markdown-Datei in Handoff angelegt werden und nicht im Fortschritt. Im Fortschritt soll einfach [  ] Hindernis - <hklmnop> nameDesHindernisses angezeigt werden. Sonst geht die Übersicht verloren.
3. Sobald das Hindernis in handoff als erledigt markiert ist, muss auch der Haken im Fortschritt zu sehen sein. Ob der Haken gesetzt wird, wenn die Datei in Handoff auf ‚erledigt‘ gesetzt wird oder ob das beim Löschen in einem Committ passiert, ist mir egal.
4. Mein Eindruck ist, dass das Setzen von Haken im Fortschritt etwas kaputt ist. Ein Haken wird gesetzt, dann verschwindet der wieder. Dann wird er wieder gesetzt. Das gefällt mir so nicht. Entweder der Haken ist gesetzt oder er ist es nicht. Der Fortschritt muss auch nicht bei jedem Committ exakt übernommen werden.“
Screenshot: [Plan](../plan.md), Zeilen 98–100: Hindernis-Zeilen unter „Fachkritiker: Kritik an den Tests zu Item anhaltenAufDemWeg“, darunter eine lange Liste von Testnamen.

Befunde dieses Zyklus zum Fortschritt, für die Prozessphase:
- (p) und (q) aus dem Startprompt des Koordinators sind schon bekannt und hier nicht wiederholt.
- Ein Commit je Item scheiterte, weil der Hook Dateien änderte, die zugleich beiseitegelegt waren (verwandt: Anliegen 11100).
- Eine Statusänderung des Implementierers an Anliegen 11920 ging verloren.
- `erledigteLoeschen` löscht erledigte Anliegen, bevor das Hindernis als beseitigt gilt (Anliegen 12440).
- Das Abhaken zählte Kriterien mit, die ein Item nur als Abhängigkeit nennt.
- Das Abhaken vergab Nummer 12082 außerhalb des zugeteilten Bereichs.
- Der Planer sah seinen Haken gesetzt, obwohl der Befehl keinen offenen Schritt fand.
- Der Implementierer brach bei Item anhaltenAufDemWeg an der Tokengrenze ab, noch in der Analyse.

Verwandt: [Fortschritt](../../prozess/ablauf/fortschritt.md), Anliegen 11500 (Abhaken kennt nur das Hindernis des eigenen Schritts).

**Kosten.**

**Gegenvorschlag.**

**Stellungnahme.**
