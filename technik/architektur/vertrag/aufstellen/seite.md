# Vertrag: Aufstellen · Seite

Abschnitt der *Aufstellung*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

- Knöpfe (V7): „Aufstellen der Einheit beenden“ immer, denn AUF-12.7 nennt den *Grund*
  nach AUF-7.4; davor „Einheit zurücklegen“, wenn `einheitInAufstellung` nicht `null` ist
  (AUF-23.4).
- Klick (V8): auf einer `.einheitenKarte` [V2](auswahl.md); auf einem *Modell* der *Einheit*,
  die in der *Armeeliste* `ausgewählt` trägt, V9 (AUF-25.1, 25.2), auf einem anderen *Modell*
  [V14](../bewegung/auswahl.md) (AUF-20.6); sonst im *Spielfeld* `karteAnklicken` mit dem
  Punkt, sonst nichts. Warum die *Armeeliste*: Ist die *Ebene* ein *Modell*, tragen die
  anderen *Modelle* kein `ausgewählt` (AUF-25.4).
- Zug (V8): Trägt das gezogene *Modell* `ausgewählt`, folgen alle mit `ausgewählt` um
  denselben Weg (AUF-21.1). Beim Loslassen im *Spielfeld* `modellLoslassen`, auch über dem
  Startpunkt (AUF-8.2), daneben nach [V10](ziehen.md), auch auf einer `armeeKarte`.
