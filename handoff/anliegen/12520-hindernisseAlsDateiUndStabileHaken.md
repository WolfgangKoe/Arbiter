# Hindernisse als Datei in handoff, Haken im Fortschritt stabil

Form: Auftrag
Von: Stakeholder
An: Organisationsentwickler
Runde: 1/3
Status: erledigt
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

**Stellungnahme.** Eingeplant als P2 der [Retro 10](../retro.md): 1 bis 4 wie gewünscht, das
Anliegen ist die Datei des Hindernisses. Von den Befunden darunter: Abhängigkeit und Nummer
außerhalb des Bereichs P3, Commit und Tokengrenze P4, die übrigen P2 je mit Scheiter-Test.
`angenommen`, sobald die Regel steht.

Umgesetzt mit P2 der [Retro 10](../retro.md), `erledigt` folgt dessen Haken: 1 und 2: Unter
dem Schritt steht nur `- [ ] Hindernis <nr> <Titel>`, der Text steht im Anliegen. 3: Der Haken
wird `[x]`, sobald das Anliegen angenommen oder erledigt und committet ist. 4: Ein gesetzter
Haken eines Hindernisses bleibt; Haken der Schritte bleiben beim Neuschreiben (Anliegen 982). Regel:
[Standregeln](../../prozess/regeln/standregeln.md), Zeile Anliegen 490 Teil 2; Ablauf:
[Fortschritt](../../prozess/ablauf/fortschritt.md). Von den Befunden darunter: 12440 steht in
derselben Regel, Abhängigkeit und Nummer in P3, Commit und Tokengrenze in P4. Die verlorene
Statusänderung an 11920 und der Haken des Planers ohne offenen Schritt haben keinen eigenen
Mechanismus bekommen; tritt eins davon wieder auf, kommt es in die nächste Retro.
Kommentar: Schauen wir mal, ob das funktioniert.
