# Vertrag: quer über die Phasen

Pfade und JSON zwischen `web/` und `frontend/`
([Ablauf, Technikphase](../../../prozess/ablauf/technikphase.md), Schritt 1); Aufbau beider:
[Web](../web.md), [Frontend](../frontend.md). Hier steht, was alle Phasen teilen; Handlungen,
Knöpfe und Beispiele je Phase in ihrer Datei: [Aufstellen](aufstellen.md),
[Schlacht](schlacht.md), [Bewegung](bewegung.md). Eine neue Route ist ein Anliegen an den
Architekten. Routen gibt es nur nach V1, V2, V5, V9, V10 und V12 bis V14.

- **V1** `GET /api/spielstand` → 200 mit dem Spielstand. Beispiel:
  [spielstand.json](spielstand.json): Spieler 2 ist *an der Reihe*, seine erste
  *Einheit* ist *Einheit in Aufstellung* mit drei *gesetzten* *Modellen* und *ausgewählt*.
  Kennungen nach [W4](../web.md#aufbau), je ab 1: `spieler[].nummer` in der Reihenfolge der
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
  Unbekannte Kennung 404, Körper ohne Zahl `x` und `y` 400. `web/` liest
  Zahlen als `Fraction(str(zahl))`, die Dezimalzahl wie gesendet (S2). Eine Zahl ist eine
  JSON-Zahl, kein Wahrheitswert, und als double endlich, denn die Seite rechnet in double;
  eine Ganzzahl, die Python nicht liest (über 4.300 Ziffern), ist keine. In der Abfrage (V10)
  gilt nur die Schreibweise einer JSON-Zahl, nicht was `float` sonst nimmt (`1_0`, ` 3 `).
  Warum `PUT`: V4; doppelt gesendet ändert nichts oder sperrt (D2).
- **V6** Antwort 200: Spielstand wie V1. *Sperre*: 409 mit `gründe` (`Sperre.gründe`, Text
  aus `Grund`, in dessen Reihenfolge) und dem unveränderten `spielstand`. Beispiele: in der
  Datei der Phase.
- **V7** Die Seite zeigt (O1):
  - `sperrmeldung`, je *Grund* ein `sperrmeldungGrund`: die `gründe` der letzten 409 einer
    Handlung (Tabelle der Phase, V5), bis die nächste Handlung beantwortet ist (BEW-2.6);
    Auswählen (V2, V9, V14) und Abfragen (V1, V10) sind keine (AUF-12.6, 12.7). Ohne *Grund*
    keine. Warum in der Seite: Die *Sperre* ändert den Stand nicht (D2).
  - `knopfGruppe`: die Knöpfe, die die Datei der Phase nennt.
- **V8** Pointer Events am Dokument, ein Weg für Maus und Finger (QUE-3.4,
  `touch-action: none` an `.karte`). Ein Zug beginnt erst, wenn der Zeiger in x oder y mehr
  als 4 px (`zugschwelle`, wie `dragStartThresholdPx` in ArbiterMap) vom Startpunkt abweicht.
  Ohne Zug ist es ein Klick; was er bedeutet, nennt die Datei der Phase. Den Punkt in Zoll
  rechnet die Seite mit `getScreenCTM().inverse()` der `.karte`.
  Gezogen wird nur ein `.karte .modell`: Es folgt dem Zeiger. Ein Zug wählt nie aus.
  Beim Druck auf ein gezogenes Element verhindert die Seite Markieren und das eigene Ziehen
  des Browsers (`preventDefault` auf `pointerdown` und `dragstart`, `user-select: none` an
  `.armeeKarte`); sonst bricht `pointercancel` den Zug ab.
- **V10** Zeigen beim Ziehen: `GET …/modelle/<m>/stelleBeimLoslassen?x=<x>&y=<y>` → 200 mit
  `modelle[]`, je *Modell*, das das Loslassen am Punkt *setzen* würde (Datei der Phase),
  `spieler`, `einheit`, `nummer` wie V1 und `x`, `y`. *Sperre*: 409 wie V6. Zahlen wie V5,
  fehlt eine: 400. Warum `GET`: Die Abfrage ändert nichts (V4).
  Statt V8 „folgt dem Zeiger“ fragt die Seite je Zeigerbewegung im *Spielfeld* nach,
  höchstens eine Anfrage zugleich, danach nur mit dem jüngsten Punkt. Auf 200 setzt sie
  `cx`, `cy` jedes genannten Kreises, sonst bleibt jeder, wo er ist, auch bei 409 (ohne
  `sperrmeldung`: keine Handlung). Eine Antwort nach dem Loslassen verwirft sie. Beim
  Loslassen schickt sie V5 mit dem Punkt des Zeigers, nicht dem gezeigten; neben dem
  *Spielfeld* mit dem Punkt der letzten 200 dieses Zugs, ohne sie keine Anfrage: Sie
  zeichnet den letzten Stand. Warum der Punkt: Zu ihm *setzt* die Handlung die gezeigten
  *Stellen*; welche *Modelle* mitgehen, entscheidet die Domäne. Prüft am Bildschirm:
  halten, auf die Antwort warten, `cx`, `cy` lesen, am selben Punkt oder neben dem
  *Spielfeld* loslassen; die *Stelle* danach gleicht den gelesenen Werten exakt (B3).

Prüft: Der Testautor vor dem Code in den Akzeptanztests der Anforderung (T1), je Kriterium:
das Backend mit `anwendungFür(aufstellung).test_client()` (ohne `flask`), das Frontend mit
einem Bildschirmtest, dem `page.route` das Beispiel statt des Servers liefert; derselbe
Ablauf gegen den echten Server ist der Akzeptanztest
([B1 bis B5](../tests.md#bildschirmtests)). Tests lesen die Beispiele, statt sie zu kopieren.
400 und 404: Unit-Tests des Implementierers in `tests/einheit/web/anwendungTest.py`.
