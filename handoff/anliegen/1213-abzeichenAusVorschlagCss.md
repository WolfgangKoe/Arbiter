# Das Abzeichen „in Aufstellung“ aus vorschlag.css streichen

Form: Kritik
Von: Architekt
An: Ux
Runde: 1/3
Status: offen
Wartet auf: Domänenphase

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet auf die nächste Phase. Im Plan 6 hat der
Stakeholder entschieden, dass die *Einheitenkarte* kein „in Aufstellung“ mehr zeigt; das
Mockup [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html) hat deshalb kein
Abzeichen. In [vorschlag.css](../../domaene/mockups/vorschlag.css) stehen trotzdem noch
`.einheitenKarte.inAufstellung` (Zeile 137) und `.einheitenKartenAbzeichen` (Zeile 149).
Kein Mockup verwendet sie. Die Komponentenseite ist nach
[O3](../../technik/architektur/oberflaeche.md) aus `vorschlag.css` gebaut, und dort streicht
der Implementierer beide Klassen (Anliegen 1212).
Die Entscheidung dazu steht in [1191](1191-abzeichenInAufstellungOhneQuelle.md).

**Kosten.** Ein neues Mockup könnte das Abzeichen aus `vorschlag.css` übernehmen, das die
Komponentenseite dann nicht mehr kennt.

**Gegenvorschlag.** Beide Regeln aus `vorschlag.css` streichen. Erledigt, wenn
`grep -n "inAufstellung\|einheitenKartenAbzeichen" domaene/mockups` nichts findet.

**Stellungnahme.**
