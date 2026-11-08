# Web: das Backend über HTTP

[Übersicht](../architektur.md); was der Browser zeigt: [Frontend](frontend.md).

## Aufbau
- **W1** Getrennt: `arbiter/web/` liefert die Dateien aus `technik/frontend/` unverändert aus
  und beantwortet Anfragen unter `/api/` mit JSON; es erzeugt kein HTML. Das Frontend kennt
  nur diese Adressen. Gegenbeispiel `ArbiterMap/backend/app/routes/map.py`: Jinja-Vorlagen,
  40.000 Zeichen in einer Datei. Prüft: `formregeln/importvertrag.py`
  (`webVerstöße`), die Fälle nennt [Regeln](../../prozess/regeln/formregeln.md).
- **W2** `web/` ist dünn, je Modul ein Grund zur Änderung:
  - `server.py`: startet den Server im eigenen Thread, eine Anfrage nach der anderen
    (`Aufstellung` ist nicht threadsicher); eine belegte Adresse wird `AdresseBelegt` (W5).
  - `anwendung.py`: Flask; Anfrage lesen, eine Handlung der Domäne aufrufen, Antwort schreiben.
  - `darstellung.py`: Spielstand der Domäne → JSON-fähige Werte.
  - `kennungen.py`: Kennungen nach W4.

  Flask und Werkzeug importieren nur `anwendung.py` und `server.py`. Regeln und Rechnen stehen
  nur in der Domäne (`messen.py`, `Ausgangslage.grenzenDerZone`); `web/` liefert Formen und
  *Abstände* in *Zoll*, keine Zeichnung, wandelt `Fraction` nur für die Antwort in `float` und
  liest die Domäne nur über ihre Abfragen (D3). Prüft: Akzeptanztests zu QUE-2 und AUF-4; die
  Importe `formregeln/importvertrag.py`; der Rest nur Text; Auslöser: zweite Route.
- **W3** Eine Anfrage je Handlung. Eine Sperre wird HTTP 409 mit der Liste ihrer Gründe
  (`Sperre.gründe`, Text aus `Grund`) und dem Spielstand ([V6](vertrag/querschnitt/anfragen.md)). JSON
  tragen nur 200 und 409; jede andere Antwort, etwa 400 und 404, schreibt Flask als HTML,
  darum holt die Seite auf sie den Spielstand neu (V1). CSRF: V4. Prüft: die Dienst-Tests zu
  AUF-12.6 und 12.7, zu AUF-10.3 gegen `sperre.json`.
- **W4** Spielobjekte haben in der Domäne keine Kennung (D1). `web/` vergibt sie nur in
  `kennungen.py`, aus der Reihenfolge der Ausgangslage: Spieler, Einheit, Modell; für die
  Antwort wie für die Anfrage. Prüft: wie W3.
- **W5** Der Befehl `python3 -m arbiter` (`arbiter/__main__.py`) lädt die Ausgangslage,
  startet den Server und gibt seine Adresse in der ersten Zeile aus (QUE-2.1): Port 8040
  (QUE-8.1), mit `--port <n>` ein anderer (B4). Ist die Adresse belegt, weicht er nicht aus,
  meldet es auf stderr und endet mit 1 (QUE-8.2). Nur `127.0.0.1` (zwei Spieler an einem
  Gerät, `domaene/ziel.md`), ohne Debug-Modus. Aus der Wurzel startet ihn `.venv/bin/arbiter`
  (`[project.scripts]`); Strg+C beendet ohne Traceback. Prüft: die Akzeptanztests zu QUE-2.1
  und QUE-8 (B4); der Eintrag in `pyproject.toml` und Strg+C nur Text.
