# Vertrag: Handlungen über HTTP

Ziehen, Loslassen, „zurück“ und Beenden zwischen `web/` und `frontend/`; Spielstand, Auswahl
und Schutz: [Vertrag](vertrag.md), Aufbau: [Web](web.md).

- **V5** Je Handlung eine Anfrage (W3), Kennungen nach W4 wie V1; `…/modelle/<m>` steht für
  `/api/spieler/<s>/einheiten/<e>/modelle/<m>`.

  Am Bildschirm | Anfrage | `Aufstellung`
  ---|---|---
  *Modell* auf der *Karte* loslassen (AUF-8.2) | `PUT …/modelle/<m>/stelle`, `{"x": 38.8, "y": 28}` | `modellLoslassen`
  *Modell* auf der *Ablage* von Spieler a (AUF-8.3, 8.4, 16.3) | `DELETE …/modelle/<m>/stelle?ablage=<a>` | `modellZurücklegen`
  *Einheit* auf der *Karte* loslassen (AUF-8.5, 14.1, 16.1) | `PUT /api/spieler/<s>/einheiten/<e>/stelle`, Körper wie oben | `einheitLoslassen`
  *Einheit* auf der *Ablage* des anderen *Spielers* a (AUF-16.5) | `DELETE /api/spieler/<s>/einheiten/<e>/stelle?ablage=<a>` | `einheitAufAblageLoslassen`
  „zurück“ (AUF-9.3, 9.4, 15.1) | `PUT /api/zurück` | `zurück`
  „Aufstellen der Einheit beenden“ (AUF-10.1) | `PUT /api/aufstellenDerEinheitBeenden` | `aufstellenDerEinheitBeenden`

  Ein *Modell* nennt jedes der *Armee*, auch einer *aufgestellten* *Einheit* (AUF-8.4); eine
  *Einheit* nur eine der *Ablage* (V2). Unbekannte Kennung 404, Körper ohne Zahl `x` und `y`
  oder ohne `ablage` 400. `web/` liest Zahlen als `Fraction(str(zahl))`, die Dezimalzahl wie
  gesendet (S2). Warum `PUT`: V4; doppelt gesendet ändert nichts oder sperrt (D2).
  In der Domäne: Gründe gegen die *Stelle* (D4) machen beim Loslassen das *Modell* *gesperrt*
  (AUF-9.1), Wächter werfen `Sperre` (AUF-12.2); kein `try` um `modellSetzen`.
  `zurück()` ohne *gesperrtes* *Modell* ändert nichts (AUF-17.1), `einheitAufAblageLoslassen`
  mit der eigenen *Ablage* auch (AUF-16.4).
- **V6** Antwort 200: Spielstand wie V1. *Sperre*: 409 mit `gründe` (`Sperre.gründe`, Text
  aus `Grund`, in dessen Reihenfolge) und dem unveränderten `spielstand`. Beispiel
  [sperre.json](vertrag/sperre.json): Stand des Beispiels von V1, danach
  `PUT /api/spieler/2/einheiten/1/modelle/4/stelle` mit `{"x": 38.8, "y": 28}` (*gesperrt*,
  ‚Base überdeckt‘) und `PUT /api/aufstellenDerEinheitBeenden` (AUF-12.1).
- **V7** Die Seite zeigt (O1, Bestandteile aus Anliegen 372):
  - `modell gesperrt` am Kreis, wenn `gesperrt` (AUF-9.1).
  - `sperrmeldung`, je *Grund* ein `sperrmeldungGrund`: die `gründe` der letzten 409, bis eine
    Anfrage außer V2 beantwortet ist (AUF-12.3, 12.4: bis zur nächsten Handlung, Auswählen ist
    keine); sonst `gründeDerGesperrten` (AUF-9.1, QUE-3.5); ohne *Grund* keine.
    Warum in der Seite: Die *Sperre* ändert den Stand nicht (D2).
  - `knopfGruppe`: „zurück“, solange ein *Modell* `gesperrt` ist; „Aufstellen der Einheit
    beenden“ immer, denn AUF-12.4 nennt auch den *Grund* nach AUF-7.4 (Anliegen 388).
- **V8** Ziehen mit Pointer Events an `.karte .modell` und `.einheitenKarte`, ein Weg für
  Maus und Finger (QUE-3.4, `touch-action: none` aus 372). Ziel des Loslassens: der Punkt in
  Zoll über `getScreenCTM().inverse()` der `.karte`; im *Spielfeld* die *Karte*, sonst die
  `armeeKarte` darunter, sonst keins: keine Anfrage, die Seite zeichnet den letzten Stand
  (AUF-16.2). Eine *Einheit* auf der *Ablage* ihres *Spielers*: keine Anfrage (AUF-16.4), auf
  der des anderen: V5 (AUF-16.5). Warum: Eine Antwort 200 beendete die `sperrmeldung` (V7),
  doch Loslassen ohne Ziel ist keine Handlung (AUF-12.3).
  Ein Zug beginnt erst, wenn der Zeiger in x oder y mehr als 4 px (`zugschwelle`) von seinem
  Startpunkt abweicht; erst dann folgt das Element dem Zeiger. Vorbild: `dragStartThresholdPx`
  in ArbiterMap (`interaction_profile.js`). Ohne Zug ist es ein Klick: auf einer *Einheit* der
  *Ablage* V2, sonst nichts. Mit Zug ist es Loslassen wie oben, auch über dem Element, an dem
  er begann (AUF-8.2), und wählt nie aus.

Prüft: Der Testautor je Kriterium mit dem Flask-Testclient gegen V5 und V6 (409 gleich
`sperre.json`) und mit Bildschirmtests nach [B1 bis B5](web.md#bildschirmtests), denen
`page.route` `sperre.json` liefert (`spielstand` auf `GET`, 409 auf die Handlung); 400 und
404: Unit-Tests des Implementierers in `tests/einheit/web/anwendungTest.py`.
