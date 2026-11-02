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

*Neben der Karte* loslassen (BEW-20.1 statt AUF-16.8): Die Seite schickt V5 mit dem Punkt der
letzten 200 (V10), die Domäne ändert sich nicht: Sie *setzt* dort, was V10 am selben Punkt
nannte (V16). Hält V16 dabei an, gilt V18 mit diesem Punkt als Punkt des Loslassens, nicht
mit dem des Zeigers neben der *Karte*. Warum: Die Domäne kennt nur Punkte, die die *Karte* gezeigt
hat. Außerhalb der *Bewegungsphase* und für ein *Modell* des anderen *Spielers* ist die
letzte 200 leer, V5 danach 200 ohne Änderung und ohne *Grund* (QUE-10.5, BEW-10.1). Beispiele:
die der *Aufstellung* ([Ziehen](../aufstellen/ziehen.md)); die Seite unterscheidet beim
Ziehen keine *Phase*.

Prüft wie im Querschnitt: V10 außerhalb der *Bewegungsphase* leer. BEW-20.1 am echten
Server: einen Boy über eine *Spielfeldkante* hinaus ziehen, halten, bis die *Karte* ihn nach
BEW-6.4 zeigt, die `cx`, `cy` lesen, *neben der Karte* loslassen; jede *Stelle* danach gleich
den gelesenen (B3), für eine *Einheit* als *Ebene* jedes ihrer *Modelle*.
