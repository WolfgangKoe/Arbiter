# Vertrag: Aufstellen · Handlungen

Abschnitt der *Aufstellung*, die anderen: [Architektur](../../../architektur.md#schichten);
was alle Phasen teilen: [Querschnitt](../querschnitt.md).

Am Bildschirm | Anfrage (V5) | `Aufstellung`
---|---|---
*Karte* anklicken (AUF-18.1 bis 18.5, 19.4) | `PUT /api/karteAnklicken`, `{"x": 39.5, "y": 30}` | `karteAnklicken`
*Modell* auf der *Karte* loslassen (AUF-8.2, 20.4, 21.1, 21.2, 24.2, 26.1) | `PUT …/modelle/<m>/stelle`, Körper wie oben | `modellLoslassen`
„Aufstellen der Einheit beenden“ (AUF-10.1) | `PUT /api/aufstellenDerEinheitBeenden` | `aufstellenDerEinheitBeenden`
„Einheit zurücklegen“ (AUF-23.1, 23.3, 23.5) | `PUT /api/zurücklegen` | `zurücklegen`

In der Domäne: Welcher *Einheit* der Klick gilt, entscheidet `karteAnklicken` (AUF-18.1),
nicht die Seite, denn eine zweite Seite kann eine alte *Auswahl* zeigen (QUE-3.2). Ob
`modellLoslassen` ein *Modell* oder den Block *setzt*, entscheiden *Auswahl* und *Ebene*
([V3](auswahl.md); AUF-20.4, 21.1). `zurücklegen` nimmt jedes *gesetzte* *Modell* der
*Einheit in Aufstellung* von der *Karte* und ruft `ganzeEinheitAlsEbene` (V3); ohne sie
ändert es nichts, ohne `Sperre` (AUF-23.5), wie `karteAnklicken` ohne *Auswahl*.
Wächter und jeder *Grund* gegen die *Stelle* (D4), der nach dem Anhalten
([V10](ziehen.md)) bleibt (QUE-1.3 nur bei Zonen unter 1″ Abstand), werfen `Sperre`
(AUF-12.5, 19.4). `modellSetzen`: [B1](../../tests.md#bildschirmtests).

Beispiele (V6): [zurueckgelegt.json](../zurueckgelegt.json): Stand von V1 oder von V9 nach
`PUT /api/zurücklegen` (AUF-23.1, 23.3). [sperre.json](../sperre.json): Stand des Beispiels von
V1, danach `DELETE /api/spieler/2/einheiten/1/ausgewählt` (AUF-5.4),
`PUT /api/spieler/2/einheiten/1/modelle/3/stelle` mit `{"x": 42, "y": 28}` (nur dieses
*Modell*, AUF-20.4; über 2″ von den anderen, QUE-4.2) und `PUT /api/aufstellenDerEinheitBeenden`
(AUF-10.3). Warum abgewählt: Ohne *Auswahl* zieht der Zug das *Modell* allein, mit und ohne
*Ebene*, so gilt das Beispiel vor und nach AUF-21.1.

Prüft wie im Querschnitt: 409 bei AUF-10.3 gleich `sperre.json`, 200 bei AUF-23.1 und 23.3
gleich `zurueckgelegt.json`.
