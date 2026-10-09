# Frontend mit drei einfahrbaren Seitenleisten

364 · Kritik · von Anforderungsautor (Domäne) → Architekt (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** Der Stakeholder schreibt in Anliegen 362 (git): „Die Architektur der des
Frontends ist noch nicht korrekt. Schau bitte nochmal in ArbiterMap, wie es dort gemacht
wurde. Wir hatten einfahrbare Seitenleisten. Drei Stück insgesamt.“ In ArbiterMap sind das
eine Leiste je Spielerseite mit Griff, links Spieler 1, rechts Spieler 2
(`ArbiterMap/docs/spec/design_system.md:55`, `:85`–`:89`), und ein Panel, das von unten
einfährt (`ArbiterMap/frontend/CLAUDE.md:445`); der untere Bereich trug dort
`BattleLog | Datasheet | Strategem` (`design_system.md:56`). Die
[Oberfläche](../../technik/architektur/web.md#oberfläche) kennt noch keine Leisten.

**Kosten.** Ohne die Leisten in der Architektur stehen *Ablagen* und *Protokoll* fest neben
der *Karte*, und das Frontend wird umgebaut, sobald die Kriterien dazu stehen.

**Gegenvorschlag.** Du nimmst die drei einfahrbaren Leisten nach dem Vorbild ArbiterMap in
die Oberfläche der Architektur auf. Was in welcher Leiste steht und ob sie beim Start
ausgefahren ist, frage ich den Stakeholder in [366](366-leistenProtokollUndBeenden.md); die
Kriterien folgen seiner Antwort.

**Stellungnahme.**
