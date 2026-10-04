# Web: Frontend und Backend

Gilt ab dem ersten Item mit Oberfläche. Übersicht und Schichten: [Architektur](../architektur.md).

## Aufbau
- **W1** Getrennt: `arbiter/web/` liefert die Dateien aus `technik/frontend/` unverändert aus
  und beantwortet Anfragen unter `/api/` mit JSON; es erzeugt kein HTML. Das Frontend kennt
  nur diese Adressen. Gegenbeispiel `ArbiterMap/backend/app/routes/map.py`: Das Backend füllt
  Jinja-Vorlagen, 40.000 Zeichen in einer Datei. Prüft: nur Text; Auslöser: erstes Modul in
  `web/`, dann ein Importvertrag „`web/` importiert kein `render_template`, kein `jinja2`“.
- **W2** `web/` ist dünn, je Modul ein Grund zur Änderung:
  - `server.py`: startet und beendet den Server, nennt die Adresse.
  - `anwendung.py`: Flask; Anfrage lesen, eine Handlung der Domäne aufrufen, Antwort schreiben.
  - `darstellung.py`: Spielstand der Domäne → JSON-fähige Werte; kennt Flask nicht.
  Regeln und Rechnen stehen nur in der Domäne: Längen in Zoll liefert `messen.py`, `web/`
  wandelt `Fraction` nur für die Antwort in `float`. `web/` liest Properties und Abfragen
  (D3), nie `_`-Felder. Prüft: nur Text; Auslöser: zweite Route.
- **W3** Eine Anfrage je Handlung. Eine Sperre wird HTTP 409 mit der Liste ihrer Gründe
  (`Sperre.gründe`, Text aus `Grund`). Prüft: nur Text; Auslöser: erste Handlung über HTTP.
- **W4** Spielobjekte haben in der Domäne keine Kennung (D1). `web/` vergibt sie aus der
  Reihenfolge der Ausgangslage: Spieler, Einheit, Modell. Prüft: wie W3.
- **W5** Der Befehl `python3 -m arbiter` (`starten()` in `arbiter/__main__.py`) lädt die
  Ausgangslage, startet den Server auf `127.0.0.1` mit einem freien Port und gibt die
  Adresse in der ersten Zeile aus (QUE-2.1). Nur `127.0.0.1`: zwei Spieler an einem Gerät
  (`domaene/ziel.md`). Werkzeug-Server von Flask, ohne Debug-Modus. Aus der Wurzel startet
  ihn `.venv/bin/arbiter` (Anliegen 243). Prüft: der Akzeptanztest zu QUE-2.1.
- Pfade und JSON der Schnittstelle wählt der Implementierer, solange es keinen Vertrag gibt
  (Anliegen 241); die Bildschirmtests prüfen die Seite, nicht das JSON.

## Oberfläche
Das Design-System gehört der Technik: die Komponentenseite (O3) als Doku, Vorlage der
Mockups und Ziel eines Bildschirmtests. Eine neue Komponente ist ein Anliegen an die Technik.
Tot ist eine Komponente ohne Template. Messbare Gestaltungsregeln werden Prüfungen.
- **O1** HTML, CSS mit Variablen, JavaScript-Module; kein Framework, kein Build-Schritt, kein
  Tailwind. Die Seite holt den Spielstand per `fetch` und zeichnet ihn in einem Schritt.
  Prüft: nur Text; eslint und stylelint: Anliegen 242.
- **O2** Die Karte ist ein SVG in Zoll: `viewBox` aus den Seitenlängen, `cx`, `cy`, `r` aus
  Stelle und Base; der Browser skaliert, gleich in x und y. Prüft: Akzeptanztests zu QUE-2.
- **O3** Die Komponentenseite ist `technik/frontend/komponenten.html` mit `komponenten.css`,
  gebaut aus `domaene/mockups/vorschlag.css`. Jede Seite verlinkt `komponenten.css`;
  Markup und CSS der Mockups übernimmt der Implementierer ohne Umschreiben. Klassen und
  Variablen deutsch, camelCase (`prozess/praemissen/wir.md`). Prüft: ihr Bildschirmtest.

## Bildschirmtests
Entschieden nach einem Wegwerf-Versuch (Flask im Thread, Playwright, Chromium aus dem Cache;
drei Tests in 2 s):
- **B1** Ein Bildschirmtest steht bei den Akzeptanztests seiner Anforderung (T1). Er baut den
  Zustand mit Handlungen der Domäne, startet `web/server.py` mit ihm im selben Prozess
  (eigener Thread, freier Port) und liest die Seite mit Playwright. Er importiert weder
  `flask` noch `werkzeug`; Browser je Sitzung, Seite je Test als Fixture in `conftest.py`.
  Prüft: nur Text; Auslöser: erster Bildschirmtest, dann der Importvertrag auch für
  `tests/akzeptanz/`.
- **B2** Elemente findet der Test über die Klassen der Komponentenseite und sichtbaren Text,
  nie über die Struktur (`nth-child`) oder eigene Test-Kennungen. Er wartet auf das Spielfeld
  und zählt erst dann: Vorher wäre „kein Modell“ grundlos grün.
- **B3** Längen prüft er an den Attributen in Zoll gegen `float(Fraction)`, exakt: JSON und
  JavaScript geben den Wert unverändert weiter. Gleichen Maßstab (QUE-2.5) prüft er an
  `getScreenCTM()`: `a == d`, `b == c == 0`. Farben vergleicht er als `getComputedStyle`
  zweier Elemente (QUE-2.6, AUF-4.6, AUF-4.7), nicht als Wert aus dem CSS.
- **B4** QUE-2.1 startet `sys.executable -m arbiter` als eigenen Prozess und öffnet die
  Adresse aus der ersten Zeile. Abdeckung dieses Prozesses: Anliegen 243.
