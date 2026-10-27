# Web: Frontend und Backend

Gilt ab dem ersten Item mit Oberfläche. Übersicht und Schichten: [Architektur](../architektur.md);
Seite: [Frontend](frontend.md), Bildschirmtests: [Tests](tests.md#bildschirmtests).

## Aufbau
- **W1** Getrennt: `arbiter/web/` liefert die Dateien aus `technik/frontend/` unverändert aus
  und beantwortet Anfragen unter `/api/` mit JSON; es erzeugt kein HTML. Das Frontend kennt
  nur diese Adressen. Gegenbeispiel `ArbiterMap/backend/app/routes/map.py`: Jinja-Vorlagen,
  40.000 Zeichen in einer Datei. Prüft: `formregeln/importvertrag.py`
  (`webVerstöße`), die Fälle nennt [Regeln](../../prozess/regeln/formregeln.md).
- **W2** `web/` ist dünn, je Modul ein Grund zur Änderung:
  - `server.py`: `serverStarten(aufstellung, port=0)` startet den Werkzeug-Server im eigenen
    Thread (W5) und gibt `Server` mit `port`, `adresse` (`adresseMitPort(port)`) und
    `beenden()` zurück; Port 0 heißt ein freier. `make_server` ohne `threaded`, denn `Aufstellung` ist
    nicht threadsicher. Den Socket bindet `socket.create_server`, `make_server` bekommt ihn
    als `fd`; bei `errno.EADDRINUSE` wirft es `AdresseBelegt(adresse)`, sonst beendete
    Werkzeug den Prozess mit englischer Meldung (Wegwerf-Versuch).
  - `anwendung.py`: Flask; Anfrage lesen, eine Handlung der Domäne aufrufen, Antwort schreiben.
  - `darstellung.py`: Spielstand der Domäne → JSON-fähige Werte. Den Namen „Spieler <n>“
    (AUF-4.2) bildet es aus der Kennung, die `kennungen.py` vergibt.
  - `kennungen.py`: Kennungen nach W4 ↔ *Spieler* und *Einheiten* der *Armeeliste*, für die
    Antwort wie für die Anfrage; nur hier wird gezählt.
  Flask und Werkzeug importieren nur `anwendung.py` und `server.py`.
  Regeln und Rechnen stehen nur in der Domäne: Längen in Zoll liefern `messen.py` und
  `Ausgangslage.grenzenDerZone`, `web/` wandelt `Fraction` nur für die Antwort in `float`. `web/` liest
  Properties und Abfragen (D3), nie `_`-Felder, die Ausgangslage über `Aufstellung.ausgangslage`.
  Prüft: Akzeptanztests zu QUE-2 und AUF-4; „nur `anwendung.py` und `server.py`“
  `formregeln/importvertrag.py`; „nie `_`-Felder“ wie D3; der Rest nur Text; Auslöser:
  zweite Route.
- **W3** Eine Anfrage je Handlung. Eine Sperre wird HTTP 409 mit der Liste ihrer Gründe
  (`Sperre.gründe`, Text aus `Grund`) und dem Spielstand ([V6](vertrag/querschnitt.md)). JSON tragen
  nur 200 und 409; jede andere Antwort, etwa 400 und 404, schreibt Flask als HTML, darum holt
  die Seite auf sie den Spielstand neu ([V1](vertrag/querschnitt.md)). CSRF:
  [Vertrag, V4](vertrag/querschnitt.md). Prüft: die Dienst-Tests zu AUF-12.6 und 12.7, zu AUF-10.3 gegen
  `sperre.json`.
- **W4** Spielobjekte haben in der Domäne keine Kennung (D1). `web/` vergibt sie aus der
  Reihenfolge der Ausgangslage: Spieler, Einheit, Modell, an einer Stelle (`kennungen.py`,
  W2). Prüft: wie W3.
- **W5** Der Befehl `python3 -m arbiter` (`starten()` in `arbiter/__main__.py`) lädt die
  Ausgangslage, startet den Server auf `127.0.0.1` und gibt die Adresse in der ersten Zeile
  aus (QUE-2.1): Port 8040 (`festerPort`, QUE-8.1), mit `--port <n>` ein anderer, für Tests
  (B4). `portDesBefehls(angaben)` liest `sys.argv[1:]` (`argparse`). Belegt
  (`AdresseBelegt`, QUE-8.2): kein Ausweichen, nichts auf stdout, eine Zeile auf stderr,
  Ende mit 1:
  `Die Adresse http://127.0.0.1:8040/ ist belegt. Läuft Arbiter schon? Dann spielt dort weiter oder beendet das andere Fenster mit Strg+C.`
  Nur `127.0.0.1`: zwei Spieler an einem Gerät
  (`domaene/ziel.md`). Werkzeug-Server von Flask, ohne Debug-Modus. Aus der Wurzel startet
  ihn `.venv/bin/arbiter` (`[project.scripts]` in `pyproject.toml`). Strg+C beendet den
  Befehl ohne Traceback. Prüft: die Akzeptanztests zu QUE-2.1 und QUE-8 (B4); der Eintrag in
  `pyproject.toml` und Strg+C nur Text.
- Pfade und JSON der Schnittstelle: [Vertrag](vertrag/querschnitt.md), je Phase eine Datei.
