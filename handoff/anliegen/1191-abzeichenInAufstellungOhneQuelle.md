# Das Abzeichen „in Aufstellung“ hat keine Quelle mehr

1191 · Kritik · von Implementierer → Architekt · Runde 1/3 · offen · wartet auf 1213

## Runde 1
**Befund.** Einordnung nach Ich 3: wartet auf die nächste Phase. Die Beispiele
[spielstand.json](../../technik/architektur/vertrag/spielstand.json) und
[sperre.json](../../technik/architektur/vertrag/sperre.json) haben in der *Ablage* kein
`inAufstellung` mehr, das Mockup [auf-18-ausgewaehlt](../../domaene/mockups/auf-18-ausgewaehlt.html)
kein Abzeichen. Ich habe `inAufstellung` aus `darstellung.py` und `seite.js` und das Abzeichen
aus dem Template in `index.html` genommen. In `komponenten.html` und `komponenten.css` stehen
`.einheitenKarte.inAufstellung` und `.einheitenKartenAbzeichen` noch; ohne Template sind sie
nach O3 tot.

**Kosten.** Tote Klassen in der Komponentenseite.

**Gegenvorschlag.** Beide Klassen aus `vorschlag.css` und der Komponentenseite streichen, oder
entscheiden, dass das Abzeichen bleibt (dann braucht der Vertrag das Feld wieder).

**Stellungnahme.** Entschieden ist die erste Variante: Das Abzeichen entfällt als
Komponente. Der Stakeholder hat es im Plan 6 abgelehnt („kein ‚in Aufstellung‘“), deshalb
bekommt der Vertrag das Feld nicht zurück. Die Arbeit verteilt sich nach Schreibpfaden: Du
streichst `.einheitenKarte.inAufstellung` und `.einheitenKartenAbzeichen` aus
`komponenten.css` und `komponenten.html`; das steht als Befund 3 in
Anliegen 1212 und hält auf. UX streicht beide aus
`vorschlag.css` ([1213](1213-abzeichenAusVorschlagCss.md)), das wartet auf die
Domänenphase. Auf `angenommen` setze ich dieses Anliegen, sobald 1213 erledigt ist.
