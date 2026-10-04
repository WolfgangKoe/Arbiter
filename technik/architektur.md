# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“ heißt: noch ohne Mechanismus; der Auslöser steht
dabei, danach baut der Regelumsetzer ihn auf Anliegen des Architekten.

## Schichten
```
technik/
  arbiter/
    domaene/    Fachlogik, nur Standardbibliothek
    katalog/    liest das YAML aus domaene/daten/ in Objekte der Domäne
    speicher/   Datenbank: die Folge der Handlungen
    web/        Flask; übersetzt Anfragen in Handlungen der Domäne
  frontend/     HTML, CSS, JS; spricht nur über HTTP mit web/
  tests/        akzeptanz/, einheit/
```
Ein Ordner entsteht mit dem ersten Item, das ihn braucht. Zusammenspiel von `web/` und
`frontend/`: [Web](architektur/web.md); die Datenbank: [Speicher](architektur/speicher.md).

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `formregeln/importvertrag.py`, auch relative Importe.
- **A2** `web` und `katalog` kennen die Domäne, nie umgekehrt; `speicher/` kennt weder sie
  noch `web/`, `web/` verdrahtet beide (P1). Prüft: wie A1.
- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, `katalog/` liest sie
  (`yaml.safe_load`). Der Spielstand ist die Folge der Handlungen in der Datenbank (P2).
  Prüft: nur Text; Auslöser: erstes Modul in `speicher/`.

## Grundschnitt der Domäne
`arbiter/domaene/` gliedert sich wie `domaene/anforderungen/`:
- `spielobjekte.py`: `Spieler`, `Armee`, `Einheit`, `Modell`, `Base`, `Spielfeld`, `Stelle`
  und was mehr als eine Phase braucht.
- `phasen/<phase>.py` heißt wie die Anforderungsdatei. Was eine Phase einführt, liegt dort,
  bis eine zweite Phase es braucht; dann zieht es nach `spielobjekte.py`. Darum liegt
  `Ausgangslage` in `phasen/aufstellen.py`.
- `querschnitt.py`: was nach `querschnitt.md` in jeder Phase gilt, zuerst QUE-1.2.
- `sperre.py`: `Sperre` und `Grund`; Übergehen und Protokoll gelten für alle Phasen.
- `messen.py`: die Messungen (M1).
- `spielablauf/` nur unter `tests/akzeptanz/`: Szenarien über mehrere Phasen.

Ein Modul wird zum Paket, ohne dass sich ein Import ändert. Prüft: die Importe der
Akzeptanztests; Spiegel im Code: nur Text (DoD 2).

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen; `web/`
  übersetzt in `Fraction`. Mit `float` überdecken sich zwei berührende Boyz, das Raster in
  `ArbiterMap/backend/app/domain/geometry.py` rundet 16 mm auf 0,63″.
  Prüft: die Grenzfälle der Akzeptanztests.

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Werte
  (`Stelle`, `Base`) nach Inhalt. Prüft: Akzeptanztests (gleiche Armeen, `stelle(…) == stelle`).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; so kann ein
  Übergehen die Prüfung überspringen und protokollieren. Prüft: je Handlung und Grund ein
  Akzeptanztest auf den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen. Spielobjekte sind `frozen`, Sammlungen Tupel oder
  `MappingProxyType`. Den Zustand einer Phase hält die Phase in `_`-Feldern, lesbar über
  Properties ohne Setter oder Abfragen (`aufstellung.gesetzt(modell)`); sonst umginge
  `modell.gesetzt = True` jede Sperre. Prüft: Python wirft bei der Zuweisung; der Rest nur
  Text; Auslöser: `web/`, dann eine Prüfung „nur `_`-Felder zuweisen, Dataclasses `frozen`“.
- **D4** Gründe, die zusammen gelten (AUF-3.5), stehen in einer Tabelle Grund → benannte
  Prüfung (`Aufstellung._prüfungen`); die Handlung sammelt ein, ein neuer Grund ist eine
  Zeile, keine geänderte Funktion; ein ausschließender Grund (AUF-3.6) bleibt Wächter.
  Vorbild: `check_rules` in `ArbiterMap/backend/app/domain/rule_checks.py`. Prüft: nur
  Text; Auslöser: zweite Tabelle.
- **M1** Phasen messen nur über drei Messungen in `messen.py`: zwei *Bases* *überdecken*
  sich, der *Abstand* zweier Modelle ist höchstens eine Zahl, eine *Base* liegt *ganz in*
  einer Fläche. Die Baseform kennt nur `messen.py`. Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann ein Vertragstest je Baseform und ein Importvertrag „`phasen`
  importiert keine Baseform“.

## Tests
- **T1** Je Anforderung eine Testdatei im Ordner der Anforderungsdatei: AUF-1 in
  `domaene/anforderungen/phasen/aufstellen.md` → `tests/akzeptanz/phasen/aufstellen/auf1Test.py`.
  Für die erste Anforderung einer Datei genügt die Sammeldatei (`querschnittTest.py`), bis
  ein offenes Item eine zweite nennt. Höchstmaß: `prozess/kennzahlen.md`; darüber wird
  die Anforderung geteilt, nicht der Test. Prüft: `kriterienregeln/rueckverfolgung.py`,
  `formregeln/benennung.py`, `formregeln/hoechstmassTest.py`.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen (`AUF-1.4`,
  `testAuf1_4…`). Spur:
  `python3 prozess/pruefungen/gemeinsam/lauf.py kriterienregeln.rueckverfolgung AUF-1.4`.
- `tests/einheit/` spiegelt `arbiter/`, etwa `tests/einheit/domaene/phasen/aufstellenTest.py`.
  Jeder Ordner dort hat eine `__init__.py`; sonst kollidiert der Dateiname mit dem
  Akzeptanztest. Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über `pythonpath` in `pyproject.toml` im Pfad, ohne `sys.path`-Eingriff.
  Prüft: `formregeln/konfigurationTest.py`.

## Oberfläche
Design-System, Komponentenseite und Bildschirmtests: [Web](architektur/web.md#oberfläche).
