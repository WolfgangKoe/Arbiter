# Mockup zum Vorrücken: ein Knopf und Kreise zum Anklicken

Form: Kritik
Von: Anforderungsautor
An: Ux
Runde: 1/3
Status: angenommen

## Runde 1
**Befund.** [bew-5](../../domaene/mockups/bew-5.html) zeigt sechs Knöpfe „Vorrücken mit 1“ bis
„mit 6“; der Stakeholder will einen Knopf (Kommentar in
Anliegen 7000) und den Wurf per Klick auf einen Kreis
(Anliegen 6998 F1). Neu gefasst:
[BEW-5](../../domaene/anforderungen/phasen/bewegung/vorruecken.md),
[BEW-12](../../domaene/anforderungen/phasen/bewegung/vorrueckenZuruecknehmen.md) („Vorrücken
zurücknehmen“), [BEW-13](../../domaene/anforderungen/phasen/bewegung/grenzkreiseBeimVorruecken.md)
(sechs Kreise, dann zwei), [BEW-11](../../domaene/anforderungen/phasen/bewegung/grenzkreise.md)
mit *Einhüllender* nach deinem Auftrag 6410; 11.2 entfällt, neu 11.5.

**Kosten.** Bleibt bew-5, baut die Technikphase sechs Knöpfe, die der Stakeholder abgelehnt hat.

**Gegenvorschlag.** bew-5 nach BEW-5 und BEW-12 neu; die Kreise aus BEW-11 und BEW-13 mit deinem
Mockup zu 6410.

**Stellungnahme.** Umgesetzt: [bew-5](../../domaene/mockups/bew-5.html) (ein Knopf „Vorrücken“),
[bew-13](../../domaene/mockups/bew-13.html) (sechs Kreise zum Anklicken),
[bew-12](../../domaene/mockups/bew-12.html) („Vorrücken zurücknehmen“ nach dem Wurf),
[bew-11](../../domaene/mockups/bew-11.html) (ein *Modell* *ausgewählt*, ein Kreis; die
*Einheit* als Ganze siehe bew-5). Die Grenzen nutzen die Komponente `grenze` nach
Anliegen 7004; `wählbar` und `grenzeZahl` liegen in
[vorschlag.css](../../domaene/mockups/vorschlag.css). bew-13 zeigt ein *Modell*, weil die
sechs Kreise der ganzen *Einheit* das Höchstmaß der Datei sprengten. Offen für den Stakeholder: Der
Wurf steht als Ziffer am Kreis; ob das so gewünscht ist, sagt er beim Ansehen.
Kommentar: Ich habe mir die Mockups angesehen. Sie gefallen mir recht gut. Die Ziffern lassen wir weg. Die Auswahl der Kreise sollte etwas "flächiger" sein. Wenn ich die Linie erwischen muss, ist das aus Nutzersicht eher schwer. Die "Klick"- oder "Tipp"-Linie muss deutlich breiter sein. Ein Finger erwischt sie vielleicht, weil er selbst breit ist. Aber ein Mauszeiger braucht eine Fläche.
Stellungnahme: Umgesetzt in [bew-13](../../domaene/mockups/bew-13.html) und [vorschlag.css](../../domaene/mockups/vorschlag.css): keine Ziffern; jeder der sechs Kreise ist über die Fläche bis zum nächstkleineren wählbar, die Linie bleibt dünn. bew-11 und bew-12 haben nichts Wählbares und bleiben. Welcher Wurf in welcher Fläche gilt, ist ein Kriterium: [Anliegen 7040](7040-klickflaecheBeimVorruecken.md).
