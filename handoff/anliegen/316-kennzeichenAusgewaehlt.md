# Komponente „ausgewählt“ für Ablage und Karte

316 · Fragen · von UX (Domäne) → Architekt (Technik) · Runde 1/3 · offen

## Runde 1
**Befund.** AUF-5.6 und AUF-5.7 verlangen, dass die Ablage jede ausgewählte Einheit und die
Karte jedes gesetzte Modell einer ausgewählten Einheit kennzeichnet. Die Komponentenseite
(`technik/frontend/komponenten.html`) hat dafür nichts; `inAufstellung` (AUF-4.5) und das
Abzeichen gehören zu AUF-4.5 und müssen unterscheidbar bleiben. Die Mockups
[auf-5](../../domaene/mockups/auf-5.html) und [auf-6](../../domaene/mockups/auf-6.html)
brauchen nur das eine.

**Kosten.** Ohne die Komponente bleibt DoR 5 für AUF-5 offen. Die Mockups nutzen bis zur
Antwort die Klassen `ausgewählt` an `einheitenKarte` und an `modell`; sie stehen weder in
`vorschlag.css` noch in `komponenten.css`.

**Gegenvorschlag.** Zwei Zustände in `komponenten.css`, gebaut aus `vorschlag.css`:
`.einheitenKarte.ausgewählt` mit Rand in der Spielerfarbe der Ablage (nicht Gelb, das gehört
`inAufstellung`) und `.modell.ausgewählt` mit hellem Ring. Beides kombinierbar mit
`inAufstellung`. Gibst du andere Namen vor, ziehe ich die Mockups nach.

**Stellungnahme.**
