# Vertrag: Aufstellen · Auswahl

Abschnitt der *Aufstellung*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt/).

- Spielstand (V1): `ausgewählt` an der *Einheit* nach AUF-5.12, am *Modell* nach AUF-5.7 und
  25.4; `ebene: true` nur am *Modell*, das die *Ebene* ist (AUF-25.1), sonst fehlt der
  Schlüssel. Warum: So gelten die Beispiele ohne *Ebene* unverändert.
  `einheitInAufstellung` nennt `spieler` und `einheit` der *Einheit in Aufstellung*, ohne
  eine `null` (AUF-7.1).
- **V2** `PUT /api/spieler/<nummer>/einheiten/<nummer>/ausgewählt` macht die *Einheit*
  *ausgewählt* (AUF-5.11), `DELETE` nicht (AUF-5.4); beide 200 mit dem Spielstand. Das
  Beispiel ist der Stand nach `PUT` auf `…/spieler/1/einheiten/2/…`, dann
  `…/spieler/2/einheiten/1/…`. Keine *Einheit* in der *Armeeliste* des *Spielers*: 404. Die Seite
  schickt `DELETE`, wenn sie die Karte *ausgewählt* gezeichnet hat, sonst `PUT`. Warum kein
  Umschalten: Zwei Seiten (QUE-3.2) oder ein doppelter Klick schalteten sonst zurück.
- **V3** Die *Auswahl* hält die Domäne in `Auswahl` ([Grundschnitt](../../domaene.md)), die
  Tür ist `Aufstellung`: `auswählen(einheit)` (AUF-5.11, 20.2), `abwählen(einheit)`,
  `modellAnklicken(modell)` ([V14](../bewegung/auswahl.md), AUF-25.1, 25.2), Abfragen
  `ausgewählt(einheit)`, `modellAusgewählt(modell)`, `ganzeEinheitIstEbene(einheit)`
  (AUF-21.1) und `modellIstEbene(modell)` (AUF-25.1). Nur in `Auswahl`, ohne Tür:
  `ganzeEinheitAlsEbene(einheit)` (AUF-23.3; ist sie nicht *ausgewählt*, nichts), die nur
  `zurücklegen` ruft ([Handlungen](handlungen.md)). `Auswahl` kennt nur *Einheit* und
  *Ebene*; ob eine *Einheit* zur Partie gehört und nicht *aufgestellt* ist, prüft
  `Aufstellung` in `auswählen` (Anliegen 1651, AUF-5.10), nicht `web/`. Auswählen ist keine
  Handlung (Glossar, *ausgewählt*): ohne Sperre, darum ohne D2.
- Klick auf ein *Modell*: [V14](../bewegung/auswahl.md) (AUF-20.6, 25.1, 25.2). Beispiel
  [ebene.json](../ebene.json): Stand von V1 nach
  `PUT /api/spieler/2/einheiten/1/modelle/3/anklicken`.
