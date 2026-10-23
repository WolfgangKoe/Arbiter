# Vertrag: Handlungen über HTTP

Klicken, Loslassen, Beenden und Zurücklegen zwischen `web/` und `frontend/`; Spielstand, Auswahl
und Schutz: [Vertrag](vertrag.md), Aufbau: [Web](web.md).

- **V5** Je Handlung eine Anfrage (W3), Kennungen nach W4 wie V1; `…/modelle/<m>` steht für
  `/api/spieler/<s>/einheiten/<e>/modelle/<m>`.

  Am Bildschirm | Anfrage | `Aufstellung`
  ---|---|---
  *Karte* anklicken (AUF-18.1 bis 18.5, 19.4) | `PUT /api/karteAnklicken`, `{"x": 39.5, "y": 30}` | `karteAnklicken`
  *Modell* auf der *Karte* loslassen (AUF-8.2, 20.4, 21.1, 21.2, 24.2, 26.1) | `PUT …/modelle/<m>/stelle`, Körper wie oben | `modellLoslassen`
  „Aufstellen der Einheit beenden“ (AUF-10.1) | `PUT /api/aufstellenDerEinheitBeenden` | `aufstellenDerEinheitBeenden`
  „Einheit zurücklegen“ (AUF-23.1, 23.3, 23.5) | `PUT /api/zurücklegen` | `zurücklegen`
  Ein *Modell* nennt jedes der *Armee*, auch einer *aufgestellten* *Einheit* (AUF-7.2, 22.2).
  Unbekannte Kennung 404, Körper ohne Zahl `x` und `y` 400. `web/` liest
  Zahlen als `Fraction(str(zahl))`, die Dezimalzahl wie gesendet (S2). Eine Zahl ist eine
  JSON-Zahl, kein Wahrheitswert, und als double endlich, denn die Seite rechnet in double;
  eine Ganzzahl, die Python nicht liest (über 4.300 Ziffern), ist keine. In der Abfrage (V10)
  gilt nur die Schreibweise einer JSON-Zahl, nicht was `float` sonst nimmt (`1_0`, ` 3 `).
  Warum `PUT`: V4; doppelt gesendet ändert nichts oder sperrt (D2).
  In der Domäne: Welcher *Einheit* der Klick gilt, entscheidet `karteAnklicken` (AUF-18.1),
  nicht die Seite, denn eine zweite Seite kann eine alte *Auswahl* zeigen (QUE-3.2). Ob
  `modellLoslassen` ein *Modell* oder den Block *setzt*, entscheiden *Auswahl* und *Ebene*
  (V3; AUF-20.4, 21.1). `zurücklegen` nimmt jedes *gesetzte* *Modell* der *Einheit in
  Aufstellung* von der *Karte* und ruft `ganzeEinheitAlsEbene` (V3); ohne sie ändert es
  nichts, ohne `Sperre` (AUF-23.5), wie `karteAnklicken` ohne *Auswahl*.
  Wächter und jeder *Grund* gegen die *Stelle* (D4), der nach dem Anhalten (V10) bleibt
  (QUE-1.3 nur bei Zonen unter 1″ Abstand), werfen `Sperre` (AUF-12.5, 19.4).
  Ohne Route: `modellSetzen(modell, stelle)` *setzt* nach QUE-1.1 bis 1.3 und AUF-7.2, 7.3
  genau an die *Stelle*, ohne Hineinrücken und Anhalten. Warum: Tests bauen damit die
  Vorgeschichte an genauen *Stellen*; eine falsche scheitert, statt verschoben zu stehen.
- **V6** Antwort 200: Spielstand wie V1, Beispiel [zurueckgelegt.json](vertrag/zurueckgelegt.json):
  Stand von V1 oder von V9 nach `PUT /api/zurücklegen` (AUF-23.1, 23.3). *Sperre*: 409 mit `gründe` (`Sperre.gründe`, Text
  aus `Grund`, in dessen Reihenfolge) und dem unveränderten `spielstand`. Beispiel
  [sperre.json](vertrag/sperre.json): Stand des Beispiels von V1, danach
  `DELETE /api/spieler/2/einheiten/1/ausgewählt` (AUF-5.4),
  `PUT /api/spieler/2/einheiten/1/modelle/3/stelle` mit `{"x": 42, "y": 28}` (nur dieses
  *Modell*, AUF-20.4; über 2″ von den anderen, QUE-4.2) und `PUT /api/aufstellenDerEinheitBeenden`
  (AUF-10.3). Warum abgewählt: Ohne *Auswahl* zieht der Zug das *Modell* allein, mit und ohne
  *Ebene*, so gilt das Beispiel vor und nach AUF-21.1.
- **V7** Die Seite zeigt (O1):
  - `sperrmeldung`, je *Grund* ein `sperrmeldungGrund`: die `gründe` der letzten 409, bis eine
    Anfrage außer V2 und V9 beantwortet ist (AUF-12.6, 12.7: Auswählen ist keine Handlung);
    ohne *Grund* keine. Warum in der Seite: Die *Sperre* ändert den Stand nicht (D2).
  - `knopfGruppe`: „Aufstellen der Einheit beenden“ immer, denn AUF-12.7 nennt den *Grund*
    nach AUF-7.4; davor „Einheit zurücklegen“, wenn `einheitInAufstellung` nicht `null` ist
    (AUF-23.4).
