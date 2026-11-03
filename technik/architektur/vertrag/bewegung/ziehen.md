# Vertrag: Bewegung · Ziehen

Abschnitt der *Bewegungsphase*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

V10 in jeder *Phase* der *Schlacht*: `stellenBeimLoslassen` (Signatur:
[Aufstellen · Ziehen](../aufstellen/ziehen.md)) nennt in `stellen` jedes
*Modell*, das `modellLoslassen` dort *setzen* würde (BEW-1.7), mit Anhalten an der
*Bewegungsweite* ([V16](handlungen.md)), ohne Hineinrücken, mit denselben Wächtern und
*Gründen*: bei einer *Sperre* 409, die *Karte* zeigt weiter die letzte 200 dieses Zugs.
Außerhalb der *Bewegungsphase* ist die Antwort 200 mit leerem `modelle[]` (QUE-10.5). Warum
409: BEW-1.5 *setzt* nur ohne *Sperre*; die *Karte* zeigt keine *Stelle*, an die nichts
*gesetzt* würde.

**Anhalten vor fremden Bases** (BEW-17, 19): Ziel des Gleitens
([Aufstellen · Ziehen](../aufstellen/ziehen.md)) sind die *Stellen* nach V16 ab der *Stelle*
vor dem Ziehen. Einen Teil nach 29.2 nimmt es nur, wenn auf ihm ab zuvor die drei Anteile
von V16 1 sind (17.1); auf der Strecke nach 29.1 gilt der kleinste aus ihr und den drei
Anteilen dort (17.3, 6.3). Ist `angehaltenAufDemWeg` die Eingabe und *überdeckt* das Ziel
nichts, hält es auf der Strecke von zuvor zum Ziel nach 6.2 an (17.4). Danach prüfen QUE-1
und BEW-2.5 wie V15, fremd nach AUF-29.3, so sperrt QUE-1.2 bei der ganzen *Einheit* keines
ihrer *Modelle* (BEW-19). *Angehalten* nach BEW-3.1 oder 6.2 (für [V18](../schlacht/uebergehen.md))
ist es, wenn deren Anteil auf der Strecke zum Ziel oder nach 17.3 und 17.4 der kleinste und
kleiner 1 ist. Warum hier: V16 kennt nur die gerade Strecke, das Gleiten nur *Bases*; die
*Bewegungsphase* setzt beides zusammen (`phasen/bewegung/`).

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
vor dem Ziehen; 17.2: V5 mit den Eingaben der letzten Abfrage, 200, *Stellen* wie sie.
