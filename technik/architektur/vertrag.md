# Vertrag zwischen Web und Frontend

Pfade und JSON zwischen `web/` und `frontend/`
([Ablauf, Technikphase](../../prozess/ablauf.md#technikphase), Schritt 1); Aufbau beider:
[Web](web.md). Eine neue Route ist ein Anliegen an den Architekten.

- **V1** `GET /api/spielstand` → 200 mit dem Spielstand. Beispiel:
  [spielstand.json](vertrag/spielstand.json): Spieler 2 ist *an der Reihe*, seine erste
  *Einheit* ist *Einheit in Aufstellung* mit drei *gesetzten* *Modellen*; je *Spieler* ist eine
  *Einheit* *ausgewählt*. Kennungen nach [W4](web.md#aufbau), je ab 1:
  `spieler[].nummer` in der Reihenfolge der Ausgangslage, `ablage[].nummer` in der
  Reihenfolge der *Armee*, auch wenn eine frühere *Einheit* nicht mehr in der *Ablage* liegt.
  `ausgewählt` an der *Einheit* nach AUF-5.6, am *Modell* nach AUF-5.7.
- **V2** `PUT /api/spieler/<nummer>/einheiten/<nummer>/ausgewählt` macht die *Einheit*
  *ausgewählt* (AUF-5.3), `DELETE` auf denselben Pfad nicht (AUF-5.4). Beide antworten 200
  mit dem Spielstand wie V1; das Beispiel ist der Stand nach `PUT` auf
  `/api/spieler/1/einheiten/2/ausgewählt` und `/api/spieler/2/einheiten/1/ausgewählt`. Nennt
  der Pfad keine *Einheit* in der *Ablage* des *Spielers*: 404. Die Seite schickt `PUT`, wenn
  sie die Karte nicht *ausgewählt* gezeichnet hat, sonst `DELETE`, und zeichnet die Antwort
  ([O1](web.md#oberfläche)).
  Warum kein Umschalten: Beide Anfragen sind idempotent. Zwei Seiten auf einem Stand
  (QUE-3.1, QUE-3.2) oder ein doppelt gesendeter Klick schalteten sonst zurück.
- **V3** Die Auswahl hält die Domäne in `Aufstellung`: `auswählen(einheit)`,
  `abwählen(einheit)`, Abfrage `ausgewählt(einheit)`; AUF-5.10 gilt dort, nicht in `web/`.
  Auswählen ist keine Handlung (Glossar, *ausgewählt*): ohne Sperre, darum ohne D2.
- **V4** Schutz vor fremden Seiten im selben Browser, statt eines CSRF-Tokens: Eine Route,
  die etwas ändert, nimmt nur `PUT` oder `DELETE` an, nie `GET` oder `POST`; `web/` gibt kein
  CORS frei (kein `Access-Control-Allow-*`, kein `flask-cors`). Dann schickt der Browser eine
  fremde Anfrage erst nach einem Preflight, den `web/` nicht beantwortet; ein Formular kann nur
  `GET` und `POST`. Gegen DNS-Rebinding nimmt `web/` nur die Hosts `127.0.0.1` und `localhost`
  an (`TRUSTED_HOSTS`, sonst 400). Wegwerf-Versuch (Anliegen 329): Von einem fremden Ursprung
  kommen `PUT` und `DELETE` nicht an, `POST` schon; ein fremder Host bekommt 400.
  Prüft: die Ausnahme von `python:S4502` (`formregeln/sonarlint.py`) gilt, solange keine Route
  `POST` annimmt und nichts CORS freigibt; `TRUSTED_HOSTS`: Unit-Test des Implementierers.

Prüft V1 bis V3: Der Testautor schreibt vor dem Code in die Akzeptanztests der Anforderung
(T1), je Kriterium benannt: das Backend mit dem Flask-Testclient
(`anwendungFür(aufstellung).test_client()`, ohne Import von `flask`) gegen V1 und V2, das
Frontend mit einem Bildschirmtest, dem Playwright `spielstand.json` per `page.route` statt des
Servers liefert; derselbe Ablauf gegen den echten Server ist der Akzeptanztest
([B1](web.md#bildschirmtests)). Tests lesen die Datei, statt sie zu kopieren. Die Antwort 404
gehört zu keinem Kriterium: Unit-Test des Implementierers in
`tests/einheit/web/anwendungTest.py`. V3: die Akzeptanztests zu AUF-5.
