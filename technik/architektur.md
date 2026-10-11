# Architektur

Jede Regel nennt, was sie prüft. „Nur Text“: ohne Mechanismus; ein Auslöser dabei: Danach
baut ihn der Regelumsetzer auf Anliegen des Architekten.

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
Ordner entstehen mit dem ersten Item, das sie braucht. Zusammenspiel von `web/` und
`frontend/`: [Web](architektur/web.md), [Vertrag](architektur/vertrag.md); die Datenbank:
[Speicher](architektur/speicher.md).

## Abhängigkeiten zeigen nach innen
- **A1** `arbiter.domaene` importiert nur die Standardbibliothek und sich selbst. Prüft:
  `formregeln/importvertrag.py`, auch relative Importe.
- **A2** `web` und `katalog` kennen die Domäne, nie umgekehrt; `speicher/` kennt weder sie
  noch `web/`, `web/` verdrahtet beide (P1). Prüft: wie A1.
- **A3** Katalogdaten stehen nur als YAML in `domaene/daten/`, `katalog/` liest sie
  (`yaml.safe_load`). Prüft: nur Text; Auslöser: erstes Modul in `speicher/`.

## Grundschnitt der Domäne
`arbiter/domaene/` spiegelt `domaene/anforderungen/` (Anliegen 345):
- Ein Ordner der Anforderungen ist ein Modul (`spielobjekte.py`), ein Paket
  (`phasen/aufstellen/__init__.py`), sobald eine seiner Anforderungen ein Modul hat. Darin
  liegt, was mehrere seiner Anforderungen brauchen: `Aufstellung`, die eine Tür zum Stand der
  Phase, oder die Spielobjekte.
- Eine Anforderung mit eigenen Regeln der Domäne wird ein gleichnamiges Modul:
  `phasen/aufstellen/auswahl.md` → `phasen/aufstellen/auswahl.py` (`Auswahl`),
  `missionsvorbereitung/ausgangslage.py` (`Ausgangslage`, `Aufstellungszone`). Anzeige und
  Bedienung (`karte.md`) liegen in `web/` und `frontend/`.
- Ohne Anforderung nur die Werkzeuge `sperre.py` (`Sperre`, `Grund`) und `messen.py` (M1).

Wird ein Modul zum Paket, bleiben die Importe dessen, was im Ordnermodul bleibt. Prüft:
kein Modul ohne Spiegel `formregeln/spiegel.py`; was wohin gehört der Reviewer.

## Stelle und Rechnen
- **S1** Eine *Stelle* ist der Mittelpunkt der *Base*, `Stelle(x, y)` in Zoll, Ursprung in
  einer Ecke des Spielfelds; x läuft entlang der ersten Seitenlänge aus `onlyWar.yaml` (44″),
  y entlang der zweiten (60″). Die erste *Aufstellungszone* liegt an der Kante x = 0, die
  zweite an x = 44. Prüft: die Fixture `zone`.
- **S2** Gerechnet wird exakt mit `fractions.Fraction`, ohne Toleranz und ohne Wurzel:
  Durchmesser in ganzen mm, 1″ = 254/10 mm, Abstände als Quadrate verglichen; `web/`
  übersetzt in `Fraction`. Mit `float` überdecken sich zwei berührende Boyz.
  Prüft: die Grenzfälle der Akzeptanztests.

## Regeln im Domänencode
- **D1** Spielobjekte haben Identität: Vergleich mit `is`, `@dataclass(eq=False)`. Werte
  (`Stelle`, `Base`) nach Inhalt. Prüft: Akzeptanztests (gleiche Armeen, gleiche Stellen).
- **D2** Eine Handlung prüft erst alle Sperren, dann ändert sie den Zustand; so überspringt
  ein Übergehen die Prüfung und protokolliert. Prüft: je Handlung und Grund ein
  Akzeptanztest auf den unveränderten Zustand.
- **D3** Zustand ändern nur Handlungen und das Auswählen ([Vertrag, V3](architektur/vertrag.md)).
  Spielobjekte sind `frozen`, Sammlungen Tupel oder `MappingProxyType`. Die Phase hält ihren
  Zustand in `_`-Feldern, lesbar über Properties ohne Setter oder Abfragen
  (`aufstellung.gesetzt(modell)`); `modell.gesetzt = True` umginge jede Sperre. `web/` und `katalog/` lesen keine `_`-Felder; `web/`
  ändert Attribute nur an `self`, nie per `object.__setattr__`, das `frozen` umgeht.
  Prüft: Python wirft bei der Zuweisung; der Rest nur Text.
- **D4** Gründe, die zusammen gelten (AUF-3.5, 10.2 und 10.3), stehen in einer Tabelle
  Grund → Prüfung im Modul ihrer Anforderung (`sperrenBeimSetzen.py`, `beenden.py`); die
  Handlung sammelt ein, ein neuer Grund ist eine Zeile; ein ausschließender Grund (AUF-3.8)
  bleibt Wächter. Vorbild: `check_rules` in ArbiterMap (`domain/rule_checks.py`). Prüft:
  `formregeln/gruendeTabellen.py` ([Regeln](../prozess/regeln.md#formregeln)).
- **M1** Phasen messen nur über drei Messungen in `messen.py`: zwei *Bases* *überdecken*
  sich, der *Abstand* zweier Modelle ist höchstens eine Zahl, eine *Base* liegt *ganz in*
  einer Fläche. In der Domäne kennt die Baseform nur `messen.py`. Prüft: nur Text; Auslöser: zweite
  Baseform (Etappe 6), dann je Baseform ein Vertragstest.

## Tests
- **T1** Spiegel: `domaene/anforderungen/<pfad>/<name>.md` → `tests/akzeptanz/<pfad>/<name>Test.py`,
  daneben nur Hilfsmodule (`handgriffe.py`). Die Testdatei übernimmt von ihrer Anforderung
  (1) die Überschrift als Docstring (`"""AUF-7 · Einheit in Aufstellung."""`), (2) nur deren
  Kriterien (`testAuf7_<m>…`), (3) deren Reihenfolge: die Tests eines Kriteriums beisammen,
  in der Folge der Kriterien, (4) Gegeben, wenn, dann als Aufbau, Handlung, Prüfung, durch
  Leerzeilen getrennt; ohne **wenn** keine Handlung. Über dem Höchstmaß
  (`prozess/kennzahlen.md`) wird die Anforderung geteilt. Prüft: der Ort
  `formregeln/benennung.py`, 1 bis 3 `formregeln/spiegel.py`; 4 Kritik am Code; Höchstmaß
  nur Text.
- **T2** Der Weg vom Kriterium zum Test und zurück wird berechnet, nicht gespeichert: keine
  Links in Anforderung oder Test, die Zuordnung steht nur im Namen (`AUF-7.3`,
  `testAuf7_3…`). Spur: [Regeln](../prozess/regeln.md).
- `tests/einheit/` spiegelt `arbiter/`, etwa `tests/einheit/domaene/phasen/aufstellenTest.py`.
  Jeder Ordner dort hat `__init__.py`, sonst kollidieren Dateinamen mit Akzeptanztests.
  Prüft: `pytest technik/tests` bricht ab.
- `arbiter` liegt über `pythonpath` (`pyproject.toml`) im Pfad, ohne `sys.path`. Prüft: nur Text.

## Oberfläche
Design-System, Komponentenseite, Leisten: [Oberfläche](architektur/oberflaeche.md);
Bildschirmtests: [Web](architektur/web.md#bildschirmtests).
