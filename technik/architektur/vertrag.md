# Vertrag zwischen Web und Frontend

Pfade und JSON zwischen `web/` und `frontend/`
([Ablauf, Technikphase](../../prozess/ablauf.md#technikphase), Schritt 1); Aufbau beider:
[Web](web.md). Eine neue Route ist ein Anliegen an den Architekten.

- **V1** `GET /api/spielstand` → 200 mit dem Spielstand. Beispiel:
  [spielstand.json](vertrag/spielstand.json): Spieler 2 ist *an der Reihe*, seine erste
  *Einheit* ist *Einheit in Aufstellung* mit drei *gesetzten* *Modellen* und *ausgewählt*.
  Kennungen nach [W4](web.md#aufbau), je ab 1: `spieler[].nummer` in der Reihenfolge der
  Ausgangslage, `ablage[].nummer` in der der *Armee*, auch wenn eine frühere *Einheit* nicht
  mehr in der *Ablage* liegt. `ausgewählt` an der *Einheit* nach AUF-5.12, am *Modell* nach
  AUF-5.7 und 25.4; `ebene: true` nur am *Modell*, das die *Ebene* ist (AUF-25.1), sonst fehlt
  der Schlüssel. Warum: So gelten die Beispiele ohne *Ebene* unverändert.
  `modelle[]` nennt *gesetzte* und *gesperrte* *Modelle* mit Kennung `einheit` (Reihenfolge
  der *Armee*) und `nummer` (Reihenfolge der *Einheit*), `gesperrt` nach AUF-9.1, ein
  *gesperrtes* an `stelleDesGesperrten`. `gründeDerGesperrten`: jeder *Grund* aller
  *gesperrten* einmal, Text aus `Grund`, in dessen Reihenfolge. `nichtGesetzt` zählt
  *gesperrte* mit (Glossar). Handlungen: [V5 bis V8](handlungen.md).
- **V2** `PUT /api/spieler/<nummer>/einheiten/<nummer>/ausgewählt` macht die *Einheit*
  *ausgewählt* (AUF-5.11), `DELETE` nicht (AUF-5.4); beide 200 mit dem Spielstand. Das
  Beispiel ist der Stand nach `PUT` auf `…/spieler/1/einheiten/2/…`, dann
  `…/spieler/2/einheiten/1/…`. Keine *Einheit* in der *Ablage* des *Spielers*: 404. Die Seite
  schickt `DELETE`, wenn sie die Karte *ausgewählt* gezeichnet hat, sonst `PUT`. Warum kein
  Umschalten: Zwei Seiten (QUE-3.2) oder ein doppelter Klick schalteten sonst zurück.
- **V3** Die *Auswahl* hält die Domäne in `Auswahl` ([Grundschnitt](../architektur.md)), die
  Tür ist `Aufstellung`: `auswählen(einheit)` (AUF-5.11, 20.2), `abwählen(einheit)`,
  `ebeneWählen(modell)` (AUF-25.1), `ebeneAbwählen(modell)` (25.2), Abfragen
  `ausgewählt(einheit)`, `modellAusgewählt(modell)`, `ebene(einheit)` → *Einheit*, *Modell*
  oder `None`. AUF-5.10 gilt dort, nicht in `web/`. Auswählen ist keine Handlung (Glossar,
  *ausgewählt*): ohne Sperre, darum ohne D2.
- **V4** Schutz vor fremden Seiten im selben Browser, statt eines CSRF-Tokens: Eine Route,
  die etwas ändert, nimmt nur `PUT` oder `DELETE` an, nie `GET` oder `POST`; `web/` gibt kein
  CORS frei (kein `Access-Control-Allow-*`, kein `flask-cors`). Dann schickt der Browser eine
  fremde Anfrage erst nach einem Preflight, den `web/` nicht beantwortet; ein Formular kann nur
  `GET` und `POST`. Gegen DNS-Rebinding nimmt `web/` nur die Hosts `127.0.0.1` und `localhost`
  an (`TRUSTED_HOSTS`, sonst 400).
  Prüft: die Ausnahme von `python:S4502` (`formregeln/sonarlint.py`) gilt, solange keine Route
  `POST` annimmt und nichts CORS freigibt; `TRUSTED_HOSTS`: Unit-Test des Implementierers.
- **V9** `PUT …/modelle/<m>/ebene` (`…` wie V5) macht das *Modell* zur *Ebene* seiner
  *Einheit* (AUF-25.1), `DELETE` macht wieder die *Einheit* dazu, wenn es die *Ebene* war
  (25.2); beide 200 mit dem Spielstand. Die Seite schickt `DELETE`, wenn das *Modell* `ebene`
  trägt, sonst `PUT`; idempotent wie V2. Beispiel [ebene.json](vertrag/ebene.json): Stand
  von V1 nach `PUT /api/spieler/2/einheiten/1/modelle/3/ebene`. Kein *gesetztes* *Modell*
  der *ausgewählten* *Einheit*: 404.

Prüft V1 bis V3 und V9: Der Testautor vor dem Code in den Akzeptanztests der Anforderung
(T1), je Kriterium: das Backend mit `anwendungFür(aufstellung).test_client()` (ohne `flask`),
das Frontend mit einem Bildschirmtest, dem `page.route` das Beispiel statt des Servers
liefert; derselbe Ablauf gegen den echten Server ist der Akzeptanztest
([B1](web.md#bildschirmtests)). Tests lesen die Beispiele, statt sie zu kopieren. 404:
Unit-Tests des Implementierers in `tests/einheit/web/anwendungTest.py`.