- **V8** Pointer Events am Dokument, ein Weg für Maus und Finger (QUE-3.4,
  `touch-action: none` an `.karte`). Ein Zug beginnt erst, wenn der Zeiger in x oder y mehr
  als 4 px (`zugschwelle`, wie `dragStartThresholdPx` in ArbiterMap) vom Startpunkt abweicht.
  Ohne Zug ist es ein Klick: auf einer `.einheitenKarte` V2; auf einem *Modell* der
  *Einheit*, die in der *Armeeliste* `ausgewählt` trägt, V9 (AUF-25.1, 25.2), auf einem anderen
  *Modell* nichts (AUF-18.1); sonst im *Spielfeld* `karteAnklicken` mit dem Punkt in Zoll
  (`getScreenCTM().inverse()` der `.karte`), sonst nichts. Warum die *Armeeliste*: Ist die
  *Ebene* ein *Modell*, tragen die anderen *Modelle* kein `ausgewählt` (AUF-25.4).
  Gezogen wird nur ein `.karte .modell`: Es folgt dem Zeiger; trägt es `ausgewählt`, folgen
  alle mit `ausgewählt` um denselben Weg (AUF-21.1). Beim Loslassen im *Spielfeld*
  `modellLoslassen`, auch über dem Startpunkt (AUF-8.2), sonst keine Anfrage, auch auf einer
  `armeeKarte`: Die Seite zeichnet den letzten Stand (AUF-16.8; neben dem *Spielfeld* nach
  AUF-28.1: Anliegen 2251). Ein Zug wählt nie aus.
  Beim Druck auf ein gezogenes Element verhindert die Seite Markieren und das eigene Ziehen
  des Browsers (`preventDefault` auf `pointerdown` und `dragstart`, `user-select: none` an
  `.armeeKarte`); sonst bricht `pointercancel` den Zug ab.

- **V10** Zeigen beim Ziehen und Anhalten an *Bases* (AUF-24.3, 26.5; AUF-28.2, 29.1 und 29.3
  nur für das erste Weiterrücken, Rest: Anliegen 2180), mit Item anhaltenAnBases:
  - Domäne: Die Abfrage `stellenBeimLoslassen(modell, stelle)` → *Modell* → *Stelle* nennt
    jedes *Modell*, das `modellLoslassen(modell, stelle)` *setzen* würde (das gezogene oder
    jedes *gesetzte* der *Einheit*, V3), an seiner *Stelle* nach AUF-8.2, 21.1, 21.2, 26.1
    und 29.1, ohne zu *setzen*; Wächter wie dort werfen `Sperre`. `modellLoslassen` *setzt*
    genau diese *Stellen*, so steht nach dem Loslassen alles, wo die *Karte* es zeigte
    (AUF-28.2). Der Weg beginnt an der *gesetzten* *Stelle*, nicht an der zuletzt gezeigten.
    Angehalten wird nur, wenn die *Stelle* am Ende des Wegs eine *Base* *überdecken* würde,
    dann an der ersten, an die eine *Base* auf der geraden Strecke stößt (Zweck AUF-29), auf
    1/100″ genau ([S3](../architektur.md#stelle-und-rechnen)). Vorbedingung bis AUF-27: Am
    Anfang des Wegs *überdeckt* keine *Base* eine, gegen die angehalten wird.
  - HTTP: `GET …/modelle/<m>/stelleBeimLoslassen?x=<x>&y=<y>` → 200 mit `modelle[]`, je
    *Modell* der Abfrage `spieler`, `einheit`, `nummer` wie V1 und `x`, `y`. Beispiel
    [stelleBeimLoslassen.json](vertrag/stelleBeimLoslassen.json): Stand von V1, `x=35&y=28`
    für *Modell* 1, AUF-21.2 rückt den Block hinein. *Sperre*: 409 wie V6. Zahlen wie V5,
    fehlt eine: 400. Warum `GET`: Die Abfrage ändert nichts (V4).
  - Seite: Statt V8 „folgt dem Zeiger“ fragt sie je Zeigerbewegung im *Spielfeld* nach,
    höchstens eine Anfrage zugleich, danach nur mit dem jüngsten Punkt. Auf 200 setzt sie
    `cx`, `cy` jedes genannten Kreises, sonst bleibt jeder, wo er ist, auch bei 409 (ohne
    `sperrmeldung`: keine Handlung). Eine Antwort nach dem Loslassen verwirft sie. Beim
    Loslassen schickt sie V5 mit dem Punkt des Zeigers, nicht dem gezeigten.

Prüft: Der Testautor je Kriterium mit dem Flask-Testclient gegen V5, V6, V9 und V10 (409 bei
AUF-10.3 gleich `sperre.json`, 200 bei AUF-23.1 und 23.3 gleich `zurueckgelegt.json`) und mit Bildschirmtests nach [B1 bis B5](web.md#bildschirmtests), denen
`page.route` die Beispiele liefert; 400 und 404: Unit-Tests des Implementierers in
`tests/einheit/web/anwendungTest.py`. Zu V10: AUF-29.1 mit einem Weiterrücken ab der *gesetzten*
*Stelle*, an der *Stelle* nach dem Loslassen (28.2): auf der Strecke zur *Stelle*, wie `web/` sie liest (S2, exakt kollinear), keine *Base* *überdeckt*, zur ersten
angestoßenen `abstandHöchstens` 1/100″; den Raster prüfen nur Unit-Tests. AUF-24.3, 26.5 am
Bildschirm: halten, auf die Antwort warten, `cx`, `cy` lesen, am selben Punkt loslassen;
die *Stelle* danach gleicht den gelesenen Werten exakt (B3).
