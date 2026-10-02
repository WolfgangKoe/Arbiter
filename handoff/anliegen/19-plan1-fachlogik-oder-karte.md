# Plan 1: Reicht Item 1 bis zur Karte?

19 · Kritik · von Architekt (Technik) → Planer · Runde 1/3 · angenommen

## Runde 1
**Befund.**
1. Die Empfehlung im [Plan](../plan.md) verspricht: „Danach können zwei Spieler die
   Reihenfolge … durchgehen“. Das braucht Oberfläche und Karte. Deren Fragen schiebt derselbe
   Plan auf: Spielfeld und Zonen (09 F10), Ablage (16 F1), Rücksprung (16 F4). Ein Mockup,
   das die DoR bei UI verlangt, gibt es nicht.
2. „Aufstellen der Einheit beenden scheitert in diesem Item nicht“: Ein Test darf so eine
   *Einheit* beenden, von der kein *Modell* gesetzt ist. Nach Empfehlung A zu 16 F3 ist genau
   das eine *Sperre*; solche Tests werden in Zyklus 2 rot.

**Kosten.** Bei 1 bauen Testautor und Implementierer Karte, Ablage und Ziehen nach eigenem
Ermessen: der teuerste Teil des Altbestands (`model_drag.js`, 85.402 Zeichen) und nach der
Antwort auf 16 vermutlich Wegwerfarbeit. Bei 2 schreibt Zyklus 2 Tests von Zyklus 1 um, statt
nur neue hinzuzufügen.

**Gegenvorschlag.**
1. Item 1 ist reine Fachlogik: Akzeptanztests rufen die Funktionen, die später Flask aufruft,
   ohne Oberfläche. Der Satz in der Empfehlung wird: „Danach belegen Akzeptanztests die
   Reihenfolge; spielbar wird sie mit Spielfeld und Ablage (09 F10, 16 F1).“ Preis: Nach
   Zyklus 1 ist nichts klickbar.
   Alternative: ein Durchstich mit Flask und einer schlichten Seite ohne Karte (Zone wählen,
   Einheit wählen, Beenden), der die Schichten früh erprobt. Dann vorher ein Mockup.
2. Neue Grenze im Plan: „Akzeptanztests beenden eine *Einheit* erst, wenn alle ihre *Modelle*
   gesetzt sind.“ Die Tests bleiben nach 16 F3 gültig, ohne Mehraufwand.

**Stellungnahme.**
Angenommen, Punkt 1 ohne die Alternative und Punkt 2, umgesetzt im [Plan](../plan.md). Item 1
ist reine Fachlogik; ein Durchstich braucht ein Mockup und Kriterien zu Spielfeld und Ablage,
die es noch nicht gibt. 09 F10 und 16 sind inzwischen beantwortet; die Kriterien dazu schreibt
der Anforderungsautor für die nächsten Items. Zusätzlich prüfen die Tests bei der Sperre aus
AUF-1.4 nur Sperre und Grund, nicht, wo das Modell danach steht (16 F4).
