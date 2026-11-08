# Vertrag: Querschnitt · Ziehen

Was alle Phasen beim Ziehen teilen; Anfragen, Antworten und Prüfung:
[Anfragen](anfragen.md), die anderen: [Architektur](../../../architektur.md#schichten).

- **V8** Pointer Events am Dokument, ein Weg für Maus und Finger (QUE-3.4,
  `touch-action: none` an `.karte`). Ein Zug beginnt erst, wenn der Zeiger in x oder y mehr
  als 4 px (`zugschwelle`, wie `dragStartThresholdPx` in ArbiterMap) vom Startpunkt abweicht.
  Ohne Zug ist es ein Klick; was er bedeutet, nennt die Datei der Phase. Den Punkt in Zoll
  rechnet die Seite mit `getScreenCTM().inverse()` der `.karte`.
  Gezogen wird nur ein `.karte .modell`; Punkt des Zugs: seine vorige *Stelle* plus Weg des
  Zeigers seit dem Greifen (AUF-8.7), ein Weg nur in x lässt y exakt. Ein Zug wählt nie aus.
  Beim Druck auf ein gezogenes Element verhindert die Seite Markieren und das eigene Ziehen
  des Browsers (`preventDefault` auf `pointerdown` und `dragstart`, `user-select: none` an
  `.armeeKarte`); sonst bricht `pointercancel` den Zug ab.
- **V10** Zeigen beim Ziehen: `GET …/modelle/<m>/stelleBeimLoslassen?x=<x>&y=<y>` → 200 mit
  `modelle[]`, je *Modell*, das das Loslassen am Punkt *setzen* würde (Datei der Phase),
  `spieler`, `einheit`, `nummer` wie V1 und `x`, `y`. *Sperre*: 409 wie V6. Zahlen wie V5,
  fehlt eine: 400. Warum `GET`: Die Abfrage ändert nichts (V4).
  Eingaben (AUF-29, BEW-17): `x`, `y` der Punkt; `zuvorX`, `zuvorY` die zuvor gezeigte
  *Stelle* des gezogenen *Modells*, beide oder keine (sonst 400), ohne sie die *Stelle* vor
  dem Ziehen; `angehaltenAufDemWeg=true`, wenn die letzte 200 es nannte. Die 200 nennt
  `"angehaltenAufDemWeg": true`, wenn BEW-17.1 bei dieser oder einer früheren Eingabe
  griff (BEW-17.4), sonst fehlt der Schlüssel. Warum Eingaben statt Zustand: Die Domäne
  merkt sich kein Ziehen; dieselben Eingaben zeigen und *setzen* dasselbe (D2).
  Mit dem Punkt des Zugs (V8) fragt die Seite je Zeigerbewegung im *Spielfeld* nach,
  höchstens eine Anfrage zugleich, danach nur mit dem jüngsten Punkt; `zuvorX`, `zuvorY`
  sind `x`, `y` des gezogenen in der letzten 200 dieses Zugs, vor ihr fehlen sie. Auf 200
  setzt sie `cx`, `cy` jedes genannten Kreises, sonst bleibt jeder, wo er ist, auch bei 409
  (ohne `sperrmeldung`: keine Handlung). Eine Antwort nach dem Loslassen verwirft sie.
  Beim Loslassen schickt sie V5 mit den Eingaben als Körper (`angehaltenAufDemWeg` als
  JSON-Wahrheitswert): im *Spielfeld* die der zuletzt beantworteten Abfrage dieses Zugs,
  wenn deren Punkt der Punkt des Zugs ist, sonst die der nächsten Abfrage zu ihm. Neben dem
  *Spielfeld* (*neben der Karte*, auch auf einer *Armeeliste*) die der letzten vor dem
  Loslassen beantworteten 200 dieses Zugs, auch mit leerem `modelle[]`; ohne sie keine
  Anfrage: Sie zeichnet den letzten Stand. Warum die Eingaben: Mit ihnen *setzt* die
  Handlung genau die gezeigten *Stellen* (AUF-28, BEW-17.2), ein zweites Mal am selben
  Punkt rückte sie weiter; welche *Modelle* mitgehen, entscheidet die Domäne. Prüft am Bildschirm:
  halten, auf die Antwort warten, `cx`, `cy` lesen, am selben Punkt oder neben dem
  *Spielfeld* loslassen; die *Stelle* danach gleicht den gelesenen Werten exakt (B3).
