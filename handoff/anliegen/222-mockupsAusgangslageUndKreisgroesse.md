# Mockups: Ausgangslage, leere Einheit und Kreisgröße

222 · Kritik · von Fachkritiker (Domäne) → UX · Runde 2/3 · offen

## Runde 1
**Befund.** Kritik an `domaene/mockups/que-2.html`, `auf-4.html`, `vorschlag.css` gegen
QUE-2 und AUF-4 (Plan 3): 1. Die Ausgangslage (AUF-4.4 „keinen, solange es keiner ist“,
AUF-4.6 „vor der Wahl … in keiner der beiden“) zeigt kein Mockup. 2. Die *Einheit in
Aufstellung* ohne fehlende *Modelle* (AUF-4.3 „auch wenn keines mehr fehlt“) zeigt kein
Mockup. 3. Die Ränder von `.modell` und Zone vergrößern die sichtbare Fläche über
*Durchmesser* und *Tiefe* hinaus (QUE-2.4, QUE-2.5).

**Kosten.** Ohne 1 und 2 baut der Implementierer ohne Vorlage; ohne 3 ist der Test grün,
während das Bild abweicht.

**Gegenvorschlag.** 1. `auf-4-ausgangslage.html`. 2. In `auf-4.html` alle Boyz *gesetzt*,
ihre unitCard ohne Modelle. 3. Kreis und Zone ohne Rand.

**Stellungnahme.**
Angenommen, alle drei Punkte umgesetzt: `auf-4-ausgangslage.html` neu; in `auf-4.html` zehn
Boyz gesetzt; `.modell`, `.aufstellungszone`, `.spielfeld` nur `fill`.

## Runde 2
**Befund.** Punkte 1 bis 3 sind in Ordnung umgesetzt (`auf-4-ausgangslage.html` gegen
`ausgangslage.yaml` geprüft). Neu: Die zwei Boyz bei `cx="8.6"` in `auf-4.html` und
`que-2.html` reichen bis 8,6 + 0,63 = 9,23″, die *Tiefe* ist 9″ (`onlyWar.yaml`). Ihre
*Base* liegt nicht *ganz in* der *Aufstellungszone*; nach AUF-3.2 ist das gesperrt, der
Zustand ist ohne Übergehen nicht erreichbar.

**Kosten.** Der Stakeholder gibt ein Bild frei, das die Regel verletzt, die der Bau
durchsetzen soll; der Implementierer übernimmt die Lage. Umsetzung: zwei Zahlen je Datei.

**Gegenvorschlag.** Die fünf Boyz je Reihe bei `cx` höchstens 8,37, etwa 2,0 / 3,4 / 4,8 /
6,2 / 7,6, in beiden Dateien gleich.

**Stellungnahme.**
