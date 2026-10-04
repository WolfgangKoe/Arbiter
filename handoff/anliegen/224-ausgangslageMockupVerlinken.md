# Mockup der Ausgangslage in Item und Plan verlinken

224 · Kritik · von Fachkritiker (Domäne) → Planer · Runde 1/3 · erledigt

## Runde 1
**Befund.** Nach Anliegen 222 gibt es `domaene/mockups/auf-4-ausgangslage.html`: beide
Zonen ohne Farbe, keiner *an der Reihe*, kein *Modell* auf der *Karte* (AUF-4.4, AUF-4.6).
Weder `domaene/items/anzeige-der-aufstellung.md:8` noch `handoff/plan.md:14` verlinken es;
der Plan sagt zudem, die Mockups zeigen „einen Zustand mit Spieler 1 an der Reihe“.

**Kosten.** Der Stakeholder gibt Plan 3 frei, ohne das Bild zu sehen, das er am Ende des
Zyklus als einziges erreicht; Testautor und Implementierer finden die Vorlage nicht.
Umsetzung: ein Link im Item, ein Link und ein Halbsatz im Plan.

**Gegenvorschlag.** Item und Plan verlinken beide Mockups von AUF-4: Ausgangslage und
Zustand mit Spieler 1 *an der Reihe*.

**Stellungnahme.** Angenommen und umgesetzt. `domaene/items/anzeige-der-aufstellung.md`
(Abhängigkeit) verlinkt beide Mockups, Ausgangslage und Spieler 1 an der Reihe. Der Link auf
den CSS-Vorschlag fällt dort weg, damit das Item unter 400 Zeichen bleibt; er steht im
Kopf beider Mockups und im Plan. `handoff/plan.md` verlinkt unter Item 2 beide Mockups und
sagt nun: die Ausgangslage ist das Bild am Ende des Zyklus, „Spieler 1 an der Reihe“ zeigt
Farben und Abzeichen.
