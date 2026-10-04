# Mockups: Ausgangslage, leere Einheit und Kreisgröße

222 · Kritik · von Fachkritiker (Domäne) → UX · Runde 1/3 · offen

## Runde 1
**Befund.** Kritik an `domaene/mockups/que-2.html`, `auf-4.html`, `vorschlag.css` gegen
QUE-2 und AUF-4 (Plan 3). Was gezeigt wird, stimmt: Zonen, Farben (QUE-2.6, AUF-4.6, AUF-4.7
nach `design_colors.md:51`, `:53`, `:72` bis `:74`), Kreise mit r 0,63″ = 32 mm, alle Bases
*ganz in* ihrer Zone, ohne Überdecken, und der Zustand ist nach AUF-1 erreichbar (Spieler 2
nicht *Gewinner*, hat Necron Warriors *aufgestellt*, Spieler 1 setzt Boyz, 3 + 7 = 10).
Es fehlen Fälle, die die Kriterien ausdrücklich regeln:
1. Ausgangslage. AUF-4.4 „keinen, solange es keiner ist“ und AUF-4.6 „vor der Wahl … in
   keiner der beiden“ zeigt kein Mockup. `.aufstellungszone.ohneSpieler` steht nur im CSS,
   in keinem Markup; ein Kopf ohne *an der Reihe* auch nicht. Gerade diesen Zustand sieht
   der Stakeholder am Ende des Zyklus (Plan, Empfehlung: „Zonen ohne Farbe, … keinen an der
   Reihe, kein Modell auf der Karte“), und der Implementierer übernimmt Markup ohne
   Umschreiben (Ablauf, Technikphase 3, Anliegen 151): Für den einzigen Zustand, den der
   Bau erreicht, hat er keine Vorlage.
2. AUF-4.3 „auch wenn keines mehr fehlt“: Eine *Einheit in Aufstellung*, deren *Modelle*
   alle *gesetzt* sind, bleibt bis *Aufstellen der Einheit beenden* in der *Ablage*. Wie sie
   aussieht (Name und Abzeichen, keine Modelle), zeigt kein Mockup.
3. QUE-2.4 „Kreis mit dem *Durchmesser* seiner *Base*“: Der Rand (`.modell`,
   `stroke-width: 0.08`) liegt in SVG mittig auf dem Kreis; sichtbar ist der Kreis 1,34″
   statt 1,26″ (rund 34 statt 32 mm). Zwei *Bases* mit *Abstand* unter 0,08″ sehen
   überdeckt aus, obwohl sie es nicht sind. Ebenso ragt der Zonenrand (`stroke-width: 0.15`)
   0,075″ über die *Tiefe* hinaus (QUE-2.5); wer nach Augenmaß „ganz in“ beurteilt, wird
   getäuscht. Ziel: „Abstände zieht man auf der Karte“.

**Kosten.** Ohne 1 baut der Implementierer die Ausgangslage aus eigener Hand, oder er
schreibt das Mockup um, was 151 ausschließt; der Stakeholder gibt ein Bild frei, das er in
diesem Zyklus nicht zu sehen bekommt. Ohne 2 bleibt offen, ob eine leere Einheit erscheint
(Testautor und Implementierer raten). Ohne 3 prüft der Test `r` und ist grün, während das
Bild abweicht. Umsetzung: eine Datei mehr, ein Beispielinhalt geändert, zwei CSS-Zeilen.

**Gegenvorschlag.**
1. Zusätzlich `domaene/mockups/auf-4-ausgangslage.html`: beide Zonen `ohneSpieler`, Kopf
   ohne `anDerReihe` und ohne `gameHeaderAnDerReihe`, kein Modell auf der Karte, beide
   *Ablagen* vollständig nach `ausgangslage.yaml`. Den Link im Item und im Plan zieht der
   Planer nach.
2. In `auf-4.html` sind alle zehn Boyz *gesetzt*: Ihre unitCard behält Name und Abzeichen,
   ohne Modelle; der Warboss zeigt weiter die Liste. Damit sind beide Formen einer unitCard
   im selben, nach AUF-1 erreichbaren Zustand zu sehen.
3. `.modell` ohne Rand (nur `fill`), Zonenrand ebenso oder innen liegend, sodass die
   sichtbare Fläche genau Kreis und Band ist.

**Stellungnahme.**
