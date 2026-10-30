# Vertrag: Bewegung · Ziehen

Abschnitt der *Bewegungsphase*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

V10 in jeder *Phase* der *Schlacht*: `stellenBeimLoslassen(modell, stelle)` nennt jedes
*Modell*, das `modellLoslassen` dort *setzen* würde (BEW-1.7), mit Anhalten an der
*Bewegungsweite* ([V16](handlungen.md)), ohne Hineinrücken, mit denselben Wächtern und
*Gründen*: bei einer *Sperre* 409, die *Karte* zeigt weiter die letzte 200 dieses Zugs.
Außerhalb der *Bewegungsphase* ist die Antwort 200 mit leerem `modelle[]` (QUE-10.5). Warum
409: BEW-1.5 *setzt* nur ohne *Sperre*; die *Karte* zeigt keine *Stelle*, an die nichts
*gesetzt* würde.

Prüft wie im Querschnitt: V10 außerhalb der *Bewegungsphase* leer.
