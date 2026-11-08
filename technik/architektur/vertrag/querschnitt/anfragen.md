# Vertrag: Querschnitt · Anfragen

Pfade und JSON zwischen `web/` und `frontend/`
([Ablauf, Technikphase](../../../../prozess/ablauf/technikphase.md), Schritt 1); Aufbau beider:
[Web](../../web.md), [Frontend](../../frontend.md). Hier und in [Ziehen](ziehen.md) steht, was
alle Phasen teilen; Handlungen, Knöpfe und Beispiele je Phase in ihrem Ordner
([Übersicht](../../../architektur.md#schichten)). Eine neue Route ist ein Anliegen an den
Architekten. Routen gibt es nur nach V1, V2, V5, V10, V12 bis V14, V18, V19 und V21.

- **V1** `GET /api/spielstand` → 200 mit dem Spielstand. Beispiel:
  [spielstand.json](../spielstand.json): Spieler 2 ist *an der Reihe*, seine erste
  *Einheit* ist *Einheit in Aufstellung* mit drei *gesetzten* *Modellen* und *ausgewählt*.
  Kennungen nach [W4](../../web.md#aufbau), je ab 1: `spieler[].nummer` in der Reihenfolge der
  Ausgangslage, `armeeliste[].nummer` in der der *Armee*, auch wenn eine frühere *Einheit*
  nicht mehr in der *Armeeliste* steht; die Klasse `armeeKarte` bleibt (O3).
  `modelle[]` nennt die *gesetzten* *Modelle* mit Kennung `einheit` (Reihenfolge der *Armee*)
  und `nummer` (Reihenfolge der *Einheit*). Schlüssel einer Phase: in ihrer Datei.
- **V4** Schutz vor fremden Seiten im selben Browser, statt eines CSRF-Tokens: Eine Route,
  die etwas ändert, nimmt nur `PUT` oder `DELETE` an, nie `GET` oder `POST`; `web/` gibt kein
  CORS frei (kein `Access-Control-Allow-*`, kein `flask-cors`). Dann schickt der Browser eine
  fremde Anfrage erst nach einem Preflight, den `web/` nicht beantwortet; ein Formular kann nur
  `GET` und `POST`. Gegen DNS-Rebinding nimmt `web/` nur die Hosts `127.0.0.1` und `localhost`
  an (`TRUSTED_HOSTS`, sonst 400).
  Prüft: die Ausnahme von `python:S4502` (`formregeln/sonarlint.py`) gilt, solange keine Route
  `POST` annimmt und nichts CORS freigibt; `TRUSTED_HOSTS`: Unit-Test des Implementierers.
- **V5** Je Handlung eine Anfrage (W3), Kennungen nach W4 wie V1; `…/modelle/<m>` steht für
  `/api/spieler/<s>/einheiten/<e>/modelle/<m>`. Die Datei der Phase nennt ihre Handlungen als
  Tabelle Am Bildschirm | Anfrage | Methode der Domäne.
  Ein *Modell* nennt jedes der *Armee*, auch einer *aufgestellten* *Einheit* (AUF-7.2, 22.2).
  Unbekannte Kennung 404, Körper ohne Zahl `x` und `y` 400; Eingaben beim Loslassen: V10. `web/` liest
  Zahlen nach [S2](../../domaene.md#stelle-und-rechnen). Eine Zahl ist eine
  JSON-Zahl, kein Wahrheitswert, und als double endlich, denn die Seite rechnet in double;
  eine Ganzzahl, die Python nicht liest (über 4.300 Ziffern), ist keine. In der Abfrage (V10)
  gilt nur die Schreibweise einer JSON-Zahl, nicht was `float` sonst nimmt (`1_0`, ` 3 `).
  Warum `PUT`: V4; doppelt gesendet ändert nichts oder sperrt (D2).
- **V6** Antwort 200: Spielstand wie V1. *Sperre*: 409 mit `gründe` (`Sperre.gründe`, Text
  aus `Grund`, in dessen Reihenfolge) und dem unveränderten `spielstand`. Beispiele: in der
  Datei der Phase.
- **V7** Die Seite zeigt (O1):
  - `sperrmeldung`, je *Grund* ein `sperrmeldungGrund`: die `gründe` der letzten 409 einer
    Handlung (Tabelle der Phase, V5), bis die nächste Handlung beantwortet ist (AUF-12.8, BEW-21.1);
    Auswählen (V2, V14) und Abfragen (V1, V10) sind keine (AUF-12.6, 12.7). Ohne *Grund*
    keine. Warum in der Seite: Die *Sperre* ändert den Stand nicht (D2).
  - `knopfGruppe`: die Knöpfe, die die Datei der Phase nennt.

Prüft, auch für [Ziehen](ziehen.md): Der Testautor vor dem Code in den Akzeptanztests der
Anforderung (T1), je Kriterium: das Backend mit `anwendungFür(aufstellung).test_client()`
(ohne `flask`), das Frontend mit einem Bildschirmtest, dem `page.route` das Beispiel statt
des Servers liefert; derselbe Ablauf gegen den echten Server ist der Akzeptanztest
([B1 bis B5](../../tests.md#bildschirmtests)). Tests lesen die Beispiele nach
[T3](../../tests.md#aufbau). 400 und 404: Unit-Tests des Implementierers in
`tests/einheit/web/anwendungTest.py`.
