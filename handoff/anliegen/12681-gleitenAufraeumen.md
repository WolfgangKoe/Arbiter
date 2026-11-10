# Gleiten aufräumen: zwei Typen für eine Aussage, sechs Parameter, Übergehen ab jetzt

Form: Kritik
Von: Architekt
An: Implementierer
Runde: 1/3
Status: offen
Wartet auf: Technikphase 11

## Runde 1
**Befund.**
1. `Geglitten` (`phasen/aufstellen/anhaltenAufDemWeg.py`) und `Gezeigt`
   (`querschnitt/setzen.py`) tragen dieselben zwei Felder; beide *Phasen* bauen das eine aus
   dem anderen ab (Wir 3).
2. `stellenMitGründenNachDemZiehen` hat sechs Parameter mit `# noqa: PLR0913`; `stellen` und
   `gegner` reicht die *Schlacht* bei jedem Aufruf gleich herein (Es, I).
3. `übergangen` kürzt an der *Spielfeldkante* ab der jetzigen *Stelle*;
   [V18](../../technik/architektur/vertrag/schlacht/uebergehen.md) rückt „mit der *Stelle* vor
   dem Ziehen und der jetzigen als zuvor“, `Angebot` merkt sich die *Stelle* vor dem Ziehen
   nicht. Anders nur an der *Spielfeldkante*.
4. Die Vorlage `protokollGrund` in `frontend/index.html` trägt noch „über eine Base“.

**Kosten.** Leser suchen zwei Typen für eine Aussage; die Signatur wächst mit jedem Item
(*Fliegen*); V18 und Code weichen am Rand ab.

**Gegenvorschlag.** 1: `gleiten` gibt `Gezeigt` zurück, `Geglitten` entfällt (Glossar:
Anforderungsautor). 2: `gegner` und `stellen` als ein Wert der *Schlacht* übergeben oder
`Bewegungsphase` liest sie aus einem Parameter-Objekt. 3: `übergangen` ruft dieselbe Rechnung
wie das Loslassen mit `Weiterrücken(jetzige, …)` und der gemerkten *Stelle* vor dem Ziehen.
4: ein *Grund*, den es gibt, etwa „Bewegungsweite“.

**Stellungnahme.** Teils erledigt, bleibt offen. Punkt 2 erledigt:
`stellenMitGründenNachDemZiehen` und `angebotNachDemZiehen` nehmen drei Parameter, kein
`# noqa: PLR0913` mehr. Offen: Punkt 1 (`Geglitten` in `anhaltenAufDemWeg.py` und `Gezeigt`
in `querschnitt/setzen.py` mit denselben zwei Feldern; `Aufstellung` baut das eine ins andere
um), Punkt 3 (V18 und `übergangen` an der *Spielfeldkante*, hängt an 15461), Punkt 4
(`protokollGrund` in `frontend/index.html` trägt noch „über eine Base“; der *Grund*
„Bewegungsweite“ existiert).
