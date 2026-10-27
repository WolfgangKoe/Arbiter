# Vertrag: Aufstellen

Die *Aufstellung*; was alle Phasen teilen: [Querschnitt](querschnitt.md).

## Auswahl
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
- **V3** Die *Auswahl* hält die Domäne in `Auswahl` ([Grundschnitt](../domaene.md)), die
  Tür ist `Aufstellung` mit `auswählen`, `abwählen`, `ebeneWählen`, `ebeneAbwählen` und
  ihren Abfragen; `ganzeEinheitAlsEbene` (AUF-23.3) ruft nur `zurücklegen`, ohne Tür.
  `Auswahl` kennt nur *Einheit* und *Ebene*; ob eine *Einheit* zur Partie gehört und nicht
  *aufgestellt* ist, prüft `Aufstellung` vor dem Auswählen (Anliegen 1651, AUF-5.10), nicht
  `web/`. Auswählen ist keine Handlung (Glossar, *ausgewählt*): ohne Sperre, ohne D2.
- **V9** `PUT …/modelle/<m>/ebene` (`…` wie V5) macht das *Modell* zur *Ebene* seiner
  *Einheit* (AUF-25.1), `DELETE` macht wieder die *Einheit* dazu, wenn es die *Ebene* war
  (25.2); beide 200 mit dem Spielstand. Die Seite schickt `DELETE`, wenn das *Modell* `ebene`
  trägt, sonst `PUT`; idempotent wie V2. Beispiel [ebene.json](ebene.json): Stand
  von V1 nach `PUT /api/spieler/2/einheiten/1/modelle/3/ebene`. Kein *gesetztes* *Modell*
  der *ausgewählten* *Einheit*: 404.

## Handlungen
Am Bildschirm | Anfrage (V5) | `Aufstellung`
---|---|---
*Karte* anklicken (AUF-18.1 bis 18.5, 19.4) | `PUT /api/karteAnklicken`, `{"x": 39.5, "y": 30}` | `karteAnklicken`
*Modell* auf der *Karte* loslassen (AUF-8.2, 20.4, 21.1, 21.2, 24.2, 26.1) | `PUT …/modelle/<m>/stelle`, Körper wie oben | `modellLoslassen`
„Aufstellen der Einheit beenden“ (AUF-10.1) | `PUT /api/aufstellenDerEinheitBeenden` | `aufstellenDerEinheitBeenden`
„Einheit zurücklegen“ (AUF-23.1, 23.3, 23.5) | `PUT /api/zurücklegen` | `zurücklegen`

In der Domäne: Welcher *Einheit* der Klick gilt, entscheidet `karteAnklicken` (AUF-18.1),
nicht die Seite, denn eine zweite Seite kann eine alte *Auswahl* zeigen (QUE-3.2); ob
`modellLoslassen` ein *Modell* oder den Block *setzt*, *Auswahl* und *Ebene* (V3; AUF-20.4,
21.1). Ohne *Einheit in Aufstellung* ändert `zurücklegen` nichts, ohne `Sperre` (AUF-23.5),
wie `karteAnklicken` ohne *Auswahl*.
Wächter und jeder *Grund* gegen die *Stelle* (D4), der nach dem Anhalten (V10) bleibt
(QUE-1.3 nur bei Zonen unter 1″ Abstand), werfen `Sperre` (AUF-12.5, 19.4).
`modellSetzen`: [B1](../tests.md#bildschirmtests).

Beispiele (V6): [zurueckgelegt.json](zurueckgelegt.json): Stand von V1 oder von V9 nach
`PUT /api/zurücklegen` (AUF-23.1, 23.3). [sperre.json](sperre.json): Stand des Beispiels von
V1, danach `DELETE /api/spieler/2/einheiten/1/ausgewählt` (AUF-5.4),
`PUT /api/spieler/2/einheiten/1/modelle/3/stelle` mit `{"x": 42, "y": 28}` (nur dieses
*Modell*, AUF-20.4; über 2″ von den anderen, QUE-4.2) und `PUT /api/aufstellenDerEinheitBeenden`
(AUF-10.3). Warum abgewählt: Ohne *Auswahl* zieht der Zug das *Modell* allein, mit und ohne
*Ebene*, so gilt das Beispiel vor und nach AUF-21.1.

## Seite
- Knöpfe (V7): „Aufstellen der Einheit beenden“ immer, denn AUF-12.7 nennt den *Grund*
  nach AUF-7.4; davor „Einheit zurücklegen“, wenn `einheitInAufstellung` nicht `null` ist
  (AUF-23.4).
- Klick (V8): auf einer `.einheitenKarte` V2; auf einem *Modell* der *Einheit*, die in der
  *Armeeliste* `ausgewählt` trägt, V9 (AUF-25.1, 25.2), auf einem anderen *Modell* V14
  (AUF-20.6); sonst im *Spielfeld* `karteAnklicken` mit dem Punkt, sonst nichts. Warum die *Armeeliste*: Ist die
  *Ebene* ein *Modell*, tragen die anderen *Modelle* kein `ausgewählt` (AUF-25.4).
- Zug (V8): Trägt das gezogene *Modell* `ausgewählt`, folgen alle mit `ausgewählt` um
  denselben Weg (AUF-21.1). Beim Loslassen im *Spielfeld* `modellLoslassen`, auch über dem
  Startpunkt (AUF-8.2), daneben nach V10, auch auf einer `armeeKarte`.

## Ziehen
Nach V10 (AUF-24.3, 26.5; 28.2, 29.1 und 29.3 nur für das erste Weiterrücken, Rest:
Anliegen 2180): `stellenBeimLoslassen(modell, stelle)` → *Modell* → *Stelle* nennt jedes
*Modell*, das `modellLoslassen` *setzen* würde (V3), an seiner *Stelle* nach AUF-8.2, 21.1,
21.2, 26.1 und 29.1, ohne zu *setzen*, Wächter wie dort; `modellLoslassen` *setzt* genau
diese (AUF-28.2). Der Weg beginnt an der *gesetzten* *Stelle*. Angehalten wird nur, wenn die
*Stelle* am Ende eine *Base* *überdecken* würde, an der ersten, an die eine *Base* auf der
geraden Strecke stößt (AUF-29, [S3](../domaene.md#stelle-und-rechnen)); bis AUF-27
*überdeckt* am Anfang des Wegs keine *Base* eine, gegen die angehalten wird. Beispiel
[stelleBeimLoslassen.json](stelleBeimLoslassen.json): Stand von V1, `x=35&y=28` für *Modell*
1, AUF-21.2 rückt den Block hinein. Neben dem *Spielfeld*: AUF-28.1, mit Item
loslassenNebenDerKarte; eine *aufgestellte* *Einheit* bekommt nur 409 (AUF-16.8).

Prüft wie im Querschnitt: 409 bei AUF-10.3 gleich `sperre.json`, 200 bei
AUF-23.1 und 23.3 gleich `zurueckgelegt.json`. Zu V10: AUF-29.1 mit einem Weiterrücken ab der
*gesetzten* *Stelle*, an der *Stelle* nach dem Loslassen (28.2): auf der Strecke zur *Stelle*,
wie `web/` sie liest (S2, exakt kollinear), keine *Base* *überdeckt*, zur ersten angestoßenen
`abstandHöchstens` 1/100″; den Raster prüfen nur Unit-Tests. AUF-24.3, 26.5 und 28.1 am
Bildschirm nach V10.
