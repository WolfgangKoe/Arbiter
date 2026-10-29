# Rollen in Prämissen und Ablauf verlinken

Form: Fragen
Von: Organisationsentwickler
An: Stakeholder
Runde: 1/3
Status: offen
Wartet auf: Prozessphase 9

## Runde 1
**Befund.** Deine Frage: „Müsste in den Prämissen (speziell in Quadrant 1 und/oder 2) nicht
konkret auf die Rollen der Agenten .claude/agents verwiesen werden? Oder zumindest besser
verlinkt, wenn im Ablauf eine Rolle konkret dran ist?“
1. [CLAUDE.md](../../CLAUDE.md) nennt `.claude/` nur als Ordner der Perspektive Prozess, ohne
   Link. Die Prämissen nennen Rollen allgemein („Ihr“, „jede Rolle“), mit Namen nur
   Koordinator, Architekt und Reviewer; verlinkt ist keine.
2. Im [Ablauf](../../prozess/ablauf/) stehen die 12 Rollen 119-mal in 16 Dateien, verlinkt nur
   4-mal: UX ([Domänenphase](../../prozess/ablauf/domaenenphase.md) 4), Koordinator zweimal
   ([Prozessphase](../../prozess/ablauf/prozessphase.md) 6), Moderator
   ([Status der Anliegen](../../prozess/ablauf/anliegenStatus.md)). Das ist uneinheitlich.
3. Umgekehrt nennt jede [Rollendefinition](../../.claude/agents/) ihre Schritte im Ablauf.
   Die Tabelle aller Rollen mit Link steht für dich in [doku/ueberblick.md](../../doku/ueberblick.md).
4. Bestehende Regel ([Ich 4](../../prozess/praemissen/ich.md)): [Wir 3](../../prozess/praemissen/wir.md)
   „Verlinke, statt zu wiederholen“ deckt beides ab; es braucht keine neue.

Einordnung: Zählst du in der Reihenfolge von CLAUDE.md, sind 1 und 2 die Innenseite: Absicht
und Wir. Sie gelten für jede Rolle gleich. Ein Rollenname dort bindet deine Worte an den
Zuschnitt der Rollen, der sich je Retro ändern kann (etwa der Frontend-Implementierer aus
[Rollen mit Auslöser](../../prozess/ablauf/rollenMitAusloeser.md)). Was eine einzelne Rolle tut
und darf, ist Außen, einzeln; zählst du oben links, oben rechts, ist das Quadrant 2. Dort gehört
der Link hin, als Zeile in CLAUDE.md, nicht in einer Prämissendatei.

**Kosten.** Am Bildschirm: nichts. Im Code: nichts; kein Skript liest die Phasendateien.
Token: siehe die Fragen. Arbeit: Organisationsentwickler in Prozessphase 9, ein Lauf.

**Gegenvorschlag.** Ein Link in CLAUDE.md unter „Außen, einzeln“, dazu in den drei
Phasendateien jede Rolle bei ihrer ersten Nennung als Link.

**Stellungnahme.**

**F1 · Wo verweisen die Prämissen auf die Rollen?**
A: In [CLAUDE.md](../../CLAUDE.md), Punkt „Außen, einzeln“, ergänzt: „Aufgabe und
Schreibpfade je Rolle: [Rollen](.claude/agents/)“ (Wir 3). Ein Klick führt zu allen Rollen.
Token: etwa 20 je Lauf, denn CLAUDE.md lädt jeder Lauf; der Link lädt nichts nach.
CLAUDE.md samt Ziel bleibt bei etwa 2.300 von 4.000 Zeichen. Rückweg: Zeile streichen.
B: In [Absicht](../../prozess/praemissen/absicht.md) oder [Wir](../../prozess/praemissen/wir.md)
die Rollen nennen (neu). Absicht schreibst nur du; jede neue oder umbenannte Rolle zöge eine
Änderung der Prämissen nach sich. Token: 20 bis 60 je Lauf, beide werden immer geladen.
C: Wie bisher, kein Verweis (Wir 3). Der Weg zu den Rollen führt über `doku/`.
Empfehlung: A, ein Ort, passend zum Quadranten, kaum Kosten.
Antwort: .

**F2 · Wie weit verlinkt der Ablauf die Rollen?**
A: In Domänen-, Technik- und Prozessphase jede Rolle bei ihrer ersten Nennung je Datei, dort,
wo sie einen Schritt hat (Wir 3): 19 neue Links, etwa 700 Zeichen. Token: etwa 75 je Lauf,
der eine Phasendatei liest. Die Tabelle im [Fortschritt](../../prozess/ablauf/fortschritt.md)
bleibt ohne Links, damit sie lesbar bleibt. Nachteil: Benennt jemand eine Rolle um, bleiben
tote Links; keine Prüfung findet sie (nur Text).
B: In allen 16 Ablaufdateien bei der ersten Nennung (Wir 3): etwa 64 Links, 2.600 Zeichen,
zusammen etwa 850 Token. Fortschritt und Status der Anliegen rücken an die Grenze von 6.000
Zeichen und müssten bald geteilt werden.
C: Wie bisher, 4 Links, uneinheitlich.
Empfehlung: A. Dort ist eine Rolle „dran“, und die Kosten bleiben klein.
Antwort: .
