# Vertrag: Bewegung · Ziehen

Abschnitt der *Bewegungsphase*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt/).

V10 in jeder *Phase* der *Schlacht*: `stellenBeimLoslassen` (Signatur:
[Aufstellen · Ziehen](../aufstellen/ziehen.md)) nennt in `stellen` jedes
*Modell*, das `modellLoslassen` dort *setzen* würde (BEW-1.7), mit Anhalten an der
*Bewegungsweite* ([V16](handlungen.md)), ohne Hineinrücken, mit denselben Wächtern und
*Gründen*: bei einer *Sperre* 409, die *Karte* zeigt weiter die letzte 200 dieses Zugs.
Außerhalb der *Bewegungsphase* ist die Antwort 200 mit leerem `modelle[]` (QUE-10.5). Warum
409: BEW-1.5 *setzt* nur ohne *Sperre*; die *Karte* zeigt keine *Stelle*, an die nichts
*gesetzt* würde.

**Anhalten vor fremden Bases** (BEW-17, 19): Ohne 17.1 zeigte V10 die *Stellen* nach V16
ab der *Stelle* vor dem Ziehen; ist `angehaltenAufDemWeg` die Eingabe, hält es auf der
Strecke von zuvor dorthin zudem nach 6.2 an (17.4). Nur wenn dort ein *Modell* der *Ebene*
ein Hindernis des Gleitens ([Aufstellen · Ziehen](../aufstellen/ziehen.md)) *überdeckt*,
gleitet es ab zuvor zum Punkt der Abfrage, ungekürzt (17.1): Einen Teil nach 29.2 nimmt es
nur, wenn auf ihm ab zuvor die drei Anteile von V16 1 sind; auf der Strecke nach 29.1 gilt
der kleinste aus ihr und den drei Anteilen dort (17.3, 6.3). Warum geprüft an den *Stellen*
nach V16: Dort fragt 17.1 („wo BEW-1.7 und 6.4 sie zeigen würden“); am ungekürzten Punkt
geprüft, sperrte QUE-1.2 vor einer *Base* an der *Bewegungsweite*, wenn der Zeiger hinter
ihr steht, und eine *Base* hinter der *Bewegungsweite* lenkte das *Modell* ab. Warum
gegleitet zum ungekürzten Punkt: Auf der Strecke von zuvor zu einer *Stelle* nach V16
hielten BEW-3.1 und 6.1 nie früher an (Kreis und Rechteck sind konvex), 17.3 nennt sie
aber. Danach prüft QUE-1
wie V15, fremd nach AUF-29.3, so sperrt QUE-1.2 bei der ganzen *Einheit* keines
ihrer *Modelle* (BEW-19). *Angehalten* nach BEW-3.1 oder 6.2 (für [V18](../schlacht/uebergehen.md))
ist es, wenn deren Anteil auf der Strecke zum Ziel oder nach 17.3 und 17.4 der kleinste und
kleiner 1 ist. Warum hier: V16 kennt nur die gerade Strecke, das Gleiten nur *Bases*; die
*Bewegungsphase* setzt beides zusammen (`phasen/bewegung/`). Mit *Fliegen*: [Fliegen](fliegen.md).

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
den gelesenen (B3), für eine *Einheit* als *Ebene* jedes ihrer *Modelle*. BEW-17 am Dienst
wie AUF-29 ([Aufstellen · Ziehen](../aufstellen/ziehen.md)); 17.3 und 17.4 mit einem
*Modell* des anderen *Spielers* neben der Strecke ab zuvor, nicht neben der ab der *Stelle*
vor dem Ziehen; 17.1 mit einer fremden *Base* an der *Bewegungsweite* und dem Punkt hinter
ihr, auch nach einer Abfrage, die davor anhielt: 200, vor ihr angehalten; mit einer *Base*
hinter der *Bewegungsweite* und dem Punkt schräg auf ihr: die *Stellen* nach V16; 17.2: V5
mit den Eingaben der letzten Abfrage, 200, *Stellen* wie sie. BEW-8.3 nach 17.1 und 17.4:
angeboten genau dann, wenn BEW-3.1 oder 6.2 der kleinste Anteil ist.
