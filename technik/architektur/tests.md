# Tests: Akzeptanztests, Einheitstests, Bildschirmtests

Übersicht und Schichten: [Architektur](../architektur.md).

## Aufbau
- **T1** Spiegel: `domaene/anforderungen/<pfad>/<name>.md` → `tests/akzeptanz/<pfad>/<name>Test.py`,
  daneben nur Hilfsmodule (`handgriffe.py`). Die Testdatei übernimmt von ihrer Anforderung
  (1) die Überschrift als Docstring (`"""AUF-7 · Einheit in Aufstellung."""`), (2) nur deren
  Kriterien (`testAuf7_<m>…`), (3) deren Reihenfolge: die Tests eines Kriteriums beisammen,
  in der Folge der Kriterien, (4) Gegeben, wenn, dann als Aufbau, Handlung, Prüfung, durch
  Leerzeilen getrennt; ohne **wenn** keine Handlung. Prüft: der Ort
  `formregeln/benennung.py`, 1 bis 3 `formregeln/spiegel.py`; 4 Kritik am Code.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen (`AUF-7.3`,
  `testAuf7_3…`). Spur: [Regeln](../../prozess/regeln/kriterienregeln.md).
- `tests/einheit/` spiegelt `arbiter/`. Jeder Ordner dort hat `__init__.py`, sonst
  kollidieren Dateinamen mit Akzeptanztests. Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über `pythonpath` (`pyproject.toml`) im Pfad, ohne `sys.path`. Prüft: nur Text.

## Bildschirmtests
- **B1** Ein Bildschirmtest steht bei den Akzeptanztests seiner Anforderung (T1). Er baut den
  Zustand mit Handlungen der Domäne, startet mit ihm `serverStarten` ([W2](web.md#aufbau)) im
  selben Prozess und liest die Seite mit Playwright, Browser je Sitzung, Seite je Test als
  Fixture in `conftest.py`. Kein Akzeptanztest importiert `flask` oder `werkzeug`.
  `Aufstellung.modellSetzen(modell, stelle)`, ohne Route, *setzt* nach QUE-1.1 bis 1.3 und
  AUF-7.2, 7.3 genau an die *Stelle*, ohne Hineinrücken und Anhalten. Warum: Tests bauen
  damit die Vorgeschichte an genauen *Stellen*; eine falsche scheitert, statt verschoben zu
  stehen. Prüft:
  `formregeln/importvertrag.py` (`akzeptanzVerstöße`).
- **B2** Elemente findet der Test über die Klassen der Komponentenseite und sichtbaren Text,
  nie über die Struktur (`nth-child`) oder eigene Test-Kennungen. Er wartet auf das Spielfeld
  und zählt erst dann: Vorher wäre „kein Modell“ grundlos grün. Jede Seite wartet höchstens
  5 s (`set_default_timeout`); länger heißt, der Server antwortet nicht.
- **B3** Längen prüft er an den Attributen in Zoll gegen `float(Fraction)`, exakt: JSON und
  JavaScript geben den Wert unverändert weiter. Was er in Pixeln misst
  (`getBoundingClientRect`, Bruchteile von Pixeln), gilt relativ auf 1e-4. Gleichen Maßstab (QUE-2.5) prüft er an
  `getScreenCTM()`: `a == d`, `b == c == 0`. Farben vergleicht er als `getComputedStyle`
  zweier Elemente (QUE-2.6, AUF-4.6, AUF-4.7), nicht als Wert aus dem CSS.
- **B4** QUE-2.1 startet `sys.executable -m arbiter --port 0` als eigenen Prozess und öffnet die
  Adresse aus der ersten Zeile, mit `PYTHONUNBUFFERED=1` wie an einem Terminal, sonst käme
  die erste Zeile in der Pipe zu spät; die Abdeckung misst coverage im Kindprozess
  (`[tool.coverage.run]`, `formregeln/abdeckung.py`). Kein Test belegt 8040, dort läuft
  vielleicht eine Partie (1650): QUE-8.1 prüft `adresseMitPort(portDesBefehls([]))`, QUE-8.2
  startet einen zweiten Befehl mit dem Port des ersten (Ende mit 1, stderr wie
  [W5](web.md#aufbau)).
- **B5** Ziehen: mit der Maus über `page.mouse` (drücken, `move` mit `steps`, loslassen), mit
  dem Finger über CDP `Input.dispatchTouchEvent` in einem Kontext mit `has_touch` (Anliegen
  372). Den Punkt rechnet der Test aus Zoll über `getScreenCTM()` der `.karte`; die *Stelle*
  danach gilt auf einen Pixel genau (`1 / a` Zoll), denn der Zeiger kennt nur Pixel. Exakt
  prüfen die Domänentests (S2).
